"""Storage layer for benchmark metrics using SQLite."""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any
from contextlib import contextmanager

from .models import BenchmarkResult, MetricData, BenchmarkStats


class MetricsStorage:
    """SQLite-based storage for benchmark metrics."""

    def __init__(self, db_path: str = "benchmark_metrics.db"):
        """Initialize storage with database path."""
        self.db_path = Path(db_path)
        self._init_db()

    def _init_db(self):
        """Initialize database schema."""
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS benchmark_runs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run_id TEXT UNIQUE NOT NULL,
                    protocol TEXT NOT NULL,
                    timestamp DATETIME NOT NULL,
                    stats_json TEXT,
                    metadata_json TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run_id TEXT NOT NULL,
                    request_id INTEGER NOT NULL,
                    request_timestamp TEXT NOT NULL,
                    response_timestamp TEXT NOT NULL,
                    latency_seconds REAL NOT NULL,
                    FOREIGN KEY (run_id) REFERENCES benchmark_runs(run_id)
                )
            """)

            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_run_id
                ON metrics(run_id)
            """)

            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_protocol
                ON benchmark_runs(protocol)
            """)

            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_timestamp
                ON benchmark_runs(timestamp)
            """)

            conn.commit()

    @contextmanager
    def _get_connection(self):
        """Get database connection context manager."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def save_benchmark(self, result: BenchmarkResult) -> int:
        """Save benchmark result to database."""
        with self._get_connection() as conn:
            # Insert benchmark run
            cursor = conn.execute("""
                INSERT INTO benchmark_runs
                (run_id, protocol, timestamp, stats_json, metadata_json)
                VALUES (?, ?, ?, ?, ?)
            """, (
                result.run_id,
                result.protocol,
                result.timestamp.isoformat(),
                json.dumps(result.stats.dict() if result.stats else None),
                json.dumps(result.metadata)
            ))

            benchmark_id = cursor.lastrowid

            # Insert metrics
            if result.metrics:
                metrics_data = [
                    (
                        result.run_id,
                        m.request_id,
                        m.request_timestamp,
                        m.response_timestamp,
                        m.latency_seconds
                    )
                    for m in result.metrics
                ]

                conn.executemany("""
                    INSERT INTO metrics
                    (run_id, request_id, request_timestamp,
                     response_timestamp, latency_seconds)
                    VALUES (?, ?, ?, ?, ?)
                """, metrics_data)

            conn.commit()
            return benchmark_id

    def get_benchmark(self, run_id: str) -> Optional[BenchmarkResult]:
        """Retrieve benchmark by run_id."""
        with self._get_connection() as conn:
            row = conn.execute("""
                SELECT * FROM benchmark_runs WHERE run_id = ?
            """, (run_id,)).fetchone()

            if not row:
                return None

            # Get metrics
            metrics_rows = conn.execute("""
                SELECT * FROM metrics WHERE run_id = ? ORDER BY request_id
            """, (run_id,)).fetchall()

            metrics = [
                MetricData(
                    request_id=m['request_id'],
                    request_timestamp=m['request_timestamp'],
                    response_timestamp=m['response_timestamp'],
                    latency_seconds=m['latency_seconds']
                )
                for m in metrics_rows
            ]

            stats_data = json.loads(row['stats_json']) if row['stats_json'] else None
            stats = BenchmarkStats(**stats_data) if stats_data else None

            return BenchmarkResult(
                id=row['id'],
                run_id=row['run_id'],
                protocol=row['protocol'],
                timestamp=datetime.fromisoformat(row['timestamp']),
                metrics=metrics,
                stats=stats,
                metadata=json.loads(row['metadata_json'])
            )

    def get_all_runs(
        self,
        protocol: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """Get all benchmark runs with optional filtering."""
        with self._get_connection() as conn:
            query = """
                SELECT id, run_id, protocol, timestamp, stats_json, metadata_json
                FROM benchmark_runs
            """
            params = []

            if protocol:
                query += " WHERE protocol = ?"
                params.append(protocol)

            query += " ORDER BY timestamp DESC LIMIT ? OFFSET ?"
            params.extend([limit, offset])

            rows = conn.execute(query, params).fetchall()

            return [
                {
                    'id': row['id'],
                    'run_id': row['run_id'],
                    'protocol': row['protocol'],
                    'timestamp': row['timestamp'],
                    'stats': json.loads(row['stats_json']) if row['stats_json'] else None,
                    'metadata': json.loads(row['metadata_json'])
                }
                for row in rows
            ]

    def get_latest_by_protocol(self) -> Dict[str, BenchmarkResult]:
        """Get latest benchmark for each protocol."""
        with self._get_connection() as conn:
            rows = conn.execute("""
                SELECT * FROM benchmark_runs
                WHERE id IN (
                    SELECT MAX(id) FROM benchmark_runs GROUP BY protocol
                )
            """).fetchall()

            results = {}
            for row in rows:
                result = self.get_benchmark(row['run_id'])
                if result:
                    results[result.protocol] = result

            return results

    def delete_run(self, run_id: str) -> bool:
        """Delete a benchmark run and its metrics."""
        with self._get_connection() as conn:
            conn.execute("DELETE FROM metrics WHERE run_id = ?", (run_id,))
            cursor = conn.execute(
                "DELETE FROM benchmark_runs WHERE run_id = ?",
                (run_id,)
            )
            conn.commit()
            return cursor.rowcount > 0

    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics."""
        with self._get_connection() as conn:
            total_runs = conn.execute(
                "SELECT COUNT(*) as count FROM benchmark_runs"
            ).fetchone()['count']

            total_metrics = conn.execute(
                "SELECT COUNT(*) as count FROM metrics"
            ).fetchone()['count']

            protocols = conn.execute("""
                SELECT protocol, COUNT(*) as count
                FROM benchmark_runs
                GROUP BY protocol
            """).fetchall()

            return {
                'total_runs': total_runs,
                'total_metrics': total_metrics,
                'protocols': {p['protocol']: p['count'] for p in protocols}
            }

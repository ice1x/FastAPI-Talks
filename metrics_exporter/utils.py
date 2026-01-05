"""Utility functions for metrics processing and conversion."""

import json
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path
import numpy as np

from .models import BenchmarkResult, MetricData, BenchmarkStats


def calculate_statistics(latencies: List[float]) -> BenchmarkStats:
    """Calculate statistical metrics from latency data."""
    if not latencies:
        return BenchmarkStats(
            mean=0, median=0, std_dev=0,
            min=0, max=0, count=0
        )

    latencies_array = np.array(latencies)

    return BenchmarkStats(
        mean=float(np.mean(latencies_array)),
        median=float(np.median(latencies_array)),
        std_dev=float(np.std(latencies_array)),
        min=float(np.min(latencies_array)),
        max=float(np.max(latencies_array)),
        count=len(latencies),
        p50=float(np.percentile(latencies_array, 50)),
        p95=float(np.percentile(latencies_array, 95)),
        p99=float(np.percentile(latencies_array, 99))
    )


def parse_legacy_grpc(data: List[Dict[str, Any]]) -> BenchmarkResult:
    """Parse gRPC legacy format from grpc_out.txt."""
    metrics = []

    for idx, item in enumerate(data):
        req_ts = item.get('grpc_requester_timestamp', '')
        resp_ts = item.get('grpc_responder_timestamp', '')

        if req_ts and resp_ts:
            req_dt = datetime.fromisoformat(req_ts.replace('Z', '+00:00'))
            resp_dt = datetime.fromisoformat(resp_ts.replace('Z', '+00:00'))
            latency = (resp_dt - req_dt).total_seconds()

            metrics.append(MetricData(
                request_id=idx,
                request_timestamp=req_ts,
                response_timestamp=resp_ts,
                latency_seconds=latency
            ))

    latencies = [m.latency_seconds for m in metrics]
    stats = calculate_statistics(latencies)

    return BenchmarkResult(
        run_id=f"grpc_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
        protocol="gRPC",
        timestamp=datetime.utcnow(),
        metrics=metrics,
        stats=stats
    )


def parse_legacy_rest(data: List[Dict[str, Any]]) -> BenchmarkResult:
    """Parse REST legacy format from rest_out.txt."""
    metrics = []

    for idx, item in enumerate(data):
        req_ts = item.get('request_timestamp', '')
        resp_ts = item.get('response_timestamp', '')

        if req_ts and resp_ts:
            req_dt = datetime.fromisoformat(req_ts.replace('Z', '+00:00'))
            resp_dt = datetime.fromisoformat(resp_ts.replace('Z', '+00:00'))
            latency = (resp_dt - req_dt).total_seconds()

            metrics.append(MetricData(
                request_id=idx,
                request_timestamp=req_ts,
                response_timestamp=resp_ts,
                latency_seconds=latency
            ))

    latencies = [m.latency_seconds for m in metrics]
    stats = calculate_statistics(latencies)

    return BenchmarkResult(
        run_id=f"rest_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
        protocol="REST",
        timestamp=datetime.utcnow(),
        metrics=metrics,
        stats=stats
    )


def parse_legacy_socketio(data: Dict[str, Any]) -> BenchmarkResult:
    """Parse Socket.IO legacy format from sio_out.txt."""
    metrics = []
    request_ts = data.get('request_ts', '')
    response_timestamps = data.get('respond_ts', [])

    for idx, resp_ts in enumerate(response_timestamps):
        if request_ts and resp_ts:
            req_dt = datetime.fromisoformat(request_ts.replace('Z', '+00:00'))
            resp_dt = datetime.fromisoformat(resp_ts.replace('Z', '+00:00'))
            latency = (resp_dt - req_dt).total_seconds()

            metrics.append(MetricData(
                request_id=idx,
                request_timestamp=request_ts,
                response_timestamp=resp_ts,
                latency_seconds=latency
            ))

    latencies = [m.latency_seconds for m in metrics]
    stats = calculate_statistics(latencies)

    return BenchmarkResult(
        run_id=f"socketio_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
        protocol="Socket.IO",
        timestamp=datetime.utcnow(),
        metrics=metrics,
        stats=stats
    )


def parse_legacy_graphql(data: List[Dict[str, Any]]) -> BenchmarkResult:
    """Parse GraphQL legacy format from graphql_out.txt."""
    metrics = []

    for idx, item in enumerate(data):
        req_ts = item.get('requestTimestamp', '')
        resp_ts = item.get('responseTimestamp', '')

        if req_ts and resp_ts:
            req_dt = datetime.fromisoformat(req_ts.replace('Z', '+00:00'))
            resp_dt = datetime.fromisoformat(resp_ts.replace('Z', '+00:00'))
            latency = (resp_dt - req_dt).total_seconds()

            metrics.append(MetricData(
                request_id=idx,
                request_timestamp=req_ts,
                response_timestamp=resp_ts,
                latency_seconds=latency
            ))

    latencies = [m.latency_seconds for m in metrics]
    stats = calculate_statistics(latencies)

    return BenchmarkResult(
        run_id=f"graphql_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
        protocol="GraphQL",
        timestamp=datetime.utcnow(),
        metrics=metrics,
        stats=stats
    )


def parse_legacy_avro(data: List[Dict[str, Any]]) -> BenchmarkResult:
    """Parse AVRO legacy format from avro_out.txt."""
    metrics = []

    for idx, item in enumerate(data):
        req_ts = item.get('request_timestamp', '')
        resp_ts = item.get('response_timestamp', '')

        if req_ts and resp_ts:
            req_dt = datetime.fromisoformat(req_ts.replace('Z', '+00:00'))
            resp_dt = datetime.fromisoformat(resp_ts.replace('Z', '+00:00'))
            latency = (resp_dt - req_dt).total_seconds()

            metrics.append(MetricData(
                request_id=idx,
                request_timestamp=req_ts,
                response_timestamp=resp_ts,
                latency_seconds=latency
            ))

    latencies = [m.latency_seconds for m in metrics]
    stats = calculate_statistics(latencies)

    return BenchmarkResult(
        run_id=f"avro_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
        protocol="AVRO",
        timestamp=datetime.utcnow(),
        metrics=metrics,
        stats=stats
    )


def parse_legacy_cbor(data: List[Dict[str, Any]]) -> BenchmarkResult:
    """Parse CBOR legacy format from cbor_out.txt."""
    metrics = []

    for idx, item in enumerate(data):
        req_ts = item.get('request_timestamp', '')
        resp_ts = item.get('response_timestamp', '')

        if req_ts and resp_ts:
            req_dt = datetime.fromisoformat(req_ts.replace('Z', '+00:00'))
            resp_dt = datetime.fromisoformat(resp_ts.replace('Z', '+00:00'))
            latency = (resp_dt - req_dt).total_seconds()

            metrics.append(MetricData(
                request_id=idx,
                request_timestamp=req_ts,
                response_timestamp=resp_ts,
                latency_seconds=latency
            ))

    latencies = [m.latency_seconds for m in metrics]
    stats = calculate_statistics(latencies)

    return BenchmarkResult(
        run_id=f"cbor_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
        protocol="CBOR",
        timestamp=datetime.utcnow(),
        metrics=metrics,
        stats=stats
    )


def import_legacy_results(base_dir: str = ".") -> List[BenchmarkResult]:
    """Import all legacy benchmark results from *_out.txt files."""
    base_path = Path(base_dir)
    results = []

    parsers = {
        'grpc_out.txt': parse_legacy_grpc,
        'rest_out.txt': parse_legacy_rest,
        'sio_out.txt': parse_legacy_socketio,
        'graphql_out.txt': parse_legacy_graphql,
        'avro_out.txt': parse_legacy_avro,
        'cbor_out.txt': parse_legacy_cbor,
    }

    for filename, parser_func in parsers.items():
        filepath = base_path / filename
        if filepath.exists():
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    result = parser_func(data)
                    results.append(result)
                    print(f"✓ Imported {filename} - {len(result.metrics)} metrics")
            except Exception as e:
                print(f"✗ Error importing {filename}: {e}")

    return results

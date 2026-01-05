"""Export functionality for different formats."""

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
import pandas as pd

from .models import BenchmarkResult, BenchmarkComparison


class MetricsExporter:
    """Export benchmark metrics to various formats."""

    @staticmethod
    def to_csv(result: BenchmarkResult, output_path: str):
        """Export benchmark to CSV file."""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)

            # Write header
            writer.writerow([
                'request_id',
                'request_timestamp',
                'response_timestamp',
                'latency_seconds'
            ])

            # Write metrics
            for metric in result.metrics:
                writer.writerow([
                    metric.request_id,
                    metric.request_timestamp,
                    metric.response_timestamp,
                    metric.latency_seconds
                ])

    @staticmethod
    def to_excel(
        results: List[BenchmarkResult],
        output_path: str,
        include_stats: bool = True
    ):
        """Export benchmark results to Excel file with multiple sheets."""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            # Create a sheet for each protocol
            for result in results:
                # Metrics sheet
                if result.metrics:
                    df = pd.DataFrame([
                        {
                            'request_id': m.request_id,
                            'request_timestamp': m.request_timestamp,
                            'response_timestamp': m.response_timestamp,
                            'latency_seconds': m.latency_seconds
                        }
                        for m in result.metrics
                    ])

                    sheet_name = f"{result.protocol}_metrics"[:31]  # Excel limit
                    df.to_excel(writer, sheet_name=sheet_name, index=False)

            # Summary sheet with statistics
            if include_stats and results:
                summary_data = []
                for result in results:
                    if result.stats:
                        summary_data.append({
                            'protocol': result.protocol,
                            'run_id': result.run_id,
                            'timestamp': result.timestamp.isoformat(),
                            'mean': result.stats.mean,
                            'median': result.stats.median,
                            'std_dev': result.stats.std_dev,
                            'min': result.stats.min,
                            'max': result.stats.max,
                            'count': result.stats.count,
                            'p95': result.stats.p95,
                            'p99': result.stats.p99
                        })

                if summary_data:
                    summary_df = pd.DataFrame(summary_data)
                    summary_df.to_excel(writer, sheet_name='Summary', index=False)

    @staticmethod
    def to_json(
        result: BenchmarkResult,
        output_path: str,
        pretty: bool = True
    ):
        """Export benchmark to JSON file."""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w') as f:
            if pretty:
                json.dump(
                    result.dict(),
                    f,
                    indent=2,
                    default=str
                )
            else:
                json.dump(result.dict(), f, default=str)

    @staticmethod
    def to_html_report(
        results: List[BenchmarkResult],
        output_path: str,
        title: str = "Benchmark Report"
    ):
        """Generate HTML report with statistics and charts."""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            border-bottom: 3px solid #4CAF50;
            padding-bottom: 10px;
        }}
        .metadata {{
            background: #f9f9f9;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
        .protocol-section {{
            margin: 30px 0;
            padding: 20px;
            border-left: 4px solid #4CAF50;
            background: #fafafa;
        }}
        .protocol-section h2 {{
            margin-top: 0;
            color: #4CAF50;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background: #4CAF50;
            color: white;
            font-weight: bold;
        }}
        tr:hover {{
            background: #f5f5f5;
        }}
        .stat-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }}
        .stat-card {{
            background: white;
            padding: 15px;
            border-radius: 5px;
            border: 1px solid #e0e0e0;
        }}
        .stat-card .label {{
            color: #666;
            font-size: 0.9em;
            margin-bottom: 5px;
        }}
        .stat-card .value {{
            font-size: 1.5em;
            font-weight: bold;
            color: #333;
        }}
        .timestamp {{
            color: #666;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{title}</h1>
        <div class="metadata">
            <p class="timestamp">Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
            <p>Total Protocols Tested: {len(results)}</p>
        </div>
"""

        for result in results:
            html_content += f"""
        <div class="protocol-section">
            <h2>{result.protocol}</h2>
            <p class="timestamp">Run ID: {result.run_id}</p>
            <p class="timestamp">Timestamp: {result.timestamp.strftime('%Y-%m-%d %H:%M:%S')}</p>
"""

            if result.stats:
                html_content += """
            <div class="stat-grid">
"""
                stats_dict = {
                    'Mean': f"{result.stats.mean:.6f}s",
                    'Median': f"{result.stats.median:.6f}s",
                    'Std Dev': f"{result.stats.std_dev:.6f}s",
                    'Min': f"{result.stats.min:.6f}s",
                    'Max': f"{result.stats.max:.6f}s",
                    'Count': str(result.stats.count)
                }

                if result.stats.p95:
                    stats_dict['P95'] = f"{result.stats.p95:.6f}s"
                if result.stats.p99:
                    stats_dict['P99'] = f"{result.stats.p99:.6f}s"

                for label, value in stats_dict.items():
                    html_content += f"""
                <div class="stat-card">
                    <div class="label">{label}</div>
                    <div class="value">{value}</div>
                </div>
"""

                html_content += """
            </div>
"""

            html_content += """
        </div>
"""

        html_content += """
    </div>
</body>
</html>
"""

        with open(output_file, 'w') as f:
            f.write(html_content)

    @staticmethod
    def export_comparison(
        comparison: BenchmarkComparison,
        output_dir: str,
        formats: Optional[List[str]] = None
    ):
        """Export comparison in multiple formats."""
        if formats is None:
            formats = ['json', 'html', 'excel']

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        results = list(comparison.results.values())

        if 'json' in formats:
            MetricsExporter.to_json(
                comparison,
                output_path / f"comparison_{comparison.run_id}.json"
            )

        if 'html' in formats:
            MetricsExporter.to_html_report(
                results,
                output_path / f"comparison_{comparison.run_id}.html",
                title=f"Benchmark Comparison - {comparison.run_id}"
            )

        if 'excel' in formats:
            MetricsExporter.to_excel(
                results,
                output_path / f"comparison_{comparison.run_id}.xlsx"
            )

        if 'csv' in formats:
            for result in results:
                MetricsExporter.to_csv(
                    result,
                    output_path / f"{result.protocol}_{result.run_id}.csv"
                )

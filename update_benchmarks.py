#!/usr/bin/env python3
"""Script to integrate metrics storage with existing benchmarks."""

import json
from datetime import datetime
from pathlib import Path

from metrics_exporter import MetricsStorage, MetricsExporter
from metrics_exporter.utils import import_legacy_results


def update_benchmarks():
    """Update existing benchmark system to use new metrics storage."""
    print("=== Benchmark Metrics Integration ===\n")

    # Initialize storage
    storage = MetricsStorage()

    # Import existing results
    print("1. Importing existing benchmark results...")
    results = import_legacy_results()

    if results:
        for result in results:
            storage.save_benchmark(result)
            print(f"   ✓ {result.protocol}: {len(result.metrics)} metrics")
        print(f"\n   Total imported: {len(results)} benchmark runs\n")
    else:
        print("   No existing results found\n")

    # Export latest results
    print("2. Exporting latest results...")

    latest_results = storage.get_latest_by_protocol()

    if latest_results:
        # Export to Excel
        result_list = list(latest_results.values())
        excel_path = "exports/latest_benchmarks.xlsx"
        MetricsExporter.to_excel(result_list, excel_path)
        print(f"   ✓ Excel: {excel_path}")

        # Export to HTML report
        html_path = "exports/latest_benchmarks.html"
        MetricsExporter.to_html_report(result_list, html_path)
        print(f"   ✓ HTML: {html_path}")

        print()

    # Show statistics
    print("3. Database Statistics:")
    stats = storage.get_stats()
    print(f"   Total Runs: {stats['total_runs']}")
    print(f"   Total Metrics: {stats['total_metrics']:,}")
    print(f"   Protocols: {list(stats['protocols'].keys())}")

    print("\n=== Integration Complete ===")
    print("\nNext steps:")
    print("  1. Start dashboard: python metrics_cli.py dashboard")
    print("  2. View dashboard at: http://localhost:8888")
    print("  3. Run new benchmarks to see real-time updates")
    print("\nCLI Usage:")
    print("  python metrics_cli.py import      # Import results")
    print("  python metrics_cli.py list        # List all runs")
    print("  python metrics_cli.py stats       # Show statistics")
    print("  python metrics_cli.py export-all  # Export all latest results")


if __name__ == "__main__":
    update_benchmarks()

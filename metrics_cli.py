#!/usr/bin/env python3
"""CLI tool for managing benchmark metrics."""

import argparse
import sys
from pathlib import Path

from metrics_exporter import MetricsExporter, MetricsStorage
from metrics_exporter.utils import import_legacy_results


def main():  # noqa: C901
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Benchmark Metrics Management Tool")

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Import command
    import_parser = subparsers.add_parser("import", help="Import legacy benchmark results")
    import_parser.add_argument("--dir", default=".", help="Directory containing *_out.txt files")

    # Export command
    export_parser = subparsers.add_parser("export", help="Export benchmark results")
    export_parser.add_argument("run_id", help="Run ID to export")
    export_parser.add_argument(
        "--format", choices=["csv", "json", "html", "excel"], default="json", help="Export format"
    )
    export_parser.add_argument("--output", help="Output file path")

    # Export all command
    export_all_parser = subparsers.add_parser("export-all", help="Export all latest results")
    export_all_parser.add_argument(
        "--format", choices=["csv", "json", "html", "excel"], default="excel", help="Export format"
    )
    export_all_parser.add_argument(
        "--output", default="exports/all_benchmarks", help="Output directory"
    )

    # List command
    list_parser = subparsers.add_parser("list", help="List all benchmark runs")
    list_parser.add_argument("--protocol", help="Filter by protocol")
    list_parser.add_argument("--limit", type=int, default=20, help="Number of results to show")

    # Stats command
    subparsers.add_parser("stats", help="Show database statistics")

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a benchmark run")
    delete_parser.add_argument("run_id", help="Run ID to delete")

    # Dashboard command
    dashboard_parser = subparsers.add_parser("dashboard", help="Start web dashboard")
    dashboard_parser.add_argument("--port", type=int, default=8888, help="Port to run dashboard on")
    dashboard_parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    storage = MetricsStorage()

    # Execute commands
    if args.command == "import":
        print(f"Importing from {args.dir}...")
        results = import_legacy_results(args.dir)

        if not results:
            print("No results found to import")
            return

        for result in results:
            storage.save_benchmark(result)
            print(f"✓ Imported {result.protocol}: {len(result.metrics)} metrics")

        print(f"\nTotal imported: {len(results)} benchmark runs")

    elif args.command == "export":
        result = storage.get_benchmark(args.run_id)
        if not result:
            print(f"Error: Run {args.run_id} not found")
            sys.exit(1)

        output_path = args.output or f"exports/{args.run_id}.{args.format}"

        if args.format == "csv":
            MetricsExporter.to_csv(result, output_path)
        elif args.format == "json":
            MetricsExporter.to_json(result, output_path)
        elif args.format == "html":
            MetricsExporter.to_html_report([result], output_path)

        print(f"✓ Exported to {output_path}")

    elif args.command == "export-all":
        results = storage.get_latest_by_protocol()

        if not results:
            print("No results found to export")
            return

        result_list = list(results.values())

        if args.format == "excel":
            output_path = f"{args.output}.xlsx"
            MetricsExporter.to_excel(result_list, output_path)
            print(f"✓ Exported to {output_path}")
        elif args.format == "html":
            output_path = f"{args.output}.html"
            MetricsExporter.to_html_report(result_list, output_path)
            print(f"✓ Exported to {output_path}")
        elif args.format == "json":
            Path(args.output).mkdir(parents=True, exist_ok=True)
            for protocol, result in results.items():
                output_path = f"{args.output}/{protocol}.json"
                MetricsExporter.to_json(result, output_path)
                print(f"✓ Exported {protocol} to {output_path}")
        elif args.format == "csv":
            Path(args.output).mkdir(parents=True, exist_ok=True)
            for protocol, result in results.items():
                output_path = f"{args.output}/{protocol}.csv"
                MetricsExporter.to_csv(result, output_path)
                print(f"✓ Exported {protocol} to {output_path}")

    elif args.command == "list":
        runs = storage.get_all_runs(protocol=args.protocol, limit=args.limit)

        if not runs:
            print("No runs found")
            return

        print(f"\n{'Protocol':<12} {'Run ID':<35} {'Timestamp':<20} {'Mean':<10}")
        print("-" * 80)

        for run in runs:
            stats = run.get("stats", {})
            mean = stats.get("mean", 0) if stats else 0
            print(
                f"{run['protocol']:<12} "
                f"{run['run_id']:<35} "
                f"{run['timestamp']:<20} "
                f"{mean:.6f}s"
            )

    elif args.command == "stats":
        stats = storage.get_stats()

        print("\n=== Benchmark Database Statistics ===")
        print(f"Total Runs: {stats['total_runs']}")
        print(f"Total Metrics: {stats['total_metrics']:,}")
        print("\nRuns by Protocol:")

        for protocol, count in stats["protocols"].items():
            print(f"  {protocol}: {count}")

    elif args.command == "delete":
        success = storage.delete_run(args.run_id)

        if success:
            print(f"✓ Deleted run {args.run_id}")
        else:
            print(f"Error: Run {args.run_id} not found")
            sys.exit(1)

    elif args.command == "dashboard":
        print(f"Starting dashboard on http://{args.host}:{args.port}")
        print("Press Ctrl+C to stop")

        import uvicorn

        from dashboard.main import app

        uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()

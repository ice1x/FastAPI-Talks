# Benchmark Metrics Dashboard

Unified metrics export and web dashboard for viewing benchmark results.

## Features

### 📊 Unified Metrics Export
- **Multiple formats**: CSV, JSON, Excel (XLSX), HTML
- **Statistical analysis**: Mean, median, std dev, percentiles (P50, P95, P99)
- **Historical tracking**: SQLite database for storing all benchmark runs
- **Protocol support**: REST, gRPC, Socket.IO, GraphQL, AVRO, CBOR

### 🌐 Web Dashboard
- **Real-time visualization**: Interactive charts using Chart.js
- **Protocol comparison**: Side-by-side performance analysis
- **Run history**: Browse and filter all benchmark runs
- **Detailed views**: Individual run analysis with latency distributions
- **Export from UI**: Download results directly from the dashboard

## Installation

Install additional dependencies:

```bash
pip install -r requirements.txt
```

## Quick Start

### 1. Import Existing Results

Import legacy benchmark results from `*_out.txt` files:

```bash
python update_benchmarks.py
```

Or manually:

```bash
python metrics_cli.py import
```

### 2. Start Dashboard

```bash
python metrics_cli.py dashboard
```

Then open your browser to: **http://localhost:8888**

### 3. Run Benchmarks

Run your benchmarks as usual with `run_benchmarks.py`. The results will be automatically saved to `*_out.txt` files, which you can import using:

```bash
python metrics_cli.py import
```

## CLI Usage

### Import Results

```bash
# Import from current directory
python metrics_cli.py import

# Import from specific directory
python metrics_cli.py import --dir /path/to/results
```

### List Runs

```bash
# List all runs
python metrics_cli.py list

# Filter by protocol
python metrics_cli.py list --protocol gRPC

# Limit results
python metrics_cli.py list --limit 10
```

### View Statistics

```bash
python metrics_cli.py stats
```

Example output:
```
=== Benchmark Database Statistics ===
Total Runs: 6
Total Metrics: 6,000

Runs by Protocol:
  REST: 1
  gRPC: 1
  Socket.IO: 1
  GraphQL: 1
  AVRO: 1
  CBOR: 1
```

### Export Results

#### Export Single Run

```bash
# Export to JSON
python metrics_cli.py export <run_id> --format json

# Export to CSV
python metrics_cli.py export <run_id> --format csv --output results.csv

# Export to HTML
python metrics_cli.py export <run_id> --format html
```

#### Export All Latest Results

```bash
# Export to Excel (recommended)
python metrics_cli.py export-all --format excel --output exports/all_benchmarks

# Export to HTML report
python metrics_cli.py export-all --format html --output exports/report

# Export to individual CSV files
python metrics_cli.py export-all --format csv --output exports/csv
```

### Delete Runs

```bash
python metrics_cli.py delete <run_id>
```

### Start Dashboard

```bash
# Default port (8888)
python metrics_cli.py dashboard

# Custom port
python metrics_cli.py dashboard --port 9000

# Custom host
python metrics_cli.py dashboard --host 127.0.0.1 --port 9000
```

## Dashboard Features

### Main View

- **Statistics Cards**: Total runs, total metrics, protocol count
- **Comparison Chart**: Bar chart comparing mean/median latency across protocols
- **Distribution Chart**: Line chart showing latency distribution (min, P50, mean, P95, P99, max)
- **Runs Table**: Searchable/filterable table of all benchmark runs

### Actions

- **Import Legacy Results**: Import existing `*_out.txt` files
- **Refresh Latest**: Reload the latest results for each protocol
- **Filter by Protocol**: Show only runs for specific protocol
- **View Details**: Open detailed view with full metrics
- **Delete Run**: Remove a benchmark run from database

### Detailed Run View

Click "View" on any run to see:
- Complete statistics (mean, median, std dev, min, max, P95, P99)
- Latency over time chart
- Individual request metrics

## Architecture

### Modules

```
metrics_exporter/
├── __init__.py          # Module exports
├── models.py            # Pydantic data models
├── storage.py           # SQLite storage layer
├── exporters.py         # Export to various formats
└── utils.py             # Legacy format parsers

dashboard/
├── main.py              # FastAPI application
├── templates/
│   └── dashboard.html   # Main dashboard template
└── static/
    ├── css/
    │   └── style.css    # Dashboard styles
    └── js/
        └── dashboard.js # Dashboard logic

metrics_cli.py           # Command-line interface
update_benchmarks.py     # Integration script
```

### Data Models

#### BenchmarkResult
```python
{
    "id": 1,
    "run_id": "grpc_20250105_123456",
    "protocol": "gRPC",
    "timestamp": "2025-01-05T12:34:56",
    "metrics": [...],
    "stats": {...},
    "metadata": {}
}
```

#### MetricData
```python
{
    "request_id": 0,
    "request_timestamp": "2025-01-05T12:34:56.123Z",
    "response_timestamp": "2025-01-05T12:34:56.456Z",
    "latency_seconds": 0.000333
}
```

#### BenchmarkStats
```python
{
    "mean": 0.001234,
    "median": 0.001100,
    "std_dev": 0.000456,
    "min": 0.000800,
    "max": 0.002500,
    "count": 1000,
    "p50": 0.001100,
    "p95": 0.001800,
    "p99": 0.002100
}
```

### Database Schema

**benchmark_runs**
- `id`: INTEGER PRIMARY KEY
- `run_id`: TEXT UNIQUE (e.g., "grpc_20250105_123456")
- `protocol`: TEXT (REST, gRPC, etc.)
- `timestamp`: DATETIME
- `stats_json`: TEXT (JSON-encoded statistics)
- `metadata_json`: TEXT (JSON-encoded metadata)
- `created_at`: DATETIME

**metrics**
- `id`: INTEGER PRIMARY KEY
- `run_id`: TEXT (foreign key)
- `request_id`: INTEGER
- `request_timestamp`: TEXT
- `response_timestamp`: TEXT
- `latency_seconds`: REAL

## API Endpoints

### GET /
Main dashboard page

### GET /api/stats
Database statistics

### GET /api/runs?protocol=&limit=&offset=
List all runs with optional filtering

### GET /api/runs/{run_id}
Get specific run details

### GET /api/latest
Get latest run for each protocol

### POST /api/import-legacy
Import legacy `*_out.txt` files

### DELETE /api/runs/{run_id}
Delete a run

### GET /api/export/{run_id}/{format}
Export run in specified format

### GET /api/compare
Compare latest results from all protocols

## Export Formats

### CSV
Simple tabular format with columns: request_id, request_timestamp, response_timestamp, latency_seconds

### JSON
Complete benchmark data including metadata and statistics

### Excel (XLSX)
Multi-sheet workbook:
- One sheet per protocol with detailed metrics
- Summary sheet with comparative statistics

### HTML
Styled report with statistics cards and formatting

## Integration with Existing Benchmarks

The new metrics system is designed to work alongside existing benchmarks:

1. **Non-invasive**: Existing `run_benchmarks.py` continues to work unchanged
2. **Import-based**: Import results from existing `*_out.txt` files
3. **Backward compatible**: All existing data formats are supported

To integrate into your workflow:

```bash
# 1. Run benchmarks as usual
python run_benchmarks.py

# 2. Import results
python metrics_cli.py import

# 3. View in dashboard
python metrics_cli.py dashboard
```

## Tips

1. **Regular Imports**: Set up a cron job or script to auto-import results after benchmark runs
2. **Export Reports**: Generate Excel reports for sharing with team members
3. **Historical Analysis**: Use the dashboard to track performance trends over time
4. **Protocol Comparison**: Use the comparison chart to identify the fastest protocol
5. **Detailed Investigation**: Use the detailed view to investigate outliers or performance issues

## Troubleshooting

### Dashboard won't start
```bash
# Check if port is in use
lsof -i :8888

# Use different port
python metrics_cli.py dashboard --port 9000
```

### Import fails
```bash
# Check if *_out.txt files exist
ls -la *_out.txt

# Try importing from specific directory
python metrics_cli.py import --dir /path/to/results
```

### Charts not displaying
- Clear browser cache and reload
- Check browser console for JavaScript errors
- Ensure Chart.js CDN is accessible

## Future Enhancements

Potential features for future versions:
- Prometheus metrics export
- Real-time monitoring during benchmark runs
- Automated email reports
- CI/CD integration
- Performance regression detection
- Multi-node distributed benchmarking

## License

Same as parent project.

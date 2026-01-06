# Dashboard Installation Guide

## Quick Install (Dashboard Only)

If you're having issues installing the full requirements (especially grpcio compilation issues on macOS/Windows), you can install just the dashboard dependencies:

```bash
pip install -r requirements-dashboard.txt
```

This will install only what's needed for the metrics dashboard and CLI tools, without the heavy grpcio/protobuf dependencies required for running benchmarks.

## What You Can Do with Dashboard-Only Install

✅ **Available:**
- Import existing benchmark results from `*_out.txt` files
- View all metrics in web dashboard
- Export to CSV, JSON, Excel, HTML
- Use all CLI commands (import, list, stats, export, etc.)
- Analyze and compare protocol performance

❌ **Not Available:**
- Running new gRPC benchmarks (requires grpcio)
- Generating new gRPC test data

## Installation Options

### Option 1: Dashboard Only (Recommended for macOS Python 3.13)

```bash
# Clone repository
git clone https://github.com/ice1x/FastAPI-Talks.git
cd FastAPI-Talks

# Install dashboard dependencies only
pip install -r requirements-dashboard.txt

# Import existing results
python metrics_cli.py import

# Start dashboard
python metrics_cli.py dashboard
```

### Option 2: Full Install with Conda (Recommended)

If you need to run benchmarks too, use conda which has pre-built packages:

```bash
# Create conda environment
conda create -n fastapi_talks python=3.11
conda activate fastapi_talks

# Install grpcio via conda (has pre-built binaries)
conda install -c conda-forge grpcio grpcio-tools

# Install remaining dependencies
pip install -r requirements.txt
```

### Option 3: Full Install with Binary Wheels

Try forcing pip to use only binary wheels:

```bash
pip install --only-binary :all: grpcio grpcio-tools
pip install -r requirements.txt
```

### Option 4: Use Docker

```bash
# Build and run in Docker (no compilation needed)
docker build -t fastapi-talks .
docker run -p 8888:8888 fastapi-talks python metrics_cli.py dashboard
```

## Common Issues

### Issue: grpcio compilation fails on macOS with Python 3.13

**Solution:** Use `requirements-dashboard.txt` instead:
```bash
pip install -r requirements-dashboard.txt
```

You can still analyze all existing benchmark data, just can't generate new gRPC benchmarks.

### Issue: Missing C++ compiler on macOS

**Solution 1 - Dashboard only:**
```bash
pip install -r requirements-dashboard.txt
```

**Solution 2 - Install build tools:**
```bash
# Install Xcode Command Line Tools
xcode-select --install

# Install cmake and protobuf
brew install cmake protobuf

# Try again
pip install -r requirements.txt
```

### Issue: Apple Silicon (M1/M2/M3) compatibility

**Solution:** Use conda with architecture-specific builds:
```bash
conda create -n fastapi_talks python=3.11
conda activate fastapi_talks
conda install -c conda-forge grpcio grpcio-tools protobuf
pip install -r requirements.txt
```

## Verification

After installation, verify the dashboard works:

```bash
# Check version
python metrics_cli.py --help

# Generate test data (works even without grpcio)
python generate_test_data.py

# Import test data
python metrics_cli.py import

# Start dashboard
python metrics_cli.py dashboard

# Open browser to http://localhost:8888
```

## Dependencies Comparison

### Full Requirements (requirements.txt)
- All benchmark protocols (REST, gRPC, Socket.IO, GraphQL, AVRO, CBOR)
- Dashboard and metrics export
- **Requires:** C++ compiler, protobuf, cmake
- **Size:** ~500MB with all dependencies

### Dashboard Only (requirements-dashboard.txt)
- Dashboard and metrics export only
- Can import and analyze existing benchmark data
- **Requires:** Nothing special
- **Size:** ~200MB

## Next Steps

Once installed, see [METRICS_DASHBOARD.md](METRICS_DASHBOARD.md) for usage instructions.

### Quick Start

```bash
# 1. Import existing benchmark results
python metrics_cli.py import

# 2. Start dashboard
python metrics_cli.py dashboard

# 3. Open in browser
open http://localhost:8888
```

## Support

If you continue to have installation issues:

1. Check your Python version: `python --version`
2. Try using Python 3.11 instead of 3.13
3. Use conda instead of pip
4. Install dashboard-only version
5. Report issue on GitHub with your OS and Python version

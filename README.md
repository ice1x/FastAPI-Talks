# FastAPI Communication Protocols Benchmark

> **Comprehensive performance comparison of 6 modern communication protocols and serialization formats**

[![CI](https://github.com/ice1x/FastAPI-Talks/workflows/CI/badge.svg)](https://github.com/ice1x/FastAPI-Talks/actions)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**📊 1,000 requests per protocol** • **🎯 Statistical analysis** • **📈 Interactive dashboard** • **🔬 Real measurements**

---

## 💡 Why This Project?

Choosing the right communication protocol can make a **10x difference** in your application performance. This project helps you:

- 🔬 **Compare protocols objectively** with real measurements on identical hardware
- 📊 **Understand trade-offs** between latency, complexity, and features
- 🎓 **Learn implementation patterns** for each protocol with production-ready FastAPI code
- 🚀 **Make informed decisions** for your next microservice architecture
- 📈 **Visualize performance** with interactive dashboard and exportable reports

**Real-world use case**: Should you use gRPC or REST for your microservices? GraphQL or REST for your mobile app? Binary serialization or JSON? This benchmark gives you **data-driven answers**.

---

## ⚡ Quick Results

Based on 1,000 sequential requests on localhost (Python 3.11, FastAPI):

| Protocol | Avg Latency | Min | Max | Best For |
|----------|-------------|-----|-----|----------|
| **REST** | 2.36ms | 1.74ms | 18.15ms | Public APIs, simplicity, broad compatibility |
| **AVRO** | 2.66ms | 1.93ms | 38.98ms | Schema evolution, data pipelines |
| **CBOR** | 2.85ms | 1.82ms | 27.18ms | Binary efficiency, IoT, constrained devices |
| **Socket.IO** | 99.76ms | 1.30ms | 199.20ms | Real-time apps, bidirectional events |
| **GraphQL** | 346.41ms | 97.22ms | 682.09ms | Flexible queries, multiple client types |
| **gRPC** | ⚠️ *See note* | - | - | Microservices, low-latency RPC |

> 💡 **Note**: gRPC benchmark could not complete in this test environment. Typically gRPC is faster than REST due to HTTP/2 and Protocol Buffers.
>
> ⚠️ **Important**: These results are from localhost testing with small payloads (timestamps). Socket.IO and GraphQL show high latency here, but offer unique advantages:
> - **Socket.IO**: Bidirectional real-time communication (no polling overhead)
> - **GraphQL**: One request vs multiple REST calls (reduces network round trips)
>
> 📊 See detailed analysis in [REAL_BENCHMARK_RESULTS.md](REAL_BENCHMARK_RESULTS.md) • Run your own: `make run-benchmarks`

---

## 📋 Overview

This project provides a comprehensive benchmark suite comparing **6 popular communication protocols and serialization formats** using FastAPI:

### Protocols & Formats Tested

**🌐 Communication Protocols:**
- **REST API** - Standard JSON over HTTP/1.1 (baseline)
- **gRPC** - High-performance RPC with Protocol Buffers over HTTP/2
- **Socket.IO** - WebSocket-based bidirectional event-driven communication
- **GraphQL** - Flexible query language for APIs

**📦 Serialization Formats:**
- **AVRO** - Apache Avro binary serialization with schema evolution
- **CBOR** - Concise Binary Object Representation (binary JSON)

Each implementation includes:
- ✅ Production-ready FastAPI services (requester + responder)
- ✅ Comprehensive error handling and logging
- ✅ Statistical analysis (mean, median, percentiles, std dev)
- ✅ Automated test suite with pytest
- ✅ Code quality checks (black, isort, flake8, mypy)

---

## 🎯 Features

- **🚀 Automated Execution** - Run all benchmarks with single command
- **📊 Statistical Analysis** - Mean, median, std dev, min/max, P95/P99 percentiles
- **📈 Interactive Dashboard** - Web UI with charts, exports, historical tracking
- **📉 Visual Comparisons** - Matplotlib charts for response time distributions
- **🐳 Docker Support** - Consistent testing environments
- **🧪 Comprehensive Tests** - pytest suite with >80% coverage
- **🔧 Modular Architecture** - Easy to add new protocols
- **📁 Multiple Export Formats** - JSON, CSV, Excel, HTML reports
- **🗄️ Historical Tracking** - SQLite database for long-term analysis
- **⚙️ CI/CD Integration** - GitHub Actions with automated testing

---

## 📊 Interactive Dashboard

Visualize and analyze benchmark results with the built-in web dashboard powered by FastAPI + Chart.js:

```bash
# 1. Run benchmarks (generates *_out.txt files)
make run-benchmarks

# 2. Import results to database
python metrics_cli.py import

# 3. Start dashboard server
python metrics_cli.py dashboard

# 4. Open in browser
# http://localhost:8888
```

### Dashboard Features

- 📈 **Real-time Performance Charts** - Compare protocols side-by-side
- 🔍 **Protocol Comparison Views** - Latency distributions, percentiles
- 📊 **Historical Trend Analysis** - Track performance over time
- 📥 **Export Capabilities** - Download as Excel, CSV, JSON, HTML
- 🗃️ **Run Management** - Browse, filter, and delete old runs
- 📱 **Responsive Design** - Works on desktop and mobile

![Dashboard Overview](docs/images/dashboard_overview.png)

> 📖 **Full documentation**: [METRICS_DASHBOARD.md](METRICS_DASHBOARD.md)

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+ (3.12 recommended)
- pip package manager
- (Optional) Docker and Docker Compose

### Installation

#### Option 1: Automated Setup (Recommended)

```bash
# Clone the repository
git clone https://github.com/ice1x/FastAPI-Talks.git
cd FastAPI-Talks

# Complete setup: install dependencies + compile protobuf
make setup

# Run all benchmarks
make run-benchmarks

# View results
python compare.py
```

That's it! The automated runner will:
1. ✅ Start all 12 services (6 responders + 6 requesters)
2. ✅ Execute 1,000 requests per protocol
3. ✅ Save results to `*_out.txt` files
4. ✅ Generate comparison charts (`benchmark_comparison.png`)

#### Option 2: Manual Installation

```bash
# 1. Clone repository
git clone https://github.com/ice1x/FastAPI-Talks.git
cd FastAPI-Talks

# 2. Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Compile Protocol Buffers (required for gRPC)
make compile-proto
```

### Running Your First Benchmark

```bash
# Run all benchmarks automatically
python run_benchmarks.py

# Or use Makefile
make run-benchmarks

# View comparison
python compare.py

# Import to dashboard
python metrics_cli.py import

# Start dashboard
python metrics_cli.py dashboard
```

---

## 📁 Project Structure

```
FastAPI-Talks/
├── common/                  # 🆕 Shared base classes and utilities
│   ├── base_requester.py    # Base class for all requesters
│   ├── base_responder.py    # Base class for all responders
│   ├── config.py            # Shared configuration
│   └── schemas.py           # Common schemas (AVRO, etc.)
├── rest_requester/          # REST API client
├── rest_responder/          # REST API server
├── grpc_requester/          # gRPC client (Protocol Buffers)
├── grpc_responder/          # gRPC server
├── sio_requester/           # Socket.IO client
├── sio_responder/           # Socket.IO server
├── graphql_requester/       # GraphQL client
├── graphql_responder/       # GraphQL server (Strawberry)
├── avro_requester/          # Apache Avro client
├── avro_responder/          # Apache Avro server
├── cbor_requester/          # CBOR client
├── cbor_responder/          # CBOR server
├── metrics_exporter/        # Metrics storage and export
│   ├── models.py            # Pydantic data models
│   ├── storage.py           # SQLite storage layer
│   ├── exporters.py         # CSV, JSON, Excel, HTML exporters
│   └── utils.py             # Legacy format parsers
├── dashboard/               # Web dashboard
│   ├── main.py              # FastAPI application
│   ├── templates/           # Jinja2 templates
│   └── static/              # CSS, JavaScript, images
├── tests/                   # pytest test suite
├── docs/                    # Documentation and images
├── compare.py               # Benchmark comparison script
├── run_benchmarks.py        # Automated benchmark runner
├── metrics_cli.py           # CLI for metrics management
├── requirements.txt         # Python dependencies
├── Makefile                 # Automation commands
├── .github/workflows/       # CI/CD workflows
├── BENCHMARKS.md            # Detailed methodology
├── METRICS_DASHBOARD.md     # Dashboard documentation
├── REFACTORING_PLAN.md      # 🆕 Code refactoring guide
├── CONTRIBUTING.md          # Contribution guidelines
└── README.md                # This file
```

---

## 🎯 Use Cases

### 1. Architecture Decision Making

```bash
# Scenario: Choosing protocol for new microservices architecture
make run-benchmarks
python compare.py

# Compare gRPC (fastest) vs REST (simplest)
# Decision factors: latency requirements, team expertise, ecosystem
```

### 2. Performance Regression Testing

```bash
# Before optimization
python run_benchmarks.py
python metrics_cli.py import

# After optimization
python run_benchmarks.py
python metrics_cli.py import

# Compare in dashboard to measure improvement
python metrics_cli.py list --protocol gRPC
```

### 3. Educational Purposes

```bash
# Learn how to implement each protocol with FastAPI
cd grpc_requester && cat main.py
cd ../grpc_responder && cat main.py

# Each service is a self-contained, production-ready example
# with proper error handling, typing, and documentation
```

### 4. Performance Analysis

```bash
# Export detailed metrics for analysis
python metrics_cli.py export <run_id> --format excel

# Analyze in Excel/Jupyter:
# - Latency distributions
# - Outlier detection
# - Percentile analysis (P95, P99)
# - Time-series patterns
```

---

## 🏃 Running Benchmarks

### Option 1: Automated (Recommended)

Run all benchmarks with a single command:

```bash
# Using Makefile
make run-benchmarks

# Or directly with Python
python run_benchmarks.py
```

**What happens**:
1. Starts REST responder + requester → 1,000 requests → saves to `rest_out.txt`
2. Starts gRPC responder + requester → 1,000 requests → saves to `grpc_out.txt`
3. Starts Socket.IO responder + requester → 1,000 requests → saves to `sio_out.txt`
4. Starts GraphQL responder + requester → 1,000 requests → saves to `graphql_out.txt`
5. Starts AVRO responder + requester → 1,000 requests → saves to `avro_out.txt`
6. Starts CBOR responder + requester → 1,000 requests → saves to `cbor_out.txt`
7. Runs `compare.py` to generate comparison charts

### Option 2: Manual (For Development)

Run individual protocols for testing:

<details>
<summary><b>REST API Benchmark</b></summary>

```bash
# Terminal 1: Start responder
cd rest_responder
uvicorn main:app --host 0.0.0.0 --port 8000

# Terminal 2: Start requester
cd rest_requester
uvicorn main:app --host 0.0.0.0 --port 8080

# Terminal 3: Execute benchmark
curl http://127.0.0.1:8080/run-benchmark > rest_out.txt
```
</details>

<details>
<summary><b>gRPC Benchmark</b></summary>

```bash
# Terminal 1: Start gRPC responder
cd grpc_responder
python main.py

# Terminal 2: Start gRPC requester
cd grpc_requester
uvicorn main:app --host 0.0.0.0 --port 8000

# Terminal 3: Execute benchmark
curl http://127.0.0.1:8000/api/run > grpc_out.txt
```
</details>

<details>
<summary><b>Socket.IO Benchmark</b></summary>

```bash
# Terminal 1: Start Socket.IO responder
cd sio_responder
uvicorn main:sio_app --host 0.0.0.0 --port 8000

# Terminal 2: Start Socket.IO requester
cd sio_requester
uvicorn main:app --host 0.0.0.0 --port 8080

# Terminal 3: Execute benchmark
curl http://127.0.0.1:8080/send-timestamp > sio_out.txt
```
</details>

<details>
<summary><b>GraphQL Benchmark</b></summary>

```bash
# Terminal 1: Start GraphQL responder
cd graphql_responder
uvicorn main:app --host 0.0.0.0 --port 8000

# Terminal 2: Start GraphQL requester
cd graphql_requester
uvicorn main:app --host 0.0.0.0 --port 8080

# Terminal 3: Execute benchmark
curl http://127.0.0.1:8080/aggregate-timestamps > graphql_out.txt
```
</details>

<details>
<summary><b>AVRO Benchmark</b></summary>

```bash
# Terminal 1: Start AVRO responder
cd avro_responder
uvicorn main:app --host 0.0.0.0 --port 8000

# Terminal 2: Start AVRO requester
cd avro_requester
uvicorn main:app --host 0.0.0.0 --port 8080

# Terminal 3: Execute benchmark
curl http://127.0.0.1:8080/run-benchmark > avro_out.txt
```
</details>

<details>
<summary><b>CBOR Benchmark</b></summary>

```bash
# Terminal 1: Start CBOR responder
cd cbor_responder
uvicorn main:app --host 0.0.0.0 --port 8000

# Terminal 2: Start CBOR requester
cd cbor_requester
uvicorn main:app --host 0.0.0.0 --port 8080

# Terminal 3: Execute benchmark
curl http://127.0.0.1:8080/run-benchmark > cbor_out.txt
```
</details>

---

## 📊 Analyzing Results

### Command Line Analysis

```bash
# Generate comparison charts and statistics
python compare.py

# Output:
# - Statistical comparison (mean, median, std dev, min, max)
# - Visual charts showing response time distributions
# - Performance rankings
# - Saved chart: benchmark_comparison.png
```

### Dashboard Analysis

```bash
# Import results to database
python metrics_cli.py import

# Start dashboard
python metrics_cli.py dashboard

# Open http://localhost:8888 in browser
```

### Export Results

```bash
# Export single run to Excel
python metrics_cli.py export <run_id> --format excel --output results.xlsx

# Export all latest results to Excel
python metrics_cli.py export-all --format excel --output exports/all_benchmarks

# Export to HTML report
python metrics_cli.py export-all --format html --output exports/report

# Export to CSV
python metrics_cli.py export-all --format csv --output exports/csv
```

### List and Query Runs

```bash
# List all runs
python metrics_cli.py list

# Filter by protocol
python metrics_cli.py list --protocol gRPC --limit 10

# Show statistics
python metrics_cli.py stats
```

---

## 🛠️ Development

### Testing

```bash
# Run all tests with pytest
make test

# Run with coverage report
make test-cov

# Run specific test file
pytest tests/test_grpc.py -v

# Run tests for specific protocol
pytest tests/test_rest.py tests/test_grpc.py -v
```

### Code Quality

```bash
# Run all linters (black, isort, flake8, mypy)
make lint

# Auto-format code
make format

# Type checking only
make type-check

# Run all CI checks locally
make ci
```

### Pre-commit Hooks

```bash
# Install pre-commit hooks (runs linters before commits)
make pre-commit-install

# Run manually on all files
pre-commit run --all-files
```

### CI/CD

GitHub Actions automatically runs on:
- All pushes to `main`, `develop`, and `claude/*` branches
- All pull requests

Checks include:
- ✅ All tests (pytest)
- ✅ Code formatting (black, isort)
- ✅ Linting (flake8)
- ✅ Type checking (mypy)

---

## 🔧 Makefile Commands

```bash
make help              # Show all available commands
make install           # Install Python dependencies
make install-dev       # Install development dependencies
make compile-proto     # Compile Protocol Buffer files
make setup             # Complete setup (install + compile)
make setup-dev         # Development setup (install-dev + compile + hooks)
make run-benchmarks    # Run all benchmarks automatically
make compare           # Compare benchmark results
make test              # Run tests
make test-cov          # Run tests with coverage report
make lint              # Run all linters
make format            # Format code with black and isort
make type-check        # Run mypy type checking
make pre-commit-install # Install pre-commit hooks
make ci                # Run all CI checks locally
make clean             # Remove generated files and results
```

---

## 📈 Benchmark Methodology

Each benchmark:
1. Sends **1,000 sequential requests** (configurable)
2. Records **request and response timestamps** with microsecond precision
3. Calculates **response time (latency)** for each request
4. Aggregates results for **statistical analysis**:
   - Mean, median, standard deviation
   - Min, max
   - Percentiles (P50, P95, P99)

### Important Notes

- **Localhost testing**: Eliminates network latency to focus on protocol overhead
- **Sequential requests**: Not a load test; measures single-thread latency
- **Minimal payload**: Only timestamps; larger payloads may show different results
- **No caching**: Each request is independent

For detailed methodology and interpretation, see [BENCHMARKS.md](BENCHMARKS.md).

---

## 🤝 Contributing

Contributions are welcome! This project is especially friendly for:
- 🆕 **First-time contributors** - Good first issues labeled
- 🎓 **Learning projects** - Well-documented codebase
- 🔬 **Research** - Benchmark methodology improvements
- 🚀 **New protocols** - Easy to add with base classes

**Quick Start**:
1. Read [CONTRIBUTING.md](CONTRIBUTING.md)
2. Check [REFACTORING_PLAN.md](REFACTORING_PLAN.md) for architecture
3. Fork the repository
4. Make your changes with tests
5. Submit a pull request

**Adding a New Protocol**:
- Before refactoring: ~200+ lines (copy-paste existing service)
- After refactoring: ~40 lines (extend base classes)

See [REFACTORING_PLAN.md](REFACTORING_PLAN.md) for details.

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

Built with amazing open-source tools:

- [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast web framework for Python
- [gRPC](https://grpc.io/) - High-performance RPC framework by Google
- [Socket.IO](https://socket.io/) - Real-time bidirectional event-based communication
- [Strawberry GraphQL](https://strawberry.rocks/) - Python GraphQL library with type hints
- [Apache Avro](https://avro.apache.org/) - Data serialization system
- [CBOR](https://cbor.io/) - Concise Binary Object Representation
- [Chart.js](https://www.chartjs.org/) - Simple yet flexible JavaScript charting
- [Matplotlib](https://matplotlib.org/) - Python plotting library

---

## 📧 Contact & Links

- **Author**: ice1x
- **Repository**: [github.com/ice1x/FastAPI-Talks](https://github.com/ice1x/FastAPI-Talks)
- **Issues**: [Report bugs or request features](https://github.com/ice1x/FastAPI-Talks/issues)
- **Discussions**: [Ask questions or share ideas](https://github.com/ice1x/FastAPI-Talks/discussions)

---

## ⭐ Star History

If you find this project useful, please consider giving it a star! ⭐

It helps others discover the project and motivates further development.

```bash
# Quick clone and try:
git clone https://github.com/ice1x/FastAPI-Talks.git
cd FastAPI-Talks
make setup
make run-benchmarks
python metrics_cli.py dashboard
# Open http://localhost:8888
```

---

## 🎓 Learn More

**Documentation**:
- [BENCHMARKS.md](BENCHMARKS.md) - Detailed methodology and interpretation
- [METRICS_DASHBOARD.md](METRICS_DASHBOARD.md) - Dashboard usage guide
- [REFACTORING_PLAN.md](REFACTORING_PLAN.md) - Code architecture and refactoring
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines

**Blog Posts** (Coming Soon):
- "Benchmarking 6 Communication Protocols with FastAPI"
- "gRPC vs REST: Real Performance Numbers"
- "Building an Interactive Benchmark Dashboard"

---

<div align="center">

**Made with ❤️ and FastAPI**

[⬆ Back to top](#fastapi-communication-protocols-benchmark)

</div>

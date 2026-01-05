# FastAPI Communication Protocols & Serialization Benchmark

A comprehensive benchmark comparing different communication protocols and serialization formats using FastAPI: **gRPC**, **Socket.IO**, **GraphQL**, **AVRO**, and **CBOR**.

## 📋 Overview

This project benchmarks the performance of five popular communication protocols and serialization formats by measuring response times for 1,000 sequential timestamp requests. Each implementation consists of a requester service and a responder service.

### Protocols & Formats Tested

**Communication Protocols:**
- **gRPC** - High-performance RPC framework using Protocol Buffers
- **Socket.IO** - WebSocket-based bidirectional event-driven communication
- **GraphQL** - Query language for APIs with flexible data fetching

**Serialization Formats:**
- **AVRO** - Apache Avro binary serialization format
- **CBOR** - Concise Binary Object Representation (binary JSON)

## 🎯 Features

- Automated benchmark execution for all protocols
- Response time measurement and statistical analysis
- Visual comparison charts using matplotlib
- Docker support for consistent testing environments
- Modular architecture for easy extension

## 📦 Prerequisites

- Python 3.11+
- pip package manager
- (Optional) Docker and Docker Compose

## 🚀 Quick Start

### Automated Setup (Recommended)

```bash
# Clone the repository
git clone https://github.com/ice1x/FastAPI-Talks.git
cd FastAPI-Talks

# Complete setup (install dependencies + compile protobuf)
make setup

# Run all benchmarks automatically
make run-benchmarks
```

That's it! The automated runner will execute all benchmarks and generate comparison results.

### Manual Installation

If you prefer manual setup:

```bash
# 1. Clone the repository
git clone https://github.com/ice1x/FastAPI-Talks.git
cd FastAPI-Talks

# 2. Install dependencies
pip install -r requirements.txt

# 3. Compile Protocol Buffers
make compile-proto
# Or manually:
cd grpc_responder
python -m grpc_tools.protoc --python_out=./pb --grpc_python_out=./pb -I=./protos hello_grpc.proto
cd ../grpc_requester
python -m grpc_tools.protoc --python_out=./pb --grpc_python_out=./pb -I=./protos hello_grpc.proto
cd ..
```

## 🏃 Running Benchmarks

### Option 1: Automated (Recommended)

Run all benchmarks with a single command:

```bash
# Using Makefile
make run-benchmarks

# Or directly with Python
python run_benchmarks.py
```

The automated runner will:
- Start each responder service
- Start each requester service
- Execute 1,000 requests
- Save results to `*_out.txt` files
- Generate comparison charts automatically

### Option 2: Run Manually

#### gRPC Benchmark

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

#### Socket.IO Benchmark

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

#### GraphQL Benchmark

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

#### AVRO Benchmark

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

#### CBOR Benchmark

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

### Option 3: Using Docker (Coming Soon)

```bash
docker-compose up
```

## 📊 Analyzing Results

After running all benchmarks, compare the results:

```bash
# Using Makefile
make compare

# Or directly
python compare.py
```

This will generate:
- Statistical comparison (mean, median, std deviation, min, max)
- Visual charts showing response time distributions
- Performance rankings
- Saved chart: `benchmark_comparison.png`

## 📁 Project Structure

```
FastAPI-Talks/
├── grpc_requester/          # gRPC client implementation
├── grpc_responder/          # gRPC server implementation
├── sio_requester/           # Socket.IO client implementation
├── sio_responder/           # Socket.IO server implementation
├── graphql_requester/       # GraphQL client implementation
├── graphql_responder/       # GraphQL server implementation
├── avro_requester/          # AVRO client implementation
├── avro_responder/          # AVRO server implementation
├── cbor_requester/          # CBOR client implementation
├── cbor_responder/          # CBOR server implementation
├── compare.py               # Benchmark comparison script
├── run_benchmarks.py        # Automated benchmark runner
├── requirements.txt         # Python dependencies
├── Makefile                 # Automation commands
├── BENCHMARKS.md            # Detailed methodology
├── CONTRIBUTING.md          # Contribution guidelines
└── README.md                # This file
```

## 🛠️ Makefile Commands

The project includes a Makefile for convenient operations:

```bash
make help              # Show all available commands
make install           # Install Python dependencies
make compile-proto     # Compile Protocol Buffer files
make setup             # Complete setup (install + compile)
make run-benchmarks    # Run all benchmarks automatically
make compare           # Compare benchmark results
make clean             # Remove generated files and results
make test              # Run tests
```

## 🔧 Configuration

Each service can be configured via environment variables. Configuration options are documented in the respective service directories.

## 📈 Benchmark Methodology

Each benchmark:
1. Sends 1,000 sequential requests
2. Records request and response timestamps
3. Calculates response time (latency)
4. Aggregates results for statistical analysis

For detailed methodology and results interpretation, see [BENCHMARKS.md](BENCHMARKS.md).

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on:
- How to report issues
- Code style guidelines
- Pull request process
- Adding new protocol benchmarks

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Built with:
- [FastAPI](https://fastapi.tiangolo.com/) - Modern async web framework
- [gRPC](https://grpc.io/) - High-performance RPC framework
- [Socket.IO](https://socket.io/) - Real-time bidirectional communication
- [Strawberry GraphQL](https://strawberry.rocks/) - Python GraphQL library
- [Apache Avro](https://avro.apache.org/) - Binary serialization system
- [CBOR](https://cbor.io/) - Concise binary object representation

## 📧 Contact

- Author: ice1x
- Repository: [https://github.com/ice1x/FastAPI-Talks](https://github.com/ice1x/FastAPI-Talks)


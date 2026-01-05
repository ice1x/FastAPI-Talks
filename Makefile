# Makefile for FastAPI Communication Protocols Benchmark

.PHONY: help install compile-proto clean run-benchmarks compare test

# Default target
help:
	@echo "FastAPI Communication Protocols Benchmark"
	@echo ""
	@echo "Available commands:"
	@echo "  make install          - Install Python dependencies"
	@echo "  make compile-proto    - Compile Protocol Buffer files"
	@echo "  make setup            - Complete setup (install + compile)"
	@echo "  make run-benchmarks   - Run all benchmarks automatically"
	@echo "  make compare          - Compare benchmark results"
	@echo "  make clean            - Remove generated files and results"
	@echo "  make test             - Run tests"
	@echo ""

# Install dependencies
install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt
	@echo "✓ Dependencies installed"

# Compile protobuf files
compile-proto:
	@echo "Compiling Protocol Buffer files..."
	cd grpc_responder && python -m grpc_tools.protoc --python_out=./pb --grpc_python_out=./pb -I=./protos hello_grpc.proto
	cd grpc_requester && python -m grpc_tools.protoc --python_out=./pb --grpc_python_out=./pb -I=./protos hello_grpc.proto
	@echo "✓ Protocol Buffers compiled"

# Complete setup
setup: install compile-proto
	@echo "✓ Setup complete! You can now run benchmarks with 'make run-benchmarks'"

# Run all benchmarks
run-benchmarks:
	@echo "Running all benchmarks..."
	python run_benchmarks.py

# Run comparison
compare:
	@echo "Comparing benchmark results..."
	python compare.py

# Clean generated files
clean:
	@echo "Cleaning generated files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*_out.txt" -delete
	find . -type f -name "benchmark_comparison.png" -delete
	rm -rf grpc_responder/pb/*.py 2>/dev/null || true
	rm -rf grpc_requester/pb/*.py 2>/dev/null || true
	@echo "✓ Cleaned"

# Run tests
test:
	@echo "Running tests..."
	pytest

# Format code
format:
	@echo "Formatting code with black..."
	black .
	@echo "✓ Code formatted"

# Lint code
lint:
	@echo "Linting code..."
	flake8 .
	@echo "✓ Linting complete"

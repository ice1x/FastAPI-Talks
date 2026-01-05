# Makefile for FastAPI Communication Protocols Benchmark

.PHONY: help install install-dev compile-proto clean run-benchmarks compare test test-cov lint format type-check pre-commit-install ci

# Default target
help:
	@echo "FastAPI Communication Protocols Benchmark"
	@echo ""
	@echo "Available commands:"
	@echo "  make install           - Install Python dependencies"
	@echo "  make install-dev       - Install development dependencies"
	@echo "  make compile-proto     - Compile Protocol Buffer files"
	@echo "  make setup             - Complete setup (install + compile)"
	@echo "  make run-benchmarks    - Run all benchmarks automatically"
	@echo "  make compare           - Compare benchmark results"
	@echo "  make test              - Run tests"
	@echo "  make test-cov          - Run tests with coverage report"
	@echo "  make lint              - Run all linters (black, isort, flake8, mypy)"
	@echo "  make format            - Format code with black and isort"
	@echo "  make type-check        - Run mypy type checking"
	@echo "  make pre-commit-install - Install pre-commit hooks"
	@echo "  make ci                - Run all CI checks locally"
	@echo "  make clean             - Remove generated files and results"
	@echo ""

# Install dependencies
install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt
	@echo "✓ Dependencies installed"

# Install development dependencies
install-dev:
	@echo "Installing development dependencies..."
	pip install -r requirements-dev.txt
	@echo "✓ Development dependencies installed"

# Compile protobuf files
compile-proto:
	@echo "Compiling Protocol Buffer files..."
	cd grpc_responder && python -m grpc_tools.protoc --python_out=./pb --grpc_python_out=./pb -I=./protos hello_grpc.proto
	cd grpc_requester && python -m grpc_tools.protoc --python_out=./pb --grpc_python_out=./pb -I=./protos hello_grpc.proto
	@echo "✓ Protocol Buffers compiled"

# Complete setup
setup: install compile-proto
	@echo "✓ Setup complete! You can now run benchmarks with 'make run-benchmarks'"

# Development setup
setup-dev: install-dev compile-proto pre-commit-install
	@echo "✓ Development setup complete!"

# Run all benchmarks
run-benchmarks:
	@echo "Running all benchmarks..."
	python run_benchmarks.py

# Run comparison
compare:
	@echo "Comparing benchmark results..."
	python compare.py

# Run tests
test:
	@echo "Running tests..."
	pytest tests/ -v

# Run tests with coverage
test-cov:
	@echo "Running tests with coverage..."
	pytest tests/ -v --cov=. --cov-report=term-missing --cov-report=html
	@echo "✓ Coverage report generated in htmlcov/"

# Format code
format:
	@echo "Formatting code..."
	black .
	isort .
	@echo "✓ Code formatted"

# Run all linters
lint:
	@echo "Running linters..."
	@echo "→ black (check only)"
	black --check .
	@echo "→ isort (check only)"
	isort --check-only .
	@echo "→ flake8"
	flake8 .
	@echo "→ mypy"
	mypy . --ignore-missing-imports || true
	@echo "✓ Linting complete"

# Run type checking
type-check:
	@echo "Running type checking..."
	mypy . --ignore-missing-imports
	@echo "✓ Type checking complete"

# Install pre-commit hooks
pre-commit-install:
	@echo "Installing pre-commit hooks..."
	pre-commit install
	@echo "✓ Pre-commit hooks installed"

# Run pre-commit on all files
pre-commit-run:
	@echo "Running pre-commit on all files..."
	pre-commit run --all-files

# Run CI checks locally
ci: lint test-cov
	@echo "✓ All CI checks passed!"

# Clean generated files
clean:
	@echo "Cleaning generated files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*_out.txt" -delete
	find . -type f -name "benchmark_comparison.png" -delete
	find . -type f -name ".coverage" -delete
	find . -type f -name "coverage.xml" -delete
	rm -rf grpc_responder/pb/*.py 2>/dev/null || true
	rm -rf grpc_requester/pb/*.py 2>/dev/null || true
	@echo "✓ Cleaned"


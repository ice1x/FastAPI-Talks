# Contributing to FastAPI Communication Protocols Benchmark

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## How to Contribute

### Reporting Issues

If you find a bug or have a suggestion:

1. Check if the issue already exists in [GitHub Issues](https://github.com/ice1x/FastAPI-Talks/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Environment details (OS, Python version, etc.)
   - Relevant logs or screenshots

### Suggesting Enhancements

Enhancement suggestions are welcome! Please:

1. Clearly describe the enhancement
2. Explain why it would be useful
3. Provide examples if possible
4. Consider implementation complexity

### Pull Requests

#### Before Submitting

1. Fork the repository
2. Create a new branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes
4. Test thoroughly
5. Update documentation if needed

#### Code Style

- Follow PEP 8 Python style guidelines
- Use type hints where appropriate
- Add docstrings to functions and classes
- Keep functions focused and modular
- Write descriptive variable names

#### Example Code Style

```python
"""
Module docstring explaining purpose.
"""

from typing import List


def calculate_average(values: List[float]) -> float:
    """
    Calculate the arithmetic mean of a list of values.

    Args:
        values: List of numeric values

    Returns:
        The average of all values

    Raises:
        ValueError: If the list is empty
    """
    if not values:
        raise ValueError("Cannot calculate average of empty list")

    return sum(values) / len(values)
```

#### Commit Messages

Write clear, descriptive commit messages:

- Use present tense ("Add feature" not "Added feature")
- Be concise but descriptive
- Reference issues when applicable

**Good examples**:
```
Add GraphQL batch processing optimization
Fix Socket.IO reconnection handling
Update benchmark methodology documentation (#42)
```

**Bad examples**:
```
Fixed stuff
Update
Changes
```

#### Testing

Before submitting a pull request:

1. Ensure all existing tests pass
2. Add tests for new functionality
3. Run benchmarks to verify performance isn't degraded
4. Test on Python 3.11+

#### Documentation

Update relevant documentation:
- README.md for user-facing changes
- BENCHMARKS.md for methodology changes
- Code comments for complex logic
- Docstrings for public APIs

### Adding New Protocols

To add a new communication protocol benchmark:

1. Create `{protocol}_requester/` directory
   - Implement client that sends 1,000 requests
   - Collect timestamp data
   - Return results in consistent format

2. Create `{protocol}_responder/` directory
   - Implement server that responds to requests
   - Return current timestamp

3. Update `compare.py`
   - Add data processing function
   - Update plotting logic

4. Update documentation
   - Add protocol to README.md
   - Describe methodology in BENCHMARKS.md
   - Add usage instructions

5. Update requirements.txt
   - Add protocol-specific dependencies

### Code Review Process

1. Maintainers will review your pull request
2. Address any feedback or requested changes
3. Once approved, your PR will be merged
4. Your contribution will be credited

## Development Setup

### Prerequisites

- Python 3.11+
- pip
- git

### Setup Steps

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/FastAPI-Talks.git
cd FastAPI-Talks

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Compile protobuf files
cd grpc_responder
python -m grpc_tools.protoc --python_out=./pb --grpc_python_out=./pb -I=./protos hello_grpc.proto
cd ../grpc_requester
python -m grpc_tools.protoc --python_out=./pb --grpc_python_out=./pb -I=./protos hello_grpc.proto
cd ..
```

### Running Tests

```bash
# Run specific protocol benchmark
cd grpc_responder
python main.py

# In another terminal
cd grpc_requester
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Questions?

If you have questions:
- Check existing [issues](https://github.com/ice1x/FastAPI-Talks/issues)
- Open a new issue with the "question" label
- Reach out to maintainers

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing! 🎉

# Contributing to getset-pox-mcp

Thank you for your interest in contributing to getset-pox-mcp! This document provides guidelines and instructions for contributing.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/getset-pox-mcp.git`
3. Create a virtual environment: `python -m venv venv`
4. Activate the virtual environment:
   - Linux/Mac: `source venv/bin/activate`
   - Windows: `venv\Scripts\activate.bat`
5. Install development dependencies: `pip install -e ".[dev]"`

## Development Workflow

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=getset_pox_mcp tests/

# Run specific test file
pytest tests/test_hello_world.py
```

### Code Quality

We use several tools to maintain code quality:

```bash
# Format code with Black
black getset_pox_mcp/ tests/

# Lint with Ruff
ruff check getset_pox_mcp/ tests/

# Type check with MyPy
mypy getset_pox_mcp/
```

### Running the Server Locally

```bash
# STDIO mode (default)
python -m getset_pox_mcp.server

# HTTP mode
TRANSPORT=http python -m getset_pox_mcp.server
```

## Adding New Services

To add a new service/tool:

1. Create a new file in `getset_pox_mcp/services/` (e.g., `my_service.py`)
2. Implement your service function:

```python
from typing import Any
from getset_pox_mcp.logging_config import get_logger

logger = get_logger(__name__)

async def my_tool(param1: str) -> dict[str, Any]:
    """
    Tool description.
    
    Args:
        param1: Parameter description
    
    Returns:
        Result dictionary
    """
    logger.info(f"my_tool called with param1: {param1}")
    
    # Your implementation here
    
    return {
        "result": "success",
        "param1": param1,
    }
```

3. Register the tool in `getset_pox_mcp/server.py`:
   - Add to `list_tools()` function
   - Add to `call_tool()` function

4. Add tests in `tests/test_my_service.py`

5. Update documentation in README.md

## Commit Guidelines

- Use clear, descriptive commit messages
- Follow conventional commits format: `type(scope): description`
  - Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
  - Example: `feat(services): add calculator service`

## Pull Request Process

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Make your changes with appropriate tests
3. Ensure all tests pass: `pytest tests/`
4. Ensure code quality checks pass
5. Update documentation as needed
6. Commit your changes with clear messages
7. Push to your fork: `git push origin feature/my-feature`
8. Create a Pull Request with a clear description

## Code Style

- Follow PEP 8 guidelines
- Use type hints for function parameters and return values
- Write docstrings for all functions, classes, and modules
- Keep functions focused and single-purpose
- Maximum line length: 100 characters

## Testing Requirements

- All new features must include tests
- Maintain or improve code coverage
- Tests should be clear and well-documented
- Use descriptive test names

## Documentation

- Update README.md for user-facing changes
- Update CHANGELOG.md following Keep a Changelog format
- Add docstrings to all new functions and classes
- Include examples where appropriate

## Questions?

If you have questions or need help, please:
- Open an issue for discussion
- Check existing issues and documentation
- Reach out to maintainers

Thank you for contributing! 🎉

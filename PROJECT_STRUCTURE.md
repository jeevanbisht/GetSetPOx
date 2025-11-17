# getset-pox-mcp Project Structure

This document provides an overview of the project structure and organization.

## Directory Structure

```
getset-pox-mcp/
├── getset_pox_mcp/              # Main package directory
│   ├── __init__.py              # Package initialization
│   ├── server.py                # Main MCP server implementation
│   ├── config.py                # Configuration management
│   ├── logging_config.py        # Logging setup
│   ├── services/                # Service implementations
│   │   ├── __init__.py          # Services package init
│   │   └── Test/                # Test service folder
│   │       ├── __init__.py      # Test package init
│   │       ├── hello_world_service.py  # HelloWorld service implementation
│   │       ├── hello_world_tools.py    # HelloWorld MCP tool definitions
│   │       ├── echo_service.py         # Echo service implementation
│   │       └── echo_tools.py           # Echo MCP tool definitions
│   └── transport/               # Transport layer (future)
│       └── __init__.py          # Transport package init
├── tests/                       # Test suite
│   ├── __init__.py              # Tests package init
│   ├── test_hello_world.py      # HelloWorld service tests
│   └── test_echo.py             # Echo service tests
├── scripts/                     # Setup and utility scripts
│   ├── setup.sh                 # Linux/Mac setup script
│   └── setup.bat                # Windows setup script
├── .env.example                 # Example environment configuration
├── .gitignore                   # Git ignore patterns
├── CHANGELOG.md                 # Version history
├── CONTRIBUTING.md              # Contribution guidelines
├── LICENSE                      # MIT License
├── MANIFEST.in                  # Package manifest
├── README.md                    # Main documentation
├── pyproject.toml               # Modern Python project config
├── requirements.txt             # Production dependencies
├── requirements-dev.txt         # Development dependencies
└── setup.py                     # Setup script (backward compatibility)
```

## Key Components

### Main Server (`getset_pox_mcp/server.py`)
- MCP server initialization
- Tool registration and handling
- Transport layer management (STDIO/HTTP)
- Error handling and logging

### Configuration (`getset_pox_mcp/config.py`)
- Environment variable management
- Configuration validation
- Default settings

### Logging (`getset_pox_mcp/logging_config.py`)
- Structured logging setup
- Console and file handlers
- Log level configuration

### Services (`getset_pox_mcp/services/`)
Services are organized in folders with the `_service.py` and `_tools.py` pattern:
- **Test/hello_world_service.py**: HelloWorld service implementation
- **Test/hello_world_tools.py**: HelloWorld MCP tool schema definitions
- **Test/echo_service.py**: Echo service implementation  
- **Test/echo_tools.py**: Echo MCP tool schema definitions

This pattern separates:
- `_service.py`: Business logic and service implementation
- `_tools.py`: MCP tool schemas and registration

### Tests (`tests/`)
Comprehensive test suite using pytest:
- Unit tests for each service
- Async test support
- Coverage reporting

## Design Principles

1. **Modularity**: Services are self-contained and easy to add/remove
2. **Configuration**: Environment-based configuration for flexibility
3. **Logging**: Comprehensive logging for debugging and monitoring
4. **Testing**: High test coverage for reliability
5. **Documentation**: Clear documentation at all levels
6. **Standards**: Follows MCP specification and Python best practices

## Adding New Services

1. Create service file in `getset_pox_mcp/services/`
2. Implement async function with proper type hints
3. Add logging using `get_logger(__name__)`
4. Register in `server.py` (list_tools and call_tool)
5. Create tests in `tests/`
6. Update documentation

## Transport Protocols

### STDIO (Default)
- Standard input/output communication
- Ideal for local development and VS Code integration
- No network configuration required

### HTTP
- Server-sent events (SSE) based communication
- Suitable for remote deployments
- Requires HTTP dependencies (uvicorn, starlette)

## Configuration Options

All configuration via environment variables:
- `TRANSPORT`: stdio or http
- `HTTP_HOST`: HTTP server host
- `HTTP_PORT`: HTTP server port
- `HTTP_PATH`: HTTP endpoint path
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `LOG_FILE`: Optional log file path

## Development Workflow

1. Clone repository
2. Run setup script (`scripts/setup.sh` or `scripts/setup.bat`)
3. Activate virtual environment
4. Make changes
5. Run tests: `pytest tests/`
6. Format code: `black getset_pox_mcp/ tests/`
7. Check linting: `ruff check getset_pox_mcp/ tests/`
8. Submit PR

## Dependencies

### Production
- `mcp>=1.0.0`: Model Context Protocol SDK
- `httpx>=0.27.0`: HTTP client library
- `pydantic>=2.0.0`: Data validation
- `python-dotenv>=1.0.0`: Environment variable management

### Development
- `pytest>=8.0.0`: Testing framework
- `pytest-asyncio>=0.23.0`: Async test support
- `pytest-cov>=4.1.0`: Coverage reporting
- `black>=24.0.0`: Code formatter
- `ruff>=0.3.0`: Linter
- `mypy>=1.8.0`: Type checker

### Optional (HTTP Transport)
- `uvicorn>=0.30.0`: ASGI server
- `starlette>=0.37.0`: Web framework

## Best Practices

1. **Type Hints**: Always use type hints for function parameters and returns
2. **Async/Await**: Use async functions for all tools
3. **Error Handling**: Catch and log exceptions appropriately
4. **Validation**: Validate input parameters
5. **Logging**: Log important events and errors
6. **Testing**: Write tests for all new functionality
7. **Documentation**: Document all functions with docstrings

## References

- [MCP Specification](https://modelcontextprotocol.io/)
- [fabric-rti-mcp](https://github.com/microsoft/fabric-rti-mcp)
- [Python Packaging](https://packaging.python.org/)

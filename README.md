# getset-pox-mcp

A Model Context Protocol (MCP) server implementation providing example services and tools for demonstration and extension purposes.

## 🎯 Overview

The getset-pox-mcp server is a Python-based MCP server that demonstrates best practices for building MCP servers, including:

- ✨ Clean modular architecture with a services folder
- 🔄 Support for multiple transport protocols (STDIO and HTTP)
- 🛡️ Robust error handling and security best practices
- 📝 Comprehensive logging and configuration
- 🧩 Easy extensibility for adding new services and tools

## ✨ Features

### Available Tools

1. **hello_world** - A simple greeting service that returns a personalized message
2. **echo** - An echo service that returns the input message with metadata
3. **check_token_permissions** - Comprehensive diagnostic tool for Microsoft Graph API permissions
   - Tests 19 critical Microsoft Graph permissions
   - Performs real API calls to verify access
   - Provides detailed success/failure reports
   - Offers actionable recommendations for missing permissions

### Authentication & Security

- **EntraID (Azure AD) Support** - Full OAuth2 authentication for Microsoft Graph API
- **Multiple Auth Modes**:
  - Application (daemon) mode with client credentials
  - Delegated (user) mode with device code flow
- **Token Management** - Automatic token refresh, secure caching, and expiry checking
- **MSAL Integration** - Uses Microsoft Authentication Library for Python
- **Non-Blocking Auth** - Background authentication prevents server startup delays
- **Secure Storage** - Token caching with restricted file permissions

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- pip or uv package manager

### Installation

#### Option 1: Install from Source

1. Clone the repository:
```bash
git clone <repository-url>
cd getset-pox-mcp
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -e ".[dev]"
```

#### Option 2: Using uv

```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e ".[dev]"
```

### Configuration for VS Code

Add the following to your VS Code `settings.json` or `mcp.json`:

#### STDIO Mode (Default)

```json
{
    "mcp": {
        "servers": {
            "getset-pox-mcp": {
                "command": "python",
                "args": [
                    "-m",
                    "getset_pox_mcp.server"
                ],
                "env": {
                    "LOG_LEVEL": "INFO"
                }
            }
        }
    }
}
```

#### HTTP Mode

```json
{
    "mcp": {
        "servers": {
            "getset-pox-mcp": {
                "command": "python",
                "args": [
                    "-m",
                    "getset_pox_mcp.server"
                ],
                "env": {
                    "TRANSPORT": "http",
                    "HTTP_HOST": "127.0.0.1",
                    "HTTP_PORT": "3000",
                    "HTTP_PATH": "/mcp",
                    "LOG_LEVEL": "INFO"
                }
            }
        }
    }
}
```

## ⚙️ Configuration

The server can be configured using environment variables:

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `TRANSPORT` | Transport mode (`stdio` or `http`) | `stdio` | `http` |
| `HTTP_HOST` | HTTP server host (HTTP mode only) | `127.0.0.1` | `0.0.0.0` |
| `HTTP_PORT` | HTTP server port (HTTP mode only) | `3000` | `8080` |
| `HTTP_PATH` | HTTP endpoint path (HTTP mode only) | `/mcp` | `/api/mcp` |
| `STATELESS_HTTP` | Use stateless HTTP mode | `false` | `true` |
| `LOG_LEVEL` | Logging level | `INFO` | `DEBUG` |
| `LOG_FILE` | Log file path | None | `logs/server.log` |

### Authentication Configuration

For EntraID (Azure AD) authentication, additional environment variables are available:

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `ENTRA_ENABLE_AUTH` | No | `false` | Enable authentication |
| `ENTRA_TENANT_ID` | Yes* | - | Azure AD tenant ID |
| `ENTRA_CLIENT_ID` | Yes* | - | Application (client) ID |
| `ENTRA_CLIENT_SECRET` | Yes** | - | Client secret |
| `ENTRA_AUTH_MODE` | No | `application` | `application` or `delegated` |
| `ENTRA_SCOPES` | No | `https://graph.microsoft.com/.default` | Comma-separated scopes |

*Required when authentication is enabled  
**Required for application mode

For complete authentication setup instructions, see **[docs/authentication.md](docs/authentication.md)**

## 🧪 Testing

Run the test suite:

```bash
pytest tests/
```

Run with coverage:

```bash
pytest --cov=getset_pox_mcp tests/
```

## 🔧 Development

### Project Structure

```
getset-pox-mcp/
├── getset_pox_mcp/          # Main package
│   ├── __init__.py
│   ├── server.py            # Main server entry point
│   ├── config.py            # Configuration management
│   ├── logging_config.py    # Logging setup
│   ├── transport/           # Transport layer implementations
│   │   ├── __init__.py
│   │   ├── stdio.py         # STDIO transport
│   │   └── http.py          # HTTP transport
│   └── services/            # MCP services and tools
│       ├── __init__.py
│       ├── hello_world.py   # HelloWorld service
│       └── echo.py          # Echo service
├── tests/                   # Test suite
│   ├── __init__.py
│   ├── test_hello_world.py
│   └── test_echo.py
├── pyproject.toml           # Project configuration
├── requirements.txt         # Production dependencies
├── requirements-dev.txt     # Development dependencies
└── README.md               # This file
```

### Adding New Services

1. Create a new service file in `getset_pox_mcp/services/`:

```python
# getset_pox_mcp/services/my_service.py
from typing import Any

async def my_tool(param1: str, param2: int) -> dict[str, Any]:
    """
    Description of your tool.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Result dictionary
    """
    # Your implementation here
    return {"result": "success"}
```

2. Register the tool in `getset_pox_mcp/server.py`:

```python
from .services.my_service import my_tool

# In register_tools():
@mcp.tool()
async def my_tool_handler(param1: str, param2: int) -> dict[str, Any]:
    """Tool description"""
    return await my_tool(param1, param2)
```

### Running in Development Mode

```bash
# With STDIO transport
python -m getset_pox_mcp.server

# With HTTP transport
TRANSPORT=http python -m getset_pox_mcp.server
```

## 📋 Example Usage

### Using with MCP Clients

Once configured, you can interact with the server through any MCP-compatible client:

```
User: Call the hello_world tool with name "Alice"
Agent: [Calls hello_world tool]
Server Response: {"message": "Hello, Alice! Welcome to getset-pox-mcp."}

User: Echo back "test message"
Agent: [Calls echo tool]
Server Response: {
    "original": "test message",
    "echoed": "test message",
    "timestamp": "2025-01-16T19:40:00.000Z",
    "length": 12
}
```

## 🛡️ Security

- The server implements proper error handling and validation
- All inputs are validated before processing
- Logging is configured to avoid exposing sensitive information
- HTTP mode supports authentication headers (when configured)

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes with appropriate tests
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🔗 Resources

- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [fabric-rti-mcp Reference](https://github.com/microsoft/fabric-rti-mcp)

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review the documentation

## 📝 Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and updates.

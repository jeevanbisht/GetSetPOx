# GetSetPOx MCP Server

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![MCP Protocol](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io/)

A Model Context Protocol (MCP) server providing comprehensive POC capabilities for **Microsoft Entra ID**, **Global Secure Access**, **Identity Governance & Administration**, **Intune Device Management**, and **Microsoft Purview** through intelligent Microsoft Graph API integration.

## 🎯 Overview

GetSetPOx is a Python-based MCP server designed for rapid POC deployment and seamless integration with AI agents, featuring:

- ✨ Clean modular architecture with a services folder
- 🔄 Support for multiple transport protocols (STDIO and HTTP)
- 🛡️ Robust error handling and security best practices
- 📝 Comprehensive logging and configuration
- 🧩 Easy extensibility for adding new services and tools

## ✨ Features

### 🔧 Available Tools & Services

#### **Test & Diagnostics**
- **hello_world** - Simple greeting service for testing MCP connectivity
- **echo** - Echo service with metadata for validation and debugging
- **check_token_permissions** - Comprehensive Microsoft Graph API permission diagnostics
  - Tests 19 critical Graph API permissions with real API calls
  - Provides detailed success/failure reports with actionable recommendations

#### **Entra ID (EID) Management**
- **EID_listUsers** - List all users from Microsoft Entra ID
- **EID_getUser** - Get specific user by ID or userPrincipalName
- **EID_searchUsers** - Search users by display name or email
- **EID_listDevices** - List all devices (Entra Joined, Hybrid Joined, Registered, Compliant)
- **EID_getDevice** - Get specific device details by ID
- **EID_getGroups** - List all groups with pagination support
- **EID_getGroup** - Get specific group details by ID
- **EID_getGroupMembers** - Get members of a specific group
- **EID_searchGroups** - Search groups by display name
- **EID_createUserGroups** - Create and manage security groups with users and nested groups

#### **Identity Governance & Administration (IGA)**
- **IGA_listAccessPackages** - List all access packages from Entitlement Management
- **IGA_createAccessCatalog** - Create new access package catalogs
- **IGA_createAccessPackage** - Create new access packages
- **IGA_addResourceGrouptoPackage** - Add Entra groups as resources to access packages

#### **Intune Device Management**
- **IN_listIntuneManagedDevices** - List all Intune-managed devices
- **IN_getManagedDeviceDetails** - Get detailed device information (compliance, enrollment, sync status)
- **IN_listDeviceCompliancePolicies** - List all device compliance policies
- **IN_listDeviceConfigurationProfiles** - List all configuration profiles
- **IN_syncManagedDevice** - Trigger device sync with Intune
- **IN_prepGSAWinClient** - Prepare Global Secure Access Windows Client for deployment
- **IN_intuneAppAssignment** - Assign Win32 apps to device groups with deployment settings

#### **Global Secure Access - Internet Access (IA)**
- **IA_checkInternetAccessForwardingProfile** - Check forwarding profile status
- **IA_enableInternetAccessForwardingProfile** - Enable/disable forwarding profiles
- **IA_createFilteringPolicy** - Create web category filtering policies
- **IA_createFilteringProfile** - Create filtering profiles
- **IA_linkPolicyToFilteringProfile** - Link policies to profiles with logging
- **IA_createConditionalAccessPolicy** - Create CA policies for filtering profiles
- **IA_TLSPOCV2** - Advanced TLS certificate workflow for inspection
- **IA_internetAccessPoc** - Automated end-to-end Web Content Filtering POC setup

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

#### Option 1: Standalone Executable (Recommended for Quick Start)

Download the pre-built standalone executable - no Python installation required!

**Windows:**
1. Download `getset-pox-mcp.exe` from releases
2. Create a `.env` file with your credentials (see `.env.example`)
3. Run: `getset-pox-mcp.exe`

**Linux/macOS:**
1. Download `getset-pox-mcp` from releases
2. Make executable: `chmod +x getset-pox-mcp`
3. Create a `.env` file with your credentials
4. Run: `./getset-pox-mcp`

See **[BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md)** for building your own executable.

#### Option 2: Install from Source

1. Clone the repository:
```bash
git clone https://github.com/jeevanbisht/GetSetPOx.git
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

#### Option 3: Using uv

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
GetSetPOx/
├── getset_pox_mcp/              # Main package
│   ├── __init__.py
│   ├── server.py                # Main server entry point
│   ├── config.py                # Configuration management
│   ├── logging_config.py        # Logging setup
│   ├── authentication/          # Authentication module
│   │   ├── __init__.py
│   │   ├── auth_config.py       # Auth configuration
│   │   ├── auth_provider.py     # OAuth2 provider
│   │   ├── middleware.py        # Auth middleware
│   │   └── token_manager.py     # Token management
│   ├── transport/               # Transport layer implementations
│   │   └── __init__.py
│   └── services/                # MCP services and tools
│       ├── diagnostics/         # Diagnostics service
│       ├── eid/                 # Entra ID management
│       ├── iga/                 # Identity Governance
│       ├── intune/              # Intune device management
│       ├── internetAccess/      # Global Secure Access
│       ├── poc/                 # POC utilities
│       └── Test/                # Test services (hello_world, echo)
├── docs/                        # Documentation
│   └── authentication.md        # Auth setup guide
├── scripts/                     # Setup scripts
│   ├── setup.bat                # Windows setup
│   └── setup.sh                 # Unix setup
├── tests/                       # Test suite
│   ├── test_authentication.py
│   ├── test_diagnostics.py
│   ├── test_echo.py
│   └── test_hello_world.py
├── BUILD_INSTRUCTIONS.md        # 📦 PyInstaller build guide
├── ENV_PACKAGING_GUIDE.md       # 🔒 Configuration packaging guide
├── getset-pox-mcp.spec          # PyInstaller specification
├── prepare_env_for_build.bat    # Windows build helper
├── prepare_env_for_build.sh     # Linux/macOS build helper
├── .gitignore                   # Git ignore rules
├── CHANGELOG.md                 # Version history
├── CODE_OF_CONDUCT.md           # Code of conduct
├── CONTRIBUTING.md              # Contribution guidelines
├── LICENSE                      # MIT License
├── pyproject.toml               # Project configuration
├── README.md                    # This file
├── requirements.txt             # Production dependencies
├── requirements-dev.txt         # Development dependencies
├── SECURITY.md                  # Security policy
└── setup.py                     # Setup script
```

### Building Standalone Executables

To package the server as a standalone executable:

**Quick Build (with embedded .env):**
```bash
# Windows
prepare_env_for_build.bat

# Linux/macOS
chmod +x prepare_env_for_build.sh
./prepare_env_for_build.sh
```

**Manual Build:**
```bash
pip install pyinstaller
pyinstaller getset-pox-mcp.spec
```

The executable will be created in the `dist/` directory (~24 MB).

For detailed build instructions, configuration options, and security considerations, see:
- **[BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md)** - Complete build guide
- **[ENV_PACKAGING_GUIDE.md](ENV_PACKAGING_GUIDE.md)** - Configuration security guide

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

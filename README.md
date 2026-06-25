<div align="center">

# GetSetPOx MCP Server

### Drive Microsoft Entra, Global Secure Access, Intune & IGA proof-of-concepts from your AI agent.

A Model Context Protocol (MCP) server that exposes **Microsoft Graph**-powered tools for **Entra ID**,
**Global Secure Access (Internet Access)**, **Identity Governance (IGA)**, and **Intune** — so an AI
agent can stand up and operate Microsoft identity & security POCs through natural language.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/downloads/)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-2EAD33)](https://modelcontextprotocol.io/)
[![Transport: STDIO · HTTP](https://img.shields.io/badge/Transport-STDIO%20%C2%B7%20HTTP-blue)](#configuration-for-vs-code)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

[Overview](#-overview) · [Tool Catalog](#-tool--service-catalog) · [Quick Start](#-getting-started) · [VS Code Setup](#configuration-for-vs-code) · [Configuration](#️-configuration) · [Development](#-development)

</div>

---

## 🎯 Overview

**GetSetPOx** is a Python-based MCP server built for **rapid Microsoft POC delivery**. Connect it to
any MCP-compatible client (VS Code, Claude, or your own agent) and drive real Microsoft Graph
operations — list and create Entra users/groups/devices, configure Global Secure Access web content
filtering, manage Intune devices and app deployments, and build Identity Governance access packages —
all through tool calls instead of clicking through portals.

**Highlights:**

- ✨ Clean, modular **service-per-domain** architecture — easy to extend with new tools
- 🔄 Dual transport: **STDIO** (default) and **HTTP**
- 🛡️ Full **OAuth2 / MSAL** auth for Microsoft Graph (application & delegated modes)
- 🧪 Built-in **permission diagnostics** that test 19 critical Graph permissions with live API calls
- 📦 Ships as source **or** a **standalone executable** (no Python install required)
- 📝 Structured logging and environment-variable configuration

> **What it's for:** turning a multi-step Microsoft identity/security POC into a handful of agent
> instructions — reproducibly, with the same Graph calls every time.

---

## Who it's for

| You are… | Use GetSetPOx to… |
|---|---|
| **An identity / security pre-sales engineer** | Spin up Entra + GSA + Intune demo environments fast, from your agent. |
| **A Microsoft 365 / Entra admin** | Script repeatable Graph operations (users, groups, devices, policies) without bespoke code. |
| **An AI-agent / MCP builder** | Plug a battle-tested Microsoft Graph toolset into your agent over a standard protocol. |
| **A POC / lab author** | Automate end-to-end Web Content Filtering and access-package setups in one call. |

---

## Table of Contents

- [🎯 Overview](#-overview)
- [🧰 Tool & Service Catalog](#-tool--service-catalog)
- [🔐 Authentication & Security](#-authentication--security)
- [🚀 Getting Started](#-getting-started)
- [Configuration for VS Code](#configuration-for-vs-code)
- [⚙️ Configuration](#️-configuration)
- [🧪 Testing](#-testing)
- [🔧 Development](#-development)
- [📋 Example Usage](#-example-usage)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## 🧰 Tool & Service Catalog

### 🧪 Test & Diagnostics
- **hello_world** — simple greeting service for testing MCP connectivity
- **echo** — echo service with metadata for validation and debugging
- **check_token_permissions** — comprehensive Microsoft Graph permission diagnostics; tests 19
  critical permissions with real API calls and returns actionable success/failure reports

### 👤 Entra ID (EID) Management
- **EID_listUsers** — list all users from Microsoft Entra ID
- **EID_getUser** — get a specific user by ID or userPrincipalName
- **EID_searchUsers** — search users by display name or email
- **EID_listDevices** — list all devices (Entra Joined, Hybrid Joined, Registered, Compliant)
- **EID_getDevice** — get specific device details by ID
- **EID_getGroups** / **EID_getGroup** — list groups (paginated) or fetch one by ID
- **EID_getGroupMembers** — get members of a specific group
- **EID_searchGroups** — search groups by display name
- **EID_createUserGroups** — create and manage security groups with users and nested groups

### 🛂 Identity Governance & Administration (IGA)
- **IGA_listAccessPackages** — list all access packages from Entitlement Management
- **IGA_createAccessCatalog** — create new access package catalogs
- **IGA_createAccessPackage** — create new access packages
- **IGA_addResourceGrouptoPackage** — add Entra groups as resources to access packages

### 💻 Intune Device Management
- **IN_listIntuneManagedDevices** — list all Intune-managed devices
- **IN_getManagedDeviceDetails** — detailed device info (compliance, enrollment, sync status)
- **IN_listDeviceCompliancePolicies** — list all device compliance policies
- **IN_listDeviceConfigurationProfiles** — list all configuration profiles
- **IN_syncManagedDevice** — trigger a device sync with Intune
- **IN_prepGSAWinClient** — prepare the Global Secure Access Windows Client for deployment
- **IN_intuneAppAssignment** — assign Win32 apps to device groups with deployment settings

### 🌐 Global Secure Access — Internet Access (IA)
- **IA_checkInternetAccessForwardingProfile** — check forwarding profile status
- **IA_enableInternetAccessForwardingProfile** — enable/disable forwarding profiles
- **IA_createFilteringPolicy** — create web-category filtering policies
- **IA_createFilteringProfile** — create filtering profiles
- **IA_linkPolicyToFilteringProfile** — link policies to profiles with logging
- **IA_createConditionalAccessPolicy** — create CA policies for filtering profiles
- **IA_TLSPOCV2** — advanced TLS certificate workflow for inspection
- **IA_internetAccessPoc** — automated end-to-end Web Content Filtering POC setup

---

## 🔐 Authentication & Security

- **Entra ID (Azure AD) OAuth2** — full authentication for Microsoft Graph
- **Multiple auth modes** — application (daemon) with client credentials, or delegated (user) via
  device-code flow
- **Token management** — automatic refresh, secure caching, and expiry checking
- **MSAL integration** — uses the Microsoft Authentication Library for Python
- **Non-blocking auth** — background authentication keeps server startup fast
- **Secure storage** — token cache written with restricted file permissions

Full setup: **[docs/authentication.md](docs/authentication.md)** · Security policy:
**[SECURITY.md](SECURITY.md)**

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+ and `pip` (or `uv`) — *not needed if you use the standalone executable*

### Option 1 — Standalone executable (fastest)

No Python install required.

**Windows:** download `getset-pox-mcp.exe` from releases → create a `.env` (see
[`.env.example`](.env.example)) → run `getset-pox-mcp.exe`.

**Linux/macOS:** download `getset-pox-mcp` → `chmod +x getset-pox-mcp` → create `.env` → run
`./getset-pox-mcp`.

Build your own: **[BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md)**.

### Option 2 — Install from source

```bash
git clone https://github.com/jeevanbisht/GetSetPOx.git
cd GetSetPOx

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -e ".[dev]"
```

### Option 3 — Using uv

```bash
uv venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
uv pip install -e ".[dev]"
```

---

## Configuration for VS Code

Add the server to your VS Code `settings.json` or `mcp.json`.

### STDIO mode (default)

```json
{
  "mcp": {
    "servers": {
      "getset-pox-mcp": {
        "command": "python",
        "args": ["-m", "getset_pox_mcp.server"],
        "env": { "LOG_LEVEL": "INFO" }
      }
    }
  }
}
```

### HTTP mode

```json
{
  "mcp": {
    "servers": {
      "getset-pox-mcp": {
        "command": "python",
        "args": ["-m", "getset_pox_mcp.server"],
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

---

## ⚙️ Configuration

Configure the server via environment variables (e.g. in a `.env` file).

### Server

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `TRANSPORT` | Transport mode (`stdio` or `http`) | `stdio` | `http` |
| `HTTP_HOST` | HTTP host (HTTP mode) | `127.0.0.1` | `0.0.0.0` |
| `HTTP_PORT` | HTTP port (HTTP mode) | `3000` | `8080` |
| `HTTP_PATH` | HTTP endpoint path (HTTP mode) | `/mcp` | `/api/mcp` |
| `STATELESS_HTTP` | Use stateless HTTP mode | `false` | `true` |
| `LOG_LEVEL` | Logging level | `INFO` | `DEBUG` |
| `LOG_FILE` | Log file path | None | `logs/server.log` |

### Authentication (Entra ID)

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `ENTRA_ENABLE_AUTH` | No | `false` | Enable authentication |
| `ENTRA_TENANT_ID` | Yes\* | – | Azure AD tenant ID |
| `ENTRA_CLIENT_ID` | Yes\* | – | Application (client) ID |
| `ENTRA_CLIENT_SECRET` | Yes\*\* | – | Client secret |
| `ENTRA_AUTH_MODE` | No | `application` | `application` or `delegated` |
| `ENTRA_SCOPES` | No | `https://graph.microsoft.com/.default` | Comma-separated scopes |

\* Required when authentication is enabled  \*\* Required for application mode

Full instructions: **[docs/authentication.md](docs/authentication.md)**.

---

## 🧪 Testing

```bash
pytest tests/                          # run the suite
pytest --cov=getset_pox_mcp tests/     # with coverage
```

---

## 🔧 Development

### Project structure

```
GetSetPOx/
├── getset_pox_mcp/              # Main package
│   ├── server.py                # Server entry point + tool registration
│   ├── config.py                # Configuration management
│   ├── logging_config.py        # Logging setup
│   ├── authentication/          # OAuth2 provider, middleware, token manager
│   ├── transport/               # Transport layer implementations
│   └── services/                # MCP services and tools (one folder per domain)
│       ├── diagnostics/         # Graph permission diagnostics
│       ├── eid/                 # Entra ID management
│       ├── iga/                 # Identity Governance
│       ├── intune/              # Intune device management
│       ├── internetAccess/      # Global Secure Access — Internet Access
│       ├── poc/                 # POC orchestration utilities
│       └── Test/                # hello_world, echo
├── docs/authentication.md       # Auth setup guide
├── scripts/                     # setup.bat / setup.sh
├── tests/                       # Test suite
├── BUILD_INSTRUCTIONS.md        # PyInstaller build guide
├── ENV_PACKAGING_GUIDE.md       # Configuration packaging guide
├── getset-pox-mcp.spec          # PyInstaller spec
├── pyproject.toml               # Project configuration
├── CHANGELOG.md · CONTRIBUTING.md · CODE_OF_CONDUCT.md · SECURITY.md
└── LICENSE
```

### Building a standalone executable

```bash
# Quick build (embeds .env)
prepare_env_for_build.bat        # Windows
./prepare_env_for_build.sh       # Linux/macOS

# Manual build
pip install pyinstaller
pyinstaller getset-pox-mcp.spec  # output in dist/ (~24 MB)
```

See **[BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md)** and
**[ENV_PACKAGING_GUIDE.md](ENV_PACKAGING_GUIDE.md)**.

### Adding a new service

1. Create a tool in `getset_pox_mcp/services/<domain>/`:

```python
from typing import Any

async def my_tool(param1: str, param2: int) -> dict[str, Any]:
    """Description of your tool.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Result dictionary
    """
    return {"result": "success"}
```

2. Register it in `getset_pox_mcp/server.py`:

```python
from .services.<domain>.my_tools import my_tool

# In register_tools():
@mcp.tool()
async def my_tool_handler(param1: str, param2: int) -> dict[str, Any]:
    """Tool description"""
    return await my_tool(param1, param2)
```

### Running in development

```bash
python -m getset_pox_mcp.server                 # STDIO transport
TRANSPORT=http python -m getset_pox_mcp.server  # HTTP transport
```

---

## 📋 Example Usage

Once configured, interact through any MCP-compatible client:

```
User:  Call the hello_world tool with name "Alice"
Agent: [calls hello_world]
Server: {"message": "Hello, Alice! Welcome to getset-pox-mcp."}

User:  Echo back "test message"
Agent: [calls echo]
Server: {
  "original": "test message",
  "echoed": "test message",
  "timestamp": "2025-01-16T19:40:00.000Z",
  "length": 12
}
```

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) and
[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

1. Fork the repository and create a feature branch
2. Make your changes with appropriate tests
3. Ensure `pytest` passes
4. Submit a pull request

---

## 📄 License

[MIT](LICENSE) — see the LICENSE file for details.

## 🔗 Resources

- [Model Context Protocol specification](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [fabric-rti-mcp reference](https://github.com/microsoft/fabric-rti-mcp)

## 📝 Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

# EntraID Authentication Guide

Complete guide for configuring and using EntraID (Azure AD) authentication with the getset-pox-mcp MCP server.

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Setup Guide](#setup-guide)
4. [Configuration](#configuration)
5. [Authentication Flows](#authentication-flows)
6. [Security Best Practices](#security-best-practices)
7. [Troubleshooting](#troubleshooting)
8. [API Reference](#api-reference)

---

## Overview

The getset-pox-mcp server supports Microsoft EntraID (formerly Azure AD) authentication for secure access to Microsoft Graph API and other Azure resources.

### Features

- **OAuth2 Authentication**: Industry-standard OAuth2/OpenID Connect
- **Multiple Auth Modes**: Application (daemon) and Delegated (user) authentication
- **Token Management**: Automatic token refresh and secure caching
- **MSAL Integration**: Uses Microsoft Authentication Library (MSAL) for Python
- **Secure by Default**: Follows Microsoft security best practices

### When to Use Authentication

Enable authentication when your MCP tools need to:
- Access Microsoft Graph API
- Call Azure services on behalf of the server
- Perform operations requiring specific permissions
- Access user-specific data (delegated mode)

---

## Architecture

### Authentication Flow Diagram

```
┌─────────────────┐
│   MCP Client    │
│  (Claude/IDE)   │
└────────┬────────┘
         │
         │ MCP Protocol
         │
         ▼
┌─────────────────────────────────────┐
│     MCP Server (getset-pox-mcp)     │
│  ┌──────────────────────────────┐   │
│  │  Authentication Middleware   │   │
│  └──────────┬───────────────────┘   │
│             │                        │
│             ▼                        │
│  ┌──────────────────────────────┐   │
│  │    EntraID Auth Provider     │   │
│  │  (MSAL + Token Manager)      │   │
│  └──────────┬───────────────────┘   │
│             │                        │
└─────────────┼────────────────────────┘
              │
              │ OAuth2/OIDC
              │
              ▼
     ┌────────────────────┐
     │  Microsoft EntraID │
     │  (Azure AD)        │
     └────────┬───────────┘
              │
              │ Access Token
              │
              ▼
     ┌────────────────────┐
     │  Microsoft Graph   │
     │  Other Azure APIs  │
     └────────────────────┘
```

### Components

1. **AuthConfig**: Configuration management for auth settings
2. **TokenManager**: Token storage, validation, and refresh
3. **EntraIDAuthProvider**: OAuth2 flows and MSAL integration
4. **AuthMiddleware**: Server integration and request handling

---

## Setup Guide

### Prerequisites

- Python 3.8 or higher
- Azure subscription (free tier works)
- Azure AD tenant
- Administrator access to Azure Portal

### Step 1: Create App Registration

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to **Azure Active Directory** → **App Registrations**
3. Click **+ New registration**
4. Fill in the details:
   - **Name**: `getset-pox-mcp` (or your preferred name)
   - **Supported account types**: Select based on your needs
   - **Redirect URI**: Leave blank for application mode
5. Click **Register**
6. **Note down**:
   - Application (client) ID
   - Directory (tenant) ID

### Step 2: Generate Client Secret

1. In your app registration, go to **Certificates & secrets**
2. Click **+ New client secret**
3. Add description: `MCP Server Secret`
4. Select expiry period (recommended: 6-12 months)
5. Click **Add**
6. **Copy the secret value immediately** (you won't see it again!)

### Step 3: Configure API Permissions

#### For Application (Daemon) Mode

1. Go to **API permissions**
2. Click **+ Add a permission**
3. Select **Microsoft Graph** → **Application permissions**
4. Add required permissions, for example:
   - `User.Read.All`
   - `Group.Read.All`
   - `Directory.Read.All`
5. Click **Add permissions**
6. Click **Grant admin consent** (requires admin)
7. Confirm the consent

#### For Delegated (User) Mode

1. Go to **API permissions**
2. Click **+ Add a permission**
3. Select **Microsoft Graph** → **Delegated permissions**
4. Add required permissions, for example:
   - `User.Read`
   - `Group.Read.All`
5. Click **Add permissions**
6. Admin consent may be required for some permissions

### Step 4: Install Dependencies

```bash
# Install MSAL library
pip install msal>=1.24.0

# Or reinstall all requirements
pip install -r requirements.txt
```

### Step 5: Configure Environment

1. Copy the authentication template:
   ```bash
   cp getset_pox_mcp/authentication/.env.auth.example .env
   ```

2. Edit `.env` with your values:
   ```bash
   # Required
   ENTRA_TENANT_ID=your-tenant-id-here
   ENTRA_CLIENT_ID=your-client-id-here
   ENTRA_CLIENT_SECRET=your-client-secret-here

   # Enable authentication
   ENTRA_ENABLE_AUTH=true

   # Set mode
   ENTRA_AUTH_MODE=application
   ```

3. Verify `.env` is in `.gitignore` (it should be by default)

### Step 6: Test Authentication

```bash
# Run the server
python -m getset_pox_mcp.server

# Check logs for:
# "Authentication: enabled=True, mode=application"
# "Server authentication successful"
```

---

## Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `ENTRA_TENANT_ID` | Yes | - | Azure AD tenant ID |
| `ENTRA_CLIENT_ID` | Yes | - | Application (client) ID |
| `ENTRA_CLIENT_SECRET` | Yes* | - | Client secret (*required for app mode) |
| `ENTRA_ENABLE_AUTH` | No | `false` | Enable authentication |
| `ENTRA_AUTH_MODE` | No | `application` | `application` or `delegated` |
| `ENTRA_SCOPES` | No | `https://graph.microsoft.com/.default` | Comma-separated scopes |
| `ENTRA_AUTHORITY` | No | Auto | Authority URL |
| `ENTRA_REDIRECT_URI` | No | `http://localhost:8000/callback` | Redirect URI (delegated mode) |
| `ENTRA_TOKEN_CACHE_PATH` | No | - | Token cache file path |

### Configuration in Code

```python
from getset_pox_mcp.authentication import AuthConfig, EntraIDAuthProvider

# Load from environment
config = AuthConfig.from_env()

# Or create manually
config = AuthConfig(
    tenant_id="your-tenant-id",
    client_id="your-client-id",
    client_secret="your-secret",
    enable_auth=True,
    auth_mode="application",
    scopes=["https://graph.microsoft.com/.default"]
)

# Initialize provider
provider = EntraIDAuthProvider(config)

# Get access token
token = await provider.get_access_token()
```

---

## Authentication Flows

### Application (Daemon) Mode

Best for server-to-server authentication without user interaction.

**Flow:**
1. Server starts
2. Requests token from EntraID using client credentials
3. Receives access token
4. Uses token for Microsoft Graph API calls
5. Token auto-refreshes when expired

**Use Cases:**
- Background processing
- Scheduled tasks
- Service accounts
- Reading organization data

**Configuration:**
```bash
ENTRA_AUTH_MODE=application
ENTRA_SCOPES=https://graph.microsoft.com/.default
```

### Delegated (User) Mode

For operations on behalf of a specific user.

**Flow:**
1. Server starts
2. Displays device code and URL
3. User visits URL and enters code
4. User authenticates and grants consent
5. Server receives access token and refresh token
6. Token auto-refreshes using refresh token

**Use Cases:**
- User-specific data access
- Operations requiring user consent
- Interactive workflows

**Configuration:**
```bash
ENTRA_AUTH_MODE=delegated
ENTRA_SCOPES=User.Read,Group.Read.All
```

---

## Security Best Practices

### 1. Secret Management

**DO:**
- ✅ Use environment variables for secrets
- ✅ Use Azure Key Vault in production
- ✅ Use Managed Identity when running in Azure
- ✅ Rotate secrets every 6-12 months
- ✅ Set appropriate secret expiry dates

**DON'T:**
- ❌ Hardcode secrets in code
- ❌ Commit `.env` files to git
- ❌ Share secrets in plain text
- ❌ Use long-lived secrets unnecessarily

### 2. Permission Scoping

**Principle of Least Privilege:**
- Only request permissions you actually need
- Prefer delegated permissions when possible
- Use specific scopes instead of broad permissions
- Regularly audit and remove unused permissions

**Example:**
```bash
# BAD: Requesting everything
ENTRA_SCOPES=https://graph.microsoft.com/.default

# GOOD: Specific permissions only
ENTRA_SCOPES=User.Read.All,Group.Read.All
```

### 3. Token Security

**Best Practices:**
- Tokens are sensitive - never log token values
- Use secure file permissions for token cache
- Clear tokens on error or logout
- Validate tokens before use
- Monitor token usage for anomalies

### 4. Network Security

- Use HTTPS for all production endpoints
- Implement rate limiting
- Monitor for suspicious authentication patterns
- Use firewall rules to restrict access
- Enable Azure AD Conditional Access policies

### 5. Error Handling

```python
try:
    token = await auth_provider.get_access_token()
    if not token:
        # Handle auth failure gracefully
        logger.error("Authentication failed")
        # Don't expose details to client
except Exception as e:
    # Log error but don't expose details
    logger.error(f"Auth error: {type(e).__name__}")
    # Clear potentially corrupted tokens
    auth_provider.clear_cache()
```

### 6. Audit and Monitoring

- Enable Azure AD sign-in logs
- Monitor authentication failures
- Set up alerts for suspicious activity
- Regularly review granted permissions
- Track token usage patterns

---

## Troubleshooting

### Common Issues

#### 1. "AADSTS7000215: Invalid client secret"

**Cause:** Client secret is incorrect or expired

**Solution:**
1. Generate new client secret in Azure Portal
2. Update `ENTRA_CLIENT_SECRET` in `.env`
3. Restart server

#### 2. "AADSTS65001: User or admin has not consented"

**Cause:** Permissions not granted or consent not provided

**Solution:**
1. Go to Azure Portal → App Registrations → API Permissions
2. Click "Grant admin consent"
3. Wait 5-10 minutes for propagation

#### 3. "AADSTS50020: User account from identity provider does not exist in tenant"

**Cause:** Wrong tenant ID or user not in tenant

**Solution:**
1. Verify `ENTRA_TENANT_ID` is correct
2. Ensure user exists in the tenant
3. Check supported account types in app registration

#### 4. "Authentication is disabled"

**Cause:** `ENTRA_ENABLE_AUTH` not set to `true`

**Solution:**
```bash
# In .env file
ENTRA_ENABLE_AUTH=true
```

#### 5. "Token expired" or "Token acquisition failed"

**Cause:** Token refresh failed or credentials invalid

**Solution:**
1. Clear token cache: Delete `.token_cache` file
2. Verify credentials are still valid
3. Check client secret hasn't expired
4. Restart server to re-authenticate

### Debugging Tips

1. **Enable debug logging:**
   ```bash
   LOG_LEVEL=DEBUG python -m getset_pox_mcp.server
   ```

2. **Check authentication status:**
   ```python
   from getset_pox_mcp.authentication.middleware import get_auth_middleware
   
   auth_middleware = get_auth_middleware()
   status = auth_middleware.get_auth_status()
   print(status)
   ```

3. **Test token acquisition:**
   ```python
   from getset_pox_mcp.authentication import AuthConfig, EntraIDAuthProvider
   
   config = AuthConfig.from_env()
   provider = EntraIDAuthProvider(config)
   token = await provider.get_access_token()
   print(f"Token obtained: {token is not None}")
   ```

4. **Verify permissions:**
   Use the `check_token_permissions` MCP tool to test permissions

---

## API Reference

### AuthConfig

Configuration class for authentication settings.

```python
class AuthConfig:
    def __init__(
        self,
        tenant_id: str,
        client_id: str,
        client_secret: Optional[str] = None,
        authority: Optional[str] = None,
        scopes: List[str] = ["https://graph.microsoft.com/.default"],
        redirect_uri: str = "http://localhost:8000/callback",
        enable_auth: bool = False,
        auth_mode: str = "application",
        token_cache_path: Optional[str] = None
    ):
        ...
    
    @classmethod
    def from_env(cls) -> "AuthConfig":
        """Load configuration from environment variables."""
        ...
    
    def validate(self) -> bool:
        """Validate the configuration."""
        ...
```

### EntraIDAuthProvider

OAuth2 authentication provider.

```python
class EntraIDAuthProvider:
    def __init__(self, config: AuthConfig):
        ...
    
    async def get_access_token(self, force_refresh: bool = False) -> Optional[str]:
        """Get a valid access token."""
        ...
    
    def clear_cache(self) -> None:
        """Clear all cached tokens."""
        ...
    
    def get_auth_status(self) -> Dict[str, Any]:
        """Get current authentication status."""
        ...
```

### AuthMiddleware

Middleware for server integration.

```python
class AuthMiddleware:
    def __init__(self, auth_config: Optional[AuthConfig] = None):
        ...
    
    async def authenticate_server(self) -> bool:
        """Authenticate during server startup."""
        ...
    
    async def get_valid_token(self) -> Optional[str]:
        """Get a valid access token."""
        ...
    
    def require_auth(self) -> Callable:
        """Decorator to require authentication."""
        ...
```

### Usage Example

```python
from getset_pox_mcp.authentication.middleware import get_auth_middleware

# Get middleware instance
auth_middleware = get_auth_middleware()

# Authenticate server
await auth_middleware.authenticate_server()

# Get token for API call
token = await auth_middleware.get_valid_token()

# Use decorator to protect functions
@auth_middleware.require_auth()
async def protected_function():
    # This function requires authentication
    pass
```

---

## Additional Resources

- [Microsoft Identity Platform Documentation](https://docs.microsoft.com/en-us/azure/active-directory/develop/)
- [MSAL Python Documentation](https://msal-python.readthedocs.io/)
- [Microsoft Graph API Reference](https://docs.microsoft.com/en-us/graph/api/overview)
- [Azure AD App Registration Guide](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app)
- [OAuth 2.0 Authorization Framework](https://oauth.net/2/)

---

## Support

For issues and questions:
1. Check this documentation
2. Review server logs with `LOG_LEVEL=DEBUG`
3. Check Azure AD sign-in logs in Azure Portal
4. Open an issue on GitHub with:
   - Error messages (sanitized, no secrets!)
   - Server logs
   - Configuration (without secrets!)
   - Steps to reproduce

---

*Last Updated: 2025-11-16*

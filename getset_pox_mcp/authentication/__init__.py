"""
EntraID (Azure AD) Authentication Module

This module provides OAuth2 authentication support for Microsoft EntraID (Azure AD)
for the getset-pox-mcp MCP server.

Components:
- auth_provider: Core OAuth2 authentication provider
- token_manager: Token validation and refresh logic
- auth_config: Configuration management for authentication
- middleware: Authentication hooks for server integration

Security Features:
- OAuth2 with PKCE support
- Secure token storage and refresh
- Token validation and expiry handling
- Support for both delegated and application permissions
"""

from getset_pox_mcp.authentication.auth_provider import EntraIDAuthProvider
from getset_pox_mcp.authentication.token_manager import TokenManager
from getset_pox_mcp.authentication.auth_config import AuthConfig

__all__ = ["EntraIDAuthProvider", "TokenManager", "AuthConfig"]

__version__ = "1.0.0"

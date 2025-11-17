"""
Authentication Configuration Module

Manages EntraID authentication configuration including client secrets,
app IDs, tenant IDs, and other authentication parameters.

Security Notes:
- Secrets should never be hardcoded
- Use environment variables or secure key vaults
- Follow principle of least privilege for permissions
"""

import os
from typing import Optional, List
from dataclasses import dataclass, field
from getset_pox_mcp.logging_config import get_logger

logger = get_logger(__name__)


@dataclass
class AuthConfig:
    """
    Configuration for EntraID (Azure AD) authentication.
    
    Attributes:
        tenant_id: Azure AD tenant ID
        client_id: Application (client) ID from Azure AD app registration
        client_secret: Application client secret (for confidential clients)
        authority: Authority URL (defaults to Azure public cloud)
        scopes: List of permission scopes to request
        redirect_uri: Redirect URI for OAuth2 flow
        enable_auth: Whether authentication is enabled
        auth_mode: Authentication mode ('delegated' or 'application')
        token_cache_path: Path to token cache file (optional)
    
    Security Considerations:
        - client_secret should be stored securely (environment variable or key vault)
        - Use managed identities in Azure when possible
        - Rotate secrets regularly
        - Use least privilege principle for scopes
    """
    
    # Required fields
    tenant_id: str
    client_id: str
    
    # Optional fields with defaults
    client_secret: Optional[str] = None
    authority: Optional[str] = None
    scopes: List[str] = field(default_factory=lambda: ["https://graph.microsoft.com/.default"])
    redirect_uri: str = "http://localhost:8000/callback"
    enable_auth: bool = False
    auth_mode: str = "application"  # 'delegated' or 'application'
    token_cache_path: Optional[str] = None
    
    def __post_init__(self):
        """Validate and set defaults after initialization."""
        # Set default authority if not provided
        if self.authority is None:
            self.authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        
        # Validate auth_mode
        if self.auth_mode not in ["delegated", "application"]:
            raise ValueError("auth_mode must be either 'delegated' or 'application'")
        
        # Warn if client_secret is missing for application mode
        if self.auth_mode == "application" and not self.client_secret:
            logger.warning(
                "Application mode requires client_secret. "
                "Authentication may fail without it."
            )
        
        # Validate scopes format
        if not isinstance(self.scopes, list) or not self.scopes:
            raise ValueError("scopes must be a non-empty list")
        
        logger.info(f"AuthConfig initialized: mode={self.auth_mode}, enabled={self.enable_auth}")
    
    @classmethod
    def from_env(cls) -> "AuthConfig":
        """
        Load authentication configuration from environment variables.
        
        Environment Variables:
            ENTRA_TENANT_ID: Azure AD tenant ID (required)
            ENTRA_CLIENT_ID: Application client ID (required)
            ENTRA_CLIENT_SECRET: Application client secret (required for app mode)
            ENTRA_AUTHORITY: Authority URL (optional)
            ENTRA_SCOPES: Comma-separated list of scopes (optional)
            ENTRA_REDIRECT_URI: OAuth redirect URI (optional)
            ENTRA_ENABLE_AUTH: Enable authentication (true/false)
            ENTRA_AUTH_MODE: Authentication mode ('delegated' or 'application')
            ENTRA_TOKEN_CACHE_PATH: Path to token cache file (optional)
        
        Returns:
            AuthConfig instance with values from environment
        
        Raises:
            ValueError: If required environment variables are missing
        """
        tenant_id = os.getenv("ENTRA_TENANT_ID")
        client_id = os.getenv("ENTRA_CLIENT_ID")
        
        if not tenant_id or not client_id:
            logger.warning(
                "ENTRA_TENANT_ID and ENTRA_CLIENT_ID not found. "
                "Authentication will be disabled."
            )
            # Return config with auth disabled
            return cls(
                tenant_id=tenant_id or "not-configured",
                client_id=client_id or "not-configured",
                enable_auth=False
            )
        
        # Parse scopes from comma-separated string
        scopes_str = os.getenv("ENTRA_SCOPES", "https://graph.microsoft.com/.default")
        scopes = [s.strip() for s in scopes_str.split(",") if s.strip()]
        
        # Parse enable_auth boolean
        enable_auth = os.getenv("ENTRA_ENABLE_AUTH", "false").lower() == "true"
        
        config = cls(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=os.getenv("ENTRA_CLIENT_SECRET"),
            authority=os.getenv("ENTRA_AUTHORITY"),
            scopes=scopes,
            redirect_uri=os.getenv("ENTRA_REDIRECT_URI", "http://localhost:8000/callback"),
            enable_auth=enable_auth,
            auth_mode=os.getenv("ENTRA_AUTH_MODE", "application"),
            token_cache_path=os.getenv("ENTRA_TOKEN_CACHE_PATH"),
        )
        
        logger.info(f"AuthConfig loaded from environment: enabled={enable_auth}")
        return config
    
    def validate(self) -> bool:
        """
        Validate the authentication configuration.
        
        Returns:
            True if configuration is valid, False otherwise
        
        Raises:
            ValueError: If configuration is invalid when auth is enabled
        """
        if not self.enable_auth:
            logger.info("Authentication is disabled")
            return True
        
        # Check required fields
        if not self.tenant_id or self.tenant_id == "not-configured":
            raise ValueError("tenant_id is required when authentication is enabled")
        
        if not self.client_id or self.client_id == "not-configured":
            raise ValueError("client_id is required when authentication is enabled")
        
        # Check mode-specific requirements
        if self.auth_mode == "application":
            if not self.client_secret:
                raise ValueError(
                    "client_secret is required for application authentication mode"
                )
        
        logger.info("AuthConfig validation successful")
        return True
    
    def get_safe_config(self) -> dict:
        """
        Get configuration dictionary with secrets masked for logging.
        
        Returns:
            Dictionary with configuration (secrets masked)
        """
        return {
            "tenant_id": self.tenant_id,
            "client_id": self.client_id,
            "client_secret": "***" if self.client_secret else None,
            "authority": self.authority,
            "scopes": self.scopes,
            "redirect_uri": self.redirect_uri,
            "enable_auth": self.enable_auth,
            "auth_mode": self.auth_mode,
            "token_cache_path": self.token_cache_path,
        }

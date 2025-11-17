"""
EntraID Authentication Provider Module

Core OAuth2 authentication provider for Microsoft EntraID (Azure AD).
Uses Microsoft Authentication Library (MSAL) for secure authentication.

Security Features:
- OAuth2 with PKCE support
- Secure token acquisition and refresh
- Support for delegated and application permissions
- Token validation and error handling
"""

from typing import Optional, Dict, Any, List
import asyncio
import msal
from getset_pox_mcp.authentication.auth_config import AuthConfig
from getset_pox_mcp.authentication.token_manager import TokenManager
from getset_pox_mcp.logging_config import get_logger

logger = get_logger(__name__)

class EntraIDAuthProvider:
    """
    OAuth2 authentication provider for Microsoft EntraID (Azure AD).
    
    Supports:
        - Application (daemon/service) authentication
        - Delegated (user) authentication with device code flow
        - Token caching and automatic refresh
        - Secure token handling
    
    Usage:
        ```python
        config = AuthConfig.from_env()
        provider = EntraIDAuthProvider(config)
        
        # Get access token
        token = await provider.get_access_token()
        ```
    """
    
    def __init__(self, config: AuthConfig):
        """
        Initialize the authentication provider.
        
        Args:
            config: Authentication configuration
        """
        self.config = config
        self.token_manager = TokenManager(cache_path=config.token_cache_path)
        self._msal_app: Optional[msal.ConfidentialClientApplication] = None
        
        # Initialize MSAL application if auth is enabled
        if config.enable_auth:
            self._initialize_msal_app()
        
        logger.info(f"EntraIDAuthProvider initialized (mode={config.auth_mode})")
    
    def _initialize_msal_app(self) -> None:
        """
        Initialize the MSAL application based on configuration.
        
        Raises:
            ValueError: If configuration is invalid
        """
        try:
            if self.config.auth_mode == "application":
                # Confidential client for application/daemon authentication
                self._msal_app = msal.ConfidentialClientApplication(
                    client_id=self.config.client_id,
                    client_credential=self.config.client_secret,
                    authority=self.config.authority,
                )
                logger.info("MSAL Confidential Client initialized")
            else:
                # Public client for delegated authentication
                self._msal_app = msal.PublicClientApplication(
                    client_id=self.config.client_id,
                    authority=self.config.authority,
                )
                logger.info("MSAL Public Client initialized")
                
        except Exception as e:
            logger.error(f"Failed to initialize MSAL application: {e}")
            raise ValueError(f"MSAL initialization failed: {e}")
    
    async def get_access_token(self, force_refresh: bool = False) -> Optional[str]:
        """
        Get a valid access token, refreshing if necessary.
        
        Args:
            force_refresh: Force token refresh even if current token is valid
        
        Returns:
            Access token string, or None if authentication fails
        
        Process:
            1. Check for cached valid token
            2. Try to refresh if expired
            3. Acquire new token if needed
        """
        if not self.config.enable_auth:
            logger.debug("Authentication is disabled")
            return None
        
        # Return cached token if valid and not forcing refresh
        if not force_refresh:
            # Run token_manager call in thread pool to avoid blocking on threading.Lock()
            cached_token = await asyncio.to_thread(self.token_manager.get_access_token)
            if cached_token:
                logger.debug("Using cached access token")
                return cached_token
        
        # Try to refresh token
        # Run token_manager call in thread pool to avoid blocking on threading.Lock()
        refresh_token = await asyncio.to_thread(self.token_manager.get_refresh_token)
        if refresh_token:
            logger.info("Attempting to refresh access token")
            token = await self._refresh_token()
            if token:
                return token
        
        # Acquire new token
        logger.info("Acquiring new access token")
        return await self._acquire_token()
    
    async def _acquire_token(self) -> Optional[str]:
        """
        Acquire a new access token based on authentication mode.
        
        Returns:
            Access token string, or None if acquisition fails
        """
        try:
            if self.config.auth_mode == "application":
                return await self._acquire_token_for_application()
            else:
                return await self._acquire_token_for_user()
        except Exception as e:
            logger.error(f"Token acquisition failed: {e}")
            return None
    
    async def _acquire_token_for_application(self) -> Optional[str]:
        """
        Acquire token using client credentials flow (application permissions).
        
        Returns:
            Access token string, or None if acquisition fails
        """
        if not self._msal_app:
            logger.error("MSAL application not initialized")
            return None
        
        try:
            # Run synchronous MSAL call in thread pool to avoid blocking
            result = await asyncio.to_thread(
                self._msal_app.acquire_token_for_client,
                scopes=self.config.scopes
            )
            
            if "access_token" in result:
                # Store tokens
                self.token_manager.store_tokens(
                    access_token=result["access_token"],
                    expires_in=result.get("expires_in", 3600)
                )
                logger.info("Application token acquired successfully")
                return result["access_token"]
            else:
                error = result.get("error")
                error_desc = result.get("error_description")
                logger.error(f"Token acquisition failed: {error} - {error_desc}")
                return None
                
        except Exception as e:
            logger.error(f"Exception during token acquisition: {e}")
            return None
    
    async def _acquire_token_for_user(self) -> Optional[str]:
        """
        Acquire token using device code flow (delegated permissions).
        
        Returns:
            Access token string, or None if acquisition fails
        
        Note:
            This flow requires user interaction to complete authentication.
        """
        if not self._msal_app:
            logger.error("MSAL application not initialized")
            return None
        
        try:
            # Initiate device code flow (run in thread pool)
            flow = await asyncio.to_thread(
                self._msal_app.initiate_device_flow,
                scopes=self.config.scopes
            )
            
            if "user_code" not in flow:
                logger.error("Failed to create device flow")
                return None
            
            # Display user code and URL
            logger.info(f"Device code flow initiated:")
            logger.info(f"  {flow['message']}")
            print(f"\n{flow['message']}\n")
            
            # Wait for user to complete authentication (run in thread pool)
            result = await asyncio.to_thread(
                self._msal_app.acquire_token_by_device_flow,
                flow
            )
            
            if "access_token" in result:
                # Store tokens including refresh token
                self.token_manager.store_tokens(
                    access_token=result["access_token"],
                    refresh_token=result.get("refresh_token"),
                    expires_in=result.get("expires_in", 3600)
                )
                logger.info("User token acquired successfully")
                return result["access_token"]
            else:
                error = result.get("error")
                error_desc = result.get("error_description")
                logger.error(f"Token acquisition failed: {error} - {error_desc}")
                return None
                
        except Exception as e:
            logger.error(f"Exception during device code flow: {e}")
            return None
    
    async def _refresh_token(self) -> Optional[str]:
        """
        Refresh the access token using the refresh token.
        
        Returns:
            New access token string, or None if refresh fails
        
        Note:
            Only applicable for delegated authentication mode.
        """
        if self.config.auth_mode != "delegated":
            logger.debug("Token refresh not applicable for application mode")
            return None
        
        # Run token_manager call in thread pool to avoid blocking on threading.Lock()
        refresh_token = await asyncio.to_thread(self.token_manager.get_refresh_token)
        if not refresh_token:
            logger.debug("No refresh token available")
            return None
        
        if not self._msal_app:
            logger.error("MSAL application not initialized")
            return None
        
        try:
            # Run synchronous MSAL call in thread pool to avoid blocking
            result = await asyncio.to_thread(
                self._msal_app.acquire_token_by_refresh_token,
                refresh_token=refresh_token,
                scopes=self.config.scopes
            )
            
            if "access_token" in result:
                # Store refreshed tokens
                self.token_manager.store_tokens(
                    access_token=result["access_token"],
                    refresh_token=result.get("refresh_token", refresh_token),
                    expires_in=result.get("expires_in", 3600)
                )
                logger.info("Token refreshed successfully")
                return result["access_token"]
            else:
                error = result.get("error")
                logger.warning(f"Token refresh failed: {error}")
                # Clear tokens on refresh failure
                self.token_manager.clear_tokens()
                return None
                
        except Exception as e:
            logger.error(f"Exception during token refresh: {e}")
            self.token_manager.clear_tokens()
            return None
    
    def clear_cache(self) -> None:
        """
        Clear all cached tokens and authentication state.
        
        Use when:
        - User logs out
        - Switching accounts
        - Authentication errors that require re-authentication
        """
        self.token_manager.clear_tokens()
        logger.info("Authentication cache cleared")
    
    def get_auth_status(self) -> Dict[str, Any]:
        """
        Get current authentication status.
        
        Returns:
            Dictionary with authentication status information
        """
        token_info = self.token_manager.get_token_info()
        return {
            "enabled": self.config.enable_auth,
            "mode": self.config.auth_mode,
            "authenticated": token_info["has_access_token"] and not token_info["is_expired"],
            "token_info": token_info,
        }
    
    def validate_token(self, token: str) -> bool:
        """
        Validate an access token (basic validation).
        
        Args:
            token: Access token to validate
        
        Returns:
            True if token appears valid, False otherwise
        
        Note:
            This is a basic validation. For production, implement
            full JWT validation with signature verification.
        """
        if not token:
            return False
        
        # Basic checks
        if len(token) < 10:
            return False
        
        # Token should be a JWT (has 3 parts separated by dots)
        parts = token.split(".")
        if len(parts) != 3:
            logger.warning("Token format invalid (not a JWT)")
            return False
        
        # TODO: Implement full JWT validation
        # - Verify signature
        # - Check expiry
        # - Validate issuer
        # - Check audience
        
        return True

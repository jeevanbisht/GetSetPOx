"""
Authentication Middleware Module

Provides authentication hooks and middleware for the MCP server.
Integrates EntraID authentication into server startup and tool invocation.

Security Features:
- Pre-authentication checks
- Token validation on requests
- Automatic token refresh
- Error handling and logging
"""

from typing import Optional, Callable, Any
from functools import wraps
from getset_pox_mcp.authentication.auth_provider import EntraIDAuthProvider
from getset_pox_mcp.authentication.auth_config import AuthConfig
from getset_pox_mcp.logging_config import get_logger

logger = get_logger(__name__)

class AuthMiddleware:
    """
    Middleware for handling authentication in the MCP server.
    
    Features:
        - Server startup authentication
        - Per-request authentication checks
        - Token refresh handling
        - Authentication error handling
    """
    
    def __init__(self, auth_config: Optional[AuthConfig] = None):
        """
        Initialize the authentication middleware.
        
        Args:
            auth_config: Authentication configuration (loads from env if None)
        """
        self.config = auth_config or AuthConfig.from_env()
        self.auth_provider: Optional[EntraIDAuthProvider] = None
        
        # Initialize provider if authentication is enabled
        if self.config.enable_auth:
            try:
                self.config.validate()
                self.auth_provider = EntraIDAuthProvider(self.config)
                logger.info("Authentication middleware initialized")
            except Exception as e:
                logger.error(f"Failed to initialize auth middleware: {e}")
                raise
        else:
            logger.info("Authentication is disabled")
    
    async def authenticate_server(self) -> bool:
        """
        Perform authentication during server startup.
        
        Returns:
            True if authentication successful or disabled, False otherwise
        
        Use:
            Call this during server initialization to ensure auth is ready
        """
        if not self.config.enable_auth:
            logger.info("Authentication disabled, skipping server auth")
            return True
        
        if not self.auth_provider:
            logger.error("Auth provider not initialized")
            return False
        
        try:
            logger.info("Authenticating server...")
            token = await self.auth_provider.get_access_token()
            
            if token:
                logger.info("Server authentication successful")
                return True
            else:
                logger.error("Server authentication failed - no token obtained")
                return False
                
        except Exception as e:
            logger.error(f"Server authentication error: {e}")
            return False
    
    async def get_valid_token(self) -> Optional[str]:
        """
        Get a valid access token for making authenticated requests.
        
        Returns:
            Valid access token or None if auth disabled/failed
        """
        if not self.config.enable_auth:
            return None
        
        if not self.auth_provider:
            logger.warning("Auth provider not available")
            return None
        
        try:
            return await self.auth_provider.get_access_token()
        except Exception as e:
            logger.error(f"Failed to get access token: {e}")
            return None
    
    def require_auth(self) -> Callable:
        """
        Decorator to require authentication for a function/method.
        
        Usage:
            ```python
            @auth_middleware.require_auth()
            async def protected_function():
                # This function requires authentication
                pass
            ```
        
        Returns:
            Decorator function
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            async def wrapper(*args, **kwargs):
                # Skip auth check if disabled
                if not self.config.enable_auth:
                    return await func(*args, **kwargs)
                
                # Check for valid token
                token = await self.get_valid_token()
                if not token:
                    error_msg = "Authentication required but no valid token available"
                    logger.error(error_msg)
                    raise PermissionError(error_msg)
                
                # Call original function
                return await func(*args, **kwargs)
            
            return wrapper
        return decorator
    
    def get_auth_headers(self, token: Optional[str] = None) -> dict:
        """
        Get HTTP headers with authentication token.
        
        Args:
            token: Optional token to use (gets new token if None)
        
        Returns:
            Dictionary with Authorization header
        """
        if not token and self.auth_provider:
            # This is sync but auth_provider methods are async
            # In production, you may need to handle this differently
            logger.warning("Sync call to get auth headers - token should be pre-fetched")
        
        if token:
            return {"Authorization": f"Bearer {token}"}
        return {}
    
    def get_auth_status(self) -> dict:
        """
        Get current authentication status.
        
        Returns:
            Dictionary with authentication status
        """
        if not self.config.enable_auth:
            return {
                "enabled": False,
                "authenticated": False,
                "message": "Authentication is disabled",
                "mode": None
            }
        
        if not self.auth_provider:
            return {
                "enabled": True,
                "authenticated": False,
                "message": "Auth provider not initialized",
                "mode": self.config.auth_mode
            }
        
        # Return basic status without calling token_manager.get_token_info()
        # which uses threading.Lock() and can block async code
        return {
            "enabled": self.config.enable_auth,
            "mode": self.config.auth_mode,
            "authenticated": False,  # Will be true after successful auth
            "message": "Auth provider initialized"
        }
    
    async def clear_auth(self) -> None:
        """
        Clear authentication state and cached tokens.
        
        Use when:
        - User logs out
        - Authentication error requires re-auth
        - Switching accounts
        """
        if self.auth_provider:
            self.auth_provider.clear_cache()
            logger.info("Authentication cleared")


# Global middleware instance
_auth_middleware: Optional[AuthMiddleware] = None

def get_auth_middleware(config: Optional[AuthConfig] = None) -> AuthMiddleware:
    """
    Get or create the global authentication middleware instance.
    
    Args:
        config: Optional authentication configuration
    
    Returns:
        AuthMiddleware instance
    """
    global _auth_middleware
    
    if _auth_middleware is None:
        _auth_middleware = AuthMiddleware(config)
        logger.info("Global auth middleware created")
    
    return _auth_middleware


def reset_auth_middleware() -> None:
    """
    Reset the global authentication middleware instance.
    
    Use for testing or when reconfiguration is needed.
    """
    global _auth_middleware
    _auth_middleware = None
    logger.info("Global auth middleware reset")

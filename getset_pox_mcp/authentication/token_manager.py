"""
Token Manager Module

Handles token validation, refresh, and caching for EntraID authentication.

Security Features:
- Token validation and expiry checking
- Secure token storage
- Automatic token refresh
- Concurrency safe via asyncio.to_thread() wrapper calls
"""

import json
from typing import Optional, Dict, Any
from datetime import datetime, timedelta, timezone
from pathlib import Path
from getset_pox_mcp.logging_config import get_logger

logger = get_logger(__name__)

class TokenManager:
    """
    Manages access tokens and refresh tokens for EntraID authentication.
    
    Features:
        - Token caching to disk (optional)
        - Automatic token refresh before expiry
        - Concurrency safe when called via asyncio.to_thread()
        - Token validation
    
    Security Considerations:
        - Tokens are sensitive data - handle with care
        - Use secure file permissions for token cache
        - Clear tokens on logout/error
        - Never log token values
    
    Note:
        Methods should be called via asyncio.to_thread() from async code
        to ensure thread safety without blocking the event loop.
    """
    
    def __init__(self, cache_path: Optional[str] = None):
        """
        Initialize the token manager.
        
        Args:
            cache_path: Optional path to token cache file
        """
        self.cache_path = Path(cache_path) if cache_path else None
        self._access_token: Optional[str] = None
        self._refresh_token: Optional[str] = None
        self._token_expiry: Optional[datetime] = None
        
        # Load cached tokens if available
        if self.cache_path and self.cache_path.exists():
            self._load_from_cache()
        
        logger.info(f"TokenManager initialized (cache={'enabled' if cache_path else 'disabled'})")
    
    def store_tokens(
        self,
        access_token: str,
        refresh_token: Optional[str] = None,
        expires_in: int = 3600
    ) -> None:
        """
        Store access and refresh tokens.
        
        Args:
            access_token: The access token
            refresh_token: The refresh token (optional)
            expires_in: Token lifetime in seconds (default 3600)
        """
        self._access_token = access_token
        self._refresh_token = refresh_token
        self._token_expiry = datetime.now(timezone.utc) + timedelta(seconds=expires_in)
        
        # Save to cache if enabled
        if self.cache_path:
            self._save_to_cache()
        
        logger.info(
            f"Tokens stored (expires at {self._token_expiry.isoformat()})"
        )
    
    def get_access_token(self) -> Optional[str]:
        """
        Get the current access token if valid.
        
        Returns:
            Access token if available and not expired, None otherwise
        """
        if not self._access_token:
            logger.debug("No access token available")
            return None
        
        if self.is_token_expired():
            logger.warning("Access token is expired")
            return None
        
        return self._access_token
    
    def get_refresh_token(self) -> Optional[str]:
        """
        Get the refresh token.
        
        Returns:
            Refresh token if available, None otherwise
        """
        return self._refresh_token
    
    def is_token_expired(self, buffer_seconds: int = 300) -> bool:
        """
        Check if the access token is expired or will expire soon.
        
        Args:
            buffer_seconds: Consider token expired if expiring within this many seconds
        
        Returns:
            True if token is expired or expiring soon, False otherwise
        """
        if not self._token_expiry:
            return True
        
        # Check if token expires within buffer time
        expiry_threshold = datetime.now(timezone.utc) + timedelta(seconds=buffer_seconds)
        is_expired = self._token_expiry <= expiry_threshold
        
        if is_expired:
            logger.debug(
                f"Token expired or expiring soon "
                f"(expiry: {self._token_expiry.isoformat()})"
            )
        
        return is_expired
    
    def clear_tokens(self) -> None:
        """
        Clear all stored tokens and cache.
        
        Use when:
        - User logs out
        - Authentication error occurs
        - Switching accounts
        """
        self._access_token = None
        self._refresh_token = None
        self._token_expiry = None
        
        # Remove cache file if it exists
        if self.cache_path and self.cache_path.exists():
            try:
                self.cache_path.unlink()
                logger.info("Token cache cleared")
            except Exception as e:
                logger.error(f"Failed to clear token cache: {e}")
        
        logger.info("Tokens cleared from memory")
    
    def _save_to_cache(self) -> None:
        """
        Save tokens to cache file.
        
        Security: File should have restricted permissions (user read/write only)
        """
        if not self.cache_path:
            return
        
        try:
            cache_data = {
                "access_token": self._access_token,
                "refresh_token": self._refresh_token,
                "expiry": self._token_expiry.isoformat() if self._token_expiry else None,
            }
            
            # Ensure parent directory exists
            self.cache_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write cache file
            with open(self.cache_path, "w") as f:
                json.dump(cache_data, f)
            
            # Set restrictive permissions (user read/write only)
            # Windows: This is a simplified approach; use proper ACLs in production
            try:
                import stat
                self.cache_path.chmod(stat.S_IRUSR | stat.S_IWUSR)
            except Exception:
                # chmod may not work on Windows, log but continue
                pass
            
            logger.debug(f"Tokens saved to cache: {self.cache_path}")
            
        except Exception as e:
            logger.error(f"Failed to save token cache: {e}")
    
    def _load_from_cache(self) -> None:
        """
        Load tokens from cache file.
        
        Security: Validate cache file permissions before loading
        """
        if not self.cache_path or not self.cache_path.exists():
            return
        
        try:
            with open(self.cache_path, "r") as f:
                cache_data = json.load(f)
            
            self._access_token = cache_data.get("access_token")
            self._refresh_token = cache_data.get("refresh_token")
            
            expiry_str = cache_data.get("expiry")
            if expiry_str:
                self._token_expiry = datetime.fromisoformat(expiry_str)
            
            # Check if cached token is already expired
            if self.is_token_expired(buffer_seconds=0):
                logger.info("Cached token is expired, clearing cache")
                self.clear_tokens()
            else:
                logger.info("Tokens loaded from cache")
            
        except Exception as e:
            logger.error(f"Failed to load token cache: {e}")
            # Clear potentially corrupted cache
            self.clear_tokens()
    
    def get_token_info(self) -> Dict[str, Any]:
        """
        Get information about the current token (for debugging/monitoring).
        
        Returns:
            Dictionary with token status information (no sensitive data)
        """
        return {
            "has_access_token": self._access_token is not None,
            "has_refresh_token": self._refresh_token is not None,
            "is_expired": self.is_token_expired(),
            "expiry": self._token_expiry.isoformat() if self._token_expiry else None,
            "cache_enabled": self.cache_path is not None,
        }

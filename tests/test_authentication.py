"""
Tests for the authentication module.
"""

import pytest
from getset_pox_mcp.authentication.auth_config import AuthConfig
from getset_pox_mcp.authentication.token_manager import TokenManager
from getset_pox_mcp.authentication.middleware import AuthMiddleware, reset_auth_middleware
from datetime import datetime, timedelta, timezone

class TestAuthConfig:
    """Tests for AuthConfig class."""
    
    def test_auth_config_creation(self):
        """Test creating AuthConfig with required fields."""
        config = AuthConfig(
            tenant_id="test-tenant",
            client_id="test-client",
            enable_auth=False
        )
        assert config.tenant_id == "test-tenant"
        assert config.client_id == "test-client"
        assert config.enable_auth is False
    
    def test_auth_config_defaults(self):
        """Test default values in AuthConfig."""
        config = AuthConfig(
            tenant_id="test-tenant",
            client_id="test-client"
        )
        assert config.auth_mode == "application"
        assert config.enable_auth is False
        assert config.scopes == ["https://graph.microsoft.com/.default"]
        assert config.authority == "https://login.microsoftonline.com/test-tenant"
    
    def test_auth_config_validation_disabled(self):
        """Test validation when auth is disabled."""
        config = AuthConfig(
            tenant_id="test",
            client_id="test",
            enable_auth=False
        )
        assert config.validate() is True
    
    def test_auth_config_validation_enabled_missing_secret(self):
        """Test validation fails when secret is missing in application mode."""
        config = AuthConfig(
            tenant_id="test",
            client_id="test",
            enable_auth=True,
            auth_mode="application"
        )
        with pytest.raises(ValueError, match="client_secret is required"):
            config.validate()
    
    def test_auth_config_invalid_mode(self):
        """Test that invalid auth mode raises error."""
        with pytest.raises(ValueError, match="auth_mode must be either"):
            AuthConfig(
                tenant_id="test",
                client_id="test",
                auth_mode="invalid"
            )
    
    def test_auth_config_safe_config(self):
        """Test that get_safe_config masks secrets."""
        config = AuthConfig(
            tenant_id="test-tenant",
            client_id="test-client",
            client_secret="super-secret"
        )
        safe_config = config.get_safe_config()
        assert safe_config["client_secret"] == "***"
        assert safe_config["tenant_id"] == "test-tenant"


class TestTokenManager:
    """Tests for TokenManager class."""
    
    def test_token_manager_initialization(self, tmp_path):
        """Test TokenManager initialization."""
        cache_path = tmp_path / "token_cache.json"
        manager = TokenManager(cache_path=str(cache_path))
        assert manager.cache_path == cache_path
    
    def test_store_and_retrieve_token(self):
        """Test storing and retrieving tokens."""
        manager = TokenManager()
        manager.store_tokens(
            access_token="test-token",
            refresh_token="test-refresh",
            expires_in=3600
        )
        
        token = manager.get_access_token()
        assert token == "test-token"
        
        refresh = manager.get_refresh_token()
        assert refresh == "test-refresh"
    
    def test_token_expiry_check(self):
        """Test token expiry detection."""
        manager = TokenManager()
        
        # Store expired token (expires in 1 second)
        manager.store_tokens(
            access_token="test-token",
            expires_in=1
        )
        
        # Should not be expired immediately
        assert not manager.is_token_expired(buffer_seconds=0)
        
        # Should be expired with large buffer
        assert manager.is_token_expired(buffer_seconds=3600)
    
    def test_clear_tokens(self):
        """Test clearing tokens."""
        manager = TokenManager()
        manager.store_tokens(access_token="test-token")
        
        assert manager.get_access_token() is not None
        
        manager.clear_tokens()
        
        assert manager.get_access_token() is None
        assert manager.get_refresh_token() is None
    
    def test_token_info(self):
        """Test getting token information."""
        manager = TokenManager()
        manager.store_tokens(
            access_token="test-token",
            refresh_token="test-refresh"
        )
        
        info = manager.get_token_info()
        assert info["has_access_token"] is True
        assert info["has_refresh_token"] is True
        assert "expiry" in info


class TestAuthMiddleware:
    """Tests for AuthMiddleware class."""
    
    def teardown_method(self):
        """Clean up after each test."""
        reset_auth_middleware()
    
    def test_middleware_initialization_disabled(self):
        """Test middleware initialization with auth disabled."""
        config = AuthConfig(
            tenant_id="test",
            client_id="test",
            enable_auth=False
        )
        middleware = AuthMiddleware(config)
        assert middleware.config.enable_auth is False
        assert middleware.auth_provider is None
    
    def test_middleware_get_auth_status_disabled(self):
        """Test getting auth status when disabled."""
        config = AuthConfig(
            tenant_id="test",
            client_id="test",
            enable_auth=False
        )
        middleware = AuthMiddleware(config)
        status = middleware.get_auth_status()
        
        assert status["enabled"] is False
        assert status["authenticated"] is False
    
    @pytest.mark.asyncio
    async def test_authenticate_server_disabled(self):
        """Test server authentication when auth is disabled."""
        config = AuthConfig(
            tenant_id="test",
            client_id="test",
            enable_auth=False
        )
        middleware = AuthMiddleware(config)
        result = await middleware.authenticate_server()
        assert result is True  # Should succeed when disabled
    
    @pytest.mark.asyncio
    async def test_get_valid_token_disabled(self):
        """Test getting token when auth is disabled."""
        config = AuthConfig(
            tenant_id="test",
            client_id="test",
            enable_auth=False
        )
        middleware = AuthMiddleware(config)
        token = await middleware.get_valid_token()
        assert token is None  # No token when disabled
    
    def test_get_auth_headers_with_token(self):
        """Test generating auth headers with token."""
        config = AuthConfig(
            tenant_id="test",
            client_id="test",
            enable_auth=False
        )
        middleware = AuthMiddleware(config)
        headers = middleware.get_auth_headers(token="test-token")
        
        assert "Authorization" in headers
        assert headers["Authorization"] == "Bearer test-token"
    
    def test_get_auth_headers_without_token(self):
        """Test generating auth headers without token."""
        config = AuthConfig(
            tenant_id="test",
            client_id="test",
            enable_auth=False
        )
        middleware = AuthMiddleware(config)
        headers = middleware.get_auth_headers()
        
        assert headers == {}


class TestAuthIntegration:
    """Integration tests for authentication components."""
    
    def test_auth_config_to_middleware_flow(self):
        """Test complete flow from config to middleware."""
        # Create config
        config = AuthConfig(
            tenant_id="test-tenant",
            client_id="test-client",
            enable_auth=False
        )
        
        # Initialize middleware
        middleware = AuthMiddleware(config)
        
        # Check status
        status = middleware.get_auth_status()
        assert status["enabled"] is False
    
    def test_token_manager_caching(self, tmp_path):
        """Test token caching to disk."""
        cache_path = tmp_path / "tokens.json"
        
        # Create manager and store token
        manager1 = TokenManager(cache_path=str(cache_path))
        manager1.store_tokens(
            access_token="cached-token",
            expires_in=3600
        )
        
        # Verify cache file exists
        assert cache_path.exists()
        
        # Create new manager with same cache path
        manager2 = TokenManager(cache_path=str(cache_path))
        
        # Should load cached token
        token = manager2.get_access_token()
        assert token == "cached-token"

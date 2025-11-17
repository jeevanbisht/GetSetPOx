# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)

## [Unreleased]

### Added
- **EntraID Authentication**: Full OAuth2 authentication support for Microsoft Entra ID (Azure AD)
  - Application (daemon) authentication mode with client credentials
  - Delegated (user) authentication mode with device code flow
  - Automatic token refresh and secure caching
  - MSAL (Microsoft Authentication Library) integration
- **Diagnostics Tool**: `check_token_permissions` - Comprehensive Microsoft Graph API permission testing
  - Tests 19 critical permissions with real API calls
  - Detailed success/failure reporting with actionable recommendations
  - Identifies missing permissions and provides setup guidance
- **Authentication Middleware**: Global authentication layer with background token acquisition
- **Token Manager**: Secure token storage and management without blocking async operations

### Changed
- **Improved Performance**: Removed threading locks from TokenManager to prevent event loop blocking
- **Better Logging**: Removed debug print statements, using proper logger throughout
- **Enhanced Error Handling**: Better timeout handling and error messages for authentication
- **Code Cleanup**: Removed unused imports and refactored for better maintainability

### Fixed
- **Threading Issues**: Resolved asyncio event loop blocking caused by threading.Lock()
- **Authentication Flow**: Background authentication prevents server startup delays
- **Token Acquisition**: Non-blocking token retrieval using asyncio.to_thread()
- **RuntimeWarning**: Fixed module import warning by removing premature server.py import

### Security
- Secure token caching with restricted file permissions
- No sensitive data in logs
- Token validation and automatic expiry checking
- OAuth2 best practices with PKCE support

## [0.1.0] - 2025-01-16

### Added
- Initial release of getset-pox-mcp
- MCP server implementation with STDIO and HTTP transport support
- HelloWorld service with personalized greeting functionality
- Echo service with message echoing and metadata
- Comprehensive configuration management via environment variables
- Structured logging with file and console output
- Modular services architecture for easy extension
- Complete test suite with pytest
- Documentation and usage examples
- Project structure based on fabric-rti-mcp best practices

### Features
- **Transport Protocols**: Support for both STDIO and HTTP transports
- **Configuration**: Environment variable-based configuration
- **Logging**: Structured logging with configurable levels
- **Error Handling**: Robust error handling and validation
- **Extensibility**: Clean architecture for adding new services
- **Testing**: Comprehensive test coverage with pytest

### Tools
- `hello_world`: Generate personalized greeting messages
- `echo`: Echo messages with metadata and optional uppercase conversion

[0.1.0]: https://github.com/yourusername/getset-pox-mcp/releases/tag/v0.1.0

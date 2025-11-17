# Security Policy

## Supported Versions

We release patches for security vulnerabilities. Currently supported versions:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

We take the security of getset-pox-mcp seriously. If you believe you have found a security vulnerability, please report it to us as described below.

### Please do NOT:

- Open a public GitHub issue for security vulnerabilities
- Discuss the vulnerability publicly until it has been addressed

### Please DO:

1. **Report via GitHub Security Advisory**
   - Go to the Security tab in the GitHub repository
   - Click "Report a vulnerability"
   - Provide detailed information about the vulnerability

2. **Include in your report:**
   - Type of vulnerability (e.g., authentication bypass, injection, etc.)
   - Full paths of affected source file(s)
   - Location of the affected source code (tag/branch/commit or direct URL)
   - Step-by-step instructions to reproduce the issue
   - Proof-of-concept or exploit code (if possible)
   - Impact of the issue, including how an attacker might exploit it

3. **Response Timeline:**
   - We will acknowledge receipt of your vulnerability report within 48 hours
   - We will provide a detailed response within 5 business days
   - We will work with you to understand and validate the issue
   - We will develop and test a fix
   - We will release a security advisory and patched version
   - We will credit you in the advisory (unless you prefer to remain anonymous)

## Security Best Practices for Users

When deploying getset-pox-mcp:

### Authentication Configuration

- **Never commit** `.env` files or credentials to version control
- Use environment variables for all sensitive configuration
- Rotate credentials regularly
- Use the principle of least privilege when configuring Azure AD app permissions
- Keep `client_secret` values secure and never log them

### Token Management

- Tokens are cached locally with restricted file permissions (0600)
- Token cache files are automatically excluded via `.gitignore`
- Review token cache location: `~/.mcp_token_cache.json`
- Consider implementing additional encryption for token storage in production

### Network Security

- When using HTTP transport mode:
  - Always use HTTPS in production
  - Implement proper authentication middleware
  - Use firewall rules to restrict access
  - Consider using a reverse proxy with additional security features

### Dependency Security

- Regularly update dependencies: `pip install --upgrade -r requirements.txt`
- Monitor security advisories for dependencies
- Use tools like `pip-audit` or `safety` to scan for vulnerabilities
- Review the `requirements.txt` file for outdated packages

### Logging Security

- Log files may contain sensitive information
- Ensure log files have appropriate permissions
- Rotate logs regularly
- Avoid logging credentials, tokens, or PII
- Review logging configuration in `logging_config.py`

### Deployment Security

- Use dedicated service accounts with minimal permissions
- Run the server in a sandboxed environment
- Implement rate limiting and request validation
- Monitor for unusual activity or errors
- Keep Python and system packages up to date

## Security Features

This project implements several security features:

- **OAuth2 Authentication** with MSAL (Microsoft Authentication Library)
- **Token Validation** and automatic refresh
- **Secure Token Caching** with restricted file permissions
- **Input Validation** for all tool parameters
- **Error Handling** that prevents information disclosure
- **Logging Controls** to prevent credential exposure
- **Environment-based Configuration** for secrets management

## Known Security Considerations

### Development vs. Production

- This is a development/demonstration server
- Additional hardening is recommended for production deployments
- Consider implementing:
  - Rate limiting
  - Request size limits
  - IP whitelisting
  - Additional authentication layers
  - Comprehensive audit logging

### MCP Protocol Security

- STDIO transport: Inherits security from the calling process
- HTTP transport: Requires additional security measures
  - Always use HTTPS
  - Implement proper authentication
  - Validate all inputs
  - Use CORS policies appropriately

## Security Updates

Security updates will be released as patch versions. Subscribe to:

- GitHub Security Advisories for this repository
- GitHub Releases for update notifications
- Watch this repository for security-related issues

## Acknowledgments

We appreciate the security research community and will acknowledge contributors who responsibly disclose vulnerabilities (unless they prefer to remain anonymous).

## Questions?

If you have questions about security that don't involve reporting a vulnerability, please open a regular GitHub issue with the `security` label.

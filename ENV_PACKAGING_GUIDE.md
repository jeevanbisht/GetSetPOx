# .env File Packaging Guide

This guide explains how to package configuration files with your standalone executable and the security considerations involved.

---

## Overview

The getset-pox-mcp build system supports two approaches for handling configuration:

1. **Embedded .env** - Configuration is bundled inside the executable
2. **External .env** - Configuration is provided separately at runtime

---

## Option 1: Embedded .env File

### When to Use
- Internal deployments within your organization
- Controlled environments where executable security is managed
- Situations where configuration convenience outweighs security concerns
- Development and testing environments

### How It Works

When you build with the helper scripts (`prepare_env_for_build.bat` or `prepare_env_for_build.sh`):

1. The script checks for `.env` in your project root
2. If not found, it creates one from `.env.example`
3. You can edit the `.env` file with your credentials
4. PyInstaller bundles the `.env` file into the executable
5. At runtime, the executable extracts `.env` to its temporary directory
6. The application reads configuration from the extracted file

### Building with Embedded .env

**Windows:**
```cmd
prepare_env_for_build.bat
```

**Linux/macOS:**
```bash
chmod +x prepare_env_for_build.sh
./prepare_env_for_build.sh
```

### Security Considerations

⚠️ **CRITICAL WARNINGS:**

1. **Extractable Credentials**
   - The `.env` file can be extracted from the executable using tools like 7-Zip, PyInstaller extractor, or similar
   - Anyone with access to the executable can potentially read embedded credentials
   - This is NOT secure for public distribution

2. **Risk Assessment**
   ```
   HIGH RISK:
   - Public distribution
   - Untrusted environments
   - Internet-facing deployments
   - Shared/multi-user systems
   
   MEDIUM RISK:
   - Internal corporate networks
   - Controlled access systems
   - Development environments
   
   LOW RISK:
   - Personal use only
   - Isolated test environments
   - Fully controlled infrastructure
   ```

3. **What Gets Embedded**
   - All API keys and secrets in `.env`
   - Client IDs and authentication credentials
   - Database connection strings
   - Any other sensitive configuration

### Best Practices for Embedded .env

If you must use embedded configuration:

1. **Use Service Accounts**
   - Don't embed personal credentials
   - Create dedicated service accounts with minimal permissions
   - Rotate credentials regularly

2. **Limit Scope**
   - Grant only the minimum required permissions
   - Use read-only access where possible
   - Implement IP whitelisting if available

3. **Monitor Access**
   - Log all executable usage
   - Track API usage from embedded credentials
   - Set up alerts for unusual activity

4. **Distribution Control**
   - Restrict who can access the executable
   - Use file system permissions
   - Consider encryption at rest
   - Document who has copies

---

## Option 2: External .env File (Recommended for Production)

### When to Use
- Production deployments
- Public distribution
- Untrusted environments
- When different users need different configurations
- When credentials must remain secret

### How It Works

1. Build the executable without a `.env` file present:
   ```bash
   pyinstaller getset-pox-mcp.spec
   ```

2. Distribute the executable with `.env.example`

3. Users create their own `.env` file next to the executable:
   ```bash
   # Copy example
   cp .env.example .env
   
   # Edit with their credentials
   nano .env  # or any text editor
   ```

4. The application reads `.env` from the current directory at runtime

### Advantages

✅ **Security Benefits:**
- Credentials never embedded in executable
- Each user has their own credentials
- Easier to rotate credentials (just update file)
- Credentials not exposed during distribution
- Can use different configs per environment

✅ **Flexibility:**
- Same executable for all environments
- Easy to update configuration without rebuilding
- Users can customize settings
- Simpler credential management

### Distributing External Configuration

**Package Structure:**
```
distribution/
├── getset-pox-mcp.exe
├── .env.example          # Template with placeholders
├── README.md             # Setup instructions
└── setup_instructions.txt
```

**setup_instructions.txt Example:**
```
Setup Instructions for getset-pox-mcp
======================================

1. Copy .env.example to .env:
   copy .env.example .env

2. Edit .env with your credentials:
   notepad .env

3. Required variables:
   - AUTH_CLIENT_ID: Your Azure AD Client ID
   - AUTH_CLIENT_SECRET: Your Azure AD Client Secret
   - AUTH_TENANT_ID: Your Azure AD Tenant ID

4. Run the application:
   getset-pox-mcp.exe

For help, see README.md
```

---

## Option 3: Environment Variables (Most Secure)

### When to Use
- Production systems with existing config management
- Cloud deployments (Azure, AWS, GCP)
- Container environments (Docker, Kubernetes)
- CI/CD pipelines
- Maximum security requirements

### How It Works

Set environment variables before running the executable:

**Windows:**
```cmd
set AUTH_CLIENT_ID=your-client-id
set AUTH_CLIENT_SECRET=your-secret
set AUTH_TENANT_ID=your-tenant-id
set MCP_TRANSPORT=stdio
getset-pox-mcp.exe
```

**Linux/macOS:**
```bash
export AUTH_CLIENT_ID=your-client-id
export AUTH_CLIENT_SECRET=your-secret
export AUTH_TENANT_ID=your-tenant-id
export MCP_TRANSPORT=stdio
./getset-pox-mcp
```

**Using .env with export (Linux/macOS):**
```bash
set -a
source .env
set +a
./getset-pox-mcp
```

### Advantages

✅ **Maximum Security:**
- No credentials in files
- Credentials injected at runtime only
- Can use secret management systems (Azure Key Vault, AWS Secrets Manager)
- Environment-specific configuration
- No file permission concerns

✅ **Automation Friendly:**
- Easy to integrate with orchestration tools
- Works well with containers
- Compatible with CI/CD systems
- Simple to script

---

## Configuration Priority

The application checks for configuration in this order:

1. **Environment Variables** (highest priority)
2. **Local .env file** (in executable directory)
3. **Embedded .env file** (if packaged)
4. **Default values** (lowest priority)

This allows you to override embedded settings with environment variables if needed.

---

## Migration Guide

### From Embedded to External

If you've been using embedded `.env` and want to switch:

1. **Build new executable without .env:**
   ```bash
   # Remove .env temporarily
   mv .env .env.backup
   
   # Build
   pyinstaller getset-pox-mcp.spec
   
   # Restore .env
   mv .env.backup .env
   ```

2. **Distribute with instructions:**
   - Include `.env.example`
   - Provide setup documentation
   - Notify users of the change

3. **Revoke old credentials:**
   - Rotate any credentials that were in the embedded version
   - Update documentation

### From External to Environment Variables

1. **Create environment variable script:**

   **Windows (set_env.bat):**
   ```cmd
   @echo off
   REM Load from .env file
   for /f "tokens=1,2 delims==" %%a in (.env) do (
       set %%a=%%b
   )
   ```

   **Linux/macOS (set_env.sh):**
   ```bash
   #!/bin/bash
   set -a
   source .env
   set +a
   ```

2. **Update startup procedure:**
   ```bash
   # Old way
   ./getset-pox-mcp
   
   # New way
   source set_env.sh && ./getset-pox-mcp
   ```

---

## Security Checklist

Before deploying with embedded .env:

- [ ] Assessed risk level (internal/controlled environment only?)
- [ ] Using service account with minimal permissions
- [ ] Documented who has access to executable
- [ ] Set up monitoring for credential usage
- [ ] Have credential rotation process in place
- [ ] Users understand security implications
- [ ] Alternative (external .env or env vars) considered and rejected for valid reasons

Before deploying with external .env:

- [ ] Created clear setup instructions
- [ ] Provided .env.example with placeholders
- [ ] Documented all required variables
- [ ] Set appropriate file permissions (.env should be readable only by owner)
- [ ] Users understand how to obtain credentials
- [ ] Support process for configuration issues in place

Before deploying with environment variables:

- [ ] Documented how to set env vars for your platform
- [ ] Integration with secret management system (if applicable)
- [ ] Startup scripts created and tested
- [ ] Environment variable names clearly documented
- [ ] Logging configured to not expose secrets

---

## Troubleshooting

### "Configuration not found" Error

**Symptom:** Application starts but reports missing configuration

**Solutions:**
1. Check if `.env` file exists in the same directory as executable
2. Verify environment variables are set (use `set` on Windows or `env` on Linux)
3. Check `.env` file permissions (must be readable)
4. Look for typos in variable names

### "Authentication failed" Error

**Symptom:** App starts but can't authenticate

**Solutions:**
1. Verify credentials are correct (check Azure portal)
2. Ensure no extra spaces in `.env` values
3. Check if credentials have expired
4. Verify client secret hasn't been rotated
5. Confirm tenant ID is correct

### Embedded .env Not Working

**Symptom:** Built with embedded .env but app can't find it

**Solutions:**
1. Verify `.env` existed during build (check build output)
2. Rebuild with `--clean` flag
3. Check if external `.env` is overriding (remove it for testing)
4. Run with `MCP_LOG_LEVEL=DEBUG` to see where it's looking

---

## Recommendations by Deployment Type

| Deployment | Recommended Method | Reason |
|------------|-------------------|---------|
| Development | Embedded .env | Convenience |
| Testing | External .env | Flexibility |
| Staging | Environment Variables | Matches production |
| Production | Environment Variables + Secret Manager | Maximum security |
| Demo/POC | External .env | Easy setup for users |
| Internal Tools | Embedded .env (with caution) | User convenience |
| Public Distribution | External .env only | Security requirement |
| Container | Environment Variables | Standard practice |
| Cloud VM | Environment Variables + Key Vault | Cloud-native approach |

---

## Additional Resources

- [12-Factor App Config](https://12factor.net/config)
- [OWASP Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
- [Azure Key Vault Documentation](https://docs.microsoft.com/en-us/azure/key-vault/)
- [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/)
- [PyInstaller Data Files](https://pyinstaller.org/en/stable/spec-files.html#adding-data-files)

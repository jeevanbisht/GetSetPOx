# PyInstaller Build Instructions for getset-pox-mcp

Complete cross-platform instructions for packaging the getset-pox-mcp MCP server into a standalone executable using PyInstaller.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Step 1: Install Dependencies](#step-1-install-dependencies)
3. [Step 2: Install PyInstaller](#step-2-install-pyinstaller)
4. [Step 3: Build the Executable](#step-3-build-the-executable)
5. [Step 4: Test the Executable](#step-4-test-the-executable)
6. [Step 5: Distribution](#step-5-distribution)
7. [Troubleshooting](#troubleshooting)
8. [Platform-Specific Notes](#platform-specific-notes)

---

## Prerequisites

- **Python 3.10 or higher** installed on your system
- **pip** package manager
- **Git** (optional, for cloning the repository)
- **Virtual environment** (recommended for isolation)

**Verify Python installation:**

```bash
python --version
```

or on some systems:

```bash
python3 --version
```

---

## Step 1: Install Dependencies

### 1.1 Create and Activate Virtual Environment (Recommended)

**On Windows:**

```cmd
python -m venv venv
venv\Scripts\activate
```

**On Linux/macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 1.2 Install Project Dependencies

Install all required dependencies including optional HTTP transport support:

```bash
pip install -r requirements.txt
```

Install additional dependencies for HTTP/SSE transport (if needed):

```bash
pip install starlette uvicorn sse-starlette
```

### 1.3 Verify Installation

Test that the server runs correctly before packaging:

```bash
python -m getset_pox_mcp.server
```

Press `Ctrl+C` to stop the server after verifying it starts without errors.

---

## Step 2: Install PyInstaller

### 2.1 Install PyInstaller

```bash
pip install pyinstaller
```

### 2.2 Verify PyInstaller Installation

```bash
pyinstaller --version
```

Expected output: `6.x.x` or higher

---

## Step 3: Build the Executable

### 3.1 Option A: Build with Embedded .env File (Recommended for Internal Use)

The project includes helper scripts that prepare your `.env` file and build the executable with embedded configuration:

**On Windows:**

```cmd
prepare_env_for_build.bat
```

**On Linux/macOS:**

```bash
chmod +x prepare_env_for_build.sh
./prepare_env_for_build.sh
```

**What these scripts do:**
1. Check if `.env` exists, create from `.env.example` if not
2. Offer to edit `.env` with your credentials
3. Show security warnings about embedded credentials
4. Build the executable with PyInstaller
5. Include the `.env` file inside the executable

**⚠️ SECURITY WARNING:**
- Embedded `.env` files can be extracted from the executable
- Only use this method for internal/trusted deployments
- For public distribution, use Option B below

### 3.2 Option B: Build Without Embedded .env (For Public Distribution)

If you don't want to embed credentials in the executable:

```bash
pyinstaller getset-pox-mcp.spec
```

**What this command does:**
- Analyzes `getset_pox_mcp/server.py` as the entry point
- Bundles all Python dependencies (MCP, httpx, msal, cryptography, etc.)
- Includes hidden imports for dynamic modules
- Packages everything into a single executable
- Outputs to the `dist/` directory

### 3.2 Alternative: Build Without Spec File

If you want to build manually without the spec file:

```bash
pyinstaller --onefile ^
    --name getset-pox-mcp ^
    --hidden-import=mcp ^
    --hidden-import=mcp.server ^
    --hidden-import=mcp.server.stdio ^
    --hidden-import=mcp.server.sse ^
    --hidden-import=mcp.types ^
    --hidden-import=starlette ^
    --hidden-import=uvicorn ^
    --hidden-import=msal ^
    --hidden-import=httpx ^
    --hidden-import=cryptography ^
    --hidden-import=getset_pox_mcp.services ^
    --hidden-import=getset_pox_mcp.authentication ^
    --collect-all cryptography ^
    --collect-all mcp ^
    getset_pox_mcp/server.py
```

**Note:** The spec file method is preferred as it includes all necessary hidden imports and configurations.

### 3.3 Build Progress

The build process will:
1. Analyze dependencies (~30 seconds)
2. Collect modules and binaries (~1-2 minutes)
3. Create the executable (~30 seconds)

Total time: **2-4 minutes** depending on your system.

**Expected output:**
```
Building EXE from EXE-00.toc completed successfully.
```

---

## Step 4: Test the Executable

### 4.1 Locate the Executable

The executable is located in the `dist/` directory:

**On Windows:**
```
dist\getset-pox-mcp.exe
```

**On Linux/macOS:**
```
dist/getset-pox-mcp
```

### 4.2 Test Execution

**Test 1: Basic Launch**

```bash
dist/getset-pox-mcp
```

or on Windows:

```cmd
dist\getset-pox-mcp.exe
```

**Expected behavior:**
- Server starts and listens on STDIO (default transport)
- Logs appear showing initialization
- No Python interpreter errors

Press `Ctrl+C` to stop.

**Test 2: HTTP Transport Mode**

Set environment variables and test HTTP mode:

**On Windows:**
```cmd
set MCP_TRANSPORT=http
set MCP_HTTP_PORT=8000
dist\getset-pox-mcp.exe
```

**On Linux/macOS:**
```bash
MCP_TRANSPORT=http MCP_HTTP_PORT=8000 dist/getset-pox-mcp
```

**Test 3: Test in a Clean Environment**

Move the executable to a different directory (without Python installed in the path) and run it:

```bash
mkdir test_environment
cp dist/getset-pox-mcp test_environment/
cd test_environment
./getset-pox-mcp
```

This verifies the executable is truly standalone.

### 4.3 Verify Tool Registration

If you have a client to test with, verify all tools are registered:

1. Connect to the server via MCP protocol
2. List available tools
3. Confirm all 30+ tools are present (hello_world, echo, diagnostics, etc.)

---

## Step 5: Distribution

### 5.1 Package Structure

When distributing your executable, include:

```
distribution/
├── getset-pox-mcp(.exe)     # The executable
├── .env.example              # Configuration template
├── README.md                 # Usage instructions
└── LICENSE                   # License file
```

### 5.2 Create Distribution Package

**On Windows:**

```cmd
mkdir distribution
copy dist\getset-pox-mcp.exe distribution\
copy .env.example distribution\
copy README.md distribution\
copy LICENSE distribution\
```

**On Linux/macOS:**

```bash
mkdir -p distribution
cp dist/getset-pox-mcp distribution/
cp .env.example distribution/
cp README.md distribution/
cp LICENSE distribution/
chmod +x distribution/getset-pox-mcp
```

### 5.3 Create Archive

**Windows (ZIP):**

```cmd
powershell Compress-Archive -Path distribution\* -DestinationPath getset-pox-mcp-windows.zip
```

**Linux/macOS (tar.gz):**

```bash
tar -czf getset-pox-mcp-linux.tar.gz -C distribution .
```

---

## Troubleshooting

### Issue 1: ModuleNotFoundError During Build

**Symptom:**
```
ModuleNotFoundError: No module named 'xyz'
```

**Solution:**
Add the missing module to hidden imports in the spec file:

```python
hiddenimports += ['xyz']
```

Then rebuild:

```bash
pyinstaller getset-pox-mcp.spec
```

### Issue 2: Executable Crashes on Startup

**Symptom:**
Executable starts but immediately crashes with no error message.

**Solution 1:** Build with debug mode to see detailed errors:

Edit `getset-pox-mcp.spec` and change:
```python
debug=False,
```
to:
```python
debug=True,
```

Rebuild and run to see detailed error messages.

**Solution 2:** Test with console output:

```bash
dist/getset-pox-mcp 2>&1 | tee output.log
```

### Issue 3: ImportError for cryptography or msal

**Symptom:**
```
ImportError: cannot import name '_openssl' from 'cryptography.hazmat.bindings'
```

**Solution:**
Ensure binary dependencies are collected:

```bash
pip install --upgrade cryptography
pyinstaller --clean getset-pox-mcp.spec
```

The spec file already includes `collect_all('cryptography')` which should handle this.

### Issue 4: Missing Environment Variables

**Symptom:**
Server starts but authentication fails or configuration is missing.

**Solution Options:**

**Option 1: Use Embedded .env (if built with helper script)**
If you built with `prepare_env_for_build.bat/sh`, the `.env` is already embedded. The server will automatically extract and use it from the executable's temporary directory.

**Option 2: External .env file**
Create a `.env` file next to the executable:

```bash
cd dist
cp ../.env.example .env
```

Edit `.env` with your actual credentials and configuration.

**Option 3: Environment Variables**
Set environment variables at runtime (most secure for production):

**Windows:**
```cmd
set MCP_TRANSPORT=stdio
set AUTH_CLIENT_ID=your-client-id
set AUTH_CLIENT_SECRET=your-secret
dist\getset-pox-mcp.exe
```

**Linux/macOS:**
```bash
export MCP_TRANSPORT=stdio
export AUTH_CLIENT_ID=your-client-id
export AUTH_CLIENT_SECRET=your-secret
dist/getset-pox-mcp
```

### Issue 5: Large Executable Size

**Symptom:**
Executable is larger than expected (>50MB).

**Explanation:**
This is normal for Python executables with many dependencies. The size includes:
- Python interpreter (~15MB)
- MCP framework (~5-10MB)
- Dependencies (httpx, cryptography, msal) (~20-30MB)
- Your application code (~1-5MB)

**Optimization (optional):**

1. Use UPX compression (already enabled in spec file):
```bash
# Install UPX first (https://upx.github.io/)
pyinstaller --upx-dir=/path/to/upx getset-pox-mcp.spec
```

2. Remove unnecessary dependencies before building.

### Issue 6: Antivirus False Positives

**Symptom:**
Antivirus software flags the executable as suspicious.

**Solution:**
This is common with PyInstaller executables. Options:
1. Sign the executable with a code signing certificate
2. Submit as false positive to antivirus vendors
3. Build with `--debug` flag and test again
4. Add to antivirus whitelist during development

### Issue 7: MCP Protocol Errors

**Symptom:**
```
Error: Failed to initialize MCP transport
```

**Solution:**
Ensure environment variables are set correctly:

```bash
export MCP_TRANSPORT=stdio
export MCP_LOG_LEVEL=DEBUG
dist/getset-pox-mcp
```

Check logs for specific transport initialization errors.

### Issue 8: HTTP/SSE Transport Not Working

**Symptom:**
Server crashes when using HTTP transport mode.

**Solution:**
Verify optional dependencies are installed before building:

```bash
pip install starlette uvicorn sse-starlette
pyinstaller --clean getset-pox-mcp.spec
```

---

## Platform-Specific Notes

### Windows

**Shell:** Use `cmd.exe` or PowerShell for all commands.

**Path separators:** Use backslash (`\`) in file paths.

**Executable extension:** Output will be `getset-pox-mcp.exe`.

**Antivirus:** Windows Defender may quarantine the executable initially. Add an exception if needed.

**Visual C++ Runtime:** If users report missing DLL errors, they may need to install:
- [Microsoft Visual C++ Redistributable](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist)

### Linux

**Shell:** Use bash or zsh.

**Executable permissions:** Make the file executable:
```bash
chmod +x dist/getset-pox-mcp
```

**System dependencies:** Ensure `libssl` and `libcrypto` are available:
```bash
sudo apt-get install libssl-dev  # Debian/Ubuntu
sudo yum install openssl-devel   # RHEL/CentOS
```

**GLIBC compatibility:** The executable is built against your system's GLIBC version. Users with older systems may need to rebuild.

### macOS

**Shell:** Use zsh (default on macOS 10.15+) or bash.

**Code signing:** For distribution, sign the executable:
```bash
codesign --sign "Developer ID Application: Your Name" dist/getset-pox-mcp
```

**Gatekeeper:** Users may need to allow the app in System Preferences > Security & Privacy.

**Universal binary:** To support both Intel and Apple Silicon:
```bash
# Build on each architecture separately, then combine
lipo -create -output getset-pox-mcp-universal getset-pox-mcp-x86_64 getset-pox-mcp-arm64
```

---

## Build Optimization Tips

### Reduce Build Time

1. **Use the spec file:** Much faster than command-line builds
2. **Clean builds:** Only use `--clean` when dependencies change
3. **Virtual environment:** Fewer packages = faster analysis

### Reduce Executable Size

1. **Remove unused services:** Comment out unused imports in `server.py`
2. **Use excludes:** Add packages you don't need to the `excludes` list in the spec file
3. **Strip debug symbols:** Already configured in spec file

### Improve Reliability

1. **Test on target platform:** Always test the executable on the deployment environment
2. **Include dependencies:** Bundle any external data files needed at runtime
3. **Version lock:** Use specific versions in `requirements.txt` for reproducible builds

---

## Quick Reference Commands

### Full Build Process (Summary)

```bash
# 1. Set up environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# 2. Install dependencies
pip install -r requirements.txt
pip install starlette uvicorn sse-starlette
pip install pyinstaller

# 3. Build
pyinstaller getset-pox-mcp.spec

# 4. Test
dist/getset-pox-mcp

# 5. Clean build (if needed)
pyinstaller --clean getset-pox-mcp.spec
```

---

## Additional Resources

- **PyInstaller Documentation:** https://pyinstaller.org/en/stable/
- **MCP Protocol Specification:** https://modelcontextprotocol.io/
- **Troubleshooting Guide:** https://pyinstaller.org/en/stable/when-things-go-wrong.html
- **Hook Development:** https://pyinstaller.org/en/stable/hooks.html

---

## Support

If you encounter issues not covered in this guide:

1. Check PyInstaller logs in `build/` directory
2. Run with `--debug=all` for verbose output
3. Test with Python directly before building
4. Verify all dependencies are installed
5. Check platform-specific requirements

For project-specific issues, refer to the project repository's issue tracker.

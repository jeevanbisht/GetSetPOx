# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for getset-pox-mcp MCP server.

This spec file configures PyInstaller to create a standalone executable
that bundles all dependencies including the MCP framework, authentication
modules, and service implementations.
"""

import os
import sys
from PyInstaller.utils.hooks import collect_all, collect_submodules

# Get the base directory
block_cipher = None
base_dir = os.path.abspath(SPECPATH)

# Collect all submodules for packages that use dynamic imports
hiddenimports = []

# MCP framework hidden imports
hiddenimports += collect_submodules('mcp')
hiddenimports += collect_submodules('mcp.server')
hiddenimports += collect_submodules('mcp.server.stdio')
hiddenimports += collect_submodules('mcp.server.sse')
hiddenimports += collect_submodules('mcp.types')

# HTTP/SSE transport dependencies (optional but included)
hiddenimports += collect_submodules('starlette')
hiddenimports += collect_submodules('uvicorn')
hiddenimports += collect_submodules('sse_starlette')

# Authentication and networking
hiddenimports += collect_submodules('msal')
hiddenimports += collect_submodules('httpx')
hiddenimports += collect_submodules('cryptography')

# Standard library modules that may be missed
hiddenimports += [
    'asyncio',
    'json',
    'typing',
    'logging',
    'logging.handlers',
    'os',
    'sys',
    'pathlib',
    'dotenv',
]

# Application-specific hidden imports
hiddenimports += [
    'getset_pox_mcp',
    'getset_pox_mcp.server',
    'getset_pox_mcp.config',
    'getset_pox_mcp.logging_config',
    'getset_pox_mcp.services',
    'getset_pox_mcp.authentication',
    'getset_pox_mcp.authentication.auth_provider',
    'getset_pox_mcp.authentication.middleware',
    'getset_pox_mcp.authentication.token_manager',
    'getset_pox_mcp.transport',
]

# Collect all service modules
service_modules = [
    'getset_pox_mcp.services.Test',
    'getset_pox_mcp.services.diagnostics',
    'getset_pox_mcp.services.eid',
    'getset_pox_mcp.services.iga',
    'getset_pox_mcp.services.internetAccess',
    'getset_pox_mcp.services.intune',
    'getset_pox_mcp.services.poc',
]

for module in service_modules:
    hiddenimports += collect_submodules(module)

# Collect data files (configuration examples, etc.)
datas = []

# Include .env.example files for reference
env_files = [
    ('.env.example', '.'),
    ('getset_pox_mcp/authentication/.env.auth.example', 'getset_pox_mcp/authentication/'),
]

for src, dst in env_files:
    if os.path.exists(os.path.join(base_dir, src)):
        datas.append((src, dst))

# Include actual .env file if it exists (for production builds)
if os.path.exists(os.path.join(base_dir, '.env')):
    datas.append(('.env', '.'))
    print("INFO: Including .env file in the executable")
else:
    print("WARNING: .env file not found - executable will use .env.example as reference")

# Include documentation files
doc_files = [
    'README.md',
    'LICENSE',
    'docs/authentication.md',
]

for doc in doc_files:
    if os.path.exists(os.path.join(base_dir, doc)):
        datas.append((doc, 'docs' if doc.startswith('docs/') else '.'))

# Collect binary dependencies for cryptography and other native extensions
binaries = []
tmp_ret = collect_all('cryptography')
datas += tmp_ret[0]
binaries += tmp_ret[1]
hiddenimports += tmp_ret[2]

# Analysis step - analyze the main script
a = Analysis(
    ['getset_pox_mcp/server.py'],
    pathex=[base_dir],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'PIL',
        'tkinter',
        'PyQt5',
        'PySide2',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# PYZ step - create the archive
pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)

# EXE step - create the executable
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='getset-pox-mcp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)

#!/bin/bash
# Prepare .env file for building standalone executable
# This script copies .env.example to .env if .env doesn't exist

set -e

echo "============================================"
echo "Preparing .env file for PyInstaller build"
echo "============================================"
echo

if [ -f .env ]; then
    echo "[INFO] .env file already exists"
    echo "[INFO] Current .env will be included in the executable"
    echo
    read -p "Do you want to review/edit .env before building? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        ${EDITOR:-nano} .env
    fi
else
    echo "[WARNING] .env file not found"
    echo "[INFO] Creating .env from .env.example..."
    cp .env.example .env
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to create .env file"
        exit 1
    fi
    echo "[SUCCESS] .env file created"
    echo
    echo "[IMPORTANT] Please edit .env with your actual credentials before building!"
    echo
    read -p "Do you want to edit .env now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        ${EDITOR:-nano} .env
    fi
fi

echo
echo "============================================"
echo "Build Options"
echo "============================================"
echo
echo "The .env file will be embedded in the executable."
echo
echo "SECURITY WARNING:"
echo "- The .env file will contain sensitive credentials"
echo "- Anyone with access to the executable can extract it"
echo "- Only use this for trusted/internal deployments"
echo
echo "For production/public distribution:"
echo "1. Do NOT include sensitive credentials in .env"
echo "2. Use environment variables at runtime instead"
echo "3. Or distribute .env separately (not embedded)"
echo
read -p "Continue with building the executable? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo
    echo "[INFO] Build cancelled"
    exit 0
fi

echo
echo "[INFO] Starting PyInstaller build..."
echo "[INFO] This will take 2-4 minutes..."
echo

pyinstaller getset-pox-mcp.spec

if [ $? -ne 0 ]; then
    echo
    echo "[ERROR] Build failed! Check the output above for errors."
    exit 1
fi

echo
echo "============================================"
echo "Build Complete!"
echo "============================================"
echo
echo "Executable location: dist/getset-pox-mcp"
echo "Size: ~24 MB"
echo
echo "The executable includes:"
echo "- All Python dependencies"
echo "- .env configuration file (embedded)"
echo "- .env.example (for reference)"
echo
echo "To test the executable:"
echo "  cd dist"
echo "  ./getset-pox-mcp"
echo
echo "Don't forget to make it executable:"
echo "  chmod +x dist/getset-pox-mcp"
echo

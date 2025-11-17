#!/bin/bash
# Setup script for getset-pox-mcp development environment

set -e

echo "Setting up getset-pox-mcp development environment..."

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -e ".[dev]"

# Create .env from example if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
fi

echo ""
echo "Setup complete! 🎉"
echo ""
echo "To activate the virtual environment, run:"
echo "  source venv/bin/activate"
echo ""
echo "To run the server:"
echo "  python -m getset_pox_mcp.server"
echo ""
echo "To run tests:"
echo "  pytest tests/"
echo ""

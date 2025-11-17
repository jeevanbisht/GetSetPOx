@echo off
REM Setup script for getset-pox-mcp development environment (Windows)

echo Setting up getset-pox-mcp development environment...

REM Check Python version
python --version

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo Installing dependencies...
pip install -e .[dev]

REM Create .env from example if it doesn't exist
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
)

echo.
echo Setup complete! 🎉
echo.
echo To activate the virtual environment, run:
echo   venv\Scripts\activate.bat
echo.
echo To run the server:
echo   python -m getset_pox_mcp.server
echo.
echo To run tests:
echo   pytest tests/
echo.

pause

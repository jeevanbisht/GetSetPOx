@echo off
REM Prepare .env file for building standalone executable
REM This script copies .env.example to .env if .env doesn't exist

echo ============================================
echo Preparing .env file for PyInstaller build
echo ============================================
echo.

if exist .env (
    echo [INFO] .env file already exists
    echo [INFO] Current .env will be included in the executable
    echo.
    choice /C YN /M "Do you want to review/edit .env before building"
    if errorlevel 2 goto :skip_edit
    if errorlevel 1 goto :edit_env
) else (
    echo [WARNING] .env file not found
    echo [INFO] Creating .env from .env.example...
    copy .env.example .env
    if errorlevel 1 (
        echo [ERROR] Failed to create .env file
        pause
        exit /b 1
    )
    echo [SUCCESS] .env file created
    echo.
    echo [IMPORTANT] Please edit .env with your actual credentials before building!
    echo.
    choice /C YN /M "Do you want to edit .env now"
    if errorlevel 2 goto :skip_edit
    if errorlevel 1 goto :edit_env
)

:edit_env
echo [INFO] Opening .env in notepad...
notepad .env
goto :continue

:skip_edit
echo [INFO] Skipping .env edit
goto :continue

:continue
echo.
echo ============================================
echo Build Options
echo ============================================
echo.
echo The .env file will be embedded in the executable.
echo.
echo SECURITY WARNING:
echo - The .env file will contain sensitive credentials
echo - Anyone with access to the executable can extract it
echo - Only use this for trusted/internal deployments
echo.
echo For production/public distribution:
echo 1. Do NOT include sensitive credentials in .env
echo 2. Use environment variables at runtime instead
echo 3. Or distribute .env separately (not embedded)
echo.
choice /C YN /M "Continue with building the executable"
if errorlevel 2 goto :cancel
if errorlevel 1 goto :build

:build
echo.
echo [INFO] Starting PyInstaller build...
echo [INFO] This will take 2-4 minutes...
echo.
pyinstaller getset-pox-mcp.spec
if errorlevel 1 (
    echo.
    echo [ERROR] Build failed! Check the output above for errors.
    pause
    exit /b 1
)
echo.
echo ============================================
echo Build Complete!
echo ============================================
echo.
echo Executable location: dist\getset-pox-mcp.exe
echo Size: ~24 MB
echo.
echo The executable includes:
echo - All Python dependencies
echo - .env configuration file (embedded)
echo - .env.example (for reference)
echo.
echo To test the executable:
echo   cd dist
echo   getset-pox-mcp.exe
echo.
pause
exit /b 0

:cancel
echo.
echo [INFO] Build cancelled
pause
exit /b 0

@echo off
echo ========================================
echo Starting NeuroLens Server
echo ========================================
echo.

cd /d "%~dp0"

echo Checking Python...
python --version
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python from python.org
    pause
    exit
)

echo.
echo Starting Flask server...
echo.

python test_server.py

if errorlevel 1 (
    echo.
    echo ========================================
    echo ERROR: Server failed to start!
    echo ========================================
    echo.
    echo Try these solutions:
    echo 1. Install dependencies: pip install flask numpy librosa torch
    echo 2. Check if port 5000 is in use
    echo 3. Read TROUBLESHOOTING.md
    echo.
)

pause

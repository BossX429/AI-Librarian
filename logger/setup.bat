@echo off
REM Claude Desktop Logger Setup Script
REM ==================================

echo.
echo ============================================================
echo Claude Desktop Conversation Logger - Setup
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

echo [1/3] Python detected successfully
echo.

REM Install required packages
echo [2/3] Installing required Python packages...
echo.
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Failed to install packages
    pause
    exit /b 1
)

echo.
echo [3/3] Setup complete!
echo.
echo ============================================================
echo Ready to capture conversations!
echo ============================================================
echo.
echo To start the logger, run:
echo     python claude_desktop_logger.py
echo.
echo Or use the start_logger.bat script
echo.
pause

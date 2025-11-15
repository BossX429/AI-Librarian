@echo off
REM Run the Claude Desktop Curator
REM Processes raw logs from Logger into structured database

echo.
echo ======================================
echo   Claude Desktop Curator
echo ======================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

REM Run the curator
echo Processing conversation logs...
echo.
python claude_curator.py

echo.
echo ======================================
echo   Processing Complete!
echo ======================================
echo.
echo You can now:
echo   - Search: python claude_curator.py search "your query"
echo   - Export: python claude_curator.py export session_id
echo.
pause

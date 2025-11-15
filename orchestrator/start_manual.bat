@echo off
REM Manually start Autonomous AI Librarian (with visible console for monitoring)
REM Use this if you want to see what's happening

echo.
echo ================================================
echo   AI LIBRARIAN - Manual Start
echo ================================================
echo.
echo Starting in manual mode (console visible)...
echo Press Ctrl+C to stop
echo.

python "%~dp0autonomous_librarian.py"

pause

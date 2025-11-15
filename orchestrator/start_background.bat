@echo off
REM Start Autonomous AI Librarian in background (hidden window)
REM This script starts the orchestrator silently without showing a console window

REM Use pythonw.exe instead of python.exe to run without console
start "" /MIN pythonw "%~dp0autonomous_librarian.py"

REM Script exits immediately - orchestrator runs in background
exit

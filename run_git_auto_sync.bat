@echo off
REM Git Auto-Sync for AI-Librarian
REM Runs silently in background

cd /d "%~dp0"
pythonw git_auto_sync.py > git_auto_sync.log 2>&1

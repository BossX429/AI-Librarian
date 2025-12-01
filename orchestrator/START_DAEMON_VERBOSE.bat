@echo off
echo Starting AI Librarian Daemon...
cd /d "%~dp0"
python autonomous_librarian.py
pause

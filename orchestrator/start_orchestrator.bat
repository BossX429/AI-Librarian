@echo off
REM Start Orchestrator in background
cd /d "C:\repos\AI-Librarian\orchestrator"
start "" /MIN "C:\Program Files\Python312\pythonw.exe" "autonomous_librarian.py"
exit

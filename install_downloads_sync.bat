@echo off
schtasks /Create /TN "DownloadsKnowledgeBaseSync" /TR "python C:\repos\AI-Librarian\downloads_kb_sync.py" /SC MINUTE /MO 5 /F
echo Auto-sync installed! Runs every 5 minutes.
pause

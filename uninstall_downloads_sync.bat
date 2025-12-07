@echo off
schtasks /Delete /TN "DownloadsKnowledgeBaseSync" /F
echo Auto-sync uninstalled.
pause

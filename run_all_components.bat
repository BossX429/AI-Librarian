@echo off
REM Shell Integration: Streamlined execution for AI-Librarian components

REM Logger Component
start "Logger" cmd /k "python logger\claude_ui_scraper.py"

REM Compressor Component
start "Compressor" cmd /k "python compressor\delta_compressor.py compress"

REM Curator Component
start "Curator" cmd /k "python curator\claude_curator.py"

REM Query Tools Component
start "Query Tools" cmd /k "python query_tools\librarian_query.py"

REM Instructions
@echo Components launched in separate terminals. Press any key to exit...
pause

@echo off
REM AI Librarian - Complete Workflow (HYDRA PARALLEL EDITION)
REM 1. Compresses raw logs using 20-core parallel processing (90% reduction!)
REM 2. Processes into searchable database
REM 3. Shows statistics

echo.
echo ============================================
echo   AI LIBRARIAN - HYDRA PARALLEL WORKFLOW
echo ============================================
echo.

REM Step 1: PARALLEL compress raw logs with Hydra
echo [1/2] Compressing raw logs (PARALLEL - 20 CORES)...
echo.
cd /d "%~dp0compressor"
python hydra_compress.py compress
if errorlevel 1 (
    echo ERROR: Compression failed!
    pause
    exit /b 1
)

echo.
echo ============================================
echo.

REM Step 2: Process compressed logs with Curator
echo [2/2] Processing into database...
echo.
cd /d "%~dp0curator"

REM Point Curator to compressed files
python claude_curator.py
if errorlevel 1 (
    echo ERROR: Curator processing failed!
    pause
    exit /b 1
)

echo.
echo ============================================
echo   WORKFLOW COMPLETE!
echo ============================================
echo.
echo Your conversations are now:
echo   - Compressed (90%% smaller via PARALLEL processing)
echo   - Organized in database
echo   - Searchable and exportable
echo.
echo Try: python curator\claude_curator.py search "your query"
echo.
pause

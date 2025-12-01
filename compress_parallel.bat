@echo off
REM Quick Hydra Parallel Compression - 20-core power
REM Compresses all uncompressed logs in parallel

echo.
echo ============================================
echo   HYDRA PARALLEL COMPRESSION
echo ============================================
echo   Using all 20 cores simultaneously
echo ============================================
echo.

cd /d "%~dp0compressor"
python hydra_compress.py compress

echo.
echo Compression complete!
echo.
pause

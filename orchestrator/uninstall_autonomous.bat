@echo off




REM Uninstall Autonomous AI Librarian Auto-Start









echo.




echo ================================================




echo   AI LIBRARIAN - Uninstall Auto-Start




echo ================================================




echo.









REM Check for admin privileges




net session >nul 2>&1




if %errorLevel% NEQ 0 (




    echo ERROR: This script requires Administrator privileges!




    echo Right-click and select "Run as Administrator"




    echo.




    pause




    exit /b 1




)









echo [1/3] Stopping AI Librarian...




echo.




call "%~dp0stop_autonomous.bat"









echo.




echo [2/3] Removing scheduled task...




echo.









schtasks /Delete /TN "AI_Librarian_Autonomous" /F >nul 2>&1









if %errorLevel% EQU 0 (




    echo  Scheduled task removed




) else (




    echo   No scheduled task found (already removed?)




)









echo.




echo [3/3] Removing from Startup folder...




echo.









set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"




set "SHORTCUT_PATH=%STARTUP_FOLDER%\AI_Librarian_Autonomous.bat"









if exist "%SHORTCUT_PATH%" (




    del "%SHORTCUT_PATH%" >nul 2>&1




    echo  Removed from Startup folder




) else (




    echo   Not found in Startup folder (already removed?)




)









echo.




echo ================================================




echo   UNINSTALL COMPLETE!




echo ================================================




echo.




echo  AI Librarian auto-start disabled




echo  All background processes stopped




echo.




echo Note: Your captured data is still safe:




echo   - Database: curator\processed\conversations.db




echo   - Compressed logs: compressor\compressed\




echo.




echo To re-enable: Run "install_autonomous.bat"




echo.




pause





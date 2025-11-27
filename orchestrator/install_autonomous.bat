@echo off




REM Install Autonomous AI Librarian for Auto-Start




REM This creates a Windows Task Scheduler task to start on boot









echo.




echo ================================================




echo   AI LIBRARIAN - Auto-Start Installation




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









echo [1/3] Creating startup task...




echo.









REM Get the full path to the background start script




set "SCRIPT_PATH=%~dp0start_background.bat"









REM Create Windows Task Scheduler task




schtasks /Create /TN "AI_Librarian_Autonomous" /TR "\"%SCRIPT_PATH%\"" /SC ONLOGON /RL HIGHEST /F









if %errorLevel% NEQ 0 (




    echo ERROR: Failed to create scheduled task!




    pause




    exit /b 1




)









echo  Startup task created successfully!




echo.









REM Optionally, also add to Startup folder for immediate visibility




echo [2/3] Adding to Startup folder...




echo.









set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"




set "SHORTCUT_PATH=%STARTUP_FOLDER%\AI_Librarian_Autonomous.bat"









REM Create a copy of the start script in Startup folder




copy "%SCRIPT_PATH%" "%SHORTCUT_PATH%" >nul 2>&1









if exist "%SHORTCUT_PATH%" (




    echo  Added to Startup folder!




) else (




    echo   Could not add to Startup folder (non-critical)




)









echo.




echo [3/3] Starting AI Librarian now...




echo.









REM Start it immediately




call "%SCRIPT_PATH%"









REM Wait a moment for it to start




timeout /t 3 /nobreak >nul









echo.




echo ================================================




echo   INSTALLATION COMPLETE!




echo ================================================




echo.




echo  AI Librarian is now running in background




echo  Will auto-start on every Windows login




echo  Runs 24/7 autonomously




echo.




echo The AI Librarian will now:




echo   • Capture all Claude conversations




echo   • Compress logs every 5 minutes




echo   • Update database automatically




echo   • Run silently in background




echo.




echo Log file: %~dp0orchestrator.log




echo.




echo To stop: Run "stop_autonomous.bat"




echo To uninstall: Run "uninstall_autonomous.bat"




echo.




pause





@echo off




REM Stop Autonomous AI Librarian









echo.




echo ================================================




echo   Stopping AI Librarian




echo ================================================




echo.









REM Kill any running pythonw processes running autonomous_librarian.py




for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq pythonw.exe" /FO LIST ^| find "PID:"') do (




    wmic process where "ProcessId=%%a" get CommandLine | find "autonomous_librarian" >nul




    if not errorlevel 1 (




        echo Stopping process %%a...




        taskkill /PID %%a /F >nul 2>&1




    )




)









REM Also kill any claude_desktop_logger processes




for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq python.exe" /FO LIST ^| find "PID:"') do (




    wmic process where "ProcessId=%%a" get CommandLine | find "claude_desktop_logger" >nul




    if not errorlevel 1 (




        echo Stopping logger %%a...




        taskkill /PID %%a /F >nul 2>&1




    )




)









echo.




echo  AI Librarian stopped




echo.




pause





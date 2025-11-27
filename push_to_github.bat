@echo off




REM Quick GitHub Setup Script




REM Run this after creating your GitHub repository









echo.




echo ============================================




echo   AI Librarian - GitHub Setup




echo ============================================




echo.









REM Check if git is installed




git --version >nul 2>&1




if errorlevel 1 (




    echo ERROR: Git is not installed!




    echo.




    echo Please install Git from: https://git-scm.com/




    echo After installing, restart this script.




    echo.




    pause




    exit /b 1




)









echo [1/5] Git is installed 




echo.









REM Prompt for GitHub username




set /p GITHUB_USER="Enter your GitHub username: "









if "%GITHUB_USER%"=="" (




    echo ERROR: Username cannot be empty!




    pause




    exit /b 1




)









echo.




echo [2/5] GitHub username: %GITHUB_USER% 




echo.




echo IMPORTANT: Before continuing, make sure you:




echo   1. Created a repository on GitHub named: AI-Librarian




echo   2. Did NOT initialize it with README




echo.




set /p CONTINUE="Ready to continue? (y/n): "









if /i not "%CONTINUE%"=="y" (




    echo.




    echo Cancelled. Create your GitHub repo first, then run this again.




    pause




    exit /b 0




)









echo.




echo [3/5] Initializing git repository...




git init




git add .




git commit -m "Initial commit: AI Librarian v1.0 - Autonomous conversation capture system"









echo.




echo [4/5] Connecting to GitHub...




git remote add origin https://github.com/%GITHUB_USER%/AI-Librarian.git




git branch -M main









echo.




echo [5/5] Pushing to GitHub...




git push -u origin main









if errorlevel 1 (




    echo.




    echo ============================================




    echo   PUSH FAILED!




    echo ============================================




    echo.




    echo Common fixes:




    echo   1. Make sure you created the repo on GitHub




    echo   2. Check your internet connection




    echo   3. Verify your GitHub credentials




    echo.




    echo Manual push:




    echo   git push -u origin main




    echo.




    pause




    exit /b 1




)









echo.




echo ============================================




echo   SUCCESS! 




echo ============================================




echo.




echo Your AI Librarian is now on GitHub!




echo.




echo Repository URL:




echo   https://github.com/%GITHUB_USER%/AI-Librarian




echo.




echo Next steps:




echo   1. Visit your repo and star it 




echo   2. Add topics: claude, ai, automation, python




echo   3. Share with others who use Claude Desktop




echo.




echo Future updates:




echo   git add .




echo   git commit -m "Your change description"




echo   git push




echo.




pause





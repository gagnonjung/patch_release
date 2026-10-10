@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if not errorlevel 1 (
    py -3 "%~dp0tools\site_publisher.py"
    goto done
)
where python >nul 2>nul
if not errorlevel 1 (
    python "%~dp0tools\site_publisher.py"
    goto done
)
echo [ERROR] Python 3 is required to start the site publisher.
echo Install Python 3 for Windows, then run this file again.
pause
exit /b 1
:done
if errorlevel 1 (
    echo.
    echo [ERROR] Site publisher ended with an error.
    pause
)

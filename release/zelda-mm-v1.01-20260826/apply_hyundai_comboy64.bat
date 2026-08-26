@echo off
setlocal
cd /d "%~dp0"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0apply_patch.ps1" -Variant HyundaiComboy64 %*
set "RC=%ERRORLEVEL%"
echo.
if not "%RC%"=="0" (echo Patch process finished with errors. Exit code: %RC%) else (echo Patch process completed successfully.)
echo.
if /I "%ZELDA_PATCH_NO_PAUSE%"=="1" exit /b %RC%
pause
exit /b %RC%

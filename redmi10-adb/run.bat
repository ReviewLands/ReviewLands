@echo off
setlocal
cd /d "%~dp0"

where adb >nul 2>&1
if errorlevel 1 (
  echo adb not found. Install Android platform-tools and add adb to PATH.
  echo https://developer.android.com/tools/releases/platform-tools
  pause
  exit /b 1
)

where py >nul 2>&1
if not errorlevel 1 (
  py -3 redmi10.py %*
  goto :eof
)
where python >nul 2>&1
if not errorlevel 1 (
  python redmi10.py %*
  goto :eof
)
where python3 >nul 2>&1
if not errorlevel 1 (
  python3 redmi10.py %*
  goto :eof
)

echo Python 3 is required. Install it from https://www.python.org/downloads/
echo Then run:  py -3 redmi10.py
pause
exit /b 1

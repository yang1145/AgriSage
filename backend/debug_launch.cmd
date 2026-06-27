@echo off
echo ============================================
echo   AgriSage Debug Launcher
echo ============================================
echo.
echo Working directory: %CD%
echo.

REM Check if files are blocked by Windows (downloaded from another PC)
echo Checking for Windows file blocking...
powershell -Command "Get-ChildItem '%~dp0' -File | Where-Object { $_.Name -match '\.(exe|dll|pyd|cmd)$' } | ForEach-Object { $stream = Get-Item $_.FullName -Stream Zone.Identifier -ErrorAction SilentlyContinue; if ($stream) { Write-Host '  BLOCKED: ' $_.Name } }" 2>nul
echo.

REM Unblock all files if blocked
echo Unblocking files...
powershell -Command "Get-ChildItem '%~dp0' -Recurse -File | Unblock-File -ErrorAction SilentlyContinue" 2>nul
echo Done.
echo.

REM List critical files (PyInstaller structure: exe + _internal/)
echo Checking critical files:
if exist "%~dp0AgriSage.exe" (echo   [OK] AgriSage.exe) else (echo   [MISSING] AgriSage.exe)
if exist "%~dp0_internal" (echo   [OK] _internal/) else (echo   [MISSING] _internal/)
if exist "%~dp0_internal\MSVCP140.dll" (echo   [OK] _internal\MSVCP140.dll) else (echo   [MISSING] _internal\MSVCP140.dll)
if exist "%~dp0_internal\python313.dll" (echo   [OK] _internal\python313.dll) else (echo   [MISSING] _internal\python313.dll)
if exist "%~dp0_internal\frontend\dist\index.html" (echo   [OK] _internal\frontend\dist\index.html) else (echo   [MISSING] _internal\frontend\dist\index.html)
echo.

REM Disable advanced CPU instructions to avoid illegal instruction crashes
set OPENBLAS_CORETYPE=CORE2

REM Run the exe and capture exit code
echo Starting AgriSage.exe ...
echo.
start /wait "" "%~dp0AgriSage.exe"
echo.
echo Exit code: %ERRORLEVEL%
echo.
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] AgriSage.exe exited with error code %ERRORLEVEL%
    echo.
    echo Common exit codes:
    echo   0xC0000135 = DLL not found
    echo   0xC000007B = 32/64-bit mismatch
    echo   0xC0000005 = Access violation
    echo   0xC000001D = Illegal instruction (CPU too old)
    echo   0xE06D7363 = C++ exception
    echo   1          = Python unhandled exception
)
echo.
if exist "%~dp0agrisage_crash.log" (
    echo --- agrisage_crash.log ---
    type "%~dp0agrisage_crash.log"
    echo.
) else (
    echo [INFO] No agrisage_crash.log found - Python did not start at all
    echo.
)
pause

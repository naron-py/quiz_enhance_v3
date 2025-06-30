@echo off
:: Check for administrator privileges
NET SESSION >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    :: Not running as administrator, elevate the script
    echo Requesting administrator privileges...
    PowerShell -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
    exit /b
)

:: If we get here, we're running with admin rights
echo Starting HPMA Quiz Assistant with administrator privileges...
echo.

:: Set the current directory to where the batch file is located
cd /d "%~dp0"
echo Working directory: %CD%

:: Make sure Python is in the path
where python >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python not found in PATH. Please check your Python installation.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)


:: Start the terminal app with full path using Windows Terminal
start wt.exe cmd /k "cd /d "%~dp0" && python "%~dp0terminal_app.py""

echo.
echo HPMA Quiz Assistant started successfully!
echo F2 - Capture and process quiz
echo F3 - Clear overlay
echo.
echo Press any key to exit this window...
pause > nul 
@echo off
setlocal
chcp 65001 >nul
title USAS Workspace Launcher

:: Define ANSI Escape Codes for True Terminal Colors (Windows 10+)
set "ESC="
set "CYAN=%ESC%[96m"
set "GREEN=%ESC%[92m"
set "YELLOW=%ESC%[93m"
set "RED=%ESC%[91m"
set "MAGENTA=%ESC%[95m"
set "RESET=%ESC%[0m"

cls
echo.
echo %MAGENTA%=======================================================%RESET%
echo %MAGENTA%              USAS Workspace Launcher%RESET%
echo %MAGENTA%=======================================================%RESET%
echo.

:: 1. Connect to WiFi
echo %CYAN%[*]%RESET% Connecting to WiFi network 'WIFI@USAS'...
netsh wlan connect name="WIFI@USAS" >nul 2>&1
if %errorlevel% equ 0 (
    echo %GREEN%[OK]%RESET% Connection request was sent successfully.
) else (
    echo %YELLOW%[!]%RESET% Could not force connection. May already be connected or not in range.
)
:: Wait briefly for connection to establish before launching captive portal
timeout /t 3 /nobreak >nul

:: 2. Python Environment Setup
echo.
echo %CYAN%[*]%RESET% Setting up Python Environment...
if not exist "venv\" (
    echo %GREEN%[+]%RESET% Creating virtual environment for the first time...
    python -m venv venv
)

:: 3. Activate venv and run script
echo %CYAN%[*]%RESET% Activating environment...
call venv\Scripts\activate.bat

echo %CYAN%[*]%RESET% Verifying dependencies...
pip install -r requirements.txt -q --no-warn-script-location
if %errorlevel% neq 0 (
    echo %YELLOW%[!]%RESET% Normal install failed ^(possible SSL error^). Trying trusted-host fallback...
    pip install -r requirements.txt -q --no-warn-script-location --trusted-host pypi.org --trusted-host files.pythonhosted.org
)

echo.
echo %MAGENTA%-------------------------------------------------------%RESET%
echo %MAGENTA%[*]%RESET% Launching Browser Automation...
echo %MAGENTA%-------------------------------------------------------%RESET%
python usas_auth_controller.py

echo.
echo %MAGENTA%-------------------------------------------------------%RESET%
echo %MAGENTA%[*]%RESET% Opening USAS OneDrive Folder...
explorer "C:\Users\RADZ\OneDrive - Universiti Sultan Azlan Shah (1)"

echo.
echo %GREEN%=======================================================%RESET%
echo %GREEN%              Batch Execution Complete!%RESET%
echo %GREEN%=======================================================%RESET%
:: Pause to let user see output if something broke, otherwise they can close it.
echo %YELLOW%Press any key to close%RESET%
pause >nul
exit

@echo off
:: Force PowerShell to allow this script just for this run
powershell -Command "Set-ExecutionPolicy Bypass -Scope Process -Force"

:: Move to script directory
cd /d %~dp0

:: Activate venv
call renenv\Scripts\activate

:: Start AI
python assistant.py

:: Keep window open
pause

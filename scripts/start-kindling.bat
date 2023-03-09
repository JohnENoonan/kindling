@echo off
@setlocal
@setlocal enableextensions
@cd /d "%~dp0"

taskkill /f /im explorer.exe /fi "memusage gt 2"
echo %cd%

cd ../applications/backend
echo %cd%
CALL startServer.bat

echo Wait 20 seconds for backend to start
timeout 20

cd  ../watchdog
echo %cd%
START startupTouch.vbs
START startupAudio.vbs

@echo off
@setlocal
@setlocal enableextensions
@cd /d "%~dp0"

rem taskkill /f /im explorer.exe /fi "memusage gt 2"

cd ../../watchdog
npm run launch:touch
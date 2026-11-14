@echo off
title Webdesign Attila - Mainframe 2.0
cd /d "%~dp0"
where python >nul 2>nul
if %errorlevel%==0 (
  python start_mainframe.py %*
) else (
  py start_mainframe.py %*
)
if errorlevel 1 pause

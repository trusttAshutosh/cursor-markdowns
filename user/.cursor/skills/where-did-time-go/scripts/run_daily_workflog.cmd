@echo off
REM Daily where-did-time-go local runner (Task Scheduler target).
setlocal
set PYTHON=C:\Python314\python.exe
set SCRIPT=%USERPROFILE%\.cursor\skills\where-did-time-go\scripts\generate_daily_workflog.py
"%PYTHON%" "%SCRIPT%" %*
set EXITCODE=%ERRORLEVEL%
exit /b %EXITCODE%

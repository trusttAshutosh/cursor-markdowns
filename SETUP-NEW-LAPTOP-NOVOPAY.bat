@echo off
setlocal EnableExtensions
title SETUP NEW LAPTOP - Novopay + Cursor AI
cd /d "%~dp0"

echo.
echo ============================================================
echo  SETUP-NEW-LAPTOP-NOVOPAY
echo  1^) Clone all Novopay repos into %%USERPROFILE%%\Desktop\novopay
echo  2^) Restore Cursor / AI config from this cursor-markdowns folder
echo ============================================================
echo.
echo This folder should be:  Desktop\cursor-markdowns
echo Current folder:         %CD%
echo.

where git >nul 2>&1
if errorlevel 1 (
  echo ERROR: git is not on PATH. Install Git for Windows, then re-run.
  goto :end
)

where python >nul 2>&1
if errorlevel 1 (
  echo ERROR: python is not on PATH. Install Python 3, then re-run.
  goto :end
)

if not exist "%~dp0novopay\AGENTS.md" (
  echo ERROR: novopay\AGENTS.md missing.
  echo Clone this repo first:
  echo   git clone https://github.com/trusttAshutosh/cursor-markdowns.git %%USERPROFILE%%\Desktop\cursor-markdowns
  echo Then double-click this bat again.
  goto :end
)

if not exist "%~dp0scripts\setup_new_laptop.py" (
  echo ERROR: scripts\setup_new_laptop.py missing from this repo.
  goto :end
)

if not exist "%~dp0novopay-repos.tsv" (
  echo ERROR: novopay-repos.tsv missing from this repo.
  goto :end
)

echo Prerequisites OK. Starting setup...
echo.
python "%~dp0scripts\setup_new_laptop.py" --backup-root "%~dp0."
set "EC=%ERRORLEVEL%"
echo.
if not "%EC%"=="0" (
  echo Setup finished with errors ^(exit %EC%^). Check clone failures above.
) else (
  echo Setup finished successfully.
)

:end
echo.
pause
endlocal

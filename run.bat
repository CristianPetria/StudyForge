@echo off
REM StudyForge Startup Script for Windows

echo.
echo ==========================================
echo StudyForge - AI Study Guide Generator
echo ==========================================
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if requirements are installed
pip show flask > nul 2>&1
if errorlevel 1 (
    echo Installing requirements...
    pip install -r requirements.txt
)

REM Check if .env file exists
if not exist ".env" (
    echo.
    echo WARNING: .env file not found!
    echo Copy .env.example to .env and configure your settings.
    echo.
)

echo.
echo Starting StudyForge API...
python main.py

pause

@echo off
echo === VC Research Engine Setup ===
echo This script will install dependencies and set up the project.

REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: Python is required but not installed.
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    if %ERRORLEVEL% NEQ 0 (
        echo Error: Failed to create virtual environment.
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate
if %ERRORLEVEL% NEQ 0 (
    echo Error: Failed to activate virtual environment.
    exit /b 1
)

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo Error: Failed to install dependencies.
    exit /b 1
)

REM Install Playwright browsers
echo Installing Playwright browsers...
playwright install chromium
if %ERRORLEVEL% NEQ 0 (
    echo Error: Failed to install Playwright browsers.
    exit /b 1
)

REM Check if .env file exists
if not exist .env (
    echo Creating .env file...
    (
        echo # API Keys
        echo OPENAI_API_KEY=your_openai_api_key_here
        echo SERPER_API_KEY=your_serper_api_key_here
    ) > .env
    echo Please update the .env file with your API keys.
) else (
    echo .env file already exists.
)

echo.
echo === Setup Complete ===
echo To run the API server:
echo 1. Activate the virtual environment: venv\Scripts\activate
echo 2. Start the server: uvicorn main:app --reload
echo 3. Access the API at: http://localhost:8000
echo.
echo Don't forget to update your API keys in the .env file!

pause

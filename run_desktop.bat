@echo off
REM Jarvis AI Desktop Application - Quick Start Script for Windows
REM This script sets up and runs the Jarvis AI desktop voice assistant

setlocal enabledelayedexpansion

echo.
echo ========================================
echo   Jarvis AI Desktop Voice Assistant
echo   Quick Start for Windows
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

REM Display Python version
echo [OK] Python is installed:
python --version
echo.

REM Check if requirements are installed
echo [INFO] Checking dependencies...
python -m pip show vosk >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Dependencies not installed
    echo [INFO] Installing dependencies from requirements.txt...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
    echo [OK] Dependencies installed successfully
) else (
    echo [OK] Dependencies are already installed
)
echo.

REM Check if Vosk model exists
echo [INFO] Checking Vosk speech model...
if exist "jarvis_desktop\models\vosk-model-en-us-0.42-gigaspeech" (
    echo [OK] Vosk model found
) else (
    echo [WARNING] Vosk model not found!
    echo.
    echo To download the Vosk model:
    echo 1. Visit: https://alphacephei.com/vosk/models
    echo 2. Download: "vosk-model-en-us-0.42-gigaspeech.zip"
    echo 3. Extract the ZIP file
    echo 4. Move the folder to: jarvis_desktop\models\
    echo.
    echo The structure should be:
    echo   jarvis_desktop\
    echo   └── models\
    echo       └── vosk-model-en-us-0.42-gigaspeech\
    echo.
    set /p continue="Do you have the Vosk model downloaded? (y/n): "
    if /i not "!continue!"=="y" (
        echo [INFO] Please download the Vosk model and try again
        pause
        exit /b 1
    )
)
echo.

REM Check if .env file exists
echo [INFO] Checking configuration...
if exist ".env" (
    echo [OK] .env file found
) else (
    echo [WARNING] .env file not found
    echo [INFO] Creating .env from .env.example...
    copy .env.example .env
    echo [OK] .env file created from template
    echo.
    echo [IMPORTANT] Edit the .env file to:
    echo   - Add your Gemini API key (optional but recommended)
    echo   - Configure other settings as needed
    echo.
    echo .env file location: %cd%\.env
    pause
)
echo.

REM Check for microphone
echo [INFO] Checking audio devices...
python -c "import pyaudio; p = pyaudio.PyAudio(); print(f'[OK] {p.get_device_count()} audio devices found'); p.terminate()" 2>nul
if errorlevel 1 (
    echo [WARNING] Could not verify audio devices
    echo Please ensure your microphone is connected
)
echo.

REM Final setup confirmation
echo.
echo ========================================
echo   Ready to start Jarvis AI Desktop!
echo ========================================
echo.
echo Starting Jarvis AI...
echo Press Ctrl+C to stop the application
echo.
echo [INSTRUCTIONS]
echo 1. When you see "Listening for wake word..." the app is ready
echo 2. Say "Jarvis" to activate the assistant
echo 3. After activation, speak your command clearly
echo 4. Wait for Jarvis to respond
echo.
echo [EXAMPLE COMMANDS]
echo - "Jarvis, open Chrome"
echo - "Jarvis, search Python tutorials"
echo - "Jarvis, what's the weather?"
echo - "Jarvis, tell me a joke"
echo - "Jarvis, shutdown the computer"
echo.
pause
echo.

REM Start the application
:run_app
echo [INFO] Starting Jarvis AI Desktop Application...
python -m jarvis_desktop.main

REM Check for errors
if errorlevel 1 (
    echo.
    echo [ERROR] Application exited with error
    echo For troubleshooting, see: DESKTOP_SETUP_GUIDE.md
    echo.
    set /p retry="Retry? (y/n): "
    if /i "!retry!"=="y" goto run_app
)

echo.
echo [INFO] Jarvis AI Desktop has stopped
echo.

endlocal

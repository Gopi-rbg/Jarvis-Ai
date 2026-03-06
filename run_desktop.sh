#!/bin/bash

# Jarvis AI Desktop Application - Quick Start Script for macOS & Linux
# This script sets up and runs the Jarvis AI desktop voice assistant

echo ""
echo "========================================"
echo "  Jarvis AI Desktop Voice Assistant"
echo "  Quick Start for macOS & Linux"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "[ERROR] Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8+ from https://www.python.org/"
    exit 1
fi

# Display Python version
echo "[OK] Python is installed:"
python3 --version
echo ""

# Check if requirements are installed
echo "[INFO] Checking dependencies..."
if ! python3 -m pip show vosk &> /dev/null
then
    echo "[WARNING] Dependencies not installed"
    echo "[INFO] Installing dependencies from requirements.txt..."
    python3 -m pip install -r requirements.txt
    if [ $? -ne 0 ]
    then
        echo "[ERROR] Failed to install dependencies"
        exit 1
    fi
    echo "[OK] Dependencies installed successfully"
else
    echo "[OK] Dependencies are already installed"
fi
echo ""

# Check if Vosk model exists
echo "[INFO] Checking Vosk speech model..."
if [ -d "jarvis_desktop/models/vosk-model-en-us-0.42-gigaspeech" ]
then
    echo "[OK] Vosk model found"
else
    echo "[WARNING] Vosk model not found!"
    echo ""
    echo "To download the Vosk model:"
    echo "1. Visit: https://alphacephei.com/vosk/models"
    echo "2. Download: 'vosk-model-en-us-0.42-gigaspeech.zip'"
    echo "3. Extract the ZIP file"
    echo "4. Move the folder to: jarvis_desktop/models/"
    echo ""
    echo "The structure should be:"
    echo "  jarvis_desktop/"
    echo "  └── models/"
    echo "      └── vosk-model-en-us-0.42-gigaspeech/"
    echo ""
    read -p "Do you have the Vosk model downloaded? (y/n): " continue
    if [ "$continue" != "y" ] && [ "$continue" != "Y" ]
    then
        echo "[INFO] Please download the Vosk model and try again"
        exit 1
    fi
fi
echo ""

# Check if .env file exists
echo "[INFO] Checking configuration..."
if [ -f ".env" ]
then
    echo "[OK] .env file found"
else
    echo "[WARNING] .env file not found"
    echo "[INFO] Creating .env from .env.example..."
    cp .env.example .env
    echo "[OK] .env file created from template"
    echo ""
    echo "[IMPORTANT] Edit the .env file to:"
    echo "  - Add your Gemini API key (optional but recommended)"
    echo "  - Configure other settings as needed"
    echo ""
    echo ".env file location: $(pwd)/.env"
    read -p "Press Enter to continue..."
fi
echo ""

# Check for microphone
echo "[INFO] Checking audio devices..."
python3 -c "import pyaudio; p = pyaudio.PyAudio(); print(f'[OK] {p.get_device_count()} audio devices found'); p.terminate()" 2>/dev/null
if [ $? -ne 0 ]
then
    echo "[WARNING] Could not verify audio devices"
    echo "Please ensure your microphone is connected"
fi
echo ""

# Final setup confirmation
echo ""
echo "========================================"
echo "  Ready to start Jarvis AI Desktop!"
echo "========================================"
echo ""
echo "Starting Jarvis AI..."
echo "Press Ctrl+C to stop the application"
echo ""
echo "[INSTRUCTIONS]"
echo "1. When you see 'Listening for wake word...' the app is ready"
echo "2. Say 'Jarvis' to activate the assistant"
echo "3. After activation, speak your command clearly"
echo "4. Wait for Jarvis to respond"
echo ""
echo "[EXAMPLE COMMANDS]"
echo "- 'Jarvis, open Chrome'"
echo "- 'Jarvis, search Python tutorials'"
echo "- 'Jarvis, what's the weather?'"
echo "- 'Jarvis, tell me a joke'"
echo "- 'Jarvis, shutdown the computer'"
echo ""
read -p "Press Enter to start..."
echo ""

# Start the application
run_app() {
    echo "[INFO] Starting Jarvis AI Desktop Application..."
    python3 -m jarvis_desktop.main
}

# Run the app and handle errors
run_app
exit_code=$?

if [ $exit_code -ne 0 ]
then
    echo ""
    echo "[ERROR] Application exited with error (code: $exit_code)"
    echo "For troubleshooting, see: DESKTOP_SETUP_GUIDE.md"
    echo ""
    read -p "Retry? (y/n): " retry
    if [ "$retry" == "y" ] || [ "$retry" == "Y" ]
    then
        run_app
    fi
fi

echo ""
echo "[INFO] Jarvis AI Desktop has stopped"
echo ""

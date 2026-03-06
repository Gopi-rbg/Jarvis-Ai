# Jarvis AI - Getting Started Guide

Complete guide to install, configure, and run Jarvis AI Voice Assistant (Desktop & Web versions)

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Running the Application](#running-the-application)
5. [First Run Experience](#first-run-experience)
6. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum Requirements
- **OS**: Windows 10, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: 3.8 or higher
- **RAM**: 2GB minimum (4GB+ recommended)
- **Storage**: 2GB free space (for Vosk models)
- **Microphone**: Built-in or USB microphone
- **Speakers/Headphones**: For voice output
- **Internet**: Required for:
  - First-time setup and dependency installation
  - Gemini API (for AI responses)
  - Django web dashboard access

### Recommended Specifications
- **Python**: 3.10+
- **RAM**: 4GB+
- **Storage**: SSD with 2GB+ free space
- **Microphone**: Quality USB microphone (e.g., Blue Yeti, Audio-Technica)
- **Internet**: Broadband (10+ Mbps)

---

## Installation

### Step 1: Install Python

**Windows:**
1. Download Python 3.10+ from https://www.python.org/downloads/
2. Run the installer
3. **IMPORTANT**: Check "Add Python to PATH"
4. Click "Install Now"

**macOS:**
```bash
# Using Homebrew (if installed)
brew install python3

# Or download from https://www.python.org/downloads/
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3.10 python3-pip

# Fedora
sudo dnf install python3.10 python3-pip

# Arch
sudo pacman -S python
```

### Step 2: Clone/Download Project

```bash
# Option A: Using Git (if installed)
git clone https://github.com/Gopi-rbg/Jarvis-Ai.git
cd Jarvis-Ai

# Option B: Download ZIP from GitHub
# 1. Go to https://github.com/Gopi-rbg/Jarvis-Ai
# 2. Click "Code" → "Download ZIP"
# 3. Extract the ZIP file
# 4. Open terminal in the extracted folder
```

### Step 3: Install Python Dependencies

**Windows:**
```bash
# Using quick-start script (easiest)
run_desktop.bat

# Or manually
pip install -r requirements.txt
```

**macOS/Linux:**
```bash
# Using quick-start script (easiest)
bash run_desktop.sh

# Or manually
pip3 install -r requirements.txt
```

### Step 4: Install Platform-Specific Audio Libraries

**Windows:**
```bash
pip install pipwin
pipwin install pyaudio
```

**macOS:**
```bash
brew install portaudio
pip3 install pyaudio
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install portaudio19-dev libssl-dev
pip3 install pyaudio
```

### Step 5: Download Vosk Speech Model

Vosk is required for offline speech recognition. The model is NOT included in the repository.

**Method 1: Automatic Download (via run_desktop.bat/run_desktop.sh)**
- The quick-start script will prompt you to download if missing

**Method 2: Manual Download**
1. Visit: https://alphacephei.com/vosk/models
2. Download: **"vosk-model-en-us-0.42-gigaspeech.zip"** (~1.4GB)
3. Extract the ZIP file
4. Move the extracted folder to:
   ```
   projectsust/jarvis_desktop/models/vosk-model-en-us-0.42-gigaspeech/
   ```

**Verify Installation:**
```bash
# Windows
if exist "jarvis_desktop\models\vosk-model-en-us-0.42-gigaspeech" (echo Model found) else (echo Model NOT found)

# macOS/Linux
ls -la jarvis_desktop/models/vosk-model-en-us-0.42-gigaspeech
```

---

## Configuration

### 1. Create .env File

**Copy template to actual .env:**
```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

### 2. Get Gemini API Key (Optional but Recommended)

For AI-powered responses:

1. **Create Google Cloud Account**
   - Visit: https://console.cloud.google.com/
   - Sign in with Google account (create if needed)

2. **Create New Project**
   - Click "Select a Project"
   - Click "NEW PROJECT"
   - Name it "Jarvis AI" (or any name)
   - Click "CREATE"

3. **Enable Generative AI API**
   - Go to "APIs & Services" → "Library"
   - Search for "Generative Language API"
   - Click on the result
   - Click "ENABLE"

4. **Create API Key**
   - Go to "Credentials" (left sidebar)
   - Click "Create Credentials" → "API Key"
   - Copy the generated key

5. **Add to .env**
   - Open `.env` file in a text editor
   - Find the line: `GEMINI_API_KEY=your_actual_api_key_here`
   - Replace with your API key: `GEMINI_API_KEY=AIzaSyD...`
   - Save the file

### 3. Configure Other Settings (Optional)

Edit `.env` to customize:

```env
# Voice settings
TTS_VOICE_TYPE=female        # 'female' or 'male'
TTS_RATE=1.0                # 0.5 (slow) to 2.0 (fast)
TTS_VOLUME=0.9              # 0.0 to 1.0

# Recognition settings
SPEECH_TIMEOUT=10           # Seconds to listen
SPEECH_CONFIDENCE=0.5       # 0.0 to 1.0

# Django web app
DJANGO_API_URL=http://localhost:8000/api
SYNC_WITH_DJANGO=True
```

---

## Running the Application

### Quick Start (Recommended)

**Windows:**
```bash
run_desktop.bat
```

**macOS/Linux:**
```bash
bash run_desktop.sh
```

### Manual Start

**Windows:**
```bash
python -m jarvis_desktop.main
```

**macOS/Linux:**
```bash
python3 -m jarvis_desktop.main
```

### Web Dashboard (Optional)

In a **separate terminal**:

```bash
# Navigate to project directory
cd projectsust

# Start Django server
python manage.py runserver

# Access dashboard at: http://localhost:8000
```

---

## First Run Experience

### What to Expect

1. **Startup Messages**
   ```
   [INFO] Initializing Jarvis AI...
   [OK] All modules loaded successfully
   [INFO] Listening for wake word...
   ```

2. **Wake Word Detection** (listening for "Jarvis")
   - App is continuously listening for the word "Jarvis"
   - Microphone LED may indicate listening state
   - No CPU spike yet (background listening mode)

3. **Say the Wake Word**
   - Speak clearly: **"Jarvis"**
   - Wait for confirmation
   - You should hear a beep or voice confirmation

4. **Speak Your Command** (within 10 seconds)
   - Example: **"Open Chrome"**
   - Speak clearly and loudly
   - Wait for Jarvis to respond

5. **Get Response**
   - Desktop action: App opens or executes command
   - AI Query: Jarvis responds with voice
   - Hear the response through speakers

6. **Repeat**
   - Go back to step 2 to issue another command
   - Or press Ctrl+C to quit

### Example First Commands

Try these simple commands to start:
```
"Jarvis, Hello"              → AI responds with greeting
"Jarvis, what's the time"    → Current time
"Jarvis, tell me a joke"     → Tells a joke
"Jarvis, open Chrome"        → Opens Chrome browser
"Jarvis, search Python"      → Searches "Python" on Google
```

### Troubleshooting First Run

**Issue**: No response to "Jarvis"
- Check microphone volume
- Reduce background noise
- Speak louder/clearer
- Verify microphone works in system settings

**Issue**: App opens but closes immediately
- Check error in terminal
- See [Troubleshooting](#troubleshooting) section
- Verify Vosk model is downloaded

**Issue**: Commands not working
- Ensure you said "Jarvis" first
- Check internet connection (for Gemini API)
- Verify .env file has correct API key

---

## Troubleshooting

### Installation Issues

**Problem**: "Python not found" or "python: command not found"
```
Solution:
1. Verify Python is installed: python --version
2. Add Python to PATH:
   - Windows: Reinstall Python, check "Add to PATH"
   - macOS/Linux: pip3 instead of pip
```

**Problem**: "No module named 'vosk'" or other missing modules
```
Solution:
1. Reinstall requirements:
   pip install -r requirements.txt
   
2. Verify pip is working:
   pip --version
   
3. Try installing individually:
   pip install vosk pyaudio pyttsx3 google-generativeai
```

**Problem**: PyAudio installation fails
```
Solution:

Windows:
  pip install pipwin
  pipwin install pyaudio

macOS:
  brew install portaudio
  pip install pyaudio

Linux:
  sudo apt-get install portaudio19-dev
  pip install pyaudio
```

### Vosk Model Issues

**Problem**: "No module named Vosk" or "Model not found"
```
Solution:
1. Verify Vosk is installed:
   pip install vosk
   
2. Verify model path is correct:
   - Windows: jarvis_desktop\models\vosk-model-en-us-0.42-gigaspeech\
   - macOS/Linux: jarvis_desktop/models/vosk-model-en-us-0.42-gigaspeech/
   
3. Check model is extracted (not a ZIP file):
   ls jarvis_desktop/models/vosk-model-en-us-0.42-gigaspeech/
   # Should show: am, conf, graph, ivector, etc.
```

**Problem**: "Model loading failed" or "Vosk initialization error"
```
Solution:
1. Redownload model from https://alphacephei.com/vosk/models
2. Verify model folder structure
3. Ensure model is extracted, not compressed
4. Check disk space (model is ~1.4GB)
```

### Microphone Issues

**Problem**: "Microphone not detected" or "Audio device error"
```
Solution:
1. Check physical connection (USB or built-in)
2. Test microphone in OS settings:
   - Windows: Settings → Sound → Microphone
   - macOS: System Preferences → Sound → Input
   - Linux: pavucontrol or alsamixer
3. Restart application
4. Restart computer if still not working
```

**Problem**: "Microphone captured but no speech recognized"
```
Solution:
1. Increase microphone volume (system level)
2. Test microphone with OS recording app
3. Reduce background noise (close fans, music, etc.)
4. Speak louder and more clearly
5. Position microphone closer to mouth
6. Check microphone sensitivity settings
```

### Gemini API Issues

**Problem**: "Invalid API key" or "Authentication failed"
```
Solution:
1. Verify API key in .env file:
   cat .env | grep GEMINI_API_KEY
   
2. Check key format:
   GEMINI_API_KEY=AIzaSyD... (starts with AIzaSy)
   
3. Verify API is enabled:
   - Go to Google Cloud Console
   - Check Generative Language API is "ENABLED"
   
4. Check API quota:
   - Google Cloud Console → Quotas & System Limits
   - Ensure you haven't exceeded free tier limits
```

**Problem**: API key not set or "Unable to use SimpleBrain as AI fallback"
```
Solution:
1. Verify .env file exists in project root
2. Without API key, app uses basic SimpleBrain (limited)
3. To get API key:
   - Go to https://console.cloud.google.com/
   - Follow Configuration section above
```

### Speech Recognition Issues

**Problem**: "Speech recognition timeout" or "Could not understand audio"
```
Solution:
1. Increase SPEECH_TIMEOUT in .env:
   SPEECH_TIMEOUT=15  # Instead of 10
   
2. Reduce background noise
3. Speak louder and more clearly
4. Ensure microphone is on
5. Move closer to microphone
```

**Problem**: Recognition works offline but fails with internet
```
Solution:
1. Check internet connection
2. Verify firewall allows Python access
3. Check if Google Speech API quota exceeded
4. Try offline mode only (Vosk)
```

### Performance Issues

**Problem**: High CPU usage or slow response
```
Solution:
1. Close unnecessary applications
2. Disable real-time antivirus scanning
3. Verify SSD has at least 1GB free
4. Use faster computer if possible
5. Check running processes (Task Manager/Activity Monitor)
```

**Problem**: Commands execute slowly or with delay
```
Solution:
1. Move closer to WiFi router (if using online APIs)
2. Check internet speed (speed.com)
3. Reduce background downloads
4. Disable VPN (if using one)
5. Restart router/internet connection
```

### Command Issues

**Problem**: Application launch fails or doesn't work
```
Solution:
1. Verify application is installed on system
2. Check command spelling in jar commands.py
3. Try shortcuts:
   Instead of: "Jarvis, open Microsoft Word"
   Try: "Jarvis, open Word"
```

**Problem**: Website opening fails
```
Solution:
1. Verify browser is installed
2. Check internet connection
3. Ensure URL is formatted correctly
4. Try explicit URL:
   Instead of: "Jarvis, open YouTube"
   Try: "Jarvis, open youtube.com"
```

### General Issues

**Problem**: Application crashes or hangs
```
Solution:
1. Check terminal for error messages
2. Note the error and check README_DESKTOP.md
3. Try starting again: python -m jarvis_desktop.main
4. If persistent, reinstall: pip install -r requirements.txt --force-reinstall
```

**Problem**: Can't find or modify .env file
```
Solution:
Windows:
  - Open File Explorer
  - Check "View" → "Show hidden files"
  - .env should be in project root
  
macOS/Linux:
  - Use terminal: cat .env
  - Or editor: nano .env or vim .env
```

---

## Next Steps

After successful installation and first run:

1. **Explore Commands**
   - Try different app launches
   - Test web searches
   - Ask AI questions
   - Use system commands

2. **Customize Voice and Settings**
   - Edit .env for voice preferences
   - Add custom applications to commands.py
   - Configure command history location

3. **Web Dashboard Integration**
   - Run Django server
   - View command history
   - Monitor Jarvis activity
   - Sync desktop and web commands

4. **Advanced Configuration**
   - Add custom speech recognition models
   - Implement custom commands
   - Integrate with other services
   - See DEVELOPER_GUIDE.md for details

5. **Get Support**
   - Check TROUBLESHOOTING.md for common issues
   - See README_DESKTOP.md for feature details
   - Review DEVELOPER_GUIDE.md for code changes
   - Check GitHub Issues for known problems

---

## Quick Reference Commands

After startup, try these voice commands:

```
General:
  "Jarvis, hello"              → Greeting
  "Jarvis, how are you"        → Status check
  "Jarvis, what can you do"    → Capabilities list

Applications:
  "Jarvis, open Chrome"        → Open Chrome
  "Jarvis, open VS Code"       → Open editor
  "Jarvis, open Spotify"       → Open music player

Web:
  "Jarvis, search Python"      → Google search
  "Jarvis, YouTube Python"     → YouTube search
  "Jarvis, open Google"        → Open website

System:
  "Jarvis, shutdown"           → Shutdown (60s warning)
  "Jarvis, restart"            → Restart computer

Information:
  "Jarvis, what time is it"    → Current time
  "Jarvis, tell me a joke"     → Joke
  "Jarvis, weather"            → Weather info
  "Jarvis, help"               → Help info
```

---

## Keyboard Shortcuts

```
Ctrl+C       → Stop Jarvis AI application
Ctrl+Z       → Pause (then type 'fg' to resume)
```

---

## File Structure

```
Jarvis-Ai/
├── projectsust/              # Django project root
│   ├── manage.py             # Django management
│   ├── requirements.txt       # Python dependencies
│   ├── .env.example           # Configuration template
│   ├── run_desktop.bat        # Windows launcher
│   ├── run_desktop.sh         # Mac/Linux launcher
│   ├── README.md              # Web app documentation
│   ├── README_DESKTOP.md      # Desktop app documentation
│   ├── DESKTOP_SETUP_GUIDE.md # Detailed setup instructions
│   ├── GETTING_STARTED.md     # This file
│   ├── jarvis_desktop/        # Desktop application
│   │   ├── main.py            # Main application loop
│   │   ├── wake_word.py       # Wake word detection
│   │   ├── speech_to_text.py  # Speech recognition
│   │   ├── text_to_speech.py  # Voice synthesis
│   │   ├── gemini_brain.py    # AI engine
│   │   ├── commands.py        # PC automation
│   │   ├── __init__.py        # Package init
│   │   └── models/            # Vosk models (download separately)
│   ├── core/                  # Django app (web API)
│   ├── appsust/               # Django app
│   ├── templates/             # HTML templates
│   └── static/                # CSS, JS, images
└── .git/                      # Git repository
```

---

## Support & Resources

- **Documentation**: See README_DESKTOP.md and DESKTOP_SETUP_GUIDE.md
- **Vosk Models**: https://alphacephei.com/vosk/models
- **Gemini API**: https://ai.google.dev/
- **Django Docs**: https://docs.djangoproject.com/
- **GitHub**: https://github.com/Gopi-rbg/Jarvis-Ai
- **Issues**: https://github.com/Gopi-rbg/Jarvis-Ai/issues

---

## Need Help?

1. Check TROUBLESHOOTING.md for common issues
2. Review error messages in terminal output
3. Check GitHub Issues for similar problems
4. Verify all installation steps completed
5. Ensure microphone is working
6. Check internet connection for online features

---

**Last Updated**: 2024 | **Status**: Production Ready | **Python**: 3.8+ | **License**: MIT

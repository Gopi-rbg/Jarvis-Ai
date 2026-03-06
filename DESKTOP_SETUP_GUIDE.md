# Jarvis AI Desktop Application - Setup Guide

This guide provides step-by-step instructions for setting up and running the standalone Jarvis AI desktop voice assistant.

## Prerequisites

- **Python 3.8+** (3.10+ recommended)
- **pip** (Python package manager)
- **microphone** connected to your computer
- **speakers** or headphones for voice output
- **Windows/Mac/Linux** operating system

## Installation Steps

### 1. Install Python Dependencies

Navigate to the project directory and install required packages:

```bash
pip install -r requirements.txt
```

### 2. Download Vosk Speech Recognition Model

The desktop app uses **Vosk** for offline speech recognition. You must download the speech model manually:

**Step 1: Download the Model**
- Visit: https://alphacephei.com/vosk/models
- Download **English (US)** model: `vosk-model-en-us-0.42-gigaspeech.zip`

**Step 2: Extract the Model**
- Extract the downloaded ZIP file
- Navigate into the extracted folder and copy the folder inside

**Step 3: Place in Correct Location**
```
projectsust/
├── jarvis_desktop/
│   ├── models/
│   │   └── vosk-model-en-us-0.42-gigaspeech/  ← Extract here
│   ├── main.py
│   ├── wake_word.py
│   └── ...
```

### 3. Configure Google Gemini API (Optional but Recommended)

For AI-powered responses, set up the Gemini API:

**Step 1: Create Google Cloud Account**
- Visit: https://console.cloud.google.com/
- Create a new project

**Step 2: Enable Generative AI API**
- Go to APIs & Services → Library
- Search for "Generative Language API"
- Click Enable

**Step 3: Create API Key**
- Go to Credentials → Create Credentials → API Key
- Copy your API key

**Step 4: Create .env File**
Create a `.env` file in the project root:

```bash
# projectsust/.env
GEMINI_API_KEY=your_api_key_here
```

**Replace `your_api_key_here`** with your actual API key from Step 3.

**Important**: Never commit `.env` to version control (it's in `.gitignore`)

### 4. Platform-Specific Setup

#### Windows

```bash
# Install PyAudio dependencies
pip install pipwin
pipwin install pyaudio

# Run the desktop app
python -m jarvis_desktop.main
```

#### macOS

```bash
# Install PyAudio dependencies
brew install portaudio
pip install pyaudio

# Run the desktop app
python3 -m jarvis_desktop.main
```

#### Linux

```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install portaudio19-dev
sudo apt-get install libssl-dev

# Install Python dependencies
pip install pyaudio

# Run the desktop app
python3 -m jarvis_desktop.main
```

## Running the Application

### Basic Usage

```bash
# From project root directory
python -m jarvis_desktop.main
```

Once running:
1. **Wake Word Detection**: Say "Jarvis" to activate the assistant
2. **Command Input**: After activation, speak your command loudly and clearly
3. **Response**: Jarvis will process your command and respond

### Exit Application

Press `Ctrl+C` in the terminal to safely shutdown

## Supported Commands

### Application Control
- "Jarvis, open Chrome"
- "Jarvis, open VS Code"
- "Jarvis, open Spotify"
- "Jarvis, open Discord"
- "Jarvis, open Calculator"

### Web Control
- "Jarvis, open Google"
- "Jarvis, open YouTube"
- "Jarvis, search Python tutorials"
- "Jarvis, YouTube Python"

### System Control
- "Jarvis, shutdown the computer"
- "Jarvis, restart the computer"

### AI Queries
- "Jarvis, what's the weather?"
- "Jarvis, tell me a joke"
- "Jarvis, how do I learn Python?"
- "Jarvis, what time is it?"

## Troubleshooting

### Issue: "No module named 'pyaudio'"

**Solution:**
```bash
# Windows
pip install pipwin
pipwin install pyaudio

# macOS
brew install portaudio
pip install pyaudio

# Linux
sudo apt-get install portaudio19-dev
pip install pyaudio
```

### Issue: "ModuleNotFoundError: No module named 'vosk'"

**Solution:**
```bash
pip install vosk
# Ensure Vosk model is downloaded in jarvis_desktop/models/
```

### Issue: "Microphone not detected"

**Solutions:**
1. Check microphone connection
2. Verify microphone is working in system settings
3. Test microphone with Windows Recording or Mac Audio MIDI Setup
4. Restart the application

### Issue: "Gemini API Key Error"

**Solutions:**
1. Verify `.env` file exists in project root
2. Check API key is correct: `GEMINI_API_KEY=xxxxx`
3. Ensure Generative Language API is enabled in Google Cloud Console
4. Without API key, SimpleBrain fallback will be used (limited responses)

### Issue: "Speech Recognition Not Working"

**Solutions:**
1. Try online mode (requires internet): SpeechRecognition library will fall back to Google Cloud
2. Adjust microphone input level in system settings
3. Speak clearly into microphone
4. Reduce background noise
5. Check microphone permissions in system settings

### Issue: "Vosk Model Not Found"

**Solution:**
Ensure the model path is correct:
```
jarvis_desktop/models/vosk-model-en-us-0.42-gigaspeech/
                       ↑ This exact folder structure
```

Check by running:
```bash
python -c "import os; print(os.path.exists('jarvis_desktop/models/vosk-model-en-us-0.42-gigaspeech'))"
```

## Environment Variables

Optional environment variables in `.env`:

```env
# Gemini API Configuration
GEMINI_API_KEY=your_api_key_here

# Optional: Logging Configuration
DEBUG=True
LOG_LEVEL=INFO
```

## File Structure

```
projectsust/
├── jarvis_desktop/
│   ├── __init__.py              # Package initialization
│   ├── main.py                  # Main application loop
│   ├── wake_word.py             # Wake word detection (Vosk)
│   ├── speech_to_text.py        # Speech recognition (offline/online)
│   ├── text_to_speech.py        # Speech synthesis (pyttsx3)
│   ├── gemini_brain.py          # AI response generation (Gemini API)
│   ├── commands.py              # System commands & automation
│   └── models/                  # Vosk models (download separately)
│       └── vosk-model-en-us-0.42-gigaspeech/
├── manage.py
├── requirements.txt
├── .env                         # Create this file with API key
└── ...other Django files...
```

## Performance Tips

1. **Reduce Background Noise**: Ensure quiet environment for better speech recognition
2. **Speak Clearly**: Enunciate commands clearly for better recognition accuracy
3. **Use Offline Mode**: Vosk-based recognition works offline without internet
4. **Monitor CPU**: The app runs continuously; monitor system resources
5. **Command History**: Commands are saved to `command_history.json`

## Advanced Configuration

### Changing Voice in Text-to-Speech

Edit `jarvis_desktop/text_to_speech.py`:
```python
def __init__(self):
    # Available voices: 'male', 'female', or set voice index
    super().__init__(voice_type='female')  # or 'male'
```

### Adjusting Speech Recognition Timeout

Edit `jarvis_desktop/wake_word.py`:
```python
# Change timeout (in seconds)
user_input = self.get_speech_input(timeout=10)  # Default is 10
```

### Using Different Vosk Language Models

Visit https://alphacephei.com/vosk/models and download alternative language models, then update the model path.

## Syncing with Web Dashboard

To log desktop commands to the Django web app:

1. Ensure Django server is running: `python manage.py runserver`
2. Desktop app automatically sends commands to Django API
3. View command history at: `http://localhost:8000/api/commands/`
4. Monitor all conversations in web dashboard

## Next Steps

1. **Customize Commands**: Edit `jarvis_desktop/commands.py` to add custom applications
2. **Extend AI Brain**: Add custom Q&A to `SimpleBrain` in `gemini_brain.py`
3. **Integrate Automations**: Use `pyautogui` in `commands.py` for screen automation
4. **Deploy Desktop App**: Create standalone executable using PyInstaller

## Support & Documentation

- **Web Dashboard**: http://localhost:8000 (after running `manage.py runserver`)
- **Vosk Models**: https://alphacephei.com/vosk/models
- **Gemini API Docs**: https://ai.google.dev/docs
- **GitHub Repository**: https://github.com/Gopi-rbg/Jarvis-Ai

## License

MIT License - See LICENSE file for details

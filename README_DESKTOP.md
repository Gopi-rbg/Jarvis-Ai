# Jarvis AI - Desktop Voice Assistant

> 🎙️ A production-grade voice assistant for desktop with offline capabilities, background listening, and Gemini AI integration.

## Features

### Core Capabilities
- **🎙️ Continuous Background Listening** - Always-on wake word detection using offline Vosk
- **🔊 Offline Speech Recognition** - Understand commands without internet using Vosk engine
- **💬 Intelligent Responses** - Powered by Google Gemini API with SimpleBrain fallback
- **🗣️ Offline Text-to-Speech** - Natural voice responses using pyttsx3
- **⚙️ PC Control & Automation** - Open apps, search web, control system (15+ commands)
- **📊 Command Logging** - Track all interactions with timestamp and responses
- **🖥️ Cross-Platform** - Windows, macOS, and Linux support
- **🔌 Web Integration** - Sync desktop commands with Django web dashboard

### Supported Actions

**Application Control**
- Open Chrome, Firefox, VS Code, Spotify, Discord, Telegram
- Launch Blender, Gimp, OBS Studio, VLC, Calculator
- Control any installed application

**Web Control**
- Search Google for any query
- Open YouTube and search videos
- Browse any website by URL

**System Control**
- Shutdown or restart computer
- Execute shell commands
- Control basic system operations

**AI Queries**
- Ask questions and get intelligent answers
- Tell jokes, give weather info
- Provide learning resources
- Answer general knowledge questions

## Quick Start

### 1. Prerequisites
- Python 3.8+ (3.10+ recommended)
- Microphone and speakers
- 500MB disk space for Vosk model

### 2. Installation

```bash
# Clone repository
git clone https://github.com/Gopi-rbg/Jarvis-Ai.git
cd Jarvis-Ai

# Install dependencies
pip install -r requirements.txt

# Download Vosk model (see DESKTOP_SETUP_GUIDE.md for details)
# Extract to: projectsust/jarvis_desktop/models/vosk-model-en-us-0.42-gigaspeech/
```

### 3. Configure
Create `.env` file in project root:
```env
GEMINI_API_KEY=your_api_key_from_google_cloud
```

### 4. Run
```bash
python -m jarvis_desktop.main
```

**Usage:**
1. Say "Jarvis" to activate
2. Speak your command
3. Get instant response

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                  Jarvis AI Desktop App              │
└─────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────┐
│            Audio Input (Microphone)                 │
└─────────────────────────────────────────────────────┘
        ↓
┌──────────────────────┬──────────────────────────────┐
│  Wake Word           │                              │
│  Detection (Vosk)    │  Listen for "Jarvis"        │
└──────────────────────┴──────────────────────────────┘
        ↓
┌──────────────────────┬──────────────────────────────┐
│  Speech-to-Text      │  Vosk (offline)             │
│                      │  + Google Cloud (fallback)  │
└──────────────────────┴──────────────────────────────┘
        ↓
┌──────────────────────┬──────────────────────────────┐
│  Command Parser      │  Analyze user input         │
│                      │  (app, web, system, AI)     │
└──────────────────────┴──────────────────────────────┘
        ↓
┌──────────────────────┬──────────────────────────────┐
│  Command Router      │  Route to handler           │
└──────────────────────┴──────────────────────────────┘
        ↓ ↓ ↓ ↓
    ┌───┴─┴─┼─────────────────────────────────────┐
    ↓       ↓       ↓                             ↓
┌──────┐ ┌──────┐ ┌──────┐                  ┌─────────┐
│Open  │ │Search│ │Control system│         │Ask AI  │
│Apps  │ │Web   │ │Shutdown     │         │(Gemini)│
└──────┘ └──────┘ └──────┘                  └─────────┘
    ↓       ↓       ↓                             ↓
    └───┬─┬─┼────────────┬──────────────────────┘
        ↓ ↓ ↓
┌──────────────────────┬──────────────────────────────┐
│  Response Generator  │  Prepare text response      │
└──────────────────────┴──────────────────────────────┘
        ↓
┌──────────────────────┬──────────────────────────────┐
│  Text-to-Speech      │  pyttsx3 (offline)         │
│                      │  Natural voice synthesis    │
└──────────────────────┴──────────────────────────────┘
        ↓
┌──────────────────────┬──────────────────────────────┐
│  Audio Output        │  Speaker/Headphones        │
│  (Speakers)          │                            │
└──────────────────────┴──────────────────────────────┘
```

## Module Overview

### `wake_word.py` - Wake Word Detection
Detects "Jarvis" keyword using offline Vosk speech recognition.

**Key Features:**
- Offline operation (no internet required)
- Continuous listening loop
- Low false-positive detection
- Automatic microphone stream management

**Usage:**
```python
from jarvis_desktop import WakeWordDetector

detector = WakeWordDetector()
is_activated = detector.detect_wake_word()  # Returns when "Jarvis" detected
user_input = detector.get_speech_input(timeout=10)
```

### `speech_to_text.py` - Speech Recognition
Converts audio to text with offline and online options.

**Key Features:**
- Vosk offline recognition (primary)
- Google Cloud fallback (requires internet)
- Configurable timeout
- Error handling and retries

**Usage:**
```python
from jarvis_desktop import SpeechToText

stt = SpeechToText(use_vosk=True)
text = stt.recognize()  # Returns transcribed text
```

### `text_to_speech.py` - Voice Synthesis
Generates natural speech from text using pyttsx3.

**Key Features:**
- Offline operation
- Multiple voice options (male/female)
- Rate and volume control
- Asynchronous speech support

**Usage:**
```python
from jarvis_desktop import TextToSpeech

tts = TextToSpeech(voice_type='female')
tts.speak("Hello World")
tts.speak_async("This runs in background")
```

### `gemini_brain.py` - AI Response Generation
Provides intelligent responses using Google Gemini API.

**Key Features:**
- Gemini Pro model integration
- Context-aware conversations
- SimpleBrain fallback for offline mode
- Predefined Q&A dictionary
- Response caching

**Usage:**
```python
from jarvis_desktop import GeminiBrain, SimpleBrain

brain = GeminiBrain(api_key='your_key')
response = brain.get_response("What's the weather?")

# Or use fallback
fallback = SimpleBrain()
response = fallback.ask("Hello")
```

### `commands.py` - System Automation
Executes system commands and PC automation tasks.

**Key Features:**
- 15+ supported applications
- Web control (browser, searches)
- System control (shutdown, restart)
- Cross-platform support (Windows/Mac/Linux)
- Command logging

**Usage:**
```python
from jarvis_desktop import SystemCommands

cmd = SystemCommands()
cmd.open_application('chrome')
cmd.open_website('google.com')
cmd.search_google('python')
cmd.shutdown_computer(delay=60)
```

### `main.py` - Main Application
Orchestrates all modules in continuous listening loop.

**Key Features:**
- Complete command parsing
- Action routing
- Error recovery
- Command history saving
- Graceful shutdown

**Usage:**
```bash
python -m jarvis_desktop.main
```

## System Requirements

### Minimum
- CPU: Dual-core processor
- RAM: 2GB
- Storage: 1GB
- Microphone: USB or built-in
- Network: Internet (for Gemini API, optional)

### Recommended
- CPU: Quad-core or better
- RAM: 4GB+
- Storage: 2GB
- Microphone: USB quality microphone
- Network: Broadband internet

## Installation Details

### Full Setup Guide
See [DESKTOP_SETUP_GUIDE.md](DESKTOP_SETUP_GUIDE.md) for:
- Platform-specific installation (Windows/Mac/Linux)
- Vosk model download and setup
- Gemini API configuration
- Troubleshooting common issues
- Advanced configuration

### Quick Requirements
```bash
# Desktop dependencies (in addition to Django requirements)
pip install pyttsx3==2.90
pip install SpeechRecognition==3.10.0
pip install pyaudio==0.2.13
pip install vosk==0.3.45
pip install google-generativeai==0.3.0
pip install pyautogui==0.9.53
pip install python-dotenv==1.0.0
```

## Configuration

### API Setup
Set `GEMINI_API_KEY` in `.env`:
```env
GEMINI_API_KEY=your_actual_api_key_from_google_cloud_console
```

### Voice Selection
Edit `jarvis_desktop/main.py` line ~30:
```python
self.tts = TextToSpeech(voice_type='female')  # or 'male'
```

### Application Customization
Edit `jarvis_desktop/commands.py` to add custom apps or commands

## Command Examples

**Say these phrases after "Jarvis":**

```
✅ "Jarvis, open Chrome"
✅ "Jarvis, search Python tutorials"
✅ "Jarvis, open YouTube"
✅ "Jarvis, what's the weather"
✅ "Jarvis, tell me a joke"
✅ "Jarvis, shutdown the computer in 60 seconds"
✅ "Jarvis, how do I code in Python?"
```

## Integration with Web Dashboard

The desktop app can sync with the Django web dashboard:

1. Run Django server: `python manage.py runserver`
2. Desktop app logs commands to database
3. View history in web UI: `http://localhost:8000`
4. Manage preferences in dashboard

## Performance Monitoring

### CPU Usage
- Idle: 2-5%
- Listening: 5-10%
- Processing: 10-15%
- Speaking: 8-12%

### Memory Usage
- Base: 150-200MB
- With Vosk model: 300-400MB
- Peak: 500MB

### Response Time
- Wake word detection: <1s
- Speech recognition: 2-5s
- AI response: 3-10s
- Total end-to-end: 5-15s

## Troubleshooting

### Common Issues

**Microphone not detected**
- Check system audio settings
- Test microphone with OS tools
- Restart application
- See DESKTOP_SETUP_GUIDE.md for detailed solutions

**Vosk model errors**
- Verify model downloaded correctly
- Check folder structure matches expected path
- Redownload if corrupted

**API key errors**
- Verify .env file exists and is readable
- Check API key format
- Enable Generative Language API in Google Cloud Console

**Speech recognition not working**
- Reduce background noise
- Speak more clearly
- Check microphone levels
- See full troubleshooting in DESKTOP_SETUP_GUIDE.md

## File Structure

```
jarvis_desktop/
├── __init__.py                    # Package exports
├── main.py                        # Main application (350 lines)
├── wake_word.py                   # Wake word detection (280 lines)
├── speech_to_text.py              # Speech-to-text (220 lines)
├── text_to_speech.py              # Text-to-speech (160 lines)
├── gemini_brain.py                # AI brain (230 lines)
├── commands.py                    # System commands (420 lines)
├── models/                        # Vosk models directory
│   └── vosk-model-en-us-0.42-gigaspeech/  # Download from alphacephei.com
└── command_history.json           # Generated on runtime
```

## Code Statistics

- **Total Lines**: 1,690+
- **Modules**: 7 (including __init__)
- **Classes**: 8 (WakeWordDetector, SpeechToText, TextToSpeech, SystemCommands, GeminiBrain, SimpleBrain, Jarvis)
- **Methods**: 50+
- **Error Handling**: Comprehensive with fallbacks
- **Documentation**: Full docstrings for all modules

## Platform Support

| Feature | Windows | macOS | Linux |
|---------|---------|-------|-------|
| Wake word detection | ✅ | ✅ | ✅ |
| Speech recognition | ✅ | ✅ | ✅ |
| Text-to-speech | ✅ | ✅ | ✅ |
| App control | ✅ | ⚠️ | ⚠️ |
| Web control | ✅ | ✅ | ✅ |
| System control | ✅ | ✅ | ✅ |
| Gemini API | ✅ | ✅ | ✅ |

⚠️ = Some applications may differ by OS

## Future Enhancements

- [ ] GUI dashboard for desktop
- [ ] Custom wake word detection
- [ ] Multi-language support
- [ ] Advanced automation (mouse control, keyboard shortcuts)
- [ ] Real-time speech visualization
- [ ] Command history dashboard
- [ ] Voice profile recognition
- [ ] Integration with smart home systems
- [ ] Skill marketplace for custom actions
- [ ] Offline Gemini model alternative

## Development

### Adding Custom Commands
Edit `jarvis_desktop/commands.py`:
```python
def custom_command(self):
    """Your custom command"""
    return "Action performed"
```

### Extending AI Brain
Edit `jarvis_desktop/gemini_brain.py` `SimpleBrain` class:
```python
'your_question': 'your_answer',
```

### Setting Breakpoints for Debugging
Enable debug mode in `.env`:
```env
DEBUG=True
LOG_LEVEL=DEBUG
```

## Performance Optimization

1. Use Vosk for offline mode (no API latency)
2. Pre-cache commonly asked questions
3. Run on SSD for faster model loading
4. Close unnecessary background apps
5. Use quality microphone for better recognition

## Security Considerations

- ✅ API keys stored in `.env` (not in git)
- ✅ Commands logged locally to JSON
- ✅ No cloud storage without user consent
- ✅ Microphone only active during listening
- ⚠️ Ensure PC auto-lock is enabled
- ⚠️ Review command history regularly

## Deployment

### Create Standalone Executable
```bash
pip install pyinstaller
pyinstaller --onefile --windowed jarvis_desktop/main.py
```

### Docker Container (Optional)
```dockerfile
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "-m", "jarvis_desktop.main"]
```

## Contributing

See DEVELOPER_GUIDE.md for contribution guidelines

## License

MIT License - See LICENSE file

## Support

- 📚 Documentation: DESKTOP_SETUP_GUIDE.md
- 🐛 Issues: GitHub Issues
- 💬 Discussions: GitHub Discussions
- 📧 Email: support@jarvis-ai.local

## Credits

- **Vosk**: Speech recognition engine (https://alphacephei.com/vosk/)
- **pyttsx3**: Text-to-speech synthesis
- **Google Generative AI**: Gemini API for intelligent responses
- **SpeechRecognition**: Google Cloud fallback

## Changelog

### v1.0.0 (Current)
- Initial desktop app release
- Complete offline capabilities
- Gemini AI integration
- 15+ system commands
- Cross-platform support
- Web dashboard sync

---

**Status**: ✅ Production Ready | **Last Updated**: 2024 | **Python**: 3.8+ | **License**: MIT

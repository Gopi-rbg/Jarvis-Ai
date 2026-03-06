# Jarvis AI Voice Assistant

A Django-based web application that works like a personal AI assistant, responding when you say the wake word **"Jarvis"**.

## Features

✨ **Voice Recognition**: Continuously listens for the wake word "Jarvis"
🎤 **Speech-to-Text**: Converts user speech to text using Web Speech API
🤖 **AI Responses**: Processes commands and generates intelligent responses
🔊 **Text-to-Speech**: Responds with voice output using browser Speech Synthesis API
⚡ **Command Execution**: Performs actions like opening websites, searching, etc.
💻 **Futuristic Dashboard**: Beautiful Jarvis-style UI with dark theme
📱 **Responsive Design**: Works on desktop and mobile devices
📝 **Conversation History**: Stores and displays past conversations
🔒 **User Authentication**: Simple login system to personalize the experience

## Supported Commands

- **"Jarvis, open YouTube"** - Opens YouTube
- **"Jarvis, open Google"** - Opens Google
- **"Jarvis, what time is it?"** - Tells current time
- **"Jarvis, search for [query]"** - Searches Google
- **"Jarvis, play music"** - Opens music streaming service
- **"Jarvis, tell me a joke"** - Tells a random joke
- **"Jarvis, open [website]"** - Opens various websites (GitHub, LinkedIn, Twitter, Facebook)
- And many more...

## Technology Stack

### Backend
- Django 5.2 - Web framework
- Django REST Framework - API development
- Python - Server-side logic
- SQLite - Database

### Frontend
- HTML5, CSS3 - Markup and styling
- Vanilla JavaScript - Interactivity
- Web Speech API - Speech recognition and synthesis
- CSS Animations - Visual effects

## Prerequisites

- Python 3.8+
- Modern web browser with:
  - Web Speech API support (Chrome, Edge, Firefox, Safari)
  - Microphone access
  - JavaScript enabled

## Installation & Setup

### 1. Clone or Download the Project

```bash
cd projectsust
```

### 2. Create Virtual Environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```
Follow the prompts to create an admin account.

### 6. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 7. Run Development Server

```bash
python manage.py runserver
```

The application will be available at: **http://localhost:8000**

## Usage

### First Time Setup

1. Navigate to `http://localhost:8000`
2. The Jarvis dashboard will load automatically
3. Allow microphone access when prompted by your browser
4. The microphone button will start listening for the wake word

### Using Jarvis

1. **Say "Jarvis"** to activate the assistant
2. After hearing "Jarvis", **say your command** (e.g., "open YouTube")
3. Jarvis will process your command and respond with voice
4. The chat history will display the conversation

### Manual Control

- **Click the microphone button** to manually toggle listening
- **Control buttons**:
  - 🗑️ Clear Chat
  - ⚙️ Settings
  - 🔊 Volume Control

### Settings

Access settings to:
- Change voice (Male/Female)
- Enable/disable auto-listen for wake word
- Toggle dark mode
- Adjust volume

### View History

Click "History" in the navigation to:
- View all past conversations
- View individual conversations
- Delete conversations

## File Structure

```
projectsust/
├── projectsust/              # Project settings
│   ├── settings.py          # Django settings
│   ├── urls.py              # URL configuration
│   ├── asgi.py
│   └── wsgi.py
├── core/                     # Main app
│   ├── models.py            # Database models
│   ├── views.py             # API views
│   ├── urls.py              # App URL routing
│   ├── serializers.py       # DRF serializers
│   └── admin.py             # Admin panel
├── templates/               # HTML templates
│   └── core/
│       └── index.html       # Main dashboard
├── static/                  # Static files
│   ├── css/
│   │   └── style.css        # Main stylesheet
│   └── js/
│       ├── app.js           # Main app logic
│       ├── speech-recognition.js
│       ├── text-to-speech.js
│       └── ui.js            # UI utilities
├── manage.py
└── requirements.txt         # Python dependencies
```

## API Endpoints

### Process Command
**POST** `/core/api/process-command/`
- Sends user text and receives Jarvis response
- Requires authentication

### Conversation History
**GET** `/core/api/conversation-history/`
- Gets all conversations for the user

### Get Conversation
**GET** `/core/api/conversation/<id>/`
- Gets details of a specific conversation

### Delete Conversation
**DELETE** `/core/api/conversation/<id>/delete/`
- Deletes a conversation

### Get Commands
**GET** `/core/api/commands/`
- Gets command history

### Clear History
**POST** `/core/api/clear-history/`
- Clears all conversation history

## Browser Compatibility

| Browser | Speech Recognition | Speech Synthesis | Status |
|---------|:------------------:|:----------------:|:------:|
| Chrome  |         ✅         |        ✅        |  Best  |
| Edge    |         ✅         |        ✅        |  Best  |
| Firefox |         ✅         |        ✅        |  Good  |
| Safari  |         ✅         |        ✅        |  Good  |

## Configuration

### OpenAI Integration (Optional)

To add AI-powered responses (instead of fallback responses):

1. Get an API key from [OpenAI](https://openai.com)
2. Update in `projectsust/settings.py`:

```python
JARVIS_CONFIG = {
    'OPENAI_API_KEY': 'your-api-key-here',
    'WAKE_WORD': 'jarvis',
}
```

3. Install openai package:
```bash
pip install openai
```

## Troubleshooting

### Microphone Not Working
- Check browser permissions for microphone access
- Ensure microphone is connected and working
- Try a different browser

### Speech Recognition Not Working
- Verify browser supports Web Speech API
- Check internet connection (some features need it)
- Refresh the page

### CSS Not Loading
- Run: `python manage.py collectstatic`
- Clear browser cache (Ctrl+Shift+Delete)

### Database Errors
- Run: `python manage.py makemigrations`
- Run: `python manage.py migrate`

### Port Already in Use
- Use a different port: `python manage.py runserver 8001`

## Performance Tips

1. **Enable compression** for faster loading
2. **Use production server** (Gunicorn) instead of Django dev server
3. **Optimize static files** with minification
4. **Use CDN** for better performance

## Security Considerations

⚠️ **For Production:**
1. Change SECRET_KEY in settings.py
2. Set DEBUG = False
3. Configure ALLOWED_HOSTS
4. Use environment variables for sensitive data
5. Use HTTPS
6. Set up proper CORS configuration
7. Implement rate limiting on API endpoints

## Deployment

### Using Gunicorn

```bash
pip install gunicorn
gunicorn projectsust.wsgi:application --bind 0.0.0.0:8000
```

### Using Docker

Create a Dockerfile (optional):

```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN python manage.py collectstatic --noinput
CMD ["gunicorn", "projectsust.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## Advanced Features

### Custom Voice Commands

Edit `parse_and_execute_command()` in `core/views.py` to add custom commands.

### Webhook Integration

Add external API calls to trigger events:

```python
def execute_command(command_type, command_text):
    if command_type == 'custom':
        # Call external API
        requests.post('https://api.example.com/command', json={'text': command_text})
```

### Intent Recognition

Integrate intent classification using:
- RASA NLU
- spaCy
- TensorFlow

## Contributing

Feel free to fork and enhance the project!

## License

MIT License - Free to use and modify

## Support

For issues or questions:
1. Check the troubleshooting section
2. Read Django documentation: https://docs.djangoproject.com
3. Check Web Speech API docs: https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API

## Future Enhancements

- [ ] Integration with more AI services
- [ ] Custom wake word training
- [ ] Multi-language support
- [ ] IoT device control
- [ ] Calendar integration
- [ ] Email automation
- [ ] Smart home integration
- [ ] Mobile app version

## Credits

Built with Django, Web Speech API, and futuristic UI design.

---

**Enjoy your personal AI assistant! 🤖**

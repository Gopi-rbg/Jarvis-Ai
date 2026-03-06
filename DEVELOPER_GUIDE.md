# Jarvis API Documentation & Developer Guide

Technical documentation for developers extending Jarvis functionality.

## REST API Endpoints

### Authentication

All protected endpoints require Django session authentication or CSRF token.

```python
# Get CSRF token from cookies
csrftoken = request.COOKIES.get('csrftoken')
```

### 1. Process Command

**Endpoint:** `POST /core/api/process-command/`

**Description:** Send user text and receive Jarvis response

**Request:**
```json
{
    "text": "open YouTube"
}
```

**Response:**
```json
{
    "response": "Opening YouTube for you. Opening in a new tab.",
    "command_type": "website",
    "command_text": "open youtube",
    "conversation_id": 1,
    "timestamp": "2024-03-06T10:30:45.123Z"
}
```

**Status Codes:**
- `200` - Success
- `400` - Bad request (missing text)
- `401` - Unauthorized
- `500` - Server error

**Example (JavaScript):**
```javascript
const response = await fetch('/core/api/process-command/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
    },
    body: JSON.stringify({ text: 'tell me a joke' })
});
const data = await response.json();
console.log(data.response);
```

### 2. Get Conversation History

**Endpoint:** `GET /core/api/conversation-history/`

**Response:**
```json
{
    "conversations": [
        {
            "id": 1,
            "user": 1,
            "created_at": "2024-03-06T10:30:45.123Z",
            "updated_at": "2024-03-06T10:30:45.123Z",
            "messages": [
                {
                    "id": 1,
                    "role": "user",
                    "content": "what time is it",
                    "command_detected": "get time",
                    "timestamp": "2024-03-06T10:30:45.123Z"
                },
                {
                    "id": 2,
                    "role": "jarvis",
                    "content": "The current time is 10:30 AM.",
                    "command_detected": null,
                    "timestamp": "2024-03-06T10:30:46.123Z"
                }
            ]
        }
    ]
}
```

### 3. Get Single Conversation

**Endpoint:** `GET /core/api/conversation/{id}/`

**Parameters:**
- `id` (integer) - Conversation ID

**Response:** Same format as individual conversation in history

### 4. Delete Conversation

**Endpoint:** `DELETE /core/api/conversation/{id}/delete/`

**Response:**
```json
{
    "success": "Conversation deleted"
}
```

### 5. Get User Commands

**Endpoint:** `GET /core/api/commands/`

**Response:**
```json
{
    "commands": [
        {
            "id": 1,
            "command_text": "open youtube",
            "command_type": "website",
            "response": "Opening YouTube for you...",
            "executed": true,
            "created_at": "2024-03-06T10:30:45.123Z"
        }
    ]
}
```

### 6. Clear History

**Endpoint:** `POST /core/api/clear-history/`

**Response:**
```json
{
    "success": "History cleared"
}
```

## Database Models

### Conversation Model

```python
class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

**Methods:**
- `.messages.all()` - Get all messages in conversation
- `.delete()` - Delete conversation and related messages

### Message Model

```python
class Message(models.Model):
    ROLE_CHOICES = [('user', 'User'), ('jarvis', 'Jarvis')]
    
    conversation = models.ForeignKey(Conversation, ...)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    command_detected = models.CharField(max_length=255, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
```

**Common Queries:**
```python
# Get all user messages
Message.objects.filter(conversation__user=user, role='user')

# Get last 10 messages
Message.objects.all().order_by('-timestamp')[:10]

# Get messages from specific conversation
conversation.messages.all()
```

### JarvisCommand Model

```python
class JarvisCommand(models.Model):
    COMMAND_TYPE_CHOICES = [
        ('website', 'Open Website'),
        ('question', 'Answer Question'),
        ('joke', 'Tell Joke'),
        ('time', 'Get Time'),
        ('search', 'Web Search'),
        ('music', 'Play Music'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, ...)
    message = models.ForeignKey(Message, ...)
    command_text = models.TextField()
    command_type = models.CharField(...)
    response = models.TextField()
    executed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
```

## Command Types

| Type | Trigger Words | Example |
|------|---------------|---------|
| `website` | youtube, google, github, etc. | "open YouTube" |
| `question` | any question | "what is Python" |
| `joke` | tell joke, make me laugh | "tell me a joke" |
| `time` | time, what time, tell me the time | "what time is it" |
| `search` | search, find, look up | "search for Django" |
| `music` | play music, play song | "play music" |
| `other` | unknown commands | any other input |

## Adding Custom Commands

### 1. Add Command Type to Model

Edit `core/models.py`:

```python
COMMAND_TYPE_CHOICES = [
    # ... existing choices ...
    ('weather', 'Get Weather'),
    ('email', 'Send Email'),
]
```

### 2. Update Command Parser

Edit `core/views.py`, in `parse_and_execute_command()` function:

```python
def parse_and_execute_command(text, user):
    text_lower = text.lower()
    
    # Your custom command
    if any(word in text_lower for word in ['weather', 'forecast']):
        command_type = 'weather'
        city = extract_city(text_lower)  # Helper function
        response = f"Getting weather for {city}..."
        return command_type, response, f"weather {city}"
    
    # ... rest of function ...
```

### 3. Add Backend Logic

```python
def get_weather(city):
    """Fetch weather data"""
    import requests
    api_url = f"https://weather.api.example.com/city/{city}"
    response = requests.get(api_url)
    return response.json()

def parse_and_execute_command(text, user):
    # ... after parsing command type ...
    if command_type == 'weather':
        weather_data = get_weather(city)
        response = f"Current temperature in {city} is {weather_data['temp']}°C"
```

### 4. Update Frontend (Optional)

Edit `static/js/app.js`, in `executeCommand()` method:

```javascript
executeCommand(commandType, commandText) {
    switch (commandType) {
        // ... existing cases ...
        
        case 'weather':
            // Handle weather command in frontend
            break;
    }
}
```

## Frontend JavaScript Classes

### SpeechRecognitionModule

```javascript
const speechRec = new SpeechRecognitionModule();

// Set wake word
speechRec.setWakeWord('hello');

// Set language
speechRec.setLanguage('en-US');

// Handle results
speechRec.onResult((type, data) => {
    if (type === 'wake-word') {
        console.log('Wake word detected!');
    } else if (type === 'command') {
        console.log('Command:', data);
    }
});

// Handle errors
speechRec.onError((message, error) => {
    console.error('Speech error:', message);
});

// Control
speechRec.start();
speechRec.stop();
speechRec.abort();
```

### TextToSpeechModule

```javascript
const tts = new TextToSpeechModule();

// Speak text
tts.speak('Hello world', (event) => {
    console.log('Speech event:', event);
});

// Set voice
tts.setVoiceByType('female');  // or 'male'

// Control volume (0-100)
tts.setVolume(80);

// Control speed (0.5-2.0)
tts.setRate(1.0);

// Control pitch (0.0-2.0)
tts.setPitch(1.0);

// Control
tts.stop();
tts.pause();
tts.resume();
tts.isSpeaking();  // returns boolean
```

### JarvisApp

```javascript
jarvisApp.startListening();
jarvisApp.stopListening();
jarvisApp.toggleListening();

jarvisApp.processCommand('open youtube');

jarvisApp.addMessageToChat('Hello', 'user');
jarvisApp.updateStatus('Processing...');

jarvisApp.clearChat();
jarvisApp.loadHistory();
jarvisApp.showSection('settingsSection');
```

## Extending with External APIs

### Example: Add Weather Integration

```python
# In core/views.py
import requests

def get_weather_response(city):
    """Get weather from OpenWeatherMap API"""
    try:
        api_key = settings.WEATHER_API_KEY
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        response = requests.get(url, timeout=5)
        data = response.json()
        
        temp = data['main']['temp']
        description = data['weather'][0]['description']
        
        return f"In {city}, it's {temp}°C with {description}"
    except:
        return f"I couldn't get the weather for {city}. Try later."

def parse_and_execute_command(text, user):
    # ... existing code ...
    
    if any(word in text_lower for word in ['weather', 'forecast']):
        match = re.search(r'weather.*?(?:in|for)\s+(\w+)', text_lower)
        city = match.group(1) if match else 'London'
        response = get_weather_response(city)
        return 'weather', response, f"weather {city}"
    
    # ... rest ...
```

## Webhooks & Event Handling

### Enable event logging

```python
# In core/views.py
import logging

logger = logging.getLogger(__name__)

def process_command(request):
    logger.info(f"User {request.user} sent command: {text}")
    # ... rest of function ...
```

### Post to External Webhook

```python
def send_webhook(data):
    """Send command to external service"""
    webhook_url = settings.WEBHOOK_URL
    try:
        requests.post(webhook_url, json=data, timeout=5)
    except Exception as e:
        logger.error(f"Webhook error: {e}")

def process_command(request):
    # ... process command ...
    send_webhook({
        'user_id': request.user.id,
        'command': user_text,
        'response': response,
        'timestamp': timezone.now().isoformat()
    })
```

## Caching Responses

### Using Django Cache

```python
from django.core.cache import cache

def parse_and_execute_command(text, user):
    # Check cache
    cache_key = f"command_{text}_{user.id}"
    cached_response = cache.get(cache_key)
    if cached_response:
        return cached_response
    
    # ... process command ...
    
    # Cache result
    cache.set(cache_key, result, timeout=3600)  # 1 hour
    return result
```

## Performance Optimization

### Use select_related for queries

```python
# Instead of:
conversations = Conversation.objects.all()

# Use:
conversations = Conversation.objects.select_related('user').prefetch_related('messages')
```

### Paginate large result sets

```python
from django.core.paginator import Paginator

def get_conversation_history(request):
    conversations = Conversation.objects.filter(user=request.user)
    paginator = Paginator(conversations, 10)  # 10 per page
    page = request.GET.get('page', 1)
    page_obj = paginator.get_page(page)
```

## Testing

### Unit Tests Example

```python
# core/tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Conversation, Message

class ConversationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@test.com', 'password')
        self.conversation = Conversation.objects.create(user=self.user)
    
    def test_message_creation(self):
        message = Message.objects.create(
            conversation=self.conversation,
            role='user',
            content='Hello'
        )
        self.assertEqual(message.content, 'Hello')
        self.assertEqual(message.conversation, self.conversation)
```

Run tests:
```bash
python manage.py test core
```

## Debugging

### Django Shell

```bash
python manage.py shell

# Then in shell:
from core.models import Conversation
Conversation.objects.all()
user.jarvis_conversations.all()
```

### Enable SQL Logging

```python
# settings.py
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

### Browser DevTools

- **Console**: Debug JavaScript
- **Network**: Monitor API calls
- **Application**: Check IndexedDB/LocalStorage

## Rate Limiting

### Add rate limiting to API

```python
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

@cache_page(1)  # Cache 1 second
def process_command(request):
    # ... prevent rapid requests ...
```

Or use package:
```bash
pip install django-ratelimit
```

---

## Resources

- [Django Docs](https://docs.djangoproject.com)
- [Web Speech API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API)
- [Django REST Framework](https://www.django-rest-framework.org)
- [Python Requests](https://requests.readthedocs.io)

---

**Happy Coding! 🚀**

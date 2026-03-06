# Jarvis AI Voice Assistant - Setup Guide

Complete step-by-step guide to get Jarvis running on your machine.

## System Requirements

- **OS**: Windows, macOS, or Linux
- **Python**: 3.8 or higher
- **Disk Space**: ~500 MB
- **RAM**: 2 GB minimum
- **Browser**: Chrome, Edge, Firefox, or Safari (latest version)

## Step-by-Step Installation

### Step 1: Verify Python Installation

Open Command Prompt (Windows) or Terminal (macOS/Linux) and run:

```bash
python --version
```

You should see Python 3.8 or higher. If not, download from https://www.python.org

### Step 2: Navigate to Project Directory

```bash
cd path/to/projectsust
```

Replace `path/to/projectsust` with your actual project directory.

### Step 3: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt when activated.

### Step 4: Upgrade pip and Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will install:
- Django 5.2
- Django REST Framework
- CORS headers
- And other dependencies

Wait for installation to complete (2-5 minutes).

### Step 5: Apply Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

This creates the database tables needed for storing conversations and commands.

### Step 6: Create Admin User

```bash
python manage.py createsuperuser
```

Follow the prompts:
```
Username: admin
Email address: admin@example.com
Password: (enter your password)
Password (again): (repeat password)
```

Remember these credentials - you'll need them to access the admin panel.

### Step 7: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

This prepares CSS, JavaScript, and other static files.

### Step 8: Start the Development Server

```bash
python manage.py runserver
```

You should see output like:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### Step 9: Open in Browser

1. Open your web browser
2. Go to: **http://localhost:8000** or **http://127.0.0.1:8000**
3. You should see the Jarvis dashboard

## First Time Usage

### Enable Microphone Access

When you first load the page, your browser will ask for microphone permission.

- **Chrome**: Click the permission icon and "Allow"
- **Firefox**: Click "Allow" when prompted
- **Safari**: System will prompt - click "Allow"
- **Edge**: Click the permission icon and "Allow"

### Start Using Jarvis

1. The microphone button should show "Click to Speak"
2. Click the button to start listening
3. Say **"Jarvis"** clearly (wake word)
4. After you hear a beep, say your command:
   - "open YouTube"
   - "what time is it"
   - "tell me a joke"
   - etc.

## Accessing Admin Panel

1. Go to: **http://localhost:8000/admin**
2. Log in with your superuser credentials
3. You can:
   - View conversation history
   - Monitor commands
   - Manage users
   - Delete data

## Common Issues & Solutions

### Issue: "Port 8000 already in use"

**Solution:**
```bash
python manage.py runserver 8001
```

Then access at `http://localhost:8001`

### Issue: "ModuleNotFoundError" or Missing Packages

**Solution:**
```bash
pip install -r requirements.txt --force-reinstall
```

### Issue: Database locked or migration errors

**Solution:**
```bash
python manage.py migrate --run-syncdb
```

### Issue: Static files not loading (no CSS)

**Solution:**
```bash
python manage.py collectstatic --noinput --clear
```

Then restart the server.

### Issue: Microphone not working

**Checklist:**
- [ ] Microphone is physically connected
- [ ] Microphone is not muted
- [ ] Browser has microphone permission
- [ ] Browser is up to date
- [ ] Try a different browser
- [ ] Check System Sound Settings

### Issue: Speech Recognition gives "No speech detected"

**Solutions:**
- Speak louder and closer to microphone
- Check microphone level in System Settings
- Reduce background noise
- Ensure stable internet connection

### Issue: Can't create superuser or migrate

**Solution:**
Delete the database and start fresh:
```bash
# Windows
del db.sqlite3

# macOS/Linux
rm db.sqlite3

# Then run migrations again
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

## Optional: OpenAI API Integration

For advanced AI responses:

### 1. Get API Key

- Visit https://openai.com/api/
- Create an account and get API key
- (Requires paid account or free trial)

### 2. Install OpenAI Package

```bash
pip install openai
```

### 3. Configure in Settings

Edit `projectsust/settings.py`:

```python
JARVIS_CONFIG = {
    'OPENAI_API_KEY': 'sk-your-actual-api-key-here',
    'WAKE_WORD': 'jarvis',
}
```

### 4. Restart Server

```bash
python manage.py runserver
```

Now Jarvis will use OpenAI for smarter responses!

## Optional: Custom Wake Word

To change from "Jarvis" to something else:

1. Edit `projectsust/settings.py`
2. Find `JARVIS_CONFIG`
3. Change `'WAKE_WORD': 'jarvis'` to your word
4. Or change in Settings on the UI

Examples:
```python
'WAKE_WORD': 'hey'
'WAKE_WORD': 'alexa'
'WAKE_WORD': 'code'
```

## Production Deployment

For deploying to a server (not for local development):

### Using Gunicorn

```bash
pip install gunicorn
gunicorn projectsust.wsgi:application --bind 0.0.0.0:8000
```

### Using Docker

Create a file named `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "projectsust.wsgi:application", "--bind", "0.0.0.0:8000"]
```

Build and run:
```bash
docker build -t jarvis .
docker run -p 8000:8000 jarvis
```

### Cloud Deployment

**Heroku, PythonAnywhere, Render, etc:**
1. Follow platform-specific Django deployment guides
2. Update `ALLOWED_HOSTS` in settings.py
3. Set `DEBUG = False`
4. Use environment variables for secrets

## Testing & Verification

### Test Speech Recognition
1. Click microphone button
2. Wait for "Listening for wake word..."
3. Say "Jarvis"
4. You should hear a beep

### Test Commands
After saying "Jarvis":
- Say: "what time is it" → Should tell you current time
- Say: "open youtube" → Should open YouTube
- Say: "tell me a joke" → Should tell a joke

### Test Admin Panel
1. Go to http://localhost:8000/admin
2. Log in with your superuser
3. You should see conversations and commands

### Test Chat History
1. After running commands, click "History"
2. You should see your conversations
3. Click "View" to see conversation details

## Performance Optimization

### Disable Debug Mode locally (faster):

Edit `projectsust/settings.py`:
```python
DEBUG = False
```

Then run:
```bash
python manage.py runserver
```

### Limit Query Results

Edit `core/views.py`, around line where commands are loaded:
```python
commands = JarvisCommand.objects.filter(user=request.user).order_by('-created_at')[:50]
```

Change `[:50]` to smaller number if needed.

## Monitoring & Logs

### View Django Logs

The terminal where you ran `python manage.py runserver` shows all logs.

### Check Database

```bash
python manage.py dbshell
```

Then you can run SQL queries to inspect data.

### View Conversation Data

```bash
python manage.py shell
```

Then in the Python shell:
```python
from core.models import Conversation
Conversation.objects.all().count()  # Show total conversations
```

## Backup & Data

### Backup Database

```bash
# Windows/macOS/Linux
cp db.sqlite3 db.sqlite3.backup
```

### Export Data

```bash
python manage.py dumpdata > backup.json
```

### Restore Data

```bash
python manage.py loaddata backup.json
```

## Uninstall & Cleanup

To remove the application:

```bash
# Deactivate virtual environment
deactivate

# Remove virtual environment folder
# Windows: rmdir venv /s
# macOS/Linux: rm -rf venv

# Delete project folder if desired
```

## Need Help?

1. **Check README.md** for feature overview
2. **Review error messages** carefully
3. **Search Django docs**: https://docs.djangoproject.com
4. **Check Web Speech API docs**: https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API
5. **Try in different browser** to isolate issues

## Next Steps

After setup is complete:
- [ ] Test all voice commands
- [ ] Set up OpenAI integration
- [ ] Customize settings
- [ ] View conversation history
- [ ] Add custom commands
- [ ] Share with others!

---

**Congratulations! You now have a working Jarvis AI Voice Assistant! 🎉**

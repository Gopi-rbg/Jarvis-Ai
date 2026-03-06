# Jarvis - Troubleshooting Guide

Complete troubleshooting guide for common issues and solutions.

## Installation Issues

### Problem: "Python not found" or "python is not recognized"

**Solutions:**
1. Ensure Python is installed: https://python.org
2. Add Python to PATH:
   - Windows: During installation, check "Add Python to PATH"
   - macOS: Usually automatic
   - Linux: `sudo apt install python3`
3. Verify: Open terminal and run `python --version`
4. Use `python3` instead of `python` on macOS/Linux

### Problem: "pip: command not found"

**Solutions:**
1. `pip` comes with Python, upgrade it:
   ```bash
   python -m pip install --upgrade pip
   ```
2. Or install explicitly:
   - Windows: `python -m ensurepip`
   - macOS/Linux: `python3 -m pip install --upgrade pip`

### Problem: "venv: command not found"

**Solutions:**
1. Create venv differently:
   ```bash
   python -m venv venv
   ```
2. Or install virtualenv:
   ```bash
   pip install virtualenv
   virtualenv venv
   ```

### Problem: "Permission denied" error

**Solutions:**
- Windows: Run Command Prompt as Administrator
- macOS/Linux: 
  ```bash
  sudo chown -R $USER ~/projectsust
  ```

---

## Virtual Environment Issues

### Problem: "Not in virtual environment"

**Check if activated:**
- Windows: Should show `(venv)` in prompt
- macOS/Linux: Should show `(venv)` before $

**Reactivate:**
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Problem: "Cannot activate venv"

**Recreate it:**
```bash
# Remove old environment
# Windows: rmdir venv /s
# macOS/Linux: rm -rf venv

# Create new
python -m venv venv

# Activate
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
```

### Problem: "pip install hangs"

**Solutions:**
1. Set timeout:
   ```bash
   pip install -r requirements.txt --default-timeout=1000
   ```
2. Use different index:
   ```bash
   pip install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt
   ```
3. Install one by one:
   ```bash
   pip install Django
   pip install djangorestframework
   pip install django-cors-headers
   ```

---

## Database Issues

### Problem: "Database is locked"

**Solutions:**
1. Stop all Django processes
2. Remove lock file:
   ```bash
   rm db.sqlite3-journal  # macOS/Linux
   del db.sqlite3-journal # Windows
   ```
3. Run migrations fresh:
   ```bash
   python manage.py migrate --no-input
   ```

### Problem: "No such table: core_conversation"

**Solutions:**
```bash
# Apply all migrations
python manage.py migrate

# Or if that doesn't work
python manage.py migrate --run-syncdb

# Or start fresh (DELETE DATA!)
rm db.sqlite3
python manage.py migrate
```

### Problem: "Error: target database is PostgreSQL"

**Solutions:**
This is just a warning. You can ignore it or:
1. Change to PostgreSQL in settings
2. Or use SQLite (default, no change needed)

### Problem: "Superuser creation failed"

**Solutions:**
```bash
# Try again (it will ask for username/password)
python manage.py createsuperuser

# Or create via shell
python manage.py shell
# Then type:
# from django.contrib.auth.models import User
# User.objects.create_superuser('admin', 'admin@test.com', 'password')
# exit()
```

### Problem: "ProgrammingError: relation does not exist"

**Solutions:**
```bash
# Reset database
rm db.sqlite3

# Reapply all migrations
python manage.py migrate

# Create superuser again
python manage.py createsuperuser
```

---

## Server Issues

### Problem: "Port 8000 already in use"

**Solutions:**
1. Use different port:
   ```bash
   python manage.py runserver 8001
   ```

2. Find and kill process:
   - Windows:
     ```bash
     netstat -ano | findstr 8000
     taskkill /PID xxxxx /F
     ```
   - macOS/Linux:
     ```bash
     lsof -i :8000
     kill -9 PID
     ```

### Problem: "Error: failed to find a valid Django app"

**Solutions:**
1. Ensure you're in correct directory (with manage.py)
2. Check settings.py INSTALLED_APPS includes 'core'
3. Ensure no syntax errors:
   ```bash
   python -m py_compile projectsust/settings.py
   ```

### Problem: "ModuleNotFoundError" when starting server

**Solutions:**
```bash
# Reinstall all requirements
pip install --force-reinstall -r requirements.txt

# Check installation
python -m pip list
```

### Problem: "Address already in use" or "Cannot bind"

**Solutions:**
```bash
# Windows
netstat -ano | findstr :8000

# macOS/Linux
sudo lsof -i :8000 | grep LISTEN

# Then kill the process
```

---

## Static Files Issues

### Problem: "CSS not loading" or "404 on static files"

**Solutions:**
1. Collect static files:
   ```bash
   python manage.py collectstatic --noinput
   ```

2. Clear cache:
   ```bash
   python manage.py collectstatic --clear --noinput
   ```

3. Check settings.py:
   ```python
   STATIC_URL = 'static/'
   STATICFILES_DIRS = [BASE_DIR / 'static']
   ```

4. Restart server:
   ```bash
   # Press Ctrl+C
   # Then run again
   python manage.py runserver
   ```

5. Hard refresh browser:
   - Ctrl+Shift+R (Windows/Linux)
   - Cmd+Shift+R (macOS)

### Problem: "Static files in wrong location"

**Check this structure:**
```
projectsust/
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── app.js
│       └── ...
├── templates/
│   └── core/
│       └── index.html
└── manage.py
```

---

## Microphone & Voice Issues

### Problem: "Microphone not working"

**Checklist:**
- [ ] Is microphone connected?
- [ ] Is microphone muted? (check system volume)
- [ ] Did you allow browser permission?
- [ ] Is browser updated to latest version?
- [ ] Are you using HTTPS? (some browsers require it)
- [ ] Try different browser

**Troubleshoot:**
1. Check browser permissions:
   - Chrome: Settings → Privacy → Site settings → Microphone
   - Firefox: Preferences → Privacy → Permissions → Microphone
   - Safari: System Preferences → Security & Privacy → Microphone

2. Test microphone:
   ```bash
   # Windows
   # Settings → Sound → Input

   # macOS
   # System Preferences → Sound → Input

   # Linux
   # Just check levels are not at 0
   ```

3. Use browser console to test:
   - Open developer tools (F12)
   - Go to Console tab
   - Paste:
     ```javascript
     navigator.mediaDevices.enumerateDevices().then(devices => {
         const mics = devices.filter(d => d.kind === 'audioinput');
         console.log('Microphones:', mics);
     });
     ```

### Problem: "No speech detected"

**Solutions:**
1. Speak louder and clearer
2. Reduce background noise
3. Move closer to microphone
4. Check microphone levels
5. Try a different brand/type of microphone
6. Use HTTPS (SSL certificate)
7. Check internet connection

### Problem: "Speech is not being recognized"

**Solutions:**
1. Say the wake word clearly: "JAR-VIS" (not "jar-bees")
2. Wait for listening indicator
3. Speak after the beep sound
4. Check language setting is English
5. Try in different browser
6. Clear browser cache (Ctrl+Shift+Delete)

### Problem: "Speaker/TTS not working"

**Solutions:**
1. Check volume isn't muted
2. Check system volume is up
3. Try different browser
4. Test with: Settings → Voice selection
5. Clear browser storage:
   - Press F12
   - Application → Storage → Clear Site Data

### Problem: "Accent not recognized"

**Solutions:**
1. Speak more clearly
2. Enunciate each word
3. Try English (US) setting instead of British
4. Train your microphone:
   - Windows: Settings → Sound
   - macOS: System Preferences → Accessibility

---

## API Issues

### Problem: "API returning 401 Unauthorized"

**Solutions:**
1. Log in first to get session
2. Ensure CSRF token is included in request
3. Check browser has cookies enabled
4. Try in incognito mode

### Problem: "CORS error"

**Solutions:**
```python
# In projectsust/settings.py
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]
```

### Problem: "API returns 500 error"

**Solutions:**
1. Check server console for error message
2. Check DEBUG = True in settings
3. Look at browser console (F12)
4. Try simpler command first
5. Check OpenAI API key if using it

---

## Admin Panel Issues

### Problem: "Can't access admin panel"

**Solutions:**
1. Go to correct URL: `http://localhost:8000/admin`
2. Log in with superuser credentials
3. Reset password if forgotten:
   ```bash
   python manage.py changepassword admin
   ```
4. Create new superuser:
   ```bash
   python manage.py createsuperuser
   ```

### Problem: "Admin panel shows no data"

**Solutions:**
1. Ensure models are registered in admin.py
2. Check core/admin.py has @admin.register decorators
3. Run migrations to create tables
4. Add some data via UI

### Problem: "Admin interface slow"

**Solutions:**
1. Limit query results
2. Use select_related/prefetch_related
3. Remove heavy filters
4. Check database is not too large

---

## Browser Issues

### Problem: "Works in Chrome but not Firefox"

**Solutions:**
1. Update browser to latest version
2. Clear cache and cookies
3. Try incognito/private mode
4. Check if Firefox has Web Speech API support
5. Enable speech recognition in about:config

### Problem: "Page takes long to load"

**Solutions:**
1. Check internet connection
2. Minimize static files
3. Use browser cache
4. Check server isn't overloaded
5. Restart server

### Problem: "Chat keeps scrolling to top"

**Solutions:**
1. This is normal behavior
2. Refresh page if needed
3. Check browser console for errors
4. Try different browser

---

## Performance Issues

### Problem: "Application is slow"

**Solutions:**
1. Upgrade to faster internet
2. Use modern browser
3. Close other tabs/programs
4. Check CPU/RAM usage
5. Restart server
6. Clear browser cache

### Problem: "Speech recognition lag"

**Solutions:**
1. Closer to router for better WiFi
2. Reduce background apps
3. Use wired connection
4. Improve microphone quality
5. Restart browser

---

## Data Issues

### Problem: "Lost conversation history"

**Solutions:**
1. Check if data is in database:
   ```bash
   python manage.py shell
   from core.models import Conversation
   Conversation.objects.count()
   ```

2. Restore from backup:
   ```bash
   python manage.py loaddata backup.json
   ```

### Problem: "Can't delete conversation"

**Solutions:**
1. Make sure you're logged in as the user
2. Go to admin panel to delete
3. Check database hasn't crashed
4. Try clearing all history instead

---

## Getting Help

If you can't fix the issue:

1. **Check error messages** carefully in:
   - Browser console (F12 → Console tab)
   - Terminal where server is running
   - Django logs

2. **Search the documentation:**
   - SETUP_GUIDE.md
   - DEVELOPER_GUIDE.md
   - README.md

3. **Check online resources:**
   - Django docs: https://docs.djangoproject.com
   - Web Speech API: https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API
   - Stack Overflow: https://stackoverflow.com/questions/tagged/django

4. **Common next steps:**
   - Restart the server
   - Clear browser cache
   - Reinstall dependencies
   - Start with fresh database
   - Try different browser

---

## Emergency Fixes

If everything breaks:

```bash
# Start completely fresh
rm db.sqlite3
rm -rf venv
python -m venv venv
venv\Scripts\activate  # or source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

**Still having issues?**

Re-read the SETUP_GUIDE.md for step-by-step instructions, or check the documentation files in the project folder.

Good luck! 🚀

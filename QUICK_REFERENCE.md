# Jarvis - Quick Reference Guide

## 🚀 Quick Start (Copy & Paste)

### Windows
```batch
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Then go to: **http://localhost:8000**

### macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Then go to: **http://localhost:8000**

---

## 🎤 Using Jarvis

1. **Allow Microphone** - Click "Allow" when browser asks
2. **Say "Jarvis"** - Activate the assistant
3. **Say Your Command** - e.g., "open YouTube"
4. **Listen to Response** - Jarvis responds with voice

---

## 📝 Command Examples

| Command | What It Does |
|---------|--------------|
| "open YouTube" | Opens YouTube |
| "open Google" | Opens Google |
| "what time is it" | Tells current time |
| "tell me a joke" | Tells random joke |
| "search for Python" | Searches Google |
| "play music" | Opens Spotify |
| "open GitHub" | Opens GitHub |
| "open LinkedIn" | Opens LinkedIn |

---

## 🎚️ Controls

| Button | Function |
|--------|----------|
| 🎤 Microphone | Click to listen/speak |
| 🗑️ Trash | Clear chat |
| ⚙️ Settings | Configure voice/theme |
| 🔊 Volume | Adjust speaker volume |

---

## ⚙️ Navigation

| Menu | What You Can Do |
|------|-----------------|
| Home | See main dashboard |
| History | View past conversations |
| Settings | Change voice, dark mode, etc. |
| Logout | Sign out |

---

## 🗂️ Important URLs

- **Dashboard**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin
- **API**: http://localhost:8000/core/api/

---

## 📚 Documentation Files

- **README.md** - Full features & setup
- **SETUP_GUIDE.md** - Detailed installation steps
- **DEVELOPER_GUIDE.md** - For programmers extending it
- **PROJECT_SUMMARY.md** - Project overview

---

## 🐛 Common Issues & Fixes

### "Port already in use"
```bash
python manage.py runserver 8001
```

### "Static files not loading"
```bash
python manage.py collectstatic --clear --noinput
```

### "Database errors"
```bash
python manage.py migrate --run-syncdb
```

### "Microphone not working"
- Check system microphone settings
- Try different browser
- Refresh page (Ctrl+R)

---

## 🔧 Development Commands

```bash
# List all models
python manage.py inspectdb

# Create backup
python manage.py dumpdata > backup.json

# Restore backup
python manage.py loaddata backup.json

# Run tests
python manage.py test core

# Django shell (for debugging)
python manage.py shell

# Show SQL queries
python manage.py sqlmigrate core 0001

# Check deployment readiness
python manage.py check --deploy
```

---

## 📦 Add OpenAI Integration (Optional)

1. Get API key from https://openai.com/api/
2. Edit `projectsust/settings.py`:
```python
JARVIS_CONFIG = {
    'OPENAI_API_KEY': 'sk-your-key',
    'WAKE_WORD': 'jarvis',
}
```
3. Install: `pip install openai`
4. Restart server

---

## 🎨 Customize UI

Colors (in `static/css/style.css`):
```css
--primary-color: #00d4ff;        /* Cyan */
--secondary-color: #ff006e;      /* Pink */
--dark-bg: #0a0e27;              /* Dark blue */
```

---

## 🌐 Deploy to Web

### Using Gunicorn
```bash
pip install gunicorn
gunicorn projectsust.wsgi:application --bind 0.0.0.0:8000
```

### Using Docker
```bash
docker build -t jarvis .
docker run -p 8000:8000 jarvis
```

### Cloud Services
- **Heroku**: `heroku create && git push heroku main`
- **PythonAnywhere**: Upload files via web interface
- **Render**: Connect GitHub repo
- **Railway**: Push to deploy

---

## 📱 Browser Compatibility

| Browser | Web Speech | TTS | Status |
|---------|:----------:|:---:|:------:|
| Chrome | ✅ | ✅ | Best |
| Edge | ✅ | ✅ | Best |
| Firefox | ✅ | ✅ | Good |
| Safari | ✅ | ✅ | Good |

---

## 🔐 Security Checklist (Before Production)

- [ ] Change SECRET_KEY in settings.py
- [ ] Set DEBUG = False
- [ ] Update ALLOWED_HOSTS
- [ ] Use environment variables (.env file)
- [ ] Use HTTPS in production
- [ ] Set up proper database (PostgreSQL, MySQL)
- [ ] Configure rate limiting
- [ ] Set SECURE_SSL_REDIRECT = True
- [ ] Use stronger authentication

---

## 📊 Project Structure

```
projectsust/
├── Backend API          (Django)
├── Frontend UI          (HTML/CSS/JavaScript)
├── Database             (SQLite)
├── Static Files         (CSS, JS, images)
└── Documentation        (Guides, README)
```

---

## 🎯 Next Steps

1. ✅ Install and run
2. ✅ Test all commands
3. ✅ Browse conversation history
4. ✅ Try different voices
5. ✅ Add custom commands
6. ✅ Integrate OpenAI
7. ✅ Deploy online

---

## 💡 Tips & Tricks

- **Faster startup**: Use `--nothreading` flag
- **Debug mode**: Set DEBUG=True in settings
- **Offline testing**: Use fallback responses
- **Voice training**: Speak clearly near microphone
- **Auto-restart server**: Use `watchdog` package
- **API testing**: Use Postman or curl

---

## 🚀 Pro Features

Enable in settings:
- [ ] HTTPS redirect
- [ ] Gzip compression
- [ ] Static file CDN
- [ ] Database caching
- [ ] Custom authentication
- [ ] Rate limiting
- [ ] Analytics
- [ ] WebSockets

---

## 📞 Support

- **Docs**: Check README.md
- **Issues**: Read SETUP_GUIDE.md
- **Code**: See DEVELOPER_GUIDE.md
- **Errors**: Check browser console (F12)

---

## 🎉 You're All Set!

**Enjoy your Jarvis AI Voice Assistant!**

Questions? Check the documentation files included in the project.

---

**Last Updated**: March 2024
**Version**: 1.0
**Status**: Production Ready ✅

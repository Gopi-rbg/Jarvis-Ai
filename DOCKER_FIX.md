# Docker Deployment Fix - PyAudio Issue Resolved

## Problem
Docker build failed with: `fatal error: portaudio.h: No such file or directory`

This happened because PyAudio (used for desktop audio) requires system-level PortAudio libraries that aren't needed for web deployment.

## Solution Applied

### 1. Created `requirements-web.txt`
A new requirements file **without** desktop-only dependencies:
- ✅ Removed: `pyaudio`, `pyttsx3`, `vosk`
- ✅ Keeps: Django, REST Framework, Gemini AI, PostgreSQL driver
- ✅ File: `requirements-web.txt`

### 2. Updated `Dockerfile`
- Added `portaudio19-dev` to build dependencies (in case needed)
- Added `libportaudio2` to runtime dependencies
- Updated to use `requirements-web.txt` for web deployment
- Avoids PyAudio compilation errors

### 3. Fixed `settings_production.py`
- Fixed `MIDDLEWARE` reference issue
- Fixed `REST_FRAMEWORK` definition
- Fixed `TEMPLATES` caching safely

---

## What to Do Now

### Option 1: Docker Deployment (Using Fixed Dockerfile)

```bash
# Build Docker image
docker build -t jarvis-ai .

# Test locally
docker-compose up -d

# Verify it works
curl http://localhost:8000/

# Access web app
http://localhost:8000
```

### Option 2: Deploy to Render (Easiest)

1. Go to https://render.com
2. Click "New Web Service"
3. Connect your GitHub repository
4. Build command:
```
pip install -r requirements-web.txt && python manage.py migrate && python manage.py collectstatic --noinput
```
5. Start command:
```
gunicorn projectsust.wsgi
```
6. Set environment variables (same as before)
7. Deploy!

### Option 3: Deploy to Railway

```
1. Go to https://railway.app
2. Import project from GitHub
3. Add PostgreSQL plugin
4. Set environment variables
5. Auto-deploys (no build commands needed)
```

---

## Key Files Changed

| File | Change | Reason |
|------|--------|--------|
| **Dockerfile** | Uses requirements-web.txt | Avoid PyAudio build issues |
| **requirements-web.txt** | NEW - Web only deps | No desktop/audio packages |
| **settings_production.py** | Fixed references | Proper error handling |

---

## Verify Deployment

After deploying, test:

```bash
# Test health check
curl https://your-app.render.com/

# Test API
curl https://your-app.render.com/api/conversations/

# Test admin panel
https://your-app.render.com/admin
```

---

## Troubleshooting

### Still getting PyAudio error?
- Ensure `requirements-web.txt` is being used, not `requirements.txt`
- Check Dockerfile is using: `pip install -r requirements-web.txt`

### Render build fails?
- Go to Deployment Settings
- Update Build command to use `requirements-web.txt`
- Or just specify: `pip install -r requirements-web.txt`

### Docker build fails locally?
```bash
# Clean build
docker build --no-cache -t jarvis-ai .

# Check Dockerfile is updated
cat Dockerfile | grep requirements-web
```

---

## Summary

✅ **Fixed**: PyAudio build error  
✅ **Created**: requirements-web.txt (no audio deps)  
✅ **Updated**: Dockerfile to use web requirements  
✅ **Fixed**: settings_production.py references  
✅ **Ready**: Deploy to any platform  

Your Jarvis AI web app is now ready to deploy without audio dependency issues!

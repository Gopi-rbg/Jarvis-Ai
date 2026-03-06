# Jarvis AI - Web Deployment Guide

Complete guide to deploy Jarvis AI web dashboard to production servers.

## Table of Contents
1. [Deployment Platforms](#deployment-platforms)
2. [Pre-Deployment Checklist](#pre-deployment-checklist)
3. [Platform-Specific Guides](#platform-specific-guides)
4. [Post-Deployment Configuration](#post-deployment-configuration)
5. [Monitoring & Maintenance](#monitoring--maintenance)

---

## Deployment Platforms

### Quick Comparison

| Platform | Ease | Cost | Free Tier | Cold Start | Notes |
|----------|------|------|-----------|-----------|-------|
| **Heroku** | ⭐⭐⭐⭐⭐ | Paid | Removed | Medium | Easiest, no longer free |
| **Render** | ⭐⭐⭐⭐ | Free + Paid | Yes | Medium | Great free option |
| **Railway** | ⭐⭐⭐⭐ | Free + Paid | Yes | Fast | Modern, user-friendly |
| **PythonAnywhere** | ⭐⭐⭐⭐ | Free + Paid | Yes | N/A | Python-focused hosting |
| **AWS** | ⭐⭐⭐ | Variable | Free tier | Fast | More complex setup |
| **DigitalOcean** | ⭐⭐⭐ | $5+/mo | Droplet | Fast | VPS control, scalable |
| **Replit** | ⭐⭐⭐⭐⭐ | Free | Yes | Fast | Great for learning |
| **Google Cloud** | ⭐⭐ | Variable | Free tier | Fast | Enterprise-grade |

**Recommendation for Beginners**: **Render** or **Railway** (free tier with good uptime)

---

## Pre-Deployment Checklist

### 1. Environment Setup
```bash
# Ensure all required files exist
✓ requirements.txt        # All dependencies listed
✓ Procfile               # Process file (Heroku/Render)
✓ runtime.txt            # Python version specified
✓ manage.py              # Django management script
✓ projectsust/wsgi.py    # WSGI application
✓ .env.example           # Environment template
✓ .gitignore             # Git ignore rules
```

### 2. Update .gitignore
Ensure `.gitignore` includes:
```
.env
*.pyc
__pycache__/
db.sqlite3
staticfiles/
*.log
node_modules/
venv/
env/
.DS_Store
```

### 3. Create .env.production
```env
DEBUG=False
SECRET_KEY=your-very-secure-secret-key-change-this-in-production
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@localhost/dbname  # For PostgreSQL
GEMINI_API_KEY=your_api_key_here
```

### 4. Update settings.py for Production
See [Production Settings](#production-settings-modifications) section below.

### 5. Test Locally with Production Settings
```bash
DEBUG=False python manage.py runserver
```

### 6. Commit to Git
```bash
git add .
git commit -m "Prepare for production deployment"
git push origin main
```

---

## Platform-Specific Guides

### Option 1: Render (⭐ RECOMMENDED - Free)

**Advantages**:
- Free tier available
- Easy GitHub integration
- Auto-deploys on push
- PostgreSQL included
- SSL certificate automatic
- Good uptime and performance

**Steps**:

#### 1. Sign Up
- Go to https://render.com
- Sign up with GitHub account
- Grant repository access

#### 2. Create Web Service
- Click "New +" → "Web Service"
- Connect your GitHub repository
- Select the Jarvis-Ai repository
- Branch: `main`
- Deploy command: `gunicorn projectsust.wsgi`
- Build command: `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`

#### 3. Configure Environment Variables
In Render dashboard:
```
DEBUG=False
SECRET_KEY=generate-a-long-random-string-here
ALLOWED_HOSTS=*.render.com,yourdomain.com
DATABASE_URL=Use the PostgreSQL instance below
GEMINI_API_KEY=your_api_key
```

#### 4. Add PostgreSQL Database
- Click "New +" → "PostgreSQL"
- Create database
- Note the `DATABASE_URL` from the dashboard
- Add to Web Service environment

#### 5. Configure Static Files
Edit `projectsust/settings.py`:
```python
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Add this for production
if not DEBUG:
    STATIC_URL = 'https://cdn.example.com/static/'  # Or use Render's built-in
```

#### 6. Deploy
- Push code to GitHub
- Render automatically deploys
- Check build logs in dashboard
- Access your app at: `https://your-app.render.com`

#### 7. Post-Deployment
```bash
# In Render dashboard terminal (if available)
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

---

### Option 2: Railway (Free + Paid)

**Advantages**:
- Clean, modern interface
- Free $5 credit monthly
- Auto-deploys from GitHub
- PostgreSQL included
- Easy environment setup

**Steps**:

#### 1. Sign Up
- Go to https://railway.app
- Sign up with GitHub
- Grant access

#### 2. Create Project
- Click "New Project"
- Select "Deploy from GitHub repo"
- Choose Jarvis-Ai repository

#### 3. Configure Services
- Railway auto-detects Django
- Add PostgreSQL plugin
  - Click Add (+)
  - Select PostgreSQL
  - Railway creates `DATABASE_URL`

#### 4. Set Environment Variables
```
DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=*.railway.app,yourdomain.com
GEMINI_API_KEY=your_key
```

#### 5. Automatic Deployment
- Railway watches your GitHub repository
- Deploys on every push to main branch
- View logs in real-time

#### 6. Access Your App
- Railway assigns a domain: `yourappname.up.railway.app`
- Or connect custom domain

---

### Option 3: Heroku (Free Tier Removed - Look for Eco Plan)

**Note**: Heroku removed free tier as of November 2022. Eco plan starts at $5/month.

**Steps** (if using paid plan):

#### 1. Sign Up & Install CLI
```bash
# Sign up at https://www.heroku.com/
# Install Heroku CLI
# Then login
heroku login
```

#### 2. Create Heroku App
```bash
heroku create jarvis-ai-yourusername
```

#### 3. Add PostgreSQL Database
```bash
heroku addons:create heroku-postgresql:mini
```

#### 4. Set Environment Variables
```bash
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-secret-key
heroku config:set ALLOWED_HOSTS=jarvis-ai-yourusername.herokuapp.com
heroku config:set GEMINI_API_KEY=your_key
```

#### 5. Deploy
```bash
git push heroku main
```

#### 6. Run Migrations
```bash
heroku run python manage.py migrate
```

#### 7. Create Superuser
```bash
heroku run python manage.py createsuperuser
```

---

### Option 4: PythonAnywhere (Student-Friendly)

**Advantages**:
- Free tier available
- Python-focused
- No credit card required for free tier
- Good for learning

**Steps**:

#### 1. Sign Up
- Go to https://www.pythonanywhere.com/
- Create free account
- No credit card needed

#### 2. Upload Code
- Use "Upload a zip file" or Git integration
- Or clone from GitHub:
```bash
git clone https://github.com/yourusername/Jarvis-Ai.git
```

#### 3. Create Web App
- Click "Web" tab
- Create new web app
- Choose Python version
- Select "Django + manual configuration"

#### 4. Configure Application
Edit WSGI configuration file to point to `projectsust.wsgi`

#### 5. Install Requirements
In PythonAnywhere bash console:
```bash
pip install -r requirements.txt
```

#### 6. Configure Database
- Store database file in `/var/www/yourusername_pythonanywhere_com/mysite/`
- Or use MySQL through PythonAnywhere panel

#### 7. Create Superuser
```bash
python manage.py createsuperuser
```

#### 8. Access Your App
- Available at: `yourusername.pythonanywhere.com`

---

### Option 5: Docker + AWS/DigitalOcean/Google Cloud

**Advantages**:
- Complete control
- Scalable
- Production-ready

Create [Dockerfile](#dockerfile-example) and deploy.

---

## Production Settings Modifications

### Update settings.py

```python
import os
from decouple import config

# Production Settings
DEBUG = config('DEBUG', default=False, cast=bool)
SECRET_KEY = config('SECRET_KEY', default='your-fallback-secret-key')
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost', cast=lambda v: [s.strip() for s in v.split(',')])

# Database Configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Use PostgreSQL in production
if config('DATABASE_URL', default=None):
    import dj_database_url
    DATABASES['default'] = dj_database_url.config(conn_max_age=600)

# Security Settings for Production
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_SECURITY_POLICY = {
        "default-src": ("'self'",),
    }
    ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')])

# Static Files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

if not DEBUG:
    # Use WhiteNoise for serving static files
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# CORS Configuration
CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default='http://localhost:8000',
    cast=lambda v: [s.strip() for s in v.split(',')]
)

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/jarvis.log',
        },
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
    },
}

# Gemini API Configuration
GEMINI_API_KEY = config('GEMINI_API_KEY', default='')
```

### Update requirements.txt

Add production dependencies:
```
dj-database-url==1.3.0
whitenoise==6.6.0
psycopg2-binary==2.9.9
```

---

## Docker Deployment

### Dockerfile Example

Create `Dockerfile` in project root:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Create non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Run gunicorn
CMD ["gunicorn", "projectsust.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    command: gunicorn projectsust.wsgi:application --bind 0.0.0.0:8000
    environment:
      - DEBUG=False
      - SECRET_KEY=${SECRET_KEY}
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/jarvis
      - ALLOWED_HOSTS=localhost,127.0.0.1
    ports:
      - "8000:8000"
    depends_on:
      - db
    volumes:
      - ./staticfiles:/app/staticfiles

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=jarvis
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Build and Run Docker
```bash
docker-compose build
docker-compose up -d
```

---

## Post-Deployment Configuration

### 1. Run Migrations
```bash
# Render/Railway (if they provide terminal access)
python manage.py migrate

# Or through shell
python manage.py shell << EOF
from django.core.management import call_command
call_command('migrate')
EOF
```

### 2. Create Superuser
```bash
python manage.py createsuperuser
# Follow prompts to create admin account
```

### 3. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### 4. Configure Domain
- Update `ALLOWED_HOSTS` with your domain
- Configure DNS (CNAME or A record)
- Enable SSL/HTTPS in hosting provider

### 5. Set Environment Variables
In your hosting platform dashboard:
```
DEBUG=False
SECRET_KEY=generate-secure-key (at least 50 characters)
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
GEMINI_API_KEY=your_api_key_from_google_cloud
DATABASE_URL=postgresql://... (provided by platform)
```

### 6. Access Admin Panel
```
https://yourdomain.com/admin
# Login with superuser credentials
```

---

## Monitoring & Maintenance

### Application Health Checks

**Render/Railway** automatically monitor your app. Check:
- Deployment logs
- Runtime errors
- Response times
- Memory usage

### View Logs
```bash
# Render
render logs --service <service-id>

# Railway
railway logs

# Heroku
heroku logs --tail

# PythonAnywhere
Check in web app section
```

### Common Issues & Solutions

**Issue**: 502 Bad Gateway
```
Solution:
- Check deploy logs for errors
- Ensure migrations ran successfully
- Verify SECRET_KEY is set
- Check allowed hosts configuration
```

**Issue**: Static files not loading (404)
```
Solution:
- Run: python manage.py collectstatic --noinput
- Check STATIC_ROOT and STATIC_URL
- Use WhiteNoise middleware
- Check web server logs
```

**Issue**: Database connection error
```
Solution:
- Verify DATABASE_URL is correct
- Check database service is running
- Run migrations: python manage.py migrate
- Check credentials in settings
```

**Issue**: CSRF Token Mismatch
```
Solution:
- Check CSRF_TRUSTED_ORIGINS in settings
- Verify SESSION_COOKIE_SECURE = True
- Check DEBUG=False
```

### Auto-Deployment Setup

**GitHub Actions** (continuous deployment):

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Render
        run: |
          curl https://api.render.com/deploy/srv-${{ secrets.RENDER_SERVICE_ID }}?key=${{ secrets.RENDER_API_KEY }}
```

---

## Database Migration Strategy

### Using PostgreSQL

**Render** auto-creates PostgreSQL instances. To migrate from SQLite:

1. **Export SQLite Data**
```bash
python manage.py dumpdata > data.json
```

2. **Update settings to use PostgreSQL**
```python
DATABASES = {
    'default': dj_database_url.config()
}
```

3. **Apply migrations on PostgreSQL**
```bash
python manage.py migrate
```

4. **Load data**
```bash
python manage.py loaddata data.json
```

---

## Security Checklist

- [ ] DEBUG = False in production
- [ ] SECRET_KEY is secure and unique
- [ ] ALLOWED_HOSTS configured correctly
- [ ] SECURE_SSL_REDIRECT = True
- [ ] SESSION_COOKIE_SECURE = True
- [ ] CSRF_COOKIE_SECURE = True  
- [ ] GEMINI_API_KEY not in code (use environment variables)
- [ ] .env file not committed to GitHub
- [ ] Superuser password is strong
- [ ] Database credentials are secure
- [ ] Regular backups enabled
- [ ] CORS_ALLOWED_ORIGINS restricted
- [ ] Firewall rules configured
- [ ] HTTPS/SSL enabled

---

## Performance Optimization

### Static File Compression
```python
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### Database Connection Pooling
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'CONN_MAX_AGE': 600,  # Connection pooling
    }
}
```

### Caching
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}
```

### CDN for Static Files
```python
if not DEBUG:
    STATIC_URL = 'https://cdn.yourdomain.com/static/'
```

---

## Scaling

### Horizontal Scaling (Multiple Instances)
- Most platforms handle this automatically
- Just upgrade your plan
- Load balancer distributes traffic

### Vertical Scaling (More Resources)
- Upgrade instance type
- Increase memory/CPU
- Add more database connections

---

## Backup & Disaster Recovery

### Database Backups
```bash
# PostgreSQL backup
pg_dump DATABASE_URL > backup.sql

# Restore
psql DATABASE_URL < backup.sql
```

### Code Backups
- GitHub is your code backup
- Ensure regular commits

### Scheduled Backups
- Render: automatic daily backups
- Railway: database backups available
- PythonAnywhere: file backups available

---

## Cost Estimation

### Monthly Costs (Approximate)

| Platform | Free Tier | Paid Tier | Notes |
|----------|-----------|-----------|-------|
| Render | ~0.32$/day shared | $7+/month | Free can be slow |
| Railway | $5 credits | $7+/month | $5 credit refreshes monthly |
| Heroku | Removed | $7+/month | Eco plan starting price |
| PythonAnywhere | Free | $5+/month | Python-specific |
| AWS | Various | $5-50+/month | Pay-as-you-go |
| DigitalOcean | - | $5+/month | VPS starting price |

---

## Troubleshooting Deployment

### Deployment Fails
```
1. Check build logs for specific errors
2. Verify Python version in runtime.txt
3. Test locally: DEBUG=False python manage.py runserver
4. Ensure all required packages in requirements.txt
5. Check for syntax errors in settings.py
```

### App Crashes After Deploy
```
1. Check application logs
2. Verify environment variables set correctly
3. Run migrations: python manage.py migrate
4. Collect static files: python manage.py collectstatic --noinput
5. Check database connection
```

### Database Errors
```
1. Verify DATABASE_URL is correct
2. Check database service is running
3. Run migrations for new tables
4. Check user permissions
5. Review database logs
```

---

## Next Steps

1. **Choose Platform**: Render or Railway recommended
2. **Prepare Code**: Update settings.py, create Procfile
3. **Deploy**: Follow platform-specific guide
4. **Configure**: Set environment variables
5. **Test**: Access your domain, test all features
6. **Monitor**: Check logs and performance
7. **Scale**: Upgrade as needed

---

## Support & Resources

- **Render Docs**: https://render.com/docs
- **Railway Docs**: https://docs.railway.app/
- **Heroku Docs**: https://devcenter.heroku.com/
- **PythonAnywhere**: https://help.pythonanywhere.com/
- **Django Deployment**: https://docs.djangoproject.com/en/stable/howto/deployment/

---

**Version**: 1.0.0  
**Last Updated**: 2024  
**Status**: Production Ready

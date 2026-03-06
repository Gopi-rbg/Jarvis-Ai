"""
Production-specific Django settings for Jarvis AI

This file contains production-ready settings that should be
used when deploying to a public server.

To use these settings, update settings.py to include:

if not DEBUG:
    from .settings_production import *
"""

import os
from decouple import config

# ============================================
# SECURITY SETTINGS
# ============================================

DEBUG = False
SECRET_KEY = config('SECRET_KEY', default='django-insecure-development-key')
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', 
                      cast=lambda v: [s.strip() for s in v.split(',')])

# SSL/HTTPS Configuration
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True

# Security Headers
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_SECURITY_POLICY = {
    "default-src": ("'self'",),
    "script-src": ("'self'", "'unsafe-inline'", "cdn.jsdelivr.net"),
    "style-src": ("'self'", "'unsafe-inline'",),
    "img-src": ("'self'", "data:", "https:"),
    "font-src": ("'self'", "fonts.googleapis.com", "fonts.gstatic.com"),
    "connect-src": ("'self'", "https:"),
}

X_FRAME_OPTIONS = 'DENY'
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# ============================================
# DATABASE CONFIGURATION
# ============================================

# Use PostgreSQL in production (via DATABASE_URL from environment)
import dj_database_url

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db.sqlite3'),
    }
}

# Override with PostgreSQL if DATABASE_URL is set
if config('DATABASE_URL', default=None):
    DATABASES['default'] = dj_database_url.config(
        default=config('DATABASE_URL'),
        conn_max_age=600,  # Persistent connections
        conn_health_checks=True,  # Health checks
        ssl_require=True,  # Require SSL for remote connections
    )

# Connection pooling
if 'psycopg2' in DATABASES['default'].get('ENGINE', ''):
    DATABASES['default']['CONN_MAX_AGE'] = 600  # 10 minutes

# ============================================
# CACHING CONFIGURATION
# ============================================

# Use Redis for caching in production
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': config('REDIS_URL', default='redis://127.0.0.1:6379/1'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS': {'max_connections': 50},
            'SOCKET_CONNECT_TIMEOUT': 5,
            'SOCKET_TIMEOUT': 5,
            'COMPRESSOR': 'django_redis.compressors.zlib.ZlibCompressor',
            'IGNORE_EXCEPTIONS': True,
        },
        'KEY_PREFIX': 'jarvis',
        'TIMEOUT': 300,  # 5 minutes default
    }
}

# Session cache backend
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

# ============================================
# STATIC FILES CONFIGURATION
# ============================================

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static'),
]

# Use WhiteNoise for efficient static file serving
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# CDN Configuration (optional - uncomment if using CDN)
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
# AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
# STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'

# ============================================
# MEDIA FILES CONFIGURATION
# ============================================

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media')

# ============================================
# CORS CONFIGURATION
# ============================================

CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default='http://localhost:8000,http://localhost:3000',
    cast=lambda v: [s.strip() for s in v.split(',')]
)

CORS_ALLOW_CREDENTIALS = True
CORS_EXPOSE_HEADERS = ['Content-Type', 'X-CSRFToken']

# ============================================
# EMAIL CONFIGURATION
# ============================================

EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@jarvis-ai.com')

# Admins to receive error emails
ADMINS = [
    ('Admin', config('ADMIN_EMAIL', default='admin@jarvis-ai.com')),
]

MANAGERS = ADMINS

# ============================================
# LOGGING CONFIGURATION
# ============================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs', 'django.log'),
            'maxBytes': 1024 * 1024 * 10,  # 10MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'performance_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs', 'performance.log'),
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'security_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs', 'security.log'),
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file', 'mail_admins'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['security_file'],
            'level': 'WARNING',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['performance_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'jarvis': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# Ensure logs directory exists
LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
os.makedirs(LOGS_DIR, exist_ok=True)

# ============================================
# ERROR HANDLING
# ============================================

# Sentry error tracking (optional)
if config('SENTRY_DSN', default=None):
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=config('SENTRY_DSN'),
        integrations=[DjangoIntegration()],
        traces_sample_rate=0.1,
        send_default_pii=False,
        environment=config('ENVIRONMENT', default='production'),
    )

# ============================================
# PRODUCTION MIDDLWARE
# ============================================

MIDDLEWARE_PRODUCTION = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.gzip.GZipMiddleware',  # Compress responses
]

# Override MIDDLEWARE in settings.py
# MIDDLEWARE = MIDDLEWARE_PRODUCTION

# ============================================
# EXTERNAL SERVICES
# ============================================

# Gemini API Configuration
GEMINI_API_KEY = config('GEMINI_API_KEY', default='')

# ============================================
# PERFORMANCE & OPTIMIZATION
# ============================================

# Query optimization
DATABASE_QUERY_TIMEOUT = 30  # seconds

# Cache templates
TEMPLATES[0]['OPTIONS']['loaders'] = [
    ('django.template.loaders.cached.Loader', [
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    ]),
]

# ============================================
# CELERY CONFIGURATION (Optional)
# ============================================

CELERY_BROKER_URL = config('REDIS_URL', default='redis://127.0.0.1:6379/0')
CELERY_RESULT_BACKEND = config('REDIS_URL', default='redis://127.0.0.1:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60  # 30 minutes

# ============================================
# RATE LIMITING (Optional)
# ============================================

REST_FRAMEWORK['DEFAULT_THROTTLE_CLASSES'] = [
    'rest_framework.throttling.AnonRateThrottle',
    'rest_framework.throttling.UserRateThrottle',
]

REST_FRAMEWORK['DEFAULT_THROTTLE_RATES'] = {
    'anon': '100/hour',
    'user': '1000/hour',
}

print("✓ Production settings loaded")

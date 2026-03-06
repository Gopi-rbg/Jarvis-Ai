# Multi-stage build for optimized Docker image
FROM python:3.10-slim as builder

WORKDIR /app

# Install build dependencies (including portaudio for PyAudio)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    postgresql-client \
    portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
# For web deployment, use requirements-web.txt (excludes desktop/audio dependencies)
# This avoids building PyAudio with portaudio headers
COPY requirements-web.txt requirements.txt ./
RUN pip install --no-cache-dir -r requirements-web.txt

# Final stage
FROM python:3.10-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    curl \
    libportaudio2 \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from builder (entire Python environment)
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy project files
COPY . .

# Create non-root user for security (but run admin tasks as root first)
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Create required directories
RUN mkdir -p /app/staticfiles /app/media /app/logs && \
    chown -R appuser:appuser /app/staticfiles /app/media /app/logs

# Collect static files (must be done as root before switching user)
RUN python manage.py collectstatic --noinput --clear

# Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Expose port
EXPOSE 8000

# Run gunicorn
CMD ["gunicorn", "projectsust.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "4", \
     "--worker-class", "sync", \
     "--worker-connections", "1000", \
     "--max-requests", "1000", \
     "--max-requests-jitter", "50", \
     "--timeout", "120", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]

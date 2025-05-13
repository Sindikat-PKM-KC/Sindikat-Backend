#!/bin/sh

# Apply DB migrations
python manage.py migrate --no-input

# Collect static files
python manage.py collectstatic --no-input

# Start Gunicorn in background
gunicorn core.wsgi:application \
    --bind 127.0.0.1:8000 \
    --workers 3 \
    --log-level info &

# Start Nginx in foreground
nginx -g "daemon off;"

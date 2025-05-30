#!/usr/bin/env bash
# Exit the script on any error
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Collect static files (like CSS, JS)
python manage.py collectstatic --noinput

# Apply database migrations
python manage.py migrate

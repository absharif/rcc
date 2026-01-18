#!/bin/bash
# Test Gunicorn script - Run this to diagnose Gunicorn issues

echo "=== Testing Gunicorn Configuration ==="
echo ""

# Change to project directory
cd /home/amtun/rcc/rcc || exit 1

# Activate virtual environment
source ../venv/bin/activate || exit 1

echo "1. Checking Python version..."
python --version
echo ""

echo "2. Checking Django installation..."
python -c "import django; print(f'Django {django.get_version()}')"
echo ""

echo "3. Checking Django configuration..."
python manage.py check --deploy
echo ""

echo "4. Checking database connection..."
python manage.py dbshell -c "\conninfo"
echo ""

echo "5. Testing Django runserver (will start on port 8000)..."
echo "   Press Ctrl+C after 5 seconds to stop..."
timeout 5 python manage.py runserver 0.0.0.0:8000 || echo "Runserver test completed"
echo ""

echo "6. Testing Gunicorn directly..."
echo "   This will show any import or configuration errors"
echo "   Press Ctrl+C to stop..."
gunicorn --bind 0.0.0.0:8001 --log-level debug city_corporation.wsgi:application

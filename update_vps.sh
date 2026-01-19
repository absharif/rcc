#!/bin/bash

# VPS Update Script
# This script updates the Django application on VPS

set -e  # Exit on error

# Configuration - UPDATE THESE PATHS
PROJECT_DIR="/path/to/your/project"  # Update this
VENV_PATH="$PROJECT_DIR/venv"  # Update if different
GIT_BRANCH="main"  # Update if different branch

echo "=========================================="
echo "Starting VPS Update Process"
echo "=========================================="

# Step 1: Navigate to project directory
cd "$PROJECT_DIR" || exit 1
echo "✓ Changed to project directory: $PROJECT_DIR"

# Step 2: Activate virtual environment
if [ -f "$VENV_PATH/bin/activate" ]; then
    source "$VENV_PATH/bin/activate"
    echo "✓ Virtual environment activated"
else
    echo "✗ Virtual environment not found at $VENV_PATH"
    exit 1
fi

# Step 3: Pull latest code
echo "Pulling latest code from git..."
git pull origin "$GIT_BRANCH" || {
    echo "✗ Git pull failed"
    exit 1
}
echo "✓ Code updated from git"

# Step 4: Install/update dependencies
echo "Installing/updating dependencies..."
pip install -r requirements.txt --quiet || {
    echo "✗ Failed to install dependencies"
    exit 1
}
echo "✓ Dependencies updated"

# Step 5: Run migrations
echo "Running database migrations..."
python manage.py migrate --noinput || {
    echo "✗ Migration failed"
    exit 1
}
echo "✓ Migrations completed"

# Step 6: Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput || {
    echo "✗ Failed to collect static files"
    exit 1
}
echo "✓ Static files collected"

# Step 7: Clear Python cache
echo "Clearing Python cache..."
find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
echo "✓ Cache cleared"

# Step 8: Restart Gunicorn
echo "Restarting Gunicorn service..."
if systemctl is-active --quiet gunicorn; then
    sudo systemctl restart gunicorn || {
        echo "✗ Failed to restart Gunicorn"
        exit 1
    }
    echo "✓ Gunicorn restarted"
else
    echo "⚠ Gunicorn service not found or not running"
fi

# Step 9: Restart Nginx (if using)
echo "Reloading Nginx..."
if systemctl is-active --quiet nginx; then
    sudo systemctl reload nginx || {
        echo "⚠ Nginx reload failed (may not be critical)"
    }
    echo "✓ Nginx reloaded"
else
    echo "⚠ Nginx not running or not installed"
fi

# Step 10: Check service status
echo ""
echo "=========================================="
echo "Service Status Check"
echo "=========================================="
if systemctl is-active --quiet gunicorn; then
    echo "✓ Gunicorn: Running"
    systemctl status gunicorn --no-pager -l | head -5
else
    echo "✗ Gunicorn: Not running"
fi

echo ""
echo "=========================================="
echo "Update Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Clear your browser cache (Ctrl+Shift+R or Cmd+Shift+R)"
echo "2. Check the website to verify updates"
echo "3. Check logs if issues: sudo journalctl -u gunicorn -f"
echo ""

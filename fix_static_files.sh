#!/bin/bash

# Script to fix Django admin CSS not loading on VPS

echo "=========================================="
echo "Fixing Django Admin Static Files"
echo "=========================================="

# Get project directory (update this path)
PROJECT_DIR="/path/to/your/project"  # UPDATE THIS
cd "$PROJECT_DIR" || exit 1

# Activate virtual environment
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    echo "✓ Virtual environment activated"
else
    echo "✗ Virtual environment not found"
    exit 1
fi

# Step 1: Collect static files
echo ""
echo "Step 1: Collecting static files..."
python manage.py collectstatic --noinput --clear
if [ $? -eq 0 ]; then
    echo "✓ Static files collected successfully"
else
    echo "✗ Failed to collect static files"
    exit 1
fi

# Step 2: Check if admin CSS exists
echo ""
echo "Step 2: Verifying Django admin CSS..."
if [ -f "staticfiles/admin/css/base.css" ]; then
    echo "✓ Django admin CSS found at: staticfiles/admin/css/base.css"
    echo "  File size: $(du -h staticfiles/admin/css/base.css | cut -f1)"
else
    echo "✗ Django admin CSS not found!"
    echo "  This might indicate a problem with collectstatic"
fi

# Step 3: Fix permissions
echo ""
echo "Step 3: Fixing file permissions..."
chmod -R 755 staticfiles/
if [ $? -eq 0 ]; then
    echo "✓ Permissions set to 755"
else
    echo "⚠ Could not set permissions (may need sudo)"
fi

# Step 4: Check Nginx configuration
echo ""
echo "Step 4: Checking Nginx configuration..."
NGINX_CONFIG="/etc/nginx/sites-available/default"
if [ -f "$NGINX_CONFIG" ]; then
    if grep -q "location /static/" "$NGINX_CONFIG"; then
        echo "✓ Nginx static files configuration found"
        echo ""
        echo "Current static files configuration:"
        grep -A 3 "location /static/" "$NGINX_CONFIG" | head -5
    else
        echo "✗ Nginx static files configuration NOT found!"
        echo ""
        echo "Add this to your Nginx config ($NGINX_CONFIG):"
        echo ""
        echo "    location /static/ {"
        echo "        alias $PROJECT_DIR/staticfiles/;"
        echo "        expires 30d;"
        echo "        add_header Cache-Control \"public, immutable\";"
        echo "    }"
    fi
else
    echo "⚠ Nginx config file not found at $NGINX_CONFIG"
fi

# Step 5: Summary
echo ""
echo "=========================================="
echo "Summary"
echo "=========================================="
echo "Static files directory: $PROJECT_DIR/staticfiles"
echo "Total static files: $(find staticfiles -type f 2>/dev/null | wc -l)"
echo ""
echo "Next steps:"
echo "1. If Nginx config was missing, add it and reload:"
echo "   sudo systemctl reload nginx"
echo ""
echo "2. Test in browser:"
echo "   http://your-domain.com/static/admin/css/base.css"
echo ""
echo "3. If still not working, check Nginx error logs:"
echo "   sudo tail -f /var/log/nginx/error.log"
echo ""

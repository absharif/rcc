# Fix Django Admin CSS Not Loading on VPS

If Django admin CSS is not loading on your VPS, follow these steps:

## Quick Fix Steps

### 1. Collect Static Files
```bash
cd /path/to/your/project
source venv/bin/activate
python manage.py collectstatic --noinput
```

### 2. Check STATIC_ROOT Configuration
Verify in `settings.py`:
```python
STATIC_ROOT = BASE_DIR / 'staticfiles'  # or your static files directory
STATIC_URL = '/static/'
```

### 3. Configure Nginx to Serve Static Files

Add this to your Nginx configuration file (usually `/etc/nginx/sites-available/your-site`):

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Static files location
    location /static/ {
        alias /path/to/your/project/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Media files location (if needed)
    location /media/ {
        alias /path/to/your/project/media/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Proxy to Gunicorn
    location / {
        proxy_pass http://127.0.0.1:8000;  # or your Gunicorn socket
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 4. Test and Reload Nginx
```bash
# Test configuration
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx
```

### 5. Check File Permissions
```bash
# Make sure static files are readable
chmod -R 755 /path/to/your/project/staticfiles/
chown -R www-data:www-data /path/to/your/project/staticfiles/  # or your nginx user
```

### 6. Verify Static Files Were Collected
```bash
# Check if admin CSS exists
ls -la staticfiles/admin/css/
# Should see files like base.css, dashboard.css, etc.
```

## Alternative: Serve Static Files with Django (Development Only)

If you're in development and DEBUG=True, Django can serve static files. Add to `urls.py`:

```python
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.STIC_URL, document_root=settings.STATIC_ROOT)
```

**Note:** This is NOT recommended for production. Always use Nginx or another web server.

## Troubleshooting

### Check if static files directory exists:
```bash
ls -la staticfiles/
```

### Check STATIC_ROOT path:
```python
# In Django shell
python manage.py shell
>>> from django.conf import settings
>>> print(settings.STATIC_ROOT)
```

### Check if files are actually collected:
```bash
find staticfiles/ -name "*.css" | head -10
```

### Check Nginx error logs:
```bash
sudo tail -f /var/log/nginx/error.log
```

### Check file permissions:
```bash
ls -la staticfiles/admin/css/
# Files should be readable (644 or 755)
```

### Verify STATIC_URL matches:
- In browser, check Network tab
- CSS requests should go to `/static/admin/css/base.css`
- If 404, check Nginx configuration

## Common Issues

### Issue 1: STATIC_ROOT not set
**Solution:** Add to `settings.py`:
```python
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

### Issue 2: collectstatic not run
**Solution:** Run `python manage.py collectstatic --noinput`

### Issue 3: Nginx not configured
**Solution:** Add static files location block to Nginx config

### Issue 4: Wrong path in Nginx
**Solution:** Verify the `alias` path matches your `STATIC_ROOT`

### Issue 5: Permission denied
**Solution:** 
```bash
chmod -R 755 staticfiles/
chown -R www-data:www-data staticfiles/  # or nginx user
```

### Issue 6: DEBUG=False but no web server serving static files
**Solution:** Configure Nginx or Apache to serve static files

## Complete Nginx Configuration Example

```nginx
upstream gunicorn {
    server unix:/path/to/your/project/gunicorn.sock;  # or 127.0.0.1:8000
}

server {
    listen 80;
    server_name your-domain.com;

    client_max_body_size 100M;

    # Static files
    location /static/ {
        alias /path/to/your/project/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Media files
    location /media/ {
        alias /path/to/your/project/media/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Django application
    location / {
        proxy_pass http://gunicorn;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

## Quick Test Script

Create `test_static_files.sh`:

```bash
#!/bin/bash
echo "Checking static files configuration..."

# Check if STATIC_ROOT exists
if [ -d "staticfiles" ]; then
    echo "✓ staticfiles directory exists"
    echo "  Files count: $(find staticfiles -type f | wc -l)"
else
    echo "✗ staticfiles directory not found"
    echo "  Run: python manage.py collectstatic"
fi

# Check admin CSS
if [ -f "staticfiles/admin/css/base.css" ]; then
    echo "✓ Django admin CSS found"
else
    echo "✗ Django admin CSS not found"
fi

# Check permissions
if [ -r "staticfiles/admin/css/base.css" ]; then
    echo "✓ Static files are readable"
else
    echo "✗ Static files not readable"
    echo "  Run: chmod -R 755 staticfiles/"
fi

# Check Nginx config
if [ -f "/etc/nginx/sites-available/default" ]; then
    if grep -q "location /static/" /etc/nginx/sites-available/default; then
        echo "✓ Nginx static files configuration found"
    else
        echo "✗ Nginx static files configuration not found"
    fi
fi
```

Run it:
```bash
chmod +x test_static_files.sh
./test_static_files.sh
```

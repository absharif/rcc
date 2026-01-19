# VPS Update Checklist

When you push code updates to VPS, follow these steps to ensure changes are reflected:

## 1. Pull Latest Code
```bash
cd /path/to/your/project
git pull origin main  # or your branch name
```

## 2. Activate Virtual Environment
```bash
source venv/bin/activate  # or your venv path
```

## 3. Install/Update Dependencies (if requirements.txt changed)
```bash
pip install -r requirements.txt
```

## 4. Run Migrations (if models changed)
```bash
python manage.py migrate
```

## 5. Collect Static Files (IMPORTANT for CSS/JS/images)
```bash
python manage.py collectstatic --noinput
```

## 6. Restart Gunicorn Service
```bash
# If using systemd
sudo systemctl restart gunicorn
# or
sudo systemctl restart gunicorn.service

# Check status
sudo systemctl status gunicorn
```

## 7. Restart Nginx (if using)
```bash
sudo systemctl restart nginx
sudo systemctl status nginx
```

## 8. Clear Browser Cache
- Hard refresh: `Ctrl+Shift+R` (Linux/Windows) or `Cmd+Shift+R` (Mac)
- Or clear browser cache manually

## 9. Verify Files Are Updated
```bash
# Check if template file exists and has recent timestamp
ls -la templates/home.html
cat templates/home.html | head -20

# Check if static files are collected
ls -la staticfiles/
```

## Quick Update Script

Create a file `update_vps.sh`:

```bash
#!/bin/bash
cd /path/to/your/project
source venv/bin/activate
git pull origin main
pip install -r requirements.txt --quiet
python manage.py migrate --noinput
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn
sudo systemctl restart nginx
echo "Update complete!"
```

Make it executable:
```bash
chmod +x update_vps.sh
```

Then run:
```bash
./update_vps.sh
```

## Troubleshooting

### Home page still shows old content:
1. **Check if file was actually updated on VPS:**
   ```bash
   git log -1 templates/home.html
   cat templates/home.html | grep "City Corporation"
   ```

2. **Check Gunicorn is running latest code:**
   ```bash
   sudo systemctl status gunicorn
   # Check the process start time - should be recent
   ps aux | grep gunicorn
   ```

3. **Check Nginx is serving correct files:**
   ```bash
   sudo nginx -t  # Test configuration
   sudo systemctl reload nginx
   ```

4. **Check static files:**
   ```bash
   # Verify static files are collected
   ls -la staticfiles/css/
   # Check if STATIC_ROOT is correct in settings.py
   ```

5. **Clear Python cache:**
   ```bash
   find . -type d -name __pycache__ -exec rm -r {} +
   find . -type f -name "*.pyc" -delete
   ```

6. **Check file permissions:**
   ```bash
   ls -la templates/home.html
   # Should be readable by gunicorn user
   ```

### Template not found error:
- Check `TEMPLATES` setting in `settings.py`
- Verify template path is correct
- Check file permissions

### Static files not loading:
- Run `python manage.py collectstatic --noinput`
- Check `STATIC_ROOT` and `STATIC_URL` in settings
- Verify Nginx is configured to serve static files
- Check file permissions on staticfiles directory

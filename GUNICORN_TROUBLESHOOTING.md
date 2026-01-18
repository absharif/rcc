# Gunicorn Troubleshooting Guide

## Connection Reset Error Fix

If you're getting `curl: (56) Recv failure: Connection reset by peer`:

### Immediate Steps:

1. **Check if Gunicorn is actually running:**
   ```bash
   ps aux | grep gunicorn
   sudo systemctl status rcc_gunicorn.service
   ```

2. **If not running, check the error:**
   ```bash
   sudo journalctl -u rcc_gunicorn.service -n 50 --no-pager
   ```

3. **Remove old socket and restart:**
   ```bash
   sudo systemctl stop rcc_gunicorn.service rcc_gunicorn.socket
   sudo rm -f /run/rcc_gunicorn.sock
   sudo systemctl daemon-reload
   sudo systemctl start rcc_gunicorn.socket
   sudo systemctl start rcc_gunicorn.service
   ```

4. **Test manually to see the real error:**
   ```bash
   cd /home/amtun/rcc/rcc
   source ../venv/bin/activate
   gunicorn --bind 0.0.0.0:8000 --log-level debug city_corporation.wsgi:application
   ```

## Quick Diagnosis Steps

### 1. Check Detailed Gunicorn Logs

```bash
# Check journal logs for more details
sudo journalctl -u rcc_gunicorn.service -n 100 --no-pager

# Or check with more context
sudo journalctl -u rcc_gunicorn.service -f
```

### 2. Test Gunicorn Manually

This will show you the actual error:

```bash
cd /home/amtun/rcc/rcc
source ../venv/bin/activate

# Test Gunicorn directly
gunicorn --bind 0.0.0.0:8000 city_corporation.wsgi:application

# Or with more verbose output
gunicorn --bind 0.0.0.0:8000 --log-level debug city_corporation.wsgi:application
```

### 3. Check Django Settings

```bash
cd /home/amtun/rcc/rcc
source ../venv/bin/activate

# Test Django configuration
python manage.py check --deploy

# Test database connection
python manage.py dbshell

# Test if Django can start
python manage.py runserver 0.0.0.0:8000
```

## Common Issues and Fixes

### Issue 1: Missing Environment Variables

**Symptoms:** Import errors, SECRET_KEY not found

**Fix:**
```bash
# Make sure .env file exists and is readable
ls -la /home/amtun/rcc/rcc/.env
cat /home/amtun/rcc/rcc/.env

# Check if systemd service loads .env
# The service file should have EnvironmentFile=/home/amtun/rcc/rcc/.env
```

### Issue 2: Database Connection Error

**Symptoms:** Database connection refused or authentication failed

**Fix:**
```bash
# Test database connection
python manage.py dbshell

# Check .env database settings
grep DB_ /home/amtun/rcc/rcc/.env
```

### Issue 3: Import Errors

**Symptoms:** ModuleNotFoundError, ImportError

**Fix:**
```bash
# Check if all dependencies are installed
pip list | grep -E "Django|psycopg2|decouple"

# Reinstall if needed
pip install -r requirements.txt
```

### Issue 4: Path Issues

**Symptoms:** FileNotFoundError, wrong working directory

**Fix:**
- Ensure systemd service has correct WorkingDirectory
- Check all paths in service file are absolute

### Issue 5: Permission Issues

**Symptoms:** Permission denied errors

**Fix:**
```bash
# Check file permissions
ls -la /home/amtun/rcc/rcc/

# Fix permissions if needed
chmod +x /home/amtun/rcc/rcc/manage.py
chmod -R 755 /home/amtun/rcc/rcc/
```

## Systemd Service File Template

Create/update `/etc/systemd/system/rcc_gunicorn.service`:

```ini
[Unit]
Description=gunicorn daemon for City Corporation
After=network.target

[Service]
User=amtun
Group=www-data
WorkingDirectory=/home/amtun/rcc/rcc
Environment="PATH=/home/amtun/rcc/venv/bin"
EnvironmentFile=/home/amtun/rcc/rcc/.env
ExecStart=/home/amtun/rcc/venv/bin/gunicorn \
    --access-logfile - \
    --workers 3 \
    --bind unix:/run/rcc_gunicorn.sock \
    city_corporation.wsgi:application

[Install]
WantedBy=multi-user.target
```

## Socket Configuration

Create/update `/etc/systemd/system/rcc_gunicorn.socket`:

```ini
[Unit]
Description=rcc_gunicorn socket

[Socket]
ListenStream=/run/rcc_gunicorn.sock

[Install]
WantedBy=sockets.target
```

## Step-by-Step Fix

### Step 1: Stop Services

```bash
sudo systemctl stop rcc_gunicorn.service
sudo systemctl stop rcc_gunicorn.socket
```

### Step 2: Test Django Manually

```bash
cd /home/amtun/rcc/rcc
source ../venv/bin/activate

# Check Django
python manage.py check

# Test runserver
python manage.py runserver 0.0.0.0:8000
# If this works, Django is fine. Press Ctrl+C to stop.
```

### Step 3: Test Gunicorn Manually

```bash
cd /home/amtun/rcc/rcc
source ../venv/bin/activate

# Test Gunicorn (this will show the actual error)
gunicorn --bind 0.0.0.0:8000 city_corporation.wsgi:application
```

### Step 4: Check Logs

```bash
# Check what error Gunicorn is showing
sudo journalctl -u rcc_gunicorn.service -n 50 --no-pager | tail -20
```

### Step 5: Verify Service File

```bash
# Check service file
sudo cat /etc/systemd/system/rcc_gunicorn.service

# Check socket file
sudo cat /etc/systemd/system/rcc_gunicorn.socket
```

### Step 6: Reload and Restart

```bash
# Reload systemd
sudo systemctl daemon-reload

# Start socket
sudo systemctl start rcc_gunicorn.socket

# Start service
sudo systemctl start rcc_gunicorn.service

# Check status
sudo systemctl status rcc_gunicorn.service
```

## Debugging Commands

```bash
# Check if socket exists
ls -la /run/rcc_gunicorn.sock

# Test socket connection
curl --unix-socket /run/rcc_gunicorn.sock http://localhost/

# Check process
ps aux | grep gunicorn

# Check ports
sudo netstat -tlnp | grep gunicorn
```

## Common Error Messages

### "ModuleNotFoundError: No module named 'city_corporation'"
- Check WorkingDirectory in service file
- Verify you're in the correct directory (should be parent of city_corporation)

### "SECRET_KEY not found"
- Check .env file exists and has SECRET_KEY
- Verify EnvironmentFile path in service file

### "Database connection failed"
- Check database credentials in .env
- Verify PostgreSQL is running: `sudo systemctl status postgresql`
- Test connection: `python manage.py dbshell`

### "Permission denied"
- Check file permissions
- Verify user in service file matches file owner
- Check socket permissions

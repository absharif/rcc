#!/bin/bash
# Gunicorn Diagnostic Script
# Run this on your VPS to diagnose the issue

echo "=========================================="
echo "Gunicorn Diagnostic Script"
echo "=========================================="
echo ""

echo "1. Checking if Gunicorn process is running..."
ps aux | grep gunicorn | grep -v grep
if [ $? -ne 0 ]; then
    echo "   ❌ Gunicorn is NOT running"
else
    echo "   ✅ Gunicorn process found"
fi
echo ""

echo "2. Checking socket file..."
if [ -S /run/rcc_gunicorn.sock ]; then
    echo "   ✅ Socket file exists"
    ls -la /run/rcc_gunicorn.sock
else
    echo "   ❌ Socket file does NOT exist"
fi
echo ""

echo "3. Checking socket permissions..."
if [ -S /run/rcc_gunicorn.sock ]; then
    SOCKET_OWNER=$(stat -c '%U:%G' /run/runicorn.sock 2>/dev/null || stat -c '%U:%G' /run/rcc_gunicorn.sock)
    echo "   Socket owner: $SOCKET_OWNER"
    echo "   Current user: $(whoami)"
fi
echo ""

echo "4. Checking systemd service status..."
sudo systemctl status rcc_gunicorn.service --no-pager -l | head -20
echo ""

echo "5. Checking recent service logs..."
echo "   Last 30 lines of service logs:"
sudo journalctl -u rcc_gunicorn.service -n 30 --no-pager | tail -30
echo ""

echo "6. Checking if .env file exists..."
if [ -f /home/amtun/rcc/rcc/.env ]; then
    echo "   ✅ .env file exists"
    echo "   Checking key variables..."
    grep -E "SECRET_KEY|DEBUG|DB_" /home/amtun/rcc/rcc/.env | head -5
else
    echo "   ❌ .env file NOT found!"
fi
echo ""

echo "7. Testing Django configuration..."
cd /home/amtun/rcc/rcc
if [ -f manage.py ]; then
    source ../venv/bin/activate
    echo "   Running Django check..."
    python manage.py check 2>&1 | head -10
else
    echo "   ❌ manage.py not found in /home/amtun/rcc/rcc"
fi
echo ""

echo "8. Checking systemd service file..."
if [ -f /etc/systemd/system/rcc_gunicorn.service ]; then
    echo "   Service file exists. Key settings:"
    grep -E "WorkingDirectory|ExecStart|EnvironmentFile|User" /etc/systemd/system/rcc_gunicorn.service
else
    echo "   ❌ Service file not found!"
fi
echo ""

echo "=========================================="
echo "Recommended Actions:"
echo "=========================================="
echo ""
echo "If Gunicorn is not running:"
echo "  1. Stop services: sudo systemctl stop rcc_gunicorn.service rcc_gunicorn.socket"
echo "  2. Test manually: cd /home/amtun/rcc/rcc && source ../venv/bin/activate"
echo "  3. Run: gunicorn --bind 0.0.0.0:8000 --log-level debug city_corporation.wsgi:application"
echo ""
echo "If socket exists but connection fails:"
echo "  1. Remove old socket: sudo rm /run/rcc_gunicorn.sock"
echo "  2. Restart socket: sudo systemctl restart rcc_gunicorn.socket"
echo "  3. Start service: sudo systemctl start rcc_gunicorn.service"
echo ""

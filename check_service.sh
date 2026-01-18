#!/bin/bash
# Check Gunicorn Service Status

echo "=========================================="
echo "Gunicorn Service Status Check"
echo "=========================================="
echo ""

echo "1. Socket Status:"
sudo systemctl status rcc_gunicorn.socket --no-pager | head -10
echo ""

echo "2. Service Status:"
sudo systemctl status rcc_gunicorn.service --no-pager -l | head -30
echo ""

echo "3. Recent Service Logs (last 50 lines):"
sudo journalctl -u rcc_gunicorn.service -n 50 --no-pager | tail -50
echo ""

echo "4. Checking if socket file exists:"
if [ -S /run/rcc_gunicorn.sock ]; then
    echo "   ✅ Socket exists"
    ls -la /run/rcc_gunicorn.sock
else
    echo "   ❌ Socket does NOT exist"
fi
echo ""

echo "5. Testing socket connection:"
curl -v --unix-socket /run/rcc_gunicorn.sock http://localhost/ 2>&1 | head -20
echo ""

echo "6. Checking Gunicorn processes:"
ps aux | grep gunicorn | grep -v grep
if [ $? -ne 0 ]; then
    echo "   ❌ No Gunicorn processes running"
else
    echo "   ✅ Gunicorn processes found"
fi
echo ""

echo "=========================================="
echo "Next Steps:"
echo "=========================================="
echo ""
echo "If service is failing, check the logs above for errors."
echo "Common fixes:"
echo "  1. Check .env file: ls -la /home/amtun/rcc/rcc/.env"
echo "  2. Test Django: cd /home/amtun/rcc/rcc && source ../venv/bin/activate && python manage.py check"
echo "  3. Test Gunicorn manually: gunicorn --bind 0.0.0.0:8000 city_corporation.wsgi:application"
echo ""

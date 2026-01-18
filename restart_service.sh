#!/bin/bash
# Restart Gunicorn Service Properly

echo "Restarting Gunicorn Service..."
echo ""

# Stop service first
echo "1. Stopping service..."
sudo systemctl stop rcc_gunicorn.service

# Wait a moment
sleep 2

# Restart socket (this will trigger service)
echo "2. Restarting socket..."
sudo systemctl restart rcc_gunicorn.socket

# Wait a moment
sleep 2

# Start service explicitly
echo "3. Starting service..."
sudo systemctl start rcc_gunicorn.service

# Wait a moment
sleep 3

# Check status
echo "4. Checking status..."
echo ""
sudo systemctl status rcc_gunicorn.service --no-pager -l | head -40

echo ""
echo "If still failing, check logs:"
echo "sudo journalctl -u rcc_gunicorn.service -n 100 --no-pager | tail -50"

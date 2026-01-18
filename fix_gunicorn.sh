#!/bin/bash
# Quick Fix Script for Gunicorn Issues

echo "Fixing Gunicorn service..."

# Stop services
echo "1. Stopping services..."
sudo systemctl stop rcc_gunicorn.service
sudo systemctl stop rcc_gunicorn.socket

# Remove old socket if exists
echo "2. Cleaning up old socket..."
sudo rm -f /run/rcc_gunicorn.sock

# Reload systemd
echo "3. Reloading systemd..."
sudo systemctl daemon-reload

# Start socket
echo "4. Starting socket..."
sudo systemctl start rcc_gunicorn.socket

# Wait a moment
sleep 2

# Start service
echo "5. Starting service..."
sudo systemctl start rcc_gunicorn.service

# Wait a moment
sleep 2

# Check status
echo "6. Checking status..."
sudo systemctl status rcc_gunicorn.service --no-pager -l | head -30

echo ""
echo "If still failing, check logs:"
echo "sudo journalctl -u rcc_gunicorn.service -n 50 --no-pager"

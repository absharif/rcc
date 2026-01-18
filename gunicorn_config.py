# Gunicorn configuration file
# Usage: gunicorn -c gunicorn_config.py city_corporation.wsgi:application

import multiprocessing
import os

# Server socket
bind = "unix:/run/rcc_gunicorn.sock"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Logging
accesslog = "-"  # Log to stdout
errorlog = "-"   # Log to stderr
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = "rcc_gunicorn"

# Server mechanics
daemon = False
pidfile = "/run/rcc_gunicorn.pid"
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL (if needed)
# keyfile = None
# certfile = None

# Preload app
preload_app = True

# Worker timeout
graceful_timeout = 30

# Restart workers after this many requests
max_requests = 1000
max_requests_jitter = 50

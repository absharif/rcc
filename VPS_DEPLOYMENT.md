# VPS Deployment Guide

## PostgreSQL Permission Error Fix

If you're getting `permission denied for schema public` error, follow these steps:

### Option 1: Grant Permissions (Recommended)

Connect to PostgreSQL as a superuser (usually `postgres`) and run:

```sql
-- Connect to your database
\c your_database_name

-- Grant usage and create privileges on the public schema
GRANT USAGE ON SCHEMA public TO your_db_user;
GRANT CREATE ON SCHEMA public TO your_db_user;

-- Grant all privileges on all tables in public schema
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO your_db_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO your_db_user;

-- Set default privileges for future tables
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO your_db_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO your_db_user;
```

### Option 2: Using psql Command Line

```bash
# Connect as postgres user
sudo -u postgres psql

# Then run:
\c your_database_name
GRANT USAGE ON SCHEMA public TO your_db_user;
GRANT CREATE ON SCHEMA public TO your_db_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO your_db_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO your_db_user;
\q
```

### Option 3: Create Schema Explicitly

If the schema doesn't exist:

```sql
CREATE SCHEMA IF NOT EXISTS public;
GRANT ALL ON SCHEMA public TO your_db_user;
GRANT ALL ON SCHEMA public TO public;
```

## Complete VPS Setup Steps

### 1. Install PostgreSQL

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install postgresql postgresql-contrib

# CentOS/RHEL
sudo yum install postgresql-server postgresql-contrib
```

### 2. Create Database and User

```bash
# Switch to postgres user
sudo -u postgres psql

# Create database
CREATE DATABASE city_corporation;

# Create user
CREATE USER your_db_user WITH PASSWORD 'your_secure_password';

# Grant privileges
GRANT ALL PRIVILEGES ON DATABASE city_corporation TO your_db_user;

# Grant schema permissions
\c city_corporation
GRANT USAGE ON SCHEMA public TO your_db_user;
GRANT CREATE ON SCHEMA public TO your_db_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO your_db_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO your_db_user;

# Exit
\q
```

### 3. Install Python Dependencies

```bash
# Install PostgreSQL adapter
pip install psycopg2-binary

# Or if that fails, install system dependencies first:
sudo apt install python3-dev libpq-dev
pip install psycopg2-binary
```

### 4. Update .env File

```bash
# Edit .env file
nano .env
```

Update with PostgreSQL settings:

```env
SECRET_KEY=your-production-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com,your-server-ip

# PostgreSQL Configuration
DB_ENGINE=django.db.backends.postgresql
DB_NAME=city_corporation
DB_USER=your_db_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432

LANGUAGE_CODE=en-us
TIME_ZONE=UTC
```

### 5. Run Migrations

```bash
# Activate virtual environment
source venv/bin/activate

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

### 6. Configure PostgreSQL Authentication (if needed)

Edit PostgreSQL config:

```bash
sudo nano /etc/postgresql/*/main/pg_hba.conf
```

Make sure you have:

```
local   all             all                                     peer
host    all             all             127.0.0.1/32            md5
host    all             all             ::1/128                 md5
```

Restart PostgreSQL:

```bash
sudo systemctl restart postgresql
```

## Troubleshooting

### Error: "role does not exist"
```sql
-- Create the role/user
CREATE USER your_db_user WITH PASSWORD 'your_password';
```

### Error: "database does not exist"
```sql
-- Create the database
CREATE DATABASE city_corporation;
```

### Error: "could not connect to server"
- Check if PostgreSQL is running: `sudo systemctl status postgresql`
- Verify DB_HOST in .env (use `localhost` or `127.0.0.1` for local connections)
- Check PostgreSQL port (default is 5432)

### Error: "password authentication failed"
- Verify password in .env matches PostgreSQL user password
- Reset password: `ALTER USER your_db_user WITH PASSWORD 'new_password';`

## Security Best Practices

1. **Use strong passwords** for database users
2. **Set DEBUG=False** in production
3. **Use environment variables** for all sensitive data
4. **Restrict database access** to localhost only
5. **Regular backups** of your database
6. **Keep PostgreSQL updated**

## Quick Fix Script

Save this as `fix_db_permissions.sh`:

```bash
#!/bin/bash
DB_NAME="city_corporation"
DB_USER="your_db_user"

sudo -u postgres psql << EOF
\c $DB_NAME
GRANT USAGE ON SCHEMA public TO $DB_USER;
GRANT CREATE ON SCHEMA public TO $DB_USER;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO $DB_USER;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO $DB_USER;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO $DB_USER;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO $DB_USER;
\q
EOF
```

Make it executable and run:
```bash
chmod +x fix_db_permissions.sh
./fix_db_permissions.sh
```

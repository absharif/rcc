-- PostgreSQL Permission Fix Script
-- Run this as postgres superuser to fix permission errors
-- Usage: sudo -u postgres psql -d your_database_name -f fix_db_permissions.sql

-- Replace 'your_db_user' with your actual database username
-- Replace 'city_corporation' with your actual database name

-- Grant usage on schema
GRANT USAGE ON SCHEMA public TO your_db_user;

-- Grant create privileges on schema
GRANT CREATE ON SCHEMA public TO your_db_user;

-- Grant privileges on all existing tables
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO your_db_user;

-- Grant privileges on all existing sequences
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO your_db_user;

-- Set default privileges for future tables
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO your_db_user;

-- Set default privileges for future sequences
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO your_db_user;

-- Optional: If you need to create the schema
-- CREATE SCHEMA IF NOT EXISTS public;
-- GRANT ALL ON SCHEMA public TO your_db_user;
-- GRANT ALL ON SCHEMA public TO public;

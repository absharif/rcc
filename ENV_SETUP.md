# Environment Variables Setup

This project uses `python-decouple` to manage environment variables securely.

## Quick Setup

1. **Copy the example file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` file** with your configuration values

3. **Generate a new SECRET_KEY** for production:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
   Copy the output and paste it into your `.env` file.

## Environment Variables

### Required Variables

- `SECRET_KEY` - Django secret key (change in production!)
- `DEBUG` - Set to `False` in production
- `ALLOWED_HOSTS` - Comma-separated list of allowed hosts

### Database Configuration

**For SQLite (default):**
```
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
```

**For PostgreSQL:**
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=city_corporation
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```

### Optional Variables

- `LANGUAGE_CODE` - Default: `en-us`
- `TIME_ZONE` - Default: `UTC`

## Security Notes

⚠️ **IMPORTANT:**
- Never commit `.env` to version control
- Always use `.env.example` as a template
- Generate a new `SECRET_KEY` for production
- Set `DEBUG=False` in production
- Use strong database passwords in production

## How It Works

The `settings.py` file uses `python-decouple` to read values from `.env`:

```python
from decouple import config, Csv

SECRET_KEY = config('SECRET_KEY', default='fallback-value')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost', cast=Csv())
```

If a variable is not found in `.env`, it uses the default value.

## Troubleshooting

**Issue:** Settings not loading from `.env`
- Make sure `.env` file exists in the project root
- Check that `.env` is not in `.gitignore` (it should be!)
- Verify variable names match exactly (case-sensitive)

**Issue:** Database connection errors
- Check database credentials in `.env`
- Ensure database server is running
- Verify `DB_ENGINE` matches your database type

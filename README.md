# City Corporation Management System

A comprehensive Django-based administrative system for managing city corporation operations with a premium, modern UI design.

## Features

- **Citizen Management**: Manage citizen records and information
- **Holding Tax**: Track and manage property tax payments
- **Trade License**: Handle business license applications and renewals
- **Certification**: Process various certificate requests (birth, death, marriage, etc.)
- **Tender Management**: Manage public tenders and procurement
- **Citizen Charter**: Display service information and requirements
- **Complaint Management**: Track and resolve citizen complaints
- **Contact Management**: Handle inquiries and feedback

## Design Features

- **Premium Login Page**: Colorful, animated gradient background with modern UI
- **Custom Admin Dashboard**: Beautiful dashboard with statistics cards, charts, and real-time data
- **Sidebar Navigation**: Modern sidebar with organized sections and smooth animations
- **Responsive Layout**: Works seamlessly on desktop and mobile devices
- **Modern Color Scheme**: Professional gradient-based color palette
- **Interactive Charts**: Chart.js integration for data visualization

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd rcc
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env file and update SECRET_KEY and other settings
# For production, generate a new SECRET_KEY:
# python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

5. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

7. Access the application:
- **Home Page**: `http://127.0.0.1:8000/`
- **Admin Dashboard**: `http://127.0.0.1:8000/admin/dashboard/`
- **Login Page**: `http://127.0.0.1:8000/admin/login/`
- **Django Admin** (optional): `http://127.0.0.1:8000/django-admin/`

## Project Structure

```
rcc/
├── citizen/              # Citizen management app
├── holdingtax/           # Holding tax management
├── tradelicense/         # Trade license management
├── certification/        # Certificate management
├── tender/               # Tender management
├── citizencharter/       # Citizen charter services
├── complaint/            # Complaint management
├── contact/              # Contact management
├── city_corporation/     # Main project settings
├── templates/            # Custom templates
│   ├── admin/           # Admin templates
│   └── registration/    # Login templates
├── static/              # Static files (CSS, JS, images)
└── manage.py            # Django management script
```

## Apps Overview

### Citizen App
- Manage citizen profiles
- Link citizens to user accounts
- Track citizen information and documents

### Holding Tax App
- Track property tax payments
- Manage tax due dates and amounts
- Payment status tracking

### Trade License App
- Business license applications
- License renewal management
- Status tracking (pending, approved, expired)

### Certification App
- Multiple certificate types (birth, death, marriage, etc.)
- Certificate issuance tracking
- Status management

### Tender App
- Public tender management
- Tender publication and tracking
- Document management

### Citizen Charter App
- Service information display
- Processing time and requirements
- Fee information

### Complaint App
- Citizen complaint tracking
- Priority and status management
- Resolution tracking

### Contact App
- Inquiry management
- Feedback collection
- Contact form submissions

## Customization

### Changing Colors
Edit `static/css/admin_custom.css` to modify the color scheme:
- Primary color: `--primary-color`
- Secondary color: `--secondary-color`
- Accent color: `--accent-color`

### Adding New Apps
1. Create the app: `python manage.py startapp appname`
2. Add to `INSTALLED_APPS` in `settings.py`
3. Create models and register in admin
4. Add navigation link in `templates/admin/base.html`

## Development

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Collecting Static Files
```bash
python manage.py collectstatic
```

## License

This project is developed for City Corporation management purposes.

## Support

For issues and questions, please contact the development team.

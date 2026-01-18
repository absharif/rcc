# User Groups and Role-Based Access Control Setup

This document explains the user group system and how to set up roles for different users.

## User Groups

The system has 4 main user groups:

### 1. **Citizen** (`citizen`)
- **Access**: Can login and view their own data
- **Capabilities**:
  - View their own properties
  - View their own holding taxes
  - View their own trade licenses
  - View their own certifications
- **Dashboard**: `/citizen/dashboard/`
- **Note**: Citizens must have a `Citizen` profile linked to their user account via the `user` field

### 2. **Holding Tax Field Officer** (`Holding Tax Field Officer`)
- **Access**: Can add citizens, create properties, and create holding taxes
- **Capabilities**:
  - Add new citizens
  - Create properties
  - Create holding taxes
  - View all citizens, properties, and holding taxes
- **Dashboard**: `/field-officer/dashboard/`
- **Workflow**: Field officers create records, which are then approved by Officers

### 3. **Officer** (`Officer`)
- **Access**: Can approve holding taxes and certificates
- **Capabilities**:
  - Approve/reject holding taxes
  - Approve/reject certifications
  - View pending items
- **Dashboard**: `/officer/dashboard/`
- **Workflow**: Officers review and approve items created by Field Officers

### 4. **SuperAdmin** (`SuperAdmin`)
- **Access**: Full Django admin access
- **Capabilities**:
  - Access to Django admin interface (`/django-admin/`)
  - Full access to all features
  - Can manage all data
- **Dashboard**: `/admin/dashboard/`
- **Note**: SuperAdmin users should have `is_staff=True` and `is_superuser=True` in Django admin

## Setup Instructions

### Step 1: Run Migrations

```bash
python manage.py migrate
```

### Step 2: Create User Groups

Run the management command to create groups and assign permissions:

```bash
python manage.py setup_user_groups
```

This will create:
- `citizen` group
- `Holding Tax Field Officer` group
- `Officer` group
- `SuperAdmin` group

### Step 3: Create Users and Assign Groups

#### Option A: Using Django Admin (for SuperAdmin)

1. Go to `/django-admin/`
2. Navigate to **Users** → **Add user**
3. Create user with username and password
4. Go to **Groups** section and assign appropriate group
5. For SuperAdmin: Check `is_staff` and `is_superuser` checkboxes

#### Option B: Using Django Shell

```python
from django.contrib.auth.models import User, Group
from citizen.models import Citizen

# Create a citizen user
user = User.objects.create_user('citizen1', 'citizen1@example.com', 'password123')
citizen_group = Group.objects.get(name='citizen')
user.groups.add(citizen_group)

# Link citizen profile to user
citizen = Citizen.objects.get(national_id='1234567890')  # Use actual NID
citizen.user = user
citizen.save()

# Create a field officer
field_officer = User.objects.create_user('fieldofficer1', 'fo@example.com', 'password123')
field_officer_group = Group.objects.get(name='Holding Tax Field Officer')
field_officer.groups.add(field_officer_group)

# Create an officer
officer = User.objects.create_user('officer1', 'officer@example.com', 'password123')
officer_group = Group.objects.get(name='Officer')
officer.groups.add(officer_group)

# Create a superadmin
superadmin = User.objects.create_user('admin', 'admin@example.com', 'admin123')
superadmin.is_staff = True
superadmin.is_superuser = True
superadmin.save()
superadmin_group = Group.objects.get(name='SuperAdmin')
superadmin.groups.add(superadmin_group)
```

## URL Routes

### Citizen Routes
- Dashboard: `/citizen/dashboard/`
- My Properties: `/citizen/my-properties/`
- My Taxes: `/citizen/my-taxes/`
- My Licenses: `/citizen/my-licenses/`
- My Certifications: `/citizen/my-certifications/`

### Field Officer Routes
- Dashboard: `/field-officer/dashboard/`
- Citizens: `/field-officer/citizens/`
- Create Citizen: `/field-officer/citizens/create/`
- Properties: `/field-officer/properties/`
- Create Property: `/field-officer/properties/create/`
- Holding Taxes: `/field-officer/holding-taxes/`
- Create Holding Tax: `/field-officer/holding-taxes/create/`

### Officer Routes
- Dashboard: `/officer/dashboard/`
- Pending Holding Taxes: `/officer/holding-taxes/`
- Approve Holding Tax: `/officer/holding-taxes/<id>/approve/`
- Pending Certifications: `/officer/certifications/`
- Approve Certification: `/officer/certifications/<id>/approve/`

### SuperAdmin Routes
- Django Admin: `/django-admin/`
- Custom Dashboard: `/admin/dashboard/`

## Login Flow

When a user logs in at `/admin/login/`, they are automatically redirected based on their group:

1. **SuperAdmin** → `/admin/dashboard/`
2. **Citizen** → `/citizen/dashboard/`
3. **Holding Tax Field Officer** → `/field-officer/dashboard/`
4. **Officer** → `/officer/dashboard/`

## Permissions

Permissions are enforced using decorators:

- `@citizen_required` - Only citizens can access
- `@field_officer_required` - Only field officers can access
- `@officer_required` - Only officers can access
- `@superadmin_required` - Only superadmins can access
- `@group_required('GroupName')` - Custom group check

## Important Notes

1. **Citizen Profile Linking**: For citizens to access their dashboard, their `Citizen` record must be linked to their `User` account via the `user` field.

2. **Django Admin Access**: Only users with `is_staff=True` and `is_superuser=True` OR users in the `SuperAdmin` group can access `/django-admin/`.

3. **Field Officer Workflow**: Field officers create records (citizens, properties, holding taxes) which are set to `PENDING` status. Officers then review and approve them.

4. **Citizen Data Access**: Citizens can only see their own data. The views filter data based on the linked citizen profile.

## Troubleshooting

### Citizen cannot access dashboard
- Check if `Citizen.user` is set to the user account
- Verify user is in the `citizen` group
- Check if citizen profile exists

### Field Officer cannot create records
- Verify user is in `Holding Tax Field Officer` group
- Check permissions are assigned correctly

### Officer cannot approve items
- Verify user is in `Officer` group
- Check if items are in `PENDING` status

### SuperAdmin cannot access Django admin
- Ensure `is_staff=True` and `is_superuser=True`
- Or add user to `SuperAdmin` group

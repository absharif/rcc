"""
Management command to create user groups and assign permissions.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from citizen.models import Citizen, CitizenDocument
from holdingtax.models import (
    Area, Street, PropertyType, Property, TaxPeriod, 
    HoldingTax, AttachmentType, PropertyAttachment, TaxPayment
)
from tradelicense.models import TradeLicense
from certification.models import Certification, CertificationType
from tender.models import Tender
from citizencharter.models import CitizenCharter
from complaint.models import Complaint
from contact.models import Contact


class Command(BaseCommand):
    help = 'Creates user groups and assigns permissions'

    def handle(self, *args, **options):
        # Create groups
        citizen_group, created = Group.objects.get_or_create(name='citizen')
        field_officer_group, created = Group.objects.get_or_create(name='Holding Tax Field Officer')
        officer_group, created = Group.objects.get_or_create(name='Officer')
        superadmin_group, created = Group.objects.get_or_create(name='SuperAdmin')

        # Get content types
        citizen_ct = ContentType.objects.get_for_model(Citizen)
        citizendocument_ct = ContentType.objects.get_for_model(CitizenDocument)
        property_ct = ContentType.objects.get_for_model(Property)
        holdingtax_ct = ContentType.objects.get_for_model(HoldingTax)
        tradelicense_ct = ContentType.objects.get_for_model(TradeLicense)
        certification_ct = ContentType.objects.get_for_model(Certification)
        
        # Citizen Group Permissions - View own data only
        # Note: We'll handle view permissions in views, not Django permissions
        # Citizens can view their own records (handled in views)
        
        # Holding Tax Field Officer Permissions
        # Use existing Django permissions (created automatically)
        field_officer_permissions = []
        
        # Citizen permissions
        try:
            field_officer_permissions.append(Permission.objects.get(codename='add_citizen', content_type=citizen_ct))
            field_officer_permissions.append(Permission.objects.get(codename='change_citizen', content_type=citizen_ct))
            field_officer_permissions.append(Permission.objects.get(codename='view_citizen', content_type=citizen_ct))
        except Permission.DoesNotExist:
            pass
        
        # Property permissions
        try:
            field_officer_permissions.append(Permission.objects.get(codename='add_property', content_type=property_ct))
            field_officer_permissions.append(Permission.objects.get(codename='change_property', content_type=property_ct))
            field_officer_permissions.append(Permission.objects.get(codename='view_property', content_type=property_ct))
        except Permission.DoesNotExist:
            pass
        
        # Holding Tax permissions
        try:
            field_officer_permissions.append(Permission.objects.get(codename='add_holdingtax', content_type=holdingtax_ct))
            field_officer_permissions.append(Permission.objects.get(codename='change_holdingtax', content_type=holdingtax_ct))
            field_officer_permissions.append(Permission.objects.get(codename='view_holdingtax', content_type=holdingtax_ct))
        except Permission.DoesNotExist:
            pass
        
        if field_officer_permissions:
            field_officer_group.permissions.set(field_officer_permissions)
        
        # Officer Group Permissions - Can approve
        officer_permissions = []
        
        # Holding Tax - approve
        try:
            officer_permissions.append(Permission.objects.get(codename='change_holdingtax', content_type=holdingtax_ct))
            officer_permissions.append(Permission.objects.get(codename='view_holdingtax', content_type=holdingtax_ct))
        except Permission.DoesNotExist:
            pass
        
        # Certification - approve
        try:
            officer_permissions.append(Permission.objects.get(codename='change_certification', content_type=certification_ct))
            officer_permissions.append(Permission.objects.get(codename='view_certification', content_type=certification_ct))
        except Permission.DoesNotExist:
            pass
        
        # Trade License - approve
        try:
            officer_permissions.append(Permission.objects.get(codename='change_tradelicense', content_type=tradelicense_ct))
            officer_permissions.append(Permission.objects.get(codename='view_tradelicense', content_type=tradelicense_ct))
        except Permission.DoesNotExist:
            pass
        
        if officer_permissions:
            officer_group.permissions.set(officer_permissions)
        
        # SuperAdmin - All permissions (handled via is_staff and is_superuser)
        # No need to assign specific permissions, they have Django admin access
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created/updated groups:\n'
                f'- Citizen\n'
                f'- Holding Tax Field Officer\n'
                f'- Officer\n'
                f'- SuperAdmin'
            )
        )

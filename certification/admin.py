from django.contrib import admin
from .models import Certification


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ('certificate_number', 'citizen', 'certificate_type', 'status', 'issue_date', 'created_at')
    list_filter = ('certificate_type', 'status', 'created_at')
    search_fields = ('certificate_number', 'citizen__first_name', 'citizen__last_name', 'citizen__nid')
    readonly_fields = ('created_at', 'updated_at')

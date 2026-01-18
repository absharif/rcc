from django.contrib import admin
from .models import Certification, CertificationType


@admin.register(CertificationType)
class CertificationTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'fee', 'validity_days', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'code')
    readonly_fields = ('created_at',)


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ('certificate_number', 'citizen', 'certification_type', 'status', 'issue_date', 'expiry_date', 'created_at')
    list_filter = ('status', 'certification_type', 'created_at', 'issue_date')
    search_fields = ('certificate_number', 'citizen__first_name', 'citizen__last_name', 'citizen__national_id')
    readonly_fields = ('created_at', 'updated_at', 'pdf_file')
    fieldsets = (
        ('Certificate Information', {
            'fields': ('certificate_number', 'citizen', 'certification_type', 'status')
        }),
        ('Dates', {
            'fields': ('issue_date', 'expiry_date')
        }),
        ('Details', {
            'fields': ('remarks', 'rejection_reason', 'pdf_file')
        }),
        ('System', {
            'fields': ('created_by', 'issued_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

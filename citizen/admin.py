from django.contrib import admin
from .models import Citizen, CitizenDocument


@admin.register(Citizen)
class CitizenAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'national_id', 'phone_number', 'email', 'city', 'is_active', 'created_at')
    list_filter = ('is_active', 'gender', 'marital_status', 'city', 'created_at')
    search_fields = ('national_id', 'citizen_id', 'first_name', 'last_name', 'middle_name', 'email', 'phone_number')
    readonly_fields = ('created_at', 'updated_at', 'full_name')
    fieldsets = (
        ('Personal Information', {
            'fields': ('citizen_id', 'first_name', 'last_name', 'middle_name', 'co_name', 'date_of_birth', 'gender', 'marital_status', 'national_id')
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'email', 'address', 'city', 'postal_code')
        }),
        ('Additional Information', {
            'fields': ('occupation', 'photo', 'notes')
        }),
        ('System Information', {
            'fields': ('is_active', 'created_by', 'created_at', 'updated_at')
        }),
    )


@admin.register(CitizenDocument)
class CitizenDocumentAdmin(admin.ModelAdmin):
    list_display = ('citizen', 'document_type', 'document_number', 'issue_date', 'expiry_date', 'uploaded_at')
    list_filter = ('document_type', 'uploaded_at')
    search_fields = ('citizen__first_name', 'citizen__last_name', 'citizen__national_id', 'document_number')
    readonly_fields = ('uploaded_at',)

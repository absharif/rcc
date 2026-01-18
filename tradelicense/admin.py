from django.contrib import admin
from .models import TradeLicense


@admin.register(TradeLicense)
class TradeLicenseAdmin(admin.ModelAdmin):
    list_display = ('license_number', 'business_name', 'citizen', 'status', 'issue_date', 'expiry_date')
    list_filter = ('status', 'issue_date', 'expiry_date', 'created_at')
    search_fields = ('license_number', 'business_name', 'citizen__first_name', 'citizen__last_name')
    readonly_fields = ('created_at', 'updated_at')

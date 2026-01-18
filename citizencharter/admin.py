from django.contrib import admin
from .models import CitizenCharter


@admin.register(CitizenCharter)
class CitizenCharterAdmin(admin.ModelAdmin):
    list_display = ('title', 'service_type', 'processing_time', 'fees', 'is_active', 'created_at')
    list_filter = ('service_type', 'is_active', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')

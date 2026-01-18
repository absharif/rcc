from django.contrib import admin
from .models import Tender


@admin.register(Tender)
class TenderAdmin(admin.ModelAdmin):
    list_display = ('tender_number', 'title', 'status', 'opening_date', 'closing_date', 'estimated_value', 'created_at')
    list_filter = ('status', 'opening_date', 'closing_date', 'created_at')
    search_fields = ('tender_number', 'title', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Tender Information', {
            'fields': ('tender_number', 'title', 'description', 'status')
        }),
        ('Dates & Value', {
            'fields': ('opening_date', 'closing_date', 'estimated_value')
        }),
        ('Document', {
            'fields': ('document_url',)
        }),
        ('System', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
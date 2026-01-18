from django.contrib import admin
from .models import Complaint


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('complaint_number', 'subject', 'citizen', 'category', 'priority', 'status', 'submitted_at')
    list_filter = ('status', 'priority', 'category', 'submitted_at')
    search_fields = ('complaint_number', 'subject', 'description', 'citizen__first_name', 'citizen__last_name', 'citizen__national_id')
    readonly_fields = ('submitted_at', 'updated_at')
    fieldsets = (
        ('Complaint Information', {
            'fields': ('complaint_number', 'citizen', 'subject', 'description', 'category')
        }),
        ('Status & Priority', {
            'fields': ('status', 'priority')
        }),
        ('Resolution', {
            'fields': ('resolution', 'resolved_at')
        }),
        ('System', {
            'fields': ('submitted_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
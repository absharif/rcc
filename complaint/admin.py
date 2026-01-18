from django.contrib import admin
from .models import Complaint


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('complaint_number', 'citizen', 'subject', 'category', 'status', 'priority', 'submitted_at')
    list_filter = ('status', 'priority', 'category', 'submitted_at')
    search_fields = ('complaint_number', 'subject', 'description', 'citizen__first_name', 'citizen__last_name')
    readonly_fields = ('submitted_at', 'updated_at')

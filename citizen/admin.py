from django.contrib import admin
from .models import Citizen


@admin.register(Citizen)
class CitizenAdmin(admin.ModelAdmin):
    list_display = ('nid', 'first_name', 'last_name', 'email', 'phone', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('nid', 'first_name', 'last_name', 'email', 'phone')
    readonly_fields = ('created_at', 'updated_at')

from django.contrib import admin
from .models import HoldingTax


@admin.register(HoldingTax)
class HoldingTaxAdmin(admin.ModelAdmin):
    list_display = ('holding_number', 'citizen', 'tax_amount', 'due_date', 'payment_status', 'created_at')
    list_filter = ('payment_status', 'due_date', 'created_at')
    search_fields = ('holding_number', 'citizen__first_name', 'citizen__last_name', 'citizen__nid')
    readonly_fields = ('created_at', 'updated_at')

from django.contrib import admin
from .models import (
    Area, Street, PropertyType, Property, TaxPeriod,
    HoldingTax, AttachmentType, PropertyAttachment, TaxPayment
)


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'code')
    readonly_fields = ('created_at',)


@admin.register(Street)
class StreetAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'area', 'is_active', 'created_at')
    list_filter = ('is_active', 'area', 'created_at')
    search_fields = ('name', 'code', 'area__name')
    readonly_fields = ('created_at',)


@admin.register(PropertyType)
class PropertyTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'code')
    readonly_fields = ('created_at',)


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('property_number', 'owner', 'property_type', 'city', 'status', 'is_active', 'created_at')
    list_filter = ('status', 'is_active', 'property_type', 'area', 'created_at')
    search_fields = ('property_number', 'owner__first_name', 'owner__last_name', 'owner__national_id', 'address')
    readonly_fields = ('created_at', 'updated_at', 'annual_tax_amount')
    fieldsets = (
        ('Basic Information', {
            'fields': ('property_number', 'property_type', 'owner', 'status', 'is_active')
        }),
        ('Location', {
            'fields': ('address', 'area', 'street', 'city', 'postal_code')
        }),
        ('Assessment', {
            'fields': ('area_sqft', 'assessed_value', 'tax_rate', 'annual_tax_amount')
        }),
        ('Workflow', {
            'fields': ('created_by', 'submitted_by', 'submitted_at', 'approved_by', 'approved_at', 'rejection_reason'),
            'classes': ('collapse',)
        }),
        ('Additional', {
            'fields': ('notes', 'created_at', 'updated_at')
        }),
    )


@admin.register(TaxPeriod)
class TaxPeriodAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name',)
    readonly_fields = ('created_at',)


@admin.register(HoldingTax)
class HoldingTaxAdmin(admin.ModelAdmin):
    list_display = ('tax_number', 'holding_property', 'tax_period', 'tax_amount', 'paid_amount', 'due_date', 'status', 'created_at')
    list_filter = ('status', 'tax_period', 'due_date', 'created_at')
    search_fields = ('tax_number', 'holding_property__property_number', 'holding_property__owner__first_name', 'holding_property__owner__last_name')
    readonly_fields = ('created_at', 'updated_at', 'balance_amount')
    fieldsets = (
        ('Tax Information', {
            'fields': ('tax_number', 'holding_property', 'tax_period', 'due_date', 'status')
        }),
        ('Amounts', {
            'fields': ('tax_amount', 'paid_amount', 'penalty_amount', 'balance_amount')
        }),
        ('Additional', {
            'fields': ('notes', 'created_by', 'created_at', 'updated_at')
        }),
    )


@admin.register(AttachmentType)
class AttachmentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'code')
    readonly_fields = ('created_at',)


@admin.register(PropertyAttachment)
class PropertyAttachmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'property', 'attachment_type', 'uploaded_by', 'uploaded_at', 'is_active')
    list_filter = ('is_active', 'attachment_type', 'uploaded_at')
    search_fields = ('title', 'property__property_number', 'description')
    readonly_fields = ('uploaded_at',)


@admin.register(TaxPayment)
class TaxPaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_number', 'holding_tax', 'payment_date', 'amount', 'payment_method', 'received_by', 'created_at')
    list_filter = ('payment_method', 'payment_date', 'created_at')
    search_fields = ('payment_number', 'holding_tax__tax_number', 'reference_number', 'cheque_number')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Payment Information', {
            'fields': ('payment_number', 'holding_tax', 'payment_date', 'amount', 'payment_method')
        }),
        ('Payment Details', {
            'fields': ('reference_number', 'cheque_number', 'bank_name', 'notes', 'received_by')
        }),
        ('System', {
            'fields': ('created_at',)
        }),
    )

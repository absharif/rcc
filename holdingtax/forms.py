from django import forms
from decimal import Decimal
from .models import (
    Area, Street, PropertyType, Property, TaxPeriod, 
    HoldingTax, AttachmentType, PropertyAttachment, TaxPayment
)


class AreaForm(forms.ModelForm):
    """Form for Area."""
    
    class Meta:
        model = Area
        fields = ['name', 'code', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class StreetForm(forms.ModelForm):
    """Form for Street."""
    
    class Meta:
        model = Street
        fields = ['name', 'code', 'area', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'area': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['area'].queryset = Area.objects.filter(is_active=True)


class PropertyTypeForm(forms.ModelForm):
    """Form for PropertyType."""
    
    class Meta:
        model = PropertyType
        fields = ['name', 'code', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class PropertyForm(forms.ModelForm):
    """Form for Property."""
    
    class Meta:
        model = Property
        fields = [
            'property_number', 'property_type', 'owner', 'address', 
            'area', 'street', 'city', 'postal_code', 'area_sqft',
            'assessed_value', 'tax_rate', 'status', 'notes', 'is_active'
        ]
        widgets = {
            'property_number': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'property_type': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'owner': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'required': True}),
            'area': forms.Select(attrs={'class': 'form-control'}),
            'street': forms.Select(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'area_sqft': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'required': True}),
            'assessed_value': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'required': True}),
            'tax_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from citizen.models import Citizen
        self.fields['property_type'].queryset = PropertyType.objects.filter(is_active=True)
        self.fields['owner'].queryset = Citizen.objects.filter(is_active=True)
        self.fields['area'].queryset = Area.objects.filter(is_active=True)
        self.fields['street'].queryset = Street.objects.filter(is_active=True)


class TaxPeriodForm(forms.ModelForm):
    """Form for TaxPeriod."""
    
    class Meta:
        model = TaxPeriod
        fields = ['name', 'start_date', 'end_date', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'required': True}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'required': True}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class HoldingTaxForm(forms.ModelForm):
    """Form for HoldingTax."""
    
    class Meta:
        model = HoldingTax
        fields = [
            'tax_number', 'holding_property', 'tax_period', 'tax_amount',
            'paid_amount', 'due_date', 'status', 'penalty_amount', 'notes'
        ]
        widgets = {
            'tax_number': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'holding_property': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'tax_period': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'tax_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'required': True}),
            'paid_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'required': True}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'penalty_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['holding_property'].queryset = Property.objects.filter(is_active=True)
        self.fields['tax_period'].queryset = TaxPeriod.objects.filter(is_active=True)


class TaxPaymentForm(forms.ModelForm):
    """Form for TaxPayment."""
    
    class Meta:
        model = TaxPayment
        fields = [
            'payment_number', 'holding_tax', 'payment_date', 'amount',
            'payment_method', 'reference_number', 'cheque_number', 
            'bank_name', 'notes'
        ]
        widgets = {
            'payment_number': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'holding_tax': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'payment_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'required': True}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'required': True}),
            'payment_method': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'reference_number': forms.TextInput(attrs={'class': 'form-control'}),
            'cheque_number': forms.TextInput(attrs={'class': 'form-control'}),
            'bank_name': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Don't filter holding_tax queryset here as it's set in the view


class PropertyAttachmentForm(forms.ModelForm):
    """Form for PropertyAttachment."""
    
    class Meta:
        model = PropertyAttachment
        fields = ['attachment_type', 'title', 'description', 'file', 'is_active']
        widgets = {
            'attachment_type': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'file': forms.FileInput(attrs={'class': 'form-control', 'required': True}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['attachment_type'].queryset = AttachmentType.objects.filter(is_active=True)
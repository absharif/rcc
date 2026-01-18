from django import forms
from .models import TradeLicense


class TradeLicenseForm(forms.ModelForm):
    """Form for TradeLicense."""
    
    class Meta:
        model = TradeLicense
        fields = [
            'license_number', 'citizen', 'business_name', 'business_type',
            'business_address', 'issue_date', 'expiry_date', 'status', 'license_fee'
        ]
        widgets = {
            'license_number': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'citizen': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'business_name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'business_type': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'business_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'required': True}),
            'issue_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'required': True}),
            'expiry_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'required': True}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'license_fee': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'required': True}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from citizen.models import Citizen
        self.fields['citizen'].queryset = Citizen.objects.filter(is_active=True)

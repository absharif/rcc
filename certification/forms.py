from django import forms
from .models import Certification, CertificationType


class CertificationTypeForm(forms.ModelForm):
    """Form for CertificationType."""
    
    class Meta:
        model = CertificationType
        fields = ['name', 'code', 'description', 'fee', 'validity_days', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'fee': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'validity_days': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class CertificationForm(forms.ModelForm):
    """Form for Certification."""
    
    class Meta:
        model = Certification
        fields = [
            'certificate_number', 'citizen', 'certification_type',
            'issue_date', 'expiry_date', 'status', 'remarks'
        ]
        widgets = {
            'certificate_number': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'citizen': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'certification_type': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'issue_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from citizen.models import Citizen
        self.fields['citizen'].queryset = Citizen.objects.filter(is_active=True)
        self.fields['certification_type'].queryset = CertificationType.objects.filter(is_active=True)

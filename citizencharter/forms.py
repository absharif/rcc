from django import forms
from .models import CitizenCharter


class CitizenCharterForm(forms.ModelForm):
    """Form for CitizenCharter."""
    
    class Meta:
        model = CitizenCharter
        fields = [
            'title', 'service_type', 'description', 'processing_time',
            'required_documents', 'fees', 'is_active'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'service_type': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'required': True}),
            'processing_time': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'required_documents': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'required': True}),
            'fees': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

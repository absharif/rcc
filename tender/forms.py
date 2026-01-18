from django import forms
from .models import Tender


class TenderForm(forms.ModelForm):
    """Form for Tender."""
    
    class Meta:
        model = Tender
        fields = [
            'tender_number', 'title', 'description', 'opening_date',
            'closing_date', 'estimated_value', 'status', 'document_url'
        ]
        widgets = {
            'tender_number': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'required': True}),
            'opening_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control', 'required': True}),
            'closing_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control', 'required': True}),
            'estimated_value': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'required': True}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'document_url': forms.URLInput(attrs={'class': 'form-control'}),
        }

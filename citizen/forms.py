from django import forms
from .models import Citizen, CitizenDocument


class CitizenForm(forms.ModelForm):
    """Form for creating and updating citizens."""
    
    class Meta:
        model = Citizen
        fields = [
            'citizen_id', 'first_name', 'last_name', 'middle_name', 'co_name',
            'date_of_birth', 'gender', 'marital_status', 'national_id',
            'phone_number', 'email', 'address', 'city', 'postal_code',
            'occupation', 'photo', 'notes', 'is_active'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'co_name': forms.TextInput(attrs={'class': 'form-control'}),
            'national_id': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+8801XXXXXXXXX'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'occupation': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'marital_status': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['national_id'].required = True
        self.fields['date_of_birth'].required = True
        self.fields['gender'].required = True
        self.fields['address'].required = False  # Made optional for migration compatibility
        self.fields['city'].required = False  # Made optional for migration compatibility


class CitizenDocumentForm(forms.ModelForm):
    """Form for adding citizen documents."""
    
    class Meta:
        model = CitizenDocument
        fields = ['document_type', 'document_number', 'file', 'issue_date', 'expiry_date', 'description']
        widgets = {
            'document_type': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'document_number': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'file': forms.FileInput(attrs={'class': 'form-control', 'required': True}),
            'issue_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

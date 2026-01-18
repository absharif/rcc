from django import forms
from .models import Complaint


class ComplaintForm(forms.ModelForm):
    """Form for Complaint."""
    
    class Meta:
        model = Complaint
        fields = [
            'complaint_number', 'citizen', 'subject', 'description',
            'category', 'status', 'priority', 'resolution'
        ]
        widgets = {
            'complaint_number': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'citizen': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'required': True}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'resolution': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from citizen.models import Citizen
        self.fields['citizen'].queryset = Citizen.objects.filter(is_active=True)


class PublicComplaintForm(forms.ModelForm):
    """Public form for Complaint submission (no login required)."""
    
    # Optional fields for anonymous complaints
    citizen_name = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Name (Optional)'
        }),
        label='Your Name'
    )
    citizen_email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Email (Optional)'
        }),
        label='Your Email'
    )
    citizen_phone = forms.CharField(
        max_length=17,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Phone Number (Optional)'
        }),
        label='Your Phone Number'
    )
    
    class Meta:
        model = Complaint
        fields = ['subject', 'description', 'category', 'priority']
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'required': True,
                'placeholder': 'Brief description of your complaint'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'required': True,
                'placeholder': 'Please provide detailed information about your complaint...'
            }),
            'category': forms.TextInput(attrs={
                'class': 'form-control',
                'required': True,
                'placeholder': 'e.g., Water Supply, Road Maintenance, Waste Management'
            }),
            'priority': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default priority
        self.fields['priority'].initial = 'medium'
        # Remove complaint_number, citizen, status, resolution from public form
        if 'complaint_number' in self.fields:
            del self.fields['complaint_number']
        if 'citizen' in self.fields:
            del self.fields['citizen']
        if 'status' in self.fields:
            del self.fields['status']
        if 'resolution' in self.fields:
            del self.fields['resolution']

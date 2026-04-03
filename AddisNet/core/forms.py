"""
Django Forms for AddisNet

Provides form classes for:
- Issue reporting with validation
- Community posts
- User signup
- Emergency alerts
"""

from django import forms
from .models import Issue, Post, CustomUser, EmergencyAlert


class IssueForm(forms.ModelForm):
    """Form for reporting city issues"""
    
    class Meta:
        model = Issue
        fields = [
            'title', 'description', 'category', 'severity',
            'latitude', 'longitude', 'address', 'sub_city',
            'image', 'video'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Brief title describing the issue',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Detailed description of the issue...',
                'rows': 5,
                'required': True
            }),
            'category': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'severity': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'latitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.000001',
                'placeholder': 'Latitude (e.g., 9.0320)',
                'required': True
            }),
            'longitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.000001',
                'placeholder': 'Longitude (e.g., 38.7469)',
                'required': True
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Street address or landmark'
            }),
            'sub_city': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Select sub-city'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'video': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'video/*'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Ethiopian sub-cities
        self.fields['sub_city'].choices = [
            ('', 'Select Sub-City'),
            ('Addis Ketema', 'Addis Ketema'),
            ('Akaky Kaliti', 'Akaky Kaliti'),
            ('Arada', 'Arada'),
            ('Bole', 'Bole'),
            ('Gullele', 'Gullele'),
            ('Kirkos', 'Kirkos'),
            ('Kolfe Keranio', 'Kolfe Keranio'),
            ('Lideta', 'Lideta'),
            ('Nifas Silk-Lafto', 'Nifas Silk-Lafto'),
            ('Yeka', 'Yeka'),
        ]


class PostForm(forms.ModelForm):
    """Form for creating community posts"""
    
    class Meta:
        model = Post
        fields = ['type', 'title', 'description', 'tags', 'latitude', 'longitude']
        widgets = {
            'type': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Post title',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe your post...',
                'rows': 5,
                'required': True
            }),
            'tags': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tags (comma-separated)'
            }),
            'latitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.000001',
                'placeholder': 'Latitude (optional)'
            }),
            'longitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.000001',
                'placeholder': 'Longitude (optional)'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tags'].help_text = 'Separate tags with commas'


class UserSignupForm(forms.ModelForm):
    """User registration form"""
    
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password',
        'required': True
    }))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm Password',
        'required': True
    }))
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'role', 'phone', 'location', 'language_preference']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email',
                'required': True
            }),
            'role': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+251...'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your neighborhood in Addis Ababa'
            }),
            'language_preference': forms.Select(attrs={
                'class': 'form-select',
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match")
        
        return cleaned_data


class EmergencyAlertForm(forms.ModelForm):
    """Form for creating emergency alerts"""
    
    class Meta:
        model = EmergencyAlert
        fields = ['alert_type', 'priority', 'title', 'description', 
                  'latitude', 'longitude', 'affected_radius_km']
        widgets = {
            'alert_type': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'priority': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Alert title',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Detailed description of the emergency...',
                'rows': 4,
                'required': True
            }),
            'latitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.000001',
                'required': True
            }),
            'longitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.000001',
                'required': True
            }),
            'affected_radius_km': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'value': '1.0'
            }),
        }

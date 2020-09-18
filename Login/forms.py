"""
This file contains forms used for user login.
"""

# -----------------------------------------------------------------------------------------------------------------------------------------
#       IMPORTS                 
# -----------------------------------------------------------------------------------------------------------------------------------------
from django import forms
from .models import User
from django.core.validators import EmailValidator

# -----------------------------------------------------------------------------------------------------------------------------------------
#       LOGIN FORM          
# -----------------------------------------------------------------------------------------------------------------------------------------
class LoginForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'id': 'email',
        'placeholder': 'email...',
    }), validators=[EmailValidator()])

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'id': 'password',
        'placeholder': 'password...',
    }))
    
    class Meta:
        model = User
        fields = {
            'email',
            'password'
        }
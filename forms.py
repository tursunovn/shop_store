from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import *

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Имя пользователя'
    }))
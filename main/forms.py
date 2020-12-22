from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CreateUserForm(UserCreationForm):
    birthdate = forms.DateField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'birthdate', 'password1', 'password2']
        
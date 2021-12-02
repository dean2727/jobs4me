from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from jobs4me.models import Resume, AppUser

class CreateUserForm(UserCreationForm):
    class Meta:
        model = AppUser
        fields = ['username', 'name', 'email', 'password1', 'password2', 'phone_number', 'email', 'country', 'state', 'city', 'gpa', 'comments']

class UploadResumeForm(ModelForm):
    class Meta: 
        model = Resume
        fields = ['name', 'resume_file']
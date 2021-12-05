from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from jobs4me.models import Resume, AppUser

class CreateUserForm(UserCreationForm):
    class Meta:
        model = AppUser
        fields = ['username', 'name', 'email', 'password1', 'password2', 'phone_number', 'email', 'country', 'state', 'city', 'gpa', 'comments']
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Username* (max of 50 characters) ...'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password* ...'
        self.fields['password2'].widget.attrs['placeholder'] = 'Re-enter Password* ...'
        self.fields['name'].widget.attrs['placeholder'] = 'Name* (first and last) ...'
        self.fields['email'].widget.attrs['placeholder'] = 'Email* (max of 254 characters)..'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Phone number* (e.g.: +14255550123) ...'
        self.fields['country'].widget.attrs['placeholder'] = 'Country* ...'
        self.fields['state'].widget.attrs['placeholder'] = 'State ...'
        self.fields['city'].widget.attrs['placeholder'] = 'City* ...'
        self.fields['gpa'].widget.attrs['placeholder'] = 'GPA (e.g. 3.26) ...'
        self.fields['comments'].widget.attrs['placeholder'] = 'Comments (optional) ...'

class UploadResumeForm(ModelForm):
    class Meta: 
        model = Resume
        fields = ['name', 'resume_file']
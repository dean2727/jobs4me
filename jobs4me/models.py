import datetime
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class AppUser(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50)
    phone_regex = RegexValidator(regex=r'^\+?[1-9]\d{1,14}$',
        message="Phone number was entered incorrectly! Make sure it is E.164 international standard format (e.g.: +14255550123)")
    phone_number = models.CharField(validators=[phone_regex], max_length=18)
    email = models.EmailField(max_length=254)
    country = models.CharField(max_length=60)
    state = models.CharField(max_length=20, null=True)
    city = models.CharField(max_length=25)
    comments = models.CharField(max_length=200, blank=True, null=True)
    gpa = models.DecimalField(max_digits=3, decimal_places=2, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'phone_number', 'email', 'country', 'state', 'city']

    def get_full_name(self):
        return self.name
    def get_short_name(self):
        return self.name
    def __str__(self):
        return self.username

def user_directory_path(instance, filename):
    return 'resumes/user_{0}/{1}'.format(instance.username, filename)

class Resume(models.Model):
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=25, null=True)
    resume_file = models.FileField(upload_to=user_directory_path)

class Job(models.Model):
    title = models.CharField(max_length=70)
    company = models.CharField(max_length=160)
    description = models.TextField(null=True)
    salary_range = models.CharField(max_length=32, null=True)
    location = models.CharField(max_length=40)
    post_age = models.CharField(max_length=20)
    url = models.CharField(max_length=100, null=True)
    def __str__(self):
        return self.title

class SuitableJob(models.Model):
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    job_id = models.ForeignKey(Job, on_delete=models.CASCADE)
import datetime

from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text

class User(models.Model):
    username = models.CharField(max_length=30, blank=False)
    password = models.CharField(max_length=30, blank=False)
    name = models.CharField(max_length=50, blank=False)
    phone_regex = RegexValidator(regex=r'^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$', message="Phone number was entered incorrectly!")
    phone_number = models.CharField(validators=[phone_regex], max_length=18, blank=True)
    email = models.EmailField(max_length=254, blank=False)
    address = models.CharField(max_length=85, blank=False)
    comments = models.CharField(max_length=200, blank=True, null=True)  # blank=True -> not needed in forms
    gpa = models.DecimalField(max_digits=3, decimal_places=2, null=True)
    def __str__(self):
        return self.username

class Resume(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    resume_file = models.FileField(upload_to='resumes')

class Job(models.Model):
    title = models.CharField(max_length=70)
    company = models.CharField(max_length=160)
    description = models.TextField(null=True)
    salary_range = models.CharField(max_length=32, null=True)
    location = models.CharField(max_length=40)
    post_age = models.CharField(max_length=20)
    def __str__(self):
        return self.title

class Qualification(models.Model):
    description = models.CharField(max_length=200)
    job_id = models.ForeignKey(Job, on_delete=models.CASCADE)
    def __str__(self):
        return self.description

class SuitableJob(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    job_id = models.ForeignKey(Job, on_delete=models.CASCADE)
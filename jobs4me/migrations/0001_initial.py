# Generated by Django 3.1.6 on 2021-11-27 16:07

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=70)),
                ('company', models.CharField(max_length=160)),
                ('description', models.TextField(null=True)),
                ('salary_range', models.CharField(max_length=32, null=True)),
                ('location', models.CharField(max_length=40)),
                ('post_age', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=50)),
                ('phone_number', models.CharField(blank=True, max_length=18, validators=[django.core.validators.RegexValidator(message='Phone number was entered incorrectly!', regex='^(\\+\\d{1,2}\\s)?\\(?\\d{3}\\)?[\\s.-]\\d{3}[\\s.-]\\d{4}$')])),
                ('email', models.EmailField(max_length=254)),
                ('address', models.CharField(max_length=85)),
                ('comments', models.CharField(blank=True, max_length=200, null=True)),
                ('gpa', models.DecimalField(decimal_places=2, max_digits=3, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SuitableJob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs4me.job')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs4me.user')),
            ],
        ),
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resume_file', models.FileField(upload_to='resumes')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs4me.user')),
            ],
        ),
        migrations.CreateModel(
            name='Qualification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
                ('job_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs4me.job')),
            ],
        ),
    ]
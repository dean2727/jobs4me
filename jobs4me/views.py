from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import CreateUserForm, UploadResumeForm

import os
import csv
import shutil

from jobs4me.ML_NLP.extract_keyword import extractKeywords
from jobs4me.ML_NLP.extract_keyword_admin import getResumeKeywords
from jobs4me.ML_NLP.ML_matching import getSuitableJobs
from jobs4me.ML_NLP.job_scraper import scrapeJobs
from jobs4me.notifications.send_notif import *
from jobs4me.notifications.send_sms import *
from jobs4me.notifications.send_mail import *

# match resumes of current user to the top 5 highest chance jobs (scraped from Indeed), finding suitable jobs
def matchResumeToJobs(user, push_bullet_key):
    resume_list = 'jobs4me/user_csvs/user_' + str(user) + '/resumes_data.csv'
    getSuitableJobs(resume_list, str(user))

    i = 0
    path = 'jobs4me/user_csvs/user_' + str(user) + '/top_jobs_' + str(i) + '.csv'
    while os.path.exists(path):
        print(path)
        with open(path, newline='') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                candidate_jobs = Job.objects.filter(title=row['job title']).filter(company=row['company name'])
                for job in candidate_jobs:
                    # only add if job isnt already in SuitableJob table
                    if SuitableJob.objects.filter(job_id=job.id).exists():
                        continue
                    new_suitable_job = SuitableJob(
                        username=user,
                        job_id=job
                    )
                    new_suitable_job.save()

                    # notify user of new suitable job
                    sendSms(str(user), user.name, user.phone_number, row['match percentage'])
                    sendEmail(user.email,
                    "<body>" +
                        "<h3>Hi " + user.name + "!</h3>" +
                        "<p><b>We found a new job for you, which matched " + row['match percentage'] + "%" + " of your resumes! Here are some details:</b><p>" +
                        "<p><b>Title</b>: " + job.title + "</p>" +
                        "<p><b>Company</b>: " + job.company + "</p>" + 
                        "<p><b>Location</b>: " + job.location + "</p>" + 
                        "<p><b>URL</b>: " + job.url + "</p>" + 
                    "</body>"
                    )
                    if push_bullet_key:
                        sendPushBulletNotification(
                            str(user),
                            "New job from Jobs4Me!",
                            "Hi " + user.name + "! We found a new job for you, which matched " + row['match percentage'] + "%" + " of your resumes! Here are some details:\n" +
                            "Title: " + job.title + "\n" +
                            "Company: " + job.company + "\n" + 
                            "Location: " + job.location + "\n" + 
                            "URL: " + job.url,
                            push_bullet_key
                        )

        i += 1
        path = 'jobs4me/user_csvs/user_' + str(user) + '/top_jobs_' + str(i) + '.csv'


# write csv data for either all users (mode = "admin") or the logged in user (mode = "user")
def resumeDataToCsv(user, mode):
    if mode == "user":
        username = str(user)
        if os.path.exists('jobs4me/user_csvs/user_' + username):
            cmd = 'rm -rfv jobs4me/user_csvs/user_' + username
            os.system(cmd)
        
        cmd = 'mkdir -p jobs4me/user_csvs/user_' + username + '/resumes'
        os.system(cmd)

        fid = open('jobs4me/user_csvs/user_' + username + '/resumes_data.csv', 'w', newline='', encoding='utf-8')
        writer = csv.writer(fid)
        writer.writerow(['username', 'name', 'email', 'gpa', 'file_name', 'additional_comments'])

        resumes = Resume.objects.filter(username=user)
        for resume in resumes:
            file_name = str(resume.resume_file).split("/")[2]
            record = [username, user.name, user.email, user.gpa, file_name, user.comments]
            writer.writerow(record)

            src = str(resume.resume_file)
            dst = 'jobs4me/user_csvs/user_' + username + '/resumes'
            shutil.copy(src, dst)

        fid.close()

    elif mode == "admin":
        if os.path.exists('jobs4me/user_csvs'):
            cmd = 'rm -rfv jobs4me/user_csvs'
            os.system(cmd)
            os.mkdir('jobs4me/user_csvs')

        users = AppUser.objects.all()
        for user in users:
            username = user.username
            
            os.mkdir('jobs4me/user_csvs/user_' + username)
            os.mkdir('jobs4me/user_csvs/user_' + username + '/resumes')

            fid = open('jobs4me/user_csvs/user_' + username + '/resumes_data.csv', 'w', newline='', encoding='utf-8') 
            writer = csv.writer(fid)
            writer.writerow(['username', 'name', 'email', 'gpa', 'file_name', 'additional_comments'])

            resumes = Resume.objects.filter(username=user)
            for resume in resumes:
                file_name = str(resume.resume_file).split("/")[2]
                record = [user.username, user.name, user.email, user.gpa, file_name, comments]
                writer.writerow(record)

                src = str(resume.resume_file)
                dst = 'jobs4me/user_csvs/user_' + username + '/resumes'
                shutil.copy(src, dst)
            
            fid.close()

def adminTest(request):
    if not request.user.is_superuser:
        return redirect('jobs4me:login')

    if request.method == "POST":
        option = request.POST.get('option')
        if option == "scrape":
            # uncomment for demo
            job_types = ['robotics engineer', 'software engineer', 'machine learning', 'data science', 'electrical engineer']
            records = scrapeJobs(job_types)

            # uncomment for initial DB population
            # with open('jobs4me/ML_NLP/jobs.csv', newline='') as csv_file:
            #     reader = csv.DictReader(csv_file)
            #     for row in reader:
            #         new_job = Job(
            #             title=row['title'],
            #             company=row['company'],
            #             description=row['job_desc'],
            #             salary_range=row['salary'],
            #             location=row['location'],
            #             post_age=row['date_posted'],
            #             url=row['url']
            #         )
            #         new_job.save()

            # uncomment for future application
            # for r in records:
            #     new_job = Job(
            #         title=r[0],
            #         company=r[1],
            #         description=r[2],
            #         salary_range=r[3],
            #         location=r[4],
            #         post_age=r[5],
            #         url=r[6]
            #     )
            #     new_job.save()
        elif option == "job-extract":
            extractKeywords()
        elif option == "resume":
            matchResumeToJobs(request.user, '')
        elif option == "resumes-csv":
            resumeDataToCsv(request.user, "admin")
        elif option == "resumes-csv-user":
            resumeDataToCsv(request.user, "user")
        elif option == "send-email":
            sendEmail(request.user.email,
                "<body>" +
                    "<h3>Hi " + request.user.name + "!</h3>" +
                    "<p><b>We found a new job for you, which matched 88" + "%" + " of your resumes! Here are some details:</b><p>" +
                    "<p><b>Title</b>: Software Engineer I</p>" +
                    "<p><b>Company</b>: Chase Bank</p>" + 
                    "<p><b>Location</b>: Dallas, TX</p>" + 
                    "<p><b>URL</b>: https://www.google.com</p>" + 
                "</body>"
            )
        
        if request.POST.get('sms-number'):
            sendSms(
                str(request.user),
                request.user.name,
                request.POST['sms-number'],
                "88%"
            )
        if request.POST.get('push-bullet'):
            sendPushBulletNotification(
                str(request.user),
                "New job from Jobs4Me!",
                "Hi " + request.user.name + "! We found a new job for you, which matched 88" + "%" + " of your resumes! Here are some details:\n" +
                "Title: Software Engineer I\n" +
                "Company: Chase Bank\n" + 
                "Location: Dallas, TX\n" + 
                "URL: https://www.google.com",
                request.POST['push-bullet']
            )

    return render(request, 'jobs4me/admin_portal.html')

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('jobs4me:home')

    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('jobs4me:login')
        
    context = {'form': form}
    return render(request, 'jobs4me/register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('jobs4me:home')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('jobs4me:home')
        else:
            messages.error(request, 'Incorrect username or password!')

    return render(request, 'jobs4me/login.html')

def logoutUser(request):
    logout(request)
    return redirect('jobs4me:login')

# if user is not logged in, send them back to the login page
@login_required(login_url='jobs4me:login')
def home(request):
    if request.method == "POST":
        # user deleted resume
        if request.POST.get("delete-resume"):
            deleted_resume = Resume.objects.filter(resume_file=request.POST.get("delete-resume"))[0]
            deleted_resume.delete()

            # update directory/file data locations which contained that resume
            os.remove(str(deleted_resume.resume_file))
            resumeDataToCsv(request.user, "user")

            messages.success(request, 'Resume \'' + deleted_resume.name + '\' was deleted!')

        # user deleted job
        elif request.POST.get("delete-job"):
            items = request.POST.get("delete-job").split("~")
            title, company = items[0], items[1]
            deleted_jobs = Job.objects.filter(title=title).filter(company=company)
            for i in range(len(deleted_jobs)):
                deleted_suitable_job = SuitableJob.objects.filter(job_id=deleted_jobs[i])
                deleted_suitable_job.delete()

                messages.success(request, 'Removed recommended job!')

        # user uploaded new resume
        else:
            form = UploadResumeForm(request.POST, request.FILES)

            # resume is valid iff a resume was actually uploaded and the form that posted the request has enctype="multipart/form-data"
            if form.is_valid():
                resume = Resume(
                    username=request.user,
                    name=request.POST['name'],
                    resume_file=request.FILES['resume_file']
                )
                resume.save()

                resumeDataToCsv(request.user, "user")
                matchResumeToJobs(request.user, request.POST['push-bullet-key'])

                messages.success(request, 'Resume \'' + resume.name + '\' added!')
    
    # get customer info and resumes from db, put it in context to pass to page
    form = UploadResumeForm()
    user_name = request.user.name
    email = request.user.email
    phone_number = request.user.phone_number
    address = request.user.city + ", " + request.user.state + " " + request.user.country
    additional_comments = request.user.comments
    resumes = Resume.objects.filter(username=request.user)
    suitable_jobs = SuitableJob.objects.filter(username=request.user)

    context = {
        'form': form,
        'user_name': user_name,
        'email': email,
        'phone_number': phone_number,
        'address': address,
        'additional_comments': additional_comments,
        'resumes': resumes,
        'suitable_jobs': suitable_jobs,
        'is_super': request.user.is_superuser
    }
    return render(request, 'jobs4me/dashboard.html', context)
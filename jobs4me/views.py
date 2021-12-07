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

from jobs4me.ML_NLP import *
from jobs4me.notifications.send_sms import sendSms

# match resumes of current user to the jobs (scraped from Indeed), finding suitable jobs
def matchResumesToJobs(user):
    resumes = Resume.objects.filter(user=user)
    for resume in resumes:
        pass
    pass

# write csv data for either all users (mode = "admin") or the logged in user (mode = "user")
def resumeDataToCsv(user, mode):
    if mode == "user":
        username = str(user)
        if os.path.exists('jobs4me/user_csvs/user_' + username):
            cmd = 'rm -rfv jobs4me/user_csvs/user_' + username
            os.system(cmd)
        
        os.mkdir('jobs4me/user_csvs/user_' + username)
        os.mkdir('jobs4me/user_csvs/user_' + username + '/resumes')

        fid = open('jobs4me/user_csvs/user_' + username + '/resumes_data.csv', 'w', newline='', encoding='utf-8')
        writer = csv.writer(fid)
        writer.writerow(['username', 'name', 'email', 'gpa', 'file_name'])

        resumes = Resume.objects.filter(username=user)
        for resume in resumes:
            file_name = str(resume.resume_file).split("/")[2]
            record = [username, user.name, user.email, user.gpa, file_name]
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
            writer.writerow(['username', 'name', 'email', 'gpa', 'file_name'])

            resumes = Resume.objects.filter(username=user)
            for resume in resumes:
                file_name = str(resume.resume_file).split("/")[2]
                record = [user.username, user.name, user.email, user.gpa, file_name]
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
        print(option)
        if option == "scrape":
            records = []
            #records = add_job_records('robotics engineer', '', 20, records)
            for r in records:
                new_job = Job(
                    title=r[0],
                    company=r[1],
                    description=r[2],
                    salary_range=r[3],
                    location=r[4],
                    post_age=r[5],
                    url=r[6]
                )
                new_job.save()
        elif option == "resume":
            matchResumesToJobs(request.user)
        elif option == "sms-number":
            sendSms("Hello World!", request.POST['sms-number'])
        elif option == "resumes-csv":
            resumeDataToCsv(request.user, "admin")
        elif option == "resumes-csv-user":
            resumeDataToCsv(request.user, "user")
    return render(request, 'jobs4me/admin_test.html')

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

            # update directory/file data locations which contained that resumea
            os.remove(str(deleted_resume.resume_file))
            resumeDataToCsv(request.user, "user")

            messages.success(request, 'Resume \'' + deleted_resume.name + '\' was deleted!')

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

                messages.success(request, 'Resume \'' + resume.name + '\' added!')
    
    # get customer info and resumes from db, put it in context to pass to page
    # request.user should hold our username
    form = UploadResumeForm()
    user_name = request.user.name
    email = request.user.email
    phone_number = request.user.phone_number
    address = request.user.city + ", " + request.user.state + " " + request.user.country
    additional_comments = request.user.comments
    resumes = Resume.objects.filter(username=request.user)

    # try:
    #     getResumeKeywords(str(resumes[0].resume_file))
    # except IndexError:
    #     print("oof")
    #print(resumes[0].resume_file)

    context = {
        'form': form,
        'user_name': user_name,
        'email': email,
        'phone_number': phone_number,
        'address': address,
        'additional_comments': additional_comments,
        'resumes': resumes
    }
    return render(request, 'jobs4me/dashboard.html', context)
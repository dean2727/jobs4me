from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import CreateUserForm, UploadResumeForm
import os

from jobs4me.ML_NLP import *
from jobs4me.notifications.send_sms import sendSms

# match resumes of current user to the jobs (scraped from Indeed), finding suitable jobs
def matchResumesToJobs(user):
    resumes = Resume.objects.filter(user=user)
    for resume in resumes:
        pass
    pass

def adminTest(request):
    if not request.user.is_superuser:
        return redirect('jobs4me:login')

    if request.method == "POST":
        option = request.POST.get('option')
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
        else:
            sendSms("Hello World!", request.POST['sms-number'])
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
            os.remove(str(deleted_resume.resume_file))
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

                # save resume to the path specified in "upload_to"
                resume.save()

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
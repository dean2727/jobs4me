# Welcome to Jobs4Me!

Hosted website (may not be accessible now): https://jobs4me.azurewebsites.net/

Project report can be found [here](https://docs.google.com/document/d/1dTBu7sjGFyVFpETi7lRof6qgons0607J/edit?usp=sharing&ouid=118151331063501736585&rtpof=true&sd=true)

## What is the problem? And how does Jobs4Me address it?
Nowadays, as college students are often on the lookout for jobs/internships in their disciplines, they are often faced with difficulties finding such roles as well as dissatisfaction when they don’t get what they are looking for. Now, some of this could be attributed to mistakes, such as being unprepared for interviews or starting the search too late in the season. But, a lot of the dissatisfaction occurs because they apply to the wrong kind of jobs. Maybe the role demands a different skill set and another candidate with less experience/qualifications could be better suited for that specific job role. This problem is not just local to one student or a university but is widespread to all age groups of students, across all technical/non-technical fields and demographic boundaries.

There is a need for a resume matching system to be in place to give career recommendations and job matches based on GPA, skill sets, and projects/internship experiences derived from resumes of students, and Jobs4Me is a web application that functions to do just that!

## How it works
On landing, the user can register an account (including information such as email, name, phone number, and GPA) and/or log in. The user is then taken to the dashboard, where they can view/delete their uploaded resumes (if any) and view/remove previously recommended jobs. When the user uploads a resume, our machine learning matching algorithm is executed in the background for all of the resumes the user has uploaded so far. We retrieve job information from a database of jobs, scraped from Indeed, and extract the keywords of the users' resumes, and perform the matching on this information. Recommended jobs are then the top 5 most matched jobs, and the user can receive notifications via email, SMS, and/or push bullet, which contains basic information about each job, and a link to the original posting.

## Demo
![Demo](https://github.com/dean2727/jobs4me/demo.gif)

## Contributions
This project was developed by Souryendu Das and Dean Orenstein, 2 students in CSCE 489 (special topics: IoT) at Texas A&M University. Souryendu focused more on the NLP and ML backend, and Dean worked on the majority of the app and cloud development/set-up.

## Technical Details and Future Improvements
This is a Django web app, hosted on Azure, that uses a PostreSQL database. To send SMS messages, we used a communication service and phone number provided by Azure. To send an email, we registered a SendGrid sender key, which we hooked up to our TAMU email, so we can send user email notifications. To send Push Bullet notifications, the user simply needs to own an Android device and provide the Push Bullet key provided to them during the Push Bullet set-up. On the ML side, we first filter the job candidates based on the user's GPA (since some jobs require certain GPAs to even be considered). Then, we perform a cosine similarity on the job description and user information, as well as a Fuzzy Wuzzy similarity index between the relevant skillsets and user information. The match percentage for each job is then calculated, and we return the top 5 jobs for the user.

In the future, we would look to add useful features on the frontend, such as a loading bar/animation (the matching routine takes a few seconds), custom made artwork in the background, scaling for mobile use, environment variables for the API keys (so the user doesn't need to type them in every time), enhanced styling/better look and feel, an official navigation bar and/or sidebar, and better formatting of information. If this project were to be released to the public long term, we would want to greatly improve the ML side of things, as well as add asynchronous operations to pull jobs every x hours/days (which perhaps the user can decide), rather than running the ML matching right after the user uploads a resume. To elaborate, our ML only runs on a set number of 80-100 (now outdated) jobs on Indeed, and these jobs are limited to the computer science/electrical engineering/data science domains. We would want to find a way to automatically assign difficulty levels to the jobs (rather than hand labeling them), so we could pull thousands of jobs and get a much larger corpus of jobs that the user may be suitable in. Because the matching would take much longer if we did this, pulling at a set interval, without the user having to wait, and then notifying the user of jobs above some certain matching threshold (perhaps 80%) would be great.


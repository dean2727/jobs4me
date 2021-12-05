import csv
from datetime import datetime
import requests
# BeautifulSoup is to extract data from the HTML job postings
from bs4 import BeautifulSoup

# generate URL from job position and location
def get_url(position, location):
    # take care of any spaces or commas in the search terms (respectfully)
    position = position.replace(" ", "%20").replace(",", "%2C")
    location = location.replace(" ", "%20").replace(",", "%2C")
    template = 'https://www.indeed.com/jobs?q={}'
    if location != '':
        template += '&l={}'
        url = template.format(position, location)
    else:
        url = template.format(position)
        # print(url)
    return url

def get_job_info(card, atag):
    job_tables = card.find_all('table')

    # job header <table> has macro information like job title, location, and salary
    job_header_table = job_tables[0]
    # job description <table> has skills and job description
    job_description_table = job_tables[1]
    
    url = 'https://www.indeed.com' + atag.get('href')
    
    # job could be "new", in which case there is a <span> before the one we need
    spans = job_header_table.find('div', 'singleLineTitle').h2.find_all('span')
    if len(spans) == 1:
        title = spans[0].text.strip()
    else:
        title = spans[1].text.strip()
    
    company = job_header_table.find('span', 'companyName').text.strip()
    location = job_header_table.find('div', 'companyLocation').text.strip()
    # print(url)
    # print(title)
    # print(company)
    # print(location)
    
    # use the obtained url to make another search to the job posting, and pull out the job description from there
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        job_description = soup.find('div', {'id': 'jobDescriptionText'}).text
    except:
        job_description = ''

    post_age = job_description_table.find('span', 'date').text
    # print(post_age)
    
    try:
        salary = job_header_table.find('div', 'salary-snippet-container').find('div', 'attribute_snippet').text.strip()
    except:
        salary = ''
    # print(salary)
    
    record = (title, company, job_description, salary, location, post_age, url)
    return record

# retrieve n jobs from indeed.com for a certain job position and location
def add_job_records(position, location, n, records):
    url = get_url(position, location)
    num_records = 0
    while True:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        url_container = soup.find('div', 'mosaic-provider-jobcards')
        cards = soup.find_all('div', 'job_seen_beacon')
        atags = url_container.find_all('a')
        
        # filter tags for job postings (are there any divs embedded in the <a> tag?)
        valid_tags = []
        for tag in atags:
            tag_divs = tag.find_all('div')
            if len(tag_divs) > 0:
                valid_tags.append(tag)

        for i in range(len(cards)):
            record = get_job_info(cards[i], valid_tags[i])
            records.append(record)
            num_records += 1
            if num_records == n:
                return records
            
        # exception occurs if this was the last page
        try:
            url = 'https://www.indeed.com' + soup.find('a', {'aria-label': 'Next'}).get('href')
        except AttributeError:
            return records
    
'''
records = []
records = add_job_records('robotics engineer', '', 20, records)
#records = add_job_records('robotics engineer', 'dallas tx', 20, records)
records = add_job_records('software engineer', '', 20, records)
records = add_job_records('electrical engineer', '', 20, records)
records = add_job_records('data science', '', 20, records)
records = add_job_records('machine learning', '', 20, records)

print("100 jobs from all over the US:")
print("1st batch of 20 = \'robotics engineer\'")
print("2nd batch of 20 = \'software engineer\'")
print("3rd batch of 20 = \'electrical engineer\'")
print("4th batch of 20 = \'data science engineer\'")
print("5th batch of 20 = \'machine learning\'")
i = 1
for r in records:
    print("~~~~~~~~~~~~~~~~~~~ JOB " + str(i) + " - " + r[0] + " ~~~~~~~~~~~~~~~~~~~~~")
    #company, job_description, salary, location, post_age, url)
    print("Company: " + r[1])
    print("Job description: " + r[2])
    print("Salary: " + r[3])
    print("Location: " + r[4])
    print("Posted: " + r[5])
    print("URL: " + r[6])
    i += 1
'''
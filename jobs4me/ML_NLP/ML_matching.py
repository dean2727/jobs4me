import os
import sys
import csv
import numpy as np
import pandas as pd
from fuzzywuzzy import process
from pdfminer.high_level import extract_text
from gensim.summarization.summarizer import summarize
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from gensim.summarization.textcleaner import split_sentences

from jobs4me.models import *

def unique_sentence(seq):
    seen = set()
    return [x for x in seq if x not in seen and not seen.add(x)]

def summary(x, perc):
    if len(split_sentences(x)) > 10:
        test_summary = summarize(x, ratio = perc, split=True)
        test_summary = '\n'.join(map(str, unique_sentence(test_summary)))
    else:
        test_summary = x
    return test_summary

def getSuitableJobs(resume_list, username):
    jobs_list = "jobs4me/ML_NLP/jobs_extracted.csv"
    resume_list_data = pd.read_csv(resume_list)
    email_array = resume_list_data[{'name', 'email', 'gpa', 'file_name'}].to_numpy()
    projectDict = {}
    element = 0
    # os.system("rm -rfv recommendation_output")
    # os.system("mkdir recommendation_output")
    for entry in email_array:
        jobs_list_data = pd.read_csv(jobs_list)
        for column in entry:
            if str(column).find(".pdf") != -1:
                file_location = 'jobs4me/user_csvs/user_' + username + '/resumes/' + str(column)
                resume = extract_text(file_location)
                text_resume = str(resume)
                summarize(text_resume, ratio=1)
            if str(column).find("@") != -1:
                email = str(column)
            try:
                float(column)
                if float(column) >= 3.5:
                    jobs_list_data1 = jobs_list_data.loc[(jobs_list_data['Competitiveness'] == 'Very High') | (jobs_list_data['Competitiveness'] == 'High') | (jobs_list_data['Competitiveness'] == 'Medium')]
                elif float(column) >= 2.5:
                    jobs_list_data1 = jobs_list_data.loc[(jobs_list_data['Competitiveness'] == 'High') | (jobs_list_data['Competitiveness'] == 'Medium')]
                else:
                    jobs_list_data1 = jobs_list_data.loc[(jobs_list_data['Competitiveness'] == 'Medium')]
            except ValueError:
                print("")

        desc_data = pd.array(jobs_list_data1['Description'])
        keyword_data = pd.array(jobs_list_data1['Keywords'])
        match_per_array = []

        #cosine similarity part
        for i in range(0, len(desc_data)):
            text = str(desc_data[i])
            text = summary(text, i)
            text_list = [text_resume, text]
            cv = CountVectorizer()
            count_matrix = cv.fit_transform(text_list)
            matchPercentage = cosine_similarity(count_matrix)[0][1] * 100
            matchPercentage = round(matchPercentage, 2)
            match_per_array.append(matchPercentage)

        #fuzzywuzzy algorithm part
        str_to_match = text_resume
        str_options = keyword_data
        ratios = process.extract(str_to_match, str_options)

        jobs_list_data1['match percentage'] = match_per_array
        jobs_list_data1 = jobs_list_data1.sort_values(by=['match percentage'])
        jobs_list_data2 = jobs_list_data1.copy()

        jobs_list_data2_array = np.array(jobs_list_data2)
        ratios = np.array(ratios)
        num_rows, num_columns = ratios.shape
        jobs_list_data_rows, jobs_list_data_columns = jobs_list_data2.shape
        index = []

        for i in range(jobs_list_data_rows):
            for j in range(num_rows):
                if jobs_list_data2_array[i][2] == ratios[j][-1]:
                    match_percent = jobs_list_data2_array[i]['match percentage']
                    jobs_list_data2_array[i]['match percentage'] = match_percent + float(ratios[j][-1])
        jobs_list_data2 = pd.DataFrame(jobs_list_data2_array)
        jobs_list_data2 = jobs_list_data2.sort_values(ascending=False, by=[5])
        jobs_list_data2 = jobs_list_data2.head(5)
        answer_array = np.array(jobs_list_data2)

        # write the top jobs to the user's csv directory
        write_filename = "jobs4me/user_csvs/user_" + username + "/top_jobs.csv"
        fields = ['job title', 'company name', 'keywords', 'competitiveness', 'description', 'match percentage']
        with open(write_filename, 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(fields)
            csvwriter.writerows(answer_array)
        csvfile.close()
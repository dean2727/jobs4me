import sys
import csv
  
def extractKeywords():
    # csv of jobs scraped from indeed
    read_filename = "jobs4me/ML_NLP/jobs.csv"
    # where to put the file of extracted job data
    write_filename = "jobs4me/ML_NLP/jobs_extracted.csv"
    
    fields = []
    rows = []
    write_fields = ['Job Title', 'Company Name', 'Keywords', 'Competitiveness', 'Description']
    write_rows = []
    
    with open(read_filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        fields = next(csvreader)
        for row in csvreader:
            rows.append(row)
        print("Total no. of rows parsed: %d"%(csvreader.line_num))
    
    with open(write_filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(write_fields)
        for row in rows:
            csvwriter.writerow([row[0], row[1], row[3], row[4], row[2]])

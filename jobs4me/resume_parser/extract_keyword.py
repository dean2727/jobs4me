import sys
import csv
  
read_filename = sys.argv[1]
write_filename = sys.argv[2]
  
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
csvfile.close()
  
with open(write_filename, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(write_fields)
    for row in rows:
        csvwriter.writerow([row[0], row[1], row[3], row[4], row[2]])
csvfile.close()

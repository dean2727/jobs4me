import os
import sys
import spacy
from pdfminer.high_level import extract_text

n = len(sys.argv)
resume_file = sys.argv[1]

name = os.path.join(resume_file)
text = extract_text(name)

nlp = spacy.load("en_core_web_lg")
doc = nlp(text)

for entry in doc.ents:
	print(entry.text, entry.label_)

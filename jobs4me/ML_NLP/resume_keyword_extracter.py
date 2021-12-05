import os
import sys
import spacy
from pdfminer.high_level import extract_text

def getResumeKeywords(resume_file_path):
    name = os.path.join(resume_file_path)
    text = extract_text(name)

    nlp = spacy.load("en_core_web_lg")
    doc = nlp(text)

    for entry in doc.ents:
        print(entry.text, entry.label_)

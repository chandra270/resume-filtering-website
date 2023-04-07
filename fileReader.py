from operator import index
from pandas._config.config import options
import textract as tx
import pandas as pd
import os
import re
import json
import csv
import textract
import PyPDF2

resume_dir = "Data/Resumes/"
job_desc_dir = "Data/JobDesc/"
resume_names = os.listdir(resume_dir)
job_description_names = os.listdir(job_desc_dir)

document = []

def read_resumes(list_of_resumes, resume_directory):
    placeholder = []
    for res in list_of_resumes:
        temp = []
        temp.append(res)
        file_ext = os.path.splitext(res)[1]
        if file_ext == ".docx":
            text = textract.process(os.path.join(resume_directory, res), encoding='ascii')
            text = str(text, 'utf-8')
        elif file_ext == ".pdf":
            with open(os.path.join(resume_directory, res), 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                text = ""
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text()
        else:
            continue
        temp.append(text)
        placeholder.append(temp)
    return placeholder


document = read_resumes(resume_names, resume_dir)

def get_cleaned_words_resume(document, skills_db_file, output_file):
    # Load skills from JSON file
    with open(skills_db_file, 'r') as f:
        skills = json.load(f)

    # Create a CSV file to write the results
    with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Name', 'Context', 'Skills', 'Email'])

        # Iterate over each document
        for i in range(len(document)):
            context = document[i][1].lower()
            skills_found = []

            # Iterate over each skill
            for skill in skills.values():
                skill_name = skill['skill_name'].lower()
                if skill_name in context:
                    skills_found.append(skill_name)

            # Extract email using regular expressions
            email = re.findall(r'\S+@\S+', context)
            email = email[0] if len(email) > 0 else ""

            # Write the results to the CSV file
            writer.writerow([document[i][0], document[i][1], ', '.join(skills_found), email])

    # Close the CSV file
    csvfile.close()

    return document

def get_cleaned_words_jobs(document, skills_db_file, output_file):
    # Load skills from JSON file
    with open(skills_db_file, 'r') as f:
        skills = json.load(f)

    # Create a CSV file to write the results
    with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Name', 'Context', 'Skills'])

        # Iterate over each document
        for i in range(len(document)):
            context = document[i][1].lower()
            skills_found = []

            # Iterate over each skill
            for skill in skills.values():
                skill_name = skill['skill_name'].lower()
                if skill_name in context:
                    skills_found.append(skill_name)

            # Write the results to the CSV file
            writer.writerow([document[i][0], document[i][1], ', '.join(skills_found)])

    # Close the CSV file
    csvfile.close()

    return document

skills_db_file = 'skill_db_relax_20.json'
output_file = 'Resume_Data.csv'
j_output_file = 'Job_Data.csv'

Doc = get_cleaned_words_resume(document, skills_db_file, output_file)

def read_jobdescriptions(job_description_names, job_desc_dir):
    placeholder = []
    for tes in job_description_names:
        temp = []
        temp.append(tes)
        text = tx.process(job_desc_dir+tes, encoding='ascii')
        text = str(text, 'utf-8')
        temp.append(text)
        placeholder.append(temp)
    return placeholder


job_document = read_jobdescriptions(job_description_names, job_desc_dir)

Jd = get_cleaned_words_jobs(job_document, skills_db_file, j_output_file)

from operator import index
from pandas._config.config import options
import Cleaner
import textract as tx
import pandas as pd
import os
import tf_idf
import re

resume_dir = "Data/Resumes/"
job_desc_dir = "Data/JobDesc/"
resume_names = os.listdir(resume_dir)
job_description_names = os.listdir(job_desc_dir)

document = []


import textract
import PyPDF2

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


def get_cleaned_words_resume(document):
    for i in range(len(document)):
        raw = Cleaner.Cleaner(document[i][1])
        document[i].append(" ".join(raw[0]))
        document[i].append(" ".join(raw[1]))
        document[i].append(" ".join(raw[2]))
        # Extract email
        email = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', document[i][1])
        document[i].append(email[0] if len(email) > 0 else '')
        sentence = tf_idf.do_tfidf(document[i][3].split(" "))
        document[i].append(sentence)
        # Reorder the columns to have email as the last column
        document[i] = document[i][:-2] + [document[i][-1], document[i][-2]]
    return document

def get_cleaned_words_jobs(document):
    for i in range(len(document)):
        raw = Cleaner.Cleaner(document[i][1])
        document[i].append(" ".join(raw[0]))
        document[i].append(" ".join(raw[1]))
        document[i].append(" ".join(raw[2]))
        sentence = tf_idf.do_tfidf(document[i][3].split(" "))
        document[i].append(sentence)
    return document

Doc = get_cleaned_words_resume(document)

Database = pd.DataFrame(document, columns=[
                        "Name", "Context", "Cleaned", "Selective", "Selective_Reduced", "TF_Based", "Email"])

Database.to_csv("Resume_Data.csv", index=False)

# Database.to_json("Resume_Data.json", index=False)


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

Jd = get_cleaned_words_jobs(job_document)

jd_database = pd.DataFrame(Jd, columns=[
                           "Name", "Context", "Cleaned", "Selective", "Selective_Reduced", "TF_Based"])

jd_database.to_csv("Job_Data.csv", index=False)


# from operator import index
# from pandas._config.config import options
# import Cleaner
# import textract as tx
# import pandas as pd
# import os
# import tf_idf

# resume_dir = "Data/Resumes/"
# job_desc_dir = "Data/JobDesc/"
# resume_names = os.listdir(resume_dir)
# job_description_names = os.listdir(job_desc_dir)

# document = []


# import textract
# import PyPDF2

# def read_resumes(list_of_resumes, resume_directory):
#     placeholder = []
#     for res in list_of_resumes:
#         temp = []
#         temp.append(res)
#         file_ext = os.path.splitext(res)[1]
#         if file_ext == ".docx":
#             text = textract.process(os.path.join(resume_directory, res), encoding='ascii')
#             text = str(text, 'utf-8')
#         elif file_ext == ".pdf":
#             with open(os.path.join(resume_directory, res), 'rb') as pdf_file:
#                 pdf_reader = PyPDF2.PdfReader(pdf_file)
#                 text = ""
#                 for page_num in range(len(pdf_reader.pages)):
#                     page = pdf_reader.pages[page_num]
#                     text += page.extract_text()
#         else:
#             continue
#         temp.append(text)
#         placeholder.append(temp)
#     return placeholder


# document = read_resumes(resume_names, resume_dir)


# def get_cleaned_words(document):
#     for i in range(len(document)):
#         raw = Cleaner.Cleaner(document[i][1])
#         document[i].append(" ".join(raw[0]))
#         document[i].append(" ".join(raw[1]))
#         document[i].append(" ".join(raw[2]))
#         sentence = tf_idf.do_tfidf(document[i][3].split(" "))
#         document[i].append(sentence)
#     return document


# Doc = get_cleaned_words(document)

# Database = pd.DataFrame(document, columns=[
#                         "Name", "Context", "Cleaned", "Selective", "Selective_Reduced", "TF_Based"])

# Database.to_csv("Resume_Data.csv", index=False)

# # Database.to_json("Resume_Data.json", index=False)


# def read_jobdescriptions(job_description_names, job_desc_dir):
#     placeholder = []
#     for tes in job_description_names:
#         temp = []
#         temp.append(tes)
#         text = tx.process(job_desc_dir+tes, encoding='ascii')
#         text = str(text, 'utf-8')
#         temp.append(text)
#         placeholder.append(temp)
#     return placeholder


# job_document = read_jobdescriptions(job_description_names, job_desc_dir)

# Jd = get_cleaned_words(job_document)

# jd_database = pd.DataFrame(Jd, columns=[
#                            "Name", "Context", "Cleaned", "Selective", "Selective_Reduced", "TF_Based"])

# jd_database.to_csv("Job_Data.csv", index=False)
import os
import csv
import pandas as pd
import Cleaner
import PyPDF2
import tf_idf

# Specify the directory where the PDF files are located
pdf_directory = 'Data/Resumes/pdf'

# Create a CSV file to store the converted data
csv_file = 'pdf_data.csv'

# Open the CSV file in write mode

with open(csv_file, 'w',encoding='utf-8', newline='') as file:
    writer = csv.writer(file)

    # Write the header row to the CSV file
    writer.writerow(['File Name', 'Text'])

    # Iterate over the PDF files in the directory
    for filename in os.listdir(pdf_directory):
        if filename.endswith('.pdf'):
            # Open the PDF file
            pdf_file = open(os.path.join(pdf_directory, filename), 'rb')
            pdf_reader = PyPDF2.PdfReader(pdf_file)

            # Extract the text from each page of the PDF file
            text = ''
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()

            # Write the filename and text to the CSV file
            writer.writerow([filename, text])

            # Close the PDF file
            pdf_file.close()

def get_cleaned_words(document):
    for i in range(len(document)):
        raw = Cleaner.Cleaner(document[i][1])
        document[i].append(" ".join(raw[0]))
        document[i].append(" ".join(raw[1]))
        document[i].append(" ".join(raw[2]))
        sentence = tf_idf.do_tfidf(document[i][3].split(" "))
        document[i].append(sentence)
    return document

# Specify the path of the input CSV file
csv_file = 'pdf_data.csv'

# Load the CSV file into a Pandas dataframe
df = pd.read_csv(csv_file)

# Clean the text and store the results in a new dataframe
cleaned_df = get_cleaned_words(df.values.tolist())
cleaned_df = pd.DataFrame(cleaned_df, columns=[
                        "Name", "Context", "Cleaned", "Selective", "Selective_Reduced", "TF_Based"])

# Save the cleaned data to a new CSV file
cleaned_csv_file = 'cleaned_pdf_data.csv'
cleaned_df.to_csv(cleaned_csv_file, index=False)

import os
import csv
import PyPDF2

# Specify the directory where the PDF files are located
pdf_directory = 'Data/Resumes/'

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

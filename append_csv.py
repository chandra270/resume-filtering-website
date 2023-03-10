import pandas as pd

# Load the contents of the first file into a DataFrame
df1 = pd.read_csv('Resume_Data.csv')

# Load the contents of the second file into another DataFrame
df2 = pd.read_csv('cleaned_pdf_data.csv')

# Append the second DataFrame to the first one
df1 = df1.append(df2)

# Write the merged DataFrame back to a new CSV file
df1.to_csv('merged.csv', index=False)

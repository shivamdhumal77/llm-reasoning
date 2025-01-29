import pandas as pd
import os

# Function to extract text from an Excel (.xls, .xlsx) file
def extract_text_from_excel(excel_file_path):
    # Read the Excel file
    df = pd.read_excel(excel_file_path, sheet_name=None)  # sheet_name=None reads all sheets
    text = ""
    
    # Iterate through each sheet and add the content
    for sheet_name, sheet_data in df.items():
        text += f"Sheet: {sheet_name}\n"
        text += sheet_data.to_string(index=False)  # Convert the sheet to text (without the index)
        text += "\n\n"
    
    return text

# Function to extract text from a CSV file
def extract_text_from_csv(csv_file_path):
    df = pd.read_csv(csv_file_path)
    text = df.to_string(index=False)  # Convert the CSV content to text
    return text

# Function to extract text from both Excel and CSV files
def extract_text_from_excel_or_csv(file_path):
    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension in ['.xls', '.xlsx']:
        return extract_text_from_excel(file_path)
    elif file_extension == '.csv':
        return extract_text_from_csv(file_path)
    else:
        raise ValueError("Unsupported file type. Please upload an Excel (.xls, .xlsx) or CSV (.csv) file.")

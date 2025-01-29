import os
from docx import Document
import win32com.client

# Function to extract text from a .docx file
def extract_text_from_docx(docx_file_path):
    doc = Document(docx_file_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

# Function to extract text from a .doc file (requires pywin32 on Windows)
def extract_text_from_doc(doc_file_path):
    # Initialize Word application
    word = win32com.client.Dispatch("Word.Application")
    doc = word.Documents.Open(doc_file_path)
    text = doc.Content.Text
    doc.Close()
    word.Quit()
    return text

# Function to extract text from both .docx and .doc files
def extract_text_from_word_file(file_path):
    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension == '.docx':
        return extract_text_from_docx(file_path)
    elif file_extension == '.doc':
        return extract_text_from_doc(file_path)
    else:
        raise ValueError("Unsupported file type. Please upload a .doc or .docx file.")

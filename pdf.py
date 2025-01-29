from PyPDF2 import PdfReader

def pdf_read(pdf_file):
    """
    Reads and extracts text from a PDF file.

    Args:
    - pdf_file (str): Path to the PDF file.

    Returns:
    - str: Extracted text from the PDF file.
    """
    try:
        text = ""
        # Open the PDF file
        pdf_reader = PdfReader(pdf_file)
        
        # Loop through the pages and extract text
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        return text
    except Exception as e:
        return f"An error occurred while reading the PDF file: {e}"

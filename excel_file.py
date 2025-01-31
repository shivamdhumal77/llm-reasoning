from langchain.document_loaders import UnstructuredExcelLoader
import pandas as pd

def extract_text_from_excel(file_path):
    """Extract both text and tabular data from Excel files"""
    try:
        # First try unstructured loading for text and tables
        loader = UnstructuredExcelLoader(file_path, mode="elements")
        unstructured_docs = loader.load()
        text_content = " ".join([doc.page_content for doc in unstructured_docs])

        # Then use pandas for structured data fallback
        df = pd.read_excel(file_path, engine='openpyxl')
        pandas_content = "\n".join([df.to_string() for _, df in df.items() if isinstance(df, pd.DataFrame)])

        return f"{text_content}\n{pandas_content}"
    
    except Exception as e:
        return f"Error processing Excel file: {str(e)}"
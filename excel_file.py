import pandas as pd
import openpyxl  # Explicitly importing openpyxl

def extract_text_from_excel(file_path):
    """Extract text and structured tabular data from an Excel file."""
    try:
        # Read all sheets from the Excel file
        dataframes = pd.read_excel(file_path, sheet_name=None, engine='openpyxl')
        structured_text = []

        for sheet_name, df in dataframes.items():
            structured_text.append(f"\nSheet: {sheet_name}\n" + "-"*50)
            
            # Convert DataFrame rows to text format
            structured_text.extend([" | ".join(map(str, row.values)) for _, row in df.iterrows()])

        return "\n".join(structured_text)
    
    except Exception as e:
        return f"Error processing Excel file: {str(e)}"

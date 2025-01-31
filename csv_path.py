import csv

def extract_stock_data(file_path):
    """
    Reads stock data from a CSV file and returns it as formatted text.
    
    :param file_path: Path to the CSV file
    :return: List of formatted text rows
    """
    extracted_data = []
    
    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        headers = next(reader)  # Extract column names

        for i, row in enumerate(reader):
            row_data = [f"{headers[j]}: {row[j]}" for j in range(len(headers))]
            extracted_data.append(" | ".join(row_data))  # Append as a single text line
    
    return extracted_data  # Return all formatted text lines

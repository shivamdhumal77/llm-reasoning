from bs4 import BeautifulSoup

# Function to extract text from an HTML file
def extract_text_from_html(html_file_path):
    try:
        with open(html_file_path, 'r', encoding='utf-8') as file:
            # Parse the HTML file using BeautifulSoup
            soup = BeautifulSoup(file, 'html.parser')
            
            # Extract text from the HTML file, removing all HTML tags
            text = soup.get_text()
        return text
    except Exception as e:
        return f"Error reading the file: {e}"

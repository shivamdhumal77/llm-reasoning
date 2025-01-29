import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    """
    Scrapes the text content from a webpage and returns the main text.

    Args:
    - url (str): The URL of the webpage to scrape.

    Returns:
    - str: Extracted text from the webpage.
    """
    try:
        # Send HTTP GET request to fetch webpage content
        response = requests.get(url)
        response.raise_for_status()  # Ensure we got a valid response (status code 200)

        # Parse the content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract all the paragraphs or relevant content
        paragraphs = soup.find_all('p')  # Adjust to target specific elements if needed
        text = ' '.join([para.get_text() for para in paragraphs])

        return text

    except requests.exceptions.RequestException as req_err:
        return f"Request error: {req_err}"
    except Exception as e:
        return f"An error occurred: {e}"

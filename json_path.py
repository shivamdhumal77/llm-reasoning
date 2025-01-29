import json

# Function to read and extract text from JSON files
def json_read(json_file_path):
    """
    This function extracts and returns text from a JSON file.
    The JSON content is converted to a string representation for further use.
    """
    text = ""
    try:
        with open(json_file_path, 'r') as json_file:
            # Parse the JSON content
            data = json.load(json_file)
            
            # Convert the JSON content into a string representation
            text = json.dumps(data, indent=2)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error reading JSON: {e}")
    return text

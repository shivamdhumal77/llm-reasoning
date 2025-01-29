import os

def extract_text_from_file(file_path):
    """
    Extracts text content from various programming language files.

    Args:
    - file_path (str): Path to the file.

    Returns:
    - str: Extracted text content or an error message.
    """
    # Get the file extension
    file_extension = os.path.splitext(file_path)[1].lower()

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Supported programming language file extensions
        supported_extensions = [
            '.c', '.cpp', '.py', '.dart', '.java', 
            '.js', '.css', '.php', '.xml'
        ]

        if file_extension in supported_extensions:
            return content
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")

    except FileNotFoundError:
        return f"Error: The file '{file_path}' was not found."
    except PermissionError:
        return f"Error: Permission denied for file '{file_path}'."
    except UnicodeDecodeError:
        return f"Error: Unable to decode the content of the file '{file_path}'."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

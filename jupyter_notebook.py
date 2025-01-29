import nbformat

def extract_text_from_notebook(notebook_path):
    """
    Extracts both markdown and code text from a Jupyter Notebook (.ipynb).
    """
    try:
        with open(notebook_path, 'r', encoding='utf-8') as file:
            notebook = nbformat.read(file, as_version=4)

        extracted_text = []

        for cell in notebook.cells:
            if cell.cell_type == "markdown":
                extracted_text.append("\n".join(cell.source))  # Extract Markdown text
            elif cell.cell_type == "code":
                extracted_text.append("```python\n" + "\n".join(cell.source) + "\n```")  # Extract code

        return "\n\n".join(extracted_text)

    except Exception as e:
        return f"Error processing notebook: {e}"

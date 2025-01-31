import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.schema import Document
from langchain_openai import ChatOpenAI

# Import all extractor functions from separate modules
from html_file import extract_text_from_html
from json_path import json_read
from mkv_file import extract_audio_and_transcribe
from mp3 import extract_text_from_mp3
from pdf import pdf_read
from powerpoint import extract_text_from_ppt_file
from programming_languages import extract_text_from_file as extract_text_from_code_file
from scrape_script import scrape_website
from word import extract_text_from_word_file
from jupyter_notebook import extract_text_from_notebook
from csv_path import extract_stock_data
from excel_file import extract_text_from_excel  # New Excel import

# Initialize ChatOpenAI models
llm_1 = ChatOpenAI(
    api_key="ollama",
    base_url="https://sunny-gerri-finsocialdigitalsystem-d9b385fa.koyeb.app/v1",
    model="athene-v2"
)

llm_2 = ChatOpenAI(
    api_key="ollama",
    base_url="https://sunny-gerri-finsocialdigitalsystem-d9b385fa.koyeb.app/v1",
    model="athene-v2"
)

huggingface_embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def generate_text(prompt):
    try:
        return llm_1.predict(prompt)
    except Exception as e:
        print(f"Error with first model: {e}")
        try:
            return llm_2.predict(prompt)
        except Exception as e:
            return "Failed to generate an answer."

def get_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return text_splitter.split_text(text)

def create_vector_store(chunks):
    docs = [Document(page_content=chunk) for chunk in chunks]
    return FAISS.from_documents(docs, huggingface_embeddings)

def extract_text_from_file(file_path):
    try:
        if isinstance(file_path, list):  
            file_path = " ".join(file_path)
        
        if isinstance(file_path, str) and file_path.startswith(("http://", "https://")):
            return scrape_website(file_path)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file or path '{file_path}' does not exist.")

        file_extension = os.path.splitext(file_path)[1].lower()
        
        extractor_map = {
            '.csv': extract_stock_data,
            '.xlsx': extract_text_from_excel,
            '.xls': extract_text_from_excel,
            '.html': extract_text_from_html,
            '.json': json_read,
            '.mkv': extract_audio_and_transcribe,
            '.mp3': extract_text_from_mp3,
            '.pdf': pdf_read,
            '.ppt': extract_text_from_ppt_file,
            '.pptx': extract_text_from_ppt_file,
            '.doc': extract_text_from_word_file,
            '.docx': extract_text_from_word_file,
            '.ipynb': extract_text_from_notebook,
        }

        if file_extension in extractor_map:
            extracted_data = extractor_map[file_extension](file_path)
        elif file_extension in ['.c', '.cpp', '.py', '.dart', '.java', '.js', '.css', '.php', '.xml']:
            extracted_data = extract_text_from_code_file(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}.")

        return " ".join(extracted_data) if isinstance(extracted_data, list) else extracted_data
    
    except Exception as e:
        return f"Error extracting text: {e}"

def generate_answer(query, retriever):
    try:
        relevant_docs = retriever.get_relevant_documents(query)
        context = " ".join([doc.page_content for doc in relevant_docs])
        return generate_text(f"Context: {context}\n\nQuestion: {query}\n\nAnswer:")
    except Exception as e:
        return f"Failed to generate an answer. Error: {e}"

def main():
    print("Select an option:")
    print("1. Text Analysis")
    print("2. Exit")
    
    choice = input("Enter your choice: ")
    if choice == "1":
        file_path = input("Enter file path or URL: ")
        extracted_text = extract_text_from_file(file_path)
        
        if extracted_text.startswith("Error"):
            print(extracted_text)
            return
        
        text_chunks = get_chunks(extracted_text)
        vector_store = create_vector_store(text_chunks)
        retriever = vector_store.as_retriever()
        
        query = input("Ask a question about the document: ")
        if query:
            response = generate_answer(query, retriever)
            print("Answer:", response)
    
    elif choice == "2":
        print("Exiting...")
        exit()
    
if __name__ == "__main__":
    main()

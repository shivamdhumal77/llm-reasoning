import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.schema import Document
from langchain_openai import ChatOpenAI
from PIL import Image

from excel import extract_text_from_excel_or_csv
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
    except Exception:
        return llm_2.predict(prompt)

def get_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return text_splitter.split_text(text)

def create_vector_store(chunks):
    docs = [Document(page_content=chunk) for chunk in chunks]
    return FAISS.from_documents(docs, huggingface_embeddings)

def extract_text_from_file(file_path):
    if file_path.startswith(("http://", "https://")):
        return scrape_website(file_path)
    
    if not os.path.exists(file_path):
        return f"File not found: {file_path}"
    
    file_extension = os.path.splitext(file_path)[1].lower()
    extractors = {
        '.xls': extract_text_from_excel_or_csv, '.xlsx': extract_text_from_excel_or_csv, '.csv': extract_text_from_excel_or_csv,
        '.html': extract_text_from_html, '.json': json_read, '.mkv': extract_audio_and_transcribe,
        '.mp3': extract_text_from_mp3, '.pdf': pdf_read, '.ppt': extract_text_from_ppt_file, '.pptx': extract_text_from_ppt_file,
        '.c': extract_text_from_code_file, '.cpp': extract_text_from_code_file, '.py': extract_text_from_code_file,
        '.dart': extract_text_from_code_file, '.java': extract_text_from_code_file, '.js': extract_text_from_code_file,
        '.css': extract_text_from_code_file, '.php': extract_text_from_code_file, '.xml': extract_text_from_code_file,
        '.doc': extract_text_from_word_file, '.docx': extract_text_from_word_file, '.ipynb': extract_text_from_notebook
    }
    
    return extractors.get(file_extension, lambda x: f"Unsupported file type: {file_extension}")(file_path)

def analyze_image(file_path, user_prompt):
    if not os.path.exists(file_path):
        return f"File not found: {file_path}"
    
    try:
        Image.open(file_path).verify()
    except Exception:
        return "Invalid image file."
    
    if not user_prompt:
        return "Please provide a description or question related to the image."
    
    llm_vision = ChatOpenAI(
        api_key="ollama",
        base_url="https://sunny-gerri-finsocialdigitalsystem-d9b385fa.koyeb.app/v1",
        model="llama3.2-vision"
    )
    return llm_vision.predict(f"Analyze the image and respond to this prompt: {user_prompt}")

def generate_answer(query, retriever):
    try:
        context = " ".join([doc.page_content for doc in retriever.get_relevant_documents(query)])
        return generate_text(f"Context: {context}\n\nQuestion: {query}\n\nAnswer:")
    except Exception as e:
        return f"Error generating answer: {e}"

def main():
    print("Choose an option:")
    print("1. Text Analysis")
    print("2. Image Analysis")
    choice = input("Enter choice (1/2): ")
    
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
        print("Answer:", generate_answer(query, retriever))
    
    elif choice == "2":
        file_path = input("Enter image file path: ")
        user_prompt = input("Enter a prompt for the image: ")
        print("Result:", analyze_image(file_path, user_prompt))
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()

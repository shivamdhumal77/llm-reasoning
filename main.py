import os
import streamlit as st
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
from jupyter_notebook import extract_text_from_notebook  # Fixed import

# Initialize the ChatOpenAI instances for different models
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
        response = llm_1.predict(prompt)
        return response
    except Exception as e:
        print(f"Error with first model: {e}")
        try:
            response = llm_2.predict(prompt)
            return response
        except Exception as e:
            return "Failed to generate an answer."

def get_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return text_splitter.split_text(text)

def create_vector_store(chunks):
    docs = [Document(page_content=chunk) for chunk in chunks]
    vector_store = FAISS.from_documents(docs, huggingface_embeddings)
    return vector_store

def extract_text_from_file(file_path):
    try:
        if file_path.startswith(("http://", "https://")):
            if "youtube.com" in file_path or "youtu.be" in file_path:
                return extract_text_from_youtube(file_path)
            else:
                return scrape_website(file_path)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file or path '{file_path}' does not exist.")

        file_extension = os.path.splitext(file_path)[1].lower()

        if file_extension in ['.xls', '.xlsx', '.csv']:
            return extract_text_from_excel_or_csv(file_path)
        elif file_extension == '.html':
            return extract_text_from_html(file_path)
        elif file_extension == '.json':
            return json_read(file_path)
        elif file_extension == '.mkv':
            return extract_audio_and_transcribe(file_path)
        elif file_extension == '.mp3':
            return extract_text_from_mp3(file_path)
        elif file_extension == '.pdf':
            return pdf_read(file_path)
        elif file_extension in ['.ppt', '.pptx']:
            return extract_text_from_ppt_file(file_path)
        elif file_extension in ['.c', '.cpp', '.py', '.dart', '.java', '.js', '.css', '.php', '.xml']:
            return extract_text_from_code_file(file_path)
        elif file_extension in ['.doc', '.docx']:
            return extract_text_from_word_file(file_path)
        elif file_extension == '.ipynb':  
            return extract_text_from_notebook(file_path)  # Fixed function call
        else:
            raise ValueError(f"Unsupported file type: {file_extension}.")
    except Exception as e:
        return f"Error extracting text: {e}"

def analyze_image(file_path, user_prompt):
    try:
        if not os.path.exists(file_path):
            return f"File not found: {file_path}"

        image = Image.open(file_path)
        image.verify()

        if not user_prompt:
            return "Please provide a description or question related to the image."

        llm_vision = ChatOpenAI(
            api_key="ollama",
            base_url="https://sunny-gerri-finsocialdigitalsystem-d9b385fa.koyeb.app/v1",
            model="llama3.2-vision"
        )

        prompt = f"Analyze the image and respond to this prompt: {user_prompt}"
        response = llm_vision.predict(prompt)
        return response

    except Exception as e:
        return f"Error analyzing the image: {e}"

def process_image(file_path, user_prompt):
    try:
        if not os.path.exists(file_path):
            return f"File not found: {file_path}"

        file_extension = os.path.splitext(file_path)[1].lower()
        if file_extension not in ['.jpeg', '.jpg', '.png']:
            return f"Unsupported file type: {file_extension}. Please upload a valid image file."

        response = analyze_image(file_path, user_prompt)
        return response

    except Exception as e:
        return f"Error processing image: {e}"

def generate_answer(query, retriever):
    try:
        relevant_docs = retriever.get_relevant_documents(query)
        context = " ".join([doc.page_content for doc in relevant_docs])

        prompt = f"Context: {context}\n\nQuestion: {query}\n\nAnswer:"
        response = generate_text(prompt)
        return response
    except Exception as e:
        return f"Failed to generate an answer. Error: {e}"

def main():
    st.title("AI-based Text & Image Analysis")

    option = st.selectbox("Choose an option:", ["Text Analysis", "Image Analysis"])

    if option == "Text Analysis":
        file_path = st.text_input("Enter file path or URL")

        if file_path:
            st.write(f"Processing file from: {file_path}")
            extracted_text = extract_text_from_file(file_path)

            if extracted_text.startswith("Error"):
                st.error(extracted_text)
                return

            st.write("Processing completed. Now, you can ask questions about the document.")

            text_chunks = get_chunks(extracted_text)
            vector_store = create_vector_store(text_chunks)
            retriever = vector_store.as_retriever()

            query = st.text_input("Ask a question about the document:")

            if query:
                response = generate_answer(query, retriever)
                st.write("Answer:")
                st.write(response)

    elif option == "Image Analysis":
        uploaded_file = st.file_uploader("Upload an image", type=["jpeg", "jpg", "png"])
        user_prompt = st.text_input("Enter a prompt for the image:")

        if uploaded_file and user_prompt:
            with open("temp_image.jpg", "wb") as f:
                f.write(uploaded_file.getbuffer())

            result = process_image("temp_image.jpg", user_prompt)
            st.write("Result:")
            st.write(result)

if __name__ == "__main__":
    main()

import os
import csv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.schema import Document
from langchain_openai import ChatOpenAI

def extract_stock_data(file_path):
    """
    Reads stock data from a CSV file and returns it as formatted text.
    :param file_path: Path to the CSV file
    :return: List of formatted text rows
    """
    extracted_data = []
    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        headers = next(reader)
        for row in reader:
            extracted_data.append(" | ".join(f"{headers[j]}: {row[j]}" for j in range(len(headers))))
    return extracted_data

# Initialize ChatOpenAI model
turbo_llm = ChatOpenAI(
    api_key="ollama",
    base_url="https://sunny-gerri-finsocialdigitalsystem-d9b385fa.koyeb.app/v1",
    model="athene-v2"
)

huggingface_embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def generate_text(prompt):
    try:
        return turbo_llm.predict(prompt)
    except Exception as e:
        return f"Failed to generate an answer: {e}"

def get_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return text_splitter.split_text(text)

def create_vector_store(chunks):
    docs = [Document(page_content=chunk) for chunk in chunks]
    return FAISS.from_documents(docs, huggingface_embeddings)

def process_csv(file_path):
    if not os.path.exists(file_path):
        return f"Error: The file '{file_path}' does not exist."
    extracted_text = extract_stock_data(file_path)
    text_chunks = get_chunks(" ".join(extracted_text))
    vector_store = create_vector_store(text_chunks)
    retriever = vector_store.as_retriever()
    return retriever

def main():
    file_path = input("Enter CSV file path: ")
    retriever = process_csv(file_path)
    
    if isinstance(retriever, str):  # If it's an error message
        print(retriever)
        return
    
    query = input("Ask a question about the CSV data: ")
    relevant_docs = retriever.get_relevant_documents(query)
    context = " ".join([doc.page_content for doc in relevant_docs])
    response = generate_text(f"Context: {context}\n\nQuestion: {query}\n\nAnswer:")
    print("Answer:", response)

if __name__ == "__main__":
    main()

import os
import shutil
from typing import List
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()

VECTOR_DB_PATH = "chroma_db"
DOCS_DIR = "docs"

def load_documents(docs_folder: str = DOCS_DIR) -> List:
    if not os.path.exists(docs_folder):
        os.makedirs(docs_folder)
        return []
    
    loader = DirectoryLoader(docs_folder, glob="*.pdf", loader_cls=PyPDFLoader)
    return loader.load()

def split_documents(documents: List, chunk_size: int = 1000, chunk_overlap: int = 200) -> List:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )
    return text_splitter.split_documents(documents)

def store_vectors(chunks: List):
    # Check if DB exists to avoid recreation if empty, or clear if forced.
    # For this simplified setup, we append or create.
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=VECTOR_DB_PATH
    )
    vector_store.persist()
    return vector_store

def clear_database():
    if os.path.exists(VECTOR_DB_PATH):
        shutil.rmtree(VECTOR_DB_PATH)

def run_ingestion():
    clear_database()
    docs = load_documents()
    if not docs:
        print("Nenhum documento encontrado em docs/.")
        return False
        
    chunks = split_documents(docs)
    store_vectors(chunks)
    print(f"Ingestão concluída! {len(chunks)} chunks armazenados.")
    return True

if __name__ == "__main__": run_ingestion()

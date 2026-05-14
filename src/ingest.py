from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import os, glob

load_dotenv()

def ingest_papers(papers_dir="papers", db_dir="chroma_db"):
    # Step 1: Load all PDFs
    pdf_files = glob.glob(f"{papers_dir}/*.pdf")
    print(f"Found {len(pdf_files)} papers")
    
    all_docs = []
    for pdf_path in pdf_files:
        print(f"Loading: {pdf_path}")
        loader = PyPDFLoader(pdf_path)
        docs = loader.load()
        all_docs.extend(docs)
    
    print(f"Total pages loaded: {len(all_docs)}")

    # Step 2: Split into chunks
    # 500 chars per chunk, 50 char overlap so context isn't lost at boundaries
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(all_docs)
    print(f"Total chunks created: {len(chunks)}")

    # Step 3: Embed and store in ChromaDB
    print("Embedding chunks (this takes a minute on first run)...")
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )
    
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=db_dir
    )
    
    print(f"Done. {len(chunks)} chunks stored in ChromaDB at '{db_dir}'")
    return vectorstore

if __name__ == "__main__":
    ingest_papers()
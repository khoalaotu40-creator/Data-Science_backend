import os
from src.ingestion.loader import load_documents
from src.chunking.chunker import split_documents
from src.vectordb.vector_store import create_vector_store
from dotenv import load_dotenv

load_dotenv()

def main():
    directory_path = os.getenv("DOCUMENTS_DIRECTORY", "documents")
    documents = load_documents(directory_path)
    chunks = split_documents(documents, chunk_size=1000, chunk_overlap=200)
    vector_store = create_vector_store(chunks)
    #rag_chain = vector_store.as_retriever()
if __name__ == "__main__":
    main()

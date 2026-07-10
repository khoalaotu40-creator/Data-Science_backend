import os
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

def create_vector_store(chunks, persist_directory="db/chroma_db"):
    """Create and persist ChromaDB vector store"""
    print("Creating embeddings and storing in ChromaDB...")
        
    embeddings = OpenAIEmbeddings(
        model="qwen/qwen3-embedding-8b", 
        openai_api_key=os.getenv("OPENROUTER_API_KEY"), # Trỏ đúng vào tên biến trong file .env
        openai_api_base="https://openrouter.ai/api/v1"  # Ép nó kết nối đến OpenRouter thay vì OpenAI
    )
    # Create ChromaDB vector store
    print("--- Creating vector store ---")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory, 
        collection_metadata={"hnsw:space": "cosine"}
    )
    print("--- Finished creating vector store ---")
    
    print(f"Vector store created and saved to {persist_directory}")
    return vectorstore
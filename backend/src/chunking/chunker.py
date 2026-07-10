from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter

def split_documents(documents, chunk_size=1000, chunk_overlap=0):
    """
    Chia nhỏ các tài liệu thành các chunks dựa trên kích thước và độ chồng lắp đã chỉ định.
    """
    print(f"[*] Đang chia nhỏ tài liệu thành chunks (chunk_size={chunk_size}, chunk_overlap={chunk_overlap})")
    
    # Sử dụng RecursiveCharacterTextSplitter để chia nhỏ văn bản
    text_splitter = CharacterTextSplitter(
        chunk_size=chunk_size, 
        chunk_overlap=chunk_overlap
    )
    chunks = text_splitter.split_documents(documents)
    if chunks:
    
        for i, chunk in enumerate(chunks[:5]):
            print(f"\n--- Chunk {i+1} ---")
            print(f"Source: {chunk.metadata['source']}")
            print(f"Length: {len(chunk.page_content)} characters")
            print(f"Content:")
            print(chunk.page_content)
            print("-" * 50)
        
        if len(chunks) > 5:
            print(f"\n... and {len(chunks) - 5} more chunks")
    
    return chunks
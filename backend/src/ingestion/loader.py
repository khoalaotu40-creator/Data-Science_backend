import os
from langchain_community.document_loaders import TextLoader, DirectoryLoader

def load_documents(directory_path):
    """
    Tải tất cả các tài liệu PDF từ thư mục chỉ định và chuyển đổi chúng thành định dạng Document của LangChain.
    """
    print(f"[*] Đang tải tài liệu từ thư mục: {directory_path}")
    if not os.path.exists(directory_path):
        raise FileNotFoundError(f"The directory {directory_path} does not exist. Please create it and add your company files.")
    
    loader = DirectoryLoader(
        path=directory_path,
        glob="*.md",
        loader_cls=TextLoader,
        loader_kwargs={'encoding': 'utf-8'}
    )
    documents = loader.load()
    if len(documents) == 0:
        raise FileNotFoundError(f"No .md files found in {directory_path}. Please add your company documents.")
    
   
    for i, doc in enumerate(documents[:len(documents)]):  # Show all documents 
        print(f"\nDocument {i+1}:")
        print(f"  Source: {doc.metadata['source']}")
        print(f"  Content length: {len(doc.page_content)} characters")
        print(f"  Content preview: {doc.page_content[:100]}...")
        print(f"  metadata: {doc.metadata}")

    return documents

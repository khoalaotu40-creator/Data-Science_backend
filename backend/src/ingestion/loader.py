import os
from langchain_community.document_loaders import TextLoader, DirectoryLoader
import json

def load_json_documents(directory_path):
    """
    Tải tất cả các tài liệu JSON từ thư mục chỉ định và chuyển đổi chúng thành định dạng Document của LangChain.
    """
    if not os.path.exists(directory_path):
        raise FileNotFoundError(f"Địa chỉ không tồn tại: {directory_path}. Vui lòng kiểm tra lại đường dẫn.")
    
    
    documents = []
    # Duyệt qua tất cả các file trong thư mục
    for filename in os.listdir(directory_path):
        if filename.endswith(".json"):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
                documents.append(json_data)
                

    if len(documents) == 0:
        raise FileNotFoundError(f"Không tìm thấy tài liệu JSON nào trong thư mục: {directory_path}. Vui lòng kiểm tra lại nội dung thư mục.")
    return documents

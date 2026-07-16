import os
from .legal_structure import parse_legal_structure

def process_file_and_chunk(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        md_text = f.read()
    
    final_data = parse_legal_structure(md_text)
    
    chunks=[]
    for item in final_data:
        # Tạo ID hoặc metadata cho từng chunk để dễ quản lý
        chunk = {
            "text": f"{item['chapter']} - {item['article']}\n{item['content']}",
            "metadata": {
                "chapter": item['chapter'],
                "article": item['article'],
                # Có thể thêm logic để trích xuất số Điều, số Khoản từ string nếu cần
            }
        }
        chunks.append(chunk)  
    return chunks
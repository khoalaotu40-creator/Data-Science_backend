from langchain_core.documents import Document

def json_structural_chunker(structure_list, document_metadata, breadcrumb_path=""):
    """
    Hàm đệ quy để duyệt cây JSON và tạo chunk.
    - structure_list: mảng 'structure_attachments' hoặc 'children'
    - document_metadata: các thông tin chung của văn bản (số hiệu, ngày ban hành...)
    - breadcrumb_path: chuỗi nối tên các cấp cha (VD: Luật -> Chương 1 -> Điều 2)
    """
    chunks = []
    
    for node in structure_list:
        # 1. Xây dựng đường dẫn ngữ cảnh (Breadcrumbs)
        current_title = node.get("title", "Không có tiêu đề")
        current_path = f"{breadcrumb_path} > {current_title}" if breadcrumb_path else current_title
        
        # 2. Nếu node có nội dung (content không null), biến nó thành một Chunk
        if node.get("content"):
            # Ghép đường dẫn vào nội dung để LLM nắm được bối cảnh
            rich_content = f"Ngữ cảnh: [{current_path}]\nNội dung: {node['content']}"
            
            # Đóng gói toàn bộ metadata quan trọng để Obsidian (hoặc VectorDB) sử dụng
            metadata = {
                "source": document_metadata.get("document_id"),
                "node_id": node.get("node_id"),
                "node_type": node.get("node_type"),
                "title": current_title,
                "document_type": document_metadata.get("document_type"),
                "issuer": document_metadata.get("issuer")
            }
            
            # Khởi tạo Document của Langchain
            chunks.append(Document(page_content=rich_content, metadata=metadata))
            
        # 3. Đệ quy xuống các node con (children)
        if node.get("children") and len(node["children"]) > 0:
            child_chunks = json_structural_chunker(
                node["children"], 
                document_metadata, 
                current_path
            )
            chunks.extend(child_chunks)
            
    return chunks

def process_legal_json_to_chunks(json_data):
    """
    Hàm chính để xử lý toàn bộ file JSON pháp lý.
    """
    print(f"[*] Đang thực hiện Structural Chunking cho văn bản: {json_data['document_id']}")
    
    # Lấy thông tin chung của văn bản làm metadata gốc
    doc_metadata = {
        "document_id": json_data["document_id"]
    }
    doc_metadata.update(json_data.get("identity_metadata", {}))
    
    # Bắt đầu trích xuất từ gốc của cây cấu trúc
    chunks = json_structural_chunker(
        json_data.get("structure_attachments", []), 
        doc_metadata
    )
    
    print(f"[*] Đã trích xuất thành công {len(chunks)} chunks cấu trúc.")
    return chunks
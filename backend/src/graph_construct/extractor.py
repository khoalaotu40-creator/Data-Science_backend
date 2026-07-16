'''
Chứa logic dùng llm để trích xuất entities và relationships (chưa hoàn thành)
'''

import json
from src.graph_construct.schema import GraphExtraction

def get_graph_data_from_llm(chunk_text: str) -> dict:
    """
    Hàm này gửi chunk_text lên LLM để trích xuất Entities và Relations.
    BẠN CẦN THAY THẾ PHẦN NÀY BẰNG CODE GỌI LLM THỰC TẾ CỦA BẠN.
    """
    prompt = f"""
    Bạn là một chuyên gia về pháp luật Việt Nam. 
    Từ đoạn văn bản sau, hãy trích xuất các thực thể (Nodes) và mối quan hệ (Edges).
    Trả về ĐÚNG định dạng JSON sau:
    {{
        "nodes": [{{"id": "Tên thực thể", "label": "Loại thực thể"}}],
        "edges": [{{"source": "ID thực thể 1", "target": "ID thực thể 2", "relation": "Mối quan hệ"}}]
    }}
    Văn bản: {chunk_text}
    """
    
    # --- ĐOẠN NÀY LÀ VÍ DỤ GỌI LLM - HÃY SỬ DỤNG CODE LLM CỦA BẠN ---
    # response = llm_client.generate(prompt)
    # response_text = response.text 
    
    # Tạm thời để một dữ liệu mẫu (mock data) để bạn test code chạy được ngay:
    mock_response = """
    {
        "nodes": [
            {"id": "Điều 10", "label": "Điều_Luật"},
            {"id": "Người sử dụng đất", "label": "Chủ_Thể"}
        ],
        "edges": [
            {"source": "Điều 10", "target": "Người sử dụng đất", "relation": "quy_định_quyền_của"}
        ]
    }
    """
    # ---------------------------------------------------------------
    
    try:
        # Parse chuỗi JSON thành Python Dictionary
        return json.loads(mock_response) # Thay mock_response bằng response_text của LLM
    except Exception as e:
        print(f"Lỗi khi parse JSON từ LLM: {e}")
        return {"nodes": [], "edges": []}
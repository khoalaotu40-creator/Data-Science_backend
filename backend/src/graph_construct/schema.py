'''
Định nghĩa cấu trúc (Data class cho Node và Edge)
'''

from pydantic import BaseModel
from typing import List

class Node(BaseModel):
    id: str        # Tên thực thể, vd: "Điều 10 Luật Đất đai", "UBND cấp tỉnh"
    label: str     # Loại thực thể, vd: "Điều_luật", "Cơ_quan", "Quyền_hạn"
    
class Edge(BaseModel):
    source: str    # ID của Node bắt đầu
    target: str    # ID của Node kết thúc
    relation: str  # Mối quan hệ, vd: "quy_định_về", "trực_thuộc", "bị_xử_phạt_bởi"

class GraphExtraction(BaseModel):
    nodes: List[Node]
    edges: List[Edge]
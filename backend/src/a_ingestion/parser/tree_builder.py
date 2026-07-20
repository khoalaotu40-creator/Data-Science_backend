from typing import Any
from .rules import LEVEL_ORDER, detect_heading
from .schema import make_node
from src.utils.utils import normalize_space

def flatten_tree(node: dict[str, Any]) -> list[dict[str, Any]]:
    """
    Duỗi thẳng cây phân cấp thành một danh sách (List) các Node.
    Rất hữu ích để lưu vào CSDL (Neo4j, VectorDB) hoặc xuất ra JSONL.
    """
    rows = [node]
    for child in node.get("children", []):
        rows.extend(flatten_tree(child))
    return rows

def assign_paths(node: dict[str, Any], prefix: list[str] | None = None) -> None:
    """
    Đệ quy chạy dọc theo cây để gắn 'đường dẫn' (breadcrumb) cho từng Node.
    Ví dụ: node["path"] = ["Luật Doanh nghiệp 2020", "Chương I", "Điều 1", "Khoản 1"]
    """
    prefix = prefix or []
    
    # Định dạng tên hiển thị cho node (VD: "article 1" -> "article 1")
    if node["level"] == "document":
        label = node["level"]
    else:
        label = f"{node.get('label', '')} {node.get('number', '')}".strip()
        
    current = prefix if node["level"] == "document" else prefix + [label]
    node["path"] = current
    
    for child in node.get("children", []):
        assign_paths(child, current)
def parse_structure(text: str, doc_id: str, title: str) -> dict[str, Any]:
    """
    Thuật toán lõi: Dựng cây phân cấp Điều/Khoản từ văn bản phẳng.
    """
    # 1. Khởi tạo Node gốc (Đại diện cho toàn bộ văn bản)
    root = make_node(doc_id, "document", "", title, None, 0)
    stack: list[dict[str, Any]] = [root]
    
    current = root
    current_start = 0
    offset = 0
    lines = text.splitlines()

    # Hàm nội bộ để chốt nội dung text cho node hiện tại khi gặp tiêu đề mới
    def close_current(end_char_index: int) -> None:
        current["source_span"]["end_char"] = end_char_index
        # Cắt lấy đoạn text thuộc về Node này
        current["text"] = text[current_start:end_char_index]
        current["clean_text"] = normalize_space(text[current_start:end_char_index])

    # 2. Duyệt qua từng dòng văn bản
    for line in lines:
        line_start = offset
        line_end = offset + len(line)
        
        # Hỏi rules.py xem dòng này có phải là Tiêu đề (Chương/Điều/Khoản...) không?
        heading = detect_heading(line)
        
        if heading:
            level, number, heading_title = heading
            
            # Nếu cấp bậc của dòng này cao hơn hoặc bằng dòng hiện tại (VD: Đang ở Khoản 2, gặp Điều 3)
            # -> Đóng Node hiện tại lại.
            if LEVEL_ORDER[level] <= LEVEL_ORDER.get(current["level"], 0):
                close_current(line_start)
                
            # Xả Stack: Tìm ngược lên trên để xem ai đủ tư cách làm Cha của Node mới này
            while stack and LEVEL_ORDER[stack[-1]["level"]] >= LEVEL_ORDER[level]:
                stack.pop()
                
            # Tạo Node mới và nối vào Cha
            parent = stack[-1] if stack else root
            node = make_node(doc_id, level, number, heading_title, parent["id"], line_start)
            
            parent["children"].append(node)
            stack.append(node)
            
            # Chuyển quyền "current" cho Node mới
            current = node
            current_start = line_start
            
        # Cộng dồn số lượng ký tự (bao gồm cả ký tự \n ở cuối dòng)
        offset = line_end + 1

# 3. Kết thúc văn bản: Đóng Node cuối cùng lại
    current["source_span"]["end_char"] = len(text)
    current["text"] = text[current_start:]
    current["clean_text"] = normalize_space(text[current_start:])
    
    # Quét dọn Node gốc: Nếu Node gốc không bắt được chữ nào ở đoạn đầu (vì tiêu đề xuất hiện ngay dòng 1)
    # thì copy 2000 ký tự đầu tiên để làm text tóm tắt.
    # if not root.get("text"):
    #     root["text"] = normalize_space(text[: min(len(text), 2000)])
    #     root["clean_text"] = root["text"]
    #     root["source_span"]["end_char"] = len(text)
        
    # Gắn đường dẫn Breadcrumb cho toàn bộ cây
    assign_paths(root)
    
    return {"root": root}
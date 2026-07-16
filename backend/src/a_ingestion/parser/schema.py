from typing import Any
from src.utils.utils import sha256_text, slugify, utc_now

def make_node(doc_id: str, level: str, number: str, title: str, parent_id: str | None, start: int) -> dict[str, Any]:
    # 1. Tạo hậu tố (suffix) cho node_id dựa trên số hiệu hoặc tiêu đề
    suffix = number or slugify(title)[:20] or sha256_text(title)[:8]
    
    if level != "document" and parent_id:
        suffix = f"{suffix}-{sha256_text(parent_id)[:8]}-{start}"
    
    node_id = f"{doc_id}:{level}:{slugify(suffix)}"
    
    return {
        "id": node_id,
        "level": level,
        "label": level,
        "number": number,
        "title": title,
        "text": "",
        "clean_text": "",
        "path": [],
        "parent_id": parent_id,
        "children": [],
        "source_span": {
            "start_char": start, 
            "end_char": None, 
            "page_start": None, 
            "page_end": None
        },
    }

def build_doc_id(metadata: dict[str, Any], text: str) -> str:
    """
    Tạo định danh duy nhất (doc_id) cho toàn bộ văn bản.
    Ví dụ: vn.luat.60-2024-qh15
    """
    doc_type = metadata.get("type") or "unknown"
    # Nếu văn bản không có số hiệu, dùng mã băm của nội dung để làm ID tạm
    number = metadata.get("number") or sha256_text(text)[:12]
    return f"vn.{slugify(doc_type)}.{slugify(number)}"

def build_document_schema(
    doc_id: str, 
    metadata: dict[str, Any], 
    source: dict[str, Any], 
    structure: dict[str, Any], 
    relations: list[dict[str, Any]]
) -> dict[str, Any]:
    """
    Tạo cấu trúc JSON tổng hợp chứa TOÀN BỘ thông tin về một văn bản pháp luật.
    Đây chính là "Source of Truth" sẽ được lưu ra đĩa.
    """
    doc_type = metadata.get("type", "unknown")
    is_normative = doc_type != "unknown"
    
    return {
        "doc_id": doc_id,
        "metadata": metadata,
        "classification": {
            "document_group": "normative" if is_normative else "unknown",
            "is_normative": is_normative,
            "normative_type": doc_type,
            "classification_basis": "parser heuristic from title/header",
            "classification_date": utc_now()[:10],
            "confidence": 0.6 if is_normative else 0.2,
        },
        "validity": {
            "effective_date": metadata.get("effective_date") or "",
            "expired_date": metadata.get("expired_date"),
            "status": metadata.get("status", "unknown"),
        },
        "source": source,
        "structure": structure,  # Cây cha-con được bơm vào từ tree_builder.py
        "appendices": [],
        "relations": relations,  # Danh sách quan hệ pháp lý
        "semantic": {            # Chừa sẵn bộ khung (Placeholder) để làm AI NER sau này
            "entities": [],
            "obligations": [],
            "rights": [],
            "prohibitions": [],
            "definitions": [],
            "topics": [],
            "semantic_links": [],
        },
        "parse_info": {
            "parser_version": "0.1.0",
            "parsed_at": utc_now(),
            "structure_confidence": 0.7,
            "metadata_confidence": 0.5,
            "relation_confidence": 0.5,
            "warnings": [],
        },
    }
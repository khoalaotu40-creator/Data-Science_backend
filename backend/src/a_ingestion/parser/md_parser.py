from pathlib import Path
from typing import Any
from .tree_builder import parse_structure, flatten_tree
from .schema import build_doc_id, build_document_schema
from src.utils.utils import sha256_text, safe_filename, write_json, write_jsonl
from .relations import extract_relations

def parse_markdown_to_dict(text: str, metadata: dict[str, Any], source: dict[str, Any]) -> dict[str, Any]:
    """
    Nhạc trưởng điều phối: Biến văn bản Markdown phẳng thành cấu trúc JSON hoàn chỉnh.
    """

    # Bước 1: Tạo ID duy nhất cho văn bản và xác định tiêu đề
    doc_id = build_doc_id(metadata, text)
    title = metadata.get("title") or metadata.get("short_title") or doc_id

    # Bước 2: Dựng cây cấu trúc (Phần -> Chương -> Điều -> Khoản)
    structure = parse_structure(text, doc_id, title)

    # Bước 3: Trích xuất mối quan hệ pháp lý (Căn cứ, Sửa đổi, Bãi bỏ...)
    relations = extract_relations(text, doc_id)

    # Bước 4: Đóng gói tất cả vào bộ khung Schema chuẩn
    doc_json = build_document_schema(
        doc_id=doc_id,
        metadata=metadata,
        source=source,
        structure=structure,
        relations=relations
    )

    return doc_json

def process_and_save_record(record: dict[str, Any], base_dir: Path) -> dict[str, Any]:
    """
    Hàm giao tiếp với bên ngoài: Đọc bản ghi từ bước Trích xuất (Extractor), 
    chạy bộ Parser và xuất dữ liệu ra đĩa cứng (File System).
    """

    # Đọc nội dung Markdown từ ổ cứng
    text_path = Path(record["text_path"])
    text = text_path.read_text(encoding="utf-8")

    # 1. Khởi tạo thông tin nguồn gốc (Source Lineage) để truy vết sau này
    source = {
        "source_name": "local",
        "source_url": "",
        "download_url": "",
        "file_path": record.get("input_path", ""),
        "content_type": Path(record.get("input_path", "")).suffix.lower().lstrip("."),
        "crawl_time": record.get("extracted_at", ""),
        "raw_checksum": "",
        "text_checksum": record.get("text_hash") or sha256_text(text),
    }

    # 2. Chạy luồng parser cốt lõi
    doc = parse_markdown_to_dict(text, record.get("metadata", {}), source)

    # 3. Chuẩn bị đường dẫn để lưu file
    doc_id = doc["doc_id"]
    safe_id = safe_filename(doc_id)
    
    doc_path = base_dir / "parsed" / "documents" / f"{safe_id}.json"
    nodes_path = base_dir / "parsed" / "nodes" / f"{safe_id}.jsonl"
    rel_path = base_dir / "parsed" / "relations" / f"{safe_id}.json"

    # Duỗi thẳng cây thành mảng 1 chiều (List) để lưu định dạng JSONL (phục vụ Graph/RAG)
    nodes = flatten_tree(doc["structure"]["root"])

    # 4. Ghi xuất ra đĩa cứng
    write_json(doc_path, doc)
    write_jsonl(nodes_path, nodes)
    write_json(rel_path, doc["relations"])

    return {
        "doc_id": doc_id, 
        "document_path": str(doc_path), 
        "nodes_path": str(nodes_path), 
        "relations_path": str(rel_path)
    }
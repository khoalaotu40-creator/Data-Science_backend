import pymupdf4llm
from pathlib import Path

def extract_pdf(pdf_path, output_dir_name: str = "output_md_paths")-> str:
    """
    Chuyển đổi PDF sang MD, lưu trữ (cache) vào output_dir và trả về nội dung text.
    """
    ingestion_dir = Path(__file__).resolve().parent.parent
    output_dir = ingestion_dir / output_dir_name
    output_dir.mkdir(parents=True, exist_ok=True)
    md_filename = pdf_path.stem + ".md"
    md_file_path = output_dir / md_filename

    # Nếu file đã được trích xuất từ trước, chỉ cần đọc nội dung ra
    if md_file_path.exists():
        with open(md_file_path, "r", encoding="utf-8") as f:
            md_text = f.read()
    
    
    else:
        # Nếu chưa tồn tại, tiến hành trích xuất từ file PDF
        md_text = pymupdf4llm.to_markdown(str(pdf_path))
        
        # Lưu nội dung lại để tái sử dụng cho các lần chạy sau (Cache)
        with open(md_file_path, "w", encoding="utf-8") as f:
            f.write(md_text)

    return md_text
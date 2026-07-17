import logging
import time
import json

from pathlib import Path
from .fetcher.pdf_path import get_local_pdf
from .extractors.pdf_to_md import extract_pdf
from .parser.md_parser import parse_markdown_to_dict

# 1. Cấu hình logger (Nếu ở file main.py bạn đã cấu hình rồi thì không cần đoạn này)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

# Đảm bảo output_dir là một đối tượng Path để tránh lỗi nối chuỗi đường dẫn ở các module sau
OUTPUT_DIR = Path("output_dir")

def run_ingestion_pipeline(file_path: str):
    logger.info(f"🚀 Bắt đầu chạy Ingestion Pipeline cho file: {file_path}")
    start_pipeline_time = time.time()
    
    try:
        # ---- BƯỚC 1: FETCH / XÁC THỰC FILE ----
        logger.info("⏳ [Bước 1/3] Đang xác thực đường dẫn file PDF...")
        start_step = time.time()

        pdf_file = get_local_pdf(file_path)
        
        logger.info(f"✓ Xác thực thành công. Đường dẫn tuyệt đối: {pdf_file} ({time.time() - start_step:.2f}s)")
        
        # ---- BƯỚC 2: TRÍCH XUẤT MARKDOWN ----
        logger.info(f"⏳ [Bước 2/3] Đang trích xuất văn bản PDF sang Markdown (Thư mục lưu trữ cache: {OUTPUT_DIR})...")
        start_step = time.time()
        md_text = extract_pdf(pdf_file, OUTPUT_DIR)
        
        # Thêm thông tin debug về độ dài đoạn văn bản trích xuất được
        logger.info(f"✓ Trích xuất hoàn tất. Độ dài text: {len(md_text)} ký tự ({time.time() - start_step:.2f}s)")
        
        # ---- BƯỚC 3: PHÂN TÍCH CẤU TRÚC JSON ----
        logger.info("⏳ [Bước 3/3] Đang phân tích cú pháp (Parsing) dựng cây cấu trúc Điều/Khoản...")
        start_step = time.time()
        
        # Lưu ý: Hàm cũ của bạn ở file md_parser cần 3 tham số (text, metadata, source). 
        # Nếu hàm của bạn đã sửa đổi chỉ cần chuỗi text, ta giữ nguyên. 
        # Nếu hàm yêu cầu metadata, hãy tạo mock dict tạm thời hoặc truyền từ ngoài vào.
        
        mock_metadata = {
            "title": pdf_file.stem, 
            "short_title": pdf_file.stem,
            "type": "unknown",         
            "number": "",              
            "effective_date": "",
            "status": "unknown"
        }
        mock_source = {
            "source_name": "local_pipeline",
            "file_path": str(pdf_file),
            "content_type": pdf_file.suffix.lower().lstrip(".")
        }
        
        # Gọi hàm (Tùy thuộc vào số lượng tham số hiện tại của parse_markdown_to_dict của bạn)
        # Nếu hàm của bạn chỉ nhận 1 tham số md_text: json_data = parse_markdown_to_dict(md_text)
        json_data = parse_markdown_to_dict(md_text, mock_metadata, mock_source)
        
        # Thống kê nhanh số lượng phần tử bóc tách được từ kết quả JSON
        doc_id = json_data.get("doc_id", "unknown")
        relations = json_data.get("relations", [])
        relations_count = len(relations)
        logger.info(f"✓ Phân tích cấu trúc thành công! Doc ID sinh ra: {doc_id} | Tìm thấy {relations_count} mối quan hệ pháp lý ({time.time() - start_step:.2f}s)")
        try:
            # 1. Xuất file JSON chi tiết ra thư mục output_dir để debug
            # (Đảm bảo biến output_directory hoặc đường dẫn lưu file của bạn đã được khai báo trước đó)
            debug_filename = f"{pdf_file.stem}_parsed.json"
            debug_filepath = OUTPUT_DIR / debug_filename
            with open(debug_filepath, "w", encoding="utf-8") as f:
                # ensure_ascii=False để hiển thị tiếng Việt, indent=4 để dễ đọc
                json.dump(json_data, f, ensure_ascii=False, indent=4)
            logger.info(f"💾 Đã lưu chi tiết cấu trúc JSON ra file: {debug_filepath}")

            # 2. In nhanh (preview) 3 mối quan hệ đầu tiên ra màn hình (nếu có)
            if relations_count > 0:
                logger.info("🔍 Preview nhanh các quan hệ (Relations) tìm thấy:")
                for i, rel in enumerate(relations[:3]):
                    rel_type = rel.get('relation_type', 'N/A')
                    target = rel.get('target_title', 'N/A')
                    logger.info(f"   [{i + 1}] {rel_type.upper()} -> {target}")
                
                if relations_count > 3:
                    logger.info(f"   ... (và {relations_count - 3} relations khác, xem chi tiết trong file JSON)")
        except Exception as e:
            logger.warning(f"⚠️ Lỗi khi xuất file debug JSON: {e}")








        # ---- KẾT THÚC PIPELINE ----
        total_time = time.time() - start_pipeline_time
        logger.info(f"🎉 Hoàn thành toàn bộ quy trình thành công trong {total_time:.2f} giây!")
        return json_data

    except Exception as e:
        # Bắt toàn bộ lỗi xảy ra trong quá trình chạy, log lại kèm vị trí lỗi (traceback) để debug
        logger.error(f"❌ Pipeline thất bại nghiêm trọng tại file '{file_path}'. Lý do lỗi: {str(e)}", exc_info=True)
        raise e
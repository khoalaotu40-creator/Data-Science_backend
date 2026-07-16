import logging
import time
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
        mock_metadata = {"title": pdf_file.stem, "type": "unknown"}
        mock_source = {"source_name": "local_pipeline"}
        
        # Gọi hàm (Tùy thuộc vào số lượng tham số hiện tại của parse_markdown_to_dict của bạn)
        # Nếu hàm của bạn chỉ nhận 1 tham số md_text: json_data = parse_markdown_to_dict(md_text)
        json_data = parse_markdown_to_dict(md_text, mock_metadata, mock_source)
        
        # Thống kê nhanh số lượng phần tử bóc tách được từ kết quả JSON
        doc_id = json_data.get("doc_id", "unknown")
        relations_count = len(json_data.get("relations", []))
        logger.info(f"✓ Phân tích cấu trúc thành công! Doc ID sinh ra: {doc_id} | Tìm thấy {relations_count} mối quan hệ pháp lý ({time.time() - start_step:.2f}s)")
        
        # ---- KẾT THÚC PIPELINE ----
        total_time = time.time() - start_pipeline_time
        logger.info(f"🎉 Hoàn thành toàn bộ quy trình thành công trong {total_time:.2f} giây!")
        return json_data

    except Exception as e:
        # Bắt toàn bộ lỗi xảy ra trong quá trình chạy, log lại kèm vị trí lỗi (traceback) để debug
        logger.error(f"❌ Pipeline thất bại nghiêm trọng tại file '{file_path}'. Lý do lỗi: {str(e)}", exc_info=True)
        raise e
import os
import logging
import time
import sys
from pathlib import Path
from dotenv import load_dotenv

from src.a_ingestion import run_ingestion_pipeline
from src.chunking import process_file_and_chunk
from src.vectordb.vector_store import create_vector_store
from src.graph_construct import get_graph_data_from_llm, KnowledgeGraphBuilder

# 1. Cấu hình Logger hệ thống
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),
        # Bạn có thể bỏ comment dòng dưới nếu muốn lưu log ra file để xem lại sau
        # logging.FileHandler("pipeline_debug.log", encoding="utf-8")
    ]
)
logger = logging.getLogger(__name__)

# Tải biến môi trường và kiểm tra nhanh
load_dotenv()
logger.info("Checking Environment Variables...")
# Thêm các API Key bạn dùng vào đây để check trước khi chạy nặng
required_keys = ["OPENAI_API_KEY"] 
for key in required_keys:
    if not os.getenv(key):
        logger.warning(f"⚠️ Không tìm thấy biến môi trường '{key}'. Các bước gọi LLM/VectorDB có thể bị crash!")

# 2. Định nghĩa các đường dẫn (Chuyển sang Path object để an toàn hệ thống)
RAW_DATA_PATH = Path("./raw_data")
OUTPUT_MD_PATHS = Path("./src/ingestion/output_md_paths")
OUTPUT_GRAPH_PATH = Path("output_folder")

def main():
    logger.info("==================================================")
    logger.info("🚀 BẮT ĐẦU CHẠY TOÀN BỘ GRAPH RAG PIPELINE")
    logger.info("==================================================")
    start_time = time.time()
    
    try:
        # ---- KIỂM TRA ĐẦU VÀO ----
        logger.info(f"🔎 Kiểm tra thư mục dữ liệu thô đầu vào: '{RAW_DATA_PATH.resolve()}'")
        if not RAW_DATA_PATH.exists():
            logger.error(f"❌ Thư mục đầu vào không tồn tại: {RAW_DATA_PATH}")
            return
            

            
        # Quét và lọc ra danh sách toàn bộ các file .pdf trong thư mục
        pdf_files = [f for f in RAW_DATA_PATH.glob("*") if f.suffix.lower() == ".pdf"]





        logger.info(f"📁 Tìm thấy {len(pdf_files)} file PDF cần xử lý.")

        if not pdf_files:
            logger.warning(f"⚠️ Không có file PDF nào trong thư mục {RAW_DATA_PATH}. Pipeline dừng tại đây.")
            return

        # Danh sách để chứa kết quả JSON của tất cả các file sau khi parse
        all_parsed_documents = []

        # ---- BƯỚC 1: CHẠY INGESTION PIPELINE CHO TỪNG FILE ----
        logger.info(f"⏳ [Bước 1] Tiến hành Ingestion dữ liệu theo dạng hàng loạt (Batch)...")
        start_step = time.time()
        
        for idx, pdf_path in enumerate(pdf_files, start=1):
            logger.info(f"==> Xử lý file ({idx}/{len(pdf_files)}): {pdf_path.name}")
            
            # Gọi pipeline xử lý cho TỪNG FILE một thay vì truyền cả thư mục
            json_data = run_ingestion_pipeline(str(pdf_path))
            
            if json_data:
                all_parsed_documents.append(json_data)
        
        step_time = time.time() - start_step
        logger.info(f"✓ [Bước 1] Hoàn thành Ingestion cho {len(all_parsed_documents)}/{len(pdf_files)} file trong {step_time:.2f} giây.")
        
        # Biến `loader` lúc này sẽ chứa danh sách cấu trúc của tất cả văn bản pháp luật
        loader = all_parsed_documents

        # ---- BƯỚC 2: CHUNKING & CÁC BƯỚC TIẾP THEO ----
        # Lúc này bạn có thể truyền biến `loader` (list danh sách doc) sang bước chunking tiếp theo...
        # logger.info("⏳ [Bước 2] Tiến hành cắt nhỏ văn bản (Chunking)...")
        # ...

        total_time = time.time() - start_time
        logger.info("==================================================")
        logger.info(f"🎉 TOÀN BỘ PIPELINE HOÀN THÀNH XUẤT SẮC TRONG {total_time:.2f}s!")
        logger.info("==================================================")

    except Exception as e:
        logger.critical(f"💥 PIPELINE BỊ SẬP NGHIÊM TRỌNG TẠI HÀM MAIN().", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
#     md_file_paths = loader.load_all()
#     print(f"Đã tạo thành công {len(md_file_paths)} file .md trong {output_md_paths}")

#     # 2. Xử lý chunking cho toàn bộ danh sách file
#     all_chunks = []
#     print("\n--- Bắt đầu quá trình Chunking ---")
#     for path in md_file_paths:
#         print(f"Đang xử lý file: {os.path.basename(path)}")
#         chunks = process_file_and_chunk(path)
#         print(f" -> Tạo được {len(chunks)} chunks từ file này.")
        
        
#         if chunks:
            
            
#             # Hiển thị đầy đủ nội dung của CHUNK 1 (index 0)
#             print("\n" + "="*30)
#             print(f"NỘI DUNG ĐẦY ĐỦ CỦA CHUNK 1:")
#             print(chunks[0]['text']) 
#             print(f"NỘI DUNG ĐẦY ĐỦ CỦA CHUNK 2:")
#             print(chunks[1]['text']) 
#             print("="*30 + "\n")

            
#         all_chunks.extend(chunks)
        
        
        
    
#     print(f"\n--- Hoàn tất! Tổng cộng {len(all_chunks)} chunks được tạo ---")
#     print("\n--- Bắt đầu Xây dựng Knowledge Graph (GraphRAG) ---")
#     knowledge_Graph_builder = KnowledgeGraphBuilder()

#     for i, chunk in enumerate(all_chunks):
#         print(f"Đang trích xuất Graph từ Chunk {i+1}/{len(all_chunks)}...")
#         chunk_text = chunk['text']
#         # 1. Gọi LLM để lấy Nodes và Edges
#         extracted_data = get_graph_data_from_llm(chunk_text)
#         # 2. Đưa dữ liệu vào NetworkX Graph
#         if extracted_data:
#             knowledge_Graph_builder.add_data(extracted_data)
        
#     # 3. Lưu Graph ra file
#     print("\n--- Hoàn tất trích xuất, tiến hành lưu Graph ---")
#     knowledge_Graph_builder.save_graph(output_graph_path)
# if __name__ == "__main__":
#     main()

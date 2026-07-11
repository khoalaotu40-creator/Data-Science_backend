import os

# Import các module đã viết
from ingestion.loader import load_json_documents
from chunking.chunker import process_legal_json_to_chunks
from graph_construct.buildGraph import build_sequential_graph

def main():
    print("="*60)
    print("🚀 KHỞI CHẠY PIPELINE GRAPH-RAG (STRUCTURAL CHUNKING)")
    print("="*60)
    
    # Cấu hình đường dẫn thư mục
    # Giả sử bạn để các file .md gốc trong thư mục 'data/raw'
    INPUT_DIR = "./raw_data"
    OBSIDIAN_VAULT_DIR = "./data/obsidian_vault"
    
    # Tự động tạo thư mục input nếu chưa có để tránh lỗi ngay lần chạy đầu
    os.makedirs(INPUT_DIR, exist_ok=True)
    
    try:
        # ---------------------------------------------------------
        # BƯỚC 1: INGESTION - Tải tài liệu
        # ---------------------------------------------------------
        print("\n[BƯỚC 1] Đang tải tài liệu...")
        documents = load_json_documents(INPUT_DIR)
        
        # ---------------------------------------------------------
        # BƯỚC 2: CHUNKING - Chia nhỏ văn bản
        # ---------------------------------------------------------
        print("\n[BƯỚC 2] Đang chia nhỏ văn bản...")
        all_chunks = []
        for doc in documents:
            chunks = process_legal_json_to_chunks(doc)
            all_chunks.extend(chunks)
        
        # ---------------------------------------------------------
        # BƯỚC 3: GRAPH CONSTRUCT - Xây dựng đồ thị Obsidian
        # ---------------------------------------------------------
        print("\n[BƯỚC 3] Đang xây dựng liên kết đồ thị...")
        build_sequential_graph(all_chunks, output_dir=OBSIDIAN_VAULT_DIR)
        
        print("\n" + "="*50)
        print("✅ PIPELINE HOÀN TẤT THÀNH CÔNG!")
        print("="*50)
        print(f"Thư mục vault của bạn đã sẵn sàng tại:\n👉 {os.path.abspath(OBSIDIAN_VAULT_DIR)}")
        print("\nHướng dẫn xem Graph:")
        print("1. Mở Obsidian.")
        print("2. Chọn 'Open folder as vault'.")
        print("3. Trỏ đến thư mục 'obsidian_vault' ở trên.")
        print("4. Mở Graph View (Ctrl+G hoặc Cmd+G) để xem thành quả!")

    except FileNotFoundError as fnf_error:
        print(f"\n[!] LỖI TÌM KIẾM: {fnf_error}")
        print(f"-> Vui lòng chép một vài file .md (ví dụ: Huong_Dan_Cap_Nhap.md) vào thư mục '{INPUT_DIR}' rồi chạy lại.")
    except Exception as e:
        print(f"\n[!] LỖI KHÔNG XÁC ĐỊNH TRONG PIPELINE: {e}")

if __name__ == "__main__":
    main()
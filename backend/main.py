import os
from src.ingestion import DocumentLoader
from src.chunking import process_file_and_chunk
from src.vectordb.vector_store import create_vector_store
from dotenv import load_dotenv
load_dotenv()

#Biến 
raw_data_path = "./raw_data"
output_md_paths = "./src/ingestion/output_md_paths"

def main():
    # 1. Khởi tạo loader và lấy danh sách file đã convert xong
    print(f"--- Bắt đầu load dữ liệu từ: {raw_data_path} ---")
    loader = DocumentLoader(raw_data_path, output_md_paths) # List
    md_file_paths = loader.load_all()
    print(f"Đã tạo thành công {len(md_file_paths)} file .md trong {output_md_paths}")

    # 2. Xử lý chunking cho toàn bộ danh sách file
    all_chunks = []
    print("\n--- Bắt đầu quá trình Chunking ---")
    for path in md_file_paths:
        print(f"Đang xử lý file: {os.path.basename(path)}")
        chunks = process_file_and_chunk(path)
        print(f" -> Tạo được {len(chunks)} chunks từ file này.")
        
        
        if chunks:
            
            
            # Hiển thị đầy đủ nội dung của CHUNK 1 (index 0)
            print("\n" + "="*30)
            print(f"NỘI DUNG ĐẦY ĐỦ CỦA CHUNK 1:")
            print(chunks[0]['text']) 
            print(f"NỘI DUNG ĐẦY ĐỦ CỦA CHUNK 2:")
            print(chunks[1]['text']) 
            print("="*30 + "\n")

            
        all_chunks.extend(chunks)
        
        
        
    
    print(f"\n--- Hoàn tất! Tổng cộng {len(all_chunks)} chunks được tạo ---")
    
     
if __name__ == "__main__":
    main()

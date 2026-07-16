import os
from src.ingestion import DocumentLoader
from src.chunking import process_file_and_chunk
from src.vectordb.vector_store import create_vector_store
from src.graph_construct import get_graph_data_from_llm, KnowledgeGraphBuilder
from dotenv import load_dotenv
load_dotenv()

#Biến 
raw_data_pdf_path = "./raw_data/pdf"
output_md_paths = "./data/extracted/text"
output_graph_path = "output_folder"

def main():
    # 1. Khởi tạo loader và lấy danh sách file đã convert xong
    print(f"--- Bắt đầu load dữ liệu từ: {raw_data_pdf_path} ---")
    loader = DocumentLoader(raw_data_pdf_path, output_md_paths) # List
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
    print("\n--- Bắt đầu Xây dựng Knowledge Graph (GraphRAG) ---")
    knowledge_Graph_builder = KnowledgeGraphBuilder()

    for i, chunk in enumerate(all_chunks):
        print(f"Đang trích xuất Graph từ Chunk {i+1}/{len(all_chunks)}...")
        chunk_text = chunk['text']
        # 1. Gọi LLM để lấy Nodes và Edges
        extracted_data = get_graph_data_from_llm(chunk_text)
        # 2. Đưa dữ liệu vào NetworkX Graph
        if extracted_data:
            knowledge_Graph_builder.add_data(extracted_data)
        
    # 3. Lưu Graph ra file
    print("\n--- Hoàn tất trích xuất, tiến hành lưu Graph ---")
    knowledge_Graph_builder.save_graph(output_graph_path)
if __name__ == "__main__":
    main()

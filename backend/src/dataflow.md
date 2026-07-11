# Luồng Dữ Liệu (Data Flow) - Hệ Thống RAG & GraphRAG

Tài liệu này mô tả chi tiết luồng xử lý dữ liệu giữa các module trong hệ thống, bao gồm hai giai đoạn chính: Tiền xử lý (Indexing) và Truy vấn (Query).

---

## 1. Giai đoạn Tiền xử lý dữ liệu (Indexing Pipeline)

Quá trình hệ thống đọc, xử lý tài liệu thô và lưu trữ dưới dạng Vector hoặc Đồ thị tri thức.

### Bước 1: Tải dữ liệu thô (`ingestion/loader.py`)
* **Input:** Các file tài liệu gốc (từ thư mục raw data với kiểu file là json).
* **Nhiệm vụ:** Đọc nội dung từ file, bóc tách văn bản và làm sạch các ký tự rác cơ bản.
* **Output:** Danh sách các đối tượng văn bản (`List[Document]`), bao gồm nội dung và metadata (tên file, tác giả, số trang).

### Bước 2: Chia nhỏ văn bản (`chunking/chunker.py`)
* **Input:** `List[Document]` từ bước Tải dữ liệu.
* **Nhiệm vụ:** Cắt các văn bản dài thành các đoạn nhỏ hơn (chunks) để phù hợp với giới hạn ngữ cảnh (context window) của LLM và tối ưu hóa việc tìm kiếm.
* **Output:** `List[Chunk]` (Các đoạn text ngắn, có sự chồng lấp - overlap - để giữ nguyên mạch ngữ cảnh).

### Bước 3: Nhúng & Lưu trữ Vector (`embeddings/embedder.py` -> `vectordb/vector_store.py`)
* **Input:** `List[Chunk]` từ bước Chia nhỏ.
* **Nhiệm vụ:** 
  * `embedder.py`: Chuyển đổi nội dung text của từng chunk thành các mảng số thực (vector/embeddings).
  * `vector_store.py`: Lưu trữ các vector này cùng với text gốc và metadata vào cơ sở dữ liệu Vector (như Chroma, FAISS, Qdrant).
* **Output:** Dữ liệu được lưu trữ thành công vào VectorDB, sẵn sàng cho thao tác tìm kiếm theo độ tương đồng.

### Bước 4 (Tuỳ chọn): Xây dựng Đồ thị Tri thức (`graph_construct/` -> `llm/llm_client.py`)
* **Input:** `List[Chunk]` từ bước Chia nhỏ.
* **Nhiệm vụ:** Sử dụng LLM để trích xuất các Thực thể (Entities) và Mối quan hệ (Relationships) từ các chunk. Sau đó, xây dựng và lưu trữ vào Graph Database (như Neo4j).
* **Output:** Một mạng lưới đồ thị tri thức kết nối các khái niệm cốt lõi trong tài liệu.

---

## 2. Giai đoạn Truy vấn & Sinh câu trả lời (Query Pipeline)

Quá trình xử lý câu hỏi của người dùng, tìm kiếm thông tin liên quan và sinh câu trả lời.

### Bước 1: Tiếp nhận câu hỏi (`app.py` / `api/`)
* **Input:** Câu hỏi dạng văn bản thô từ người dùng.
* **Nhiệm vụ:** Tiếp nhận request, tiền xử lý hoặc viết lại câu hỏi (Query rewrite) để hệ thống dễ dàng tìm kiếm hơn.
* **Output:** Câu hỏi đã được làm sạch và tối ưu.

### Bước 2: Tìm kiếm ngữ cảnh (`retrieval/retriever.py`)
* **Input:** Câu hỏi đã được tối ưu.
* **Nhiệm vụ:** 
  * Gọi `embedder.py` để biến câu hỏi thành vector.
  * Truy vấn `vector_store.py` để lấy ra Top K đoạn văn bản (chunks) có vector tương đồng nhất.
  * (Tuỳ chọn GraphRAG): Truy vấn `graph_construct` để lấy thêm các node/quan hệ liên quan.
* **Output:** Chuỗi ngữ cảnh tổng hợp (Context) chứa các thông tin liên quan nhất.

### Bước 3: Lắp ráp Prompt (`prompts/prompt_templates.py`)
* **Input:** Câu hỏi của người dùng + Chuỗi ngữ cảnh tổng hợp.
* **Nhiệm vụ:** Đưa câu hỏi và ngữ cảnh vào các mẫu prompt đã được thiết kế sẵn (ví dụ: *"Dựa vào thông tin sau: {context}, hãy trả lời: {question}"*).
* **Output:** Một chuỗi Prompt hoàn chỉnh, định hướng rõ ràng cho LLM.

### Bước 4: Sinh câu trả lời (`llm/llm_client.py`)
* **Input:** Chuỗi Prompt hoàn chỉnh.
* **Nhiệm vụ:** Gửi Prompt đến LLM thông qua API để mô hình suy luận và tạo ra câu trả lời dựa trên ngữ cảnh được cung cấp.
* **Output:** Câu trả lời cuối cùng trả về cho người dùng thông qua giao diện hoặc API.

#### I - Ingestion
1. Class DocumentLoader
	**Đây là class với chức năng load data và biến đổi dữ liệu từ pdf sang md. Lý do cho việc này:**
	- PDF được thiết kế để in ấn hoặc hiển thị cố định trên màn hình chứ không phục vụ truy xuất dữ liệu. Vì thế, thường gây lỗi ngắt dòng, mất thứ tự đọc , không phân biệt được đâu là tiêu đề, đâu là nội dung.
	- Markdown có phân cấp cấu trúc (thường sử dụng các ký hiệu đơn giản #, ##, ...) để đánh dấu tiêu đề, danh sách. Điều này giúp cho văn bản được tái lập một cách rõ ràng. Giúp cho các mô hình AI hiểu được mối quan hệ phân cấp. Ngoài ra, markdown dễ đàng được chunking (cắt nhỏ) theo logic, giúp quá trình retrieval (tìm kiếm) chính xác hơn nhiều
	 DocumentLoader(raw_data_path, output_md_path)
	Giải thích:
	- raw_data_path: Đường dẫn thư mục chứa các file chưa được xử lý sang file đuôi .md
	- output_md_path: Đường dẫn thư mục các file .md được sinh ra 
2. Pdf thành markdown
	Sử dụng  **pymupdf4llm** để chuyển đổi pdf sang md. Lý do sử dụng: nhanh và chính xác

#### II - Chunking
1. Xử lý cấu trúc văn bản pháp luật
	Chương - Điều - Khoản
2. Kĩ thuật chunk
	Tìm vị trí các # để tách chương điều khoản ra, sau đó tạo metadata cho từng chunk để dễ quản lý 

#### III - Graph_construct
1. Schema
	Node: bao gồm tên thực thể (id) và loại thực thể (label)
	Edge: bao gồm thực thể nguồn (source), thực thể đích (target) và mối quan hệ giữa chúng (relation)
	GraphExtraction: Ngữ cảnh tổng quan của các Node và các Edge. Mục tiêu để llm hiểu được ngữ cảnh tổng quát
2. Extractor
	Dự đoán GraphExtraction bằng mô hình LLM
3. BuildGraph
	class KnowledgeGraphBuilder: có chức năng add_data, lưu trữ graph ( có xử lý trùng lặp)

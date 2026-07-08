# Cấu trúc thư mục
scr\
│   Huong_Dan_Cap_Nhap.md
│   
├───api
│       __init__.py
│       
├───chunking
│       chunker.py
│       __init__.py
│       
├───embeddings
│       emberdder.py
│       __init__.py
│       
├───ingestion
│       loader.py
│       __init__.py
│       
├───llm
│       llm_client.py
│       __init__.py
│       
├───prompts
│       prompt_templates.py
│       __init__.py
│       
├───retrieval
│       retriever.py
│       __init__.py
│       
├───utils
│       __init__.py
│       
└───vectordb
        vector_store.py
        __init__.py
# Giải thích
## Thư mục **ingestion** (ingestion - quá trình nạp và tiền xử lý dữ liệu)
#### cấu trúc thư mục
RAG_project/
├── 
├── 
├── 
├── 
└── ingestion/                 
    ├── __init__.py
    ├── loader.py 

- **loader.py**: (Data loading) file tải và trích xuất dữ liệu 
## Thư mục **chunking** (chunking - Chia nhỏ văn bản)
#### cấu trúc thư mục
RAG_project/
├── 
├── 
├── 
├── 
└── chunking/                 
    ├── __init__.py
    ├── chunker.py 

- **chunker.py**: (chunking) Cắt tài liệu thành các đoạn văn ngắn mang ý nghĩa trọn vẹn.

## Thư mục **embeddings** (embeddings - Mã hó dữ liệu bằng cách biến chúng thành các vector database)
#### cấu trúc thư mục
RAG_project/
├── 
├── 
├── 
├── 
└── embedding/                 
    ├── __init__.py
    ├── emberdder.py 

- **emberdder.py**: (embeddings) Sử ụng mô hình Embedding để chuyển đổi các chunk thành một mảng số học đa chiều (vector) đại diện cho ngữ nghĩa của đoạn văn đó
## Thư mục **vectordb** (vector storage - Lưu trữ đánh chỉ mục)
#### cấu trúc thư mục
RAG_project/
├── 
├── 
├── 
├── 
└── vectordb/                 
    ├── __init__.py
    ├── vector_store.py 

- **vector_store.py**: Lưu trữ các vector bằng cách nạp vào cơ sở dữ liệu chuyên dụng 
- **Metadata**: Các siêu dữ liệu giúp hệ thống RAG trích dẫn nguồn một cách chính xác 

- Đây là thư mục hỗ trợ chức năng giao tiếp Database ( kết nối + truy vấn )
## Thư mục **retrieval** (retrieval- Truy xuất thông tin)
#### cấu trúc thư mục
RAG_project/
├── 
├── 
├── 
├── 
└── retriever/                 
    ├── __init__.py
    ├── retriever.py 

- **retriever.py** các kĩ thuật chỉnh sửa thông tin, sắp xếp, mở rộng  input người dùng 

## Thư mục **prompts** (prompts- Khuôn mẫu chỉ thị )
#### cấu trúc thư mục
RAG_project/
├── 
├── 
├── 
├── 
└── prompts/                 
    ├── __init__.py
    ├── prompt_templates.py 

- **prompt_templates.py** Các cấu trúc prompts cho các system

**Đọc thêm**: https://www.promptingguide.ai/techniques?fbclid=IwY2xjawS5jFtleHRuA2FlbQIxMABicmlkETFOME1NOUxWS1lYQjNyZ0tic3J0YwZhcHBfaWQQMjIyMDM5MTc4ODIwMDg5MgABHtcjYL_avrI3X-PXQyD0ChoULOBPbY_JMfx6Q_SHbuhPDWsSEpq7jBxoc-Bk_aem_z2oLZOwU-tz1pSdPUcCJNg

## Thư mục **llm** (llm - Giao tiếp với mô hình)
#### cấu trúc thư mục
RAG_project/
├── 
├── 
├── 
├── 
└── llm/                 
    ├── __init__.py
    ├── llm_client.py 

- **llm_client.py** Khởi tạo model từ các provider, generation functions, streaming
## Thư mục **graph_construct** (graph_construct - xây dựng graph knowledge)
#### cấu trúc thư mục
RAG_project/
├── 
├── 
├── 
├── 
└── graph_construct/                 
    ├── __init__.py
    ├── extractor.py    # Gọi LLM để trích xuất Thực thể pháp lý (Entities) và Quan hệ (Relationships) từ các chunk.
    ├── builder.py      # Định hình các node/edge và nối chúng lại thành một cấu trúc đồ thị (sử dụng thư viện như NetworkX).
    └── graph_store.py  # Đảm nhiệm việc lưu đồ thị vào thư mục datas/ (định dạng .json, .graphml) hoặc kết nối thẳng vào Graph Database (như Neo4j).

Dữ liệu được "thái nhỏ" thành các đoạn văn. Sau đó, module graph_construct (quan trọng nhất) sẽ dùng AI để quét các đoạn văn này, nhặt ra các "Thực thể pháp lý" (Legal Entities) và nối chúng lại thành một Sơ đồ tri thức khổng lồ lưu vào thư mục datas/

## Thư mục **utils** (utilities - tiện ích)
#### Vị trí thư mục
RAG_project/
├── 
├── 
├── 
├── 
└── utils/                 
    ├── __init__.py
    ├── text_cleaner.py    # Hàm: remove_html_tags(), normalize_spaces()
    ├── document_parser.py # Hàm: extract_text_from_pdf()
    ├── api_helpers.py     # Hàm: retry_on_timeout()
    └── prompt_utils.py    # Hàm: format_rag_prompt(context, query)

- **Chức năng**: Đây là thư mục chứa các hàm hỗ trợ ( helper functions), các hằng số, hoặc các đoạn code dùng chung cho toàn bộ dự án 
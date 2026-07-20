1_ingestion/       
│   ├── output_dir   (file md sau khi extract sẽ được lưu ở đây để được tái sử dụng)
│   ├── fetcher      (Tải web/file)
|   │   ├── pdf_path.py      
│   ├── extractors   (PDF/Word -> Text markdown)
|   │   ├── pdf_to_md.py      
│   ├── parser       (Text markdown -> Cấu trúc JSON)
|   │   ├── rules.py         # Chứa LEVEL_ORDER và Regex bắt thẻ (Điều, Khoản...)
|   │   ├── tree_builder.py  # Thuật toán Stack dựng cây cha-con (parse_structure)
|   │   ├── schema.py        # Định nghĩa khung JSON đầu ra (make_node)
|   │   └── md_parser.py     # File lõi điều phối 3 file trên
|   └── ingestion.py # Entry-point kết nối fetcher -> extractor -> parser
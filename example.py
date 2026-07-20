# Cài đặt thư viện 
# Ví dụ
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

# Đặt tên biến toàn cục (In hoa)
# Ví dụ
RAW_DATA_PATH = Path("./raw_data")
OUTPUT_MD_PATHS = Path("./src/ingestion/output_md_paths")
OUTPUT_GRAPH_PATH = Path("output_folder")

# Đặt biến thường ( không in hoa )

# Đặt tên hàm ( bắt buộc phải định nghĩ đầu ra):
# Ví dụ
def get_local_pdf(file_path: Union[str, Path]) -> Path:
import os
from pathlib import Path
from .pdf_to_md import convert_pdf_to_md

class DocumentLoader:
    def __init__(self, raw_data_path: str, output_md_path: str):
        self.raw_data_path = Path(raw_data_path) # vị trí thư mục raw_Data
        self.output_md_path = Path(output_md_path) # vị trí thư mục các file md được tạo ra từ pdf
        self.output_md_path.mkdir(parents=True, exist_ok=True)
    
    def _run_conversion(self, pdf_path): # Đổi tên thành _run_conversion
        return convert_pdf_to_md(pdf_path, self.output_md_path)
    
    def load_all(self):
        """Quét toàn bộ thư mục raw_data và trả về danh sách path file .md"""
        md_files = []
        for raw_data_file in self.raw_data_path.glob("*.pdf"):
            md_path = self._run_conversion(raw_data_file)
            md_files.append(md_path)
        return md_files
    
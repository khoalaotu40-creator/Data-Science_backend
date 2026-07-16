import pymupdf4llm

def convert_pdf_to_md(pdf_path, output_dir):
    """Chuyển đổi PDF sang MD và lưu lại"""
    md_filename = pdf_path.stem + ".md"
    md_file_path = output_dir / md_filename
    if not md_file_path.exists():
        md_text = pymupdf4llm.to_markdown(str(pdf_path))
        with open(md_file_path, "w", encoding="utf-8") as f:
            f.write(md_text)
                
    return str(md_file_path)
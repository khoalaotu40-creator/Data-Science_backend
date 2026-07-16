from .fetcher.pdf_path import get_local_pdf
from .extractors.pdf_to_md import extract_pdf
from .parser.md_parser import parse_markdown_to_dict

output_dir = "output_dir"

def run_ingestion_pipeline(file_path: str):
    pdf_file = get_local_pdf(file_path)
    md_text = extract_pdf(pdf_file, output_dir)
    json_data = parse_markdown_to_dict(md_text)
    return json_data
import re
from src.utils.utils import normalize_space, strip_accents

LEVEL_ORDER = {
    "document": 0,
    "part": 1,
    "chapter": 2,
    "section": 3,
    "subsection": 4,
    "article": 5,
    "clause": 6,
    "point": 7,
    "subpoint": 8,
}

def detect_heading(line: str) -> tuple[str, str, str] | None:
    # 1. TIỀN XỬ LÝ MARKDOWN: Bóc các ký tự định dạng (#, **, *) ra khỏi dòng
    # Xóa dấu '#' (ví dụ: '### Điều 1' -> 'Điều 1')
    line_no_md = re.sub(r"^#+\s*", "", line)
    # Xóa dấu '*' in đậm/in nghiêng (ví dụ: '**Điều 1.**' -> 'Điều 1.')
    line_no_md = line_no_md.replace("**", "").replace("*", "")
    
    # 2. CHUẨN HÓA KHOẢNG TRẮNG VÀ BỎ DẤU TIẾNG VIỆT
    clean = normalize_space(line_no_md)
    if not clean:
        return None
    ascii_line = strip_accents(clean)
    
    # 3. NHẬN DIỆN BẰNG REGEX
    patterns = [
        ("part", r"^PHAN\s+([IVXLCDM0-9A-Z]+)\b\.?\s*(.*)$"),
        ("chapter", r"^(?:CHUONG|CHAPTER)\s+([IVXLCDM0-9A-Z]+)\b\.?\s*(.*)$"),
        ("section", r"^(?:MUC|SECTION)\s+([IVXLCDM0-9A-Z]+)\b\.?\s*(.*)$"),
        ("subsection", r"^TIEU\s+MUC\s+([IVXLCDM0-9A-Z]+)\b\.?\s*(.*)$"),
        ("article", r"^(?:DIEU|ARTICLE)\s+([0-9]+[A-Za-z]?)\s*[.:]?\s*(.*)$"),
        ("clause", r"^([0-9]+)\.\s*(.+)$"),
        ("point", r"^([a-z])\)\s*(.+)$"),
    ]
    
    for level, pattern in patterns:
        match = re.match(pattern, ascii_line, flags=re.IGNORECASE)
        if match:
            number = match.group(1)
            title = clean
            
            # Với Điều, Khoản, Điểm: Trả về phần tên tiêu đề đã được tách rời số hiệu
            if level in {"article", "clause", "point"} and len(match.groups()) >= 2:
                title = normalize_space(match.group(2))
                
            return level, number, title
            
    return None
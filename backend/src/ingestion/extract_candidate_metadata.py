from __future__ import annotations
import re
from src.utils import normalize_space, strip_accents


def infer_type_from_text(text: str) -> str:
    head = strip_accents(text[:3000]).lower()
    patterns = [
        ("hien_phap", r"\bhien phap\b"),
        ("bo_luat", r"\bbo luat\b"),
        ("luat", r"\bluat\b|\blaw\b"),
        ("phap_lenh", r"\bphap lenh\b"),
        ("nghi_quyet_quoc_hoi", r"\bnghi quyet\b"),
        ("nghi_dinh", r"\bnghi dinh\b"),
        ("quyet_dinh_thu_tuong", r"\bquyet dinh\b"),
        ("thong_tu", r"\bthong tu\b"),
    ]
    for doc_type, pattern in patterns:
        if re.search(pattern, head):
            return doc_type # Trả về giá trị cho biết văn bản pháp luật đang xem là loại văn bản pháp luật nào?
    return "unknown" # Không tồn tại thì trả về unknown
def extract_candidate_metadata(text: str, extra: dict | None = None) -> dict:
    extra = extra or {}
    plain = strip_accents(text) # Loại văn bản
    head = text[:5000] 
    head_plain = plain[:5000]
    number_match = re.search(
        r"(?im)^\s*(?:So|S[o0]|Law\s+No\.?)\s*[:.]?\s*([0-9][0-9A-Za-z/.-]{1,40})\b",
        head_plain,
    )

    date_match = re.search(r"ngay\s+(\d{1,2})\s+thang\s+(\d{1,2})\s+nam\s+(\d{4})", head_plain, flags=re.IGNORECASE)
    english_date_match = re.search(
        r"\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2}),\s+(\d{4})\b",
        head_plain,
        flags=re.IGNORECASE,
    )

    title = extra.get("html_title") or ""
    lines = [normalize_space(line) for line in head.splitlines() if normalize_space(line)]
    for idx, line in enumerate(lines[:-1]):
        if strip_accents(line).upper() == "LAW":
            nxt = lines[idx + 1]
            if 2 <= len(nxt) <= 80:
                title = f"Law on {nxt.title()}"
                break

    for line in head.splitlines():
        clean = normalize_space(line)
        if 10 <= len(clean) <= 220:
            ascii_line = strip_accents(clean).lower()
            if any(token in ascii_line for token in ["luat", "nghi dinh", "thong tu", "quyet dinh", "phap lenh", "hien phap"]):
                title = clean
                break



    # Ngày khởi tạo      
    issued_date = ""
    if date_match:
        day, month, year = date_match.groups()
        issued_date = f"{int(year):04d}-{int(month):02d}-{int(day):02d}"
    elif english_date_match:
        month_name, day, year = english_date_match.groups()
        month_map = {
            "january": 1,
            "february": 2,
            "march": 3,
            "april": 4,
            "may": 5,
            "june": 6,
            "july": 7,
            "august": 8,
            "september": 9,
            "october": 10,
            "november": 11,
            "december": 12,
        }
        issued_date = f"{int(year):04d}-{month_map[month_name.lower()]:02d}-{int(day):02d}"
    return {
        "title": title,
        "short_title": title,
        "number": number_match.group(1) if number_match else "",
        "type": infer_type_from_text(text),
        "issuer": "",
        "signer": "",
        "issued_date": issued_date,
        "effective_date": "",
        "expired_date": None,
        "status": "unknown",
        "field": [],
        "keywords": [],
        "summary": "",
    }

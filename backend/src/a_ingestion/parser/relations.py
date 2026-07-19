from __future__ import annotations

import re
from typing import Any

from src.utils.utils import normalize_space, sha256_text, strip_accents


RELATION_PATTERNS = [
    ("amends", r"\bsua doi, bo sung\b"),
    ("amends", r"\bamend(?:s|ed|ing)?\b"),
    ("repeals", r"\bbai bo\b"),
    ("repeals", r"\brepeal(?:s|ed|ing)?\b"),
    ("replaces", r"\bthay the\b"),
    ("replaces", r"\breplace(?:s|d|ing)?\b"),
    ("guides", r"\bhuong dan\b"),
    ("guides", r"\bguide(?:s|d|ing)?\b"),
    ("details", r"\bquy dinh chi tiet\b"),
    ("details", r"\bdetail(?:s|ed|ing)?\b"),
    ("implements", r"\bthi hanh\b"),
    ("implements", r"\bimplement(?:s|ed|ing)?\b"),
    ("basis_for", r"\bcan cu\b"),
    ("basis_for", r"\bpursuant to\b"),
    ("basis_for", r"\bin accordance with\b"),
]

MENTION_PATTERN = re.compile(
    r"\b(Constitution|Code|Law|Ordinance|Resolution|Decree|Decision|Circular|Hien phap|Bo luat|Luat|Phap lenh|Nghi quyet|Nghi dinh|Quyet dinh|Thong tu)\b"
    r"(?:\s+so)?\s*([0-9A-Za-z/.-]{1,40})?",
    flags=re.IGNORECASE,
)


def relation_type_for_sentence(sentence_ascii: str) -> str:
    for rel_type, pattern in RELATION_PATTERNS:
        if re.search(pattern, sentence_ascii, flags=re.IGNORECASE):
            if rel_type == "basis_for":
                return "cites"
            return rel_type
    return "cites"


def split_sentences(text: str) -> list[str]:
    chunks = re.split(r"(?<=[.;:])\s+|\n+", text)
    return [normalize_space(chunk) for chunk in chunks if len(normalize_space(chunk)) > 10]


def extract_relations(text: str, doc_id: str) -> list[dict[str, Any]]:
    relations: list[dict[str, Any]] = []
    seen: set[str] = set()
    for sentence in split_sentences(text[:12000]):
        sentence_ascii = strip_accents(sentence)
        if not any(re.search(pattern, sentence_ascii, flags=re.IGNORECASE) for _, pattern in RELATION_PATTERNS):
            continue
        for match in MENTION_PATTERN.finditer(sentence_ascii):
            target_type = match.group(1)
            target_number = match.group(2) or ""
            if target_type.lower() != "constitution" and not any(ch.isdigit() for ch in target_number):
                continue
            if target_type.lower() == "constitution":
                target_number = ""
                target_title = "Constitution"
            else:
                target_title = normalize_space(match.group(0))
            rel_type = relation_type_for_sentence(sentence_ascii)
            rel_id = f"rel:{doc_id}:{rel_type}:{sha256_text(target_title + sentence)[:12]}"
            if rel_id in seen:
                continue
            seen.add(rel_id)
            relations.append(
                {
                    "relation_id": rel_id,
                    "relation_type": rel_type,
                    "source_doc_id": doc_id,
                    "source_ref": "",
                    "target_doc_id": None,
                    "target_ref": "",
                    "target_title": target_title,
                    "target_type": target_type.lower().replace(" ", "_"),
                    "target_number": target_number,
                    "evidence_text": sentence[:500],
                    "legal_effect": "",
                    "direction": "outgoing",
                    "extraction_method": "parser_regex",
                    "confidence": 0.55,
                    "needs_resolution": True,
                }
            )
    return relations

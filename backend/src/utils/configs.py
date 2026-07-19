from __future__ import annotations

from pathlib import Path

from .utils import ensure_dir, write_json


DEFAULT_ENUMS = {
    "document_group": ["normative", "administrative", "international", "internal", "unknown"],
    "normative_type": [
        "hien_phap",
        "bo_luat",
        "luat",
        "phap_lenh",
        "nghi_quyet_quoc_hoi",
        "nghi_dinh",
        "quyet_dinh_thu_tuong",
        "thong_tu",
        "unknown",
    ],
    "status": ["draft", "not_yet_effective", "in_force", "partially_expired", "expired", "unknown"],
    "node_level": [
        "document",
        "part",
        "chapter",
        "section",
        "subsection",
        "article",
        "clause",
        "point",
        "subpoint",
        "appendix",
        "table",
        "form",
    ],
    "relation_type": [
        "amends",
        "amended_by",
        "repeals",
        "repealed_by",
        "replaces",
        "replaced_by",
        "suspends",
        "extends",
        "implements",
        "implemented_by",
        "guides",
        "guided_by",
        "details",
        "basis_for",
        "cites",
        "cited_by",
        "references_article",
        "same_topic",
    ],
    "semantic_type": [
        "definition",
        "entity",
        "right",
        "obligation",
        "prohibition",
        "condition",
        "sanction",
        "deadline",
        "competent_authority",
    ],
    "extraction_method": ["metadata", "parser_regex", "manual", "llm", "unknown"],
}


DEFAULT_CRAWL_SOURCES = [
    {
        "source_id": "vbpl",
        "base_url": "https://vbpl.vn",
        "robots_url": "https://vbpl.vn/robots.txt",
        "decision": "allowed",
        "allowed_paths": ["/"],
        "disallowed_paths": ["/api/", "/Pages/"],
        "rate_limit_seconds": 2,
        "use_cases": ["metadata", "html_text", "sitemap_discovery"],
        "notes": "Primary source for VBQPPL. Do not crawl disallowed API paths.",
    },
    {
        "source_id": "vanban_chinhphu",
        "base_url": "https://vanban.chinhphu.vn",
        "robots_url": "https://vanban.chinhphu.vn/robots.txt",
        "decision": "allowed",
        "allowed_paths": ["/"],
        "disallowed_paths": [],
        "rate_limit_seconds": 2,
        "use_cases": ["metadata", "html_text", "attachments"],
        "notes": "Official government document portal.",
    },
    {
        "source_id": "phapluat_gov",
        "base_url": "https://phapluat.gov.vn",
        "robots_url": "https://phapluat.gov.vn/robots.txt",
        "decision": "allowed",
        "allowed_paths": ["/"],
        "disallowed_paths": ["/api/", "/_next/", "/admin/"],
        "rate_limit_seconds": 2,
        "use_cases": ["metadata", "html_text"],
        "notes": "Do not crawl API, Next internal assets, or admin paths.",
    },
    {
        "source_id": "thuvienphapluat",
        "base_url": "https://thuvienphapluat.vn",
        "robots_url": "https://thuvienphapluat.vn/robots.txt",
        "decision": "conditional",
        "allowed_paths": ["/"],
        "disallowed_paths": [],
        "rate_limit_seconds": 5,
        "use_cases": ["manual_reference", "link_reference"],
        "notes": "Content signals include ai-train=no and use=reference. Do not use for model training/fine-tuning.",
    },
    {
        "source_id": "congbobanan",
        "base_url": "https://congbobanan.toaan.gov.vn",
        "robots_url": "https://congbobanan.toaan.gov.vn/robots.txt",
        "decision": "blocked",
        "allowed_paths": [],
        "disallowed_paths": ["*"],
        "rate_limit_seconds": None,
        "use_cases": [],
        "notes": "Requires written permission for reuse; outside current VBQPPL MVP.",
    },
]


DEFAULT_TOPIC_SEED = {
    "topic_id": "data_law",
    "topic_name": "Du lieu va bao ve du lieu",
    "seed_documents": [
        {"number": "60/2024/QH15", "type": "Luat", "title": "Luat Du lieu"},
    ],
    "allowed_types": [
        "Hien phap",
        "Bo luat",
        "Luat",
        "Phap lenh",
        "Nghi quyet cua Quoc hoi",
        "Nghi dinh",
        "Quyet dinh cua Thu tuong",
        "Thong tu",
    ],
    "relation_depth": 2,
}


DEFAULT_DISPLAY_OVERRIDES = {
    "vn.luat.60-2024-qh15": {
        "display_title": "Luat Du lieu 2024",
        "canonical_title": "Luat Du lieu",
        "short_slug": "luat_du_lieu_2024",
        "language": "en",
        "display_order": 1,
    }
}


SCHEMA_V01 = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "ChatbotLaw Parsed Document v0.1",
    "type": "object",
    "required": ["doc_id", "metadata", "classification", "validity", "source", "structure", "appendices", "relations", "semantic", "parse_info"],
    "properties": {
        "doc_id": {"type": "string", "minLength": 1},
        "metadata": {"type": "object"},
        "classification": {"type": "object"},
        "validity": {"type": "object"},
        "source": {"type": "object"},
        "structure": {"type": "object"},
        "appendices": {"type": "array"},
        "relations": {"type": "array"},
        "semantic": {"type": "object"},
        "parse_info": {"type": "object"},
    },
}

# Khởi tạo thư mục config
def init_configs(base_dir: Path) -> list[Path]:
    config_dir = base_dir / "configs"
    ensure_dir(config_dir)
    outputs = [
        config_dir / "enums.json",
        config_dir / "crawl_sources.json",
        config_dir / "topic_seed.json",
        config_dir / "schema.v0.1.json",
        config_dir / "display_overrides.json",
    ]
    write_json(outputs[0], DEFAULT_ENUMS)
    write_json(outputs[1], DEFAULT_CRAWL_SOURCES)
    write_json(outputs[2], DEFAULT_TOPIC_SEED)
    write_json(outputs[3], SCHEMA_V01)
    write_json(outputs[4], DEFAULT_DISPLAY_OVERRIDES)
    return outputs

# Khởi tạo các output
def init_output_dirs(base_dir: Path) -> None:
    for rel in [
        "raw/html",
        "raw/pdf",
        "raw/docx",
        "extracted/text",
        "extracted/metadata",
        "parsed/documents",
        "parsed/nodes",
        "parsed/appendices",
        "parsed/relations",
        "semantic/entities",
        "semantic/obligations",
        "semantic/rights",
        "semantic/prohibitions",
        "semantic/definitions",
        "normalized/documents",
        "graph",
        "rag/bm25_index",
        "rag/vector_index",
        "obsidian/documents",
        "obsidian/chapters",
        "obsidian/articles",
        "obsidian/clauses",
        "obsidian/points",
        "obsidian/relations",
        "obsidian/nodes",
        "reports",
    ]:
        ensure_dir(base_dir / rel)

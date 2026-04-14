from __future__ import annotations

import re
import json
import unicodedata
from pathlib import Path
from typing import Any

import yaml

from .models import ProjectRepository, SeedTerm, SanskritChineseMapping, TermAnalysis
from .paths import DATA_DIR, DEMO_SOURCE_PATH


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def load_seed_terms(path: Path | None = None) -> list[SeedTerm]:
    yaml_path = path or DATA_DIR / "seed_terms.yaml"
    payload = load_yaml(yaml_path)
    return [SeedTerm.from_dict(item) for item in payload.get("terms", [])]


def load_analyses(path: Path | None = None) -> list[TermAnalysis]:
    yaml_path = path or DATA_DIR / "analyses" / "term_analyses.yaml"
    payload = load_yaml(yaml_path)
    return [TermAnalysis.from_dict(item) for item in payload.get("analyses", [])]


def load_mappings(path: Path | None = None) -> list[SanskritChineseMapping]:
    yaml_path = path or DATA_DIR / "mappings" / "sanskrit_chinese_mappings.yaml"
    payload = load_yaml(yaml_path)
    return [SanskritChineseMapping.from_dict(item) for item in payload.get("mappings", [])]


def load_repository() -> ProjectRepository:
    return ProjectRepository(
        seed_terms=load_seed_terms(),
        analyses=load_analyses(),
        mappings=load_mappings(),
    )


def load_demo_bundle(path: Path | None = None) -> list[dict[str, Any]]:
    json_path = path or DEMO_SOURCE_PATH
    with json_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def normalized_slug(text: str) -> str:
    folded = unicodedata.normalize("NFKD", text)
    no_marks = "".join(char for char in folded if not unicodedata.combining(char))
    lowered = no_marks.lower().replace("√", "")
    slug = re.sub(r"[^a-z0-9]+", "-", lowered).strip("-")
    return slug


def transliteration_aliases(term_id: str, transliteration: str) -> list[str]:
    aliases: list[str] = []
    candidates = {
        term_id,
        transliteration,
        transliteration.lower(),
        normalized_slug(transliteration),
        normalized_slug(transliteration).replace("-", " "),
        term_id.replace("_", " "),
    }
    for candidate in sorted(candidates):
        if candidate:
            aliases.append(candidate)
    return aliases

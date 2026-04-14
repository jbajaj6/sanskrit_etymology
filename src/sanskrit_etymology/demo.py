from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import DemoTerm, ProjectRepository
from .paths import DEMO_DIR
from .repository import load_demo_bundle, transliteration_aliases


def _normalize_payload(value: object) -> object:
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        return [_normalize_payload(item) for item in value]
    if isinstance(value, dict):
        return {key: _normalize_payload(item) for key, item in value.items()}
    return value


def _demo_term_from_dict(payload: dict[str, Any]) -> DemoTerm:
    return DemoTerm(
        id=str(payload["id"]),
        devanagari=str(payload["devanagari"]),
        transliteration=str(payload["transliteration"]),
        chapter=str(payload["chapter"]),
        segmentation=str(payload["segmentation"]),
        roots=list(payload.get("roots", [])),
        prefixes=list(payload.get("prefixes", [])),
        suffixes=list(payload.get("suffixes", [])),
        compound_type=payload.get("compound_type"),
        literal_gloss=str(payload["literal_gloss"]),
        philosophical_gloss=str(payload["philosophical_gloss"]),
        doctrinal_significance=str(payload["doctrinal_significance"]),
        ambiguity_notes=payload.get("ambiguity_notes"),
        confidence=str(payload["confidence"]),
        chinese_counterparts=payload.get("chinese_counterparts"),
        search_aliases=list(payload.get("search_aliases", [])),
        priority_bucket=payload.get("priority_bucket"),
        thematic_bucket=payload.get("thematic_bucket"),
    )


def build_demo_terms(repo: ProjectRepository) -> list[DemoTerm]:
    demo_bundle = load_demo_bundle()
    analyses_by_id = {analysis.id: analysis for analysis in repo.analyses}
    mappings_by_slug = {mapping.normalized_slug: mapping for mapping in repo.mappings}
    seed_by_id = {seed.id: seed for seed in repo.seed_terms}

    demo_terms: list[DemoTerm] = []
    for entry in demo_bundle:
        term_id = str(entry["id"])
        base_payload = dict(entry)
        analysis = analyses_by_id.get(term_id)
        seed = seed_by_id.get(term_id)

        if analysis is not None:
            base_payload.update(
                {
                    "id": analysis.id,
                    "devanagari": analysis.devanagari,
                    "transliteration": analysis.transliteration,
                    "chapter": analysis.chapter,
                    "segmentation": analysis.segmentation,
                    "roots": [component.__dict__ for component in analysis.roots],
                    "prefixes": [component.__dict__ for component in analysis.prefixes],
                    "suffixes": [component.__dict__ for component in analysis.suffixes],
                    "compound_type": analysis.compound_type,
                    "literal_gloss": analysis.literal_gloss,
                    "philosophical_gloss": analysis.philosophical_gloss,
                    "doctrinal_significance": analysis.doctrinal_significance,
                    "ambiguity_notes": analysis.ambiguity_notes,
                    "confidence": analysis.confidence,
                    "search_aliases": transliteration_aliases(analysis.id, analysis.transliteration),
                }
            )

        if seed is not None:
            base_payload["priority_bucket"] = seed.priority_bucket
            base_payload["thematic_bucket"] = seed.thematic_bucket
        else:
            base_payload.setdefault("priority_bucket", None)
            base_payload.setdefault("thematic_bucket", None)

        mapping = mappings_by_slug.get(seed.normalized_slug if seed is not None else "")
        chinese_counterparts = base_payload.get("chinese_counterparts")
        if mapping is not None:
            chinese_counterparts = [
                candidate.to_counterpart().__dict__ for candidate in mapping.chinese_candidates
            ]
        elif analysis and analysis.chinese_counterparts:
            chinese_counterparts = [counterpart.__dict__ for counterpart in analysis.chinese_counterparts]
        base_payload["chinese_counterparts"] = chinese_counterparts

        demo_terms.append(_demo_term_from_dict(base_payload))

    return demo_terms


def sort_demo_terms(terms: list[DemoTerm]) -> list[DemoTerm]:
    order = {"must": 0, "nice": 1, "stretch": 2}
    return sorted(
        terms,
        key=lambda term: (order.get(term.priority_bucket or "", 99), term.transliteration.lower()),
    )


def write_demo_artifacts(
    terms: list[DemoTerm],
    json_path: Path | None = None,
    inline_path: Path | None = None,
) -> tuple[Path, Path]:
    target_json = json_path or DEMO_DIR / "terms.json"
    target_inline = inline_path or DEMO_DIR / "terms_inline.js"
    payload = [_normalize_payload(term.to_dict()) for term in sort_demo_terms(terms)]

    target_json.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    target_inline.write_text(
        "window.TERMS_DATA = "
        + json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
        + ";\n",
        encoding="utf-8",
    )

    return target_json, target_inline

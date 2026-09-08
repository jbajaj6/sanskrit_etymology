from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path
from typing import Any

from .models import DemoTerm, ProjectRepository
from .paths import DEMO_DIR
from .relations import build_relations
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
        source_context=payload.get("source_context"),
        citation_trail=list(payload.get("citation_trail", [])),
        verification=str(payload.get("verification", "unverified")),
        professor_gloss=payload.get("professor_gloss"),
        source_text=str(payload.get("source_text", "yoga_sutras")),
    )


def build_demo_terms(repo: ProjectRepository) -> list[DemoTerm]:
    demo_bundle = load_demo_bundle()
    analyses_by_id = {analysis.id: analysis for analysis in repo.analyses}
    mappings_by_slug = {mapping.normalized_slug: mapping for mapping in repo.mappings}
    seed_by_id = {seed.id: seed for seed in repo.seed_terms}

    # The bundle holds working entries; a canonical analysis can stand on its
    # own, so a verified term needs no duplicate stub in demo_terms.json.
    bundle_ids = {str(entry["id"]) for entry in demo_bundle}
    entries: list[dict[str, Any]] = list(demo_bundle)
    entries.extend(
        {"id": analysis.id}
        for analysis in repo.analyses
        if analysis.id not in bundle_ids
    )

    demo_terms: list[DemoTerm] = []
    for entry in entries:
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
                    "source_context": analysis.source_context,
                    "citation_trail": list(analysis.citation_trail),
                    "verification": "source-verified",
                }
            )
        else:
            base_payload.setdefault("source_context", None)
            base_payload.setdefault("citation_trail", [])
            base_payload["verification"] = "unverified"

        if seed is not None:
            base_payload["priority_bucket"] = seed.priority_bucket
            base_payload["thematic_bucket"] = seed.thematic_bucket
            base_payload["professor_gloss"] = seed.professor_gloss
            base_payload["source_text"] = seed.source_text
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

    # Relations are between terms, so they can only be worked out once every
    # term exists. Rebuild each entry with its cross-references attached.
    relations = build_relations(demo_terms)
    return [
        replace(
            term,
            related_morphemes=relations[term.id]["morphemes"],
            related_mentions=relations[term.id]["mentions"],
        )
        for term in demo_terms
    ]


def sort_demo_terms(terms: list[DemoTerm]) -> list[DemoTerm]:
    order = {"must": 0, "nice": 1, "stretch": 2, "extended": 3}
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

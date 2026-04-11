from __future__ import annotations

import json
from pathlib import Path

from .models import DemoTerm, ProjectRepository
from .paths import DEMO_DIR
from .repository import transliteration_aliases


def _normalize_payload(value: object) -> object:
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        return [_normalize_payload(item) for item in value]
    if isinstance(value, dict):
        return {key: _normalize_payload(item) for key, item in value.items()}
    return value


def build_demo_terms(repo: ProjectRepository) -> list[DemoTerm]:
    analyses_by_id = {analysis.id: analysis for analysis in repo.analyses}
    mappings_by_slug = {mapping.normalized_slug: mapping for mapping in repo.mappings}

    demo_terms: list[DemoTerm] = []
    for seed in repo.seed_terms:
        analysis = analyses_by_id.get(seed.id)
        mapping = mappings_by_slug.get(seed.normalized_slug)

        chinese_counterparts = None
        if mapping is not None:
            chinese_counterparts = [
                candidate.to_counterpart().__dict__ for candidate in mapping.chinese_candidates
            ]
        elif analysis and analysis.chinese_counterparts:
            chinese_counterparts = [counterpart.__dict__ for counterpart in analysis.chinese_counterparts]

        if analysis is None:
            demo_terms.append(
                DemoTerm(
                    id=seed.id,
                    devanagari=seed.devanagari,
                    transliteration=seed.transliteration,
                    chapter=seed.chapter,
                    segmentation="Pending canonical analysis",
                    roots=[],
                    prefixes=[],
                    suffixes=[],
                    compound_type=None,
                    literal_gloss=seed.professor_gloss,
                    philosophical_gloss=(
                        f"Detailed morphological analysis for {seed.transliteration} "
                        "has not yet been added to the canonical dataset."
                    ),
                    doctrinal_significance=seed.notes,
                    ambiguity_notes="Canonical morphological breakdown pending.",
                    confidence="low",
                    chinese_counterparts=chinese_counterparts,
                    search_aliases=transliteration_aliases(seed.id, seed.transliteration),
                    priority_bucket=seed.priority_bucket,
                    thematic_bucket=seed.thematic_bucket,
                )
            )
            continue

        demo_terms.append(
            DemoTerm(
                id=analysis.id,
                devanagari=analysis.devanagari,
                transliteration=analysis.transliteration,
                chapter=analysis.chapter,
                segmentation=analysis.segmentation,
                roots=[component.__dict__ for component in analysis.roots],
                prefixes=[component.__dict__ for component in analysis.prefixes],
                suffixes=[component.__dict__ for component in analysis.suffixes],
                compound_type=analysis.compound_type,
                literal_gloss=analysis.literal_gloss,
                philosophical_gloss=analysis.philosophical_gloss,
                doctrinal_significance=analysis.doctrinal_significance,
                ambiguity_notes=analysis.ambiguity_notes,
                confidence=analysis.confidence,
                chinese_counterparts=chinese_counterparts,
                search_aliases=transliteration_aliases(analysis.id, analysis.transliteration),
                priority_bucket=seed.priority_bucket,
                thematic_bucket=seed.thematic_bucket,
            )
        )

    return demo_terms


def sort_demo_terms(terms: list[DemoTerm]) -> list[DemoTerm]:
    order = {"must": 0, "nice": 1, "stretch": 2}
    return sorted(terms, key=lambda term: (order.get(term.priority_bucket, 99), term.transliteration.lower()))


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

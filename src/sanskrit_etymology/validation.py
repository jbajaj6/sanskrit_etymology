from __future__ import annotations

from collections import Counter

from .models import ProjectRepository, ValidationIssue
from .repository import normalized_slug


ALLOWED_PRIORITY_BUCKETS = {"must", "nice", "stretch"}
ALLOWED_THEMATIC_BUCKETS = {
    "meditation_core",
    "mind_psychology",
    "affliction_obstacle",
    "practice_discipline",
    "insight_knowledge",
    "liberation_metaphysics",
    "advanced_compound",
}
ALLOWED_CROSS_CULTURAL_PRIORITY = {"high", "medium", "low"}
ALLOWED_CONFIDENCE = {"high", "medium", "low"}
REQUIRED_ANALYSIS_FIELDS = {
    "id",
    "devanagari",
    "transliteration",
    "chapter",
    "source_context",
    "segmentation",
    "roots",
    "prefixes",
    "suffixes",
    "compound_type",
    "literal_gloss",
    "philosophical_gloss",
    "doctrinal_significance",
    "ambiguity_notes",
    "confidence",
    "chinese_counterparts",
    "mapping_type",
    "phonetic_evidence",
    "semantic_evidence",
    "citation_trail",
}


def _duplicate_issues(values: list[str], location_prefix: str) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for value, count in Counter(values).items():
        if count > 1:
            issues.append(
                ValidationIssue(
                    severity="error",
                    location=location_prefix,
                    message=f"duplicate value '{value}' appears {count} times",
                )
            )
    return issues


def validate_repository(repo: ProjectRepository) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    issues.extend(_duplicate_issues([term.id for term in repo.seed_terms], "data/seed_terms.yaml"))
    issues.extend(
        _duplicate_issues(
            [term.normalized_slug for term in repo.seed_terms], "data/seed_terms.yaml"
        )
    )
    issues.extend(
        _duplicate_issues([analysis.id for analysis in repo.analyses], "data/analyses/term_analyses.yaml")
    )
    issues.extend(
        _duplicate_issues(
            [mapping.normalized_slug for mapping in repo.mappings],
            "data/mappings/sanskrit_chinese_mappings.yaml",
        )
    )

    seed_by_id = {term.id: term for term in repo.seed_terms}
    seed_by_slug = {term.normalized_slug: term for term in repo.seed_terms}
    analysis_ids = {analysis.id for analysis in repo.analyses}

    for term in repo.seed_terms:
        if term.priority_bucket not in ALLOWED_PRIORITY_BUCKETS:
            issues.append(
                ValidationIssue(
                    severity="error",
                    location=f"seed:{term.id}",
                    message=f"invalid priority_bucket '{term.priority_bucket}'",
                )
            )
        if term.thematic_bucket not in ALLOWED_THEMATIC_BUCKETS:
            issues.append(
                ValidationIssue(
                    severity="error",
                    location=f"seed:{term.id}",
                    message=f"invalid thematic_bucket '{term.thematic_bucket}'",
                )
            )
        if term.cross_cultural_priority not in ALLOWED_CROSS_CULTURAL_PRIORITY:
            issues.append(
                ValidationIssue(
                    severity="error",
                    location=f"seed:{term.id}",
                    message=f"invalid cross_cultural_priority '{term.cross_cultural_priority}'",
                )
            )

    for analysis in repo.analyses:
        if analysis.id not in seed_by_id:
            issues.append(
                ValidationIssue(
                    severity="error",
                    location=f"analysis:{analysis.id}",
                    message="analysis id does not exist in seed terms",
                )
            )
            continue

        seed = seed_by_id[analysis.id]
        if analysis.devanagari != seed.devanagari:
            issues.append(
                ValidationIssue(
                    severity="error",
                    location=f"analysis:{analysis.id}",
                    message="Devanagari does not match seed term",
                )
            )
        if normalized_slug(analysis.transliteration) != seed.normalized_slug:
            issues.append(
                ValidationIssue(
                    severity="error",
                    location=f"analysis:{analysis.id}",
                    message="transliteration slug does not match seed normalized_slug",
                )
            )
        if analysis.confidence not in ALLOWED_CONFIDENCE:
            issues.append(
                ValidationIssue(
                    severity="error",
                    location=f"analysis:{analysis.id}",
                    message=f"invalid confidence '{analysis.confidence}'",
                )
            )

    for mapping in repo.mappings:
        seed = seed_by_slug.get(mapping.normalized_slug)
        if seed is None:
            issues.append(
                ValidationIssue(
                    severity="error",
                    location=f"mapping:{mapping.normalized_slug}",
                    message="mapping does not align with a seed term normalized_slug",
                )
            )
            continue

        if mapping.devanagari != seed.devanagari:
            issues.append(
                ValidationIssue(
                    severity="error",
                    location=f"mapping:{mapping.normalized_slug}",
                    message="Devanagari does not match seed term",
                )
            )
        if mapping.overall_confidence not in ALLOWED_CONFIDENCE:
            issues.append(
                ValidationIssue(
                    severity="error",
                    location=f"mapping:{mapping.normalized_slug}",
                    message=f"invalid overall_confidence '{mapping.overall_confidence}'",
                )
            )
        for candidate in mapping.chinese_candidates:
            if candidate.confidence not in ALLOWED_CONFIDENCE:
                issues.append(
                    ValidationIssue(
                        severity="error",
                        location=f"mapping:{mapping.normalized_slug}:{candidate.characters}",
                        message=f"invalid candidate confidence '{candidate.confidence}'",
                    )
                )

    missing_analyses = [
        seed.id for seed in repo.seed_terms if seed.id not in analysis_ids and seed.priority_bucket != "stretch"
    ]
    for term_id in missing_analyses:
        issues.append(
            ValidationIssue(
                severity="warning",
                location=f"seed:{term_id}",
                message="non-stretch seed term is missing a canonical analysis entry",
            )
        )

    return issues

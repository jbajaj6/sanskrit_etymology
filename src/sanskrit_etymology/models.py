from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class RootComponent:
    root: str
    devanagari: str | None
    meaning: str
    dhatu_number: str | None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "RootComponent":
        return cls(
            root=str(data["root"]),
            devanagari=data.get("devanagari"),
            meaning=str(data["meaning"]),
            dhatu_number=data.get("dhatu_number"),
        )


@dataclass(frozen=True)
class PrefixComponent:
    prefix: str
    meaning: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PrefixComponent":
        return cls(prefix=str(data["prefix"]), meaning=str(data["meaning"]))


@dataclass(frozen=True)
class SuffixComponent:
    suffix: str
    meaning: str
    grammatical_function: str | None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SuffixComponent":
        return cls(
            suffix=str(data["suffix"]),
            meaning=str(data["meaning"]),
            grammatical_function=data.get("grammatical_function"),
        )


@dataclass(frozen=True)
class ChineseCounterpart:
    characters: str
    pinyin: str
    mapping_type: str
    source: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ChineseCounterpart":
        return cls(
            characters=str(data["characters"]),
            pinyin=str(data["pinyin"]),
            mapping_type=str(data["mapping_type"]),
            source=data.get("source"),
        )


@dataclass(frozen=True)
class SeedTerm:
    id: str
    devanagari: str
    transliteration: str
    normalized_slug: str
    priority_bucket: str
    chapter: str
    professor_gloss: str
    thematic_bucket: str
    cross_cultural_priority: str
    notes: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SeedTerm":
        return cls(
            id=str(data["id"]),
            devanagari=str(data["devanagari"]),
            transliteration=str(data["transliteration"]),
            normalized_slug=str(data["normalized_slug"]),
            priority_bucket=str(data["priority_bucket"]),
            chapter=str(data["chapter"]),
            professor_gloss=str(data["professor_gloss"]),
            thematic_bucket=str(data["thematic_bucket"]),
            cross_cultural_priority=str(data["cross_cultural_priority"]),
            notes=str(data["notes"]),
        )


@dataclass(frozen=True)
class TermAnalysis:
    id: str
    devanagari: str
    transliteration: str
    chapter: str
    source_context: str
    segmentation: str
    roots: list[RootComponent]
    prefixes: list[PrefixComponent]
    suffixes: list[SuffixComponent]
    compound_type: str | None
    literal_gloss: str
    philosophical_gloss: str
    doctrinal_significance: str
    ambiguity_notes: str | None
    confidence: str
    chinese_counterparts: list[ChineseCounterpart] | None
    mapping_type: str | None
    phonetic_evidence: str | None
    semantic_evidence: str | None
    citation_trail: list[str]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TermAnalysis":
        counterparts = data.get("chinese_counterparts") or None
        return cls(
            id=str(data["id"]),
            devanagari=str(data["devanagari"]),
            transliteration=str(data["transliteration"]),
            chapter=str(data["chapter"]),
            source_context=str(data["source_context"]),
            segmentation=str(data["segmentation"]),
            roots=[RootComponent.from_dict(item) for item in data.get("roots", [])],
            prefixes=[PrefixComponent.from_dict(item) for item in data.get("prefixes", [])],
            suffixes=[SuffixComponent.from_dict(item) for item in data.get("suffixes", [])],
            compound_type=data.get("compound_type"),
            literal_gloss=str(data["literal_gloss"]),
            philosophical_gloss=str(data["philosophical_gloss"]),
            doctrinal_significance=str(data["doctrinal_significance"]),
            ambiguity_notes=data.get("ambiguity_notes"),
            confidence=str(data["confidence"]),
            chinese_counterparts=(
                [ChineseCounterpart.from_dict(item) for item in counterparts]
                if counterparts
                else None
            ),
            mapping_type=data.get("mapping_type"),
            phonetic_evidence=data.get("phonetic_evidence"),
            semantic_evidence=data.get("semantic_evidence"),
            citation_trail=[str(item) for item in data.get("citation_trail", [])],
        )


@dataclass(frozen=True)
class ChineseMappingCandidate:
    characters: str
    pinyin: str
    historical_reading_notes: str | None
    source_tradition: str
    attestation_source: list[str]
    mapping_type: str
    phonetic_evidence: str | None
    semantic_evidence: str | None
    translation_strategy: str
    doctrinal_shift_notes: str | None
    confidence: str
    ambiguity_notes: str | None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ChineseMappingCandidate":
        return cls(
            characters=str(data["characters"]),
            pinyin=str(data["pinyin"]),
            historical_reading_notes=data.get("historical_reading_notes"),
            source_tradition=str(data["source_tradition"]),
            attestation_source=[str(item) for item in data.get("attestation_source", [])],
            mapping_type=str(data["mapping_type"]),
            phonetic_evidence=data.get("phonetic_evidence"),
            semantic_evidence=data.get("semantic_evidence"),
            translation_strategy=str(data["translation_strategy"]),
            doctrinal_shift_notes=data.get("doctrinal_shift_notes"),
            confidence=str(data["confidence"]),
            ambiguity_notes=data.get("ambiguity_notes"),
        )

    def to_counterpart(self) -> ChineseCounterpart:
        source = self.attestation_source[0] if self.attestation_source else None
        return ChineseCounterpart(
            characters=self.characters,
            pinyin=self.pinyin,
            mapping_type=self.mapping_type,
            source=source,
        )


@dataclass(frozen=True)
class SanskritChineseMapping:
    sanskrit_term: str
    devanagari: str
    normalized_slug: str
    chinese_candidates: list[ChineseMappingCandidate]
    overall_mapping_type: str
    overall_confidence: str
    overall_notes: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SanskritChineseMapping":
        return cls(
            sanskrit_term=str(data["sanskrit_term"]),
            devanagari=str(data["devanagari"]),
            normalized_slug=str(data["normalized_slug"]),
            chinese_candidates=[
                ChineseMappingCandidate.from_dict(item)
                for item in data.get("chinese_candidates", [])
            ],
            overall_mapping_type=str(data["overall_mapping_type"]),
            overall_confidence=str(data["overall_confidence"]),
            overall_notes=str(data["overall_notes"]),
        )


@dataclass(frozen=True)
class DemoTerm:
    id: str
    devanagari: str
    transliteration: str
    chapter: str
    segmentation: str
    roots: list[dict[str, Any]]
    prefixes: list[dict[str, Any]]
    suffixes: list[dict[str, Any]]
    compound_type: str | None
    literal_gloss: str
    philosophical_gloss: str
    doctrinal_significance: str
    ambiguity_notes: str | None
    confidence: str
    chinese_counterparts: list[dict[str, Any]] | None
    search_aliases: list[str]
    priority_bucket: str
    thematic_bucket: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ValidationIssue:
    severity: str
    location: str
    message: str


@dataclass(frozen=True)
class ProjectRepository:
    seed_terms: list[SeedTerm]
    analyses: list[TermAnalysis]
    mappings: list[SanskritChineseMapping]

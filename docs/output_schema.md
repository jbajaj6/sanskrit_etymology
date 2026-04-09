# Term Analysis Output Schema

Version: 1.0
Date: 2026-04-08

Every term analysis produced by this project must conform to the fields below. This schema ensures consistency across batches and makes future aggregation possible.

## Required Fields

### Identity

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Normalized slug matching `seed_terms.yaml` |
| `devanagari` | string | Term in Devanagari script |
| `transliteration` | string | IAST with diacritics |

### Context

| Field | Type | Description |
|-------|------|-------------|
| `chapter` | string | YS chapter(s) where the term appears (e.g., "YS 1, 3") |
| `source_context` | string | Key sutra(s) or passage(s) where the term is most important, quoted or paraphrased |

### Morphological Analysis

| Field | Type | Description |
|-------|------|-------------|
| `segmentation` | string | Visible breakdown of the word (e.g., "sam + ā + √dhā + -i") |
| `roots` | list of objects | Each root: `{root, devanagari, meaning, dhatu_number}`. `dhatu_number` is optional. |
| `prefixes` | list of objects | Each prefix: `{prefix, meaning}`. Empty list if none. |
| `suffixes` | list of objects | Each suffix: `{suffix, meaning, grammatical_function}`. Empty list if none. |
| `compound_type` | string or null | One of: `tatpuruṣa`, `dvandva`, `bahuvrīhi`, `avyayībhāva`, `karmadhāraya`, or `null` if not a compound |

### Meaning

| Field | Type | Description |
|-------|------|-------------|
| `literal_gloss` | string | Compositional meaning built from morphological parts |
| `philosophical_gloss` | string | How the term functions as a technical concept in Yoga/Sāṃkhya/Buddhist philosophy |
| `doctrinal_significance` | string | Why this term matters in the broader system (1-3 sentences) |

### Confidence & Ambiguity

| Field | Type | Description |
|-------|------|-------------|
| `ambiguity_notes` | string or null | Any scholarly debate about the derivation, meaning, or interpretation |
| `confidence` | string | One of: `high`, `medium`, `low` — reflects certainty of the morphological analysis |

### Chinese Mapping (Provisional)

These fields are placeholders for the mapping stage. They may be `null` or `provisional` in early batches.

| Field | Type | Description |
|-------|------|-------------|
| `chinese_counterparts` | list of objects or null | Each: `{characters, pinyin, mapping_type, source}` |
| `mapping_type` | string or null | One of: `phonetic`, `semantic`, `hybrid`, or `null` |
| `phonetic_evidence` | string or null | If phonetic: reconstruction or transliteration logic |
| `semantic_evidence` | string or null | If semantic: explanation of meaning correspondence |
| `citation_trail` | list of strings | Texts or references supporting the mapping (Taishō numbers, translator names, dates) |

## Notes on Usage

- Every field must be present in the YAML output, even if the value is `null`.
- `confidence` refers to the morphological analysis, not the philosophical interpretation.
- `chinese_counterparts` should remain `null` until the mapping stage unless there is strong, well-attested evidence (e.g., 般若 for prajñā).
- All claims must be supportable by standard reference works (Monier-Williams, Apte, Edgerton's Buddhist Hybrid Sanskrit Dictionary). Do not fabricate.

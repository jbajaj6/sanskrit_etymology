# Sanskrit Etymology Project

Computational philology project focused on meditation and philosophical vocabulary.

## Project Goals

1. Analyze Sanskrit philosophical/meditation terms (especially Yoga Sutras) — roots, prefixes, suffixes, compound structure, transliteration, literal and philosophical meaning.
2. Trace how meditation and Buddhist concepts moved from India to China — comparing Sanskrit terms with Chinese Buddhist equivalents using phonetic and semantic evidence.

## Audience

Philosophy professor with a meditation emphasis (samadhi meditation). Very little technical background. All outputs must prioritize interpretability, disciplined sourcing, and human-readable formats.

## Key Conventions

- Sanskrit: always provide Devanagari + IAST transliteration
- Chinese: always provide characters + pinyin
- Citations: Yoga Sutras by number (YS 1.2), Buddhist texts by Taisho number (T.1579)
- Never fabricate etymologies, citations, or translator attributions
- Use `source-discipline` skill standards on all outputs

## Directory Structure

```
data/raw/          — Original source texts (TEI-XML, plain text)
data/processed/    — Cleaned and structured data
src/ingest/        — Text ingestion and parsing
src/lexicon/       — Term analysis and morphological breakdown
src/mapping/       — Sanskrit-Chinese term mapping
src/utils/         — Shared utilities
notebooks/         — Exploratory analysis
docs/              — Documentation and presentation materials
```

## Available Skills

- `/sanskrit-term-breakdown` — Morphological + philosophical analysis of a Sanskrit term
- `/buddhist-term-mapper` — Map Sanskrit terms to Chinese Buddhist equivalents
- `/corpus-ingest-tei` — Parse TEI-XML texts into structured data
- `/philology-presentation-writer` — Generate presentation materials for class
- `/source-discipline` — Audit sourcing rigor on any output

## PowerPoint Generation

Generate .pptx presentations from YAML slide specs:

```
/opt/homebrew/bin/python3.11 src/utils/generate_pptx.py <input.yaml> <output.pptx>
```

Supported slide types: `title`, `section`, `content`, `two_column`, `table`, `quote`.
Theme colors, fonts, and speaker notes are configurable in the YAML.
Requires: `python-pptx` and `pyyaml` (installed in `/opt/homebrew/lib/python3.11/`).

## MCP Servers

- `buddha` — buddha-cli (formerly daizo-mcp). Full Buddhist text MCP: search, fetch, and index across CBETA, GRETIL, SARIT, MUKTABODHA, Pali Tipitaka. This is the primary domain-specific tool.
- `fetch` — General web content retrieval (for online references not covered by buddha)
- `filesystem` — Local file access scoped to this project

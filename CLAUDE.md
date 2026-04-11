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
data/raw/                           — Original source texts (TEI-XML, plain text)
data/processed/                     — Cleaned and structured data
data/seed_terms.yaml                — Canonical term catalog
data/analyses/term_analyses.yaml    — Canonical term analyses
data/mappings/*.yaml                — Canonical mapping data
src/sanskrit_etymology/             — Package code, CLI, validators, demo builders
demo/                               — Static demo and generated artifacts
docs/                               — Documentation and research materials
```

## Available Skills

- `/sanskrit-term-breakdown` — Morphological + philosophical analysis of a Sanskrit term
- `/buddhist-term-mapper` — Map Sanskrit terms to Chinese Buddhist equivalents
- `/corpus-ingest-tei` — Parse TEI-XML texts into structured data
- `/philology-presentation-writer` — Generate presentation materials for class
- `/source-discipline` — Audit sourcing rigor on any output

## Software Commands

Validate canonical data:

```
sanskrit-etymology validate-data
```

Build demo artifacts from canonical YAML:

```
sanskrit-etymology build-demo
```

Print dataset stats:

```
sanskrit-etymology stats
```

## MCP Servers

- `buddha` — buddha-cli (formerly daizo-mcp). Full Buddhist text MCP: search, fetch, and index across CBETA, GRETIL, SARIT, MUKTABODHA, Pali Tipitaka. This is the primary domain-specific tool.
- `fetch` — General web content retrieval (for online references not covered by buddha)
- `filesystem` — Local file access scoped to this project

Treat the MCP stack as optional. The repo should remain usable through the packaged CLI even when MCP servers are unavailable.

---
name: corpus-ingest-tei
description: Ingest and parse TEI-XML encoded texts (e.g., from GRETIL, SARIT, or CBETA) into structured data for analysis. Use when processing source texts in TEI format.
user-invocable: true
---

# Corpus Ingest (TEI-XML)

You are helping ingest TEI-XML encoded Sanskrit or Chinese Buddhist texts into a structured format suitable for computational philology.

## Supported Sources

- **GRETIL** (Goettingen Register of Electronic Texts in Indian Languages): Sanskrit and Pali texts
- **SARIT** (Search and Retrieval of Indic Texts): Critical editions in TEI
- **CBETA** (Chinese Buddhist Electronic Text Association): Chinese Tripitaka in TEI-like XML
- **Digital Corpus of Sanskrit (DCS)**: Morphologically tagged Sanskrit

## Workflow

When the user provides a TEI-XML file or URL:

1. **Validate** the XML structure and identify the TEI schema version
2. **Extract metadata**: title, author, editor, source, language, encoding
3. **Extract body text** preserving:
   - Verse/prose structure (lg, l, p elements)
   - Chapter/section divisions (div elements with type attributes)
   - Critical apparatus notes (app, rdg elements) if present
   - Manuscript sigla if present
4. **Output** a clean structured representation:
   - Plain text with reference markers (e.g., verse numbers)
   - Metadata JSON sidecar
   - Save to `data/processed/` with a clear filename

## Guidelines

- Preserve original text encoding (UTF-8 with proper diacritics).
- Do not silently drop any text content.
- Flag any encoding issues or malformed XML.
- For CBETA texts, handle the juan (scroll) structure.
- Output should be ready for downstream term extraction, not for display.

## File Naming Convention

```
data/processed/{source}_{text_id}_{language}.json
data/processed/{source}_{text_id}_{language}.txt
```

Example: `data/processed/gretil_yogasutra_sa.json`

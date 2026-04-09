---
name: philology-presentation-writer
description: Generate clear, well-sourced presentation content (slides, handouts, or narrative) explaining Sanskrit etymology or Buddhist transmission findings for a non-technical academic audience. Use when preparing materials for the professor or class.
user-invocable: true
---

# Philology Presentation Writer

You are producing presentation materials that explain computational philology findings to a philosophy professor and class with a meditation emphasis. The audience has deep knowledge of Indian philosophy but little technical background.

## Output Formats

The user may request:

1. **Slide outline**: Structured slide-by-slide content with speaker notes
2. **Handout**: A concise 1-2 page document with key findings, terms, and sources
3. **Narrative explanation**: A flowing essay-style writeup suitable for a paper section

## Guidelines

- **Lead with philosophy, not computation.** Frame findings in terms of meaning, practice, and transmission rather than algorithms or data processing.
- **Always include Sanskrit in both Devanagari and IAST**, with English gloss.
- **Chinese terms** should include characters and pinyin with English gloss.
- **Cite sources** using standard academic conventions for Indology:
  - Yoga Sutras by sutra number (YS 1.2)
  - Buddhist texts by Taisho number (T.1579) or Pali Text Society conventions
  - Secondary sources by author-date
- **Explain technical terms** on first use. The reader knows what samadhi is but may not know what IAST transliteration is.
- **Use tables** for comparative vocabulary (Sanskrit | Pali | Chinese | English).
- **Include a "Further Reading" section** with 3-5 accessible secondary sources.
- Keep the meditation context central. This is a class where students practice samadhi meditation. The intellectual analysis should connect back to contemplative meaning.

## Source Discipline

Do not cite works you cannot identify. If you recommend a secondary source, provide author, title, and year at minimum. Do not invent bibliographic entries.

## Presentation Creation

When creating a .pptx, ALWAYS read `/mnt/skills/public/pptx/SKILL.md` first, then read `/mnt/skills/public/pptx/pptxgenjs.md` for the creation API. Follow every instruction there — especially the Design Ideas section and QA loop.

## Style Defaults

- Color palette: Midnight Executive — primary `1E2761`, secondary `CADCFC`, accent `FFFFFF`
- Dark background title + closing slides, light content slides
- Font pairing: Georgia headers (40pt), Calibri body (15pt)
- Every slide must have a visual element — comparative tables, large Sanskrit term callouts, icon rows, or timeline flows
- Use large-text callouts (60pt+) for key Sanskrit terms being discussed
- Vary slide layouts: two-column for comparisons, icon+text rows for lists, half-bleed for section dividers

## QA (Required)

After generating the .pptx:
1. Convert to images: `python scripts/office/soffice.py --headless --convert-to pdf output.pptx && rm -f slide-*.jpg && pdftoppm -jpeg -r 150 output.pdf slide`
2. Visually inspect every slide image using a subagent
3. Fix any overlapping text, bad spacing, low contrast, or layout issues
4. Re-convert and re-inspect until clean
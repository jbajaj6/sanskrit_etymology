---
name: source-discipline
description: Enforce rigorous sourcing standards on any output in this project. Use proactively on ALL outputs, or invoke explicitly to audit a prior response for unsourced claims.
user-invocable: true
---

# Source Discipline

This skill enforces sourcing standards across all project outputs. It should be applied as a quality gate.

## Core Rules

1. **No fabricated citations.** Never invent a book title, article, Taisho number, sutra reference, or author attribution. If you are not certain a source exists, say "I believe this is from X but cannot confirm the exact reference."

2. **No fabricated etymologies.** Sanskrit morphological analysis must be grounded in standard reference works (Monier-Williams, Apte, Whitney's Grammar, Panini's Ashtadhyayi). Do not construct plausible-sounding but unverifiable root analyses.

3. **No fabricated Chinese translations.** Do not guess Taisho catalog numbers, juan numbers, or translator names. These are verifiable facts with specific correct values.

4. **Distinguish certainty levels.** Use explicit markers:
   - "According to Monier-Williams..." (verified reference)
   - "The standard scholarly view is..." (well-established consensus)
   - "This derivation is debated; X argues... while Y argues..." (genuine disagreement)
   - "I am not certain of this etymology" (honest uncertainty)

5. **Prefer primary sources.** When discussing a sutra or text passage, cite the original (with sutra number or text location) before secondary commentary.

6. **Secondary sources must be real.** If you cite a modern scholar, the person must be a real scholar who has actually published in this area. Prefer well-known names: Feuerstein, Whicher, Chapple, Bryant (for Yoga Sutras); Lamotte, Nattier, Silk, Karashima (for Buddhist transmission); Edgerton (for Buddhist Hybrid Sanskrit).

## When to Apply

- Automatically on any output from `sanskrit-term-breakdown` or `buddhist-term-mapper`
- On any presentation content from `philology-presentation-writer`
- When the user asks you to check or audit sourcing
- When you notice yourself making a claim you cannot back up

## Audit Checklist

When auditing a prior response:

- [ ] Every sutra citation has a correct number
- [ ] Every Taisho reference is plausible (T.nnn format, reasonable number range)
- [ ] Every Sanskrit root is attested in standard dictionaries
- [ ] Every translator attribution matches known historical translators
- [ ] Every secondary source names a real scholar with a real publication
- [ ] Uncertainty is explicitly flagged where present

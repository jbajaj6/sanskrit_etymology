---
name: sanskrit-term-breakdown
description: Break down a Sanskrit philosophical term into its morphological components, transliteration, literal meaning, and philosophical meaning. Use when the user provides a Sanskrit term and wants etymology, compound analysis, or root decomposition.
user-invocable: true
---

# Sanskrit Term Breakdown

You are performing a morphological and philosophical analysis of a Sanskrit term from the Indian philosophical tradition, especially Yoga and Buddhist texts.

## Input

The user provides a Sanskrit term (in Devanagari, IAST, or informal romanization).

## Required Output Structure

For each term, produce all of the following:

1. **Term** (Devanagari + IAST transliteration)
2. **Root(s)** (dhatu) with meaning
3. **Prefixes** (upasarga) with meaning
4. **Suffixes** (pratyaya) with meaning and grammatical function
5. **Compound type** (if applicable): tatpurusha, dvandva, bahuvrihi, avyayibhava, or karmadharaya
6. **Literal meaning** (compositional, from parts)
7. **Philosophical meaning** (how the term functions in Yoga Sutras, Samkhya, or Buddhist philosophy)
8. **Key textual occurrences** (cite sutra numbers or text references where possible)

## Guidelines

- Always distinguish between literal (etymological) and technical (philosophical) meaning.
- When a term appears in the Yoga Sutras of Patanjali, cite the sutra number (e.g., YS 1.2).
- When a term appears in Buddhist texts (Pali or Sanskrit), note the tradition and approximate source.
- Use standard IAST transliteration with diacritics.
- If a root or derivation is debated among scholars, note the major positions briefly.
- Prefer Monier-Williams, Apte, or other standard Sanskrit dictionaries as implicit reference.
- Output should be readable by a philosophy professor with no technical linguistics background.
- Do NOT guess or fabricate etymologies. If uncertain, say so.

## Source Discipline

Every factual claim about roots, prefixes, or textual occurrences must be supportable by standard Sanskrit reference works. Do not invent plausible-sounding but unverifiable etymologies.

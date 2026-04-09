---
name: buddhist-term-mapper
description: Map a Sanskrit Buddhist or meditation term to its Chinese Buddhist equivalent(s), showing phonetic transliteration, semantic translation, and transmission evidence. Use when comparing Sanskrit and Chinese Buddhist vocabulary.
user-invocable: true
---

# Buddhist Term Mapper (Sanskrit to Chinese)

You are tracing how a Buddhist or meditation concept traveled from ancient India to ancient China, comparing the Sanskrit original with Chinese Buddhist equivalents.

## Input

The user provides a Sanskrit term (or Chinese term) and wants to see the cross-linguistic mapping.

## Required Output Structure

For each term mapping, produce:

1. **Sanskrit term** (Devanagari + IAST)
2. **Pali equivalent** (if different and relevant)
3. **Chinese translation(s)**
   - Phonetic transliteration (yinyi): Chinese characters that approximate the Sanskrit sound, with pinyin
   - Semantic translation (yiyi): Chinese characters chosen for meaning, with pinyin
   - Which translation became standard and in which period
4. **Key translator(s)**: Who produced the translation (e.g., Kumarajiva, Xuanzang, Paramartha)
5. **Translation strategy**: Was this a phonetic borrowing, semantic calque, or hybrid?
6. **Semantic shift**: Did the meaning change, narrow, or expand in Chinese reception?
7. **Source texts**: Sanskrit source text and Chinese translation text (e.g., T.1579 for Yogacarabhumi)

## Guidelines

- Distinguish between early translations (e.g., An Shigao, Lokaksema, 2nd c. CE) and later standardized translations (Kumarajiva 5th c., Xuanzang 7th c.).
- Use standard pinyin for Chinese romanization.
- Note when multiple Chinese translations competed for the same Sanskrit term.
- If a term entered Chinese via Central Asian intermediaries, note this.
- The audience is a philosophy professor, not a sinologist. Explain Chinese Buddhist terminology clearly.
- Do NOT fabricate Taisho catalog numbers or translator attributions. If uncertain, say so.

## Source Discipline

All Taisho numbers, translator attributions, and phonetic reconstructions must be verifiable. Prefer established scholarship (e.g., Karashima, Nattier, Lamotte, Zacchetti).

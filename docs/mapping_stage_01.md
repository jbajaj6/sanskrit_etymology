# Mapping Stage 01 — Sanskrit to Chinese Buddhist Vocabulary

Date: 2026-04-09
Machine-readable source: `data/mappings/sanskrit_chinese_mappings.yaml`

This document presents the first dedicated cross-cultural mapping analysis: how nine core Sanskrit philosophical terms were rendered in Chinese Buddhist translation. The goal is not to claim smooth equivalence but to understand what was preserved, what was changed, and why.

---

## How to Read This Document

### What Counts as Evidence

This project recognizes four kinds of evidence for Sanskrit-Chinese mappings, ranked from strongest to weakest:

1. **Direct attestation** — The Chinese term appears in specific Buddhist texts (identified by Taishō number) as the standard rendering of the Sanskrit term. This is the strongest evidence. Example: 三昧 for samādhi in T01n0001.

2. **Phonetic carryover** — The Chinese characters approximate the *sound* of the Sanskrit (or Prakrit/Gāndhārī) word, indicating direct borrowing rather than translation. Example: 般若 (bōrě) for prajñā, reflecting Prakrit paññā.

3. **Semantic continuity** — The Chinese term captures the *meaning* of the Sanskrit term using native Chinese words. This is translation rather than borrowing. The evidence is strong when the semantic mapping is consistent across many texts and periods. Example: 煩惱 (fánnǎo, "vexation-affliction") for kleśa.

4. **Doctrinal shift** — The Chinese rendering introduces a change in connotation, scope, or metaphysical framework. This is not a failure of translation but evidence of how concepts change when they cross cultural boundaries. Example: 滅 (miè, "extinction") for nirodha, which shifts the meaning from "restraint" toward "annihilation."

### Controlled Vocabularies

**Mapping type**: `transliteration` (sound-based), `semantic_translation` (meaning-based), `hybrid` (both), `broad_equivalent` (approximate), `inconclusive` (insufficient evidence)

**Translation strategy**: `sound_preserving`, `meaning_preserving`, `mixed`, `doctrinal_adaptation`, `unknown`

---

## The Nine Mappings

### Tier 1: Strong, Well-Attested Mappings

These terms have clear, stable, multiply-attested Chinese counterparts.

---

#### 1. dhyāna → 禪那 / 禪 / 禪定 / 靜慮

**Strongest mapping in the project.**

| Chinese | Pinyin | Type | Strategy | Confidence |
|---------|--------|------|----------|------------|
| 禪那 | chánnà | Transliteration | Sound-preserving | High |
| 禪 | chán | Transliteration (abbreviated) | Sound-preserving | High |
| 禪定 | chándìng | Hybrid | Mixed | High |
| 靜慮 | jìnglǜ | Semantic translation | Meaning-preserving | High |

The phonetic chain dhyāna → jhāna → 禪那 → 禪 → chán → zen is one of the best-documented loanword paths in Asian languages. Four distinct Chinese renderings exist, spanning every translation strategy — a richness that itself tells a story about how Chinese Buddhism assimilated this concept.

**What changed in transmission**: The Yoga Sutras define dhyāna narrowly as limb 7 — the unbroken stream of attention between concentration (dhāraṇā) and absorption (samādhi). In Chinese Buddhism, 禪 expanded to name an entire school (Chan/Zen) and a total orientation toward awakening that sometimes de-emphasized the very seated meditation the word originally denoted. Xuanzang's semantic rendering 靜慮 ("quiet contemplation") is a late attempt to recover precision, found throughout his Prajñāpāramitā translations.

---

#### 2. samādhi → 三昧 / 三摩地 / 定

| Chinese | Pinyin | Type | Strategy | Confidence |
|---------|--------|------|----------|------------|
| 三昧 | sānmèi | Transliteration | Sound-preserving | High |
| 三摩地 | sānmódì | Transliteration | Sound-preserving | High |
| 定 | dìng | Semantic translation | Meaning-preserving | Medium |

Samādhi has two competing transliterations: 三昧 (older, more common, reflecting Prakrit samāi) and 三摩地 (Xuanzang's more precise syllable-by-syllable rendering). Both are massively attested. The semantic rendering 定 ("stability") is used alone and as part of compounds (禪定).

**What changed in transmission**: Chinese Buddhism proliferated named samādhis (法華三昧, 念佛三昧, etc.) far beyond the Yoga Sutras' framework, where samādhi is a single specific state. The Chinese usage is broader and more diverse than the Sanskrit original.

---

#### 3. prajñā → 般若 / 慧

| Chinese | Pinyin | Type | Strategy | Confidence |
|---------|--------|------|----------|------------|
| 般若 | bōrě | Transliteration | Sound-preserving | High |
| 慧 | huì | Semantic translation | Meaning-preserving | High |

The coexistence of 般若 (phonetic) and 慧 (semantic) for the same Sanskrit term reveals a deliberate translation principle: when Chinese translators judged a concept to be doctrinally irreducible, they preserved the foreign sound rather than domesticating it. 般若 signals "this requires special understanding" — a form of semantic quarantine that prevents false equivalence with existing Chinese ideas about wisdom.

**What changed in transmission**: 般若 in Chinese carries the full weight of the Prajñāpāramitā tradition (perceiving śūnyatā). The Yoga Sutras' prajñā (perceiving the puruṣa-prakṛti distinction) is a different metaphysical claim wearing the same word.

---

#### 4. kleśa → 煩惱

| Chinese | Pinyin | Type | Strategy | Confidence |
|---------|--------|------|----------|------------|
| 煩惱 | fánnǎo | Semantic translation | Meaning-preserving | High |

One of the most stable mappings in Chinese Buddhist translation. 煩惱 ("vexation-affliction") captures the experiential quality of kleśa — the felt sense of being tormented. Attested from the earliest translations through the latest. Confirmed in compound forms: 煩惱障 (kleśāvaraṇa) in T03n0159 and T03n0160.

**What changed in transmission**: Minor shift from structural cause (Sanskrit) to felt experience (Chinese). The Yoga Sutras' five kleśas are categorical structures; 煩惱 emphasizes how affliction *feels*. A subtle but real difference.

---

#### 5. avidyā → 無明

| Chinese | Pinyin | Type | Strategy | Confidence |
|---------|--------|------|----------|------------|
| 無明 | wúmíng | Semantic translation (calque) | Meaning-preserving | High |

A structural calque: 無 ("without") + 明 ("brightness") mirrors a- ("not") + vidyā ("knowledge"). The Chinese rendering chooses a light/darkness metaphor over an epistemological one — "without clarity" rather than "without knowledge." This is a genuine interpretive choice, not just neutral transfer.

The dependent origination formula 無明緣行 ("avidyā conditions saṃskāra") is confirmed across multiple canonical collections: T01n0003, T02n0099, T02n0124.

**What changed in transmission**: The metaphor shifts from knowledge-failure (Sanskrit) to obscuration/darkness (Chinese). Both are valid readings, but they foreground different phenomenological dimensions. The Chinese image of "darkness" may be more immediately evocative for a non-specialist audience.

---

### Tier 2: Attested but Contextually Limited

These mappings are real and documented but require careful contextual framing.

---

#### 6. nirodha → 滅

| Chinese | Pinyin | Type | Strategy | Confidence |
|---------|--------|------|----------|------------|
| 滅 | miè | Semantic translation | Meaning-preserving | Medium |

滅 ("to extinguish") renders Buddhist nirodha in the Four Noble Truths formula (苦集滅道) — ubiquitous and stable. But the Chinese term is stronger than the Sanskrit: nirodha means "restraint" or "stilling" (ni + √rudh, "to hold back"), while 滅 means "extinction" (as in putting out a fire).

**Why this matters**: Applied to the Yoga Sutras, 滅 would overstate the case. Patañjali's nirodha does not destroy the mind — it quiets it. The difference between "stilling" and "extinguishing" is philosophically consequential. This mapping works for Buddhist contexts but would misrepresent the Yogic concept.

---

#### 7. saṃskāra → 行

| Chinese | Pinyin | Type | Strategy | Confidence |
|---------|--------|------|----------|------------|
| 行 | xíng | Semantic translation | Doctrinal adaptation | Medium |

行 captures the "volitional formation" sense of saṃskāra (Buddhist Abhidharma) but not the "latent subliminal impression" sense (Yoga Sutras). The dependent origination formula (無明緣行) and the five aggregates (色受想行識) are well attested.

**Why this is the most complex mapping**: Sanskrit saṃskāra is radically polysemous — it means "ritual consecration," "latent psychological trace," and "volitional formation" depending on context. Chinese 行 is also radically polysemous — it can render saṃskāra, carya, caryā, and other action-related terms. Two maximally polysemous words mapped to each other creates a situation where the mapping is technically correct but practically ambiguous. Context is everything.

---

### Tier 3: Broad or Weak Mappings

These require heavy caveats and should not be presented as clean equivalences.

---

#### 8. citta → 心

| Chinese | Pinyin | Type | Strategy | Confidence |
|---------|--------|------|----------|------------|
| 心 | xīn | Broad equivalent | Meaning-preserving | Medium |

心 ("heart-mind") is the standard Chinese rendering of citta, but the mapping is broad rather than precise. Three significant gaps:

1. 心 includes emotional and volitional dimensions that the Yoga Sutras' citta does not foreground
2. 心 does not carry the Sāṃkhya framework of citta as material (prakṛti)
3. 心 also renders manas, hṛdaya, and sometimes vijñāna — it is a catch-all, not a precise equivalent

For the professor: a Chinese reader encountering 心 would not automatically understand the Yoga Sutras' claim that the mind is material and must be distinguished from the witnessing self. The Chinese "heart-mind" tradition carries its own deep philosophical history (Mencius, Wang Yangming) that has no counterpart in Patañjali.

---

#### 9. svarūpa → 自性

| Chinese | Pinyin | Type | Strategy | Confidence |
|---------|--------|------|----------|------------|
| 自性 | zìxìng | Broad equivalent | Doctrinal adaptation | Low |

**Weakest mapping in the project.** 自性 corresponds more precisely to svabhāva ("own-being") than to svarūpa ("own-form"). More importantly, in Chinese Buddhist usage 自性 typically appears in contexts that *deny* inherent nature (自性空, "empty of own-nature") — the opposite of the Yoga Sutras' affirmation that puruṣa has a real essential nature.

The Chan/Zen expression 見性 (jiànxìng, "seeing one's nature") looks superficially like YS 1.3 (svarūpe 'vasthānam, "the seer abides in its own form"). But the metaphysics are opposed: Chan says there is no fixed self-nature to find; Yoga says there is.

**Why this mapping is still valuable**: The gap is more instructive than the overlap. Svarūpa and 自性 mark the same philosophical question — "does anything have an essential nature?" — and the two traditions answer it in opposite ways. This is excellent material for cross-cultural analysis precisely because the mapping *fails* as a simple equivalence.

---

## Summary Table

| Sanskrit | Chinese | Type | Confidence | Key Finding |
|----------|---------|------|------------|-------------|
| dhyāna | 禪那/禪/禪定/靜慮 | Transliteration + semantic | High | Strongest case; 4 renderings spanning all strategies |
| samādhi | 三昧/三摩地/定 | Transliteration + semantic | High | Two competing transliterations; concept expanded in China |
| prajñā | 般若/慧 | Transliteration + semantic | High | Phonetic preserved to signal doctrinal weight |
| kleśa | 煩惱 | Semantic | High | Most stable single mapping; structural + felt sense |
| avidyā | 無明 | Semantic (calque) | High | Morphological calque; light/dark metaphor shift |
| nirodha | 滅 | Semantic | Medium | Works for Buddhist context; overstates Yogic sense |
| saṃskāra | 行 | Semantic | Medium | Captures "formation" not "impression"; polysemy issue |
| citta | 心 | Broad equivalent | Medium | Broad catch-all; misses Sāṃkhya framework |
| svarūpa | 自性 | Broad equivalent | Low | Opposite usage (affirm vs. deny); gap is instructive |

---

## What This Stage Reveals

Three patterns emerge from the mapping analysis:

### 1. Sound-preserving translations signal doctrinal importance

When Chinese translators preserved the foreign sound (般若 for prajñā, 禪那 for dhyāna, 三昧 for samādhi), they were making a deliberate choice: this concept is too important or too foreign to domesticate. When they translated the meaning instead (煩惱 for kleśa, 無明 for avidyā), they judged the Chinese rendering adequate. The choice between transliteration and translation is itself evidence of how the Chinese tradition weighted these concepts.

### 2. The strongest mappings are Buddhist, not Yogic

Every strong mapping in this batch comes from Buddhist translation literature. The Yoga Sutras were not systematically translated into Chinese, so terms like vṛtti, viveka-khyāti, kaivalya, and abhyāsa have no Chinese counterparts at all. The mappings that exist connect Sanskrit Buddhist vocabulary to Chinese Buddhist vocabulary — the Yoga Sutras' specialized usage is a secondary comparison, not the source of the Chinese terms.

### 3. The most instructive cases are the failures

Svarūpa → 自性 is the weakest mapping — but it is also the most philosophically illuminating. The fact that the same question ("does anything have an essential nature?") received opposite answers in Yoga and Mādhyamaka Buddhism, and that the Chinese term 自性 became the vehicle for the *denial* of what the Sanskrit term *affirms*, is exactly the kind of finding this project exists to surface.

---

## Evidence Sources Used

- **CBETA** (via buddha-cli): Primary attestation source for all Chinese renderings. Specific texts cited by Taishō number throughout.
- **GRETIL** (via buddha-cli): Sanskrit-side attestation and context.
- **SARIT** (via buddha-cli): Additional Sanskrit attestation.
- **Monier-Williams Sanskrit-English Dictionary**: Morphological analysis.
- **Edgerton, Buddhist Hybrid Sanskrit Dictionary**: Buddhist-specific Sanskrit usage.
- **Soothill & Hodous, A Dictionary of Chinese Buddhist Terms**: Chinese Buddhist terminology (implicit reference for standard renderings).

## Cross-References to Earlier Analyses

No corrections to batches 01–03 are necessary. The mapping data is consistent with the provisional Chinese counterparts noted in the term analyses. The mapping stage deepens and contextualizes those provisional notes — it does not contradict them.

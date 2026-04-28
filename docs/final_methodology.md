# Methodology — Plain Language Summary

## What This Project Does

This project takes Sanskrit philosophical terms — especially those from the Yoga Sutras and Buddhist meditation traditions — and does two things with them:

1. **Breaks them open.** Sanskrit words are built by combining roots, prefixes, and suffixes in precise ways. By taking a word apart into its components, we can see how its literal meaning connects to (or diverges from) its philosophical meaning.

2. **Traces them across cultures.** When Buddhist ideas traveled from India to China, translators had to decide how to render Sanskrit concepts in Chinese. Sometimes they approximated the *sound* of the Sanskrit word (transliteration). Sometimes they translated the *meaning* using native Chinese words. Sometimes they did both. Each choice shaped how the concept was understood in its new cultural setting.

## How the Sanskrit Breakdown Works

Every Sanskrit term is analyzed for:

- **Root** (dhātu): The core verbal root that carries the word's primary meaning. Example: √dhā means "to place."
- **Prefixes** (upasarga): Particles added before the root that modify its direction or intensity. Example: sam- means "together," ā- means "toward."
- **Suffixes** (pratyaya): Endings that determine the word's grammatical category and shade its meaning. Example: -i forms an action noun.
- **Compound type** (if applicable): How two or more words are joined. Sanskrit has a rich compound system with specific structural types (tatpuruṣa, karmadhāraya, bahuvrīhi, etc.).

Putting these together: sam + ā + √dhā + -i = samādhi = "a complete placing-together."

The breakdown is not just a linguistic exercise. It reveals how the ancient grammarians and philosophers *thought about* the concept. The structure of the word is a compressed argument about what the concept means.

In presentation terms, you can think of this as a form of word-level philology: each term is treated like a small constructed object. The analysis asks what parts are present, which of them are structurally important, and what philosophical claim becomes visible once the word is taken apart and put back together.

## Where AI Entered the Workflow

This project did use AI, but in a constrained way.

- A custom Sanskrit analysis workflow generated first-pass breakdowns in a fixed structure: root, prefixes, suffixes, compound type, literal meaning, philosophical meaning, and key textual occurrences.
- A second workflow proposed candidate Chinese Buddhist renderings and classified them as phonetic, semantic, hybrid, or broader equivalents.
- Corpus tools were then used to check whether proposed Chinese forms were actually attested in Buddhist texts and whether the mapping strategy was defensible.

The important point is that AI generated hypotheses and structure, not final authority. Every claim still had to pass through dictionaries, grammatical reference works, and textual evidence.

## How the Chinese Mapping Works

For terms that entered Chinese through Buddhist translation, we evaluate:

- **Attestation**: Does the Chinese rendering actually appear in specific Buddhist texts? We cite texts by their Taishō catalogue number (e.g., T01n0001) to anchor claims in real documents.
- **Mapping type**: Is the Chinese rendering a transliteration (sound-based), a semantic translation (meaning-based), a hybrid, or a broad equivalent?
- **Phonetic evidence**: If transliterated, does the Chinese pronunciation (reconstructed for the historical period) match the Sanskrit or Prakrit source form?
- **Semantic evidence**: If translated, does the Chinese meaning actually correspond to the Sanskrit meaning? Where does it diverge?
- **Doctrinal shift**: Did the Chinese rendering introduce a change in connotation or philosophical framework?

## What Counts as Evidence vs. Interpretation

This project tries to be explicit about the difference:

**Evidence** (things we can verify):
- A Chinese term appears in a specific text (confirmed by corpus search)
- A Sanskrit root has a specific meaning in standard dictionaries (Monier-Williams, Apte)
- A phonetic reconstruction follows established historical linguistics

**Interpretation** (things we argue for):
- What a metaphor shift (e.g., "without knowledge" → "without brightness") means philosophically
- Whether a "broad equivalent" is close enough to count as a real mapping
- Whether a doctrinal shift was intentional or incidental

When the evidence is strong, we say so. When it is weak or contested, we say that too. The project rates every claim with a confidence level (high, medium, low) and flags ambiguity explicitly.

## What This Project Does Not Do

- It does not reconstruct precise historical phonology beyond what standard references support
- It does not claim that similarity between terms proves historical transmission
- It does not treat Chinese Buddhist renderings as equivalent to Yoga Sutras concepts — these are different traditions using overlapping vocabulary
- It does not fabricate etymologies or citations

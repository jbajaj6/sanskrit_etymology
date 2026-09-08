# Sanskrit Etymology & Buddhist Transmission Project

Validated data pipeline and static demo for analyzing Sanskrit meditation and
philosophical vocabulary, drawn from the Yoga Sutras and the principal Upanisads.

## What This Repo Contains

- Canonical term catalog in [data/seed_terms.yaml](data/seed_terms.yaml) — the
  explorer and the catalog now hold the same 126 terms
- Structured analyses in [data/analyses/term_analyses.yaml](data/analyses/term_analyses.yaml)
- Sanskrit-to-Chinese mappings in [data/mappings/sanskrit_chinese_mappings.yaml](data/mappings/sanskrit_chinese_mappings.yaml)
- A working-entry bundle in [data/demo_terms.json](data/demo_terms.json)
- A generated browser demo in [demo/](demo/)
- Research notes and presentation materials in [docs/](docs/)

The software surface is now a small Python package with validation and build commands. The Claude/MCP setup remains optional for interactive research work, but it is no longer the primary way to use the repo.

## Quick Start

### Prerequisites

- Python 3.11+
- `pip`

### Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Validate Canonical Data

```bash
sanskrit-etymology validate-data
```

### Build Demo Artifacts

```bash
sanskrit-etymology build-demo
python3 -m http.server 8000 --directory demo
```

Then open `http://localhost:8000`.

## Reading the Explorer

Every term gets its own address. Opening samādhi puts `#samadhi` in the URL, so a
single term can be linked from a syllabus, a slide, or an email:

```text
https://jbajaj6.github.io/sanskrit_etymology/#samadhi
```

Two labels appear on each term card, and they mean different things:

- **Source-verified / not yet source-verified** — whether a passage from the text
  has actually been quoted and cited for this term. Only terms with an entry in
  `data/analyses/term_analyses.yaml` earn this.
- **Confidence** — how settled the *morphological* analysis is. A term can have a
  high-confidence etymology and still be unsourced; the two are independent.

Terms come from two corpora and the explorer filters by source. Yoga Sutra terms
cite by sutra number (YS 1.2); Upanisadic terms cite by text and verse (BrU 2.4.5,
ChU 6.2.1, MaU 7). Every verified Upanisadic passage was checked against the GRETIL
mula text named in its citation trail, not quoted from memory.

## Cross-references

Terms link to each other, and every link states its basis so it can be checked.

- **Shared morpheme.** Two terms built from the same root, prefix, or suffix link
  from that row of the Word structure section. `nididhyāsana` reaches `dhyāna`
  through the root `√dhyai`; `vidyā` reaches `avidyā` through `√vid`. A morpheme
  shared by more than 20 terms is treated as a grammatical default rather than a
  family, which suppresses the bare `-a` suffix.
- **Named in the entry.** Where one entry's prose discusses another term, it is
  listed under "Discussed in this entry". This catches pairs no shared morpheme
  would, such as `guru` and `ācārya`.

Links are never derived from one term's name containing another's. That would
read `nididhyāsana` as containing `āsana` and `praṇava` as containing `prāṇa`,
both of which are false derivations. See
[relations.py](src/sanskrit_etymology/relations.py).

`sanskrit-etymology validate-data` prints the current sourcing gap as a warning,
and `sanskrit-etymology stats` reports the coverage percentage. It currently
stands at 120 of 126.

Six terms are deliberately left unverified, and each says why on its own card:

- **ahaṃkāra, rajas, tamas, vibhūti, mokṣa** do not occur anywhere in the
  Yogasūtra. A search of all 195 sūtras finds no instance. They are Sāṃkhya
  vocabulary, or later tradition: Patañjali names the guṇas as a set but never
  as a triad, and says kaivalya where other systems say mokṣa.
- **guru**'s locus is Muṇḍaka 1.2.12, and neither the Muṇḍaka nor the Kena is in
  the corpus consulted. See ācārya for the verified Upaniṣadic term.

That five of the six are absences rather than gaps is itself a finding, and the
reason the label distinguishes "not yet source-verified" from "checked and not
there".

Browsing is filtered by thematic bucket (meditation, mind, afflictions, practice,
knowledge, liberation, compounds), and search matches English meanings as well as
Sanskrit — typing `absorption` or `fear of death` finds the relevant terms.

## Free Demo Deployment

This repo is set up for GitHub Pages, which can host the static browser demo for free from a public repository.

1. Push `main` to GitHub:

```bash
git push origin main
```

2. In GitHub, open `Settings -> Pages`.
3. Under `Build and deployment`, set `Source` to `GitHub Actions`.
4. Open the `Actions` tab and run or wait for `Deploy demo to GitHub Pages`.

After the workflow succeeds, the class demo should be available at:

```text
https://jbajaj6.github.io/sanskrit_etymology/
```

## Supported Commands

```bash
sanskrit-etymology validate-data
sanskrit-etymology build-demo
sanskrit-etymology stats
```

## Project Layout

```text
data/
  analyses/        Canonical morphological analyses
  demo_terms.json  Source bundle for the 84-term browser demo
  mappings/        Canonical Sanskrit-Chinese mappings
  seed_terms.yaml  Canonical term catalog
demo/
  assets/          Static CSS/JS for the browser demo
  terms.json       Generated demo dataset
  terms_inline.js  Generated offline-friendly demo payload
docs/              Research notes, paper draft, presentation scripts
src/
  sanskrit_etymology/
                   Package code, validation, and build pipeline
tests/             Pipeline regression tests
```

## Data Flow

The canonical philology sources of truth are:

1. `data/seed_terms.yaml`
2. `data/analyses/term_analyses.yaml`
3. `data/mappings/sanskrit_chinese_mappings.yaml`

The browser demo is built from `data/demo_terms.json`, with canonical analyses and mappings merged in where IDs overlap. Do not edit `demo/terms.json` or `demo/terms_inline.js` by hand; regenerate them with `sanskrit-etymology build-demo`.

A term reaches the explorer as *source-verified* only by way of
`data/analyses/term_analyses.yaml`, which is the file that carries `source_context`
and `citation_trail`. Adding a term to `data/demo_terms.json` alone makes it
browsable but leaves it explicitly labelled unverified on the page. Promoting a
term is therefore a deliberate act: write the analysis entry, quote the passage,
record the citations.

`priority_bucket` values are `must`, `nice`, `stretch`, and `extended`. The first
three are the analysis queue; `extended` marks terms that are carried in the
explorer without being queued for canonical analysis.

## Optional Claude / MCP Workflow

If you use Claude Code, the repo still includes:

- `.claude/skills/` for philology-specific prompts and guardrails
- `.mcp.json` for optional MCP server wiring

Those files are now auxiliary to the core package/CLI workflow rather than the definition of the project itself.

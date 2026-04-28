# Sanskrit Etymology & Buddhist Transmission Project

Validated data pipeline and static demo for analyzing Sanskrit meditation vocabulary and tracing Buddhist concept transmission from India to China.

## What This Repo Contains

- Canonical term catalog in [data/seed_terms.yaml](data/seed_terms.yaml)
- Structured analyses in [data/analyses/term_analyses.yaml](data/analyses/term_analyses.yaml)
- Sanskrit-to-Chinese mappings in [data/mappings/sanskrit_chinese_mappings.yaml](data/mappings/sanskrit_chinese_mappings.yaml)
- An 84-term demo source bundle in [data/demo_terms.json](data/demo_terms.json)
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

## Optional Claude / MCP Workflow

If you use Claude Code, the repo still includes:

- `.claude/skills/` for philology-specific prompts and guardrails
- `.mcp.json` for optional MCP server wiring

Those files are now auxiliary to the core package/CLI workflow rather than the definition of the project itself.

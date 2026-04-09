# Sanskrit Etymology & Buddhist Transmission Project

Computational philology tooling for analyzing Sanskrit meditation vocabulary and tracing Buddhist concept transmission from India to China.

## Setup

This project is designed to be used with [Claude Code](https://claude.com/claude-code).

### Prerequisites

- Node.js (v18+)
- Python 3.9+ with `uvx` (for MCP fetch server)
- Rust toolchain (installed automatically by buddha-cli bootstrap)
- Claude Code CLI

### MCP Servers

Configured in `.mcp.json`:

| Server | Purpose | Status |
|--------|---------|--------|
| `buddha` | Buddhist text corpus search/fetch (CBETA, GRETIL, SARIT, MUKTABODHA, Tipitaka) | Installed and indexed |
| `fetch` | General web content retrieval | Configured |
| `filesystem` | Local file read/write scoped to project | Configured |

### Custom Skills

Located in `.claude/skills/<name>/SKILL.md`:

| Skill | Purpose |
|-------|---------|
| `sanskrit-term-breakdown` | Morphological + philosophical analysis of Sanskrit terms |
| `buddhist-term-mapper` | Map Sanskrit to Chinese Buddhist equivalents |
| `corpus-ingest-tei` | Parse TEI-XML source texts |
| `philology-presentation-writer` | Generate class presentation materials |
| `source-discipline` | Enforce sourcing rigor on all outputs |

### Directory Structure

```
data/raw/          — Original source texts
data/processed/    — Cleaned structured data
src/ingest/        — Text ingestion
src/lexicon/       — Term analysis
src/mapping/       — Sanskrit-Chinese mapping
src/utils/         — Shared utilities
notebooks/         — Exploratory analysis
docs/              — Documentation and presentations
```

## Usage

Start Claude Code in this directory. The skills and MCP servers will be available automatically.

Example commands:
```
/sanskrit-term-breakdown samadhi
/buddhist-term-mapper dhyana
/philology-presentation-writer
```

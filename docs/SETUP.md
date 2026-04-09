# Setup Summary

Date: 2026-04-08 (revised)

## What Was Set Up

### MCP Servers (in `.mcp.json`)

| Server | Status | Notes |
|--------|--------|-------|
| **buddha** | Installed and verified | `~/.buddha/bin/buddha mcp` — buddha-cli v0.6.13 (formerly daizo-mcp). Full Buddhist text MCP with search, fetch, and indexing across CBETA, GRETIL, SARIT, MUKTABODHA, and Pali Tipitaka. All corpora downloaded and indexed. Verified via `buddha doctor --verbose`. |
| **fetch** | Configured | `uvx mcp-server-fetch` — verified working. General web content retrieval. |
| **filesystem** | Configured | `npx @modelcontextprotocol/server-filesystem` — scoped to project directory. Structured file read/write. |

### MCP Servers NOT Installed (and why)

| Server | Status | Reason |
|--------|--------|--------|
| **github MCP** | Not configured | `@modelcontextprotocol/server-github` exists on npm but requires a `GITHUB_PERSONAL_ACCESS_TOKEN`. Can be added later if you push to GitHub. |
| **CbetaMCP (standalone)** | Not needed | A separate Python project exists at `github.com/tendayspace/cbetamcp`, but buddha-cli already includes full CBETA corpus access with indexing, making it redundant. |

### Buddha-CLI Details

Installed at `~/.buddha/` via the official bootstrap script. Built from source using Rust (rustup was installed as a prerequisite).

**Corpora downloaded and indexed:**
- CBETA xml-p5 (4,990 texts indexed)
- Pali Tipitaka romn (217 texts indexed)
- SARIT TEI P5 (85 texts indexed)
- MUKTABODHA IAST (499 texts indexed)
- GRETIL Sanskrit (downloaded, zip extracted)
- Online access: SAT, Jodo Shu Zensho, Tibetan (BUDA/BDRC)

**MCP tools exposed:** search (regex across corpora), fetch (text by ID with context), title-search, pipelines (multi-file summarization), cbeta-index, tipitaka-index, sarit-index, muktabodha-index.

### Custom Skills (in `.claude/skills/`)

Skills use the folder structure: `.claude/skills/<skill-name>/SKILL.md`

| Skill | Path | Purpose |
|-------|------|---------|
| `sanskrit-term-breakdown` | `sanskrit-term-breakdown/SKILL.md` | Decompose a Sanskrit term into roots, prefixes, suffixes, compound type, literal meaning, philosophical meaning |
| `buddhist-term-mapper` | `buddhist-term-mapper/SKILL.md` | Map Sanskrit terms to Chinese Buddhist equivalents with phonetic/semantic evidence |
| `corpus-ingest-tei` | `corpus-ingest-tei/SKILL.md` | Parse TEI-XML texts from GRETIL, SARIT, or CBETA into structured data |
| `philology-presentation-writer` | `philology-presentation-writer/SKILL.md` | Generate presentation materials for a non-technical philosophy audience |
| `source-discipline` | `source-discipline/SKILL.md` | Enforce citation rigor — no fabricated etymologies, references, or attributions |

Each SKILL.md has YAML frontmatter with `name`, `description`, and `user-invocable: true`.

### Project Scaffold

```
sanskrit_etymology/
  .claude/skills/
    sanskrit-term-breakdown/SKILL.md
    buddhist-term-mapper/SKILL.md
    corpus-ingest-tei/SKILL.md
    philology-presentation-writer/SKILL.md
    source-discipline/SKILL.md
  .mcp.json                — MCP server configuration (buddha, fetch, filesystem)
  .gitignore               — Ignores data/*, caches, OS files
  CLAUDE.md                — Project context for Claude Code
  README.md                — Human-readable setup guide
  data/raw/                — For original source texts
  data/processed/          — For cleaned/structured data
  src/ingest/              — Text ingestion code (future)
  src/lexicon/             — Term analysis code (future)
  src/mapping/             — Sanskrit-Chinese mapping code (future)
  src/utils/               — Shared utilities (future)
  notebooks/               — Exploratory analysis (future)
  docs/                    — Documentation and presentations
```

Git initialized. No initial commit made yet.

## Manual Steps Still Needed

1. **Approve MCP servers**: Next time you start Claude Code in this directory, it will prompt you to approve the `buddha`, `fetch`, and `filesystem` MCP servers. Say yes to all three.

2. **GitHub MCP (optional)**: If you want GitHub integration later:
   - Create a GitHub Personal Access Token
   - Add to `.mcp.json`:
     ```json
     "github": {
       "command": "npx",
       "args": ["-y", "@modelcontextprotocol/server-github"],
       "env": {
         "GITHUB_PERSONAL_ACCESS_TOKEN": "<your-token>"
       }
     }
     ```

3. **Initial commit**: Done (2026-04-08). Scaffold committed as `fed0bd2`.

## What Was Installed as a Side Effect

- **Rust toolchain** (rustup/cargo) at `~/.cargo/` — needed to build buddha-cli from source
- **Buddha-cli corpora** at `~/.buddha/` (~500MB total) — CBETA, GRETIL, SARIT, MUKTABODHA, Tipitaka
- **PATH modification** in `~/.zshrc` — adds `~/.buddha/bin` and `~/.buddha/PATH` exports

## Smoke Test — 2026-04-08

All components verified end-to-end:

| Component | Result | Detail |
|-----------|--------|--------|
| `.mcp.json` | Valid | Three servers configured (buddha, fetch, filesystem) |
| `buddha` MCP | Working | v0.6.13, all 5 corpora available. Search for "samadhi" in GRETIL returned results. |
| `fetch` MCP | Working | Successfully fetched httpbin.org test endpoint. |
| `filesystem` MCP | Working | Listed project directory contents correctly. |
| `/sanskrit-term-breakdown` skill | Working | Invoked on "dharma" — skill loaded and produced structured output. |

No issues found. Setup is fully operational.

## Next Steps When You Want to Begin the Actual Project

1. Start with `/sanskrit-term-breakdown samadhi` to test the skill on a known term.
2. Use the buddha MCP to search corpora directly (e.g., search for "samadhi" across GRETIL Sanskrit texts).
3. Use `/corpus-ingest-tei` to bring in a Yoga Sutras text from GRETIL or SARIT.
4. Build the term lexicon one term at a time using the breakdown skill.
5. When ready for Chinese comparison, use `/buddhist-term-mapper` on key terms like dhyana.
6. Use `/philology-presentation-writer` to format findings for class.

# The Middle Powers Monitor

A multi-agent system that produces weekly geopolitical intelligence briefs covering 28 countries across 5 regions. Uses Claude for collection, analysis, and editorial synthesis. Published at [middlepowers.fyi](https://middlepowers.fyi).

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set API keys (or use .env file)
export ANTHROPIC_API_KEY="sk-ant-..."
export BRAVE_API_KEY="..."
export SEARCHAPI_KEY="..."

# Run the full weekly pipeline
python -m src.monitor run --date 2026-02-08

# Resume from assembly (if pipeline failed after country agents)
python -m src.monitor assemble --date 2026-02-08

# Publish site pages from ledger data (no editing)
python -m src.monitor publish --date 2026-02-08
```

## Pipeline

```
Layer 2 Collection (government source search + extraction)
  → Expansion (Brave News search: actors, vocab, wire/domestic)
  → Story Map (cluster search results into story groups)
  → Extraction (full-text retrieval of representative articles)
  → Country Agent (per-country analytical assessment)
  → Devil's Advocate (adversarial review)
  → Ledger Write (persist to country ledgers)
  → Regional Synthesis (cross-country dynamics per region)
  → Executive Synthesis (top-level briefing items)
  → Newsletter Assembly (render to Markdown/MDX)
  → Editor (rewrite into narrative prose per country/region/executive)
  → Watchlist Editor (rewrite watchlist into prose)
  → Copyeditor (style and consistency pass)
  → Card Summary (Haiku condensation for overview cards)
  → Publish (Mintlify site with archives management)
```

## Traces

Every LLM call saves a trace to `briefs/{date}/traces/` for inspection and recovery:

```
government_{code}.json     — Layer 2 agent (28 per run)
story_map_{code}.json      — Story map agent (28 per run)
country_{code}.json        — Country agent (28 per run)
devils_advocate_{code}.json — Devil's advocate (28 per run)
regional_{region}.json     — Regional synthesis (5 per run)
executive.json             — Executive synthesis (1 per run)
editor_{code}.json         — Country editor (28 per run)
editor_regional_{region}.json — Regional editor (5 per run)
editor_executive.json      — Executive editor (1 per run)
editor_watchlist.json      — Watchlist editor (1 per run)
copyeditor_{label}.json    — Copyeditor (variable per run)
```

## Project Structure

```
pdb/
├── src/monitor/           # Pipeline code
│   ├── cli.py             # CLI entry point
│   ├── orchestrator.py    # Pipeline orchestration
│   ├── config.py          # Model config, paths, prompt loading
│   ├── models.py          # Data models (ledger, weekly entry, etc.)
│   ├── trace.py           # LLM trace persistence
│   ├── agents/            # LLM agents
│   │   ├── country.py     # Country desk analyst
│   │   ├── story_map.py   # Story clustering (with json_repair fallback)
│   │   ├── editor.py      # Prose editor (country, regional, executive, watchlist)
│   │   ├── copyeditor.py  # Style/consistency pass
│   │   ├── regional.py    # Cross-country synthesis
│   │   ├── executive.py   # Global synthesis + watchlist
│   │   ├── government.py  # Government source analysis
│   │   ├── expansion.py   # Search expansion
│   │   └── devils_advocate.py
│   ├── collection/        # Search and extraction
│   │   ├── brave.py       # Brave News API
│   │   ├── searchapi.py   # Google via SearchAPI
│   │   ├── extract.py     # Multi-method extraction (curl, diffbot, browserbase)
│   │   └── guardian.py    # Guardian API
│   ├── newsletter/        # Assembly and publishing
│   │   ├── assembly.py    # MDX page rendering
│   │   └── publish.py     # Site publishing + archives management
│   └── ledger/            # Ledger storage and management
├── assets/
│   ├── prompts/           # Agent prompt templates
│   └── country_configs/   # Per-country config (actors, domains, goggles)
├── docs/                  # Style guide
├── ledgers/               # Country ledgers, regional reports, story maps
├── briefs/                # Pipeline output (traces, newsletter markdown)
├── site/                  # Mintlify site
│   ├── briefs/            # Published brief pages (MDX)
│   ├── docs.json          # Site navigation config
│   └── about.mdx          # About page
└── tests/monitor/         # Test suite (~1100 tests)
```

## Configuration

API keys via environment variables or `.env` file:

```bash
ANTHROPIC_API_KEY=sk-ant-...     # Required — Claude API
BRAVE_API_KEY=...                # Required — Brave Search
SEARCHAPI_KEY=...                # Required — Google via SearchAPI
DIFFBOT_API_KEY=...              # Optional — Diffbot extraction
BROWSERBASE_API_KEY=...          # Optional — Browserbase extraction
BROWSERBASE_PROJECT_ID=...       # Optional — Browserbase project
GUARDIAN_API_KEY=...             # Optional — Guardian API
```

## Development

```bash
# Run full test suite (excludes E2E tests that make API calls)
pytest tests/ --ignore=tests/monitor/test_e2e_mexico.py -q

# Run specific test modules
pytest tests/monitor/test_story_map.py -q
pytest tests/monitor/test_newsletter.py -q
```

## License

MIT

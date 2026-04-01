# PDB — Geopolitical Intelligence Monitor

A multi-agent system that produces weekly geopolitical intelligence briefs covering 28 countries across 5 regions. Uses Claude for collection, analysis, and editorial synthesis.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set API key
export ANTHROPIC_API_KEY="your-api-key"

# Run the weekly pipeline for a given date
python -m src.monitor.cli run --date 2026-01-26

# Publish assembled brief (no LLM editing)
python -m src.monitor.cli publish --date 2026-01-26

# Force deep dive on all 28 countries (skips triage)
python -m src.monitor.cli run --date 2026-01-26 --force-deep-dive
```

## Pipeline

```
Collection (Layer 1 + Layer 2)
    → Triage (deep-dive vs maintenance per country)
    → Expansion (search augmentation for deep-dive countries)
    → Story Map (cluster media coverage into story groups)
    → Extraction (full-text retrieval of key articles)
    → Country Agents (per-country analytical assessment)
    → Devil's Advocate (adversarial review)
    → Ledger Write (persist to country ledgers)
    → Regional Synthesis (cross-country dynamics per region)
    → Executive Synthesis (top-level brief)
    → Newsletter Assembly (render to Markdown/MDX)
    → Editor → Copyeditor (prose polish)
    → Page Assembly → Publish (Mintlify site)
```

## Project Structure

```
pdb/
├── src/monitor/           # v4 pipeline
│   ├── cli.py             # CLI entry point
│   ├── orchestrator.py    # Pipeline orchestration
│   ├── config.py          # Model config, paths, prompt loading
│   ├── models.py          # Data models (ledger, weekly entry, etc.)
│   ├── agents/            # LLM agents (country, editor, copyeditor, etc.)
│   ├── collection/        # Layer 1/2 collection and extraction
│   ├── newsletter/        # Assembly and publishing
│   └── trace.py           # LLM trace persistence
├── assets/prompts/        # Agent prompt templates
├── docs/                  # Style guide, architecture docs
├── ledgers/               # Country ledgers and story maps
├── site/                  # Mintlify site (briefs, dossiers, pages)
└── tests/monitor/         # Test suite
```

## Configuration

```bash
ANTHROPIC_API_KEY=sk-ant-...    # Required
LOG_LEVEL=INFO                   # Optional: DEBUG, INFO, WARNING, ERROR
```

## Development

```bash
# Run tests
pytest tests/monitor/ -v

# Run a specific test
pytest tests/monitor/test_story_map.py -v
```

## License

MIT

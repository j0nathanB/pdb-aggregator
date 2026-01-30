# Presidential Daily Brief Aggregator

A multi-agent system that generates weekly intelligence briefs tracking world leaders. Uses LLM-powered agents for source aggregation, translation, classification, and synthesis.

## Features

- **Multi-tier source aggregation**: Wire services (Reuters, AP, AFP) + domestic press in native languages
- **Automatic translation**: Political/diplomatic-aware translation preserving nuance
- **Paragon taxonomy classification**: Event type, leader role, impact level scoring
- **Cross-cutting thread detection**: Identifies themes connecting multiple leaders
- **Structured output**: JSON data + human-readable Markdown briefs

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set API key
export ANTHROPIC_API_KEY="your-api-key"

# List tracked leaders
python -m src.main --list-leaders

# Run for a single leader (good for testing)
python -m src.main --leader "Mark Carney"

# Full run with all 10 leaders
python -m src.main

# Custom date range
python -m src.main --start 2026-01-13 --end 2026-01-21

# List previous briefs
python -m src.main --list-briefs
```

## Project Structure

```
pdb-aggregator/
├── requirements.txt
├── README.md
└── src/
    ├── __init__.py
    ├── config.py          # Data models, taxonomy weights, leader configs
    ├── graph.py           # PDBWorkflow orchestration
    ├── main.py            # CLI entry point
    ├── persistence.py     # Brief storage (JSON + Markdown)
    └── agents/
        ├── base.py            # Shared LLM client, retry logic, utilities
        ├── global_pulse.py    # Fetches top world stories for context
        ├── source_fetcher.py  # Multi-source article fetching
        ├── translator.py      # Non-English content translation
        ├── classifier.py      # Paragon taxonomy classification
        ├── dossier_builder.py # Per-leader dossier synthesis
        ├── thread_detector.py # Cross-cutting theme detection
        └── synthesizer.py     # Executive summary generation
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      PDBWorkflow                            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    GlobalPulseAgent                         │
│              (Top 5 world stories for context)              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              Per-Leader Pipeline (parallel)                 │
│                                                             │
│   SourceFetcher → Translator → Classifier → DossierBuilder │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   ThreadDetectorAgent                       │
│            (Semantic clustering across leaders)             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    SynthesizerAgent                         │
│        (Executive summary + regional context)               │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Persistence                            │
│              (briefs/YYYYMMDD/brief.md + JSON)              │
└─────────────────────────────────────────────────────────────┘
```

## Paragon Taxonomy

Articles are classified on three dimensions:

| Dimension | Values | Weight Range |
|-----------|--------|--------------|
| **Event Type** | policy_announcement, international_visit, major_speech, cabinet_change, legal_development, bilateral_agreement, crisis_response, economic_action, other | 0.10 - 0.35 |
| **Leader Role** | initiator, participant, subject | 0.10 - 0.40 |
| **Impact Level** | international, national, regional, local | 0.05 - 0.25 |

**Priority Score** = (event_weight + role_weight + impact_weight) / 1.0

Articles with priority < 0.4 are filtered out.

## Tracked Leaders

| Region | Leader | Title | Country |
|--------|--------|-------|---------|
| Americas | Mark Carney | Prime Minister | Canada |
| Americas | Claudia Sheinbaum | President | Mexico |
| Europe | Volodymyr Zelenskyy | President | Ukraine |
| Europe | Emmanuel Macron | President | France |
| Europe | Friedrich Merz | Chancellor | Germany |
| Europe | Keir Starmer | Prime Minister | UK |
| Europe | Karol Nawrocki | President | Poland |
| Europe | Alexander Stubb | President | Finland |
| Europe | Mark Rutte | Secretary General | NATO |
| Asia-Pacific | Xi Jinping | President | China |

## Output Format

Briefs are saved to `briefs/YYYYMMDD/`:

```
briefs/
  20260121/
    brief.md          # Human-readable Markdown
    dossiers.json     # Structured leader data
    threads.json      # Cross-cutting threads
    meta.json         # Brief metadata
    output.json       # Full serialized state
```

## Python API

```python
import asyncio
from src.graph import PDBWorkflow

async def main():
    workflow = PDBWorkflow()
    
    # Full run
    brief = await workflow.run(
        date_range_start="2026-01-13",
        date_range_end="2026-01-21",
    )
    
    print(f"Threads: {len(brief.cross_cutting_threads)}")
    print(brief.executive_summary)
    
    # Single leader
    dossier = await workflow.run_single_leader("Emmanuel Macron")
    print(dossier.assessment)

asyncio.run(main())
```

## Configuration

### Environment Variables

```bash
ANTHROPIC_API_KEY=sk-ant-...    # Required
LOG_LEVEL=INFO                   # Optional: DEBUG, INFO, WARNING, ERROR
```

### Customizing Leaders

Edit `src/config.py` → `get_leader_configs()` to add/remove leaders or modify their domestic sources.

### Adjusting Thresholds

In `src/config.py`:
- `RELEVANCE_THRESHOLD` (default 0.4): Minimum priority score
- `EVENT_TYPE_WEIGHTS`, `LEADER_ROLE_WEIGHTS`, `IMPACT_LEVEL_WEIGHTS`: Taxonomy weights

## Current Limitations

1. **News fetching is placeholder**: RSS feeds work, but non-RSS sources use LLM-generated placeholders. Integrate NewsAPI/Google News for production.

2. **Thread detection uses LLM clustering**: Works but is slower than embedding-based DBSCAN. The embedding approach is stubbed in `thread_detector.py`.

3. **No real-time data**: Relies on LLM knowledge + RSS. Add web search integration for current events.

4. **Translation quality**: Political nuance may be lost. Consider human review for critical content.

## Development

```bash
# Run tests
pytest tests/ -v

# Format
black src/

# Lint
ruff check src/

# Type check
mypy src/
```

## Roadmap

- [ ] Integrate NewsAPI or Google News API for real article fetching
- [ ] Add embedding-based thread detection (sentence-transformers + DBSCAN)
- [ ] Add web search tool for current events
- [ ] Comprehensive test suite
- [ ] Week-over-week trajectory analysis
- [ ] DOCX/PDF export
- [ ] Scheduled runs (cron/Airflow)
- [ ] Web UI for viewing briefs

## License

MIT
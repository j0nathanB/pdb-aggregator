# Presidential Daily Brief Aggregator

An agentic news aggregator that produces weekly intelligence briefs tracking world leaders using:
- **Multi-tier source aggregation** (wire services + domestic press)
- **Translator agent** for non-English sources
- **Paragon taxonomy classification** (event type, leader role, impact level)
- **Cross-cutting thread detection** via semantic clustering
- **LangGraph orchestration** for the full pipeline

## Quick Start

### Installation

```bash
# Clone or copy the project
cd pdb-aggregator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt

# Set API key
export ANTHROPIC_API_KEY="your-api-key"
```

### Basic Usage

```bash
# Full run with all 10 leaders
python -m src.main

# Single leader (useful for testing)
python -m src.main --leader "Claudia Sheinbaum"

# Custom date range
python -m src.main --start 2026-01-13 --end 2026-01-21

# Simple pipeline without LangGraph (for debugging)
python -m src.main --simple --leader "Mark Carney"

# List stored briefs
python -m src.main --list-briefs
```

### Python API

```python
import asyncio
from src.graph import PDBWorkflow

async def main():
    workflow = PDBWorkflow()
    
    # Full run
    state = await workflow.run(
        date_range_start="2026-01-13",
        date_range_end="2026-01-21",
    )
    
    print(f"Threads detected: {len(state['threads'])}")
    for thread in state['threads']:
        print(f"  - {thread['title']} ({thread['leader_count']} leaders)")

asyncio.run(main())
```

## Architecture

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                     ORCHESTRATOR                             â”‚
â”‚                    (LangGraph Entry)                         â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                              â”‚
                              â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                    GLOBAL PULSE                              â”‚
â”‚         (Top 5 world stories for context)                    â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                              â”‚
                              â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚              PARALLEL LEADER AGENTS (10x)                    â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”        â”‚
â”‚  â”‚ Carney  â”‚  â”‚Sheinbaumâ”‚  â”‚Zelenskyyâ”‚  â”‚  ...    â”‚        â”‚
â”‚  â””â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”˜  â””â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”˜  â””â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”˜  â””â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”˜        â”‚
â”‚       â”‚            â”‚            â”‚            â”‚              â”‚
â”‚  â”Œâ”€â”€â”€â”€â–¼â”€â”€â”€â”€â”  â”Œâ”€â”€â”€â”€â–¼â”€â”€â”€â”€â”  â”Œâ”€â”€â”€â”€â–¼â”€â”€â”€â”€â”  â”Œâ”€â”€â”€â”€â–¼â”€â”€â”€â”€â”        â”‚
â”‚  â”‚ SOURCE  â”‚  â”‚ SOURCE  â”‚  â”‚ SOURCE  â”‚  â”‚ SOURCE  â”‚        â”‚
â”‚  â”‚ FETCHER â”‚  â”‚ FETCHER â”‚  â”‚ FETCHER â”‚  â”‚ FETCHER â”‚        â”‚
â”‚  â””â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”˜  â””â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”˜  â””â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”˜  â””â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”˜        â”‚
â”‚       â”‚            â”‚            â”‚            â”‚              â”‚
â”‚  â”Œâ”€â”€â”€â”€â–¼â”€â”€â”€â”€â”  â”Œâ”€â”€â”€â”€â–¼â”€â”€â”€â”€â”  â”Œâ”€â”€â”€â”€â–¼â”€â”€â”€â”€â”  â”Œâ”€â”€â”€â”€â–¼â”€â”€â”€â”€â”        â”‚
â”‚  â”‚TRANSLATEâ”‚  â”‚TRANSLATEâ”‚  â”‚TRANSLATEâ”‚  â”‚TRANSLATEâ”‚        â”‚
â”‚  â””â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”˜  â””â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”˜  â””â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”˜  â””â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”˜        â”‚
â”‚       â”‚            â”‚            â”‚            â”‚              â”‚
â”‚  â”Œâ”€â”€â”€â”€â–¼â”€â”€â”€â”€â”  â”Œâ”€â”€â”€â”€â–¼â”€â”€â”€â”€â”  â”Œâ”€â”€â”€â”€â–¼â”€â”€â”€â”€â”  â”Œâ”€â”€â”€â”€â–¼â”€â”€â”€â”€â”        â”‚
â”‚  â”‚CLASSIFY â”‚  â”‚CLASSIFY â”‚  â”‚CLASSIFY â”‚  â”‚CLASSIFY â”‚        â”‚
â”‚  â””â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”˜  â””â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”˜  â””â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”˜  â””â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”˜        â”‚
â”‚       â”‚            â”‚            â”‚            â”‚              â”‚
â”‚  â”Œâ”€â”€â”€â”€â–¼â”€â”€â”€â”€â”  â”Œâ”€â”€â”€â”€â–¼â”€â”€â”€â”€â”  â”Œâ”€â”€â”€â”€â–¼â”€â”€â”€â”€â”  â”Œâ”€â”€â”€â”€â–¼â”€â”€â”€â”€â”        â”‚
â”‚  â”‚ FILTER  â”‚  â”‚ FILTER  â”‚  â”‚ FILTER  â”‚  â”‚ FILTER  â”‚        â”‚
â”‚  â”‚ (>0.4)  â”‚  â”‚ (>0.4)  â”‚  â”‚ (>0.4)  â”‚  â”‚ (>0.4)  â”‚        â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜        â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                              â”‚
                              â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                        REDUCER                               â”‚
â”‚               (Merge all leader dossiers)                    â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                              â”‚
                              â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚               CROSS-CUTTING THREAD DETECTION                 â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”       â”‚
â”‚  â”‚   Extract    â”‚  â”‚   Semantic   â”‚  â”‚   Thread     â”‚       â”‚
â”‚  â”‚  Underlying  â”‚â”€â”€â–¶â”‚  Clustering  â”‚â”€â”€â–¶â”‚  Synthesis   â”‚       â”‚
â”‚  â”‚   Events     â”‚  â”‚   (DBSCAN)   â”‚  â”‚              â”‚       â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜       â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                              â”‚
                              â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                    SYNTHESIS AGENTS                          â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”       â”‚
â”‚  â”‚  Executive   â”‚  â”‚ Per-Leader   â”‚  â”‚  Regional    â”‚       â”‚
â”‚  â”‚  Summary     â”‚  â”‚   Briefs     â”‚  â”‚  Context     â”‚       â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜       â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                              â”‚
                              â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                    BRIEF COMPILER                            â”‚
â”‚         (Markdown + JSON + Appendices)                       â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

## Classification Taxonomy (Paragon)

### Event Types
| Type | Description | Weight |
|------|-------------|--------|
| POLICY_ANNOUNCEMENT | New policy, law, regulation | 0.35 |
| INTERNATIONAL_VISIT | Foreign travel, hosting leaders | 0.30 |
| MAJOR_SPEECH | Significant public address | 0.30 |
| CABINET_CHANGE | Government personnel changes | 0.25 |
| LEGAL_DEVELOPMENT | Court rulings, investigations | 0.25 |
| BILATERAL_AGREEMENT | Treaties, deals, MOUs | 0.30 |
| CRISIS_RESPONSE | Emergency actions | 0.35 |
| ECONOMIC_ACTION | Tariffs, sanctions, fiscal | 0.25 |
| OTHER | Doesn't fit above | 0.10 |

### Leader Role
| Role | Description | Weight |
|------|-------------|--------|
| INITIATOR | Driving the action | 0.40 |
| PARTICIPANT | Involved but not driving | 0.25 |
| SUBJECT | Being reported on | 0.10 |

### Impact Level
| Level | Description | Weight |
|-------|-------------|--------|
| INTERNATIONAL | Multiple countries | 0.25 |
| NATIONAL | Country-wide | 0.20 |
| REGIONAL | Sub-national region | 0.10 |
| LOCAL | Limited local | 0.05 |

**Priority Score** = (Event Type Weight + Leader Role Weight + Impact Level Weight) / Max

**Threshold**: Articles with priority < 0.4 are filtered out.

## Tracked Leaders

| Leader | Title | Country | Domestic Sources |
|--------|-------|---------|------------------|
| Mark Carney | Prime Minister | Canada | Globe & Mail, CBC, National Post |
| Claudia Sheinbaum | President | Mexico | El Universal, Reforma, La Jornada |
| Volodymyr Zelenskyy | President | Ukraine | Ukrinform, Kyiv Independent |
| Emmanuel Macron | President | France | Le Monde, Le Figaro, LibÃ©ration |
| Friedrich Merz | Chancellor | Germany | FAZ, SÃ¼ddeutsche, Der Spiegel |
| Keir Starmer | Prime Minister | UK | BBC, Guardian, Telegraph |
| Karol Nawrocki | President | Poland | Gazeta Wyborcza, Rzeczpospolita |
| Alexander Stubb | President | Finland | Helsingin Sanomat, Yle |
| Mark Rutte | NATO Secretary General | NATO | NATO Press |
| Xi Jinping | President | China | Xinhua*, SCMP, Caixin |

*State media analyzed separately (messaging vs. reality)

## Output Structure

```
briefs/
  20260121/
    brief.md          # Human-readable brief
    dossiers.json     # Structured leader data
    threads.json      # Cross-cutting threads
    meta.json         # Brief metadata
    output.json       # Full output
```

### Brief Sections
1. **Executive Summary** - 3-4 paragraphs on key developments
2. **Cross-Cutting Threads** - Themes connecting multiple leaders
3. **Leader Briefs** - Per-leader analysis with actions, context, assessment
4. **Regional Context** - Europe, Americas, Asia-Pacific
5. **Source Quality Notes** - Gaps and reliability caveats
6. **Appendix: Sources** - Full source table
7. **Appendix: Methodology** - Classification details

## Configuration

### Environment Variables
```bash
ANTHROPIC_API_KEY=sk-ant-...    # Required
LOG_LEVEL=INFO                   # Optional: DEBUG, INFO, WARNING, ERROR
```

### Customization

Edit `src/config.py` to:
- Add/remove tracked leaders
- Configure source URLs and selectors
- Adjust priority weights and thresholds
- Modify regional groupings

## Development

```bash
# Run tests
pytest tests/ -v

# Format code
black src/

# Lint
ruff check src/

# Type check
mypy src/
```

## Known Limitations

1. **Paywalled sources**: Some domestic sources may require subscription
2. **Rate limits**: API calls are rate-limited; full runs take ~10-15 minutes
3. **RSS availability**: Not all sources have RSS feeds
4. **Translation quality**: Political nuance may be lost in translation
5. **Thread detection**: Requires 2+ leaders mentioning same underlying event

## Roadmap

- [ ] Add more sources (Proceso, Animal PolÃ­tico, etc.)
- [ ] Implement proper web search integration
- [ ] Add trajectory analysis (week-over-week)
- [ ] Support for more languages (Chinese, Arabic)
- [ ] DOCX/PDF export
- [ ] Web UI for brief viewing
- [ ] Scheduled weekly runs (cron)

## License

MIT License - See LICENSE file for details.
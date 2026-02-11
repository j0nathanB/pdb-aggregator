# PDB Application Architecture

## Overview

PDB is an intelligent news aggregation and synthesis system that generates weekly intelligence briefs tracking world leaders. It monitors 15 global leaders across Americas, Europe, and Asia-Pacific regions, aggregating news from multiple sources and synthesizing them into structured, story-centric briefs.

**Key Innovation**: Event-centric clustering pipeline that groups related news snippets into events *before* full article fetching, reducing API costs by 60-80% while improving relevance.

---

## System Flow Diagram

```
                              ┌─────────────────────────────────┐
                              │           USER / CLI            │
                              │      python -m src.main         │
                              │  [--leader] [--langgraph] etc.  │
                              └───────────────┬─────────────────┘
                                              │
                                              ▼
                              ┌─────────────────────────────────┐
                              │     ORCHESTRATION LAYER         │
                              │   Simple (seq) or LangGraph     │
                              └───────────────┬─────────────────┘
                                              │
                 ┌────────────────────────────┼────────────────────────────┐
                 │                            │                            │
                 ▼                            ▼                            ▼
        ┌────────────────┐           ┌────────────────┐           ┌────────────────┐
        │   Leader 1     │           │   Leader 2     │           │   Leader N     │
        └───────┬────────┘           └───────┬────────┘           └───────┬────────┘
                │                            │                            │
                └────────────────────────────┼────────────────────────────┘
                                             │
                                             ▼
┌────────────────────────────────────────────────────────────────────────────────────┐
│                          EVENT CLUSTERING AGENT                                    │
│                                                                                    │
│   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐    │
│   │  SearchAPI  │────▶│   Opinion   │────▶│  Sentence   │────▶│   HDBSCAN   │    │
│   │  Snippets   │     │   Filter    │     │ Transformer │     │  Clustering │    │
│   │             │     │             │     │  Embeddings │     │             │    │
│   └─────────────┘     └─────────────┘     └─────────────┘     └──────┬──────┘    │
│                                                                      │           │
│                                                                      ▼           │
│   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐    │
│   │  Processed  │◀────│   Diffbot   │◀────│  Select Top │◀────│   Score     │    │
│   │   Events    │     │  Full Fetch │     │   Events    │     │   Events    │    │
│   └─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘    │
│                                                                                    │
└────────────────────────────────────────────┬───────────────────────────────────────┘
                                             │
                                             ▼
┌────────────────────────────────────────────────────────────────────────────────────┐
│                          DOSSIER BUILDER AGENT                                     │
│                                                                                    │
│   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐                        │
│   │     LLM     │────▶│  Categorize │────▶│  Between    │                        │
│   │  Synthesis  │     │   Stories   │     │ The Lines   │                        │
│   │  (AP Style) │     │ Main/Intl/  │     │  Analysis   │                        │
│   │             │     │  Domestic   │     │             │                        │
│   └─────────────┘     └─────────────┘     └──────┬──────┘                        │
│                                                  │                                │
│                                                  ▼                                │
│                                          ┌─────────────┐                          │
│                                          │   Leader    │                          │
│                                          │   Dossier   │                          │
│                                          └─────────────┘                          │
│                                                                                    │
└────────────────────────────────────────────┬───────────────────────────────────────┘
                                             │
                                             ▼
┌────────────────────────────────────────────────────────────────────────────────────┐
│                       AGGREGATE BRIEFING BUILDER                                   │
│                                                                                    │
│   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐    │
│   │  Collect    │────▶│ Entity URI  │────▶│    LLM      │────▶│  Select     │    │
│   │  All Leader │     │   Overlap   │     │ Validation  │     │  Top 5      │    │
│   │  Stories    │     │   Matching  │     │             │     │  Stories    │    │
│   └─────────────┘     └─────────────┘     └─────────────┘     └──────┬──────┘    │
│                                                                      │           │
│                                                                      ▼           │
│                        ┌─────────────┐     ┌─────────────────────────────┐       │
│                        │  Aggregate  │◀────│  Distribute Overflow to     │       │
│                        │    BTL      │     │  International / Domestic   │       │
│                        └─────────────┘     └─────────────────────────────┘       │
│                                                                                    │
└────────────────────────────────────────────┬───────────────────────────────────────┘
                                             │
                                             ▼
┌────────────────────────────────────────────────────────────────────────────────────┐
│                          SYNTHESIZER AGENT                                         │
│                                                                                    │
│   ┌─────────────────────────┐       ┌─────────────────────────────────┐           │
│   │   Executive Summary     │       │  Source Quality Assessment      │           │
│   │   (2-4 sentences)       │       │  & Methodology Notes            │           │
│   └─────────────────────────┘       └─────────────────────────────────┘           │
│                                                                                    │
└────────────────────────────────────────────┬───────────────────────────────────────┘
                                             │
                                             ▼
┌────────────────────────────────────────────────────────────────────────────────────┐
│                          PERSISTENCE LAYER                                         │
│                                                                                    │
│   briefs/YYYYMMDD/                                                                │
│   ├── brief.md           (Human-readable Markdown)                                │
│   ├── dossiers.json      (Structured leader data)                                 │
│   ├── meta.json          (Brief metadata)                                         │
│   ├── output.json        (Full serialized state)                                  │
│   └── debug/             (Optional: step-by-step JSON)                            │
│                                                                                    │
└────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Component Details

### 1. Entry Point (`src/main.py`)

The CLI provides several execution modes:

| Flag | Description |
|------|-------------|
| `--leader "Name"` | Process single leader only |
| `--simple` | Sequential pipeline (default) |
| `--langgraph` | Parallel processing with resume capability |
| `--debug` | Save intermediate JSON at each step |
| `--start/--end` | Custom date range (default: last 7 days) |
| `--list-leaders` | Show all tracked leaders |
| `--list-briefs` | Show stored briefs |

---

### 2. Event Clustering Agent (`src/agents/event_clustering.py`)

The core innovation: **two-phase fetching** that reduces API costs by 60-80%.

#### Phase 1: Cheap Snippet Fetching

```
SearchAPI  ──▶  Opinion Filter  ──▶  Relevance Filter  ──▶  Snippets
   │                 │                      │
   │                 │                      └── Must contain leader name
   │                 └── Removes editorials/opinion pieces
   └── Returns title, snippet, URL, date (no full text)
```

#### Phase 2: Clustering & Selective Full Fetch

```
Snippets  ──▶  Embed  ──▶  HDBSCAN  ──▶  Score  ──▶  Top N  ──▶  Diffbot
                │            │            │                         │
                │            │            │                         └── Full article text
                │            │            └── Source diversity, wire bonus
                │            └── min_cluster_size=2, singleton absorption
                └── SBERT embeddings (EN or multilingual)
```

**Embeddings**:
- English leaders: `BAAI/bge-small-en-v1.5`
- Multilingual: `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`

**Scoring Formula**:
```
score = source_diversity * wire_bonus * log(cluster_size)
where:
  - source_diversity = unique_sources / total_articles
  - wire_bonus = 1.5 if has wire source (AP, Reuters, AFP)
  - cluster_size capped with log scale
```

---

### 3. Dossier Builder Agent (`src/agents/dossier_builder.py`)

Converts processed events into intelligence-style stories using LLM synthesis.

**Story Categories**:
| Category | Criteria |
|----------|----------|
| Main Stories | Require 2+ sources, highest priority |
| International | Global scope, bilateral relations |
| Domestic | National/regional focus |

**Style Guide**:
- AP-style inverted pyramid
- Neutral verbs (said, announced, stated)
- Source attribution required
- No editorializing

**Between-the-Lines Analysis**:
- Thematic bullets highlighting patterns
- Unstated implications
- Strategic context

---

### 4. Aggregate Briefing Builder (`src/agents/aggregate_builder.py`)

Merges per-leader dossiers into a unified weekly brief.

```
All Leader Dossiers
        │
        ▼
┌───────────────────────┐
│  Entity URI Overlap   │  ← Find stories mentioning same entities
│  Detection            │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│  LLM Validation Gate  │  ← Confirm thematic relevance
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│  Select Top 5 Stories │  ← Highest-scoring cross-leader stories
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│  Distribute Overflow  │  ← Remaining stories to Intl/Domestic
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│  Aggregate BTL        │  ← Cross-cutting themes across all leaders
└───────────────────────┘
```

---

### 5. Synthesizer Agent (`src/agents/synthesizer.py`)

Final polish on the weekly brief:

- **Executive Summary**: 2-4 sentences distilling the week's key developments
- **Source Quality Assessment**: Methodology notes and coverage gaps
- **Brief Compilation**: Assemble all components into `WeeklyBrief`

---

## Data Models (`src/config.py`)

### Core Types

| Model | Description |
|-------|-------------|
| `Article` | News item: title, URL, source, classification, translation |
| `Story` | Synthesized narrative with scope, source refs, entities |
| `EventCluster` | Grouped snippets representing a single event |
| `ProcessedEvent` | Event with fetched articles, entities, summary, score |
| `LeaderDossier` | Per-leader intel: main stories, intl, domestic, BTL |
| `WeeklyBrief` | Final aggregate with all stories, dossiers, exec summary |

### Paragon Taxonomy

Scoring system for article relevance:

**Leader Roles**:
| Role | Weight |
|------|--------|
| Initiator | 0.40 |
| Participant | 0.25 |
| Subject | 0.10 |

**Impact Levels**:
| Level | Weight |
|-------|--------|
| International | 0.25 |
| National | 0.20 |
| Regional | 0.10 |
| Local | 0.05 |

**Priority Score** = Normalized(role_weight + impact_weight)

Articles scoring < 0.4 are filtered out.

---

## External Integrations

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          EXTERNAL APIs                                  │
│                                                                         │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐        │
│  │    SearchAPI    │  │     Diffbot     │  │    Anthropic    │        │
│  │                 │  │                 │  │     Claude      │        │
│  │  Google News    │  │  Article        │  │                 │        │
│  │  Snippets       │  │  Extraction     │  │  LLM Synthesis  │        │
│  │                 │  │  + NLP          │  │  Translation    │        │
│  │                 │  │                 │  │  Classification │        │
│  │  (cheap)        │  │  5 req/min      │  │  50 req/min     │        │
│  │                 │  │  (20s delay)    │  │  (2s delay)     │        │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘        │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │  Arize AX (Optional)                                            │  │
│  │  Observability & Tracing for LLM calls                          │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | Yes | LLM synthesis and translation |
| `SEARCHAPI_KEY` | Yes | News snippet fetching |
| `DIFFBOT_TOKEN` | No | Full article extraction |
| `ARIZE_SPACE_ID` | No | Observability tracing |
| `ARIZE_API_KEY` | No | Observability tracing |

---

## Rate Limiting & Resilience

```python
# Global rate limiters
AnthropicRateLimiter:  2 seconds between API calls (50 req/min max)
DiffbotRateLimiter:   20 seconds between calls (5 req/min)

# Retry logic
@with_retry(max_attempts=3)  # Exponential backoff on failures
```

---

## Pipeline Modes

### Simple Pipeline (Default)

Sequential processing for easier debugging:

```python
for leader in leaders:
    events = EventClusteringAgent.process_leader(leader)
    dossier = DossierBuilderAgent.build_from_events(events)
    dossiers.append(dossier)

aggregate = AggregateBriefingBuilder.build(dossiers)
brief = SynthesizerAgent.finalize(aggregate)
save_brief(brief)
```

### LangGraph Pipeline (`--langgraph`)

Parallel processing with state management:

```
┌────────────────┐
│   Initialize   │  Check for resume state
└───────┬────────┘
        │
        ▼
┌───────────────────────────────────────────────────┐
│          PARALLEL LEADER PROCESSING               │
│  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐         │
│  │Lead 1│  │Lead 2│  │Lead 3│  │ ...  │         │
│  └──┬───┘  └──┬───┘  └──┬───┘  └──┬───┘         │
└─────┼─────────┼─────────┼─────────┼──────────────┘
      │         │         │         │
      └─────────┴────┬────┴─────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │    State Merge        │  operator.or_
         │    & Aggregate        │
         └───────────┬───────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │     Save Brief        │
         └───────────────────────┘
```

---

## Tracked Leaders

| Region | Leaders |
|--------|---------|
| **Americas** | Mark Carney (Canada), Claudia Sheinbaum (Mexico), Lula da Silva (Brazil), Yamandu Orsi (Uruguay) |
| **Europe** | Emmanuel Macron (France), Keir Starmer (UK), Friedrich Merz (Germany), Volodymyr Zelenskyy (Ukraine), Alexander Stubb (Finland), Donald Tusk (Poland), Giorgia Meloni (Italy) |
| **Baltics** | Gitanas Nauseda (Lithuania), Evika Silina (Latvia), Kristen Michal (Estonia), Maia Sandu (Moldova) |

---

## Directory Structure

```
pdb/
├── src/
│   ├── main.py                 # CLI entry point
│   ├── config.py               # Configuration, data models, taxonomy
│   ├── state.py                # Workflow state management
│   ├── graph.py                # Simple pipeline orchestration
│   ├── graph_langgraph.py      # LangGraph pipeline orchestration
│   ├── persistence.py          # Output formatting and saving
│   │
│   ├── agents/
│   │   ├── event_clustering.py # Snippet fetch → cluster → score
│   │   ├── dossier_builder.py  # Event → story synthesis
│   │   ├── aggregate_builder.py# Cross-leader aggregation
│   │   ├── synthesizer.py      # Executive summary, quality assessment
│   │   └── (legacy agents...)
│   │
│   ├── fetcher/
│   │   ├── diffbot.py          # Full article extraction
│   │   ├── search_api.py       # News snippet search
│   │   └── opinion_filter.py   # Editorial content detection
│   │
│   └── clustering/
│       ├── embedder.py         # Sentence transformer embeddings
│       ├── clusterer.py        # HDBSCAN clustering
│       └── scorer.py           # Event importance scoring
│
├── briefs/                     # Generated output
│   └── YYYYMMDD/
│       ├── brief.md
│       ├── dossiers.json
│       └── ...
│
├── data/
│   ├── leaders_sources.csv     # Leader configurations
│   └── opinion_filters.csv     # Editorial detection patterns
│
└── docs/
    ├── architecture.md         # Deployment architecture
    └── app_architecture.md     # This document
```

---

## Key Design Patterns

### 1. Story-Centric (Not Article-Centric)

Events are synthesized into **stories** with source references. Stories are then aggregated across leaders to identify cross-cutting themes.

### 2. Two-Phase Fetching

**Cheap snippet phase** identifies relevant events via clustering. **Expensive full-fetch phase** only runs for top-scoring events. Result: **60-80% API cost reduction**.

### 3. Multi-Model Clustering

- HDBSCAN for snippet clustering (fast, density-based)
- Entity URI overlap for cross-leader story matching
- LLM gates for ambiguous merge validation

### 4. Graceful Degradation

- Diffbot optional (system works without full article extraction)
- Rate limiters prevent API overload
- Retry logic with exponential backoff

### 5. Debug Mode

With `--debug`, each pipeline step saves intermediate JSON:

```
debug/
├── 00_pipeline_summary.json
├── 01_fetch_leader_name.json
├── 02_cluster_leader_name.json
└── ...
```

---

## Configuration

Key constants in `src/config.py`:

```python
RELEVANCE_THRESHOLD = 0.4           # Min priority score for articles
DEFAULT_MODEL = "claude-sonnet-4-20250514"
MAX_ARTICLES_PER_LEADER = 5
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
MULTILINGUAL_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"
API_CALL_DELAY_SECONDS = 2.0        # Anthropic rate limit
```

Leader configurations are loaded from `data/leaders_sources.csv`.
Opinion patterns are loaded from `data/opinion_filters.csv`.

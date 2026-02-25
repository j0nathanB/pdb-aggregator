# PDB Application Architecture

## Overview

PDB (The Middle Powers Monitor) is an intelligent news aggregation and synthesis system that generates weekly intelligence briefs tracking world leaders. It monitors 15 global leaders across Americas, Europe, and the Baltics, aggregating news from multiple sources and synthesizing them into structured, story-centric briefs published to [idealbrief.org](https://idealbrief.org) via Mintlify and distributed by email.

**Key Innovations**:
- Event-centric clustering pipeline that groups related news snippets into events *before* full article fetching, reducing API costs by 60-80%
- Three-stage story matching (entity URI overlap + bi-encoder + cross-encoder) for cross-leader deduplication
- Model tiering: Opus for editorial prose, Sonnet for structured extraction
- Batch API for parallel synthesis with prompt caching

---

## System Flow Diagram

```
                              ┌─────────────────────────────────┐
                              │        SCHEDULED TRIGGER         │
                              │   EventBridge → ECS Fargate      │
                              │   (Sunday 11 PM ET weekly)       │
                              └───────────────┬─────────────────┘
                                              │
                                              ▼
                              ┌─────────────────────────────────┐
                              │     ORCHESTRATION LAYER          │
                              │   Simple (seq) or LangGraph      │
                              │       src/graph.py               │
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
│   │  SearchAPI  │────▶│   Opinion   │────▶│ E5-multilin │────▶│   HDBSCAN   │    │
│   │  Snippets   │     │   Filter    │     │  Embeddings │     │  Clustering │    │
│   └─────────────┘     └─────────────┘     └─────────────┘     └──────┬──────┘    │
│                                                                      │           │
│                                                                      ▼           │
│   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐    │
│   │  Processed  │◀────│   Diffbot   │◀────│  Select Top │◀────│   Cluster   │    │
│   │   Events    │     │  Full Fetch │     │   Events    │     │  Reasoning  │    │
│   └─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘    │
│                                                                                    │
└────────────────────────────────────────────┬───────────────────────────────────────┘
                                             │
                                             ▼
┌────────────────────────────────────────────────────────────────────────────────────┐
│                       DOSSIER BUILDER AGENT (Batch API)                            │
│                                                                                    │
│   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐    │
│   │  Per-Event  │────▶│  Classify   │────▶│  Group as   │────▶│     BTL     │    │
│   │  Synthesis  │     │  (Paragon)  │     │ Main/Intl/  │     │  Analysis   │    │
│   │  (AP Style) │     │             │     │  Domestic   │     │  + Summary  │    │
│   └─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘    │
│                                                                                    │
└────────────────────────────────────────────┬───────────────────────────────────────┘
                                             │
                                             ▼
┌────────────────────────────────────────────────────────────────────────────────────┐
│                     AGGREGATE BRIEFING BUILDER                                     │
│                                                                                    │
│   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐    │
│   │  Entity URI │────▶│  Bi-Encoder │────▶│   Cross-    │────▶│  Select     │    │
│   │   Overlap   │     │  Similarity │     │   Encoder   │     │  Top 5      │    │
│   │ (hard link) │     │ (soft link) │     │  Validation │     │  Stories    │    │
│   └─────────────┘     └─────────────┘     └─────────────┘     └──────┬──────┘    │
│                                                                      │           │
│                                                                      ▼           │
│   ┌─────────────────┐     ┌─────────────────────────────────────────────┐        │
│   │  Aggregate BTL  │◀────│  Distribute Overflow to Intl / Domestic     │        │
│   │  + Exec Summary │     │  (sorted by Paragon priority, max 7 each)  │        │
│   └─────────────────┘     └─────────────────────────────────────────────┘        │
│                                                                                    │
└────────────────────────────────────────────┬───────────────────────────────────────┘
                                             │
                                             ▼
┌────────────────────────────────────────────────────────────────────────────────────┐
│                          PERSISTENCE & PUBLISHING                                  │
│                                                                                    │
│   briefs/YYYY-MM-DD/                                                              │
│   ├── overview.mdx         (Mintlify brief page)                                  │
│   ├── dossiers/*.mdx       (Per-leader Mintlify pages)                            │
│   ├── dossiers.json        (Structured leader data)                               │
│   ├── meta.json            (Brief metadata)                                       │
│   ├── output.json          (Full serialized state)                                │
│   └── email.html           (Email digest)                                         │
│                                                                                    │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐   │
│   │  Upload to   │───▶│  Push to     │───▶│  Mintlify    │───▶│  Email via   │   │
│   │  S3 Bucket   │    │  GitHub      │    │  Auto-Deploy │    │  SES/Lambda  │   │
│   └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘   │
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

In production, the pipeline is invoked via `scripts/run_pipeline.py` as the ECS Fargate entrypoint.

---

### 2. Event Clustering Agent (`src/agents/event_clustering.py`)

The core innovation: **two-phase fetching** that reduces API costs by 60-80%.

#### Phase 1: Cheap Snippet Fetching

```
SearchAPI  ──▶  Opinion Filter  ──▶  Relevance Filter  ──▶  Snippets
   │                 │                      │
   │                 │                      └── Must contain leader name
   │                 └── Removes editorials/opinion pieces (URL + content patterns)
   └── Returns title, snippet, URL, date (no full text)
```

#### Phase 2: Clustering & Selective Full Fetch

```
Snippets  ──▶  Embed  ──▶  HDBSCAN  ──▶  Reason  ──▶  Score  ──▶  Top N  ──▶  Diffbot
                │            │            │            │                         │
                │            │            │            │                         └── Full article text
                │            │            │            └── Source diversity, wire bonus
                │            │            └── LLM dedup + story arc detection (single call)
                │            └── min_cluster_size=2, min_samples=1, cosine metric
                └── E5-multilingual-small (unified for all languages)
```

**Embedding Model**: `intfloat/multilingual-e5-small` (118M params, unified for all languages)
- Replaces the previous split approach (bge-small-en + paraphrase-multilingual)
- All vectors exist in the same latent space, enabling cross-lingual comparison
- Query prefix `"query: "` for optimal retrieval performance

**Cluster Reasoning** (`src/clustering/cluster_reasoning.py`):
- Single LLM call combining deduplication + story arc detection
- Uses `MODEL_ANALYTICAL` (Sonnet 4.5) with 4k thinking budget
- Replaces two separate dedup/grouping passes

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

**Batch API Mode**: All per-event synthesis calls are batched into a single Batch API request (50% cost discount). Polls every 30s, max wait 3600s.

**Story Categories**:
| Category | Criteria |
|----------|----------|
| Main Stories | Require 2+ sources, highest priority |
| International | Global scope, bilateral relations |
| Domestic | National/regional focus |

**Style Guide**:
- AP-style inverted pyramid with datelines
- Neutral verbs (said, announced, stated)
- Source attribution required
- No editorializing
- Translation to English for non-English leaders

**Between-the-Lines Analysis** (uses `MODEL_EDITORIAL` / Opus):
- Thematic bullets highlighting patterns
- Unstated implications
- Strategic context

---

### 4. Aggregate Briefing Builder (`src/agents/aggregate_builder.py`)

Merges per-leader dossiers into a unified weekly brief using three-stage story matching.

```
All Leader Dossiers
        │
        ▼
┌───────────────────────┐
│  1. Entity URI Overlap│  ← Hard link: precise, low recall
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│  2. Bi-Encoder        │  ← Soft link: high recall, 0.82 threshold
│     Similarity        │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│  3. Cross-Encoder     │  ← Catches semantic inversions, 0.7 threshold
│     Validation        │     ("Leader denies charges" vs "Leader indicted")
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│  Select Top 5 Stories │  ← Highest-scoring cross-leader stories (2+ sources)
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│  Distribute Overflow  │  ← Remaining stories to Intl/Domestic (max 7 each)
│  (Paragon priority)   │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│  Aggregate BTL        │  ← Cross-cutting themes across all leaders
│  + Executive Summary  │
└───────────────────────┘
```

**Cross-Encoder**: `cross-encoder/ms-marco-MiniLM-L-6-v2` — reads both texts together to catch subtle semantic differences that bi-encoder cosine similarity misses.

---

### 5. Email Digest Agent (`src/agents/email_digest.py`)

Condenses the full brief into an email-friendly HTML digest:
- Selects top stories and summarizes dossiers
- Optimized for email length constraints
- Rendered via `src/email_template.py`
- Output saved as `email.html` in the brief directory

---

## Model Tiering

```python
MODEL_EDITORIAL  = "claude-opus-4-6"           # BTL, exec summary (few calls, quality matters)
MODEL_ANALYTICAL = "claude-sonnet-4-5-20250929" # Dedup, story arcs, validation (structured)
MODEL_SYNTHESIS  = "claude-sonnet-4-5-20250929" # Event synthesis (bulk calls via Batch API)

THINKING_EDITORIAL  = 16000  # Full extended thinking
THINKING_ANALYTICAL = 4000   # Moderate thinking
THINKING_SYNTHESIS  = 0      # Disabled — structured extraction, not deep reasoning
```

Prompt caching enabled with 1h TTL for system prompts.

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

Scoring system for article relevance and story prioritization.

**Event Types** (weights 0.10–0.35):

| Type | Weight |
|------|--------|
| POLICY_ANNOUNCEMENT | 0.35 |
| CRISIS_RESPONSE | 0.35 |
| INTERNATIONAL_VISIT | 0.30 |
| MAJOR_SPEECH | 0.30 |
| BILATERAL_AGREEMENT | 0.30 |
| CABINET_CHANGE | 0.25 |
| LEGAL_DEVELOPMENT | 0.25 |
| ECONOMIC_ACTION | 0.25 |
| OTHER | 0.10 |

**Leader Roles**:

| Role | Weight | Note |
|------|--------|------|
| Initiator | 0.40 | Driving the action |
| Participant | 0.25 | Involved but not driving |
| Subject | 0.10 | Passive; elevated 3x for LEGAL, CRISIS, CABINET |

**Impact Levels**:

| Level | Weight |
|-------|--------|
| International | 0.25 |
| National | 0.20 |
| Regional | 0.10 |
| Local | 0.05 |

**Priority Score** = Normalized(event_weight + role_weight + impact_weight). Articles scoring < 0.4 are filtered out.

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
│  │  Snippets       │  │  Extraction     │  │  Opus: BTL,     │        │
│  │                 │  │  + NLP          │  │    summaries    │        │
│  │  (cheap)        │  │  5 req/min      │  │  Sonnet: synth, │        │
│  │                 │  │  (20s delay)    │  │    analysis     │        │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘        │
│                                                                         │
│  ┌─────────────────┐  ┌─────────────────────────────────────────┐     │
│  │  Sentence       │  │  Arize AX (Optional)                    │     │
│  │  Transformers   │  │  Observability & Tracing for LLM calls  │     │
│  │  E5-multilingual│  │                                         │     │
│  │  Cross-Encoder  │  │                                         │     │
│  └─────────────────┘  └─────────────────────────────────────────┘     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | Yes | LLM synthesis and translation |
| `SEARCHAPI_KEY` | Yes | News snippet fetching |
| `DIFFBOT_TOKEN` | No | Full article extraction |
| `GITHUB_TOKEN` | Prod | Git push to content repo |
| `ARTIFACTS_BUCKET` | Prod | S3 bucket for brief artifacts |
| `SES_FROM_EMAIL` | Prod | Email sender address |
| `ALERT_EMAIL` | Prod | Admin notification address |
| `ARIZE_SPACE_ID` | No | Observability tracing |
| `ARIZE_API_KEY` | No | Observability tracing |

---

## AWS Infrastructure (`infra/`)

All infrastructure managed with Terraform. The pipeline runs weekly on ECS Fargate, with Lambda functions handling email distribution and monitoring.

```
┌────────────────────────────────────────────────────────────────────────────┐
│                        AWS ARCHITECTURE                                    │
│                                                                            │
│   EventBridge                                                              │
│   ┌──────────────────┐    ┌──────────────────┐                            │
│   │ generate-brief   │───▶│  ECS Fargate     │                            │
│   │ Sun 11PM ET      │    │  (ARM64, spot)   │                            │
│   └──────────────────┘    │                  │                            │
│   ┌──────────────────┐    │  run_pipeline.py │                            │
│   │ dead-mans-switch │    └────────┬─────────┘                            │
│   │ Mon 8AM ET       │             │                                      │
│   └────────┬─────────┘             │                                      │
│            │                       ├── Upload artifacts to S3              │
│            ▼                       ├── Push .mdx to GitHub (main)          │
│   ┌──────────────────┐             └── Send admin preview via SES          │
│   │ Dead Man's Switch│                                                     │
│   │ Lambda           │    ┌──────────────────────────────────────┐        │
│   └──────────────────┘    │  GitHub push triggers:                │        │
│                           │  1. Mintlify auto-deploys site        │        │
│                           │  2. GitHub Actions → email webhook    │        │
│                           └───────────────┬──────────────────────┘        │
│                                           │                                │
│   ┌───────────────────────────────────────┼───────────────────────┐       │
│   │              API Gateway (REST)       │                       │       │
│   │                                       ▼                       │       │
│   │   POST /trigger-email  ──▶  email_sender Lambda               │       │
│   │   POST /unsubscribe    ──▶  unsubscribe Lambda                │       │
│   │                                                               │       │
│   │   x-api-key authentication                                    │       │
│   └───────────────────────────────────────────────────────────────┘       │
│                                                                            │
│   ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐   │
│   │ S3               │    │ DynamoDB         │    │ SES              │   │
│   │ Brief artifacts  │    │ subscribers      │    │ Email delivery   │   │
│   │ email.html       │    │ ses_events       │    │ Bounce tracking  │   │
│   │ meta.json        │    │                  │    │                  │   │
│   └──────────────────┘    └──────────────────┘    └──────────────────┘   │
│                                                                            │
│   ┌──────────────────┐    ┌──────────────────┐                            │
│   │ Secrets Manager  │    │ ECR              │                            │
│   │ API keys         │    │ Docker image     │                            │
│   └──────────────────┘    └──────────────────┘                            │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

### Lambda Functions (`infra/lambda/`)

| Function | Trigger | Purpose |
|----------|---------|---------|
| `email_sender` | API Gateway webhook | Load email.html from S3, send to subscribers via SES |
| `authorizer` | API Gateway | Validate x-api-key header |
| `unsubscribe` | API Gateway | Process unsubscribe requests, update DynamoDB |
| `ses_events` | SNS (from SES) | Track bounces and complaints in DynamoDB |
| `dead_mans_switch` | EventBridge (Mon 8AM) | Alert admin if pipeline didn't complete |

### DynamoDB Tables

| Table | PK | Purpose |
|-------|-----|---------|
| `subscribers` | email | Email subscriptions, last_sent_brief_id, unsubscribe_token |
| `ses_events` | email + event_type | Bounce/complaint tracking |

---

## Docker & Deployment

### Dockerfile

```dockerfile
FROM python:3.12-slim
# System deps: git, gh CLI, gcc/g++ (for hdbscan)
# Pre-downloads embedding models (~500MB) baked into image:
#   - intfloat/multilingual-e5-small
#   - cross-encoder/ms-marco-MiniLM-L-6-v2
# Entrypoint: python -m scripts.run_pipeline
```

### ECS Fargate Entrypoint (`scripts/run_pipeline.py`)

1. Run `PDBWorkflow` (the full pipeline)
2. Find generated brief directory
3. Upload artifacts (meta.json, email.html) to S3
4. Clone content repo, copy .mdx files, push to main
5. Send admin preview email via SES

### GitHub Actions (`.github/workflows/deploy-and-notify.yml`)

Triggers on push to `main` when `briefs/**` or `mint.json` change:
1. Wait 45s for Mintlify CDN propagation
2. POST to email webhook (API Gateway → email_sender Lambda)
3. Lambda loads email.html from S3 and sends to all active subscribers

---

## Mintlify Documentation Site

The brief is published as a Mintlify documentation site at `idealbrief.org`.

**Navigation structure** (managed by `mint.json`):
```
Latest Brief
├─ Overview (briefs/YYYY-MM-DD/overview.mdx)
Dossiers
├─ Leader 1 (briefs/YYYY-MM-DD/dossiers/leader_name.mdx)
├─ Leader 2 ...
Archives
├─ Index (archives/index.mdx, auto-generated)
Week of [Date]
├─ Overview + Dossiers (previous briefs)
...
```

**Auto-update flow**:
1. Pipeline saves `.mdx` files to `briefs/YYYY-MM-DD/`
2. `persistence.py` calls `update_mint_json()` and `update_archives_page()`
3. `run_pipeline.py` pushes to main
4. Mintlify auto-deploys via GitHub integration
5. GitHub Actions triggers email webhook after 45s

---

## Rate Limiting & Resilience

```python
# Global rate limiters
AnthropicRateLimiter:  2 seconds between API calls
DiffbotRateLimiter:   20 seconds between calls (5 req/min)

# Retry logic
@with_retry(max_attempts=3)  # Exponential backoff on failures

# Batch API
BATCH_POLL_INTERVAL = 30s    # Poll every 30s for completion
BATCH_MAX_WAIT = 3600s       # Timeout after 1 hour
BATCH_ENABLED = True         # 50% cost discount on synthesis calls

# Prompt caching
CACHE_TTL = "1h"             # System prompts cached for repeated calls
```

---

## Pipeline Modes

### Simple Pipeline (Default)

Sequential processing for easier debugging:

```python
for leader in leaders:
    events = EventClusteringAgent.process_leader(leader)
    dossier = DossierBuilderAgent.build_from_events(events)  # Batch API
    dossiers.append(dossier)

aggregate = AggregateBriefingBuilder.build(dossiers)
brief = save_brief(aggregate)
email = generate_email(brief)
```

### LangGraph Pipeline (`--langgraph`)

Parallel processing with state management and resume capability:

```
┌────────────────┐
│   Initialize   │  Check for resume state (completed dossiers)
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
         │    State Merge        │
         │    & Aggregate        │
         └───────────┬───────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │   Save & Publish      │
         └───────────────────────┘
```

Resume: saves dossiers to JSON after each leader completes. On restart, `get_existing_dossiers()` skips completed leaders.

---

## Tracked Leaders

| Region | Leaders |
|--------|---------|
| **Americas** | Mark Carney (Canada), Claudia Sheinbaum (Mexico), Lula da Silva (Brazil), Yamandu Orsi (Uruguay) |
| **Europe** | Emmanuel Macron (France), Keir Starmer (UK), Friedrich Merz (Germany), Volodymyr Zelenskyy (Ukraine), Alexander Stubb (Finland), Donald Tusk (Poland), Giorgia Meloni (Italy) |
| **Baltics & Moldova** | Gitanas Nauseda (Lithuania), Evika Silina (Latvia), Kristen Michal (Estonia), Maia Sandu (Moldova) |

Each leader has 3-5 domestic news sources (native language) and wire service coverage (Reuters, AP), configured in `leaders_sources.csv`.

---

## Directory Structure

```
pdb/
├── src/
│   ├── main.py                 # CLI entry point
│   ├── config.py               # Configuration, data models, taxonomy
│   ├── state.py                # Workflow state management (TypedDict schemas)
│   ├── graph.py                # Simple + LangGraph pipeline orchestration
│   ├── graph_langgraph.py      # LangGraph StateGraph implementation
│   ├── persistence.py          # Mintlify .mdx output, JSON artifacts, email gen
│   ├── email_template.py       # HTML email template rendering
│   ├── debug.py                # Debug output at each pipeline step
│   │
│   ├── agents/
│   │   ├── base.py             # LLM client, rate limiting, batch API, retries
│   │   ├── event_clustering.py # Snippet fetch → cluster → score
│   │   ├── dossier_builder.py  # Event → story synthesis (Batch API)
│   │   ├── aggregate_builder.py# Cross-leader matching + aggregation
│   │   ├── synthesizer.py      # Executive summary, quality assessment
│   │   ├── email_digest.py     # Condense brief for email distribution
│   │   ├── translator.py       # Political/diplomatic-aware translation
│   │   ├── classifier.py       # Paragon taxonomy classification
│   │   └── source_fetcher.py   # RSS/API article fetching
│   │
│   ├── clustering/
│   │   ├── embedder.py         # E5-multilingual-small embeddings
│   │   ├── clusterer.py        # HDBSCAN clustering
│   │   ├── scorer.py           # Event importance scoring
│   │   ├── cluster_reasoning.py# LLM dedup + story arc (single call)
│   │   ├── dedup.py            # Cluster deduplication helpers
│   │   ├── story_grouper.py    # Story arc detection helpers
│   │   └── transcript_processor.py # Press conference processing
│   │
│   ├── fetcher/
│   │   ├── core.py             # SearchAPI + Diffbot integration
│   │   ├── opinion_filter.py   # Editorial content detection
│   │   └── diffbot_nlp.py      # Diffbot NLP API (disabled)
│   │
│   └── nodes/                  # LangGraph node wrappers
│       ├── init.py, fetch.py, translate.py, dedupe.py,
│       │   classify.py, dossier.py, synthesis.py, compile.py
│       └── threads.py          # (deprecated)
│
├── scripts/
│   ├── run_pipeline.py         # ECS Fargate entrypoint
│   ├── extract_fixtures.py     # Extract test fixtures from debug output
│   └── migrate_to_mintlify.py  # Migration from old format to .mdx
│
├── infra/                      # Terraform IaC
│   ├── main.tf, variables.tf, outputs.tf
│   ├── ecs.tf, ecr.tf          # Fargate cluster + container registry
│   ├── eventbridge.tf          # Weekly schedule + dead man's switch
│   ├── api_gateway.tf          # REST API for webhooks
│   ├── s3.tf, dynamodb.tf      # Storage
│   ├── ses.tf                  # Email delivery
│   ├── iam.tf, secrets.tf, vpc.tf
│   └── lambda/
│       ├── email_sender/       # Distribute digest to subscribers
│       ├── authorizer/         # API key validation
│       ├── unsubscribe/        # Handle unsubscribe requests
│       ├── ses_events/         # Bounce/complaint tracking
│       └── dead_mans_switch/   # Pipeline health monitoring
│
├── tests/
│   ├── conftest.py             # Shared fixtures and loaders
│   ├── fixtures/               # Processed events + clusters for replay
│   └── test_*.py               # Clustering, dossier, aggregate quality tests
│
├── briefs/                     # Generated output (YYYY-MM-DD/)
├── archives/                   # Mintlify archives page
├── data/
│   ├── leaders_sources.csv     # Leader configurations
│   └── opinion_filters.csv     # Editorial detection patterns
│
├── Dockerfile                  # Python 3.12 + models baked in
├── mint.json                   # Mintlify site configuration
├── requirements.txt            # Python dependencies
└── docs/
    └── app_architecture.md     # This document
```

---

## Key Design Patterns

### 1. Story-Centric (Not Article-Centric)

Events are synthesized into **stories** with source references. Stories are then aggregated across leaders to identify cross-cutting themes. Old architecture was action-centric (LeaderAction lists); new architecture produces AP-style narratives.

### 2. Two-Phase Fetching

**Cheap snippet phase** identifies relevant events via clustering. **Expensive full-fetch phase** only runs for top-scoring events. Result: **60-80% API cost reduction**.

### 3. Three-Stage Story Matching

1. **Entity URI overlap** (hard link, precise, low recall)
2. **Bi-encoder similarity** (soft link, high recall, 0.82 threshold)
3. **Cross-encoder validation** (catches semantic inversions, 0.7 threshold)

### 4. Model Tiering

Opus for high-value editorial prose (BTL, summaries). Sonnet for structured extraction (dedup, validation, synthesis). Extended thinking budgets matched to task complexity.

### 5. Batch API + Prompt Caching

All per-event synthesis calls batched into a single Batch API request (50% cost discount). System prompts cached for 1h TTL across calls.

### 6. Graceful Degradation

- Diffbot optional (system works without full article extraction)
- Rate limiters prevent API overload
- Retry logic with exponential backoff

### 7. Debug Mode

With `--debug`, each pipeline step saves intermediate JSON to `briefs/YYYY-MM-DD/debug/`.

---

## Configuration

Key constants in `src/config.py`:

```python
RELEVANCE_THRESHOLD = 0.4
DEFAULT_MODEL = "claude-opus-4-6"
MODEL_ANALYTICAL = "claude-sonnet-4-5-20250929"
MODEL_SYNTHESIS = MODEL_ANALYTICAL

EMBEDDING_MODEL = "intfloat/multilingual-e5-small"
CROSS_ENCODER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"
CROSS_ENCODER_THRESHOLD = 0.7

MAX_EVENTS_FOR_BRIEF = 5
MAX_ARTICLES_PER_EVENT = 3
MAX_SNIPPETS_PER_SOURCE = 20

BATCH_ENABLED = True
BATCH_POLL_INTERVAL_SECONDS = 30.0
CACHE_TTL = "1h"

API_CALL_DELAY_SECONDS = 2.0        # Anthropic rate limit
```

Leader configurations loaded from `leaders_sources.csv`. Opinion patterns loaded from `opinion_filters.csv`.

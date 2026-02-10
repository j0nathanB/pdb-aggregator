# PDB Aggregator: Event Clustering Architecture

> **Status**: Implemented with extensions beyond original spec.
> Last updated: 2026-02-07

## Overview

The news ingestion pipeline uses **event clustering** before full article fetching. This replaces the naive approach (fetch all articles → classify each one) with an efficient pipeline (fetch snippets → cluster into events → fetch representative articles per event → synthesize).

## Architecture

```
Leader → SerpAPI (all sources) → Pre-filter (relevance + opinions) →
Embed snippets → HDBSCAN cluster → LLM dedup → Story arc detection →
Score events → Fetch top articles via Diffbot → LLM synthesize narratives → Build dossier
```

> **Note**: Diffbot NLP entity extraction was removed (2026-02-09) due to 500 calls/month API limit.
> Summarization is now handled implicitly by the dossier builder's LLM synthesis step.

**Benefits:**
- Cluster before fetching reduces Diffbot calls by 60-80%
- Events (not articles) become the unit of analysis
- Source diversity scoring surfaces important stories
- Story arc detection merges multi-day developing stories
- Cross-leader thematic validation prevents spurious merges

---

## Implementation Status

### 1. Clustering Module: `src/clustering/` ✅

| Component | File | Status |
|-----------|------|--------|
| Snippet embedder | `embedder.py` | ✅ Complete |
| HDBSCAN clusterer | `clusterer.py` | ✅ Complete |
| Event scorer | `scorer.py` | ✅ Complete |
| Pre-filters | `filters.py` | ✅ Complete |
| Story grouper | `story_grouper.py` | ✅ Complete |

#### Key Classes

**`SnippetEmbedder`** - Embeds search result snippets using sentence-transformers.
- Default model: `BAAI/bge-small-en-v1.5` (English)
- Multilingual model: `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` (auto-selected based on leader's source languages)

**`EventClusterer`** - HDBSCAN clustering with configurable parameters.
- `min_cluster_size=2` - Minimum snippets per cluster
- `min_samples=1` - Density threshold
- Noise points become singleton clusters

**`EventScorer`** - Scores clusters by importance.
- Wire coverage bonus (1.5x)
- Source diversity weight
- Log-scaled size bonus (prevents syndication dominance)

**`filter_relevant()`** - Pre-filter snippets for leader relevance.
- Checks if leader name appears in title or snippet
- Removes generic news that mentions leader tangentially

**`separate_opinions()`** - Separates opinion/editorial content.
- Detects opinion indicators in titles and URLs
- Returns (news_snippets, opinion_snippets)

**`detect_story_arcs()`** - LLM-based detection of multi-day developing stories.
- Groups events like "Orsi arrives in China", "Orsi meets Xi", "Orsi signs agreements"
- Returns list of cluster index groups to merge

**`validate_cross_leader_match()`** - LLM gate for cross-leader story merging.
- Prevents merging stories that share entities but aren't thematically related
- Example: Blocks merging "Carney discusses trade" + "Sheinbaum discusses trade" if unrelated

**`deduplicate_clusters()`** - LLM-based deduplication pass.
- Catches same-event clusters that HDBSCAN failed to merge
- Compares cluster titles and identifies duplicates

---

### 2. Two-Phase Fetching: `src/fetcher/core.py` ✅

**Phase 1: Snippet fetching (cheap)**
```python
async def fetch_snippets_for_leader(
    leader_name: str,
    sources: list[dict],
    date_start: str,
    date_end: str,
) -> list[dict]
```
- SerpAPI only, no Diffbot
- Returns title, snippet, URL, source metadata

**Phase 2: Full article fetching (expensive)**
```python
async def fetch_full_articles(
    urls: list[str],
    source_metadata: dict[str, dict],
) -> list[dict]
```
- Diffbot extraction for selected URLs only
- Called after clustering identifies important events

---

### 3. Diffbot NLP Integration: `src/fetcher/diffbot_nlp.py` ⏸️ DISABLED

```python
async def extract_nlp(text: str) -> Optional[dict]
def extract_high_salience_entities(nlp_result: dict, threshold: float = 0.5) -> list[dict]
def get_summary(nlp_result: dict) -> str
```

**Status: DISABLED** (2026-02-09)

**Why disabled:**
- Diffbot NLP API (`nl.diffbot.com`) has a 500 calls/month limit
- With 15 leaders × 10-20 articles each, we'd burn through quota in 1-2 runs
- The Article API (`api.diffbot.com/v3/article`) has much higher limits and is sufficient

**What we lose:**
- Entity extraction with salience scores (used for cross-leader story matching)
- Pre-computed summaries

**Mitigation:**
- Dossier builder synthesizes summaries implicitly during LLM narrative generation
- Cross-leader matching in aggregate_builder is degraded but still works via LLM thematic validation
- Full article content is passed to Claude, which handles summarization as part of synthesis

---

### 4. Event Clustering Agent: `src/agents/event_clustering.py` ✅

Orchestrates the full per-leader pipeline:

```python
class EventClusteringAgent:
    async def process_leader(
        self,
        leader: LeaderConfig,
        date_start: str,
        date_end: str,
        max_events_for_brief: int = 5,
        max_articles_per_event: int = 3,
    ) -> tuple[list[ProcessedEvent], list[ProcessedEvent], list[dict]]
```

**Pipeline steps:**
1. Build source list (wire + domestic)
2. Fetch snippets (SerpAPI only)
3. Pre-filter: relevance check + opinion separation
4. Embed snippets (model selected by leader's language mix)
5. Cluster with HDBSCAN
6. LLM deduplication pass
7. Story arc detection and merging
8. Score events
9. Split into top/rest
10. Fetch full articles for top events (Diffbot Article API)
11. ~~Extract NLP entities from articles~~ (disabled - NLP API rate limit)

**Returns:** `(top_events, remaining_events, opinions)`

---

### 5. Dossier Builder: `src/agents/dossier_builder.py` ✅

Converts ProcessedEvents into Story objects with LLM-synthesized narratives.

```python
class DossierBuilderAgent:
    async def build(
        self,
        leader: LeaderConfig,
        top_events: list[ProcessedEvent],
        remaining_events: list[ProcessedEvent],
        opinions: list[dict],
    ) -> LeaderDossier
```

**Key methods:**

**`_synthesize_story()`** - LLM synthesis of event into AP-style narrative.
- Takes ProcessedEvent with raw Diffbot summaries
- Generates title (max 12 words) and narrative (3-4 sentences)
- Enforces dateline format, neutral verbs, source attribution
- **This addresses the "TODO: LLM synthesis" from original spec**

**`_looks_non_english()`** - Heuristic check for non-English content.
- Detects Spanish/Portuguese stopwords and characters
- Triggers translation fallback if detected

**`_ensure_english()`** - LLM translation to English.
- Translates title and narrative while preserving facts
- Maintains AP style in translated output

**`_generate_between_the_lines()`** - LLM analysis of themes.
- Identifies patterns not immediately obvious
- Things to watch as events develop

**`_classify_story()`** - Paragon taxonomy classification for overflow sorting.
- Classifies by event type, leader role, impact level
- Calculates priority score for sorting briefs section
- Used to break ties when signal strength is similar

**`_generate_executive_summary()`** - 2-3 sentence overview of leader's week.
- Distills key developments across all stories
- Leads with most significant development
- Uses neutral, factual language (AP style)
- Rendered as blockquote at top of dossier markdown

---

### 6. Aggregate Briefing Builder: `src/agents/aggregate_builder.py` ✅

Synthesizes per-leader dossiers into aggregate briefing.

```python
class AggregateBriefingBuilder:
    async def build(
        self,
        dossiers: dict[str, LeaderDossier],
    ) -> tuple[list[Story], list[Story], list[Story], list[str], str]
    # Returns: (main_stories, intl_stories, dom_stories, btl, executive_summary)
```

**Key features:**

**Entity-based cross-leader matching:**
- Finds stories across leaders with 3+ shared entity URIs
- No transitivity - prevents chaining A→B→C when A and C don't directly match
- Max group size of 4 to prevent mega-clusters

**LLM thematic validation:**
- Validates entity-matched groups are actually about the same topic
- Rejects false positives (stories that share entities but different events)

**Shared story synthesis:**
- Merges multiple leaders' perspectives into combined narrative
- Aggregates source refs and entities

**Classification-based sorting for overflow (Briefs section):**
- Main stories (top 5) sorted by signal strength (score)
- Overflow stories sorted by Paragon classification priority
- Classification scores: event type + leader role + impact level
- Briefs section limited to 7 stories (top by classification priority)

**Executive summary generation:**
- 2-4 sentence overview of the week's key developments
- Leads with dominant theme or most significant development
- References specific leaders and their actions
- Connects developments across regions where relevant

---

### 7. Workflow Integration: `src/graph.py` ✅

LangGraph-style workflow with nodes:
- `init` - Initialize state
- `process_leaders` - Parallel leader processing via EventClusteringAgent
- `build_dossiers` - Build dossiers from events
- `aggregate` - Build aggregate briefing
- `persist` - Save to disk

---

### 8. Output Format: `src/persistence.py` ✅

**Brief structure:**
- Executive Summary (2-4 sentences, rendered as blockquote)
- Top Stories (full narratives)
- Briefs (country-grouped headlines linking to dossiers)
- Between the Lines

**Dossier structure:**
- Executive Summary (2-3 sentences, rendered as blockquote)
- Top Stories
- International Stories
- Domestic Stories
- Between the Lines

**Features:**
- Country headers link to primary leader's dossier
- Story headlines link to anchors within dossiers
- Emoji flags for countries

---

## Extensions Beyond Original Spec

| Feature | Description |
|---------|-------------|
| **Pre-filtering** | Relevance check + opinion separation before clustering |
| **Multilingual support** | Auto-selects embedding model based on source languages |
| **LLM deduplication** | Catches duplicates HDBSCAN misses |
| **Story arc detection** | Merges multi-day developing stories |
| **Cross-leader validation** | LLM gate prevents spurious entity-based merges |
| **No transitivity** | Prevents chaining in cross-leader grouping |
| **English enforcement** | Detects + translates non-English content |
| **Country-grouped briefs** | Headlines grouped by country with emoji flags |
| **Executive summaries** | 2-3 sentence overview at top of each dossier |

---

## Configuration: `src/config.py`

```python
# Event clustering settings
MAX_SNIPPETS_PER_SOURCE = 10
MAX_EVENTS_FOR_BRIEF = 5
MAX_ARTICLES_PER_EVENT = 3
MIN_EVENT_SCORE_RATIO = 0.5

# Embedding models
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
MULTILINGUAL_EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

# Wire services (shared across all leaders)
WIRE_SERVICES = [Reuters, AP News]
```

---

## Remaining TODOs

From `docs/output_format_v2.md`:
- [ ] **Domestic Context flow**: Search domestic news for background context per country (separate from event-driven news)
- [ ] **Foreign ministry expansion**: Add foreign ministry sources for better international coverage

From `docs/architecture.md`:
- [ ] **Phase 1**: GitHub Actions automation, S3 hosting, subscriber notifications
- [ ] **Phase 2**: FastAPI backend, Postgres schema, email tracking
- [ ] **Phase 3**: Archive browser, full-text search
- [ ] **Phase 4**: Vector embeddings for semantic search, trajectory analysis

---

## Tuning Notes

**Clustering with 20 snippets/source**: With `MAX_SNIPPETS_PER_SOURCE=20` and ~6 sources per leader, major stories may exceed `max_cluster_size=8` in the clusterer, triggering megacluster splits. This could cause over-fragmentation of big stories (e.g., "Trump tariffs" split into multiple events). Monitor for this pattern; if observed, consider bumping `max_cluster_size` to 12-15.

---

## Success Metrics

- ✅ **Diffbot calls reduced by 60%+** (from ~30/leader to ~10-12/leader)
- ✅ **Events properly deduplicated** (same story from 3 sources = 1 event)
- ✅ **Top events surfaced correctly** (wire coverage + diversity = high rank)
- ✅ **Multi-day stories merged** (story arc detection working)
- ✅ **Cross-leader merging validated** (no spurious entity-based matches)
- ✅ **English output enforced** (translation fallback working)

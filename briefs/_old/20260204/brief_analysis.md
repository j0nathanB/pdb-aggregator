# Brief Analysis — 2026-02-04

## The Deduplication Problem

**Is deduplication happening?**

No. There is no explicit deduplication pass anywhere in the pipeline. The **only** mechanism that's supposed to prevent duplicates is HDBSCAN clustering — if two snippets are similar enough, they cluster together and become one event. That's the entire dedup strategy.

**Is it working?**

No. HDBSCAN is under-clustering. Snippets about the same event (Stubb's parliament speech, the train inauguration, Starmer's China defense) are ending up in separate clusters. Once they're separate clusters, they flow through the entire pipeline as separate stories with no dedup check anywhere.

**Where should deduplication happen?**

At the **per-leader dossier stage**, before stories are assembled. Two options:

1. **Fix clustering** — tune HDBSCAN params, lower the singleton absorption threshold (currently 0.85), or use a different clustering approach
2. **Add a post-clustering dedup pass** — after HDBSCAN, compare cluster centroids and merge clusters that are too similar (e.g., cosine similarity > 0.8)

The aggregate stage is the wrong place — it's designed for cross-leader matching, not same-leader dedup. By the time stories reach the aggregate builder, they should already be deduplicated within each leader.

---

## How the Pipeline Works (Context)

### Per-Leader Stage
1. **Snippet fetching**: Search results from wire services + domestic sources
2. **Embedding**: Snippets embedded with sentence-transformers
3. **Clustering**: HDBSCAN groups snippets into event clusters
4. **Scoring**: Events scored by source diversity + wire coverage
5. **Full article fetch**: Top events get up to 3 articles fetched via Diffbot
6. **Story synthesis**: Each event → LLM synthesizes an AP-style Story with scope (international/domestic)
7. **Dossier assembly**: Top 7 stories → `main_stories`, overflow split by scope → `international_stories` / `domestic_stories`

### Aggregate Stage
1. **Collection**: ALL stories from ALL dossiers collected (main + intl + dom from each leader)
2. **Cross-leader matching**: Stories matched via 2+ shared entity URIs (only across different leaders)
3. **Re-synthesis**: Matched story groups → LLM writes a NEW combined narrative covering all leaders
4. **Standalone passthrough**: Unmatched stories used as-is from their dossiers
5. **Ranking**: All stories sorted by score (multi-leader stories get 20% boost per additional leader)
6. **Final assembly**: Top 7 → aggregate `main_stories`, overflow split by scope → aggregate `international_stories` / `domestic_stories`

**Key point**: Aggregate main stories are a mix of:
- **Re-synthesized multi-leader stories** (LLM writes fresh combined narrative)
- **Standalone per-leader stories** (used verbatim from the dossier)

---

## 1. Why is the top main story a mega-cluster?

The first story tags 8 leaders and cites ~50 sources. This is caused by the **transitive union-find merging** in `AggregateBriefingBuilder._find_shared_stories` (`src/agents/aggregate_builder.py:132-208`). Two stories from different leaders are merged if they share 2+ entity URIs. Then the union-find groups them transitively: Story A (Starmer-Xi) overlaps Story B (Xi-Putin), which overlaps Story C (Putin-Zelenskyy), which overlaps Story D (Zelenskyy-Rutte), etc. The entire chain collapses into one mega-group. The LLM then synthesizes that mega-group into a single kitchen-sink narrative.

The 2-entity threshold is low enough that stories sharing just "China" + "United States" (as entity URIs) get linked. The transitive closure means a single shared entity between two pairs can chain everything together.

## 2. Why are there singletons (stories with 1 source) in main stories?

Two factors:

- **Per-leader dossier builder** (`src/agents/dossier_builder.py:96-99`): Takes top 7 events by score regardless of source count. A singleton from Reuters scores `1.0 × 1.5 (wire bonus) + log(2) × 0.5 ≈ 1.85`. If a leader only had a few multi-source events, singletons fill the top 7.
- **Aggregate builder** (`src/agents/aggregate_builder.py:93-95`): Collects ALL stories from ALL dossiers (main + intl + dom) and takes top 7 by score. No minimum source threshold is enforced at either level.

Stories like "Columnist warns Labour electoral stance" (1 Guardian source) and "German chancellor calls Europe alternative" (1 AP source) made it because there's no floor on source count.

## 3. Why does "Starmer defends China visit" appear in both Main Stories and International Stories?

Two near-identical stories from the same leader (Starmer) weren't merged:
- Main: "Starmer defends China engagement after Trump criticism" (Reuters)
- International: "Starmer defends China visit after Trump warning" (AP News)

**This is a clustering failure at the dossier level, not an aggregate-level problem.** These two snippets should have been grouped into the same event cluster during HDBSCAN clustering. Instead, they became separate events, which produced separate stories in Starmer's dossier.

The aggregate builder's entity-matching (`src/agents/aggregate_builder.py:168`) explicitly **skips same-leader pairs**: `if leader_i == leader_j: continue`. This is by design — the aggregate stage is meant to find cross-leader overlaps, not deduplicate within a leader. Same-leader deduplication should happen upstream at clustering time.

**The fix belongs in the clustering stage**, not the aggregate stage.

## 4 & 5. Duplicate Stubb stories and duplicate Mexico City-Toluca train stories

Same root cause as #3 — **clustering failures at the dossier level**.

The Stubb case: Three separate Helsingin Sanomat articles about the same parliamentary address clustered as three separate events.

The train case: El Universal and La Jornada covering the same inauguration clustered as separate events.

HDBSCAN with `min_cluster_size=2, epsilon=0.3` didn't group them. Possible reasons:
- Short snippets produce noisy embeddings
- Different angles/framing of the same event produce different embedding vectors
- Singleton absorption threshold (`0.85` similarity) is too strict for paraphrased coverage

These then pass through the full pipeline as separate events. There's no downstream dedup because **deduplication is supposed to happen at clustering time**.

## 6. Why do dossiers have lots of single-source citations like "(BBC News 1)"?

The `source_refs` on a Story come only from articles that were **actually fetched**, not from the full snippet cluster. In `event_clustering.py:136-139`:

```python
rest_thin = [s for s in rest_scored if s.cluster.unique_source_count < 3]
rest_events += await self._process_events(rest_thin, max_articles_per_event=1)
```

For remaining events with fewer than 3 unique sources, **only 1 full article is fetched**. Even for top events (max 3 articles), if the cluster only had snippets from 1 source, you get 1 source in the story. The snippet-level source diversity (used for scoring) doesn't carry through to the story's displayed source references.

## 7. How are the aggregate briefing's "international" and "domestic" stories built?

Two-stage process:

**Stage 1 — Per-leader** (`dossier_builder.py:86-103`): Claude classifies each event as `international` or `domestic` during synthesis (line 191: `"scope": "international or domestic"`). All stories sorted by score. Top 7 → `main_stories`. Overflow split by scope → `international_stories` / `domestic_stories`.

**Stage 2 — Aggregate** (`aggregate_builder.py:66-99`): Collects ALL stories from ALL leaders (main + intl + dom lists). Matches across leaders via 2+ shared entity URIs. Matched groups get re-synthesized into combined narratives. Standalone stories pass through as-is. Everything sorted by boosted score. Top 7 → aggregate `main_stories`. Overflow split by scope → aggregate `international_stories` / `domestic_stories`.

The scope label sticks from Claude's original per-leader classification. No reclassification happens at the aggregate level. This is why "Starmer defends China visit" can appear as a main story (high score) while an almost-identical version appears in international (lower score, classified as international scope).

---

## Summary of Structural Issues

| Issue | Root Cause | Where to Fix |
|-------|-----------|--------------|
| Same-event duplicates | **No dedup exists** — HDBSCAN under-clustering | `clustering/` — add LLM dedup pass after HDBSCAN |
| Mega-clusters (per-leader) | Actor over-indexing in embeddings | `clustering/` — strip counterparties, use `'leaf'` selection for sub-clustering |
| Mega-clusters (aggregate) | Transitive entity merging with low threshold (2 URIs) | `aggregate_builder.py` — raise threshold or limit transitivity |
| Singletons in main stories | No minimum source count | `dossier_builder.py` and/or `aggregate_builder.py` — add 2+ source floor |
| Single-source citations | Only fetched articles shown | `event_clustering.py` — fetch more articles per event |
| Story arcs out of order | No temporal awareness, no developing-story detection | `clustering/` — add story arc detection pass, merge or group related events |

**Key insight**: There is no deduplication system. HDBSCAN clustering is supposed to group same-event snippets together, but it's under-clustering. Once snippets become separate clusters, nothing downstream catches duplicates. The fix belongs at the per-leader clustering stage, not the aggregate stage.

---

## Technical Refinements (Clustering)

### Actor Over-Indexing Problem

The embedding model (`bge-small-en-v1.5`) treats **actors** as the primary signal and **events** as noise. When a leader is in a dominant, multi-front relationship (Sheinbaum-Trump), distinct events (trade, oil, extradition) collapse into one mega-cluster because the actor names dominate the embedding space.

**Current mitigation:** `SnippetEmbedder._strip_leader_name()` removes the tracked leader's name before embedding.

**Gap:** Counterparty names (Trump, Xi, Putin) are not stripped. These create "semantic gravity" that pulls unrelated events together.

**Potential fix:** In a sub-clustering pass, also replace major counterparties with generic tokens like `[COUNTERPARTY]` to force the embedding to represent verbs and nouns (actions) rather than actors.

### HDBSCAN Selection Method: `leaf` vs `eom`

Current configuration uses the default `cluster_selection_method='eom'` (Excess of Mass), which finds large, stable "mountains" — good for initial clustering.

For **sub-clustering mega-clusters**, switch to `cluster_selection_method='leaf'`:
- `'leaf'` selects the smallest, most homogeneous nodes at the bottom of the hierarchy
- This splits actor-dominated mega-clusters into distinct event-level atoms
- Use alongside tighter epsilon (current: `0.1` for sub-clustering)

```python
# In _split_megaclusters()
sub_clusterer = hdbscan.HDBSCAN(
    min_cluster_size=2,
    min_samples=2,
    cluster_selection_epsilon=0.1,
    cluster_selection_method='leaf',  # ADD THIS
    metric="euclidean",
)
```

### Near-Miss Absorption Relaxation

Current absorption: requires similarity ≥ 0.85 AND gap ≥ 0.03.

**Proposed relaxation:** Also absorb if:
- Similarity ≥ 0.80
- Gap ≥ 0.20 (clearly better than all alternatives)
- Only one cluster is a candidate

This catches "long-tail" mentions that are statistically more likely to be the same event than a new story.

### Source Overlap Validation (Anti-Fragmentation)

Risk: Sub-clustering with tight epsilon can over-fragment, splitting one event because sources used different vocabulary.

**Safety check:** Before accepting sub-clusters, verify source overlap:
- If two sub-clusters share 3+ unique sources (e.g., both have AP, BBC, Reuters), they are almost certainly the same event
- Re-merge regardless of embedding distance

```python
def should_merge_subclusters(c1: EventCluster, c2: EventCluster) -> bool:
    shared_sources = c1.sources & c2.sources
    return len(shared_sources) >= 3
```

### Two Distinct Problems

The feedback conflates two opposite problems:

| Problem | Symptom | Cause | Fix |
|---------|---------|-------|-----|
| **Actor over-indexing** | Mega-clusters (over-merging) | Actor names dominate embeddings | Strip counterparties, use `'leaf'` selection |
| **Under-clustering** | Duplicates (Stubb, Starmer) | Embeddings too far apart | LLM dedup pass, relax absorption threshold |

These need different fixes. Actor-blind embedding helps mega-clusters but won't fix under-clustering. LLM dedup helps under-clustering but won't fix mega-clusters.

---

## How Scoring Works

### The Formula (`src/clustering/scorer.py`)

```
score = diversity_score + size_score

where:
  diversity_score = unique_source_count × 1.0 × (1.5 if has_wire else 1.0)
  size_score = log(1 + snippet_count) × 0.5
```

### Example Scores

| Event | Sources | Wire? | Snippets | Calculation | Score |
|-------|---------|-------|----------|-------------|-------|
| Multi-source wire story | 4 | Yes | 6 | (4 × 1.0 × 1.5) + (log(7) × 0.5) = 6.0 + 0.97 | **6.97** |
| Multi-source domestic | 3 | No | 4 | (3 × 1.0 × 1.0) + (log(5) × 0.5) = 3.0 + 0.80 | **3.80** |
| Singleton from Reuters | 1 | Yes | 1 | (1 × 1.0 × 1.5) + (log(2) × 0.5) = 1.5 + 0.35 | **1.85** |
| Singleton from domestic | 1 | No | 1 | (1 × 1.0 × 1.0) + (log(2) × 0.5) = 1.0 + 0.35 | **1.35** |

### Top Event Selection (`filter_top_events`)

After scoring, events are split into "top" and "rest":

1. Take the highest score as reference
2. Threshold = top_score × 0.5 (`min_score_ratio`)
3. Include up to 5 events (`max_events`) that meet the threshold
4. Everything else goes to "rest"

**Example:** If top score is 6.97, threshold is 3.49. Events scoring ≥3.49 make the top list (up to 5). A singleton at 1.85 would normally go to "rest" — but if there aren't 5 events above threshold, singletons fill the remaining slots.

### Aggregate-Level Score Boost

The aggregate builder (`aggregate_builder.py:89-91`) boosts multi-leader stories:

```python
if len(story.contributing_leaders) > 1:
    story.score *= (1.0 + 0.2 * len(story.contributing_leaders))
```

- 2-leader story: 1.2× original score
- 3-leader story: 1.4× original score
- etc.

### Where Scoring Flows in the Pipeline

```
Per-leader:
  clusters → scorer.score_events() → ScoredEvent with .score
           → dossier_builder → Story objects inherit .score from event

Aggregate:
  all stories collected → multi-leader boost applied
                        → sorted by .score → top 7 = main stories
```

The score computed at clustering time flows unchanged through the entire pipeline (except for the multi-leader boost).

---

## Problems with Current Scoring

### 1. No minimum source count floor

Nothing prevents a 1-source story from becoming a "main story." The scoring formula gives singletons low scores, but if a leader doesn't have enough multi-source events, singletons fill the top 7 per-leader slots. Then they compete at the aggregate level.

### 2. Singletons can dominate sparse leaders

If a leader only has 3 multi-source events and 10 singletons, the top 7 per-leader will include 4 singletons. These then flow to the aggregate where they compete with better-sourced stories from other leaders.

### 3. Wire bonus applies equally to singletons

A Reuters singleton scores 1.85, which isn't much lower than a 2-source domestic story at 2.35. The wire bonus (1.5×) was designed to reward stories that wire services deemed newsworthy, but for singletons it just inflates weak stories.

### 4. No re-scoring at aggregate level

Scores computed per-leader aren't recalibrated when stories are pooled. A "top story" for a sparse leader (score 2.0) competes directly with overflow from a dense leader (score 3.5). The sparse leader's weak stories can crowd out the dense leader's stronger overflow.

### 5. Size bonus has minimal impact

The size component `log(1 + snippets) × 0.5` maxes out around 1.0 even for large clusters. A 10-snippet cluster only gets +1.2 from size. This was intentional (to avoid syndicated stories dominating), but it means source diversity is almost the entire signal.

---

## Potential Scoring Improvements

### Option A: Add minimum source threshold

**At per-leader level:**
```python
# Only include events with 2+ sources in main_stories
main_candidates = [s for s in all_stories if s.source_count >= 2]
main_stories = main_candidates[:7]
# Singletons go directly to international/domestic overflow
```

**At aggregate level:**
```python
# Only consider stories with 2+ sources for aggregate main
candidates = [s for s in all_candidates if s.source_count >= 2]
main_stories = candidates[:7]
```

**Pros:** Simple, directly addresses the singleton problem
**Cons:** May exclude legitimate breaking news that only has one source so far

### Option B: Penalize singletons more aggressively

Change the scoring formula to penalize low source counts:

```python
def _compute_score(self, cluster: EventCluster) -> float:
    source_count = cluster.unique_source_count

    # Singletons get heavy penalty
    if source_count == 1:
        diversity_score = 0.5  # Fixed low score
    else:
        diversity_score = source_count * self.diversity_weight

    if cluster.has_wire_coverage:
        diversity_score *= self.wire_bonus

    size_score = math.log1p(len(cluster.snippets)) * self.size_weight

    return diversity_score + size_score
```

**Pros:** Singletons naturally sink to the bottom
**Cons:** Might be too harsh for legitimate exclusive stories

### Option C: Require corroboration for main stories

Only stories with 2+ sources OR wire coverage can be "main stories":

```python
def is_main_eligible(story: Story) -> bool:
    return story.source_count >= 2 or story.has_wire
```

**Pros:** Wire singletons (likely legitimate breaking news) still qualify
**Cons:** Still allows some singletons through

### Option D: Re-score at aggregate level

When collecting stories for the aggregate, recalibrate scores based on the global distribution:

```python
# Normalize scores across all leaders
all_scores = [s.score for s in all_stories]
mean_score = statistics.mean(all_scores)
std_score = statistics.stdev(all_scores)

for story in all_stories:
    story.normalized_score = (story.score - mean_score) / std_score
```

Then rank by normalized score. This prevents weak leaders from polluting the aggregate with their "top" stories that are objectively weak.

**Pros:** Fair comparison across leaders with different coverage levels
**Cons:** More complex, may have edge cases

### Option E: Separate singleton track

Don't mix singletons with multi-source stories at all:

```python
# Per-leader
multi_source_stories = [s for s in all_stories if s.source_count >= 2]
singleton_stories = [s for s in all_stories if s.source_count == 1]

main_stories = multi_source_stories[:7]
# Singletons go to a separate "Also Noted" or "Developing" section
```

**Pros:** Clean separation, singletons don't compete with corroborated stories
**Cons:** Requires new section in brief format, more complexity

### Recommendation

**Start with Option A (minimum source threshold)** — it's the simplest fix and directly addresses the problem. Apply at both per-leader and aggregate levels:

1. Per-leader: Only stories with 2+ sources can be `main_stories`
2. Aggregate: Only stories with 2+ sources compete for top 7

Singletons still appear in `international_stories` and `domestic_stories` sections, but they don't crowd out corroborated stories from the main brief.

If that's too aggressive, fall back to **Option C (corroboration OR wire)** — this lets breaking news from Reuters/AP through while still filtering out random domestic singletons.

---

## Temporal Ordering and Story Arcs

### The Problem

Related stories have temporal sequences that get lost when sorted purely by score. Example from this brief — the Cuba oil story:

1. **Feb 1-2**: Mexico pauses oil shipments (responding to Trump pressure)
2. **Feb 2-3**: Mexico announces humanitarian aid instead
3. **Feb 4**: Sheinbaum denies agreeing to Trump's request

These are **distinct events** (correctly not merged by dedup) but **narratively linked** (a developing story). Showing them by score alone loses the thread and confuses the reader.

### Options

#### Option A: Merge developing stories into one narrative

Ask the LLM during synthesis: "These events are part of the same developing story. Write a single narrative covering the full arc chronologically."

```
Mexico's Sheinbaum navigates Cuba oil pressure
  Feb 1: Paused shipments after Trump call
  Feb 2: Announced humanitarian aid instead
  Feb 4: Denied agreeing to Trump's request
```

**Pros:** Clean, coherent, reader gets the full picture
**Cons:** Need to detect which events are "same developing story" (another clustering problem)

#### Option B: Group related stories, order chronologically within group

Keep stories separate but display together:

```
## Mexico-Cuba Oil Dispute

### Mexico pauses oil shipments to Cuba (Feb 1)
[narrative]

### Mexico announces humanitarian aid for Cuba (Feb 2)
[narrative]

### Sheinbaum denies Trump agreement on Cuba (Feb 4)
[narrative]
```

**Pros:** Preserves granularity, shows sequence
**Cons:** Needs topic/thread detection, format change

#### Option C: Chronological ordering as tiebreaker

When stories have similar scores (within 10-15%), order by date:

```python
def sort_key(story):
    return (-story.score, story.earliest_date)  # score desc, then date asc
```

**Pros:** Simple, no format change
**Cons:** Only helps when scores are close; doesn't group related stories

#### Option D: Add dates prominently to narratives

Don't change ordering, but make dates visible in the dateline:

```
MEXICO CITY, Feb. 4 — President Sheinbaum denied...
```

**Pros:** Minimal change, AP style already supports this
**Cons:** Reader still sees stories out of sequence

#### Option E: "Developing Story" section

Detect multi-beat stories and present them separately:

```
## Developing Stories

### Mexico-Cuba Oil Dispute
A timeline of this week's developments...
[chronological narrative]

## Other Main Stories
[single-event stories ranked by score]
```

**Pros:** Clear separation between ongoing situations and discrete events
**Cons:** Significant format change, needs thread detection

### The Core Question

Are these:
1. **Separate stories** that happen to be related? → Group/order them (Options B, C, E)
2. **One developing story** with multiple beats? → Merge them (Option A)

Right now the pipeline treats them as separate (correct for dedup), but the brief format assumes stories are independent (incorrect for reader comprehension).

### Story Arc Detection Approaches

If we want to merge or group developing stories, we need to detect them:

1. **Entity overlap + temporal proximity** — if two events share 3+ entities and are within 3 days, they might be one developing story

2. **LLM judgment** — after clustering, ask "which of these events are part of the same developing story?" Similar to the dedup pass but looking for narrative arcs rather than duplicates.

3. **Topic modeling** — cluster stories by topic (separate from event clustering), then merge events within each topic chronologically

This is the inverse of the dedup problem:
- Dedup: "Are these the same event?" → Merge if yes
- Story arc: "Are these the same ongoing situation?" → Group/merge if yes

### Recommendation

**Option A (merge developing stories)** is probably right for the reader. The Cuba situation is one story with updates, not three separate stories.

Implementation approach: Add an LLM-based "story arc detection" pass after event clustering but before scoring. Similar structure to the dedup pass:

```
clusters → dedup pass → story arc pass → score → fetch → synthesize
                              ↓
                    groups events into arcs,
                    merges or flags for grouped display
```

The story arc pass would:
1. Present all event titles to LLM
2. Ask which events are part of the same developing story
3. Either merge them into one event (for single narrative) or tag them for grouped display

---

## Format Changes

### Renaming
- "Main Stories" → **"Top Stories"**
- "International Stories" → **"International"**
- "Domestic Stories" → **"Domestic"**

### Top Stories
- Reduce from 7 to **4-5 stories**
- More concise: **3-4 sentences** (summarize, don't rewrite)
- For multi-leader shared stories: same conciseness, but synthesis covers all leaders

### Brief Structure
- **Remove Leader Dossiers** from the aggregated brief
- Keep dossiers as separate files for deep-dive reference, but the main brief should be standalone

### Rationale
The brief should be scannable. 7 stories with 5+ sentences each is too dense. Top stories are summaries pointing to the full picture, not comprehensive rewrites. Leader dossiers duplicate content already in the aggregate sections.

---

## Implementation Plan

### Phase 1: Core Fixes (High Priority)

#### 1.1 LLM Dedup Pass (`src/clustering/dedup.py`)

Add post-HDBSCAN deduplication using LLM judgment.

**New file:** `src/clustering/dedup.py`

```
Pipeline position: clusters → [LLM DEDUP] → score → fetch → synthesize
```

**Function:** `deduplicate_clusters(clusters, leader_name) -> clusters`
- Present all cluster titles to LLM
- Ask which clusters are the same event
- Merge identified duplicates
- Single LLM call per leader (~500 tokens)

**Integration point:** `EventClusteringAgent.process_leader()` after step 5 (cluster), before step 6 (score)

#### 1.2 Megacluster Splitting Improvements (`src/clustering/clusterer.py`)

Enhance `_split_megaclusters()` with:

1. **`leaf` selection method** — find atomic events at bottom of hierarchy
2. **Counterparty stripping** — remove high-frequency entities before re-embedding
3. **Source overlap validation** — re-merge sub-clusters sharing 3+ sources

**Changes to `EventClusterer`:**
- Add `_strip_counterparties(snippets, threshold=0.5)` method
- Update `_split_megaclusters()` to use `cluster_selection_method='leaf'`
- Add `_validate_subclusters(subclusters)` with source overlap check

#### 1.3 Absorption Threshold Relaxation (`src/clustering/clusterer.py`)

Update `_absorb_singletons()` to also absorb when:
- Similarity ≥ 0.80 (currently 0.85)
- Gap ≥ 0.20 (currently 0.03)

This catches long-tail paraphrased mentions.

#### 1.4 Minimum Source Threshold (`src/agents/dossier_builder.py`, `src/agents/aggregate_builder.py`)

**Per-leader:** Only stories with 2+ sources can be `main_stories`
**Aggregate:** Only stories with 2+ sources compete for top 7

Singletons flow to `international_stories` / `domestic_stories` based on scope.

### Phase 2: Enhanced Processing (Medium Priority)

#### 2.1 Fetch All Sources (`src/agents/event_clustering.py`)

Change article fetch to retrieve all sources in the cluster, not just 2-3.

**Change:** `max_articles_per_event` → fetch all URLs in cluster (up to reasonable limit like 10)

This improves `source_refs` display without affecting scoring.

#### 2.2 Story Arc Detection (`src/clustering/story_arc.py`)

New module to detect developing stories.

**Function:** `detect_story_arcs(clusters, leader_name) -> list[StoryArc]`
- Present cluster titles + dates to LLM
- Ask which events are part of same developing story
- Return arc groupings for merged synthesis

**Integration:** After dedup, before scoring

### Phase 3: Aggregate Fixes (Lower Priority)

#### 3.1 Limit Transitive Merging (`src/agents/aggregate_builder.py`)

Prevent mega-clusters at aggregate level by:
- Raising entity overlap threshold from 2 to 3
- Or limiting transitivity depth (max 3 stories per merged group)

#### 3.2 Aggregate Score Normalization

Add z-score normalization when pooling stories from all leaders.

---

## File Changes Summary

| File | Changes |
|------|---------|
| `src/clustering/dedup.py` | **NEW** — LLM dedup pass |
| `src/clustering/clusterer.py` | Megacluster improvements, absorption relaxation |
| `src/clustering/__init__.py` | Export new functions |
| `src/agents/event_clustering.py` | Integrate dedup pass, increase fetch limit |
| `src/agents/dossier_builder.py` | Add 2+ source threshold for main_stories |
| `src/agents/aggregate_builder.py` | Add 2+ source threshold, limit transitivity |
| `src/clustering/story_arc.py` | **NEW** — Story arc detection (Phase 2) |

---

## Proposed Pipeline (After Implementation)

```
Per-leader:
  1. Fetch snippets
  2. Embed (strip leader name)
  3. HDBSCAN cluster
  4. [NEW] LLM dedup pass — merge same-event clusters
  5. [NEW] Story arc detection — group developing stories
  6. [IMPROVED] Split megaclusters (leaf + counterparty strip + source validation)
  7. Score events
  8. [IMPROVED] Fetch ALL articles per event
  9. Synthesize stories (arcs get chronological treatment)
  10. [NEW] Filter: 2+ sources for main_stories

Aggregate:
  1. Collect all stories
  2. [IMPROVED] Cross-leader matching (3+ entities, limited transitivity)
  3. Re-synthesize shared stories
  4. [NEW] Filter: 2+ sources for main_stories
  5. Rank and assemble
```

---

## To-Do List

### High Priority

#### Opinion/Commentary Detection Improvements

**Problem**: Opinion pieces are slipping through to final output (e.g., "Opinion piece compares Trump, Sheinbaum through literary analysis" in Feb 6 Sheinbaum dossier).

**Current approach**: Pattern matching on "person:title" — but this matches our principals (leaders we're tracking), so it's not reliable.

**Proposed improvements**:

1. **URL pattern detection**:
   - `/opinion/` path segments
   - `/columnas/` (Spanish)
   - `/editorial/`
   - `/op-ed/`
   - Known opinion columnist URL patterns

2. **Snippet language signals**:
   - First-person pronouns ("I think", "in my view", "yo creo")
   - Speculative language ("appears to", "seems to", "suggests that")
   - Literary/philosophical references (García Lorca, Freud, etc.)
   - Lack of direct quotes or attribution

3. **Source metadata**:
   - Tag known opinion sections of publications
   - Columnist bylines vs reporter bylines

4. **LLM classification**:
   - Add opinion/news classification to snippet processing
   - Filter or demote opinion content before clustering

**Implementation location**: `src/clustering/embedder.py` (relevance filter) or new `src/clustering/opinion_filter.py`

---

### Cross-Leader Story Merging Issues

**Problem**: The aggregate builder is merging unrelated stories across leaders when they share common entities (like "U.S.", "trade", or counterparty names). Example from Feb 6 brief:

> "Bessent warns Carney on trade criticism as Mexico navigates Cuba tensions (Sheinbaum, Carney)"

This incorrectly combines:
- Bessent/Carney trade dispute (Canada-US USMCA context)
- Sheinbaum/Cuba oil policy (Mexico-Cuba-US context)

These are completely unrelated stories that happen to share "U.S." as an entity.

**Root cause**: The 2-entity overlap threshold in `aggregate_builder.py` is too permissive, and transitive merging chains stories together through shared entities like major powers.

**Proposed fixes**:
1. Raise entity overlap threshold from 2 to 3+ for cross-leader merging
2. Filter out high-frequency entities ("United States", "China", "European Union") from overlap calculations
3. Require thematic similarity (LLM judgment) before merging, not just entity overlap
4. Limit transitivity depth — don't chain A→B→C if A and C don't directly overlap

---

### Story Arc Detection (Under-clustering of Related Events)

**Problem**: The Orsi China visit is fragmented into 10+ separate stories when it should be ONE major developing story:

From the Feb 6 Orsi dossier:
- "Uruguay, China Sign 11 Agreements During Orsi State Visit" (Top)
- "Uruguay's Orsi visits automated port in Shanghai" (Top)
- "Uruguay's Orsi meets with Chinese President Xi Jinping" (Top)
- "Uruguay's Orsi begins China state visit to boost trade" (Top)
- "Uruguay's Orsi leads 150-person delegation to China" (Intl)
- "Uruguay's Orsi leads largest trade delegation to China" (Intl)
- "Uruguay's Orsi pitches country to Chinese business leaders" (Intl)
- ... and more

All of these are **the same story** — Orsi's state visit to China.

**Current behavior**: HDBSCAN treats each day/angle as a separate event because embeddings are too different (different cities, different activities, different quotes).

**Proposed fix**: Add a **Story Arc Detection** pass after clustering:
1. Group events by shared major theme + temporal proximity (same week)
2. LLM judgment: "Are these part of the same developing story?"
3. Merge into a single chronological narrative covering the full arc

This is the inverse of dedup:
- Dedup: "Is this the same event?" (same day, same quotes)
- Story arc: "Is this the same developing situation?" (multi-day, related events)

**Implementation**: New `src/clustering/story_arc.py` module, runs after dedup but before scoring.

---

### International/Domestic Section Format Change

**Current format**: Full multi-paragraph stories in International/Domestic sections, essentially duplicating dossier content.

**Proposed format**: Headlines that link to dossiers + one-sentence summary:

```markdown
## International

### 🇨🇦 Canada

- [Canada scraps EV mandate, introduces purchase incentives](/dossiers/mark_carney.md#canada-scraps-ev-mandate-introduces-purchase-incentives) — Carney replaces 2035 EV sales mandate with C$2.3B purchase incentives and stricter emissions standards.

- [Carney announces $7.4 billion auto industry transformation strategy](/dossiers/mark_carney.md#carney-announces-74-billion-auto-industry-transformation-strategy) — New spending to boost EV production and reduce U.S. trade dependence.

### 🇲🇽 Mexico

- [Mexico's Sheinbaum says will cooperate in Epstein investigation if asked](/dossiers/claudia_sheinbaum.md#mexicos-sheinbaum-says-will-cooperate-in-epstein-investigation-if-asked) — President says DOJ formal request required for collaboration.

### 🇧🇷 Brazil

- [Brazil's Lula meets Russian PM, backs multilateralism](/dossiers/lula_da_silva.md#brazils-lula-meets-russian-pm-backs-multilateralism) — Leaders discuss untapped $10.9B trade potential at bilateral commission.
```

**Benefits**:
1. Much more scannable — readers see headlines at a glance
2. No content duplication — dossiers have the full story
3. Country grouping provides geographic context
4. Emoji flags aid quick visual scanning
5. Links create navigation to deep-dive content

**Implementation**:
1. Update dossier generation to include anchor IDs in headings
2. Update aggregate brief template to use country-grouped headline format
3. Add one-sentence summary generation (can use existing title or add LLM call)
4. Add country→emoji mapping utility

**File changes**:
- `src/agents/aggregate_builder.py` — new template format
- `src/agents/dossier_builder.py` — ensure anchors in headings
- `src/config.py` — add country→emoji mapping

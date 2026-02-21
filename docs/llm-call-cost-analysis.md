# LLM Call & Cost Analysis

Analysis of pipeline LLM calls before and after commit `c666fa3` (2026-02-20),
which enabled extended thinking, prompt caching, batch API, and consolidated
LLM round-trips.

## Variables

- **N** = number of leaders (currently 15)
- **E** = events per leader (typically ~8)
- **S** = shared cross-leader story groups (typically ~3)

---

## LLM Calls Per Stage

### Stage 1: Event Clustering (per leader)

| Step | Before | After |
|------|--------|-------|
| Dedup clusters | 1 `complete()` call | merged |
| Story arc detection | 1 `complete()` call | merged |
| Combined `reason_about_clusters()` | — | 1 `complete()` call |
| **Subtotal (×N)** | **2N** | **N** |

- Before: `deduplicate_clusters()` + `detect_story_arcs()` as two sequential calls
- After: `reason_about_clusters()` combines both via CoT with `remaining_distinct_events` bridge

### Stage 2: Dossier Building (per leader)

| Step | Before | After |
|------|--------|-------|
| Synthesize event | E sequential `complete()` calls | 1 `batch_complete()` with E requests |
| Classify story | E sequential `complete()` calls | merged into synthesis prompt |
| Between the Lines | 1 `complete()` call | merged |
| Executive summary | 1 `complete()` call | merged |
| BTL + summary combined | — | 1 `complete()` call |
| **Subtotal (×N)** | **2E + 2 per leader** | **E + 1 per leader** |

- Synthesis prompt now includes `event_type`, `leader_role`, `impact_level` fields — no separate classify call
- BTL + executive summary collapsed into `_generate_btl_and_summary()` (single CoT)
- Batch API submits all E synthesis requests as one async operation

### Stage 3: Aggregate Briefing

| Step | Before | After |
|------|--------|-------|
| Validate shared groups | S `complete()` calls | merged |
| Synthesize shared stories | S `complete()` calls | merged |
| Validate + synthesize combined | — | S `complete()` calls |
| Aggregate BTL | 1 `complete()` call | merged |
| Executive summary | 1 `complete()` call | merged |
| BTL + summary combined | — | 1 `complete()` call |
| **Subtotal** | **2S + 2** | **S + 1** |

- `_validate_and_synthesize_group()` uses conditional output: if `same_topic=false`, skips synthesis
- `_generate_aggregate_btl_and_summary()` generates thematic BTL + exec summary in one call; per-leader BTL bullets appended via pure Python

### Call Count Totals

| | Formula | N=15, E=8, S=3 |
|--|---------|-----------------|
| **Before** | 2NE + 4N + 2S + 2 | **308** |
| **After** | NE + 2N + S + 1 | **154** |

**50% reduction across the board.**

---

## Model Assignment

### Before

All calls: `claude-sonnet-4-20250514` ($3/MTok input, $15/MTok output).
No extended thinking. `max_tokens=4096`.

### After

| Task type | Model | Thinking budget | Notes |
|-----------|-------|-----------------|-------|
| Cluster reasoning | Sonnet 4.5 (`claude-sonnet-4-5-20250929`) | 4,000 | Analytical |
| Event synthesis | Sonnet 4.5 (batch) | **disabled** | Structured extraction, not deep reasoning |
| BTL + summary | Opus 4.6 (`claude-opus-4-6`) | 16,000 | Editorial, quality matters |
| Validate + synthesize | Opus 4.6 | 16,000 | Editorial |
| Aggregate BTL + summary | Opus 4.6 | 16,000 | Editorial |

Model tiering rationale: Opus is reserved for the few high-value editorial calls (BTL,
executive summaries) where prose quality matters. Synthesis is structured extraction
(articles → AP-style JSON) that Sonnet 4.5 handles well — and at 120 calls per run,
it's the cost-dominant component. Thinking is disabled for synthesis since the task
is extraction, not reasoning.

---

## API Pricing Reference

| Model | Input | Output | Batch Input | Batch Output |
|-------|-------|--------|-------------|--------------|
| Sonnet 4 / 4.5 | $3/MTok | $15/MTok | $1.50/MTok | $7.50/MTok |
| Opus 4.6 | $15/MTok | $75/MTok | $7.50/MTok | $37.50/MTok |

Extended thinking tokens are billed at **output token rates**.
Prompt cache: 25% surcharge on cache writes, 90% discount on cache reads.

---

## Per-Call Token Estimates

Thinking budget is a maximum; actual usage varies. Estimates below reflect
typical usage observed in production.

### Before (Sonnet 4, no thinking)

| Call | System | User prompt | Output | Count (N=15, E=8, S=3) |
|------|--------|-------------|--------|------------------------|
| `deduplicate_clusters()` | ~150 | ~1,500 | ~300 | 15 |
| `detect_story_arcs()` | ~200 | ~800 | ~300 | 15 |
| `_synthesize_event()` | ~150 | ~3,000 | ~400 | 120 |
| `_classify_story()` | ~150 | ~300 | ~100 | 120 |
| `_generate_between_the_lines()` | ~150 | ~1,000 | ~200 | 15 |
| `_generate_executive_summary()` | ~150 | ~500 | ~150 | 15 |
| `validate_cross_leader_match()` | ~200 | ~500 | ~100 | 3 |
| `_synthesize_shared_story()` | ~150 | ~800 | ~300 | 3 |
| `_generate_agg_btl()` | ~150 | ~1,000 | ~200 | 1 |
| `_generate_agg_exec_summary()` | ~150 | ~1,000 | ~200 | 1 |

### After (mixed models, extended thinking)

| Call | Model | System | User prompt | Thinking | Text out | Count |
|------|-------|--------|-------------|----------|----------|-------|
| `reason_about_clusters()` | Sonnet 4.5 | ~250 | ~1,500 | ~2,000 | ~400 | 15 |
| `_batch_synthesize_events()` | Sonnet 4.5 (batch) | ~1,000 | ~3,000 | **0** | ~400 | 120 |
| `_generate_btl_and_summary()` | Opus | ~1,000 | ~1,000 | ~4,000 | ~300 | 15 |
| `_validate_and_synthesize_group()` | Opus | ~1,000 | ~600 | ~3,000 | ~400 | 3 |
| `_generate_thematic_btl_and_summary()` | Opus | ~1,000 | ~1,500 | ~4,000 | ~400 | 1 |

System prompts grew from ~150 tokens to ~1,000 tokens due to addition of AP style
reference and Paragon taxonomy inline documentation.

---

## Cost by Stage (N=15, E=8, S=3)

### Before

| Stage | Calls | Input tok | Output tok | Cost |
|-------|-------|-----------|------------|------|
| Clustering (dedup + arcs) | 30 | 39,750 | 9,000 | $0.25 |
| Dossier (synth + classify + BTL + summary) | 270 | 459,000 | 65,250 | $2.36 |
| Aggregate (validate + synth + BTL + summary) | 8 | 7,250 | 1,600 | $0.05 |
| **Total** | **308** | **506K** | **76K** | **$2.66** |

### After (initial — Opus + thinking everywhere)

| Stage | Calls | Input tok | Output tok | Rate | Cost |
|-------|-------|-----------|------------|------|------|
| Clustering (Sonnet 4.5) | 15 | 26,250 | 36,000 | standard | $0.62 |
| Dossier synthesis (Opus batch) | 120 | 480,000 | 768,000 | batch 50% off | $32.40 |
| Dossier BTL+summary (Opus) | 15 | 30,000 | 64,500 | standard | $5.29 |
| Aggregate (Opus) | 4 | 7,300 | 14,600 | standard | $1.21 |
| **Total** | **154** | **543K** | **883K** | | **$39.52** |

### After (optimized — Sonnet synthesis, no thinking)

Synthesis moved to Sonnet 4.5 with thinking disabled. Opus retained only for
BTL+summary (editorial prose) and aggregate calls.

| Stage | Calls | Input tok | Output tok | Rate | Cost |
|-------|-------|-----------|------------|------|------|
| Clustering (Sonnet 4.5 + thinking) | 15 | 26,250 | 36,000 | standard | $0.62 |
| Dossier synthesis (Sonnet 4.5 batch, no thinking) | 120 | 480,000 | 48,000 | batch 50% off | $1.08 |
| Dossier BTL+summary (Opus + thinking) | 15 | 30,000 | 64,500 | standard | $5.29 |
| Aggregate (Opus + thinking) | 4 | 7,300 | 14,600 | standard | $1.21 |
| **Total** | **154** | **543K** | **163K** | | **$8.20** |

### Comparison

| | Before | Initial | Optimized | Change (before→optimized) |
|--|--------|---------|-----------|---------------------------|
| Calls | 308 | 154 | 154 | **-50%** |
| Input tokens | 506K | 543K | 543K | +7% |
| Output tokens | 76K | 883K | 163K | +2.1× |
| **Cost per run** | **$2.66** | **$39.52** | **$8.20** | **~3×** |

The initial 15× cost explosion was caused by extended thinking on 120 Opus
synthesis calls (~720K thinking tokens at $37.50/MTok). Moving synthesis to
Sonnet 4.5 with thinking disabled eliminates this: output tokens drop from
883K to 163K, and the remaining output is billed at Sonnet batch rates ($7.50/MTok)
instead of Opus batch rates ($37.50/MTok).

### Cost Breakdown by Component (Optimized)

| Component | Cost | % of total |
|-----------|------|------------|
| Opus BTL+summary output (thinking + text) | $4.84 | 59% |
| Sonnet batch synthesis (input + output) | $1.08 | 13% |
| Aggregate (Opus, thinking + text) | $1.21 | 15% |
| Clustering (Sonnet, thinking + text) | $0.62 | 8% |
| Opus BTL+summary input | $0.45 | 5% |

The dominant cost is now Opus BTL+summary — exactly where quality matters most.

---

## Scaling Projections

Cost scales linearly with N (dominant term is NE for synthesis, N for BTL+summary).

| Leaders (N) | Before | Optimized | Marginal cost per leader |
|-------------|--------|-----------|--------------------------|
| 15 (current) | $2.66 | $8.20 | — |
| 20 | $3.54 | $10.63 | ~$0.49 |
| 30 | $5.30 | $15.50 | ~$0.49 |
| 45 | $7.93 | $22.80 | ~$0.49 |
| 60 | $10.56 | $30.10 | ~$0.49 |

Each additional leader adds ~$0.49/run (optimized), vs ~$0.18/run (before).

### Wall-Clock Latency

Sequential `complete()` calls are rate-limited at 2s each:

| | Before | After |
|--|--------|-------|
| Sequential calls | 308 × 2s = ~10 min | 2N + S + 1 = 34 × 2s = ~68s |
| Batch API polling | n/a | ~30-120s async |
| **Effective wall time** | **~10 min** | **~2-3 min** |

The batch API runs E synthesis requests per leader in parallel, removing them
from the sequential rate-limit bottleneck.

---

## Cost Reduction Levers

Status of levers identified during analysis:

1. ~~**Reduce thinking budget for synthesis**~~ — **DONE**: Thinking disabled entirely
   for batch synthesis. Structured extraction doesn't need scratchpad reasoning.

2. ~~**Move synthesis to Sonnet 4.5**~~ — **DONE**: Synthesis moved from Opus to
   Sonnet 4.5. 5× cheaper per token; quality is equivalent for structured extraction.

3. **Reduce thinking budget for BTL+summary** (16K → 8K): Now the dominant cost
   component at $5.29/run. Could save ~$2.50 if 8K thinking suffices for editorial.

4. **Prompt caching**: Already implemented. Saves ~$1/run on repeated system prompts
   across sequential calls. Limited benefit for batch requests.

5. **Reduce E (events per leader)**: Currently processes all clustered events.
   Could cap at top 10 and skip low-score singletons to reduce batch size.

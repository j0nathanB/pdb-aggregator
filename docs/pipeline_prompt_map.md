# Pipeline × Prompt Map

How every LLM call maps to the system architecture. Read alongside
[prompt_inventory.md](prompt_inventory.md) for full prompt text and
[ideal-brief-architecture-v2.md](ideal-brief-architecture-v2.md) for infra details.

---

## System Flow (with prompt callouts)

```
EventBridge (Sun 11 PM ET)
  │
  ▼
ECS Fargate Task ── scripts/run_pipeline.py
  │
  ├─ 1. src/graph.py  →  PDBWorkflow.run()
  │     │
  │     ├─ PER LEADER (parallel) ─────────────────────────────────────────────
  │     │   │
  │     │   ├─ FETCH ── src/agents/source_fetcher.py
  │     │   │   RSS/API fetch (no LLM)
  │     │   │   Placeholder generation if APIs down ─── [P1]
  │     │   │
  │     │   ├─ TRANSLATE ── src/agents/translator.py
  │     │   │   For non-English articles ─── [P2a] system + [P2b] user
  │     │   │   Title-only translation ─── [P2c]
  │     │   │
  │     │   ├─ TRANSCRIPT PROCESSING ── src/clustering/transcript_processor.py
  │     │   │   Mexican mañanera press conferences ─── [P3a] system + [P3b] user
  │     │   │   Single-topic event speeches ─── [P3c] system + [P3d] user
  │     │   │
  │     │   ├─ CLASSIFY ── src/agents/classifier.py
  │     │   │   Per-article classification ─── [P4a] system + [P4b] user
  │     │   │   Event extraction ─── [P4c]
  │     │   │   Article deduplication ─── [P4d] system + [P4e] user
  │     │   │
  │     │   ├─ CLUSTER ── src/clustering/
  │     │   │   HDBSCAN embedding clustering (no LLM)
  │     │   │   Combined dedup + arc detection ─── [P5a] system + [P5b] user
  │     │   │
  │     │   ├─ SYNTHESIZE ── src/agents/dossier_builder.py
  │     │   │   Per-event story synthesis ─── [P6a] system + [P6b] user
  │     │   │   Post-synthesis classification ─── [P6a] system + [P6c] user
  │     │   │   Non-English output translation ─── [P6a] system + [P6d] user
  │     │   │   BTL + executive summary ─── [P6a] system + [P6e] user
  │     │   │
  │     │   └─ OUTPUT: LeaderDossier
  │     │       (main_stories, intl_stories, domestic_stories, BTL, exec_summary)
  │     │
  │     ├─ AGGREGATE ── src/agents/aggregate_builder.py ──────────────────────
  │     │   │
  │     │   ├─ Cross-leader story matching (entity overlap, no LLM)
  │     │   ├─ Validate + synthesize shared stories ─── [P7a] system + [P7b] user
  │     │   └─ Global BTL + executive summary ─── [P7a] system + [P7c] user
  │     │
  │     └─ OUTPUT: WeeklyBrief
  │         (main_stories, leader_dossiers, exec_summary, BTL)
  │
  ├─ 2. src/persistence.py  →  save_brief()
  │     Write briefs/YYYYMMDD/ (overview.mdx, dossiers/*.mdx, JSON artifacts)
  │
  ├─ 3. src/persistence.py  →  generate_email()
  │     │
  │     └─ EMAIL DIGEST ── src/agents/email_digest.py
  │         Condense brief to email ─── [P8a] system + [P8b] user
  │         OUTPUT: email.html
  │
  ├─ 4. Upload artifacts to S3
  │     meta.json, dossiers.json, output.json, overview.mdx, email.html
  │
  ├─ 5. Push brief to docs repo ── push_brief_to_repo()
  │     Clone j0nathanb/docs, copy .mdx files
  │     update_docs_json()   (no LLM — navigation bookkeeping)
  │     update_archives_page() (no LLM — archives page rebuild)
  │     git push origin main
  │
  └─ 6. Send preview email to admin (SES, no LLM)

─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

Mintlify Cloud auto-deploys on push to main

GitHub Actions (docs repo) ── .github/workflows/deploy-and-notify.yml
  │
  ├─ Wait 45s for Mintlify CDN propagation
  └─ POST webhook → API Gateway → Lambda (email-distributor)
       │
       ├─ Load email.html from S3
       ├─ Query active subscribers from DynamoDB
       └─ Send via SES (idempotent, checks last_sent_brief_id)
```

---

## Prompt Index

### Per-Leader Stage (runs N times, once per leader)

| ID | Prompt | File | System | Temp | Model | Thinking |
|----|--------|------|--------|------|-------|----------|
| P1 | Placeholder article gen | `source_fetcher.py:360` | *(none)* | 0.7 | default | default |
| P2a | Translation system | `translator.py:19` | `TRANSLATION_SYSTEM` | — | — | — |
| P2b | Article translation | `translator.py:142` | `TRANSLATION_SYSTEM` | 0.1 | default | default |
| P2c | Title translation | `translator.py:175` | *(none)* | 0.1 | default | default |
| P3a | Press conference system | `transcript_processor.py:95` | `PRESS_CONFERENCE_SYSTEM` | — | — | — |
| P3b | Press conference extract | `transcript_processor.py:101` | `PRESS_CONFERENCE_SYSTEM` | 0.2 | default | default |
| P3c | Event speech system | `transcript_processor.py:133` | `EVENT_SPEECH_SYSTEM` | — | — | — |
| P3d | Event speech rewrite | `transcript_processor.py:138` | `EVENT_SPEECH_SYSTEM` | 0.2 | default | default |
| P4a | Classification system | `classifier.py:32` | `CLASSIFICATION_SYSTEM` | — | — | — |
| P4b | Article classification | `classifier.py:134` | `CLASSIFICATION_SYSTEM` | 0.1 | default | default |
| P4c | Event extraction | `classifier.py:258` | *(none)* | 0.1 | default | default |
| P4d | Dedup system | `classifier.py:369` | `DEDUPE_SYSTEM` | — | — | — |
| P4e | Article deduplication | `classifier.py:319` | `DEDUPE_SYSTEM` | 0.1 | default | default |
| P5a | Cluster reasoning system | `cluster_reasoning.py:21` | `REASONING_SYSTEM` | — | — | — |
| P5b | Dedup + arc detection | `cluster_reasoning.py:90` | `REASONING_SYSTEM` | 0.1 | `MODEL_ANALYTICAL` | 4k |
| P6a | Dossier system | `dossier_builder.py:37` | `DOSSIER_SYSTEM` | — | — | — |
| P6b | Event synthesis | `dossier_builder.py:138` | `DOSSIER_SYSTEM` | default | `MODEL_SYNTHESIS` | 0 |
| P6c | Story classification | `dossier_builder.py:193` | `DOSSIER_SYSTEM` | default | default | default |
| P6d | Ensure-English translation | `dossier_builder.py:1080` | `DOSSIER_SYSTEM` | 0.1 | default | default |
| P6e | BTL + exec summary | `dossier_builder.py:811` | `DOSSIER_SYSTEM` | 0.4 | `MODEL_EDITORIAL` | 16k |

### Aggregate Stage (runs once per brief)

| ID | Prompt | File | System | Temp | Model | Thinking |
|----|--------|------|--------|------|-------|----------|
| P7a | Aggregate system | `aggregate_builder.py:31` | `AGGREGATE_SYSTEM` | — | — | — |
| P7b | Validate + synthesize | `aggregate_builder.py:471` | `AGGREGATE_SYSTEM` | 0.3 | `MODEL_SYNTHESIS` | 0 |
| P7c | Global BTL + exec summary | `aggregate_builder.py:767` | `AGGREGATE_SYSTEM` | 0.4 | `MODEL_EDITORIAL` | 16k |

### Post-Processing (runs once per brief)

| ID | Prompt | File | System | Temp | Model | Thinking |
|----|--------|------|--------|------|-------|----------|
| P8a | Email digest system | `email_digest.py:36` | `SYSTEM_PROMPT` | — | — | — |
| P8b | Email digest generation | `email_digest.py:52` | `SYSTEM_PROMPT` | 0.3 | default | default |

---

## Call Volume per Brief Run

Assuming 15 leaders, ~12 articles each, ~8 clusters each, ~6 shared story groups:

| Stage | Calls per leader | × Leaders | Total calls |
|-------|-----------------|-----------|-------------|
| Translation (P2b+P2c) | 0–12 (non-EN only) | ~4 leaders | ~30 |
| Transcript processing (P3b/P3d) | 0–5 | 1 leader (Mexico) | ~3 |
| Article classification (P4b) | ~12 | 15 | ~180 |
| Event extraction (P4c) | ~12 | 15 | ~180 |
| Article dedup (P4e) | 1 | 15 | 15 |
| Cluster reasoning (P5b) | 1 | 15 | 15 |
| Event synthesis (P6b) | ~8 | 15 | ~120 |
| Story classification (P6c) | ~8 | 15 | ~120 |
| Ensure-English (P6d) | 0–8 (non-EN only) | ~4 leaders | ~20 |
| BTL + exec summary (P6e) | 1 | 15 | 15 |
| Validate + synthesize (P7b) | — | — | ~6 |
| Global BTL + summary (P7c) | — | — | 1 |
| Email digest (P8b) | — | — | 1 |
| **Total** | | | **~700** |

---

## Token Cost Breakdown (approximate per run)

| Model | Calls | Avg input | Avg output | Cost/1K in | Cost/1K out | Subtotal |
|-------|-------|-----------|------------|------------|-------------|----------|
| Opus (`MODEL_EDITORIAL`) | ~16 | 3K | 500 | $0.015 | $0.075 | ~$1.30 |
| Sonnet (`MODEL_SYNTHESIS`) | ~250 | 4K | 300 | $0.003 | $0.015 | ~$4.10 |
| Sonnet (`MODEL_ANALYTICAL`) | ~15 | 2K | 500 | $0.003 | $0.015 | ~$0.20 |
| Default (Opus) | ~420 | 1.5K | 200 | $0.015 | $0.075 | ~$15.70 |
| **Total per run** | | | | | | **~$21** |

*Prompt caching reduces system prompt costs ~50% on repeated calls within an hour.*

---

## Prompt Dependency Graph

Which prompts feed into which:

```
Articles (raw)
  │
  ├── P2b/P2c (translate) ──┐
  │                          │
  ├── P3b/P3d (transcripts) ─┤
  │                          │
  ▼                          ▼
Articles (English)
  │
  ├── P4b (classify) ── P4c (extract events) ── P4e (dedup articles)
  │
  ▼
Clustered events (HDBSCAN)
  │
  ├── P5b (dedup clusters + detect arcs)
  │
  ▼
Merged event clusters
  │
  ├── P6b (synthesize each → Story)
  │     │
  │     ├── P6c (classify story)
  │     └── P6d (translate if non-EN)
  │
  ▼
Stories per leader
  │
  ├── P6e (BTL + exec summary per leader) ── LeaderDossier
  │
  ▼
All LeaderDossiers
  │
  ├── P7b (validate + synthesize cross-leader stories)
  ├── P7c (global BTL + exec summary) ── WeeklyBrief
  │
  ▼
WeeklyBrief
  │
  ├── save_brief() ── .mdx pages + JSON artifacts
  ├── P8b (email digest) ── email.html
  ├── upload to S3
  └── push to docs repo (docs.json update, no LLM)
```

---

## Deprecated Prompts (not in active flow)

These remain in the codebase as fallbacks but are not called in the main pipeline:

| ID | Was | Replaced by | File |
|----|-----|-------------|------|
| D1 | Standalone cluster dedup | P5b (combined dedup+arcs) | `clustering/dedup.py` |
| D2 | Standalone arc detection | P5b (combined dedup+arcs) | `clustering/story_grouper.py` |
| D3 | Cross-leader validation | P7b (validate+synthesize) | `clustering/story_grouper.py` |
| D4 | Standalone shared story synthesis | P7b (validate+synthesize) | `aggregate_builder.py` |
| D5 | Standalone thematic BTL | P7c (merged BTL+summary) | `aggregate_builder.py` |
| D6 | Standalone exec summary | P7c (merged BTL+summary) | `aggregate_builder.py` |
| D7 | Thread detector (full agent) | P7b+P7c (aggregate_builder) | `agents/thread_detector.py` |

See [prompt_inventory.md](prompt_inventory.md) sections D1–D4 for full deprecated prompt text.

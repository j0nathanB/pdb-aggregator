# V3 Analytical Pipeline — Implementation Summary

## What changed

The synthesis layer of the Middle Powers Monitor pipeline was replaced. Everything from `build_dossier` onward is now a multi-phase analytical architecture. Upstream stages (source fetching, translation, event clustering) are unchanged.

The old pipeline produced per-leader dossiers via a single LLM call, then aggregated them into a brief. The new pipeline separates data logging from analysis, adds persistent per-leader context, and introduces significance-based filtering before publication rendering.

## Architecture

```
Event Clustering (unchanged)
        │
        ▼
Cross-Correlation Pass ──────────────────────┐
  thematic clusters + Phase 0 trigger        │
        │                                    │
        ▼ (conditional)                      │
Phase 0: Global Context Brief                │
        │                                    │
        ▼                                    │
Phase 1 Call A (per leader)                  │
  structured running picture entry           │
        │                                    │
        ▼                                    │
Phase 1 Call B (per leader)                  │
  analytical assessment                      │
        │                                    │
        ▼                                    │
Pre-Filter (pure Python)                     │
  T1/T2/T3 tier assignment                   │
        │                                    │
        ▼                                    ▼
Phase 2 Renderer ◄──── thematic clusters brief
  publication output
        │
        ▼
Consolidation Check (every 4 weeks)
```

## New modules

### `src/running_picture/` — persistent per-leader context

One markdown file per weekly entry per leader, stored in `running_picture/weekly/{leader_slug}/YYYY-MM-DD.md`.

- **`schema.py`** — `RunningPictureEntry` and `ConsolidationSummary` dataclasses, frontmatter/section parsing, `leader_slug()` helper.
- **`storage.py`** — File I/O for weekly entries, consolidation summaries, dormant threads, and archival. Directory structure: `weekly/`, `consolidation/`, `dormant_threads/`, `archive/`.
- **`validation.py`** — Schema validation with `ValidationResult` (errors/warnings/correction prompt). Checks: required sections, frontmatter fields, Key Actions source attribution, Commitments Audience/Binding Force, ACTIVE/DORMANT thread structure, Missing Thread Audit count, claim namespace format `[STRUC-XX]`/`[PROF-XX]`.
- **`extraction.py`** — Python-only extraction (no LLM) of thread checklists and commitment ledgers from prior entries. These are injected into Call A's user prompt as hard-coded context.

### `src/context/` — baseline document processing

- **`claims.py`** — Extracts numbered claims from country dossiers (`[STRUC-XX]`) and leader profiles (`[PROF-XX]`). Handles both plain and bold markdown claim headers. Produces a Claims Index for system prompt injection.
- **`assembly.py`** — Builds the cached system prompt (dossier + profile + claims index, identical for Call A and Call B) and role-specific user prompts for both calls.

### `src/phases/` — pipeline stages

- **`cross_correlation.py`** — Single LLM call that identifies thematic clusters across 2+ leaders and recommends whether Phase 0 should trigger. Parses output for trigger decision and cluster text.
- **`phase0.py`** — Conditional global context brief (500-800 words) injected into all Phase 1 calls when triggered.
- **`prefilter.py`** — Pure Python tier assignment. No LLM. Parses Call B outputs for attention flags, deviation classifications, cross-leader mentions, and active thread counts. Assigns Tier 1 (full), Tier 2 (condensed), or Tier 3 (stub). Randomizes within tiers for position bias alignment.
- **`renderer.py`** — Phase 2 publication renderer. Single editorial LLM call (Opus) that takes tiered inputs + thematic clusters + key evidence and produces the Middle Powers Monitor brief.
- **`consolidation.py`** — Every-4-weeks task that compresses 4 weekly entries into a period summary per leader. Manages thread lifecycle, analytical inertia checks, and structural claim refresh recommendations.

### `src/agents/analyst.py` — refactored for v3

- System prompt = cached dossier + profile + claims index (same for Call A and B, maximizes prompt cache hits).
- User prompt = role instructions + running context + events + thread checklist (Call A) or Call A output (Call B).
- Auto-retry once on validation failure with correction prompt. Accepts with warning if retry also fails.
- Call A saves entries via `save_weekly_entry()` (one file per week per leader).
- Call B produces analytical assessment with structured sections (Activity Summary, Event Analysis, Cross-Leader Relevance, Between the Lines, Attention Flags, Key Evidence for Phase 2).

### `src/graph.py` — orchestrator

New `AnalyticalPipeline` class wires all stages together. Legacy `PDBWorkflow` preserved for backwards compatibility.

`AnalyticalPipeline.run()` accepts a `baseline_dir` parameter and loads `{slug}_country.md` and `{slug}_profile.md` from it.

## Key design decisions

**Prompt caching.** The system prompt (dossier + profile + claims index) is identical for Call A and Call B per leader. Role-specific instructions go in the user prompt. This means 2 calls per leader share the same ~15k-token cached prefix.

**Thread checklist injection.** The thread checklist is extracted by Python (not LLM) from the prior entry and injected as a numbered list into the Call A user prompt. The LLM must account for every thread in its Missing Thread Audit. This prevents thread drift.

**Claims namespacing.** All baseline claims use `[STRUC-XX]` or `[PROF-XX]` format. Validation rejects bare-number references and warns on references not found in baseline documents.

**Pre-filter is pure Python.** No LLM call. Parses structured sections from Call B output using regex. This keeps the pipeline deterministic at the tier assignment stage.

**Auto-retry strategy.** On validation failure, retry once with the correction prompt appended. Never more than once. Accept with warning flag if retry fails. This avoids infinite loops while catching most LLM formatting errors.

## Deleted

- `src/running_picture.py` — Old single-module v1 implementation (single file per leader, entries separated by `---`, 10-entry window). Conflicted with the new `src/running_picture/` package.

## Tests

202 tests across 8 test files, all passing.

| Test file | Count | What it covers |
|-----------|-------|----------------|
| `test_running_picture.py` | 42 | Schema parsing, storage CRUD, validation, thread/commitment extraction |
| `test_claims.py` | 17 | Claims extraction against Mexico sample dossier and Sheinbaum profile |
| `test_assembly.py` | 20 | System/user prompt construction, event formatting |
| `test_cross_correlation.py` | 14 | Event formatting, output parsing, empty input handling |
| `test_phase0.py` | 12 | Prompt content, user prompt formatting, function signature |
| `test_prefilter.py` | 44 | All extraction helpers, tier assignment rules, ordering, edge cases |
| `test_renderer.py` | 30 | Key evidence extraction, prompt assembly, metadata parsing |
| `test_consolidation.py` | 16 | Needs-consolidation logic, prompt assembly, dormant thread extraction |

## Spec reference

The implementation follows `docs/runtime_pipeline_prompts_v3.md` (primary spec) and `docs/phase2_renderer_revised.md` (Phase 2 details).

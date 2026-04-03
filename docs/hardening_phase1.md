# Phase 1: Stop the Bleeding — Architectural Hardening

> **Status**: COMPLETED
> **Completed**: 2026-04-02
> **Branch**: mintlify
> **Tests**: 651 passed (40 new + 611 existing), 0 failures

## Context

Staff-level code review of the mintlify branch identified fragile patterns that would cause the next production failure to cascade: unprotected enum parses, duplicate ledger entries on re-runs, string-literal enum comparisons, and duplicated JSON extraction logic across all agent parsers.

All claims were validated against the codebase before implementation.

---

## What Was Done

### 1.1 — Shared LLM Output Sanitization (`src/monitor/sanitize.py`)

**New file** with 5 utilities + 1 diagnostics class:

| Function | Purpose |
|----------|---------|
| `safe_enum(enum_class, value, default, context)` | Parse enum, return default on invalid |
| `safe_enum_list(enum_class, values, context)` | Parse list of enums, skip invalid |
| `safe_date(value, fallback, context)` | Parse ISO date string, return fallback on invalid |
| `safe_int(value, default, min_val, max_val, context)` | Bounded int parse |
| `extract_json(text, context)` | Unified JSON extraction using `raw_decode()` — replaces 8 duplicated patterns |
| `ParseDiagnostics` | Accumulates fallbacks/skips per parse, escalates if threshold exceeded |

**9 files migrated** to use sanitize utilities:

| File | Changes |
|------|---------|
| `agents/executive.py` | 3 unprotected `DynamicStatus`/`SignalCategory` parses fixed, duplicate `_safe_categories` deleted, JSON extraction + ad-hoc date parsing replaced, `GlobalWeeklyEntry` dedup added |
| `agents/country.py` | 4 try/except enum blocks replaced with `safe_enum`, brace-counting JSON extraction replaced, 3 string-literal `ClaimStatus` comparisons fixed, posture summary enum parses protected |
| `agents/regional.py` | JSON extraction replaced |
| `agents/devils_advocate.py` | JSON extraction replaced |
| `agents/story_map.py` | JSON extraction replaced (json_repair fallback preserved) |
| `agents/triage.py` | JSON extraction replaced, unprotected `Depth()` replaced with `safe_enum` (falls back to MAINTENANCE) |
| `agents/government.py` | Regex-based JSON extraction replaced |
| `ledger/initialize.py` | JSON extraction replaced |
| `orchestrator.py` | See 1.2–1.4 below |

**Removed dead imports**: `json` and `re` removed from 6 files where they were only used for JSON extraction.

### 1.2 — Deduplicate Weekly Entries on Ledger Write

`orchestrator.py:apply_to_ledger()` — blind `.append()` replaced with upsert (check if entry for same week exists, replace if so).

Same treatment applied to `executive.py:_build_and_append_weekly_entry()` for `GlobalWeeklyEntry`.

### 1.3 — Fix String-Literal Enum Comparisons

`orchestrator.py` — `check.status in ("under_pressure", "weakened")` replaced with `ClaimStatus.UNDER_PRESSURE`, `ClaimStatus.WEAKENED`, `ClaimStatus.CONFIRMED`.

`country.py` — 3 additional string-literal `ClaimStatus` comparisons fixed in structural claims filtering (lines 162, 167, 168).

Note: These comparisons worked by accident because `ClaimStatus(str, Enum)` inherits `__eq__` from `str`. Fix is for type safety and clarity.

### 1.4 — Explicit `consecutive_maintenance_weeks` Reset

`orchestrator.py` deep-dive path — after posture summary assignment, unconditionally reset `consecutive_maintenance_weeks = 0` and set `last_deep_dive` to the current week. No longer depends on LLM output for this counter.

---

## Test Changes

**New**: `tests/monitor/test_sanitize.py` — 40 tests covering all sanitize utilities.

**Updated** (7 files): `json.JSONDecodeError` assertions widened to `(json.JSONDecodeError, ValueError)` since `extract_json` raises `ValueError` instead of `JSONDecodeError` for non-JSON input.

**Updated**: `test_triage.py:test_invalid_depth_raises` renamed to `test_invalid_depth_falls_back_to_maintenance` — invalid depth now gracefully degrades instead of crashing.

---

## Remaining Work (Future Phases)

### Phase 2: Resumable Pipeline — COMPLETED (2026-04-02)

**Run manifest** — `RunRecorder` now tracks stage status (pending/running/completed/failed/skipped) in `manifest.json` with atomic writes. `find_latest_manifest()` finds the most recent run for resume.

**Ledger snapshots** — `snapshot_ledgers()` copies all country ledgers, global ledger, and regional reports to `{run_dir}/snapshots/` before any mutations.

**`--resume-from`** — New CLI flag: `--resume-from={regional,executive,newsletter,publishing}`. Skips prior stages, loads state from disk via shared `_load_pipeline_state()`. Each stage in `cmd_run` wrapped with manifest tracking + try/except.

**Also**: `cmd_assemble` and `cmd_publish` simplified to use `_load_pipeline_state()`, reducing duplication.

671 tests passing (20 new).

### Phase 2b: Deployment Rewire — COMPLETED (2026-04-02)

**`run_pipeline.py` rewrite** — Full rewrite as subprocess-based entrypoint. Runs `python -m src.monitor.cli run --date`, auto-commits `ledgers/` + `site/briefs/`, pushes to main if `GITHUB_TOKEN` set. Auto-detects next date from last brief. Local mode (in-repo) and Fargate mode (clone-and-run) supported. S3 upload and preview email stubbed for later.

**Dockerfile simplified** — Runtime env only (Python + deps + ML models). Removed: `COPY src/`, dead CSV files, `gh` CLI install. Only entrypoint script is baked in; everything else comes from clone at runtime.

**Dead code removed** — Deleted `scripts/migrate_to_mintlify.py` (imported nonexistent `src.persistence`).

### Phase 3: Observability
- Cost tracking per run
- ParseDiagnostics aggregation in pipeline summary
- Prompt change detection (hash comparison)

### Phase 4: Structural Improvements
- Consolidation integrity (structured metadata companion)
- Global rate limiting for API calls
- Typed `AgentResult[T]` with degradation metadata

### Phase 5: Cleanup
- Remove dead files (`opinion_filters.csv`, `leaders_sources.csv`)
- Pin `end_date` at pipeline entry (audit `date.today()` fallbacks)
- Deprecate `cmd_assemble`/`cmd_publish` once `--resume-from` ships

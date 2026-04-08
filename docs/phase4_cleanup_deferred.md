# Phase 4 cleanup (steps 9-10): delete the old regex pipeline

**Status:** Scoped, deferred. New pipeline has been running cleanly for several weeks but old code remains on disk as a fallback. Pick up when ready.

## What's still on disk

| Module | Lines | What it does | Replaced by |
|--------|-------|--------------|-------------|
| `src/monitor/newsletter/assembly.py` | 805 | Old markdown rendering: `assemble_newsletter`, `assemble_newsletter_pages`, plus 18 `_render_*` / `_collect_*` helpers | `content_builder.py` + `renderer.py` + Jinja2 templates |
| `src/monitor/agents/editor.py` | 919 | Old markdown editor: `style_edit_page`, `_strip_sources_accordion`, `_sanitize_mdx`, etc. | `structured_editor.py` |
| `src/monitor/agents/copyeditor.py` | 383 | Old markdown copyeditor: `_build_copyeditor_prompt`, `_is_boilerplate`, `_split_newsletter_sections`, `copyedit_newsletter` | `structured_copyeditor.py` |
| **Total dead code** | **2,107 lines** | | |

## Dependencies that block deletion

### 1. New code still imports constants from `assembly.py`

| File | Imports |
|------|---------|
| `newsletter/content_builder.py:20` | `REGION_DISPLAY_NAMES`, `REGION_ICONS`, `REGION_ORDER`, `REGION_SLUGS`, `SIGNAL_CATEGORY_DISPLAY` |
| `newsletter/renderer.py:16` | `REGION_SLUGS`, `REGION_ORDER` |
| `scripts/reedit.py:58` | `REGION_SLUGS`, `REGION_DISPLAY_NAMES` |

**Fix**: extract these into a new `newsletter/constants.py` (~40 lines), update the 3 imports.

### 2. CLI still has dead code paths

| Location | Issue |
|----------|-------|
| `cli.py:155` | `cmd_run` imports `assemble_newsletter*` but never calls them — dead import |
| `cli.py:425` | `cmd_assemble` exists and uses `assemble_newsletter` |
| `cli.py:448` | `cmd_publish` exists and uses `assemble_newsletter_pages` |
| `cli.py:684–686` | argparse subcommand wiring for both |

**Fix**: delete `cmd_assemble` entirely (the new `cmd_run` does everything it did + more). Rewrite `cmd_publish` to use `content_builder` + `renderer` (it's the "publish from existing ledger data without LLM calls" path, which is genuinely useful for re-publishing without re-running LLMs).

### 3. Tests reference old code

| Test file | Lines | What it tests |
|-----------|-------|---------------|
| `tests/monitor/test_newsletter.py` | 655 | 10 test classes for `_render_*`, `assemble_newsletter`, etc. |
| `tests/monitor/test_copyeditor.py` | 157 | `_build_copyeditor_prompt`, `_is_boilerplate`, `_split_newsletter_sections` |
| `tests/monitor/test_e2e_mexico.py:670–684` | ~15 lines | One test calls `assemble_newsletter` to verify e2e output |

**Fix**:
- `test_newsletter.py` — delete entirely. The new pipeline is template-based; existing tests test private helpers that no longer exist in the same form. Structural correctness is already validated by published briefs.
- `test_copyeditor.py` — delete entirely. Tests private helpers of the old copyeditor.
- `test_e2e_mexico.py` — drop the one assertion that uses `assemble_newsletter`. Keep the rest (desk pipeline + Layer 2 integration tests).

### 4. One-off recovery script

`scripts/resume_style_edit.py` — One-off written for the 2026-02-15 brief recovery. No longer needed; `reedit.py` handles this generically now. Delete.

## Plan of execution

Sequenced so the codebase compiles between each step:

1. **Create `newsletter/constants.py`** with `REGION_DISPLAY_NAMES`, `REGION_ICONS`, `REGION_ORDER`, `REGION_SLUGS`, `SIGNAL_CATEGORY_DISPLAY`. Re-export from `assembly.py` so nothing breaks immediately.
2. **Update 3 importers** (`content_builder.py`, `renderer.py`, `scripts/reedit.py`) to import from `constants.py` instead of `assembly.py`.
3. **Rewrite `cmd_publish`** to use `content_builder.build_all_pages` + `renderer.render_pages` (skipping the LLM editorial stages — that's the "publish without re-running editors" flow).
4. **Delete `cmd_assemble`** from `cli.py`, including its argparse subcommand.
5. **Delete the dead import** at `cli.py:155`.
6. **Delete `tests/monitor/test_newsletter.py`** entirely.
7. **Delete `tests/monitor/test_copyeditor.py`** entirely.
8. **Trim `test_e2e_mexico.py`** — remove the `assemble_newsletter` assertion (lines ~670-684), keep the rest.
9. **Delete `scripts/resume_style_edit.py`**.
10. **Delete `src/monitor/newsletter/assembly.py`** (805 lines).
11. **Delete `src/monitor/agents/editor.py`** (919 lines).
12. **Delete `src/monitor/agents/copyeditor.py`** (383 lines).
13. **Run full test suite** to confirm nothing slipped through.
14. **Update `docs/hardening_phase1.md`** to mark steps 9-10 done.

## Risks

| Risk | Mitigation |
|------|-----------|
| `cmd_publish` is genuinely used and the rewrite breaks it | Test by running `python -m src.monitor.cli publish --date {latest}` and verify it produces the same MDX as the existing brief |
| Test deletion removes useful coverage | The deleted tests cover **private helpers** of the old code path. The new pipeline is exercised by the e2e mexico test (after trimming) and by every real pipeline run. |
| Some unknown caller still imports `assembly` | Step 1-2 keeps `assembly` working; deletion is at step 10. If anything else still imports it, the test suite at step 13 will fail with `ImportError` before deletion lands. |
| `cmd_assemble` is used by CI/scripts not discovered in the scoping | Worth a `grep -rn cmd_assemble` final check before deletion. |
| Overlap with `_render_notes_section` | Already moved to `renderer.py:55`. Old `_render_sources_section` in `assembly.py:260` is obsolete. |

## Net result

| Metric | Before | After | Delta |
|--------|--------|-------|-------|
| Source LOC | ~2,107 dead lines | ~40 lines (constants.py) | **−2,067** |
| Test LOC | 812 lines testing old code | ~30 lines kept from test_e2e_mexico | **−782** |
| CLI commands | 7 (`init`, `run`, `triage`, `assemble`, `publish`, `replay`, `status`) | 6 (drop `assemble`, keep rewritten `publish`) | **−1** |
| Files deleted | 0 | 6 (assembly.py, editor.py, copyeditor.py, test_newsletter.py, test_copyeditor.py, resume_style_edit.py) | **−6 files** |

## Effort estimate

- Constants extraction + import updates: 20 min
- `cmd_publish` rewrite + verification: 30 min
- `cmd_assemble` deletion: 5 min
- Test deletions + trim: 15 min
- File deletions + final test run: 10 min
- Doc update: 5 min

**Total: ~1.5 hours**, mostly mechanical. Risk surface is small because the new pipeline has been running cleanly for weeks.

## Decisions still open

1. **Keep or delete `cmd_publish`?** It's the "republish without re-running LLMs" flow. Useful when manually editing ledgers and wanting to regenerate the MDX. Recommendation: keep but rewrite. Alternative: delete and rely on `reedit.py` for ad-hoc recovery.
2. **Delete `test_newsletter.py` or rewrite?** The deleted tests have no equivalent in the new code. Rewriting would mean writing template/renderer tests from scratch (~1-2 hours additional). Recommendation: delete and trust e2e validation.
3. **Aggressive or safe?** The plan above is the safe sequenced approach. The aggressive version skips constant-extraction and just inlines: copy the constants into content_builder.py, delete assembly.py in one shot. Saves ~10 min, slightly higher risk.

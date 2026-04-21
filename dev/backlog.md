# Backlog

Running list of known work items that are deferred but shouldn't get lost.
Append new items as they surface. Each item has a scope estimate + enough
context that a future person can pick it up cold.

---

## Wasted LLM calls on unrendered watchlist content

**Status**: noted 2026-04-20. Not urgent.

**Problem**: commit 015a040 (2026-04-13) removed watchlist-page rendering
but left the editor/copyeditor/style-editor pipeline wired to still
process watchlist content on every run. Each run makes 3 LLM calls on
content that is never published.

**Evidence**:
- `content_builder.build_all_pages` still builds a
  `WatchlistPageContent` from `global_ledger.watchlist` and returns it.
- `structured_editor.edit_all(scope="countries")` still calls
  `edit_watchlist(watchlist, ...)` when `watchlist.items` is non-empty.
- `structured_copyeditor.copyedit_all` still calls
  `copyedit_watchlist(...)`.
- `structured_editor.style_edit_all` still has a watchlist branch.
- `cli.py`'s newsletter stage threads `watchlist_content` through all
  three editors.
- `renderer.render_pages` accepts `watchlist` as a parameter but never
  produces `pages["watchlist"]` — the LLM work is pure waste.
- Output lives in the structured `WatchlistPageContent` in memory,
  then gets garbage-collected.

**Impact**: 3 LLM calls per run × ~10-item watchlist = real tokens burned
every Sunday. Low per-run cost but unambiguous waste.

**Scope**: ~100 lines of deletion across:
- `src/monitor/newsletter/content_builder.py` (drop the watchlist
  construction, return tuple without it)
- `src/monitor/newsletter/content_models.py`
  (delete `WatchlistPageContent`, `WatchlistItemContent`; drop
  `watchlist_card_summary` and `watchlist_count` from `OverviewPageContent`)
- `src/monitor/newsletter/structured_editor.py` (delete
  `edit_watchlist` + its call sites in `edit_all` / `style_edit_all`,
  remove `watchlist` parameter)
- `src/monitor/newsletter/structured_copyeditor.py` (delete
  `copyedit_watchlist` + call site in `copyedit_all`, remove parameter)
- `src/monitor/newsletter/renderer.py` (remove the now-dead
  `watchlist` parameter and import)
- `src/monitor/cli.py` (update the newsletter stage's
  `edit_all/copyedit_all/style_edit_all/render_pages` calls)
- Also: `recover` subcommand path in cli.py has the same signatures.

**Tests affected**: search for `test_watchlist` or `_test_watchlist()`
fixture usage. Update signatures.

**Why not done yet**: scope was larger than the ancillary-cleanup
commit (eaa2c38) warranted, and the user was mid-spot-check of a
brief. Land as a standalone commit when the current brief has been
reviewed and any other work has stabilized.

**Watchlist state in the ledger is NOT being deleted** by this work —
`global_ledger.watchlist` stays as an analytical tracking field; only
the rendering path is removed.

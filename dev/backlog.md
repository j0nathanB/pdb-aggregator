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

---

## Web_search fallback — surface source URLs in brief output

**Status**: noted 2026-04-20. Not urgent for 2026-04-19 (user accepted
the gap for this run) but needed before regular use.

**Problem**: when story_map fails (e.g., truncation at max_tokens,
server-side streaming drops), the country agent falls back to
Anthropic's `web_search_20250305` tool and does its own research. The
content that lands in the brief doesn't distinguish itself from the
normal-pipeline path — there's no "sources: [...]" list, no Notes
block, nothing indicating that the URLs read weren't from the normal
Brave+extraction audit trail.

Observed on the 2026-04-19 run: JP went through the web_search fallback
after two story_map failures. The resulting country content in
`site/briefs/2026-04-19/asia-pacific.mdx` reads like any other
country's content — but the reader has no way to know the sources
Claude consulted or evaluate their credibility.

**What we already have**: the country agent code at
`src/monitor/agents/country.py` already captures each web_search call's
`query + results_count + results[]` into `search_log: list[dict]` and
persists it into the trace via `extra={"search_log": search_log}`. So
the data is saved — it just doesn't propagate to the ledger or the
rendered page.

**Policy question** (decide before implementing): should the Notes/
Sources section appear:
- Only when web_search was used (fallback signal)?
- Always for every country (parity + transparency)?
- Only when *most* developments came from web_search rather than
  pre-built content?

The user's framing suggests option 1: "if we exclusively use web
search" → attach a Notes/sources footer.

**Scope sketch** (~50-100 lines):
- `CountryAgentOutput`: add a `search_log: list[dict] | None = None`
  field.
- `country.py run_country_agent`: populate it from the web_search
  branch (leave None for story_map-driven runs).
- `models.CountryLedger.weekly_entries[i]`: add an optional
  `research_sources: list[SourceAttribution] | None` field populated
  from search_log so the ledger has an audit trail.
- `content_builder.build_all_pages`: when populating `CountryContent`
  for the region page, copy the sources across.
- `content_models.CountryContent`: add `research_sources` field.
- `templates/region.mdx.j2`: if `country.research_sources`, emit a
  "Sources" block (distinct from the normal per-development citations).
- `structured_editor.edit_country` / copyeditor / style_editor: pass
  the sources through unchanged (they're a factual block, not prose to
  edit).

**Tests**: a fixture with a `search_log` populated, asserting the
rendered region page includes the sources block; and parallel assertion
that a story_map-path country has no sources block.

**Why this matters operationally**: right now we have *zero* visible
signal when a country went through the fallback. Even for auditing
purposes, there's no in-brief marker. Adding this makes the fallback
path transparent to readers and preserves our provenance story.

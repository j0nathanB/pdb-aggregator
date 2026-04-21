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

**Related gap** (fold into same PR): the at-a-glance page
(`at-a-glance.mdx`) pulls top-story headlines from `story_map` data.
When story_map fails and the country falls back to web_search, the
at-a-glance card for that country is simply absent — the country
appears in the region page but is missing from the regional
at-a-glance section. JP on the 2026-04-19 brief demonstrates this
(fixed manually in commit 10778a2 as a one-off). The fix belongs
here: when story_map isn't available, derive the at-a-glance card
from the country agent's own top-development headline (or the
web_search results' summary) rather than skipping the country
entirely.

---

## Migrate remaining LLM stages to tool_use

**Status**: noted 2026-04-20. Continues the pattern established for
country agent (`fa2ec4b`) and story_map (`bce0bdd`).

**Motivation**: the 2026-04-19 run fired `json_repair_used` 45 times:
  - 28 × `[story_map]` (tool_use max_tokens truncation → free-form fallback)
  - 17 × `[editor_XX]` (one per country — unescaped quotes in prose JSON)

Romania's brief was sharply truncated (main narrative ~2 short paras
ending mid-sentence) because the editor emitted `"Momentul
Adevărului"` inside the JSON's `narrative_body` value without
escaping the quotes. The JSON parser terminated the string at char
393; json_repair recovered 791 chars total (ending with a dangling
comma) plus a few phantom keys like `"puppet premier."` and `"only"`
— which were actually chunks of prose that got mis-parsed as JSON
keys. The LLM wrote far more narrative than 791 chars; most was lost.

Every country's editor has this risk. Romania was just where the
unescaped quote landed earliest. The same failure mode applies to
every free-form JSON stage that emits prose.

**Stages still on free-form JSON** (all call `extract_json` with
`json_repair` fallback in `sanitize.py`):

Prose-heavy (highest leverage — internal quotes common):
- `newsletter/structured_editor.py` — `edit_country`, `edit_regional`,
  `edit_executive`, `edit_watchlist` (the 17 editor_XX failures above)
- `newsletter/structured_copyeditor.py` — per-country + regional + executive
- `newsletter/structured_editor.py:style_edit_prose` — style pass
- `newsletter/regional_writer.py` — writes regional essays
- `newsletter/global_writer.py` — writes global executive essay

Structured analytical output (medium leverage):
- `agents/regional.py` — regional synthesis (6 calls/week)
- `agents/executive.py` — executive synthesis (1 call/week, large)
- `agents/devils_advocate.py` — 30 calls/week (one per country)
- `agents/government.py` — 30 calls/week (one per country)

Lower priority (small output, less drift risk):
- `agents/triage.py` — depth decisions (1 call/week, short rationales)
- `ledger/initialize.py` — new-country dossier seed (rare)

**Suggested migration order** (by leverage × risk):

1. **Editor + copyeditor + style_editor** (combined PR). Same content
   models (`CountryContent`, `RegionPageContent`, `ExecutiveBriefContent`).
   A single shared tool schema (or a small family) serves all three.
   Eliminates the 17× editor failures per run. ~200-300 lines.

2. **Regional writer + global writer**. Both produce long prose
   essays (the most quote-heavy prose in the pipeline). High shape-
   drift risk, low test coverage today. ~80-120 lines.

3. **Regional + executive synthesis**. Structured JSON output, but
   `executive` already shows 1 `[executive]` json_repair hit per run.
   Used downstream by the prose-writing stages — worth locking down.
   ~100-150 lines.

4. **Devil's advocate + government agent**. Per-country calls, so
   error rates compound. Output structure is simpler than country
   agent's so migration is lighter. ~80 lines each.

5. **Triage + initialize** (last). Small output, low failure
   frequency, no urgency.

**Cleanup debt unlocked by migration**: once each stage is on
tool_use, most of the defensive patches we've layered on can be
deleted. `parse_country_response`'s resilience patches from today
(ledger carry-forward for missing categories in `3170f48`, enum
coercion in `bca63ae`, `safe_enum`/`safe_int` scaffolding in
`36f7c12`) become dead code when the schema prevents the shape drift
at the API boundary. Same applies to stage-by-stage as they migrate.

**Tooling already in place**: `src/monitor/schema_helpers.py`'s
`pydantic_to_tool_schema` handles schema generation from Pydantic v2
models. `MPM_USE_TOOL_SCHEMA` env var gate is the A/B mechanism.
Story_map's text-fallback path (commit `b0404af`) is a template for
handling the case where tool_use fails mid-stream.

**One wrinkle per stage to watch**: the country agent uses
`web_search_20250305` alongside its record tool, and that combination
works. Other stages are simpler — single tool, no web_search. Should
be less wrinkle to port.

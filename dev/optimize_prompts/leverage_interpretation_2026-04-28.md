# Leverage Interpretation 2026-04-28

Reading of `leverage_split_2026-04-28.md`. Three-way token split confirms the
hypothesis: the editor cluster is the biggest win by far, country and story_map
need template restructures to be cacheable, and the existing country.py cache
is not just decorative — **it's actively losing tokens**.

## The leverage ranking flipped

Raw input volume vs actual cacheable leverage:

| agent | rank by raw volume | rank by leverage |
|---|---:|---:|
| story_map | 1 | bottom (n=1 per cluster) |
| country | 2 | bottom (n=1 per cluster) |
| editor | 3 | **3** (368K/run) |
| copyeditor | 4 | **1** (393K/run) |
| style_editor | 5 | **2** (372K/run) |

The editor trio together: **~1.13M tokens saved per pipeline run**.

Why story_map and country drop to the bottom: each call lands in its own cluster
because `{{COUNTRY}}` interpolates into the first ~200 chars of the system
prompt. With n=1 per cluster, `(n-1) × prefix = 0`. Confirmed structurally
what we saw in the CV analysis — these agents need template restructure to be
cacheable across calls within a single run.

## The editor cluster is even bigger than these numbers suggest

The script clusters by first-200-char of system_prompt. That puts editor's 4
sub-templates (country/regional/executive/style) into 4 separate clusters
(rows #0-#3 in editor table). Each row independently caches its own system.

But the **shared 30KB style guide is in all 4 templates** — just at the end,
not the beginning. If we flip `_build_system_prompt` order to put style guide
FIRST, all 4 editor sub-types collapse to a single shared cluster. Same for
copyeditor and style_editor.

Combined: country editor (30) + regional editor (6) + executive editor (1) +
style editor (37) + copyeditor (38) + a few more = **~110+ calls per week**
all sharing one ~10-12K token cache prefix.

That's an additional ~1M tokens/run on top of the 1.13M within-cluster savings.
**Total estimated leverage: ~2M tokens saved per pipeline run, ~4M per
two-week window.**

For context: total input across all editor agents over 2 weeks is 3.45M
(per baseline analysis). Savings of 4M is impossible against a 3.45M base —
the actual savings is bounded by `total_input × 0.9` (since cache reads are
~10% of full price). True savings is closer to **2-3M tokens per 2 weeks**
on the editor cluster alone, ~60-80% input-token reduction. Still huge.

## Country.py existing cache_control is actively losing tokens

The script confirms each country call is its own cluster (line 47-76 in the
data file: 30 country clusters, n=1 each). Cache reads = 0. But cache writes
happen because `cache_control` is set — and writes cost **1.25× the normal
input price**.

Net effect: every weekly run pays an extra 25% on the system prompt portion
(~3.9K tokens/call × 30 calls × 0.25 premium = ~29K tokens wasted/run, ~58K
per 2 weeks).

That's small compared to the editor savings opportunity, but it's a strict
loss with no upside. Phase 2 should either:
- Restructure the country template to enable cross-country reuse (medium
  effort, modest win — ~3.9K × 29 calls × 0.9 = ~100K saved/run)
- Remove the `cache_control` (zero effort, stops the bleeding)

The user's loose-end note was right: third option (leave as-is) is worst.

## Story_map shape mirrors country

Same per-call clustering pattern. Adding `cache_control` today without a
template restructure would have the same decorative-and-costly effect.
Don't add it to story_map until/unless the template gets the country-tail
treatment. The 6.4M raw input volume is mostly user-message search results,
which are inherently per-country.

## Updated Phase 3 ordering

Original plan: editor cluster shared-prefix flip first. **Confirmed correct,
even more strongly than I thought.**

Revised priority:

1. **Phase 3a — Editor cluster shared prefix flip** (highest leverage,
   structurally clean). Flip `_build_system_prompt` order in
   `newsletter/structured_editor.py:226`. Add `cache_control` after the
   shared block in all 5 editor sites. Single small PR, ~2M+ tokens/run.
   Includes the A/B noise-floor check (run new prompt twice, compare to
   itself first).

2. **Phase 3b — Stop the country.py bleeding** (zero-effort win).
   Either remove the existing `cache_control` from `country.py:967-971`
   pending template restructure, OR ship the template restructure now.
   Phase 2 trace data from Sunday will confirm zero cache reads, then act.

3. **Phase 4 — Per-agent rollout for the rest** (smaller wins).
   government, devils_advocate, regional, ledger/consolidation, executive.
   Each: wrap system in cache_control. **Only do this for agents where
   the system prompt is structurally shared across calls** — devils_advocate
   has per-country system prompts (same {{COUNTRY}} pattern), so it'd
   need restructure too. Government has shared system across all 30
   calls (cluster #0-29 all share 2451-2454 token system LCP) — that's
   a clean win.

4. **Phase 4.5 (deferred) — Template restructures for country + story_map**.
   Largest absolute savings but also largest engineering effort. Defer
   until editor cluster results validate the approach end-to-end.

## What still needs Sunday's run

- Confirm editor cluster system_prompt assembly produces byte-identical
  prefixes across all 5 editor sites after the order flip (cache hit % >
  0.5 on calls 2+ per agent).
- Confirm country.py cache hit rate is actually zero today (validates the
  "decorative" finding).
- Establish baseline cache hit % for the per-agent alerting threshold.

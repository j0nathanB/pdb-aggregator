# Leverage Interpretation 2026-04-29 (corrected)

Supersedes `leverage_interpretation_2026-04-28.md`. Two corrections after the
script labeling fix and LCS verification:

1. The headline win comes from `cache_control` alone, NOT the order flip.
2. The "additional ~1M tokens from cross-cluster sharing" claim was wrong —
   the flip's marginal value is near zero against per-cluster caching.

Country.py framing also updated to "signal hygiene" per pushback.

## Verified numbers (units: tokens per single Sunday pipeline run)

`n` in the leverage table is **per-week** (verified: copyeditor week 20260419
had 39 calls, week 20260426 had 38 calls; script's `top.n=38` matches one
week, not the sum). The script previously had a `savings_tokens_2wk_estimate`
field that wasn't displayed but was the source of confusion. Removed.

| agent (top cluster) | stable prefix | per-run calls | savings per run |
|---|---:|---:|---:|
| copyeditor #0 | 10,622 | 38 | **393,014** |
| style_editor #0 | 10,325 | 37 | **371,700** |
| editor #0 (country editor) | 12,695 | 30 | **368,155** |
| editor #1 (regional editor) | 10,817 | 6 | 54,085 |

Editor cluster total per run: **~1.19M tokens** (within-cluster reuse only,
no order flip). Per 2 weeks: **~2.4M tokens**. That's ~70% of the editor
cluster's 3.45M-token 2-week input budget.

## The order flip is NOT the headline win

LCS verification across the 5 editor sub-templates (editor + style_editor —
copyeditor's per-country `<leader_reference>` tail breaks LCS when included):

- **Post-flip cross-cluster prefix: 9,825 tokens**

Comparing:

- Within-cluster `cache_control` alone (no flip): ~1.19M/run
- Flip + 2nd breakpoint after style guide: cross-cluster shared = 9,825 ×
  74 = ~727K. **But that's smaller than the within-cluster total.** The
  per-cluster prefixes (10,317-12,695 tokens) are LARGER than the cross-cluster
  prefix (9,825), so flipping to cross-cluster sharing is a net wash or loss
  unless layered with a 2nd breakpoint.

With a 2nd breakpoint after the per-cluster prefix, you get both — but the
incremental win over within-cluster-only is tiny (~5%) because most leverage
is already captured.

**Conclusion:** the order flip is polish, not the load-bearing change.
Phase 3a is just `cache_control` on the existing system block in all 5
editor sites — no template restructure required.

## Country.py: signal hygiene, not "actively losing tokens"

User pushback was right — the ~58K wasted tokens / 2 weeks is rounding-error
against a multi-million-token baseline. The reason to act is signal hygiene:

- Live `cache_control` that does nothing makes "is caching working?" return
  a misleading "yes, it's configured."
- It biases the Phase 4 alerting threshold work — country.py would never trip
  a hit-rate floor because nobody expected it to hit.
- After Phase 1 instrumentation lands, country.py's 0% hit rate will show
  prominently in any cache dashboard, requiring re-explanation each time.

**Phase 3b recommendation:** delete the `cache_control` from
`country.py:967-971` with an inline comment referencing the Phase 4.5 template
restructure. If/when that lands, the cache_control comes back.

```python
"system": [{
    "type": "text",
    "text": system_prompt,
    # TODO(Phase 4.5): re-add cache_control after country_agent.md template
    # is restructured to push {{COUNTRY}}/{{ANALYSIS_DATE}} interpolation to
    # a tail section. Today every call is its own cluster — cache_control
    # would just pay the 1.25× write premium for zero reads.
}],
```

## Updated Phase 3 plan

**Phase 3a — Editor cluster: add cache_control, no flip required**

- Files: `newsletter/structured_editor.py` (4 sites: edit_country,
  edit_regional, edit_executive, style_edit_prose),
  `newsletter/structured_copyeditor.py` (1+ sites)
- Change: wrap the existing `system_prompt` string in a list-of-blocks with
  `cache_control={"type": "ephemeral"}` — same pattern as country.py:967-971
- Expected savings: ~1.19M tokens/run, ~2.4M per 2 weeks (~70% reduction on
  editor cluster input)
- Risk: minimal — system prompt content unchanged, just adding a cache hint
- A/B noise floor still warranted: run new code path twice with same input,
  compare to itself first, before rolling to production

**Phase 3a.1 (optional polish, defer until Phase 3a's results land)**

Flip `_build_system_prompt` to put style_guide first, add 2 breakpoints. Adds
modest cross-cluster sharing for low-volume sub-templates (executive editor,
overview/at-a-glance variants with n=1). Marginal value ~5% — not worth
shipping until Phase 3a's wins are confirmed.

**Phase 3b — Country.py signal hygiene**

Delete the `cache_control` per the snippet above. Wait for Phase 1
instrumentation traces from Sunday's run to confirm zero cache reads, then
land the deletion (so the trace data documents the diagnosis).

**Phase 4 — Per-agent rollout (only for agents with structurally shared system)**

- ❌ government: ORIGINAL ANALYSIS WAS WRONG. The 2,451-token system LCP
  is the LCP *within a single n=1 cluster* (i.e., the size of one call's
  system prompt). Across the 30 calls in a run, government has 30 distinct
  clusters because `{{COUNTRY}}` interpolates into the system prompt at
  ~character 83 ("processing official institutional content for Mexico" /
  "...for Brazil" / etc.). Cross-call LCP across all 60 traces in two
  weeks is **22 tokens**. Same per-country pattern as country.py — defer
  to Phase 4.5 with the template restructure.
- ❌ devils_advocate: per-country `{{COUNTRY}}` pattern. Defer to Phase 4.5.
- ✅ regional_writer: 12 calls across 2 weeks share **10,122-token cross-call
  LCP** (verified). Single cluster of n=6 per run. Clean win, ~50K/run.
- ❌ regional: 6 calls/run, but each is a unique cluster (per-region system
  prompt). Same per-region structural problem as per-country. Skip.
- ❌ executive, global_writer: n=1 — can't benefit.
- ❌ story_map: per-country, same as country.py. Phase 4.5.

**Lesson learned:** within-cluster LCP is meaningless for clusters with
n=1 — it equals the full system prompt size, not the cacheable shared
content across calls. Always check cross-call LCP across the full agent
trace set before declaring a Phase 4 candidate. The `leverage_score`
formula correctly returns 0 for n=1 clusters, but the ranking table
showing "stable_prefix tokens (top cluster)" can be misread as
"shareable across all calls" when it's really "size of one cluster's
system prompt." Confusing, fixed forward by always doing the cross-call
LCP check separately.

**Phase 4.5 (deferred) — Template restructures**

country_agent.md, story_map_agent.md, devils_advocate_agent.md: push
country-specific interpolation to a tail section. Largest absolute potential
savings, biggest engineering effort. Defer until Phase 3a/3b/4 land and the
hit-rate measurement is stable.

## Post-Phase-3a observability check

After Phase 3a ships and Sunday's traces land, compare:

- Predicted within-cluster prefix size (from this script): 10,322-12,695 tokens
- Actual hit rate × system_prompt size for each editor agent (from
  `cache_read_input_tokens` / total prompt tokens)

If the hit rate suggests the model is caching substantially less than the
predicted prefix (e.g. only 7K instead of 10K), there's per-call variability
in the prompt assembly that the LCP didn't catch. That gap reveals additional
silent invalidators worth cleaning up before Phase 4 rollout.

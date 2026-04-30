# Interpretation: Baseline Analysis 2026-04-28

Reading of `baseline_analysis_2026-04-28.md`. The script is the data; this is the
take.

## Q1 — Country agent: cache_control is almost certainly NOT producing cross-country reuse

CV (coefficient of variation) for country agent input_tokens:
- Week 20260419: **0.16**
- Week 20260426: **0.171**

If cache was producing cross-country reuse, we'd expect a **bimodal distribution**:
call 1 has full prompt size (writes the cache), calls 2-28 have only
user-message-sized input_tokens (read the cache). That would produce a CV near 0
in the 2-28 cluster *with one outlier at the high end*. We don't see that.

What we see is a **smooth distribution** with the lowest values in specific
countries (de, no, cz, pk, ee, ae) and highest in others (lv, lt, jp, cl, es).
This is dossier/ledger-size variance, not cache hit/miss variance. Confirmed
by spot check: DE went 39K→70K week-over-week — same country, different week,
~76% jump. That's content variance, not cache behavior.

**Verdict:** the existing `cache_control` on country.py is not producing
cross-country reuse today. Either re-runs of the same country within 5 min
(rare in normal pipeline) or nothing at all. Phase 2.5 (template restructure
to enable cross-country reuse) has the leverage we expected.

Definitive confirmation still requires Sunday's run with `cache_read_input_tokens`
in the trace, but the structural evidence is strong enough to plan around.

## Q3 — Story map is the highest-leverage uncached agent, not editor cluster

The biggest surprise. Per the leverage ranking:

| agent | 2-week total input | rank |
|---|---:|---:|
| **story_map** | **6,441,437** | **1** |
| country (already partially cached) | 4,035,029 | 2 |
| editor | 1,669,365 | 3 |
| copyeditor | 958,204 | 4 |
| style_editor | 821,596 | 5 |
| government | 701,424 | 6 |

Story map runs ~30x/week with mean **109K input_tokens per call**. If most of
that is a stable system prompt or stable instructions across countries, caching
it produces savings rivaling the entire editor cluster combined.

Caveat: I haven't verified the story_map system prompt is stable across
countries. The audit said it was 12KB — but that may have been the static
template, with country-specific story content arriving via the user message.
Need to confirm before sequencing story_map ahead of the editor cluster.

Editor cluster combined (editor + copyeditor + style_editor) is **3.45M tokens**
across 2 weeks — still significant, and they have the additional shared-prefix
opportunity across 5 agents.

## Q2 — Confirmed by enumeration

Every non-country agent has 0 cache hit rate today. The Phase 4 hit-rate floor
should alert when these drop *below their post-instrumentation baseline*, not
against the literal 0.0 (else nothing alerts on regression).

## Reordering of work

Original Phase 3/4 plan: editor cluster first, then per-agent rollout.

Updated plan based on actual leverage:

1. **Phase 3a (story_map first):** confirm system prompt is stable across
   countries; if yes, add `cache_control` — this is the largest single win
   in the codebase.
2. **Phase 3b (editor cluster):** flip `_build_system_prompt` order, add
   `cache_control` to all 5 sites. Same scope as before, just relabeled.
3. **Phase 4 (rest):** government, devils_advocate, regional, ledger/consolidation,
   executive — smaller wins, mechanical.

Note: this still gates on Sunday's run for verification of the country agent
behavior (Q1 confirmation) and to establish per-agent baselines for Phase 4
alerting thresholds.

## What's NOT in this analysis (worth knowing)

We do not yet measure:
- **System-prompt vs user-message token ratio per agent.** Would tell us the
  cache leverage *ceiling* — caching a 5KB system inside a 100K user message
  saves 5%, while caching a 50KB system inside a 60K user message saves 80%.
  Cheap follow-up: add a script that approximates token counts from the
  trace's `system_prompt` and `user_message` strings (chars/4 heuristic) and
  reports per-agent ratios.
- **Within-week call ordering.** If we knew which country call ran first vs
  28th in a single pipeline run, we could check whether the first one's
  input_tokens differs from the rest. Today we only have per-country labels,
  not call ordering. Would require capturing call timestamp or sequence in
  the trace `extra` field.

Both are nice-to-have, neither blocks Phase 3.

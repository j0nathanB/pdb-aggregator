# Batch API rework plan — editor, copyeditor, style_editor, devils_advocate

Builds on `f0c7891` (Batch API foundation) + `4d72d0d` (country + government
wiring). After Phase 1 (flipping `MPM_USE_BATCH=1` in `infra/ecs.tf`),
**story_map, country, government** run through batch for ~$23/run savings.
This plan covers the remaining four fan-out stages — **editor, copyeditor,
style_editor, devils_advocate** — worth ~$8.50/run.

## Cost ceiling

Per `dev/cost_by_stage.py` (avg of 5/24, 5/17, 5/10):

| Stage | $/run | 50% batch | Effort |
|---|---|---|---|
| editor | 5.48 | 2.74 | M — streaming → non-stream, retry path |
| copyeditor | 5.55 | 2.78 | M — same as editor + 2-block cached system |
| style_editor | 4.01 | 2.01 | M — same as editor |
| devils_advocate | 2.45 | 1.23 | H — orchestrator surgery (extract from _post_country_agent) |
| **Total** | **17.49** | **8.75** | |

## Phase 1 preconditions before starting any of this

1. `MPM_USE_BATCH=1` shipped to prod via `infra/ecs.tf` change (already drafted).
2. Two weekly runs land cleanly with batch enabled for story_map / country /
   government.
3. Audit batch latency in prod logs — confirm 3 sequential batches fit the
   Sunday 9 PM ET → Monday morning publish window (the 2026-05-25 memory note
   projected 3–5h total at typical Anthropic SLA).
4. `eaf53fe`'s fallback usage tracking confirmed flowing correctly via batch
   path. **Audited:** the fallback recording in `process_story_map_response`
   (story_map.py:730–753) is path-agnostic — captures first-call usage before
   the fallback overwrites `response`. Batch path supplies `_sync_fallback_call`
   at orchestrator.py:619; sync path supplies `_stream`. Both flow through the
   same code. No change needed.
5. **Known cost-reporting gap:** `dev/cost_by_stage.py` does not know about
   batch pricing (50% off input + output). After Phase 1 ships, per-stage cost
   readouts for batched stages will be over-stated by ~50%. The trace's
   `extra.{first_call_usage, retry_usage}` field already disambiguates batch vs
   sync — fix cost_by_stage.py to apply batch multipliers when `extra.batched`
   is set. Small, not a blocker, but should land alongside Phase 2 to avoid
   misreading the savings.

## Architecture pattern (carried over from country/government)

Each batchable agent gets split into three layers:

1. **`build_X_request(...) → XBuilt`** — pure, no I/O. Returns a frozen
   dataclass with `params` (kwargs for `messages.create`) plus any side data
   needed by the response processor (config, label, prompts for tracing).
2. **`process_X_response(built, message, *, fallback_call=None) → output`** —
   parses the response, runs any tool_use → free-form fallback via the
   supplied closure, writes the trace.
3. **`run_X(...)`** — thin wrapper composing `build` + non-streaming
   `messages.create` (or streaming for the sync path where the agent
   currently streams) + `process`.

Orchestrator wires a fourth function for the batch path:
**`_run_X_batched(...)`** — calls `build_X_request` for all targets, submits
one batch, dispatches `process_X_response(built, br.message,
fallback_call=_sync_fallback_call)` per result, falls back to full sync
`run_X` on per-request batch failures.

This is the same shape proven in story_map (`src/monitor/agents/story_map.py:584,
672, 796` + orchestrator.py:595–664).

## Key constraint: streaming → non-streaming on the batch path

`editor`, `copyeditor`, and `style_editor` all use
`stream_with_retry` (their fallback for long responses + timeout safety).
**Batch API does not support streaming** — `messages.batches.create` returns
final messages only, no SSE.

This is fine because:
- Batch has no per-call HTTP timeout; the polling loop waits for the whole
  batch to end, so the timeout that motivated streaming doesn't apply.
- `max_tokens` is already capped well below Anthropic's per-message limit
  (currently `THINKING_BUDGET_TOKENS + 8192` = ~24k).

But it means `build_X_request` returns kwargs that are **streaming-agnostic**.
The sync path's `run_X` keeps `stream_with_retry` for resilience. The batch
path submits the same kwargs without stream.

## Per-stage scope

### editor (structured_editor.py:336 `edit_country`)

**Current shape:**
- Builds system + user message, calls `_call_editor_once` → `stream_with_retry`.
- Has a one-shot retry path: if first response missing `narrative_body`, sends
  `retry_message` (original + stricter instruction), without tools.

**Refactor:**
- Extract `build_editor_request(country, analysis_date, model) → EditorBuilt`
  — pure prompt assembly + kwargs.
- Extract `process_editor_response(built, response, *, retry_call=None) →
  CountryContent` — parses tool_use/free-form, runs `retry_call` if shape
  invalid. `retry_call` receives the retry kwargs (free-form, no tools) and
  must return a Message.
- `run_editor` becomes `build → stream_with_retry → process(retry_call=…)`.

**Batch path (`_run_editor_batched`):**
- Build per-country requests; submit one batch.
- Per-result: `process_editor_response(built, br.message,
  retry_call=_sync_retry_call)`. The sync retry closure is one-shot
  `messages.create` (no stream needed; retry payloads are small).
- Per-request batch failure → fall back to full sync `run_editor`.

**Hazard:** the existing retry path uses a stricter `retry_message` that
references the *original* user_message. `process_editor_response` needs the
original `user_message` to construct the retry — that's why `EditorBuilt`
must carry it.

### copyeditor (structured_copyeditor.py:83 `_copyedit_prose`)

Same pattern as editor, two extra wrinkles:

1. **Two-block cached system prompt.** Stable prefix is cached
   (`cache_control: ephemeral`); per-country `leader_reference` tail is
   uncached. The 2-block shape must be preserved in `build_X_request` — the
   memory note about cache hit rate (line 109 in the file) is load-bearing.
2. **Three caller sites:** `copyedit_country`, `copyedit_regional`,
   `copyedit_executive`, `copyedit_at_a_glance` all call `_copyedit_prose`.
   The batch path only makes sense for the country fan-out (30 calls).
   Regional/executive are 1 call each — keep them on the sync path.

### style_editor (structured_editor.py:701 `style_edit_prose`)

Same shape as editor + copyeditor. Country-scope tool_use only when
`prose_fields.keys() == {"narrative_body"}` (line 727). Build/process split
must preserve that conditional.

### devils_advocate (agents/devils_advocate.py:202 `run_devils_advocate`)

**Most surgery.** Called from `_post_country_agent` (orchestrator.py:811),
which runs **inside** the per-country processing chain. To batch DA, we have
to extract it from `_post_country_agent` and run it as a separate batched
stage after the country batch completes.

**Refactor:**
1. Split `run_devils_advocate` into `build_devils_advocate_request` +
   `process_devils_advocate_response` (already non-streaming, so no
   stream-strip needed).
2. Modify `_post_country_agent` to skip the DA call and instead emit a
   pending-DA marker on the CountryResult.
3. Add `_run_devils_advocate_batched(country_results)` that runs after the
   country batch completes — builds requests for all deep-dive results, submits
   one batch, dispatches process, attaches the DevilsAdvocate back to each
   entry.

**Trade-off:** this re-shapes the orchestrator's deep-dive flow. The current
chain is `country agent → story-cluster attach → recorder write → DA →
validation → source attrib`. Pulling DA out means validation runs without DA
attached, then DA gets stitched in after the second batch.

Validation references `entry.devils_advocate` — confirm whether order matters
(I suspect it doesn't, since DA is a downstream-of-country check, not an
input to validation). **If validation needs DA**, the simpler option is to
defer DA batching to a follow-up and accept the $1.23/run cost as the price
of orchestrator simplicity.

## Test requirements

For each refactored agent, two test classes:

1. **Sync byte-equivalence.** The existing `run_X` test (parameterized
   `messages.create`-mocked) must still pass with the refactor. No behavior
   change on the sync path. Add an assertion that
   `build_X_request(...).params` matches the kwargs the sync path used to
   call with — locks the split.

2. **Batch path.** Mirror `tests/monitor/test_batch.py` and the existing
   story_map / country / government batch tests:
   - All requests succeed → output matches sync per-country.
   - One request fails → `_sync_fallback_call` (or full `run_X` fallback)
     runs and produces output.
   - Whole batch raises → orchestrator falls back to full sync path.
   - Trace files written are byte-identical to sync (same `save_raw_response`
     calls, same `extra` keys when fallback runs).

For DA specifically, add an end-to-end orchestrator test that asserts the
`devils_advocate` field is attached to every CountryResult after the deferred
DA batch completes.

## Order of work + ROI

Recommended sequence:

1. **editor + style_editor together** (~$4.75/run). Both live in
   `structured_editor.py`, share helpers, and the refactor pattern is
   identical. Single PR.
2. **copyeditor** (~$2.78/run). Separate file; uses the 2-block cached system.
3. **devils_advocate** (~$1.23/run). Skip unless we're already in the
   orchestrator for another reason — the orchestrator surgery isn't worth
   $1.23/run on its own. Revisit if DA cost grows or if we want a totally
   clean "all fan-out batched" property.

Skip in this plan: regional, executive, global_writer. Each is 1 call/run
and not worth batching (combined ~$2.50/run). Executive is also locked to
streaming by 518e25a (output > 30k tokens).

## Open questions

1. **Sequential batch latency budget.** Six sequential batches in the Phase
   1 path (story_map → government → country → regional → exec → global) plus
   three more from this plan (editor → copyeditor → style_editor) is nine
   sequential batches. At Anthropic's typical <1h SLA, that's ~9h worst case.
   The Fargate task runs Sun 9 PM ET; Monday morning publish target gives ~12h
   wall-clock. Need a real-prod measurement before committing.
2. **DA validation order.** Does the country-agent validation step depend on
   `entry.devils_advocate`? Read `_post_country_agent` carefully before
   committing to the DA batch split.
3. **Cost-reporting fix order.** `dev/cost_by_stage.py` should learn about
   batch pricing alongside Phase 2 — otherwise the per-stage cost numbers
   used to evaluate the rework will be wrong by ~50% on already-batched
   stages.

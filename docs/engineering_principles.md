# Engineering Principles

Extracted from the 2026-04-20 debugging session. Every principle here is
anchored to a specific failure we hit — this is not generic advice.

Read these when starting work on the pipeline. They prevent the specific
classes of pain we've already paid for.

---

## 1. Validate at the boundary, not in the parser

**Failure pattern we paid for**: five consecutive commits (`539b22c`,
`3170f48`, `bca63ae`, `36f7c12`, `bce0bdd`) each patched one flavor of
"LLM returned slightly-off JSON." Missing category → KeyError. Invalid
enum → ValidationError. String-instead-of-int → ValidationError.
Construction failure → whole country lost.

The structural fix (Anthropic tool_use with typed `input_schema`) was
discovered only after the fifth patch. The API validates the tool call
server-side, so shape drift is caught at the boundary instead of
discovered by Python fragility.

**Rule**: when you've written more than 2-3 `except` blocks at the same
boundary, stop patching and fix the boundary.

**Apply it by**: treating every LLM call that expects structured output
as a tool_use call with a real JSON schema. `src/monitor/schema_helpers.py`
(the `pydantic_to_tool_schema` helper) is there so adding new tool schemas
costs one line per pydantic model.

---

## 2. Fail loudly at the lowest reasonable layer

**Failure pattern we paid for**: `trafilatura` and the spaCy model were
missing from the container for weeks. Each raised `ImportError` at
runtime, got caught by generic `except Exception` handlers, and logged
at DEBUG (for curl) or WARNING per-URL (for browserbase). The pipeline
kept "working" — just silently cascading every URL to diffbot, burning
quota and producing degraded briefs.

Commit `7cc79e1` established the fix pattern in an earlier incident:
hoist import-time dependencies to module scope so they crash the
container at startup, not per-invocation at runtime. Today we extended
it for trafilatura (`c9ab83c`) and spaCy (`2a2716b`).

**Rule**: infrastructure failures (missing deps, missing models,
misconfigured services) belong at process startup. Data-shape failures
can be soft IF they're loudly logged and telemetered.

**Apply it by**:
- Imports of required third-party modules at the top of the file, not
  deferred into functions.
- `from X import thing` for each thing you rely on — not `X.thing`
  deferred.
- A CI smoke-test that builds the container and runs
  `python -c "from src.monitor.cli import main"` (or equivalent) so any
  import error blocks deploy.

---

## 3. Hermetic builds

**Failure pattern we paid for**: the local dev environment accumulates
transitive installs over time; the container image builds from scratch
with only `requirements.txt`. Three separate outages today came from
this drift: `trafilatura`, `en_core_web_md`, and a cluster of missing
deps (`jinja2`, `pydantic`, `pyyaml`, `python-dotenv`).

**Rule**: the delta between `pip install -r requirements.txt` into a
clean venv and your current local venv is a bug waiting to happen.

**Apply it by**:
- Periodically rebuild your local venv from scratch to catch drift.
- Keep `requirements.txt` authoritative — no one should rely on
  "just `pip install`-ing whatever was needed at the time."
- CI builds the container on every push (the ECR workflow now does
  this; see `0d0d0153f` era notes — actually `e97be61`).

---

## 4. Verify, don't infer

**Failure pattern we paid for**: during this session I confidently
stated several things that turned out to be wrong, each recoverable
with 30 seconds of `grep`:
- Claimed `--skip-layer2` was a CLI flag (it isn't — it's only a
  function parameter).
- Claimed `--country it --resume-from regional` would limit synthesis
  to that region (it doesn't — `--country` only gates desk stage).
- Miscalculated a task's elapsed time by ~40 minutes.
- Initially claimed always-rebuilding ECR would prevent running-task
  staleness (it wouldn't; the clone is fixed at task launch).

Each was unforced. The user caught them; each cost trust and
conversation turns.

**Rule**: grep before claim. Before asserting "X does Y," read the
code that implements it. Before acting on inferred state, check the
actual state.

**Apply it by**:
- When you're about to recommend a flag or command, run `--help` on it
  first.
- When you're about to describe behavior, open the file and read the
  function. If the behavior is more than two levels of indirection from
  what you can see, either read the whole chain or say so explicitly.
- Distinguish "I verified this by reading X" from "I believe this based
  on Y."

---

## 5. Observability is prevention, not a luxury

**Failure pattern we paid for**: the filtering pipeline was dropping
results in several stages without any counters. We couldn't answer
"are `$discard` rules firing?" until we added logging in `0eee655`.
Commit `b0404af` added `[fallback]` tagging to story_map's tool-use
path so we can measure how often the fallback fires.

Earlier in the day we found that `force_deep_dive=True` silently nuked
the triage scan (commit `8480b23` from weeks ago). No counter, no
warning — just empty wire/domestic lists downstream.

**Rule**: every silent branch is a potential silent failure.

**Apply it by**:
- A `logger.info("filter X: dropped %d/%d", n, total)` line costs
  nothing and converts invisible into measurable.
- When you write an if/else, ask: "if this branch took the other path
  tomorrow, would I know?"
- Fallback paths must announce themselves. A fallback that fires
  silently is indistinguishable from a bug.

---

## 6. Integration tests against real historical data

**Failure pattern we paid for**: the repo has 643+ unit tests. None of
them caught the `KeyError: 'alignment_diplomatic'` that lost Italy,
the `ValidationError: status='unchanged'` that dropped claim checks,
or the `force_deep_dive` bug that nuked triage scan data.

All three would have been caught by a test that replayed saved traces
from past runs through the current parser / pipeline code.

**Rule**: unit tests verify "this function does what I wrote."
Integration tests against production data verify "the system handles
real-world inputs." You need both.

**Apply it by**:
- A `tests/monitor/test_replay.py` that loads last month's
  `briefs/*/traces/*.json` and runs each through the current
  `parse_country_response` / `parse_story_map_response`. If any raises,
  the test fails.
- Update monthly or when response shape changes.

---

## 7. Blast-radius awareness and checkpointing

**Failure pattern we paid for**: a Fargate run lost most of 30
countries' expensive country-agent work when each country tripped on
a single-point parse failure. Italy died to a KeyError, then other
countries died to `ValidationError`, and there was no mechanism to
recover one country without re-running everything.

Commit `3806936` added the `recover` subcommand (one country + its
region + executive + affected pages). Commit `539b22c` made the
attribution check non-blocking. Commit `3170f48` made missing
categories fall back to prior ledger state instead of losing the
country.

**Rule**: for any expensive operation, ask: "what do I lose if this
one step fails at minute N?" If the answer is "everything before
minute N," it's a design problem, not a reliability problem.

**Apply it by**:
- Checkpoint after each expensive LLM call so work isn't lost on
  downstream failure.
- Wrap per-item loops in try/except so one bad item doesn't kill the
  batch.
- Have a "recover just this one" path for any expensive multi-step
  workflow.

---

## 8. Feature flags for uncertain changes

**Failure pattern we paid for**: several changes today (tool_use for
country agent + story_map, the inverted allowlist, the story_map
fallback) were landed behind `MPM_USE_TOOL_SCHEMA` and
`MPM_DOMAIN_ALLOWLIST` env var gates. That meant we could ship them
without betting the pipeline on them, A/B them in production, and
flip defaults once validated.

**Rule**: a feature flag is cheaper than a revert commit, and much
cheaper than a bad production run.

**Apply it by**:
- Default: new risky behavior OFF. Flag enables it.
- Log clearly when the new path is active: `Story map: [fallback]`,
  `Brave: dropped X off-allowlist URLs`.
- Once a run validates the new path, flip the default.

---

## 9. Capture the why, not just the what

**Session benefit we noticed**: the plan documents I wrote to
`dev/*.md` (`story_map_tool_use_plan.md`, `story_map_input_volume_plan.md`,
`off_topic_filter_proposal.md`, `goggle_audit_2026-04-12.md`, this
file) created continuity that would otherwise have lived only in chat.

Also: the per-country commit message on `aafa75a` (media-audit goggle
changes) explains *why* each domain got the tier it did — future me
won't have to re-derive that decision.

**Rule**: code captures *what*. Commit messages and plan docs capture
*why*. The why decays fastest and costs most to reconstruct.

**Apply it by**:
- For any non-trivial decision, write a `dev/*.md` plan doc before
  implementing. Even a 50-line sketch.
- Commit messages that include: the symptom, the root cause, the fix,
  and what it explicitly does NOT fix.
- Keep exploratory work in `dev/` — it's not production but it's
  durable and reviewable.

---

## 10. Scope discipline

**Failure pattern we noticed**: the default tooling regenerated the
entire pipeline output for a single-country recovery. The fix
(`recover` subcommand) scoped the work to just what changed.

Similarly: `MPM_DOMAIN_ALLOWLIST` was designed as a flag because we
couldn't confidently assert the right default — instead of arguing,
we made both options available.

**Rule**: the scope of a fix should match the scope of the problem.
When in doubt, provide the narrower option as a flag and let actual
usage determine the default.

**Apply it by**:
- "Recovery" flows should exist alongside full-run flows. Failing in
  production shouldn't force a full re-run.
- When debating "should this be the default," ship both behind a flag
  and decide based on a month of real runs.

---

# The two that matter most

If you internalize only two: **(1)** schema-validation at the LLM
boundary, and **(6)** integration tests against real historical data.
Together they would have collapsed most of today's five-patch cascade
into one prevented incident.

The rest are supporting habits. Work on those two and the others tend
to come with them.

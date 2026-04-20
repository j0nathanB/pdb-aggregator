# Plan: migrate country agent to Anthropic tool-use for structured output

## Why

Today's local Fargate run surfaced three distinct LLM-shape-drift failures in
`parse_country_response` — each a single-point-of-failure that previously
discarded an entire country's expensive (extended-thinking + web-search) agent
output:

- `KeyError: 'alignment_diplomatic'` — LLM omitted a signal category in
  `updated_signal_categories` (lost Italy on 2026-04-20)
- `ValidationError: status='unchanged'` — LLM invented an enum value outside
  `ClaimStatus` (silently dropped the claim check)
- `ValidationError: confidence_in_claim='high'` — LLM used a word instead of
  1-5

Today we landed five consecutive defensive fixes (commits `539b22c`,
`3170f48`, `bca63ae`, `36f7c12`) that treat each symptom: ledger carry-
forward on missing fields, `safe_enum` with defaults, string-to-int coercion,
try/except wrappers around pydantic constructions. Each fix works, but the
pattern is brittle: the *next* unanticipated LLM drift will require another
patch, and silent carry-forward means we lose data that would have been
captured if the shape had been right.

The root cause is free-form JSON output from a large, nested schema. The
durable fix is Anthropic's tool-use with a typed `input_schema`: the API
validates the tool call's `input` against the schema **server-side** before
returning. Missing required fields and wrong enum values are caught at the
API boundary. By the time we see the response, the shape is guaranteed.

This is the same pattern planned for `story_map` in
`dev/story_map_tool_use_plan.md`, but the country agent is higher priority:
its output is much larger and more nested, and it's where we've been
hemorrhaging work today.

## Scope

- `src/monitor/agents/country.py` — swap to tool-use; delete the shape-drift
  fallbacks that become dead code (most of `parse_country_response`,
  `_coerce_confidence`, the ledger-carry-forward branches).
- `assets/prompts/agents/country_agent.md` — replace the "output this JSON
  shape" section with "call the `record_country_analysis` tool" instruction.
- `src/monitor/schema_helpers.py` (new) — small helper to convert a Pydantic
  v2 model into an Anthropic-friendly JSON schema (inline `$defs` into
  `$refs`; drop fields Anthropic doesn't like like `title`, `description` on
  sub-models). Reusable for the story_map plan when it lands.
- `tests/monitor/test_country_agent.py` — update mocks to return a response
  with a `tool_use` block; keep the resilience tests from today as defense-
  in-depth (hydration still uses `.get()` for optional fields).

Out of scope (tracked elsewhere or do separately):
- Bumping `max_tokens` for truncation — orthogonal to this refactor.
- `story_map` tool-use refactor — see `dev/story_map_tool_use_plan.md`.
  Implement after this lands as a reuse of the same helper + pattern.
- Other agents (triage, government, regional, executive). Smaller surface
  areas and haven't bit us; port later if needed.

## Target architecture

Today (`country.py:782-815`):
```python
api_kwargs = {
    "model": MODEL,
    "max_tokens": THINKING_BUDGET_TOKENS + 8192,
    "thinking": {"type": "enabled", "budget_tokens": THINKING_BUDGET_TOKENS},
    "system": [...],
    "messages": [{"role": "user", "content": prompt}],
}
if not use_story_map:
    api_kwargs["tools"] = [{"type": "web_search_20250305", ...}]

response = await client.messages.create(**api_kwargs)
# ... collect text_parts from response.content ...
response_text = "\n".join(text_parts)
# then parse_country_response(response_text, ...) via extract_json + a
# hundred lines of defensive parsing
```

After:
```python
api_kwargs = {
    "model": MODEL,
    "max_tokens": THINKING_BUDGET_TOKENS + 8192,
    "thinking": {"type": "enabled", "budget_tokens": THINKING_BUDGET_TOKENS},
    "system": [...],
    "messages": [{"role": "user", "content": prompt}],
    "tools": [RECORD_COUNTRY_ANALYSIS_TOOL],
    "tool_choice": {"type": "auto"},   # so the model can use web_search first
}
if not use_story_map:
    api_kwargs["tools"].append({"type": "web_search_20250305", ...})

response = await client.messages.create(**api_kwargs)

tool_input: dict | None = None
for block in response.content:
    if block.type == "tool_use" and block.name == "record_country_analysis":
        tool_input = block.input   # validated by API against input_schema
        break
if tool_input is None:
    raise ValueError(f"Country agent {config.code}: no record_country_analysis call")

output = hydrate_country_output(tool_input, week_date, date_range, ledger)
```

The `tool_choice` is `"auto"` rather than forced, because when `web_search`
is also available the model needs multiple turns (search → think → record).
In the story_map-mode path (no web_search), we can still use `auto` — the
system prompt should make clear this is a one-tool task.

## Schema

The output shape is already captured in pydantic models. Rather than
hand-writing 200+ lines of JSON schema (error-prone and will drift from
the models), generate it with `model.model_json_schema()` and inline
`$defs` via a small helper.

```python
# src/monitor/schema_helpers.py

def pydantic_to_tool_schema(model_cls: type[BaseModel]) -> dict:
    """Produce an Anthropic-compatible input_schema from a Pydantic model.

    Pydantic emits $defs + $refs; Anthropic's tool schema accepts those but
    inlined schemas are easier for the model to reason about. This helper
    resolves all $refs into their $def bodies and returns the flat schema.

    Drops Pydantic-internal keys Anthropic doesn't need (title on
    sub-schemas, etc.).
    """
    raw = model_cls.model_json_schema()
    defs = raw.pop("$defs", {})
    resolved = _inline_refs(raw, defs)
    return _drop_titles(resolved)
```

Then at module scope in country.py:
```python
RECORD_COUNTRY_ANALYSIS_TOOL = {
    "name": "record_country_analysis",
    "description": (
        "Record the complete weekly deep-dive analysis for this country. "
        "All fields are required — omit nothing. Call exactly once when "
        "your analysis is complete."
    ),
    "input_schema": _build_record_country_schema(),
}

def _build_record_country_schema() -> dict:
    """Compose the tool input schema from the three top-level components."""
    return {
        "type": "object",
        "required": ["weekly_entry", "updated_signal_categories",
                     "updated_posture_summary"],
        "properties": {
            "weekly_entry": pydantic_to_tool_schema(WeeklyEntry),
            "updated_signal_categories": {
                "type": "object",
                "required": [c.value for c in SignalCategory],
                "properties": {
                    c.value: pydantic_to_tool_schema(SignalCategoryAssessment)
                    for c in SignalCategory
                },
            },
            "updated_posture_summary": pydantic_to_tool_schema(PostureSummary),
        },
    }
```

This keeps the schema in lockstep with the pydantic models: if we add a
field to `WeeklyEntry`, the schema updates automatically on next launch.

## Implementation steps

1. **Write `src/monitor/schema_helpers.py`** with `pydantic_to_tool_schema`
   and unit tests. Edge cases to cover: enums (should become `"enum": [...]`
   in the schema), nested models (recursive inlining), list[Model], dict[K, V]
   (Pydantic emits `additionalProperties`; Anthropic accepts it).

2. **Define `RECORD_COUNTRY_ANALYSIS_TOOL`** and `_build_record_country_schema`
   at module scope in country.py. Verify the generated schema parses cleanly
   by calling the Anthropic API's `/v1/messages/count_tokens` endpoint (or
   a lightweight dry-run call) so misshaped schema is caught before first use.

3. **Add `hydrate_country_output(tool_input, week_date, date_range, ledger)`**
   — thin constructor that takes the validated dict and returns
   `CountryAgentOutput`. Most of the logic in today's `parse_country_response`
   goes away. Keep `safe_date` / `safe_enum` for the date and enum fields
   (the schema guarantees the string *value* but Python still needs to
   parse "2026-04-19" into `date`). Drop the ledger-carry-forward branches —
   the schema guarantees presence.

4. **Replace the API call in `run_country_agent`** (country.py:782-815):
   - Add `RECORD_COUNTRY_ANALYSIS_TOOL` to `tools` list alongside any
     existing `web_search` tool.
   - Use `tool_choice={"type": "auto"}` (not forced — the model needs to be
     able to call web_search during its reasoning).
   - Iterate `response.content` and locate the `tool_use` block with
     `name == "record_country_analysis"`.
   - Raise a clear error if no such block exists (shouldn't happen; the
     prompt will instruct the model to end with this call).

5. **Update the prompt** (`assets/prompts/agents/country_agent.md`):
   - Delete the `## Your Output` JSON-shape example.
   - Add: *"When your analysis is complete, call the
     `record_country_analysis` tool exactly once. The tool input schema
     enforces the structure, so provide every field. Do not emit the
     analysis as text — only via the tool call."*

6. **Preserve tracing**: `save_raw_response` currently saves a text string;
   pass `response_text=json.dumps(tool_input, indent=2)` so existing trace
   analyzers keep working. Add the original web_search queries as a
   parallel tracked field.

7. **Delete dead code in country.py**:
   - `parse_country_response` body simplifies to ~15 lines (call
     `hydrate_country_output`)
   - `_coerce_confidence`, `_CONFIDENCE_WORD_MAP` become defense-in-depth
     in `hydrate_country_output` (still useful for the `confidence` int
     since pydantic's `ge=1, le=5` is enforced but the schema itself
     just says `integer`); keep them.
   - Ledger carry-forward branches become dead — remove them once verified
     on a real run.

8. **Tests**:
   - Update `TestParseCountryResponse` → `TestHydrateCountryOutput`; mock
     a valid tool_input dict and verify hydration.
   - Keep the resilience tests from today but mark them defence-in-depth;
     they should still pass since `hydrate_country_output` retains `.get()`
     for optional fields.
   - Add: schema-generation test (call `pydantic_to_tool_schema(WeeklyEntry)`
     and assert no `$ref` remains in the output).

## Validation

1. **Schema sanity check**: generate the tool schema, `json.dumps(schema)`,
   pretty-print it, eyeball for pathologies (circular refs, missing
   required fields, etc.). Total size should be <20kB.

2. **Smoke test on three countries**:
   - Canada (`ca`) — was the first to fail in today's run. Small-ish output.
   - Italy (`it`) — had the `alignment_diplomatic` KeyError. Complex output.
   - Mexico (`mx`) — highest-volume country historically; stresses the
     `developments` arrays.

3. **Local CLI invocation**: `python -m src.monitor.cli run --country it
   --date 2026-04-19 --skip-layer2 --skip-synthesis`. Verify:
   - No `KeyError` / `ValidationError` in logs
   - No `Skipping malformed …` warnings for well-formed LLM responses
   - The `tool_input` dict matches what `hydrate_country_output` expects
   - Downstream ledger write succeeds

4. **Fargate rollout**: push, let the rebuild complete, fire a manual task.
   Watch for:
   - Absence of the three error classes we fixed today
   - Absence of any new error classes the schema might surface (the model
     refusing to emit because the schema is too constraining)

## Known wrinkles

1. **Extended thinking + tool_use + web_search all enabled simultaneously**:
   supported per Anthropic's docs but lightly-tested combination. Budget
   a half-day for smoke-testing; specifically watch for:
   - Does the model emit `thinking` blocks, then `server_tool_use` for
     web_search, then the final `tool_use` for record_country_analysis,
     all in one response?
   - If the model hits `max_tokens` mid-way, do we get a partial response
     with no tool_use block? If so, raise a clear error (don't fall back).

2. **Schema size and complexity**: 200+ fields across the nested tree
   may exceed what the model can reliably populate in a single tool call.
   Watch for cases where the model "gives up" partway through — if
   observed, consider splitting into multiple tools (e.g., one for
   `weekly_entry` and one for `updated_*`) and instructing the prompt
   to call both.

3. **`additionalProperties` on SignalCategory → CategoryMovement map**:
   pydantic emits `dict[SignalCategory, CategoryMovement]` as `type: object,
   additionalProperties: <CategoryMovement schema>`. Anthropic accepts
   this, but forcing specific keys (all 5 signal categories required) is
   better. The `_build_record_country_schema` function hard-codes the
   expected keys explicitly rather than relying on `additionalProperties`
   for this exact reason.

4. **Web_search tool vs record_country_analysis tool interaction**: the
   system prompt already tells the model when to search. The
   `record_country_analysis` description should explicitly note "call
   exactly once when finished" so the model doesn't call it multiple
   times during search iterations.

5. **Cost and token impact**: the input_schema counts toward the input
   context. Our CountryAgentOutput schema is ~6kB; that's ~1500 tokens
   per request. Negligible compared to the dossier + ledger + prompt,
   but note it.

6. **Backward compatibility with existing traces**: our trace format
   assumes `response_text` is the JSON. Dumping `tool_input` as JSON and
   storing it in the same slot preserves all existing trace analysis
   tooling (`dev/goggle_audit_*.py`, etc.). No change needed there.

## Rollout plan

1. Land schema_helpers.py + tests as a standalone commit (low-risk
   utility).
2. Land country.py refactor behind a feature flag
   (`MPM_USE_TOOL_SCHEMA=1`) so we can A/B on real runs. Default off.
3. Smoke test on 3 countries with flag on. Compare outputs against a
   parallel run with flag off.
4. If outputs match within expected variance, flip default to on.
5. After one full Fargate run succeeds, delete the flag and the legacy
   parse path.
6. Separately, port `story_map` to the same pattern using the now-proven
   `pydantic_to_tool_schema` helper.

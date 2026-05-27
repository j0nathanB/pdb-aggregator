# Plan: migrate story_map agent to Anthropic tool-use for structured output

## Why

`story_map` LLM output is malformed JSON ~38% of the time (11/29 countries in
the 2026-04-12 run). It always gets rescued by `json_repair`, but the warning
in `src/monitor/sanitize.py:175` is accurate: *"Repaired output may be
structurally incorrect; verify downstream parsing."* json_repair guesses
structure without schema knowledge, so downstream clustering can silently be
wrong.

Failure modes observed on 2026-04-12:
- `Expecting ',' delimiter` × 8 — missing commas between JSON elements
- `Unterminated string` × 2 — output truncated near `max_tokens` (fr @ 55k, it @ 56k chars)
- `Expecting value: line 1 col 1` × 1 — model prepended prose ("Looking at the search results for Taiwan...")

Forcing tool-use eliminates the malformed-JSON class entirely: the API
validates `tool_use.input` against the declared schema before returning.

## Scope

- `src/monitor/agents/story_map.py` — swap to tool-use, drop json_repair path
- `assets/prompts/agents/story_map_agent.md` — replace JSON-example section
  with tool-call instruction
- `tests/monitor/` — update any story_map mocks to return `tool_use` blocks

Out of scope (do separately):
- `max_tokens` bump for truncation (fr/it at ~55k chars). Orthogonal to this
  refactor — tool-use has the same output budget. Bump `THINKING_BUDGET_TOKENS + 8192`
  → `THINKING_BUDGET_TOKENS + 16384` (or higher) as a separate change.
- **Story_map input volume reduction** (goggle audit, discard enforcement,
  per-domain caps). See `dev/story_map_input_volume_plan.md` and the
  underlying audit in `dev/goggle_audit_2026-04-12.md`. Those cuts attack
  the upstream pressure on output size; this plan handles JSON validity.
- Porting other JSON-heavy agents (triage, expansion, government, regional,
  executive). If this lands cleanly, it's the template.

## Target architecture

Today (`story_map.py:394-414`):
```python
async with client.messages.stream(
    model=..., max_tokens=THINKING_BUDGET_TOKENS + 8192,
    thinking={"type": "enabled", "budget_tokens": THINKING_BUDGET_TOKENS},
    system=..., messages=[...],
) as stream:
    response = await with_heartbeat(stream.get_final_message(), ...)

for block in response.content:
    if block.type == "text":
        text_content = block.text
        break
# then extract_json → json.loads → json_repair
```

After:
```python
async with client.messages.stream(
    model=..., max_tokens=...,
    thinking={"type": "enabled", "budget_tokens": THINKING_BUDGET_TOKENS},
    tools=[RECORD_STORY_MAP_TOOL],
    tool_choice={"type": "tool", "name": "record_story_map"},
    system=..., messages=[...],
) as stream:
    response = await with_heartbeat(stream.get_final_message(), ...)

tool_input: dict | None = None
for block in response.content:
    if block.type == "tool_use" and block.name == "record_story_map":
        tool_input = block.input  # already a validated dict
        break
if tool_input is None:
    raise ValueError(f"Story map {config.code}: no tool_use block in response")
output = hydrate_story_map(tool_input)
```

## Schema

One tool definition. Sketch — refine based on the current dataclasses in
`story_map.py:39-98`:

```python
RECORD_STORY_MAP_TOOL = {
    "name": "record_story_map",
    "description": "Record the complete clustered story map for this country's week of news coverage.",
    "input_schema": {
        "type": "object",
        "required": [
            "country", "analysis_date", "search_results_total",
            "stories_identified", "off_topic_filtered",
            "stories", "single_source_items", "unassigned", "noise_summary",
        ],
        "properties": {
            "country": {"type": "string"},
            "analysis_date": {"type": "string", "description": "YYYY-MM-DD"},
            "search_results_total": {"type": "integer"},
            "stories_identified": {"type": "integer"},
            "off_topic_filtered": {"type": "integer"},
            "stories": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": [
                        "story_id", "headline", "summary", "actors_involved",
                        "signal_category_hint", "source_count", "sources",
                        "date_range", "articles", "representative_urls",
                    ],
                    "properties": {
                        "story_id": {"type": "integer"},
                        "headline": {"type": "string"},
                        "summary": {"type": "string"},
                        "actors_involved": {"type": "array", "items": {"type": "string"}},
                        "signal_category_hint": {
                            "type": "string",
                            "enum": [
                                "alignment_diplomatic", "security_defense",
                                "economic_tech", "institutional",
                                "domestic_regime", "unclear",
                            ],
                        },
                        "source_count": {"type": "integer"},
                        "sources": {"type": "array", "items": {"type": "string"}},
                        "date_range": {"type": "string"},
                        "articles": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "required": ["title", "source", "url", "date"],
                                "properties": {
                                    "title": {"type": "string"},
                                    "source": {"type": "string"},
                                    "url": {"type": "string"},
                                    "date": {"type": "string"},
                                },
                            },
                        },
                        "representative_urls": {
                            "type": "array", "items": {"type": "string"},
                        },
                    },
                },
            },
            "single_source_items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["headline", "source", "url", "signal_category_hint"],
                    "properties": {
                        "headline": {"type": "string"},
                        "source": {"type": "string"},
                        "url": {"type": "string"},
                        "signal_category_hint": {"type": "string"},
                    },
                },
            },
            "unassigned": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["url", "description", "extra_snippets"],
                    "properties": {
                        "url": {"type": "string"},
                        "description": {"type": "string"},
                        "extra_snippets": {"type": "array", "items": {"type": "string"}},
                    },
                },
            },
            "noise_summary": {"type": "string"},
        },
    },
}
```

Mark everything `required` to avoid the model silently omitting fields the
dataclass expects. The dataclass still has defaults, so hydration stays
defensive.

## Implementation steps

1. Define `RECORD_STORY_MAP_TOOL` at module scope near the dataclasses.
2. Add `hydrate_story_map(data: dict) -> StoryMapOutput` — mostly the same
   logic as the current `parse_story_map_response`, minus the JSON parsing.
   Keep the `.get()` defaulting for defence-in-depth.
3. Replace the API call in `run_story_map_agent`:
   - Add `tools=[RECORD_STORY_MAP_TOOL]` and `tool_choice={...}`.
   - Iterate blocks looking for `tool_use`, not `text`.
   - Error clearly if no tool_use block found (shouldn't happen under forced choice).
4. Update `save_raw_response` call: pass `response_text=json.dumps(tool_input, indent=2)`
   so traces stay inspectable and the existing per-country trace parser
   (`dev/*` scripts that aggregate `response_text`) keeps working.
5. Edit `assets/prompts/agents/story_map_agent.md`:
   - Delete `## Your Output` JSON example.
   - Add: *"When finished, call the `record_story_map` tool with the
     complete clustering. Do not output text — only the tool call. The tool
     input validates the structure, so all fields must be present."*
6. Delete the unused `json_repair` import and `repair_json` fallback in
   `parse_story_map_response` (src/monitor/agents/story_map.py:18, 273-277).
7. Check `tests/monitor/test_story_map.py` (or equivalent) — update mocks to
   return a response with a `tool_use` block. Pattern:
   ```python
   mock_response.content = [
       MagicMock(type="tool_use", name="record_story_map", input={...}),
   ]
   ```

## Validation

Smoke test on 3 countries with varied output sizes:
- **mx** (consistently large, historically ~500 results)
- **tw** (the prose-preamble case from 2026-04-12)
- **fr** or **it** (the truncation cases — will surface if `max_tokens` needs bumping)

Run locally via the pipeline CLI for a single country. Verify:
- No `JSON repair fallback used [story_map]` warnings in logs.
- `tool_input` hydrates to a complete `StoryMapOutput` with no missing fields.
- Downstream country agent receives the same clustering shape it got before.
- Accounting check (`story_map.py:444-455`) still balances.

Then deploy via the same ECR build path, let it run next Sunday, check the
WARNING count for `JSON repair fallback used` drops to 0 for `[story_map]`.

## Known wrinkles to resolve during implementation

- **Thinking + forced tool_choice combo**: supported but less-common; verify
  the streaming SDK delivers both `thinking` and `tool_use` blocks cleanly.
  Likely fine, but budget an hour for a rough spot.
- **`extract_usage` / `extract_thinking` helpers**: confirm they handle a
  response whose primary content block is `tool_use`, not `text`. Probably
  already do since they look at `response.usage` and thinking blocks
  separately, but verify.
- **Empty tool_use**: if the model somehow returns a tool_use with
  schema-invalid content, the API should reject before we see it. If we do
  see partial output, fail loudly — don't fall back to json_repair.

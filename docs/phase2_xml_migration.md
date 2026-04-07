# Phase 2: Editorial layer XML migration

Migrate the editorial layer (editors, copyeditors, style editor) from JSON to XML-tagged markdown to eliminate the most frequent class of LLM parse failures.

**Status:** Scoped, not yet implemented. Phase 1 (`json-repair` for structured agents) is implemented separately.

## Why

JSON parse failures cluster in editorial agents because their output is mostly prose wrapped in a single key. Every quote, dash, newline, and backslash is an opportunity for the LLM to mis-escape and break parsing. We've already added `_unwrap_double_json()` and prose-fallback logic specifically because of this.

Anthropic's prompting guides recommend XML tags for structured output — Claude is well-trained on this format. The migration eliminates the escape burden entirely for prose-heavy outputs while keeping JSON for genuinely structured agents (country, triage, story map, synthesis).

## Scope

The editorial layer has **9 LLM call points** across 3 stages × 4 content types, plus a generic style editor. All live in `src/monitor/newsletter/structured_editor.py` and `structured_copyeditor.py`.

| File | Function | Output fields |
|------|----------|---------------|
| `structured_editor.py` | `edit_country` | `narrative_body` |
| `structured_editor.py` | `edit_regional` | `regional_lead`, `card_summary` |
| `structured_editor.py` | `edit_executive` | `edited_essay` |
| `structured_editor.py` | `edit_watchlist` | `edited_narrative` |
| `structured_editor.py` | `style_edit_prose` | varies (dispatches by field name) |
| `structured_copyeditor.py` | `copyedit_country` | `narrative_body` |
| `structured_copyeditor.py` | `copyedit_regional` | `regional_lead`, `card_summary` |
| `structured_copyeditor.py` | `copyedit_executive` | `edited_essay` |
| `structured_copyeditor.py` | `copyedit_watchlist` | `edited_narrative` |

## Format change

### Output (changes)

**Before:**
```json
{"narrative_body": "Pakistan lurched between crises this week. The Iran war pulled it deeper into Saudi Arabia's orbit while \"open war\" erupted on the Afghan border..."}
```

**After:**
```
<narrative_body>
Pakistan lurched between crises this week. The Iran war pulled it deeper into Saudi Arabia's orbit while "open war" erupted on the Afghan border...
</narrative_body>
```

For multi-field outputs (regional editor):
```
<regional_lead>
Across the region, three patterns came into focus...
</regional_lead>

<card_summary>
Five countries pulled in different directions on the Iran crisis.
</card_summary>
```

### Input (unchanged)

Inputs stay JSON. They're constructed deterministically by Python (`_build_country_input`, `_build_regional_input`, etc.) — no escape risk. Nested structures (developments, sources, claims) are where JSON is the right tool.

## New parser

Single helper at the top of `structured_editor.py`:

```python
import re

def extract_tag(text: str, tag: str) -> str | None:
    """Extract content from <tag>...</tag>. Returns None if not found.

    Tolerant of leading/trailing whitespace inside the tag boundaries.
    Uses non-greedy matching so multiple tags in one response work.
    """
    pattern = rf"<{tag}>\s*(.*?)\s*</{tag}>"
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1).strip() if match else None
```

Per-agent result handling:

```python
narrative = extract_tag(response_text, "narrative_body")
if narrative is None:
    narrative = response_text.strip()  # fallback
country.narrative_body = narrative
```

Replaces the current `extract_json` + `_unwrap_double_json` + JSON parse fallback chain.

## Migration order

Sequential rollout, one agent at a time, monitoring parse failures between each:

1. Country editor (biggest blast radius, simplest output)
2. Country copyeditor
3. Country style editor
4. Regional editor (first multi-field test)
5. Regional copyeditor + style editor
6. Executive editor + copyeditor + style editor
7. Watchlist editor + copyeditor + style editor

Run a real pipeline cycle after step 1 and step 4 to validate end-to-end.

## Prompt rewrites

Each agent's `<output_format>` block needs updating. Pattern:

```
<output_format>
Return your edited prose wrapped in <narrative_body> tags. No JSON. No commentary outside the tags. Quotes, dashes, em-dashes, and newlines pass through verbatim — do not escape them.

<narrative_body>
Your edited prose here.
</narrative_body>
</output_format>
```

The `<example>` blocks also need their example outputs converted from JSON to XML — they're the strongest training signal.

**Estimated diff:** ~30 lines per prompt × 9 agents ≈ 270 lines of prompt edits. Mostly mechanical.

## Backward compatibility

Two options:

- **Option A: Hard cutover.** Switch parsers, rewrite prompts, accept that old traces in `briefs/{date}/traces/editor_*.json` can't be re-parsed by replay tooling.
- **Option B: Dual parser.** Try XML extraction first; fall back to JSON if no tag found. Lets old traces continue to replay. Recommended for one release cycle.

## Test impact

- `tests/monitor/test_structured_editor.py` (if exists): mock LLM responses return JSON → switch to XML
- `tests/monitor/test_structured_copyeditor.py` (if exists): same
- E2E tests that mock the editor: same
- Estimated: 15–25 fixture updates

## Files changed

| Type | Count |
|------|-------|
| Source files | 2 (`structured_editor.py`, `structured_copyeditor.py`) |
| Prompts (in code as constants) | 9 system prompts inside the same 2 files |
| Test fixtures | ~15-25 |
| Helper added | 1 (`extract_tag`) |

Total LOC change: roughly +50/-150 (parsers get simpler).

## Risks

| Risk | Mitigation |
|------|-----------|
| LLM ignores tags and returns prose-only | Same prose-only fallback we already have |
| LLM emits literal `<` or `>` inside content | Uncommon in geopolitical prose; non-greedy regex still works |
| Multiple `<narrative_body>` tags in one response | Take first match; warn in trace |
| Old traces can't be replayed | Use Option B dual-parser for one release |
| Tag name collision with MDX components in prose | Editor prompt already prohibits JSX. Tag names are lowercase/unusual to avoid collision. |

## Effort estimate

- Parser helper + tests: 30 min
- Country editor (prompt + parser + 1 test): 45 min
- Country copyeditor + style editor: 30 min
- Regional triple: 45 min
- Executive triple: 30 min
- Watchlist triple: 30 min
- Pipeline validation runs between phases: 2-3 (each ~30 min wall time)
- Test sweep + fixes: 1 hour

Total: roughly half a day of focused work plus pipeline validation time.

## Acceptance criteria

- [ ] All 9 editorial agents emit XML-tagged output
- [ ] `extract_tag` helper handles multi-field outputs
- [ ] Dual parser (Option B) lets old traces replay
- [ ] Full pipeline run for one date completes with zero JSON parse failures in editor stages
- [ ] Existing tests pass (with fixture updates)
- [ ] `_unwrap_double_json` deleted (no longer needed)
- [ ] Editor prompts no longer have JSON `<output_format>` blocks

## Open questions

1. **Option A or B?** B is safer; depends on how often old briefs get reedited.
2. **Watchlist scope** — rarely invoked. Migrate now or defer indefinitely?
3. **Style editor dispatch** — `style_edit_prose` takes a dict of field names dynamically. Match input field names in output tags (recommended) or fix a tag set?

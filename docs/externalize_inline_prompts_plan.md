# Externalize Inline LLM Prompts — Implementation Plan

## Goal

All LLM system prompts and multi-line user-message templates used by the pipeline should live in `assets/prompts/*.md`. Execution code loads them via `load_prompt()` — **zero multi-line inline prompt string constants in Python**.

The correct pattern is already used by all 11 agents in `src/monitor/agents/`; the remaining inline-prompt problem is confined to the newsletter editors and two ledger modules.

---

## 1. Audit Table

10 inline prompts found across 4 files. All are triple-quoted constants used as `system=` or embedded into a system prompt.

| # | File:line | Constant | Description | Proposed file | ~lines |
|---|---|---|---|---|---|
| 1 | `src/monitor/newsletter/structured_editor.py:208` | `COUNTRY_EDITOR_SYSTEM` | Country-section structured editor system prompt (role/inputs/instructions/style/constraints/example/output_format) | `assets/prompts/country_editor.md` | 119 |
| 2 | `src/monitor/newsletter/structured_editor.py:329` | `REGIONAL_EDITOR_SYSTEM` | Regional-page structured editor system prompt (3 sub-tasks: regional_lead, gap_paragraphs, card_summary) | `assets/prompts/regional_editor.md` | 84 |
| 3 | `src/monitor/newsletter/structured_editor.py:415` | `EXECUTIVE_EDITOR_SYSTEM` | Executive-brief structured editor system prompt (weave items into unified essay) | `assets/prompts/executive_editor.md` | 86 |
| 4 | `src/monitor/newsletter/structured_editor.py:795` | `WATCHLIST_EDITOR_SYSTEM` | Watchlist structured editor system prompt | `assets/prompts/watchlist_structured_editor.md` | 53 |
| 5 | `src/monitor/newsletter/structured_editor.py:992` | `STYLE_EDITOR_SYSTEM` | Style editor system prompt for `style_edit_prose()` (final style-guide pass) | `assets/prompts/style_editor_structured.md` | 50 |
| 6 | `src/monitor/newsletter/structured_editor.py:116` | `NAMES_AND_TITLES_SECTION` | Names/titles convention block embedded into all 5 structured editor system prompts via `_build_system_prompt()` | `assets/prompts/style_names_and_titles.md` | 8 |
| 7 | `src/monitor/newsletter/structured_editor.py:537` | `_RETRY_INSTRUCTION` | Retry user-message appended when country editor returns wrong shape | `assets/prompts/country_editor_retry.md` | 5 |
| 8 | `src/monitor/newsletter/structured_copyeditor.py:52` | `COPYEDITOR_SYSTEM` | Structured copyeditor system prompt (abbreviations + prose polish) | `assets/prompts/structured_copyeditor.md` | 68 |
| 9 | `src/monitor/ledger/consolidation.py:32` | `CONSOLIDATION_SYSTEM_PROMPT` | Ledger consolidation system prompt (compress old weekly entries) | `assets/prompts/ledger_consolidation.md` | 24 |
| 10 | `src/monitor/ledger/initialize.py:144` | `INIT_SYSTEM_PROMPT` | Ledger cold-start initialization system prompt (posture summary + 5 category baselines from dossier) | `assets/prompts/ledger_initialize.md` | 32 |

### Explicitly excluded from migration

| File:line | What it is | Why excluded |
|---|---|---|
| `src/monitor/agents/executive.py:167` (`_build_executive_prompt`) | User-message template, f-string | Heavy runtime interpolation of regional_sections + ledger state. Out of scope per "f-string interpolation" exclusion. |
| `src/monitor/agents/country.py:230` (`_build_country_agent_prompt`) | User-message template, f-string | Heavy f-string interpolation of dossier text, ledger context, search vocabulary, language note. |
| `src/monitor/agents/country.py:321` (`_build_story_map_country_prompt`) | User-message template, f-string | Same — story_map_block + extracted_articles + dossier text. |
| `src/monitor/agents/regional.py:215` (`_build_regional_prompt`) | User-message template, f-string | Same — assembles per-country sections. |
| `src/monitor/ledger/initialize.py:185` (`_build_init_prompt`) | User-message template, f-string | Same — assembles actor list + dossier text. |
| `src/monitor/agents/editor.py:175,266,527,685,827` | `f"{task_prompt}\n\n---\n\n## Reference Style Guide\n\n{style_guide}"` | Template-assembly glue, not a prompt. The two pieces are already file-backed. |
| `src/monitor/newsletter/structured_editor.py:599` | Retry message composition | Once `_RETRY_INSTRUCTION` (item #7) is externalized the call site composes from a loaded value. |

### Already clean (verified)

- All 11 agent files in `src/monitor/agents/` (executive, triage, regional, country, devils_advocate, copyeditor, editor, government, story_map, expansion, __init__): every `system=...` site routes to `load_prompt(...)`. No inline triple-quoted system constants.
- `src/monitor/orchestrator.py`, `src/monitor/cli.py`: only docstrings.
- `src/monitor/newsletter/{assembly,renderer,publish,content_builder,content_models}.py`: deterministic code, no LLM calls.

---

## 2. Migration Order — 4 PRs

Each PR is self-contained. Each step is: (a) create `.md` file with byte-identical content, (b) rename old constant to `_OLD_*`, (c) add `NAME = load_prompt(...)`, (d) run byte-equivalence test, (e) move on.

### PR 1 — Ledger system prompts (smallest, lowest risk, establishes pattern)

Files touched: `src/monitor/ledger/consolidation.py`, `src/monitor/ledger/initialize.py`.

1. Create `assets/prompts/ledger_consolidation.md` from `CONSOLIDATION_SYSTEM_PROMPT` (`consolidation.py:32-54`). **The constant uses `"""\` and `\\` line-continuations.** The runtime value collapses these into a single block — the `.md` must match the post-Python-processing bytes. Use `print(repr(CONSOLIDATION_SYSTEM_PROMPT))` in a REPL to get the exact string.
2. Replace the constant definition with `CONSOLIDATION_SYSTEM_PROMPT = load_prompt("ledger_consolidation")`. Keep the constant name unchanged so call sites at lines 128 and 148 are unaffected. Add `load_prompt` to the import block at lines 19-26.
3. Same for `assets/prompts/ledger_initialize.md` from `INIT_SYSTEM_PROMPT` (`initialize.py:144-175`). Replace with `INIT_SYSTEM_PROMPT = load_prompt("ledger_initialize")`. Add `load_prompt` to import at lines 14-22.
4. Run `tests/monitor/test_consolidation.py` and `test_initialize.py`.

### PR 2 — Structured copyeditor

Files touched: `src/monitor/newsletter/structured_copyeditor.py`.

5. Create `assets/prompts/structured_copyeditor.md` from `COPYEDITOR_SYSTEM` (lines 52-119). Note the leading `\n` from `"""\n<role>...` — preserve exactly.
6. Replace constant with `COPYEDITOR_SYSTEM = load_prompt("structured_copyeditor")`.
7. Reused at line 133 inside `_copyedit_prose()` via `_build_system_prompt(COPYEDITOR_SYSTEM)` which is imported from `structured_editor.py`. No other call sites.
8. Smoke-test module import.

### PR 3 — Structured editor (the big one — 6 prompts in one file)

Files touched: `src/monitor/newsletter/structured_editor.py`.

**Sequence matters:** do `NAMES_AND_TITLES_SECTION` first because it is composed into the other 5 prompts via `_build_system_prompt()`.

9. Create `assets/prompts/style_names_and_titles.md` from `NAMES_AND_TITLES_SECTION` (lines 116-123). Replace constant with `load_prompt("style_names_and_titles")`. **Important:** the f-string at line 159 wraps the section in `<style_guide>` tags and concatenates with `_load_style_guide()` — whitespace at the boundaries matters. The byte-equivalence test must cover the composed result, not just the leaf.
10. Create `assets/prompts/country_editor.md` from `COUNTRY_EDITOR_SYSTEM` (208-326). Replace constant. Consumed at line 556.
11. Create `assets/prompts/regional_editor.md` from `REGIONAL_EDITOR_SYSTEM` (329-412). Replace constant. Consumed at line 664.
12. Create `assets/prompts/executive_editor.md` from `EXECUTIVE_EDITOR_SYSTEM` (415-500). Replace constant. Consumed at line 743.
13. Create `assets/prompts/country_editor_retry.md` from `_RETRY_INSTRUCTION` (537-541). Replace with `_RETRY_INSTRUCTION = load_prompt("country_editor_retry")`. Consumed at line 600 in retry-message composition.
14. Create `assets/prompts/watchlist_structured_editor.md` from `WATCHLIST_EDITOR_SYSTEM` (795-847). Replace constant. Consumed at line 872.
15. Create `assets/prompts/style_editor_structured.md` from `STYLE_EDITOR_SYSTEM` (992-1041). Replace constant. Consumed at line 1054.
16. Run `tests/monitor/test_narrative_sanitizer.py`, `test_newsletter.py`, `test_run_recorder.py`.

**Tricky points for PR 3:**
- All 5 full system prompts share the `\n<role>...</role>` opening pattern. The runtime value starts with `\n` and ends without trailing newline. Pick one convention (include the leading `\n` or strip it) and enforce it with the byte test.
- `NAMES_AND_TITLES_SECTION` is the only one without the `<role>` opening — starts immediately with `####`. Its trailing `\n` matters for the concatenation at line 159.
- `_RETRY_INSTRUCTION` is used inside an f-string at line 600 — after migration the f-string is unchanged; only the constant's source changes.
- The example_input/example_output blocks inside `COUNTRY_EDITOR_SYSTEM` and `EXECUTIVE_EDITOR_SYSTEM` contain escaped Unicode (`\u201c`, `\u2019`) and escaped newlines. The Python literal processes one level of escaping; the `.md` must contain the **post-processing** bytes (real Unicode quotes, real `\n\n` sequences).

### PR 4 — Verification cleanup

17. Delete `tests/monitor/test_prompt_migration.py` (the temporary byte-equivalence test module).
18. Delete all `_OLD_*` constant aliases.
19. Confirm `cli.py:179` `record_prompt_hashes()` picks up the 10 new files automatically (no code change needed).
20. Optional: add a one-line note to `assets/prompts/README.md` (if one exists) documenting the "all prompts live here" convention.

---

## 3. Risks

| # | Risk | Likelihood | Mitigation |
|---|---|---|---|
| R1 | **Hash drift breaks resume detection.** After migration, 10 new hashes appear in the manifest. `check_prompt_changes()` reports new files as `<name> (new)` — non-fatal, but prints a warning on the first resume after the cutover. | Low | Document in the PR description. Optionally run a fresh (non-resume) full run after the cutover to clear the warning for subsequent comparisons. |
| R2 | **`assets/prompts/style_editor.md` has dual purpose.** Pre-existing: loaded as a system prompt at `agents/editor.py:825` AND read raw as a style-guide block embedded inside three other prompts (`structured_editor.py:130-135`, `structured_copyeditor.py:44-48`). Picking the name `style_editor_structured.md` (item #5) keeps the new prompt distinct, but the existing fragility is unchanged. | Medium (pre-existing) | Out of scope for this refactor. Add a comment in `_load_style_guide()` flagging the dual usage. Follow-up PR: split into `style_guide.md` (raw guide content) + `style_editor.md` (system prompt that includes the guide via `{{STYLE_GUIDE}}`). |
| R3 | **Byte-equivalence is fragile.** A single trailing newline, BOM, smart-quote, or escaped-character difference shifts the SHA-256 hash and changes the LLM output. | High without test, low with it | **Mandatory:** temporary `assert load_prompt("X") == _OLD_CONSTANT` test before deleting the constant. Run on every step of every PR. |
| R4 | **`NAMES_AND_TITLES_SECTION` is composed inside an f-string** at `structured_editor.py:159`. Boundary whitespace is sensitive. | Medium | Byte-equivalence test must check the **composed result**, not just the leaf prompt. Add a second assertion that builds the composed prompt both ways and compares. |
| R5 | **Per-process prompt cache may mask file changes during dev.** `load_prompt()` caches by name in module-global `_prompt_cache`. | Low | Run the byte test as `pytest` in a fresh process, not interactively. |
| R6 | **Existing CI / automation matching prompt text.** Verified: no tests reference any of the 10 inline constants; no CI grep. `tests/monitor/test_run_recorder.py::TestPromptHashing` constructs a temp prompts dir so it's unaffected. | Low | Already verified. |
| R7 | **Backslash line-continuation** in `consolidation.py` and `initialize.py` (`"""\` and lines ending with `\`). The runtime value collapses continuations into a single block with no internal newline at the continuation points. | High without test | Use `print(repr(CONSTANT))` in a REPL to capture the runtime value. Byte test catches any mismatch. |
| R8 | **PR 3's six prompts are coupled** — all in one file, all use `_build_system_prompt()`, all share `NAMES_AND_TITLES_SECTION`. | Medium | Sequence within PR 3: do `NAMES_AND_TITLES_SECTION` first so downstream prompts can be tested against the new path. Then country → regional → executive → retry → watchlist → style. Byte test after each. |

---

## 4. Verification Plan

### Phase A — Per-prompt byte equivalence (during refactor)

Add a temporary test file `tests/monitor/test_prompt_migration.py` (deleted in PR 4). For each prompt, the migration step is:

1. Create the `.md` file.
2. **Rename** the existing constant to `_OLD_<NAME>`.
3. Add `<NAME> = load_prompt("…")`.
4. Add a byte-equivalence test:

```python
from src.monitor.config import load_prompt
from src.monitor.newsletter import structured_editor as se

def test_country_editor_byte_equivalent():
    assert load_prompt("country_editor") == se._OLD_COUNTRY_EDITOR_SYSTEM

def test_country_editor_composed_equivalent():
    # Guards against whitespace drift at f-string boundaries
    composed_new = se._build_system_prompt(load_prompt("country_editor"))
    composed_old = se._build_system_prompt(se._OLD_COUNTRY_EDITOR_SYSTEM)
    assert composed_new == composed_old
```

5. Run `pytest tests/monitor/test_prompt_migration.py -k <name> -x`.
6. In PR 4: delete all `_OLD_*` aliases and the test module.

### Phase B — Hash continuity check

After PR 3 completes and aliases are deleted:

1. Capture the new hash set: `python -c "from src.monitor.run_recorder import RunRecorder; r=RunRecorder(); print(r.record_prompt_hashes())"`
2. Confirm count went from 15 to 25 (15 existing + 10 new). No existing hash should change — spot-check `executive.md`, `regional_synthesis.md`, `country_agent.md` against hashes captured before the refactor.

### Phase C — Functional smoke test

1. `pytest tests/monitor/test_run_recorder.py::TestPromptHashing -v`
2. `pytest tests/monitor/test_consolidation.py test_initialize.py test_narrative_sanitizer.py test_newsletter.py -v`
3. Smoke import: `python -c "import src.monitor.cli, src.monitor.newsletter.structured_editor, src.monitor.newsletter.structured_copyeditor, src.monitor.ledger.consolidation, src.monitor.ledger.initialize"` — confirms no `FileNotFoundError` from `load_prompt` at module load (file-level `FOO = load_prompt(...)` executes during import).

### Phase D — Manifest comparison against a real run

Pick the most recent run's `manifest.json` from `updated_architecture/`. After the refactor, on a fresh run of the same `end_date`, compare the hash set: every old key must match exactly; the 10 new keys should be additions only. Any changed old hash means an existing `.md` was accidentally edited — `git diff assets/prompts/` will reveal it.

---

## 5. Recommendations

1. **Stay flat — no subdirectories.** 25 total files fit comfortably. A subdir like `assets/prompts/editor/` would break the `load_prompt(name)` convention (would need to handle paths). Not worth the churn.

2. **Naming convention disambiguators.** Three filenames are already taken by different prompts used by the older `agents/editor.py` and `agents/copyeditor.py` paths:
   - Existing `style_editor.md`, `copyeditor.md`, `watchlist_editor.md` are owned by the legacy editor path.
   - New structured-editor variants use `_structured` / `structured_` qualifiers.
   - Ledger prompts use the `ledger_*` prefix to make ownership explicit.
   - `style_names_and_titles.md` uses `style_*` prefix to group with related style assets.
   - `country_editor_retry.md` ties to the editor it retries.

3. **Long-term cleanup — `style_editor.md` dual usage** (pre-existing R2). Out of scope here but flag as follow-up: split into `style_guide.md` (raw content) + `style_editor.md` (system prompt that includes it via `{{STYLE_GUIDE}}`). Removes the magic file-path reads in `_load_style_guide()` helpers across three modules.

4. **Long-term cleanup — f-string user-message templates.** The five `_build_*_prompt()` helpers construct user messages by string-formatting runtime data. Out of scope here, but they're 40+ line templates with embedded headings and instructions. A future `{{INTERPOLATION}}` extension of `load_prompt()` would let these move to files too.

5. **`record_prompt_hashes()` is already correct for the post-migration world.** It globs `PROMPTS_DIR/*.md`, so the 10 new files automatically join the hash manifest. No code change needed.

---

## Critical Files

- `src/monitor/newsletter/structured_editor.py` — 6 of 10 prompts live here
- `src/monitor/newsletter/structured_copyeditor.py` — 1 prompt
- `src/monitor/ledger/consolidation.py` — 1 prompt
- `src/monitor/ledger/initialize.py` — 1 prompt
- `src/monitor/config.py` — the `load_prompt()` helper (read-only reference)

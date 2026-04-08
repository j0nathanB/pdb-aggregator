# Prompt Comparison — Old vs New (Round 2)

## Prompt Sizes (inline only, before style guide)

| Prompt | Old | New |
|--------|-----|-----|
| Country editor | 12592 chars (shared) | 8117 chars |
| Regional editor | 12592 chars (shared) | 1657 chars |
| Executive editor | 12592 chars (shared) | 3220 chars |
| Copyeditor | 17985 chars | 3997 chars |
| Style editor | (embedded in old pipeline) | 1141 chars |

## Key Changes in Round 2

1. **Country editor** — ported full style rules (plain words, active voice, cut ruthlessly, etc.), added raw_analysis field documentation, kept Ukraine example
2. **Executive editor** — added BAD/GOOD worked example from old pipeline
3. **Regional editor** — instructs 3-5 substantial paragraphs, references cross_cutting_dynamics
4. **Copyeditor** — ported full naming conventions (per old copyeditor.md), abbreviation rules, Orwell's rules, all style directives
5. **Style editor** — unchanged (focuses purely on style compliance)

## Old vs New — What Changed

The old pipeline used ONE prompt (editor.md, 5.6K chars) for all three editor types, differentiated by user message framing. The new pipeline has specialized prompts per editor type.

The old copyeditor prompt (copyeditor.md, 8.5K chars) was very detailed on naming conventions. The new copyeditor prompt now matches that depth.

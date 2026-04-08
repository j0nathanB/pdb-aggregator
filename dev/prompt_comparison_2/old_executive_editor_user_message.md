# Old Executive Editor — User Message Framing

**System prompt:** Same `editor.md` as country/regional (see `old_editor_prompt.md`)

**User message** (built inline in `run_executive_editor()`, editor.py lines 543-587):

```
## ASSEMBLED SECTION

This is the **executive brief** — the top-level analytical summary of the week. 
It was assembled mechanically as a series of separate items with ### headings. 
Your job is to weave these into a unified analytical essay:

- Drop the ### item headings.
- Merge items that make related points.
- Reorder for narrative flow — lead with the most important development.
- Add transitions so the brief reads as a coherent story, not disconnected observations.
- Eliminate redundancy across items.
- If evidence is thin, say so in plain language — do not include pipeline metadata like 
  '(confidence: contested)' parentheticals.
- The result should be 3-5 paragraphs of flowing prose.

### Worked example

**BAD** (jargon-heavy, abstract, repetitive):

> Allied countries are developing fundamentally incompatible strategies for managing 
> alliance burden-sharing and strategic commitments, fragmenting traditional coordination 
> mechanisms along regional lines. Czech Republic explicitly rejected NATO 3.5% spending 
> targets while Romania secured €16.6 billion in EU defense funding and Finland targets 
> 3% GDP by 2029. This represents structural evolution of alliance systems beyond 
> traditional coordination mechanisms — when allies cannot agree on burden-sharing 
> fundamentals or strategic priorities, the alliance becomes a framework for managing 
> disagreement rather than coordinating action.

**GOOD** (concrete, sequential, readable):

> Allied countries are splitting over the basics of burden-sharing, and the splits are 
> hardening along regional lines.
>
> In Europe, the Czech Republic has rejected NATO's 3.5% spending target outright, while 
> Romania secured €16.6 billion in EU defence funding and Finland aims for 3% of GDP by 
> 2029. France, Germany and Spain are each articulating versions of strategic autonomy — 
> separately, and without American participation. They agree on the direction but not the 
> details, and Washington is not in the room.
>
> In Asia, the pressures point in opposite directions. Japan is deepening its operational 
> planning for a Taiwan contingency. South Korea is pursuing what it calls a 'full-scale 
> restoration' of relations with China. Both are responding to American unreliability, but 
> their answers are incompatible.

Notice: short sentences, concrete facts first, plain language, regional grouping with 
narrative flow, no jargon like 'institutional logic' or 'strategic incoherence'. 
Say what is happening, who is doing it, why it matters, and stop.

---

## YOUR INPUT

{assembled_brief — the mechanically rendered ### items}

---

## RAW ANALYSIS

```json
{briefing_items serialized as JSON array}
```
```

**Key difference from new:** The old executive editor received the assembled markdown 
(the rendered ### items) as its primary input, with the raw JSON as supplementary context. 
The new executive editor receives ONLY the JSON items array — no pre-rendered markdown.

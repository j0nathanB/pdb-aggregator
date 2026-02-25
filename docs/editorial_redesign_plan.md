# Editorial Redesign: AP Wire → Intelligence Briefing

Plan to transform the brief overview page from AP wire copy into a
policymaker-oriented intelligence product. Individual dossier pages
stay AP-style as source material.

## Target Output Structure

```
# The Middle Powers Monitor
## Week of February 9, 2026

Editorial lede (2-3 sentences with attitude, names the top shifts)

---

## This Week's Signal (2-3 elevated stories)

### 🇩🇪🇫🇷 Merz Opens Nuclear Deterrence Talks with Macron

**BLUF:** One-sentence bottom line.

- Analytical bullet with context (2-3 bullets)
- ...

**Assessment:** Forward-looking editorial judgment. "Watch whether..."

---

## Regional Briefs (per-leader condensed bullets)

### North America

#### 🇨🇦 Canada / Mark Carney

- **Bolded topic:** 1-2 sentence analytical summary
- **Another topic:** ...

**Between the Lines:** Sharp, specific, forward-looking.

---

## Also Tracking (one-liners for minor items)

- **Canada:** Fish conservation concern amid port expansion.
- **Uruguay:** Orsi tested negative for chickenpox after China trip.
```

---

## Current Output vs. Target

### Voice & Tone

| Current | Target |
|---------|--------|
| AP wire: "said", "stated", neutral | Intelligence analyst: "Watch whether...", pointed judgments |
| No editorializing, no speculation | Assessments stated as editorial voice |
| Dateline leads: "OTTAWA, Canada —" | No datelines on overview. Concise analytical bullets |
| Every claim attributed to a source | Assessments as editorial voice; sources on dossier pages |

### Page Structure

| Current | Target |
|---------|--------|
| Exec summary (blockquote) | 2-3 sentence editorial lede with attitude |
| Top Stories (full AP narratives) | "This Week's Signal" — 2-3 stories with BLUF + Assessment |
| Regional Briefs (per-leader, story links + first sentence) | Regional Briefs — condensed analytical bullets per leader + BTL |
| *(nothing)* | "Also Tracking" — minor items as one-liners |

### Per-Leader Treatment

| Current | Target |
|---------|--------|
| Full AP stories (3-4 sentences, dateline, attribution) | Bolded topic + 1-2 sentence analytical bullet |
| Inline source citations | No citations on overview (available on dossier page) |
| Between the Lines (generic observations) | BTL with sharp, specific, "watch for" language |

### Story Triage (new capability)

The current pipeline treats all stories roughly equally. The target requires a
triage step that doesn't exist today:

- **Signal** (2-3 stories): Deep BLUF + bullets + Assessment. Cross-leader or structurally significant.
- **Brief** (most stories): 1-2 analytical bullets per leader in Regional Briefs.
- **Also Tracking** (minor): One-line mentions. Fish, chickenpox, gold medals.

---

## Changes Required

### 1. New aggregate system prompt — intelligence analyst voice

**File:** `src/agents/aggregate_builder.py`
**What:** Replace `AGGREGATE_SYSTEM` (AP Senior Editor) with an intelligence
analyst persona for the overview page. Keep the AP prompt for dossier-level work.

Current opening:
```
You are a Senior Editor for the Associated Press compiling a global leadership
intelligence briefing. Your writing is objective, detached, and authoritative.
```

New direction:
```
You are a senior intelligence analyst writing a weekly leadership briefing for
policymakers. Your voice is analytical, direct, and forward-looking. You make
assessments. You distinguish signal from noise.

Your output must:
- Lead with the "so what" — why this matters, not just what happened
- Use BLUF (Bottom Line Up Front) for major stories
- Make assessments: "Watch whether...", "The question is...", "This signals..."
- Distinguish between structural shifts and routine activity
- Name patterns across leaders and regions
- Be specific about what to watch next
```

### 2. New "Signal selection + triage" prompt

**File:** `src/agents/aggregate_builder.py` (new method)
**What:** After cross-leader synthesis, a new prompt that takes all stories +
dossiers and produces:

1. **Signal picks** (2-3): Which stories are structurally significant? Write
   BLUF + 2-3 analytical bullets + Assessment for each.
2. **Regional brief bullets**: For each leader, condense their stories into
   2-3 bolded analytical bullets + BTL.
3. **Also Tracking**: Which items are minor but worth noting? One line each.

This replaces the current P7c (global BTL + exec summary) with a much larger
editorial role. Could be a single prompt or broken into two (triage → write).

### 3. Sharpen BTL prompts (per-leader and aggregate)

**Files:** `src/agents/dossier_builder.py` (P6e), `src/agents/aggregate_builder.py` (P7c)
**What:** Shift from generic observations to pointed assessments.

Current BTL instruction:
```
- Identify 2-4 themes or patterns not immediately evident from individual stories
- Things to watch as events develop
- Grounded in the week's content, not general trajectory speculation
```

New direction:
```
- Make a judgment: what is this leader actually doing beneath the surface?
- Name the tension or trade-off they face
- Identify the specific thing to watch: a vote, a meeting, a deadline, a reaction
- Use "Watch whether...", "The question is...", "Expect..."
- Be specific enough that a reader could verify your assessment next week
```

### 4. Add `brief_bullet` to synthesis output

**File:** `src/agents/dossier_builder.py` (P6b)
**What:** Add a field to the synthesis JSON output — a 1-2 sentence analytical
summary for the overview page, separate from the full AP narrative.

Current return schema:
```json
{
    "title": "...",
    "narrative": "AP-style 3-4 sentences with dateline...",
    "scope": "...",
    "event_type": "...",
    ...
}
```

Add:
```json
{
    "title": "...",
    "narrative": "AP-style 3-4 sentences with dateline...",
    "brief_bullet": "1-2 sentence analytical summary for overview page, no dateline, no attribution",
    ...
}
```

This lets the overview page use `brief_bullet` while the dossier page uses
`narrative`. The full AP story remains the canonical source material.

### 5. Rewrite overview page template

**File:** `src/persistence.py` — `_generate_markdown()`
**What:** New page structure.

Current flow:
```
frontmatter → exec summary blockquote → Top Stories (full AP) → Regional Briefs (story links)
```

New flow:
```
frontmatter → editorial lede → This Week's Signal (BLUF/Assessment blocks)
→ Regional Briefs (bullet summaries per leader + BTL) → Also Tracking
```

This is a `_generate_markdown()` rewrite, plus corresponding changes in
`scripts/migrate_to_mintlify.py` `generate_mintlify_overview()`.

### 6. Keep dossier pages as-is

Individual dossier pages (`_generate_dossier_markdown()`) stay AP-style with
full narratives, datelines, source citations. They serve as the detailed
source material that the overview page summarizes analytically.

---

## Implementation Order

1. **P6b: Add `brief_bullet` field** to synthesis prompt + parse it in dossier builder.
   Low risk, additive. Full AP stories unaffected.

2. **P6e: Sharpen BTL prompt** for per-leader assessments.
   Moderate change to editorial voice. Test on one leader.

3. **New aggregate prompt: Signal triage.** This is the biggest piece —
   selecting Signal stories, writing BLUF/Assessment, condensing Regional
   Briefs, producing Also Tracking. Build and test standalone before integrating.

4. **New aggregate system prompt.** Replace AP editor voice with analyst voice
   for the overview page only.

5. **`_generate_markdown()` rewrite.** Wire up the new data structures
   (Signal stories, brief bullets, Also Tracking) into the overview .mdx template.

6. **Run side-by-side.** Generate both old and new format for a few weeks.
   Compare quality before cutting over.

---

## What Stays the Same

- **Dossier pages**: Full AP stories, datelines, source citations. Unchanged.
- **Source fetching, translation, classification, clustering**: All upstream
  pipeline stages stay identical. The editorial voice change only affects
  the last-mile synthesis and page generation.
- **Email digest**: Separate prompt, already has its own condensed voice.
  May eventually adopt the new analytical style but not in this change.
- **docs.json / navigation / archives**: Structural plumbing unchanged.

## Risks

- **Assessment quality**: The AP wire style is a safety net — neutral voice
  can't be wrong. Analytical assessments can be wrong, and wrong assessments
  sent to policymakers are worse than no assessments. Mitigate with the
  human review gate (PR-based flow).
- **Prompt complexity**: The Signal triage prompt is doing a lot — selection,
  BLUF writing, bullet condensation, Also Tracking triage. May need to be
  split into two calls if output quality degrades.
- **Token cost**: The triage step adds one more Opus call per brief. Marginal
  cost ~$1-2/run.

# Weekly Pipeline — Runtime Prompts & Running Picture Schema

## Architecture Overview

Each weekly cycle processes leaders in two phases:

**Phase 1: Per-Leader Analysis** (runs once per leader, parallelizable)
- Input: Country dossier + Leader profile + Running picture + This week's events
- Output: Leader analytical assessment + Running picture entry
- Two tasks in a single LLM call to manage cost

**Phase 2: Aggregate Synthesis** (runs once per cycle, after all leaders processed)
- Input: All leader analytical assessments from Phase 1
- Output: Reader-facing weekly brief
- Single LLM call

---

## Running Analytical Picture — Schema

One file per leader, append-only. The pipeline loads the most recent 10 entries
(~10 weeks of coverage) at runtime. Older entries rotate into an archive that
can be queried if needed but is not loaded by default.

Each weekly entry follows this structure:

```markdown
---
leader: {{LEADER_NAME}}
country: {{COUNTRY}}
week_of: {{YYYY-MM-DD}}  # Monday of the reporting week
generated_at: {{ISO_TIMESTAMP}}
event_count: {{N}}  # number of classified events this week
source_count: {{N}}  # number of articles processed
---

### Activity Level
[ONE OF: High / Moderate / Low / Quiet]
[One sentence characterizing the week — e.g., "Dominated by NATO summit
preparations; no significant domestic developments."]

### Key Actions
[Numbered list of significant actions the leader took this week. Each entry
should be a concrete, verifiable action — not a media narrative or analyst
interpretation. Include date where known.]

1. [DATE] [ACTION]: [Brief description of what the leader actually did].
   Source: [primary source attribution]
   Significance: [One sentence on why this matters — reference structural
   claims or profile claims by number where relevant]

2. ...

### Commitments & Positions
[New commitments made, positions taken, or existing positions reinforced
or shifted. These accumulate over time and allow the pipeline to detect
when a leader contradicts or abandons a prior commitment.]

- [COMMITMENT/POSITION]: [What was said/pledged, to whom, in what context]
  Status: [NEW / REINFORCED / SHIFTED FROM [previous position] / WALKED BACK]

### Relationships
[Significant interactions with other tracked leaders or important external
actors. Focus on observable interactions, not inferred relationship states.]

- [INTERACTION]: [With whom, format (bilateral meeting / phone call / joint
  statement / multilateral sidebar), topic, observable outcome]
  Assessment: [What this interaction suggests about the relationship trajectory]

### Domestic Political Position
[Any changes to the leader's domestic political standing this week. Only
include if something actually changed — do not repeat the baseline from
the leader profile.]

- [DEVELOPMENT]: [What changed and why it matters for foreign policy capacity]

### Developing Threads
[Situations that are unresolved and should be monitored in coming weeks.
Each thread should specify what to watch for.]

- [THREAD]: [Current status]
  Watch for: [Specific observable event that would indicate development]
  Originated: [Week this thread first appeared]

### Structural Claim Check
[Flag any structural claims (from country dossier) or profile claims (from
leader profile) that were CHALLENGED, REINFORCED, or made NEWLY RELEVANT
by this week's events.]

- [CLAIM TYPE + NUMBER]: [CHALLENGED / REINFORCED / NEWLY RELEVANT]
  Evidence: [What happened that affects this claim]
  Recommendation: [If challenged — does the source document need refresh?]

### Analytical Notes
[1-3 sentences of analyst-level observation that don't fit the structured
fields above. These are the "between the lines" observations — but grounded
in the accumulated context rather than generated from this week's events
alone. These should reference the running picture's trajectory, not just
this week's data.]
```

### Running Picture Maintenance Rules

**Developing Threads** carry forward automatically. If a thread from a
previous week is not resolved and not mentioned in this week's events,
it should still appear in the current entry with its status unchanged
and "Watch for" criteria intact. Threads are only removed when:
- Resolved (note the resolution and date)
- Superseded by a new development (note what replaced it)
- Stale after 8+ weeks with no development (note that monitoring is
  being deprioritized and why)

**Commitments & Positions** are cumulative across the running picture.
The pipeline should be able to scan all entries in the window and
construct a current ledger of active commitments. When a commitment
is walked back or contradicted, the entry should reference the original
commitment's date.

---

## Phase 1: Per-Leader Analysis Prompt

This prompt runs once per leader per weekly cycle. It produces two
outputs in a single LLM call: an analytical assessment (used as input
to Phase 2) and a running picture entry (appended to the leader's
running picture file).

### System Prompt

```
You are an intelligence analyst producing a weekly analytical assessment
of a national leader's significant actions. You work within a structured
analytical framework that layers three types of context:

1. STRUCTURAL CONTEXT (Country Dossier): Persistent features of the
   country — geography, institutions, economy, history — that constrain
   any leader's behavior. Updated quarterly. Contains numbered
   STRUCTURAL CLAIMS that represent falsifiable assertions about
   persistent features.

2. LEADER CONTEXT (Leader Profile): How this specific individual
   exercises power — decision-making patterns, relationships, political
   positioning, crisis behavior. Updated on major political shifts.
   Contains numbered PROFILE CLAIMS that represent observable behavioral
   patterns.

3. RUNNING CONTEXT (Running Analytical Picture): Cumulative record of
   this leader's actions, commitments, and developing situations over
   recent weeks. Updated weekly. Shows trajectory.

4. THIS WEEK'S EVENTS: Classified news events from the current
   reporting period. Ephemeral — replaced each cycle.

Your analytical method:
- Compare this week's events against all three context layers
- Determine whether events represent CONTINUITY (expected given context)
  or DEVIATION (unexpected, requires explanation)
- For deviations, assess severity: TACTICAL ADJUSTMENT (minor, within
  normal parameters) / SIGNIFICANT SHIFT (materially changes the
  analytical picture) / POTENTIAL STRUCTURAL CHANGE (challenges
  fundamental assumptions in the dossier or profile)
- Ground every assessment in specific evidence and specific context
  references (cite structural claims and profile claims by number)
- Maintain rigorous epistemic standards: distinguish between what
  happened (observable), what it likely means (assessment), and what
  might happen next (projection, always flagged as such)

You will produce TWO outputs:

OUTPUT 1 — ANALYTICAL ASSESSMENT
A structured analytical product that will be read by another LLM in
Phase 2 to produce an aggregate cross-leader brief. Write for an
analytical consumer, not a general reader. Be precise, cite your
reasoning, and flag uncertainty.

OUTPUT 2 — RUNNING PICTURE ENTRY
A structured entry following the Running Analytical Picture schema
that will be appended to this leader's running context file and used
as context in future weekly cycles. This must be concise, structured,
and optimized for future LLM consumption — not for human reading.
```

### User Prompt Template

```
## STRUCTURAL CONTEXT: {{COUNTRY}}

{{COUNTRY_DOSSIER_CONTENT}}

---

## LEADER CONTEXT: {{LEADER_NAME}}

{{LEADER_PROFILE_CONTENT}}

---

## RUNNING CONTEXT: {{LEADER_NAME}} — Recent Weeks

{{RUNNING_PICTURE_ENTRIES}}  <!-- Last 10 weekly entries -->

---

## THIS WEEK'S EVENTS: {{LEADER_NAME}}
Reporting period: {{DATE_START}} to {{DATE_END}}

{{CLASSIFIED_EVENTS}}

---

## INSTRUCTIONS

Produce two outputs for {{LEADER_NAME}} ({{TITLE}}, {{COUNTRY}}) based
on the context and events above.

### OUTPUT 1: ANALYTICAL ASSESSMENT

Structure your assessment as follows:

**ACTIVITY SUMMARY**
One paragraph characterizing this leader's week — what they did,
what it means, and where it fits in the running trajectory.

**EVENT ANALYSIS**
For each significant event this week (skip routine/low-significance
events), provide:

[EVENT]: [Brief description]
- Context: Which structural claims and/or profile claims are relevant?
  Cite by number.
- Running picture fit: Is this part of a developing thread from
  previous weeks? Does it continue, escalate, reverse, or resolve
  a prior trajectory?
- Assessment: CONTINUITY or DEVIATION? If deviation, what level
  (tactical adjustment / significant shift / potential structural
  change)?
- Forward implications: What does this event create going forward?
  New commitments, foreclosed options, opened possibilities?
  [Flag as PROJECTION]

**CROSS-LEADER RELEVANCE**
Identify any events or developments this week that are relevant to
other monitored leaders. For each:
- Which leader(s) are affected?
- What is the connection?
- What should the aggregate brief highlight about this intersection?

**BETWEEN THE LINES**
1-3 analytical observations that emerge from reading this week's
events against the full context stack. These should be things that
are NOT obvious from the events alone — insights that require the
structural context, leader profile, or running trajectory to see.
Each observation must reference specific context (claim numbers,
running picture entries, or profile sections) that supports it.

**ATTENTION FLAGS**
List anything that warrants elevated monitoring in coming weeks.
Distinguish between:
- WATCH: Developing situation, monitor for further signals
- ALERT: Significant deviation from baseline, may require profile
  or dossier reassessment
- STRUCTURAL: Event challenges a foundational assumption in the
  country dossier or leader profile

### OUTPUT 2: RUNNING PICTURE ENTRY

Produce a structured entry following the Running Analytical Picture
schema. This entry will be appended to the running context file.
Ensure:
- Key Actions are concrete and verifiable, not interpretive
- Commitments reference prior commitments where relevant
- Developing Threads carry forward unresolved threads from previous
  entries (check the running context above)
- Structural Claim Checks flag any claims challenged or reinforced
- Analytical Notes draw on the full trajectory, not just this week
```

---

## Phase 2: Aggregate Synthesis Prompt

This prompt runs once per cycle after all per-leader analyses are
complete. It produces the reader-facing weekly brief.

### System Prompt

```
You are the senior editor of the Middle Powers Monitor, an intelligence
publication that tracks democratic coordination among middle power
nations. You have received analytical assessments for all monitored
leaders this week, each produced by an analyst with deep context on
that specific leader.

Your task is to synthesize these per-leader assessments into a single,
coherent weekly brief for an audience of educated generalists — people
who are informed about world affairs but do not have specialist knowledge
of any particular country.

Your editorial principles:
- LEAD WITH SIGNIFICANCE, NOT GEOGRAPHY. The brief should be organized
  around the most important developments and cross-leader patterns,
  not structured as a country-by-country tour.
- SURFACE CONNECTIONS the individual analysts may not have flagged.
  When multiple leaders' actions this week are responding to the same
  external pressure, coordinating on the same initiative, or pulling
  in different directions on the same issue — make that visible.
- DISTINGUISH SIGNAL FROM NOISE. Not every leader does something
  significant every week. Leaders with quiet weeks should get minimal
  or no coverage rather than inflated treatment. Readers should be
  able to scan the brief and immediately identify what matters.
- MAINTAIN ANALYTICAL DEPTH WITHOUT JARGON. The per-leader assessments
  use structural claims, profile claims, and analytical terminology.
  The brief should convey the analytical insight in accessible language
  without the scaffolding.
- RESPECT READER TIME. This publication succeeds when readers can
  extract value in 5-7 minutes but have the option to read deeper.
  Structure accordingly.
```

### User Prompt Template

```
## PER-LEADER ANALYTICAL ASSESSMENTS

{{FOR_EACH_LEADER}}
### {{LEADER_NAME}} ({{TITLE}}, {{COUNTRY}})
{{ANALYTICAL_ASSESSMENT_OUTPUT_1}}
{{END_FOR_EACH}}

---

## THIS WEEK'S BRIEF

Produce the Middle Powers Monitor weekly brief for the week of
{{DATE_START}} to {{DATE_END}}.

Structure the brief as follows:

**EXECUTIVE SUMMARY**
3-5 sentences capturing the week's most significant developments
across all monitored leaders. What happened, why it matters, and
what it signals. A reader who reads only this paragraph should
come away with the essential picture.

**[LEAD STORY / STORIES]**
The 1-3 most significant developments this week. These may be
single-leader stories with broad implications or multi-leader
stories where coordination, conflict, or parallel action is the
story. For each:
- What happened (concrete, sourced)
- Why it matters (analytical context — but expressed in accessible
  language, not in terms of structural claims)
- What to watch for next

**NOTABLE DEVELOPMENTS**
3-6 shorter items covering significant developments that don't
warrant full lead treatment. Each should be 2-4 sentences:
what happened and why it's worth noting.

**BETWEEN THE LINES**
2-4 analytical observations that emerge from looking across all
leaders' weeks simultaneously. These are the cross-leader patterns,
the non-obvious connections, the developing trajectories that
individual country coverage would miss. Each should be grounded
in specific developments from this week but illuminated by
structural context.

**QUIET WATCH**
Brief mention of monitored leaders with quiet weeks, noting any
developing threads from previous weeks that remain active even
though nothing new occurred this week. This section tells readers
"we're still watching these situations" without pretending something
happened when it didn't. Can be omitted if all leaders had active
weeks.

**METHODOLOGY NOTE**
Brief, standardized disclosure: number of leaders monitored, number
of sources processed, date range, and any notable source gaps or
limitations for this week's coverage.
```

---

## Implementation Notes

### Token Budget Estimate (Per-Leader, Phase 1)

| Component | Estimated Tokens |
|-----------|-----------------|
| Country dossier | 8,000–12,000 |
| Leader profile | 3,000–5,000 |
| Running picture (10 weeks) | 4,000–8,000 |
| This week's events | 2,000–6,000 |
| System + user prompt | 2,000–3,000 |
| **Total input** | **~19,000–34,000** |
| Output (assessment + entry) | 2,000–4,000 |

This fits comfortably within Claude Sonnet's context window. If country
dossiers run long, the STRUCTURAL CLAIMS blocks can be loaded in full
while prose sections are truncated, with a note to the LLM that full
prose is available but claims are the primary reference.

### Token Budget Estimate (Phase 2, Aggregate)

| Component | Estimated Tokens |
|-----------|-----------------|
| 15 leader assessments @ ~2,000 each | ~30,000 |
| System + user prompt | 2,000–3,000 |
| **Total input** | **~32,000–33,000** |
| Output (brief) | 3,000–6,000 |

Also fits within context limits. If the leader count expands beyond
~25, consider splitting Phase 2 into regional batches with a final
synthesis pass.

### Cost Estimate (Per Weekly Cycle)

At 15 leaders:
- Phase 1: 15 LLM calls (parallelizable)
- Phase 2: 1 LLM call
- Total: 16 LLM calls per cycle

Using Claude Sonnet with estimated input/output volumes:
- Phase 1: ~15 × (25k input + 3k output) = ~375k input + 45k output
- Phase 2: ~1 × (32k input + 5k output) = ~32k input + 5k output
- **Total: ~407k input tokens + 50k output tokens per cycle**

### File Management

**Running picture files:**
- Location: one file per leader, e.g., `running_picture/macron.md`
- Append new entries to the top (most recent first)
- Pipeline reads the first 10 entries at runtime
- Monthly maintenance job rotates entries older than 12 weeks to
  `running_picture/archive/macron_archive.md`

**Analytical assessments:**
- Ephemeral within each cycle — produced by Phase 1, consumed by Phase 2
- Optionally archived for debugging and quality review

**Structural claim refresh flags:**
- When Phase 1 produces a STRUCTURAL or ALERT attention flag, the
  system should log it to a review queue
- After 3+ flags against the same claim across different weeks, trigger
  a dossier section refresh

### Bootstrap Problem

The first weekly run has no running picture entries. The Phase 1 prompt
handles this gracefully because the running context section will simply
be empty, and the LLM is instructed to work with available context. The
first few weeks' analytical assessments will be thinner — no trajectory
detection, no thread tracking — but the system improves as entries
accumulate. By week 4-5, the running picture is contributing meaningfully
to analysis quality.

The leader profiles partially compensate during the bootstrap period,
since they contain baseline behavioral patterns and relationship
assessments that provide some of the context the running picture
would otherwise supply.

### Quality Control

**Automated checks on Running Picture entries:**
- Every Key Action must have a source attribution
- Every Developing Thread must have a "Watch for" field
- Commitments with status SHIFTED or WALKED BACK must reference the
  original commitment date
- Structural Claim Checks should average 1-3 per week — zero suggests
  the LLM is not engaging with the context; more than 5 suggests
  either an unusual week or over-flagging

**Editorial review of Phase 2 output:**
- Before publication, review for: analytical claims not grounded in
  the per-leader assessments, geographic/leader balance, tone
  consistency, and factual accuracy of sourced events
- The Phase 2 output is a draft, not a finished publication —
  human editorial review is the final quality gate

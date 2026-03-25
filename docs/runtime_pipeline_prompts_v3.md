# Weekly Pipeline — Runtime Prompts & Running Picture Schema (v3)

## Revision History

- **v1**: Initial architecture. 10-week running picture window, single
  Phase 1 call, editorial Phase 2.
- **v2**: Incorporated dual reviewer feedback. Split Phase 1 into Call A
  (structured) and Call B (analytical). Added Phase 0 conditional global
  context. Reduced running picture window to 3 entries + consolidation.
  Added thread dormancy, missing thread audit, anti-anchoring falsification,
  claims namespacing, and output validation.
- **v3**: Incorporated Phase 2 scaling review. Added significance-based
  pre-filtering for 30+ leaders. Added Cross-Correlation Pass replacing
  raw event timeline. Merged Cross-Correlation Pass with Phase 0 trigger.
  Adjusted tier assignment criteria (thread awareness, weighted cross-leader
  threshold). Enriched Tier 2 compression (retained Between the Lines and
  falsification). Leveraged tier ordering for position bias alignment.

---

## Architecture Overview

Each weekly cycle processes leaders in up to four steps:

**Cross-Correlation Pass** (runs every week)
- Input: Global event timeline (all classified events across all leaders)
- Output: Thematic Clusters Brief (~300-500 tokens) + Phase 0 trigger
  decision
- Single lightweight LLM call (can use Haiku for cost efficiency)

**Phase 0: Global Context** (conditional — triggered by Cross-Correlation
Pass when a thematic cluster is significant enough)
- Input: Cross-cutting events identified by the Cross-Correlation Pass
- Output: Global Context Brief (~500-800 words) injected into all
  Phase 1 calls
- Single LLM call

**Phase 1: Per-Leader Analysis** (runs once per leader, parallelizable)
- **Call A** (Structured): Produces the Running Picture Entry
- **Call B** (Analytical): Produces the Analytical Assessment using
  Call A's output
- Two LLM calls per leader

**Phase 2: Publication Rendering** (runs once per cycle, after all
leaders processed and pre-filtered)
- Input: Pre-filtered leader assessments (tiered) + Thematic Clusters
  Brief + key evidence appendix
- Output: Reader-facing weekly brief in existing publication format
- Single LLM call

**Consolidation Task** (runs every 4 weeks, separate from weekly cycle)
- Input: Last 4 weeks of running picture entries per leader
- Output: Compressed period summary + dormant thread archive
- One LLM call per leader

---

## Claim Namespacing Convention

All baseline documents (country dossiers, leader profiles) use prefixed
namespacing for numbered claims:

- **Country Dossier claims**: `[STRUC-01]`, `[STRUC-02]`, etc.
- **Leader Profile claims**: `[PROF-01]`, `[PROF-02]`, etc.

This convention must be used consistently in all pipeline outputs.
Never use bare numbers for claim references. Never mix namespaces.

---

## Running Analytical Picture — Schema

One file per leader, append-only. The pipeline loads the most recent
3 entries + latest consolidation summary at runtime.

### Weekly Entry Schema

```markdown
---
leader: {{LEADER_NAME}}
country: {{COUNTRY}}
week_of: {{YYYY-MM-DD}}
generated_at: {{ISO_TIMESTAMP}}
event_count: {{N}}
source_count: {{N}}
---

### Activity Level
[ONE OF: High / Moderate / Low / Quiet]
[One sentence characterizing the week.]

### Key Actions
1. [DATE] [ACTION]: [Brief description].
   Source: [primary source attribution]
   Significance: [One sentence — reference [STRUC-XX] or [PROF-XX]
   where relevant]

2. ...

### Commitments & Positions
- [COMMITMENT/POSITION]: [What was said/pledged, to whom, in what context]
  Status: [NEW / REINFORCED / SHIFTED FROM [previous position] / WALKED BACK]
  Audience: [Domestic rally / Parliamentary address / Bilateral meeting /
  Multilateral summit / Media interview / Social media / Other — specify]
  Binding force: [HIGH (formal treaty/vote/signed agreement) / MODERATE
  (public pledge to international audience) / LOW (domestic rhetoric,
  aspirational statement)]

### Relationships
- [INTERACTION]: [With whom, format, topic, observable outcome]
  Assessment: [What this suggests about relationship trajectory]

### Domestic Political Position
[Changes only. If nothing changed: "No material change this week."]

### Developing Threads

ACTIVE THREADS:
- [THREAD]: [Current status]
  Watch for: [Specific observable event]
  Originated: [Week first appeared]
  Last updated: [This week / Week of YYYY-MM-DD if carried forward]

DORMANT THREADS:
- [THREAD]: [Last known status]
  Dormant since: [Week of YYYY-MM-DD]
  Reactivation trigger: [What would make this active again]

### Missing Thread Audit
- [THREAD from prior entry]: [RESOLVED (explain) / MERGED INTO [other
  thread] / MOVED TO DORMANT (explain) / OMITTED IN ERROR]

### Structural Claim Check
- [STRUC-XX] or [PROF-XX]: [CHALLENGED / REINFORCED / NEWLY RELEVANT]
  Evidence: [What happened]
  Recommendation: [If challenged — does source document need refresh?]

[If none: "No structural or profile claims materially affected."]

### Analytical Notes
[1-3 sentences. CONSTRAINT: Do not repeat insights from previous
3 weeks unless material new evidence exists.]
```

### Consolidation Summary Schema (Every 4 Weeks)

```markdown
---
leader: {{LEADER_NAME}}
country: {{COUNTRY}}
period: {{YYYY-MM-DD}} to {{YYYY-MM-DD}}
generated_at: {{ISO_TIMESTAMP}}
consolidates_entries: [list of week_of dates]
---

### Period Trajectory
[2-3 paragraphs synthesizing the 4-week period.]

### Stable Assessments
1. [ASSESSMENT]: [Evidence basis — cite specific weeks]
2. ...

### Resolved Threads
- [THREAD]: [Resolution, date, outcome]

### Escalated Threads
- [THREAD]: [Trajectory over 4 weeks, current urgency]

### Newly Dormant Threads
- [THREAD]: [Reason for dormancy, reactivation trigger]

### Commitment Ledger Update
[Current state of all active commitments.]

### Structural Claim Status
- [CLAIM]: [Flagged N times — REINFORCE / RECOMMEND REFRESH / MONITOR]

### Analytical Inertia Check
- [ASSESSMENT]: [VALIDATED — still supported / FLAGGED — may reflect
  analytical inertia, recommend fresh assessment next cycle]

### Slow-Burn Review
[Looking at 4 weeks holistically: did we miss a slow-burn deviation
that was labeled as continuity at the time?]
```

### Thread Lifecycle

NEW → ACTIVE → DORMANT → REACTIVATED → RESOLVED

Threads are never hard-deleted. Dormant threads remain visible during
consolidation cycles and are reactivated if new evidence emerges.

### Context Loading at Runtime

- Standard week: 3 recent entries + latest consolidation = ~3,000-5,000 tokens
- Consolidation week: 4 entries + prior consolidation + dormant archive = ~5,000-8,000 tokens

---

## Cross-Correlation Pass

Runs every week before Phase 0 and Phase 1. Serves two purposes:
1. Produces a Thematic Clusters Brief for Phase 2
2. Determines whether Phase 0 should be triggered

### System Prompt

```
You are a thematic clustering engine for a weekly intelligence
pipeline. You will receive a chronological list of classified
news events across multiple national leaders.

Your task is to identify events that share themes, entities, or
represent parallel actions across 2+ leaders — even when the
leaders use different terminology or framing for similar actions.

Produce two outputs:

OUTPUT 1 — THEMATIC CLUSTERS BRIEF
Group events into 3-8 thematic clusters where 2+ leaders are
involved. For each cluster:
- Cluster title (concise, descriptive)
- Leaders involved
- Brief description of the shared theme or parallel action
- Assessment: ROUTINE (expected regional coordination) or
  NOTABLE (represents convergence, divergence, or coordinated
  response worth highlighting)

Only include clusters involving 2+ leaders. Ignore events that
are purely domestic with no cross-leader dimension.

OUTPUT 2 — PHASE 0 TRIGGER RECOMMENDATION
Assess whether any cluster is significant enough to warrant a
shared Global Context Brief. Criteria:
- 3+ leaders responding to the same external event or crisis
- A cluster marked NOTABLE that involves a major shift in
  regional dynamics
- A systemic event (summit, crisis, institutional decision)
  that multiple leaders must respond to

Respond with: TRIGGER PHASE 0: [Yes/No]
If yes, identify which cluster(s) warrant the Global Context Brief.
```

### User Prompt

```
## GLOBAL EVENT TIMELINE
Week of {{DATE_START}} to {{DATE_END}}

{{CHRONOLOGICAL_EVENT_LIST}}
```

### Output Handling

- Thematic Clusters Brief → stored for Phase 2 input
- Phase 0 trigger decision → if Yes, trigger Phase 0 with identified
  cluster events as input
- This call can use Claude Haiku for cost efficiency (~3,000-5,000
  tokens input, ~300-500 tokens output)

---

## Phase 0: Global Context (Conditional)

Triggered only when the Cross-Correlation Pass recommends it.

### System Prompt

```
You are producing a concise Global Context Brief for a weekly
intelligence production cycle. A major event this week affects
multiple national leaders being monitored. Your brief will be
injected into per-leader analytical calls so that each analyst
has a shared baseline understanding of the event without
describing it independently.

Produce a factual, analytical summary of the shared event:
- What happened (concrete facts, dates, key actors)
- Why it matters for the international system
- What decisions or responses it demands from national leaders

Do NOT assess individual leaders' responses — that is the job of
the per-leader analysts.

Target length: 500-800 words.
```

### User Prompt

```
## CROSS-CUTTING EVENTS THIS WEEK

The following event clusters were identified as requiring shared
context across multiple monitored leaders:

{{TRIGGERED_CLUSTER_EVENTS}}

Produce the Global Context Brief for this week's cycle.
```

---

## Phase 1: Per-Leader Analysis

### Context Assembly (System Prompt — Cached)

The system prompt is identical for Call A and Call B for the same
leader. Role-specific instructions go in the user prompt.

```
## STRUCTURAL CONTEXT: {{COUNTRY}}

{{COUNTRY_DOSSIER_CONTENT}}

---

## LEADER CONTEXT: {{LEADER_NAME}}

{{LEADER_PROFILE_CONTENT}}

---

## CLAIMS INDEX (for reference)

### Country Structural Claims ({{COUNTRY}})
[STRUC-01]: [One-sentence summary]
[STRUC-02]: [One-sentence summary]
...

### Leader Profile Claims ({{LEADER_NAME}})
[PROF-01]: [One-sentence summary]
[PROF-02]: [One-sentence summary]
...
```

### Call A: Running Picture Entry (Structured)

Runs first. Produces the system of record.

#### User Prompt

```
You are a structured intelligence data logger. Process this week's
events and produce a Running Picture Entry following the schema
exactly.

Requirements:
- Key Actions must be concrete and verifiable with source attribution
- Commitments must include Audience and Binding Force fields
- Use [STRUC-XX] and [PROF-XX] prefixes for all claim references
- Address every thread in the Thread Checklist below
- Analytical Notes must NOT repeat insights from previous 3 weeks
  unless material new evidence exists

---

## RUNNING CONTEXT: {{LEADER_NAME}} — Recent Weeks

{{RUNNING_PICTURE_ENTRIES}}

---

{{#IF GLOBAL_CONTEXT}}
## GLOBAL CONTEXT: Week of {{DATE_START}}

{{GLOBAL_CONTEXT_BRIEF}}

---
{{/IF}}

## THIS WEEK'S EVENTS: {{LEADER_NAME}}
Reporting period: {{DATE_START}} to {{DATE_END}}

{{CLASSIFIED_EVENTS}}

---

## THREAD CHECKLIST (from prior entry — you MUST address each)
{{FOR_EACH_THREAD}}
{{N}}. [{{THREAD_TITLE}}] — Status as of last week: {{STATUS}}
{{END_FOR_EACH}}

For each: provide updated status in the Missing Thread Audit
(ACTIVE / DORMANT / RESOLVED / MERGED)

---

Produce the Running Picture Entry for {{LEADER_NAME}} ({{TITLE}},
{{COUNTRY}}) for the week of {{DATE_START}} to {{DATE_END}}.
```

### Call B: Analytical Assessment (Prose)

Uses Call A's structured output alongside the full context stack.

#### User Prompt

```
You are an intelligence analyst producing a weekly analytical
assessment. You have structural context, a leader profile,
running analytical picture, and a structured summary of this
week's developments.

Analytical method — apply to each significant event:

1. WHAT HAPPENED: State the concrete action from this week's
   reporting.

2. STRUCTURAL FIT: Does this align with or deviate from
   persistent patterns in the country dossier and leader
   profile? Cite specific [STRUC-XX] and [PROF-XX] claims.

3. TRAJECTORY FIT: Does this continue, escalate, reverse, or
   break from the recent trajectory in the running picture?
   Reference specific prior entries or threads.

4. COMBINED ASSESSMENT: What does the intersection of structural
   context and recent trajectory tell you? Classify as:
   CONTINUITY / DEVIATION (with level: TACTICAL ADJUSTMENT /
   SIGNIFICANT SHIFT / POTENTIAL STRUCTURAL CHANGE)

5. FALSIFICATION: What would you expect to see in the next
   1-2 weeks if your assessment is WRONG?

Anti-anchoring discipline:
- Do not default to CONTINUITY simply because the running
  picture establishes a strong prior
- Genuinely novel signals can emerge at any time

---

## RUNNING CONTEXT: {{LEADER_NAME}} — Recent Weeks

{{RUNNING_PICTURE_ENTRIES}}

---

{{#IF GLOBAL_CONTEXT}}
## GLOBAL CONTEXT: Week of {{DATE_START}}

{{GLOBAL_CONTEXT_BRIEF}}

---
{{/IF}}

## THIS WEEK'S STRUCTURED SUMMARY

{{CALL_A_OUTPUT}}

---

## RAW EVENTS (for reference)

{{CLASSIFIED_EVENTS}}

---

Produce an analytical assessment for {{LEADER_NAME}} ({{TITLE}},
{{COUNTRY}}) for the week of {{DATE_START}} to {{DATE_END}}.

Structure:

**ACTIVITY SUMMARY**
One paragraph: what they did, what it means, trajectory fit.

**EVENT ANALYSIS**
For each significant event:
- Context: [STRUC-XX] and [PROF-XX] references
- Running picture fit: thread connection, trajectory
- Assessment: CONTINUITY or DEVIATION (level)
- Falsification: If wrong, what would I see next? [1-2 sentences]
- Forward implications: [Flag as PROJECTION]

**CROSS-LEADER RELEVANCE**
- Which leader(s) affected?
- Nature of connection
- What should the aggregate brief highlight?

**BETWEEN THE LINES**
1-3 observations requiring full context stack. Must reference
specific claims or running picture entries. Do not repeat prior
weeks' observations.

**ATTENTION FLAGS**
- WATCH: Developing situation
- ALERT: Significant deviation
- STRUCTURAL: Challenges foundational assumption

**KEY EVIDENCE FOR PHASE 2**
3 most significant direct quotes, actions, or data points.
Format: [Leader action/quote] — [Source] — [Date]
```

---

## Phase 2: Pre-Filtering and Publication Rendering

### Step 1: Pre-Filter (Python Script, No LLM)

After all Phase 1 calls complete, a Python script reads structured
metadata from all Call B outputs and assigns each leader to a tier.

#### Tier Assignment Criteria

**Tier 1 — Full Assessment** (passed to Phase 2 in full)
Any ONE of:
- Any attention flag of STRUCTURAL or ALERT
- Any event classified as POTENTIAL STRUCTURAL CHANGE or SIGNIFICANT
  SHIFT
- Named in 1+ other leaders' Cross-Leader Relevance sections AND has
  any deviation classification above CONTINUITY (weighted threshold)
- Named in 3+ other leaders' Cross-Leader Relevance sections
  (hub for cross-cutting events, regardless of own deviation level)

Expected: 4-8 leaders per week at 30 total

**Tier 2 — Condensed Summary** (~400-500 tokens)
All of:
- Attention flags of WATCH only (or no flags)
- Events classified as TACTICAL ADJUSTMENT or mixed TACTICAL/CONTINUITY
- Named in 0-1 other leaders' Cross-Leader Relevance sections
  (without meeting the weighted Tier 1 threshold)

OR: 3+ active developing threads regardless of this week's activity
level (thread-aware elevation)

Condensed summary retains:
- Activity Summary paragraph
- All Cross-Leader Relevance entries (full)
- All Between the Lines observations (full)
- All Falsification criteria (full)
- Attention flags
- Key Evidence for Phase 2 block

Dropped: Detailed per-event analysis, structural fit prose,
trajectory fit prose

Expected: 10-15 leaders per week at 30 total

**Tier 3 — Minimal Stub** (~50-80 tokens)
All of:
- No attention flags
- All events classified as CONTINUITY
- Not named in any other leader's Cross-Leader Relevance
- Fewer than 3 active developing threads

Stub contains:
- Leader name, title, country
- Activity level
- One-sentence activity summary
- Active developing thread titles (list only)

Expected: 7-12 leaders per week at 30 total

#### Pre-Filter Output Assembly

```python
# Pseudocode for pre-filter logic

for leader in all_leaders:
    assessment = load_call_b_output(leader)
    flags = extract_attention_flags(assessment)
    deviations = extract_deviation_classifications(assessment)
    cross_refs = count_cross_leader_mentions(leader, all_assessments)
    active_threads = count_active_threads(leader)

    if (has_flag(flags, ['STRUCTURAL', 'ALERT'])
        or has_deviation(deviations, ['POTENTIAL_STRUCTURAL_CHANGE',
                                       'SIGNIFICANT_SHIFT'])
        or (cross_refs >= 1 and has_deviation(deviations,
            ['TACTICAL_ADJUSTMENT', 'SIGNIFICANT_SHIFT',
             'POTENTIAL_STRUCTURAL_CHANGE']))
        or cross_refs >= 3):
        assign_tier(leader, TIER_1)

    elif (has_deviation(deviations, ['TACTICAL_ADJUSTMENT'])
          or active_threads >= 3):
        assign_tier(leader, TIER_2)
        compress_assessment(leader)  # retain key fields

    else:
        assign_tier(leader, TIER_3)
        generate_stub(leader)

# Randomize order WITHIN each tier
shuffle(tier_1_leaders)
shuffle(tier_2_leaders)
shuffle(tier_3_leaders)
```

### Step 2: Phase 2 LLM Call (Renderer)

#### System Prompt

```
You are the production editor for the Middle Powers Monitor, a
weekly intelligence publication tracking democratic leaders
defending liberal international order.

You have received analytical inputs organized by significance:
- TIER 1: Full analytical assessments for leaders with
  significant developments
- TIER 2: Condensed summaries for leaders with moderate
  developments
- TIER 3: Minimal stubs for leaders with routine weeks

You also have a Thematic Clusters Brief identifying cross-leader
patterns detected across all leaders' events.

Your job is to render these into the publication's established
format. You are NOT generating new analysis. You are selecting,
organizing, and translating existing analytical work.

CRITICAL RULE: Every claim in every AI Assessment must be
traceable to a specific statement in the corresponding Phase 1
output. Do not introduce claims, connections, or interpretations
not present in the analyst's work. If analysis is thin, the AI
Assessment should be proportionally brief.
```

#### User Prompt

```
## ANALYTICAL INPUTS

[NOTE: Leaders are organized by analytical significance.
Randomized within tiers. Tier assignment reflects this week's
significance, not overall importance.]

### TIER 1: Full Assessments
[These leaders had significant developments. Complete analytical
assessment available.]

{{TIER_1_ASSESSMENTS — RANDOMIZED}}

### TIER 2: Condensed Summaries
[Moderate developments. Activity summary, cross-leader
connections, between the lines, falsification, and key evidence
available.]

{{TIER_2_SUMMARIES — RANDOMIZED}}

### TIER 3: Quiet Weeks
[Routine weeks. Activity level and active thread titles only.]

{{TIER_3_STUBS — RANDOMIZED}}

---

## THEMATIC CLUSTERS BRIEF

{{THEMATIC_CLUSTERS_FROM_CROSS_CORRELATION_PASS}}

---

## KEY EVIDENCE APPENDIX (Tier 1 + Tier 2)

{{AGGREGATED_KEY_EVIDENCE_EXTRACTS}}

---

{{#IF PRIOR_BRIEF}}
## PRIOR WEEK'S BRIEF (for continuity)

{{PRIOR_BRIEF}}
{{/IF}}

---

## INSTRUCTIONS

Produce the Middle Powers Monitor weekly brief for the week of
{{DATE_START}} to {{DATE_END}}.

### Step 1: Selection

**SIGNAL STORIES (1-3):**
Draw exclusively from Tier 1 leaders. Select based on:
- STRUCTURAL or ALERT attention flags
- SIGNIFICANT SHIFT or POTENTIAL STRUCTURAL CHANGE classifications
- NOTABLE clusters in the Thematic Clusters Brief
- Impact on middle power coordination / liberal order defense

If no events meet the SIGNIFICANT SHIFT threshold, select the
most consequential TACTICAL ADJUSTMENT developments. Do not force
drama — a consolidation week should read as such.

**AI ASSESSMENT SELECTION (Regional Briefs):**
- Tier 1 leaders: always include AI Assessment
- Tier 2 leaders: include when Between the Lines or falsification
  criteria contain non-obvious analytical substance
- Tier 3 leaders: no AI Assessment

**ALSO TRACKING:**
- Low-priority Key Actions from Tier 1 and Tier 2
- Tier 3 leaders with active threads worth noting
- Domestic events with minimal foreign policy implications
- If a Tier 3 leader is named in the Thematic Clusters Brief,
  include them in Also Tracking with a note about the connection

### Step 2: Write the Brief

# The Middle Powers Monitor

## Week of {{DATE_RANGE}}

[Opening paragraph: 2-3 sentences identifying the week's most
significant developments. Direct, concrete.]

---

## This Week's Signal

[For each Signal story (1-3):]

### [FLAG EMOJI] [Headline]

**BLUF:** [1-2 sentences. What happened.]

- [Bullet points: concrete sourced facts from Key Evidence and
  structured summaries. No analysis in bullets.]

**AI Assessment:** [3-5 sentences. Drawn EXCLUSIVELY from the
Phase 1 analytical assessment. Drop [STRUC-XX]/[PROF-XX]
references. Preserve: structural grounding, running picture
trajectory, deviation classification. Translate falsification
criteria into "watch for" language.]

---

## Regional Briefs

[Group by region. For each leader:]

#### [FLAG EMOJI] [Country] / [Leader Name]

- [Bullet points: 3-6 for active weeks, 1-2 for quiet weeks.]

[If AI Assessment selected:]
**AI Assessment:** [2-4 sentences. Same rules, briefer.]

---

## Also Tracking

- **[Country]:** [One-line items.]

---

*[Methodology line: leaders monitored, sources processed, date
range, notable gaps.]*

---

### Writing Guidelines

TONE: Informed, direct, occasionally dry. Wire service clarity
with analyst depth.

BULLETS: Factual, concrete. No analysis — that's the AI
Assessment's job.

AI ASSESSMENTS: Answer "so what?" Use "watch for" language.
Never bluff depth. If the analyst's assessment is thin, keep
the AI Assessment short.

TIER RULES:
- Signal stories from Tier 1 only
- AI Assessments from Tier 1 (always) and Tier 2 (selective)
- Tier 3 in Also Tracking only (or omitted if no active threads)
- If Thematic Clusters Brief identifies a pattern involving a
  Tier 2 or Tier 3 leader, ensure that pattern is surfaced
  somewhere in the brief

DO NOT:
- Introduce analysis not present in Phase 1 outputs
- Produce AI Assessments for every leader
- Repeat analytical observations from prior week without new
  evidence
- Editorialize about whether actions are good or bad
```

---

## Output Validation

### Cross-Correlation Pass
- [ ] Output contains Thematic Clusters Brief with 1+ clusters
- [ ] Each cluster names 2+ leaders
- [ ] Phase 0 trigger recommendation present (Yes/No)

### Phase 1 Call A
**Required field checks:**
- [ ] All schema fields present
- [ ] Each Key Action has Source field
- [ ] Each Commitment has Status, Audience, Binding Force
- [ ] Active and Dormant thread sections present
- [ ] Each Active Thread has Watch For, Originated, Last Updated
- [ ] Missing Thread Audit present and accounts for all threads
      from prior entry (automated count check)
- [ ] All claim references use [STRUC-XX] or [PROF-XX] format
- [ ] All referenced claims exist in baseline documents

**On failure:** Auto-retry once with correction prompt specifying
missing fields. If retry fails, accept with WARNING flag.
Thread count mismatch: retry with explicit thread list.
Hallucinated claims: strip invalid references, flag for review.

### Phase 1 Call B
- [ ] All sections present (Activity Summary, Event Analysis,
      Cross-Leader Relevance, Between the Lines, Attention Flags,
      Key Evidence for Phase 2)
- [ ] Each event has Falsification field
- [ ] Length within range (~1,500-3,000 words)
- [ ] Claim references valid

**On failure:** Auto-retry once. If fails, pass to Phase 2 with
flag: "[LEADER] assessment may be incomplete."

### Phase 2
- [ ] Opening paragraph present
- [ ] At least 1 Signal story present
- [ ] Regional Briefs present
- [ ] Also Tracking present
- [ ] No ALERT/STRUCTURAL-flagged leader appears only in Also
      Tracking
- [ ] Length within range (~1,500-4,000 words)

---

## Structural Claim Refresh Trigger

If the same [STRUC-XX] or [PROF-XX] claim is flagged as CHALLENGED
in 3+ separate weekly entries, add to refresh queue for human review.
Consolidation summaries recommending REFRESH also add to queue.

---

## Token Budget Estimates

### Cross-Correlation Pass (every week)
| Component | Tokens |
|-----------|--------|
| Global event timeline | 3,000-5,000 |
| System + user prompt | 500 |
| **Total input** | **~3,500-5,500** |
| Output | 300-500 |

Can use Claude Haiku for cost efficiency.

### Phase 0 (conditional, ~30% of weeks)
| Component | Tokens |
|-----------|--------|
| Triggered cluster events | 2,000-4,000 |
| System + user prompt | 500 |
| **Total input** | **~2,500-4,500** |
| Output | 500-800 |

### Phase 1 Call A (per leader)
| Component | Tokens |
|-----------|--------|
| Country dossier (cached) | 8,000-12,000 |
| Leader profile (cached) | 3,000-5,000 |
| Claims index (cached) | 1,000-2,000 |
| Running picture (3 entries + consolidation) | 3,000-5,000 |
| Global context (if applicable) | 500-800 |
| This week's events | 2,000-6,000 |
| Thread checklist + prompt | 1,500-2,000 |
| **Total input** | **~19,000-32,800** |
| Output | 1,000-2,000 |

### Phase 1 Call B (per leader)
| Component | Tokens |
|-----------|--------|
| Country dossier (cached) | 8,000-12,000 |
| Leader profile (cached) | 3,000-5,000 |
| Claims index (cached) | 1,000-2,000 |
| Running picture (3 entries + consolidation) | 3,000-5,000 |
| Call A output | 1,000-2,000 |
| Global context (if applicable) | 500-800 |
| Raw events | 2,000-6,000 |
| Prompt | 2,000 |
| **Total input** | **~20,500-34,800** |
| Output | 1,500-3,000 |

### Phase 2 (single call, with pre-filtering at 30 leaders)
| Component | Tokens |
|-----------|--------|
| Tier 1 assessments (6 × 2,000) | ~12,000 |
| Tier 2 summaries (12 × 450) | ~5,400 |
| Tier 3 stubs (12 × 65) | ~780 |
| Thematic Clusters Brief | 300-500 |
| Key evidence appendix | 2,000-4,000 |
| Prior week's brief | 3,000-5,000 |
| System + user prompt | 2,500 |
| **Total input** | **~26,000-30,180** |
| Output | 2,000-5,000 |

### Weekly Totals (30 leaders)
| Phase | Calls | Input | Output |
|-------|-------|-------|--------|
| Cross-Correlation | 1 | ~4,500 | ~400 |
| Phase 0 | 0-1 | 0-4,500 | 0-800 |
| Phase 1A | 30 | ~570k-984k | 30k-60k |
| Phase 1B | 30 | ~615k-1,044k | 45k-90k |
| Phase 2 | 1 | ~28,000 | ~3,500 |
| **Total** | **62-63** | **~1.2M-2.1M** | **~79k-154k** |

With prompt caching on dossiers/profiles (~12,000-17,000 tokens ×
60 calls), effective cost is significantly reduced.

### Consolidation (every 4 weeks, 30 leaders)
| Component | Per leader input | Per leader output |
|-----------|-----------------|-------------------|
| 4 entries + consolidation + dormant + claims + prompt | ~8,000-14,500 | 1,500-3,000 |
| **30 leaders total** | **~240k-435k** | **~45k-90k** |

---

## File Management

### Directory Structure

```
running_picture/
├── weekly/
│   ├── macron/
│   │   ├── 2026-02-24.md
│   │   ├── 2026-02-17.md
│   │   └── 2026-02-10.md
│   └── .../
├── consolidation/
│   ├── macron/
│   │   └── 2026-02-24_consolidation.md
│   └── .../
├── dormant_threads/
│   ├── macron_dormant.md
│   └── .../
├── archive/
│   └── .../
└── cross_correlation/
    ├── 2026-02-24_clusters.md
    └── .../
```

### Runtime Context Assembly (per leader)

1. Load country dossier + leader profile + claims index (system prompt, cached)
2. Load 3 most recent weekly entries from `running_picture/weekly/X/`
3. Load most recent consolidation from `running_picture/consolidation/X/`
4. Load dormant threads (consolidation weeks only)
5. Load global context brief (if Phase 0 triggered)
6. Load classified events for this leader
7. Extract thread checklist from most recent weekly entry (Python script)
8. Assemble user prompt

### Post-Cycle Maintenance

After each weekly cycle:
1. Append Call A outputs to `running_picture/weekly/X/`
2. Store Cross-Correlation output to `cross_correlation/`
3. Archive entries older than retention window
4. Update dormant thread files if status changed
5. Log all [STRUC-XX] and [PROF-XX] flags to refresh tracker
6. Log validation failures for human review
7. Archive Call B outputs for debugging

After each consolidation (every 4 weeks):
1. Write consolidation summary to `consolidation/X/`
2. Update dormant thread files
3. Archive consolidated weekly entries
4. Generate structural claim refresh recommendations if threshold met

---

## Scaling Limits

This architecture handles up to ~50 leaders before Phase 2 input
exceeds comfortable ranges even with pre-filtering (12-15 Tier 1
leaders at 50 total approaches 30,000 tokens for Tier 1 alone).

Beyond 50: move to tiered rendering (regional Phase 2 calls +
final synthesis). Design separately when needed.

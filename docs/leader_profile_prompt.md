# Leader Profile — Seed Prompt

## Usage
Replace `{{LEADER_NAME}}`, `{{TITLE}}`, and `{{COUNTRY}}` with the target leader. This prompt generates a profile designed to be loaded alongside the Structural Country Dossier for {{COUNTRY}} and the leader's Running Analytical Picture at pipeline runtime.

This document should be regenerated when:
- The leader leaves office (archive and create new profile for successor)
- A major political realignment occurs (coalition collapse, snap election, constitutional crisis)
- Accumulated running picture entries reveal that the profile's assessments are systematically wrong

For routine updating based on weekly developments, use the Running Analytical Picture rather than revising this document.

---

## Prompt

You are producing a **Leader Profile** for **{{LEADER_NAME}}**, {{TITLE}} of {{COUNTRY}}.

This profile is not a biography. It is an **operational assessment** of how this specific individual exercises power — how they make decisions, who influences them, what they prioritize, how they behave under pressure, and what constrains their realistic options. A biography asks "who is this person?" This profile asks **"if I see this leader do X next week, what does it mean and what are they likely to do after that?"**

This profile operates in conjunction with a separate Structural Country Dossier for {{COUNTRY}} that covers persistent institutional, geographic, economic, and historical features. **Do not reproduce country-level structural analysis here.** This profile covers only what is specific to {{LEADER_NAME}}'s tenure — the aspects of the political landscape that would change if a different person held the office.

### Primary Consumer: Automated Intelligence Pipeline

This profile will be ingested as persistent context by a large language model that generates weekly intelligence briefs. The LLM will receive this profile alongside the country's structural dossier, a running analytical picture of recent weeks' developments, and incoming news events. The profile must enable the pipeline to:

- Interpret this leader's actions within the context of their specific political positioning, relationships, and constraints — not just the structural features of the country they lead
- Distinguish between actions that reflect this leader's deliberate strategic choices and actions that are structurally determined (any leader in this position would have done the same)
- Assess the significance of interactions between this leader and other monitored leaders based on the relationship dynamics described here
- Detect changes in this leader's behavior, signaling, or political position by comparing incoming events against the baseline described in this profile

Write accordingly:
- Every claim should be **grounded in observable behavior or credible reporting**, not inferred personality traits. "Tusk has consistently prioritized EU institutional channels over bilateral deals, as demonstrated by [examples]" is useful. "Tusk is a pragmatist by nature" is not — it's unfalsifiable and the pipeline can't match events against it.
- Distinguish explicitly between **observed patterns** (supported by multiple examples) and **tentative assessments** (based on limited evidence or single instances). Use confidence markers: **[HIGH CONFIDENCE]** (multiple corroborating examples), **[MODERATE CONFIDENCE]** (limited but credible evidence), **[ASSESSED]** (analytical inference from indirect evidence).
- **Name specific examples** to support behavioral claims. The pipeline LLM uses these examples as reference points for pattern-matching. A behavioral claim without examples is an unsupported assertion.
- When information is unknown or opaque, say so. Inner circle dynamics, private motivations, and health status are often genuinely unknowable — acknowledging this is more useful than speculating.

Each section must conclude with a **`PROFILE CLAIMS`** block: discrete, numbered assertions that the pipeline LLM will match against incoming events. These should describe **behavioral patterns and political positions**, not personality traits.

```
PROFILE CLAIMS:
1. [Observable behavioral pattern or political position with supporting evidence]
2. [Another claim]
...
```

---

### Output Structure

Produce the profile in the following structure. Write in analytical prose. Prioritize predictive utility over comprehensive coverage — the pipeline needs to know what this leader is likely to *do*, not everything about who they *are*.

---

#### METADATA
- **Leader:** {{LEADER_NAME}}
- **Title:** {{TITLE}}
- **Country:** {{COUNTRY}}
- **In Office Since:** [date]
- **Mandate Expires:** [date or condition — e.g., next scheduled election]
- **Associated Country Dossier:** {{COUNTRY}} Structural Country Dossier
- **Date Generated:** [current date]
- **Last Updated:** [current date]

---

#### 1. PATH TO POWER & POLITICAL MANDATE

How did this leader come to hold their current position? Not a career biography — an analysis of the **political conditions that produced this leader** and what mandate those conditions confer.

Address: What political problem or crisis did their ascent resolve or respond to (e.g., elected as a corrective to a predecessor's failures, emerged from a revolutionary movement, inherited power through institutional succession)? What coalition or political forces brought them to power, and what debts or obligations does that create? What mandate do they claim — and is the claimed mandate broader or narrower than what the political conditions actually support?

Assess the **durability of the political conditions** that produced them. Are the forces that brought them to power still operative, or have conditions shifted? If they were elected as a reaction against something, has that something dissipated (weakening their political rationale) or intensified (reinforcing it)?

---

#### 2. GOVERNING COALITION & DOMESTIC POLITICAL POSITION

Map the current political configuration that sustains this leader in power. This section answers the question: **what can this leader actually do, given who they depend on?**

Address: What is the formal governing arrangement (single-party majority, coalition, minority government, extra-parliamentary support)? Identify the key coalition partners or support factions and what each demands in exchange for support. Where are the **veto points** — which actors can block the leader's preferred policies, and on which issues? What is the leader's current approval trajectory, and what is driving it?

Identify the **most likely sources of political crisis** for this government. Coalition fracture points, upcoming electoral tests, pending judicial or legislative challenges, economic vulnerabilities that could erode public support. Assess which of these the leader can manage and which are outside their control.

Specifically address this leader's **political capital for foreign policy action**. Foreign policy often requires spending domestic political capital (defense spending, sanctions compliance, refugee acceptance, trade concessions). How much latitude does this leader have, and on which issues? Where would foreign policy ambition run into domestic political constraints?

---

#### 3. DECISION-MAKING ARCHITECTURE

Analyze how decisions actually get made in this leader's system. This is not about formal constitutional authority (that's in the country dossier) — it's about **how this specific leader uses the institutional tools available to them**.

Address: Is decision-making **centralized** (small inner circle, leader makes final calls personally, institutional process is largely performative) or **distributed** (genuine deliberation within cabinet or institutional structures, leader operates as chair rather than director)? How does this compare to their predecessors — have they centralized or decentralized relative to established norms?

Identify the **inner circle** where knowable — the specific individuals who have consistent access, influence, and the leader's trust. For each, note their role, their known policy orientation, and the nature of their influence (gatekeeper who controls information flow, trusted advisor on specific domains, political fixer, ideological anchor). Where the inner circle is opaque, state what is unknown and identify what observable indicators would reveal its composition (e.g., who travels with the leader, who appears at bilateral meetings, who is quoted in background briefings).

Assess the **information environment** around the leader. Is there institutional capacity for delivering bad news or dissenting analysis, or has the system optimized for consensus and confirmation? This directly affects how the pipeline should interpret this leader's decisions — a leader operating in an information bubble may make choices that appear irrational from the outside but are rational given the distorted picture they're receiving.

---

#### 4. FOREIGN POLICY ORIENTATION & STRATEGIC PRIORITIES

What is this leader trying to accomplish internationally, and what analytical framework do they operate from?

Address: What are their **stated foreign policy priorities** — and to what degree does their behavior match the rhetoric? Identify gaps between stated priorities and revealed preferences (where they actually spend time, political capital, and resources). Which foreign policy issues do they appear to care about personally versus which they delegate? Are there **signature initiatives** — specific international projects or campaigns this leader has championed and attached their credibility to?

Assess their **analytical framework** for international affairs. Not ideology in the abstract, but the operational lens they apply. Do they think primarily in terms of institutional multilateralism, bilateral deal-making, values-based alignment, transactional interest-balancing, or historical narrative? How does this framework shape which opportunities they see and which they miss? Provide specific examples of decisions that reveal the framework in action.

Address this leader's **posture toward the current international disruption** — American retrenchment, authoritarian assertiveness, institutional stress. Is this leader actively building alternative coordination mechanisms, doubling down on existing institutions, hedging across multiple frameworks, or primarily focused domestically? How early did they recognize the shift, and how has their response evolved?

---

#### 5. KEY BILATERAL RELATIONSHIPS

Map this leader's most important bilateral relationships — particularly with other leaders in the monitored set. For each significant relationship, analyze:

- **Structural basis**: Is this relationship driven by institutional imperatives (these countries must coordinate regardless of who leads them) or is it personality-dependent (these specific leaders have built a working relationship that their successors might not maintain)?
- **Current dynamic**: What are they cooperating on, where do they disagree, and what is the trajectory (deepening, stable, fraying)?
- **Interaction pattern**: How do they engage — through formal institutional channels, bilateral summits, back-channel communication, public signaling? What does the choice of channel reveal about the nature of the relationship?
- **Leverage dynamics**: Who needs whom more in this relationship, and on what issues? Where does asymmetric dependency create leverage?

Prioritize the relationships that are most likely to generate events the pipeline will need to interpret. A detailed assessment of three key relationships is more useful than a shallow survey of ten.

Also assess this leader's **relationship with the United States** — however that relationship is currently configured. For MPM's purposes, every monitored leader's posture toward Washington (cooperative, adversarial, hedging, transactional, resigned) shapes their broader international behavior and how they approach middle power coordination.

---

#### 6. COMMUNICATION & SIGNALING PATTERNS

How does this leader communicate, and how should the pipeline interpret their public signals?

Address: What are their **preferred communication channels** (formal press conferences, social media, parliamentary addresses, interviews with specific outlets, international forum speeches, unofficial background briefings)? Does the choice of channel carry meaning — do they use different channels for different audiences or different types of messages?

Analyze their **rhetorical patterns**. How do they signal policy shifts — gradually through adjusted language, abruptly through dramatic statements, or indirectly through proxies and background briefings? Are there known **linguistic markers** that indicate significant intent versus routine positioning? (E.g., some leaders have specific phrases or formulations they deploy when committing to action versus when they're floating trial balloons.)

Assess the **reliability of their public statements as indicators of actual intent**. Some leaders say what they mean; others systematically use public communication for audience management while actual policy is set through private channels. Where does this leader fall on that spectrum? Provide specific examples of cases where their public communication did and did not predict subsequent action.

Address any **non-standard communication channels** relevant to pipeline monitoring. Does this leader use Telegram, specific social media platforms, or unconventional formats (e.g., Zelenskyy's nightly addresses, Sheinbaum's mañaneras) that the pipeline should treat as primary sources?

---

#### 7. DEMONSTRATED CRISIS BEHAVIOR

How has this leader actually behaved when under pressure? This section draws exclusively from observed behavior — not from inferred personality traits or speculative scenarios.

Identify **2-4 specific crisis episodes** this leader has navigated (domestic political crises, international confrontations, economic emergencies, security incidents). For each:

- What was the nature and severity of the crisis?
- How did the leader respond — what did they do in the first 48 hours, and how did their approach evolve?
- Did they centralize decision-making or rely on institutional process?
- Did they escalate externally (blame foreign actors, create diversionary crises) or absorb the pressure domestically?
- Did they communicate publicly or go quiet?
- What was the outcome, and did their response strengthen or weaken their position?

From these episodes, assess whether there are **consistent patterns** in crisis behavior. Does this leader have a default crisis mode? How reliable is the pattern — is it consistent enough that the pipeline can use it to predict behavior in future crises?

**[CALIBRATION NOTE]:** Crisis behavior analysis is inherently limited by the sample size of observed crises and the specificity of each situation. Identify patterns where they exist but flag confidence levels honestly. A leader who has navigated one crisis provides weaker evidence than one who has navigated five.

---

#### 8. LIBERAL ORDER DEFENSE — TRACK RECORD

This section is specific to MPM's analytical mission. Assess this leader's **concrete actions** in defense of liberal international order, multilateral institutions, and democratic coordination among middle powers.

Address: What specific actions has this leader taken that qualify as defending or strengthening liberal international order? Be precise — name the initiatives, votes, commitments, deployments, institutional proposals, or coalition-building efforts. Distinguish between **rhetorical support** (speeches, declarations, communiqués) and **material action** (resource commitments, institutional proposals with follow-through, diplomatic capital expenditure, domestic political risk-taking for international objectives).

Assess the **consistency and credibility** of their commitment. Has their support for liberal order been steady or opportunistic? Have they maintained commitments when doing so became politically costly, or do they defect under domestic pressure? Are there domains where they champion liberal order (e.g., security) but obstruct it in others (e.g., trade, climate, migration)?

Identify **the specific contribution this leader makes** to middle power coordination that would not exist without them. What role do they play in the ecosystem of democratic coordination — convener, enabler, norm entrepreneur, security provider, institutional reformer, financial backer? What would be lost if they left office tomorrow?

---

#### 9. VULNERABILITIES & RISK FACTORS

Identify the factors that could significantly alter this leader's behavior, political position, or tenure. Organize by type:

**Political vulnerabilities**: coalition fragility, electoral exposure, intra-party challenges, judicial investigations, legislative obstacles. For each, assess likelihood and timeline.

**External vulnerabilities**: dependence on foreign relationships that could shift, exposure to economic sanctions or trade pressure, security dependencies that create leverage for other actors. For each, identify who holds the leverage and under what conditions they might exercise it.

**Personal factors** where credibly reported and strategically relevant: health issues that affect governance capacity, financial exposure to specific jurisdictions, family or personal situations that create political vulnerability. **Apply strict evidential standards** — include only factors supported by credible reporting, not rumor or speculation. Where credible reporting is limited, state what is unknown.

**Succession dynamics**: If this leader were to leave office unexpectedly, what is the most likely succession scenario? Is there an obvious successor, a contested succession, or an institutional vacuum? How would the succession scenario affect the foreign policy orientation and liberal order commitments assessed in Section 8?

---

#### 10. OPEN QUESTIONS & ANALYTICAL GAPS

List 5-8 specific questions about this leader that the profile cannot answer but that would significantly improve analytical accuracy if resolved. For each:

- State the question precisely
- Explain why it matters for the pipeline's analytical output
- Identify what observable evidence would help resolve it
- Note whether the running analytical picture is likely to accumulate evidence over time or whether this requires dedicated research

This section serves as a **research agenda** — it tells the pipeline what to watch for that would improve the profile's predictive utility.

---

#### 11. PIPELINE INTEGRATION NOTES

This section is for the consuming LLM only. Provide:

- **Behavioral baseline for deviation detection**: Describe this leader's "normal" behavior pattern across key domains (foreign policy engagement frequency, domestic political management style, communication cadence, institutional interaction patterns). The pipeline should flag deviations from this baseline as potentially significant. Be specific enough that "deviation" is operationally detectable: "Macron typically engages in 2-3 bilateral meetings per week during EU council periods and makes substantive foreign policy statements primarily through Élysée readouts rather than social media; a shift to direct social media communication or a significant increase in bilateral meeting frequency would signal [assessment]."
- **Interaction interpretation guide**: When this leader meets with other monitored leaders, what contextual factors from this profile should the pipeline apply? Which meetings are routine (structurally determined, would happen regardless of who held office) versus discretionary (reflecting this leader's specific choices)? Provide examples.
- **Source weighting for leader-specific coverage**: Which media outlets or journalists have reliable access to this leader's thinking? Which outlets are known to receive authorized leaks or background briefings from this leader's team? Which outlets are systematically hostile and should be read as opposition framing rather than independent reporting?
- **Common misinterpretation patterns**: What analytical errors do outside observers most commonly make about this leader? Identify 3-5 recurring misreadings that the pipeline should be calibrated to avoid. (E.g., "International media frequently interpret [leader]'s [behavior] as [misreading], when it actually reflects [structural dynamic described in Section X].")

---

### Stylistic Instructions

- Write in analytical prose. No bullet points except in Sections 9, 10, and 11.
- Ground every behavioral claim in **specific examples**. "This leader tends to X" must be followed by "as demonstrated by [concrete instance 1] and [concrete instance 2]." Ungrounded behavioral claims are analytically useless and the pipeline cannot match events against them.
- **Distinguish sharply between this leader and their country.** If a claim would be equally true of any leader in this position, it belongs in the country dossier, not here. This profile covers only what is specific to this individual's exercise of power.
- Do not psychoanalyze. Describe observable behavioral patterns and decision-making system features. "Risk-averse" is a personality label; "has consistently chosen incremental policy adjustments over bold moves when facing uncertainty, as seen in [examples]" is an observable pattern.
- When information is genuinely unknown (inner circle dynamics, private motivations, health), state this clearly rather than filling the gap with speculation. The pipeline handles explicit uncertainty better than confident-sounding guesses.
- Every section must conclude with a `PROFILE CLAIMS` block of numbered, discrete, evidence-based assertions.
- Target length: 3,000–5,000 words.

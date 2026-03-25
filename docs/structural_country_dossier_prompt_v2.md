# Structural Country Dossier — Seed Prompt v2

## Usage
Replace `{{COUNTRY}}` with the target country. This prompt generates a seed dossier designed to be periodically updated with current events analysis. Each section is self-contained for targeted refresh.

Generate in two passes to manage context window limits:
- **Pass 1:** Metadata through Section 9 (Illicit Networks & Shadow Governance)
- **Pass 2:** Sections 10–20, with Pass 1 output provided as context

---

## Prompt

You are producing a **Structural Country Dossier** for **{{COUNTRY}}**. This dossier is not a chronological history. It is an analytical reference document that explains why this country behaves the way it does today by identifying the historical structures, traumas, dependencies, and constraints that continue to exert gravitational pull on its decision-makers and population.

### Primary Consumer: Automated Intelligence Pipeline

This dossier will be ingested as persistent context by a large language model that generates weekly intelligence briefs. The LLM will receive this dossier alongside incoming news events and must use it to:
- Determine whether an event represents continuity or deviation from structural patterns
- Generate grounded analytical observations rather than contextless commentary
- Identify when a leader's actions are constrained by structural factors versus representing genuine policy choice
- Detect when surface-level reporting obscures deeper structural dynamics

Write accordingly:
- Every analytical claim should be **concrete and pattern-matchable** — the consuming LLM needs to be able to compare incoming events against specific structural features described here
- Favor **falsifiable assertions** over hedged generalities: "Poland's judiciary crisis creates a persistent vulnerability to EU institutional pressure" is more useful than "Poland has complex relations with the EU"
- Define regional terms, acronyms, and institutional names in-line on first use (e.g., "the IRGC (Islamic Revolutionary Guard Corps, the ideological military branch parallel to the conventional army)")
- When referencing political figures, briefly identify their role and significance rather than assuming name recognition
- Where evidence is thin or contested, flag it explicitly with a confidence marker: **[HIGH CONFIDENCE]**, **[MODERATE CONFIDENCE]**, or **[ASSESSED]** (for analytical inference rather than established fact)

Each section must conclude with a **`STRUCTURAL CLAIMS`** block: a set of discrete, numbered assertions that distill the section's core analytical content into extractable statements. These are the claims the pipeline LLM will pattern-match against incoming events. Format:

```
STRUCTURAL CLAIMS:
1. [Concrete, falsifiable assertion about a persistent structural feature]
2. [Another assertion]
...
```

---

### Output Structure

Produce the dossier in the following structure. For each section, write in analytical prose — not bullet points. Prioritize explanatory depth and causal reasoning over encyclopedic coverage.

---

#### METADATA
- **Country:** {{COUNTRY}}
- **Date Generated:** [current date]
- **Last Updated:** [current date]
- **Priority Refresh Sections:** [leave blank — to be populated during updates]

---

#### 0. KEY ACTORS & INSTITUTIONS PRIMER

Provide a concise reference guide to the political actors, institutions, and organizations that the analyst will encounter in current reporting and that recur throughout this dossier. For each entry, explain not just what it is but *why it matters structurally* — what role it plays in the country's power dynamics. Organize into categories (e.g., state institutions, political parties/movements, security actors, economic actors, non-state/civil society actors, external actors with persistent domestic influence).

This section should function as a glossary the consuming LLM can reference when processing news articles that mention these actors without explanation. Include standard abbreviations and alternate names used in English-language and domestic media.

---

#### 1. FORMATION TRAUMA & FOUNDING MYTHOLOGY

How did this state come into being? Was it forged through revolution, decolonization, partition, unification, secession, or the collapse of a predecessor state? What is the founding narrative the state tells itself — and what does it suppress or rewrite? Identify the specific historical wound or triumph that continues to shape elite threat perception, national identity, and political legitimacy. Explain how this origin story is actively maintained, contested, or instrumentalized today.

---

#### 2. GEOGRAPHIC DETERMINISM & PERSISTENT STRATEGIC PROBLEMS

Analyze the physical geography as a set of permanent strategic constraints. Address: defensibility of borders (natural barriers vs. open approaches), access to maritime trade routes or landlocked dependency, chokepoint control, resource geography (abundance, scarcity, curse), climate zones and agricultural viability, and proximity to major powers. Identify which strategic problems are *structurally unsolvable* given the geography — these are the problems every government of this country will face regardless of ideology or capability.

---

#### 3. IMPERIAL LEGACY & INSTITUTIONAL INHERITANCE

Who ruled this territory before the current state, and what institutional residue did they leave behind? Address: legal systems, administrative structures, border demarcation logic, language hierarchies, security sector models, and economic integration patterns. Explain how the specific character of the former imperial power continues to shape governance capacity, elite formation, and external orientation. If multiple imperial legacies overlap (e.g., Ottoman then British, or Qing then Japanese), analyze how they interact and which layer is dominant in which domain.

---

#### 4. ETHNIC, SECTARIAN & LINGUISTIC CLEAVAGE STRUCTURE

Map the primary identity cleavages — but focus on *how and when they became politically activated* rather than treating them as primordial. Explain which cleavages were hardened by colonial census-taking, imperial administrative boundaries, or deliberate divide-and-rule policies. Identify which cleavages are currently salient versus dormant, and what historical conditions have caused activation or deactivation in the past. Address how political entrepreneurs have instrumentalized these cleavages and whether the state's institutional design manages or exacerbates them.

---

#### 5. DEMOGRAPHIC TIDES & GENERATIONAL DYNAMICS

Analyze the country's demographic structure as a strategic variable. Address: current age distribution (youth bulge vs. aging population), historical birth rate transitions, migration patterns (brain drain, diaspora networks, labor importation, refugee flows), urbanization trajectory, and the political implications of generational cohorts with distinct formative experiences. Identify the demographic "clock" — what structural pressures are building or dissipating based on population dynamics, and on what timeline.

---

#### 6. ECONOMIC STRUCTURE, FINANCIAL ARCHITECTURE & DEPENDENCY PATTERNS

What does this country produce, who buys it, and what does that do to domestic power relations? Analyze: primary economic base (rentier, manufacturing, agricultural, services), commodity dependency and Dutch Disease dynamics, the identity and leverage of key trading partners, the structure of state-business relations (oligarchic capture, state capitalism, competitive markets), informal economy scale, and the distribution mechanism for national wealth. Explain how the economic structure shapes the state-society bargain and constrains foreign policy autonomy.

Additionally, analyze the **financial system architecture** as a distinct set of structural constraints: central bank independence (de jure and de facto), currency regime (free float, managed float, peg, dollarization, currency union membership), sovereign debt profile and creditor composition (domestic vs. foreign, bilateral vs. multilateral), credit rating trajectory, foreign reserve adequacy, sanctions exposure and vulnerability to financial isolation, and the degree to which the financial system is integrated into or insulated from global capital flows. Identify where financial architecture creates **binding constraints on policy autonomy** — e.g., eurozone membership eliminates monetary policy discretion; dollar-denominated debt creates vulnerability to Fed rate decisions; dependence on IMF lending programs conditions fiscal choices.

---

#### 7. INFRASTRUCTURAL INHERITANCE & RESOURCE PATHWAYS

Analyze the physical infrastructure as materialized path dependency. Address: transportation networks (rail, road, port orientation — who were they built to connect, and for whose benefit?), energy infrastructure (pipeline routes, grid dependencies, generation mix), telecommunications architecture, and water management systems. Identify where the physical topology of infrastructure encodes historical dependency relationships that persist despite political reorientation. Flag critical infrastructure chokepoints that create leverage for external actors.

---

#### 8. ENVIRONMENTAL & CLIMATIC STRUCTURE

Analyze the country's relationship between environmental conditions and political stability. Address: historical climate patterns and their role in regime legitimacy (flood management, drought cycles, agricultural viability), exposure to natural disasters and institutional capacity to respond, water security (transboundary river dependencies, aquifer depletion), and climate change trajectory as a threat multiplier. Identify whether environmental stewardship is historically embedded in the state's legitimacy narrative, and assess vulnerability to climate-driven destabilization.

---

#### 9. ILLICIT NETWORKS & SHADOW GOVERNANCE

Assess whether illicit economic activity and criminal networks function as **structural features of governance** rather than deviations from it.

**Where the illicit economy is not a structurally significant feature of governance**, state this assessment explicitly and briefly (1–2 sentences explaining why), then move on. Use the format:

> **STRUCTURAL RELEVANCE: LOW.** [Brief explanation — e.g., "Estonia's illicit economy is peripheral to governance. Organized crime exists but does not provide parallel governance functions, sustain patronage networks, or meaningfully constrain foreign policy autonomy."]

**Where the illicit economy is structurally significant**, provide full analysis addressing: the scale and character of the primary illicit economy (narcotics, extractive smuggling, human trafficking, arms flows, sanctions evasion); the degree of state-criminal integration (spectrum from hostile enforcement through tolerant coexistence to active symbiosis, including cases where security services directly manage illicit operations); how illicit revenue flows sustain regime patronage networks, fund security actors, or substitute for formal taxation in ungoverned spaces; whether criminal organizations provide parallel governance functions (dispute resolution, employment, infrastructure, protection) that the formal state cannot or chooses not to provide; and how illicit networks create transnational dependencies that constrain or enable foreign policy.

Identify whether the illicit economy is a regime vulnerability (exposure to external law enforcement pressure, anti-corruption campaigns as political weapons) or a regime asset (funding streams outside formal budget scrutiny, leverage over compromised elites, informal influence channels). Assess what would happen to regime stability if the primary illicit revenue stream were suddenly disrupted.

---

#### 10. INFORMATION ECOSYSTEM & MEDIA STRUCTURE

*[Analytical frame: comparative media systems analysis (Hallin & Mancini typology as starting point) combined with operational source reliability assessment.]*

Classify the country's media system and analyze how information flows shape political reality. Address:

**Ownership and control structure:** Who owns the major media outlets (state, oligarchic, foreign, diversified private), and what editorial constraints does ownership impose? Identify the key media proprietors and their political alignments. Map the relationship between media ownership and political power — is media a tool of state control, a weapon in oligarchic competition, an instrument of partisan mobilization, or a relatively autonomous institution?

**State-media relationship:** Where does this country fall on the spectrum from full state monopoly through captured-but-nominally-independent to genuinely pluralistic? How does the state exert influence — direct censorship, licensing regimes, advertising revenue manipulation, legal harassment, informal pressure, or ownership by allied business figures? Identify whether state influence is uniform or whether different media types (broadcast, print, digital) operate under different constraint levels.

**Source reliability mapping for intelligence consumers:** For the major domestic outlets that produce reporting relevant to this country's political and foreign policy behavior, provide an operational assessment: which outlets are reliably independent, which function as government mouthpieces, which represent specific opposition or factional perspectives, and which oscillate depending on the issue? This assessment should be concrete enough that a consuming LLM can weight source credibility when processing incoming articles.

**Digital information environment:** Assess the role of social media platforms, messaging apps, and digital-native outlets. Address: which platforms dominate political discourse (and whether this differs from global norms — e.g., Telegram in post-Soviet space, LINE in Japan/Thailand), the scale and character of state or partisan information operations, vulnerability to foreign disinformation campaigns, and whether digital platforms function as a safety valve for expression suppressed in traditional media or as an amplifier of polarization.

**Information flow under stress:** How does the information ecosystem behave during crises? Identify historical patterns: does the state impose information blackouts, does independent media surge or self-censor, do diaspora media channels become primary information sources, and how quickly does the information environment fragment along cleavage lines identified in Section 4?

---

#### 11. INTERNATIONAL INSTITUTIONAL COMMITMENTS & LEGAL FRAMEWORKS

*[Analytical frame: international institutional law and institutional lock-in analysis — focus on how treaty obligations and organizational memberships create binding constraints on state behavior versus serving as cheap talk.]*

Map the country's institutional architecture — the web of international commitments that constrain, enable, and shape its realistic policy options. Distinguish between **binding constraints** (commitments with meaningful enforcement mechanisms or high defection costs) and **aspirational memberships** (commitments with weak compliance mechanisms that function primarily as signaling).

**Multilateral institutional membership:** Identify the key organizations (UN system, regional bodies, trade organizations, security alliances, international financial institutions) and for each, assess: the degree of institutional lock-in (how costly would exit or non-compliance be?), whether the country is a norm-maker, norm-taker, or norm-contester within the institution, and where institutional commitments actively constrain domestic or foreign policy choices versus being routinely circumvented.

**Treaty obligations with operational significance:** Identify the specific treaties, agreements, and legal frameworks that create binding constraints — particularly those relevant to the country's behavior in international crises, trade disputes, or security coordination. Address: EU acquis compliance (for EU members or candidates), NATO Article 5 obligations and defense spending commitments, WTO dispute settlement exposure, bilateral defense agreements, and ICC/ICJ jurisdiction acceptance. For each, assess whether compliance is substantive or performative.

**Institutional reform posture:** Where does this country stand on reform of the institutions it belongs to? Is it invested in the current institutional architecture or actively seeking to reshape it? This is particularly relevant for middle powers navigating the tension between preserving existing multilateral institutions and adapting to shifting power dynamics.

**Defection costs and pivot constraints:** Assess the institutional costs of realignment. If this country were to significantly shift its international orientation (e.g., moving away from Western institutional frameworks or deepening integration with alternative structures like BRICS, SCO, AIIB), what institutional ties would have to be severed, at what cost, and with what precedent? Identify which institutional commitments function as genuine lock-in versus which could be abandoned at manageable cost.

---

#### 12. MILITARY & SECURITY SECTOR DNA

Analyze the institutional culture, economic interests, and political role of the military and security services. Address: historical role (guardian of the state, party instrument, autonomous actor, guarantor of ideological order), economic footprint (does the military own significant economic assets?), doctrinal orientation (conventional defense, internal security, expeditionary capability), relationship to civilian governance (subordinate, coequal, dominant), and the security sector's likely behavior under regime stress. Identify the military's institutional redlines — what would trigger intervention or defection.

---

#### 13. HISTORY OF DISSENT & CIVIL SOCIETY INFRASTRUCTURE

Map the historical infrastructure of opposition and non-state governance. Address: which institutions historically absorb dissent when the state fails or represses (religious institutions, labor unions, tribal structures, universities, professional associations, diaspora networks, criminal organizations), the dominant *form* of historical dissent (mass mobilization, armed insurgency, legal opposition, exile politics), and how the character of dissent movements has shaped post-crisis governance. Identify who currently provides parallel governance functions and where the next revolution (or counter-revolution) would likely be incubated.

---

#### 14. PATRON-CLIENT HISTORY & ALLIANCE GENEALOGY

Trace the country's historical alignment choices and external dependencies. Address: Cold War positioning and its residual effects, shifts in patronage and what triggered them, current security guarantees and their credibility, economic dependency relationships that constrain diplomatic autonomy, and diaspora or ethnic linkages that create transnational alignment pressures. Identify the country's realistic pivot options — who could they realign toward, at what cost, and what historical precedent exists for such a shift.

Specifically address this country's **structural relationship to American power** — the degree of dependence on US security guarantees, trade access, institutional backing, or technology transfer — and assess the impact of American retrenchment, hostility, or institutional disengagement on this country's realistic options. Where US withdrawal creates a security vacuum, identify which actors (regional powers, institutional frameworks, bilateral partnerships) could partially substitute and at what cost. This is the defining structural context for middle power behavior in the current period.

---

#### 15. CONSTITUTIONAL CRISES & REGIME TRANSITION PATTERNS

Analyze how power has actually transferred in this country historically. Identify the dominant pattern: elections, coups, dynastic succession, negotiated pacts, revolution, or state collapse. Look for cyclical patterns and their periodicity. Address: what typically triggers regime crisis, what institutions or actors serve as stabilizers or accelerants, whether democratic experiments have been sustained or repeatedly interrupted (and why), and the typical duration of political cycles. Assess the current regime's position within the historical pattern.

Within the analysis of the current regime, dedicate specific attention to the **decision-making architecture and leadership environment**. Address: the degree of decision-making centralization (does policy emerge from institutional process or from the principal's inner circle?); the quality and diversity of information reaching the top decision-maker (is there institutional capacity for dissent or bad-news delivery, or has the system optimized for telling the leader what they want to hear?); the composition and influence dynamics of the inner circle (identify key advisors, gatekeepers, and rival factions within the leadership's immediate environment where this is knowable); the leader's **demonstrated crisis behavior** based on historical precedent (does the system centralize further under pressure, fragment, or escalate externally to deflect domestic stress?); and personal factors with strategic relevance where credibly reported — health, succession planning or its absence, financial exposure to specific foreign jurisdictions, and risk appetite as revealed by past decisions rather than rhetoric.

**[CALIBRATION NOTE]:** Assess leadership dynamics only on the basis of observable behavior, institutional structure, and credible reporting. Flag confidence levels explicitly. Do not engage in speculative psychological profiling — the goal is to map the *decision-making system*, not to psychoanalyze the individual. Where information is opaque (as it often is for authoritarian inner circles), state what is unknown and identify what observable indicators would help resolve the uncertainty.

---

#### 16. COLLECTIVE MEMORY OF HUMILIATION & GRIEVANCE

Identify the emotional substrate beneath rational strategy. What historical events function as national trauma or sacred narrative — events whose invocation can mobilize populations, justify policy, or establish political redlines? Address: how these narratives are maintained (education, media, commemorations, political rhetoric), whether they are genuinely popular or elite-manufactured, how they map onto current geopolitical disputes, and where Western or external analytical frameworks systematically misread these redlines because they discount the grievance narrative as irrational.

---

#### 17. CROSS-FACET INTERSECTION ANALYSIS

This is the most critical section. Identify **at least five** significant intersections between the facets above — places where two or more structural forces interact to produce outcomes that no single facet would predict. For each intersection:

- Name the interacting facets
- Explain the mechanism of interaction
- Provide a concrete historical or contemporary example from this country
- State the analytical implication (what does this intersection tell the pipeline LLM to watch for in incoming events?)

Prioritize non-obvious intersections over self-evident ones.

---

#### 18. KEY ANALYTICAL JUDGMENTS

Provide 5–7 summary judgments about this country's structural posture. These should be:
- Falsifiable (the pipeline LLM can check them against future events)
- Structurally grounded (derived from the facets above, not from current news)
- Temporally bounded where appropriate (distinguish permanent constraints from generational pressures)
- Honest about uncertainty (use confidence markers)

---

#### 19. WATCH INDICATORS

List 8–12 observable indicators that would signal significant structural change in this country. For each indicator, specify which section(s) it relates to and what shift it would suggest. These should be things an analyst or automated pipeline can actually monitor — not abstract conditions but concrete observables (e.g., "officer corps purge reaching brigade command level" rather than "military becoming politicized").

---

#### 20. PIPELINE INTEGRATION NOTES

This section is for the consuming LLM only. Provide:

- **Source interpretation guidance:** When processing articles from this country's media landscape, what systematic biases or framing patterns should the pipeline expect and adjust for? Reference the source reliability assessments in Section 10.
- **Event significance thresholds:** What kinds of events represent structural continuity (expected behavior given the dossier) versus genuine deviation that warrants elevated attention? Provide 3–5 examples of each.
- **Common misreading patterns:** What analytical errors do outside observers most commonly make about this country? Identify 3–5 recurring misinterpretations that the pipeline should be calibrated to avoid.
- **Cross-leader connection points:** Which other countries' leaders (from the monitored set) does this country most frequently interact with, and what structural dynamics drive those interactions? This helps the pipeline identify when a bilateral event is routine versus significant.

---

### Stylistic Instructions

- Write in analytical prose. No bullet points within sections except in Sections 0, 18, 19, and 20.
- Favor causal explanation over description. "X happened" is less valuable than "X happened *because* Y, which means Z for today."
- Be specific. Name dates, figures, percentages, and treaty names where they strengthen the argument. Avoid vague hedging when you have evidence.
- Assume the consuming LLM has no prior regional expertise loaded in context. Provide enough context that references are self-contained — a name, date, or event mentioned without explanation is useless.
- When the historical record is contested or the analytical inference is uncertain, say so explicitly rather than presenting interpretation as settled fact.
- Do not editorialize about whether the country's behavior is good or bad. Explain the logic of its behavior from its own structural position.
- Where a concept has a direct parallel in another country the reader might know better, a brief comparative aside (one sentence) can accelerate understanding — but do not overuse this technique.
- Every section must conclude with a `STRUCTURAL CLAIMS` block of numbered, discrete, falsifiable assertions.
- Target length: 7,000–10,000 words for the initial seed dossier.

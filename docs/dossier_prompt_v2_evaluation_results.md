# Structural Country Dossier Prompt v2 — Expert Panel Evaluation Results

## Executive Summary

This document presents the results of a systematic expert review of the Structural Country Dossier Seed Prompt v2. Each section (0-20) was evaluated against the criteria specified in the Expert Prompt Review Guide, adopting the designated expert perspective for each section.

**Overall assessment:** The v2 prompt is architecturally sound — its section structure, analytical framing, and pipeline-orientation are well-designed. The most consistent gap across sections is **mechanism specificity**: the prompt tends to name the right analytical topics but does not force the LLM to trace causal chains from structural features to political outcomes, producing description rather than analysis. Secondary patterns include insufficient forward-looking trajectory analysis, underweighting of digital dimensions, and inconsistent pipeline operationalization guidance.

---

## Gap Severity Summary

### Critical Gaps

| Section | Gap | Impact |
|---------|-----|--------|
| 0 | No instruction to flag actors as institutionally stable vs. regime-specific | Glossary becomes outdated after transitions with no signal to pipeline |
| 2 | No distinction between genuine geographic constraints and governance failures framed as geographic | Encourages geographic determinism; misidentifies contingent problems as permanent |
| 4 | No analysis of cross-cutting vs. reinforcing cleavage structure | Misses one of the strongest predictors of conflict potential |
| 4 | No accommodation for countries where the dominant cleavage is not identity-based | Forces ethnic framing on countries where other cleavages are more consequential |
| 7 | Digital infrastructure entirely absent | Major blind spot for a dossier intended to remain relevant through the late 2020s |
| 12 | No disaggregation of conventional military vs. internal security services vs. parallel structures | Treats the entire security sector as a single unit; misses structurally critical inter-institutional rivalries |
| 13 | No analysis of state co-optation strategies for managing civil society | Misses the most common and durable civil society management strategy |
| 14 | No framework for multi-vector foreign policies | Force-fits patron-client model onto countries whose strategy is defined by multi-vector hedging |
| 14 | No analysis of domestic politics of alignment choices | Misses that alliance shifts are domestically contested events with winners and losers |
| 15 | Democratic backsliding mechanisms entirely omitted | The gradual-erosion mode of regime change most relevant to democratic middle powers is absent |
| 19 | No indicator sensitivity calibration (leading vs. confirming) | Watch indicators will be pitched at wrong sensitivity level for early warning |
| 20 | LLM-specific misreading patterns not addressed | Primary consumer is an LLM, yet LLM-specific analytical tendencies are not corrected for |

### Significant Gaps

| Section | Gap | Impact |
|---------|-----|--------|
| 0 | Actor categories miss religious authorities, monarchies, tribal leaders, judiciary as political actors | Incomplete actor maps for many country types |
| 0 | Insufficient guidance on distinguishing formal mandate from actual political function | Descriptions mirror organizational charts rather than power realities |
| 1 | No requirement to map competing founding narratives to specific political factions | Misses the contest between narratives |
| 1 | No instruction to identify institutional transmission channels for founding mythology | Misses observable indicators of narrative shift |
| 1 | Singular framing ("the specific historical wound or triumph") for layered-trauma countries | May produce single-trauma analysis |
| 2 | No instruction to analyze geography-technology interaction | Treats geographic constraints as more static than they are |
| 2 | Insufficient maritime dimension specificity | Underweights dominant geographic feature for coastal/island states |
| 3 | Insufficient specificity on elite formation pathways | Vague claims about imperial influence on elites |
| 3 | No accommodation for institutional absence as the relevant imperial legacy | Cannot handle countries where colonial power left near-zero capacity |
| 4 | Insufficient specification of institutional mechanisms for cleavage management | Generic assessments rather than identifying specific institutional tools |
| 5 | No causal mechanisms specified for demographic-to-political-outcome pathways | Demographic description rather than analysis |
| 5 | Political economy of aging absent | Misses the dominant demographic force for European middle powers |
| 5 | Diaspora as a distinct political actor collapsed into migration flows | Loses analytically distinct phenomenon |
| 6 | State-business relationship lacks actor/mechanism specificity | Pipeline cannot interpret policy decisions in terms of who benefits |
| 6 | Trade dependency not disaggregated into binding vs. substitutable | Cannot distinguish structural constraints from large but substitutable flows |
| 7 | Energy infrastructure underweighted relative to its geopolitical significance | Insufficient specificity for pipeline interpretation of energy events |
| 7 | No forward-looking infrastructure reorientation analysis | Misses one of the most reliable long-lead indicators of strategic realignment |
| 8 | Uses "threat multiplier" language the review guide explicitly warns against | Encourages vague assertion rather than causal mechanism tracing |
| 8 | Environmental-foreign-policy nexus absent | Misses cross-domain tensions in middle power coordination |
| 9 | No decision criteria for structural relevance determination | LLM must make threshold judgment without defined criteria |
| 9 | Elite foreign financial exposure absent | Misses structural foreign policy constraint from elite asset jurisdiction |
| 9 | Pipeline source interpretation of corruption reporting absent | Corruption articles will be taken at face value |
| 10 | Source reliability assessments lack structured template for outlet-by-outlet analysis | Assessments may be too vague to operationalize |
| 10 | Platform architecture effects on information flows not addressed | Misses how platform design shapes political discourse character |
| 10 | Crisis information precedents not anchored in specific historical episodes | Patterns too abstract to recognize when recurring |
| 11 | Defection costs not disaggregated by cost type | Treats realignment cost as single variable |
| 11 | No framework for competing/simultaneous institutional memberships | Misses dual-membership tensions increasingly common among middle powers |
| 12 | Military intervention spectrum not specified; redlines treated as binary | Misses spectrum from behind-the-scenes influence to outright seizure |
| 12 | Doctrinal orientation too compressed to interpret defense events | Pipeline cannot contextualize procurement, exercises, or deployments |
| 13 | Current organizational capacity vs. historical infrastructure not distinguished | May describe defunct institutions as if they retain mobilization capacity |
| 13 | No analysis of transnational civil society connections | Misses resources, protection, and vulnerabilities from international networks |
| 14 | US dependency not disaggregated by dimension | Cannot assess differential vulnerability to different modes of withdrawal |
| 14 | Pivot option feasibility not rigorously tested | Theoretical pivot possibilities presented as viable options |
| 15 | Succession dynamics buried in parenthetical rather than dedicated sub-analysis | Underweights one of the highest-consequence structural uncertainties |
| 16 | Competing grievance narratives not explicitly mapped | Assumes single dominant narrative; misses analytically significant competition |
| 16 | Grievance-to-geopolitical-positioning connection underspecified | Missing explicit causal tracing from historical memory to alliance behavior |
| 17 | No concrete example of target intersection depth | LLM will produce self-evident rather than non-obvious intersections |
| 17 | Intersections lack operational specificity for pipeline | Analytical implications too vague to operationalize |
| 18 | No example of target falsifiable judgment format | Judgments will be directionally correct but operationally unfalsifiable |
| 18 | Confidence levels not tied to evidence quality standards | Confidence markers become decorative rather than informative |
| 19 | No observation channel specified for indicators | Pipeline doesn't know where to look for signals |
| 19 | Indicators don't map to specific STRUCTURAL CLAIMS | Pipeline cannot determine which claims to reassess when indicators fire |
| 20 | Source interpretation guidance as prose rather than conditional rules | Less operationally useful for automated pipeline |
| 20 | Event significance thresholds at instance level rather than pattern level | Examples become stale quickly |

---

## Section-by-Section Evaluation

---

### Section 0: Key Actors & Institutions Primer

**Review perspective:** Country/regional political analyst + political risk analyst

**Criterion 1 — Actor category coverage:** *Partially addressed.* The suggested categories (state institutions, political parties, security actors, economic actors, non-state/civil society, external actors) are reasonable but omit: religious authorities with constitutional or de facto veto power, tribal/clan/customary governance leaders, royal courts or monarchies as parallel power structures, and judiciary/judicial councils as autonomous political actors. These are structurally dominant in many country contexts.

**Criterion 2 — Structural function vs. organizational description:** *Partially addressed.* The instruction "explain not just what it is but why it matters structurally" is the right direction, but lacks guidance to force distinction between an institution's formal mandate and its actual political role (e.g., a constitutional court that formally adjudicates law but functionally serves as regime legitimation tool or opposition veto point).

**Criterion 3 — Institutional stability vs. regime-specificity:** *Not addressed.* No instruction to flag which actors will persist across government changes versus which are tied to the current regime. This is essential for a glossary intended for long-term pipeline use.

**Criterion 4 — Operational utility for article processing:** *Adequately addressed.* The prompt explicitly requires "standard abbreviations and alternate names used in English-language and domestic media" and frames the section as "a glossary the consuming LLM can reference when processing news articles."

---

### Section 1: Formation Trauma & Founding Mythology

**Review perspective:** Historical sociologist specializing in nationalism and collective memory

**Criterion 1 — Event-narrative gap:** *Partially addressed.* "What does it suppress or rewrite?" gestures at the gap but does not force side-by-side comparison of historical event and constructed narrative, or analysis of what distortions reveal about current political dynamics.

**Criterion 2 — Competing founding narratives:** *Partially addressed.* "Contested" and "instrumentalized" imply multiple versions exist but do not explicitly require mapping which political forces champion which version and what is at stake in the contest.

**Criterion 3 — Institutional transmission channels:** *Partially addressed.* "Actively maintained, contested, or instrumentalized today" asks the right general question but does not push for identification of specific channels (school curricula, military training, state media, commemorative calendar, museum curation) — changes to which are observable indicators of narrative shift.

**Criterion 4 — Multiple layered formation traumas:** *Partially addressed.* The prompt lists multiple formation modes but uses singular framing ("the specific historical wound or triumph"), which may push the LLM toward identifying a single dominant trauma rather than analyzing how layered traumas interact.

---

### Section 2: Geographic Determinism & Persistent Strategic Problems

**Review perspective:** Political geographer + military/defense planner

**Criterion 1 — Genuine constraints vs. geographic excuses:** *Not adequately addressed.* The prompt frames geographic problems as "structurally unsolvable" without asking the LLM to test which problems are genuinely geographic versus which are institutional failures framed as geographic constraints.

**Criterion 2 — Geography-technology interaction:** *Not addressed.* The prompt treats geographic constraints as permanent and does not ask how technology and infrastructure mediate them. No bridge to Section 7 (Infrastructure).

**Criterion 3 — Maritime dimension:** *Partially addressed.* "Access to maritime trade routes" and "chokepoint control" gesture at the maritime dimension but omit EEZ claims, maritime boundary disputes, naval strategic geography, and fisheries as a political variable.

**Criterion 4 — Proximity as dynamic feature:** *Partially addressed.* "Proximity to major powers" is mentioned but framed as a permanent constraint rather than a dynamic relationship whose strategic meaning shifts with changing power dynamics.

---

### Section 3: Imperial Legacy & Institutional Inheritance

**Review perspective:** Comparative colonial institutions scholar + legal historian

**Criterion 1 — Mundane institutional channels:** *Partially addressed.* The list (legal systems, administrative structures, border demarcation, language hierarchies, security sector models, economic integration) captures political dimensions but underweights administrative and bureaucratic residues: land registration systems, railway gauge, educational credentialing, tax collection models, civil service recruitment patterns — often more consequential precisely because they are invisible and unreformed.

**Criterion 2 — Temporal layering:** *Partially addressed.* The prompt explicitly raises the issue and asks how layers interact and which dominates. Could be strengthened by requiring analysis of the specific interaction mechanism (selective adoption, selective destruction, institutional hybridization).

**Criterion 3 — Elite formation pathways:** *Partially addressed.* The prompt mentions "elite formation" as one thing imperial legacy shapes but does not push the LLM to trace specific pathways (where the current elite was educated, what professional networks were established, how generational divides in elite formation shape policy orientation).

**Criterion 4 — Absence of institutional inheritance:** *Not addressed.* The prompt assumes imperial powers leave "institutional residue." For countries left with near-zero institutional capacity at independence (e.g., Belgian Congo), the relevant analysis is about the gap, not the residue.

---

### Section 4: Ethnic, Sectarian & Linguistic Cleavage Structure

**Review perspective:** Comparative ethnic politics scholar + country-specific ethnographer

**Criterion 1 — Anti-primordialism and activation mechanisms:** *Adequately addressed conceptually, partially at the specificity level.* The constructivist framing ("how and when they became politically activated") is correct. The prompt asks about "political entrepreneurs" but does not push for identification of specific institutional channels of activation (party systems, media, patronage networks, census categories, electoral system design).

**Criterion 2 — Cross-cutting vs. reinforcing cleavages:** *Not addressed.* The prompt catalogs cleavages individually but does not ask how they relate to each other. This is one of the strongest predictors of whether identity politics will be manageable or explosive.

**Criterion 3 — Institutional cleavage management mechanisms:** *Partially addressed.* "Whether the state's institutional design manages or exacerbates them" is the right question but does not push for identification of specific mechanisms (federalism, consociationalism, electoral system design, language policy, affirmative action, decentralization) or assessment of their effectiveness.

**Criterion 4 — Non-identity dominant cleavages:** *Not addressed.* The section title and framing center on ethnic/sectarian/linguistic cleavages. No accommodation for countries where the dominant fault line is urban-rural, class-based, regional, generational, or ideological.

---

### Section 5: Demographic Tides & Generational Dynamics

**Review perspective:** Political demographer + migration studies scholar

**Criterion 1 — Demographic-to-political-outcome mechanisms:** *Partially addressed.* The prompt asks for "political implications" and identifies a "demographic clock" but does not force the LLM to trace causal chains (e.g., youth bulge + labor market failure + housing unaffordability = specific mobilization pathway).

**Criterion 2 — Emigration and brain drain as structural force:** *Partially addressed.* Listed as items in a list rather than analyzed as a structural force with downstream political and economic consequences (labor shortages, remittance dependency, electoral composition changes, emigration as political grievance or safety valve).

**Criterion 3 — Political economy of aging:** *Not adequately addressed.* "Aging population" is one pole of a spectrum but lacks analytical weight: no mention of pension sustainability, healthcare costs, intergenerational fiscal transfers, elderly voting bloc power, or fiscal constraints on defense/foreign policy spending.

**Criterion 4 — Diaspora political influence:** *Partially addressed.* "Diaspora networks" mentioned as a migration pattern but not treated as a distinct political phenomenon (diaspora lobbying, voting rights, remittance leverage, return migration).

---

### Section 6: Economic Structure, Financial Architecture & Dependency Patterns

**Review perspective:** Political economist + international financial economist + trade economist

**Criterion 1 — State-business relationship specificity:** *Partially addressed.* Categories listed ("oligarchic capture, state capitalism, competitive markets") but no push to identify specific firms, conglomerates, their political channels (party financing, media ownership, revolving doors, regulatory capture), or which policy domains they influence.

**Criterion 2 — Financial architecture depth:** *Adequately addressed.* The financial architecture paragraph is a strength — it explicitly asks where financial architecture creates "binding constraints on policy autonomy" and provides concrete examples of causal chains. Could be slightly stronger on tracing political consequences of each constraint.

**Criterion 3 — Trade dependency granularity:** *Partially addressed.* "Key trading partners" mentioned but no distinction between structural constraints (non-substitutable dependencies creating actionable leverage) and large but substitutable trade relationships.

**Criterion 4 — Informal economy:** *Partially addressed.* "Informal economy scale" mentioned as one item in a list. No push to assess whether formal economic statistics actually represent how the economy functions, or to analyze political implications of large-scale informality.

---

### Section 7: Infrastructural Inheritance & Resource Pathways

**Review perspective:** Infrastructure historian + energy security analyst

**Criterion 1 — Political intentionality carried forward to present:** *Adequately addressed on historical dimension, gap on forward-looking analysis.* "Who were they built to connect, and for whose benefit?" is excellent framing. Missing: whether current infrastructure investment is reinforcing or reorienting inherited dependency patterns.

**Criterion 2 — Energy infrastructure as geopolitical variable:** *Partially addressed.* "Pipeline routes, grid dependencies, generation mix" mentioned as one item. For European countries especially, this deserves far more weight: LNG terminals, nuclear dependency, renewable supply chains, strategic reserves — each consequential for foreign policy autonomy.

**Criterion 3 — Digital infrastructure dependency:** *Not addressed.* "Telecommunications architecture" is mentioned but submarine cables, data centers, cloud provider dependency, telecom equipment supply chains (Huawei/5G), and satellite internet are absent. Major blind spot.

**Criterion 4 — Infrastructure as strategic reorientation indicator:** *Not adequately addressed.* The prompt is backward-looking ("encodes historical dependency relationships"). Major current infrastructure projects signaling strategic reorientation are among the most reliable long-lead indicators of realignment.

---

### Section 8: Environmental & Climatic Structure

**Review perspective:** Environmental security scholar + climate scientist with regional expertise

**Criterion 1 — Environmental-to-political causal mechanisms:** *Partially addressed.* Mentions relevant topics but uses "climate change trajectory as a threat multiplier" — precisely the vague framing the review guide warns against. No push to trace specific causal pathways from environmental stress to political outcomes.

**Criterion 2 — Transboundary environmental dependencies:** *Partially addressed.* "Transboundary river dependencies, aquifer depletion" mentioned in parenthetical list. No push for upstream-downstream power dynamics, institutional management frameworks, or escalation scenarios.

**Criterion 3 — Environmental policy as foreign policy variable:** *Not addressed.* No analysis of how environmental position shapes international negotiation stance or creates tensions with other foreign policy dimensions (e.g., fossil fuel exporter committed to liberal order on security but obstructionist on climate).

**Criterion 4 — Environmental determinism vs. institutional mediation:** *Partially addressed.* "Institutional capacity to respond" gestures at the distinction but does not explicitly require differentiating between genuinely binding environmental constraints and those mediated by institutional/economic capacity.

---

### Section 9: Illicit Networks & Shadow Governance

**Review perspective:** Organized crime and illicit economies researcher + governance specialist

**Criterion 1 — Calibration problem:** *Well addressed with a gap in decision criteria.* The "STRUCTURAL RELEVANCE: LOW" escape valve is one of the best design features in the entire prompt. Gap: no explicit criteria for the LLM to determine whether illicit activity crosses the threshold into structural governance relevance.

**Criterion 2 — State-criminal integration spectrum:** *Adequately addressed.* The spectrum from "hostile enforcement through tolerant coexistence to active symbiosis" is specific and well-framed.

**Criterion 3 — Illicit financial flows as foreign policy constraint:** *Not adequately addressed.* Elite wealth parked in foreign jurisdictions (London, Swiss, Dubai) creates actionable leverage and constrains alignment options — analytically distinct from the criminal economy per se.

**Criterion 4 — Pipeline source interpretation of corruption reporting:** *Not addressed.* Anti-corruption campaigns are frequently weapons in intra-elite competition. The pipeline needs to know this dynamic to contextualize corruption-related articles.

---

### Section 10: Information Ecosystem & Media Structure

**Review perspective:** Comparative media systems scholar + press freedom analyst + digital information environment researcher

**Criterion 1 — Beyond formal legal framework:** *Adequately addressed.* The prompt asks about specific mechanisms of state influence and recognizes differential constraint across media types.

**Criterion 2 — Operationally useful source reliability assessments:** *Partially addressed.* The right question is asked but the prompt lacks a structured template forcing outlet-by-outlet assessment with ownership, editorial orientation, and specific topic reliability.

**Criterion 3 — Platform-specific dynamics:** *Partially addressed.* Country-specific platform dominance is acknowledged. Missing: how platform architecture (encryption, algorithms, moderation) shapes the character of political discourse.

**Criterion 4 — Information ecosystem under stress:** *Partially addressed.* Good sub-questions about crisis behavior. Missing: requirement to anchor patterns in specific historical episodes with enough detail for pattern recognition.

---

### Section 11: International Institutional Commitments & Legal Frameworks

**Review perspective:** International institutional law scholar + foreign policy constraints analyst + regional integration specialist

**Criterion 1 — Binding vs. cheap talk distinction:** *Adequately addressed, minor gap.* The binding/aspirational distinction is strong. Missing: explicit requirement to identify specific enforcement mechanisms for each commitment.

**Criterion 2 — Domain-level institutional lock-in:** *Partially addressed.* The right question is asked but the prompt does not push for domain-by-domain disaggregation of constraint strength.

**Criterion 3 — Defection cost disaggregation:** *Partially addressed.* Defection costs treated as a single variable. Should disaggregate into economic, security, political, and institutional costs to identify binding constraint category.

**Criterion 4 — Institutional reform dimension:** *Adequately addressed.* Dedicated sub-section with right framing. Could be enhanced by requiring identification of specific named reform positions.

**Criterion 5 — Competing institutional frameworks:** *Partially addressed.* BRICS/SCO/AIIB mentioned as realignment destinations but not analyzed as concurrent memberships creating tensions. Missing: framework for dual-membership contradictions.

---

### Section 12: Military & Security Sector DNA

**Review perspective:** Civil-military relations scholar + country/regional defense analyst + intelligence services analyst

**Criterion 1 — Military economic interests:** *Partially addressed.* "Economic footprint" identified as a question but treated as one list item. Not analyzed as a structural force shaping institutional behavior, reform resistance, and regime stability.

**Criterion 2 — Conventional military vs. internal security services:** *Not adequately addressed.* The prompt treats "military and security services" as a combined category. Misses the critical structural feature of inter-institutional rivalry (IRGC vs. Artesh, FSB vs. GRU, etc.).

**Criterion 3 — Security sector behavior under stress:** *Partially addressed.* "Institutional redlines" is the right concept but treats intervention as binary. Should analyze a spectrum from behind-the-scenes influence through institutional neutrality to outright seizure of power.

**Criterion 4 — Doctrinal orientation specificity:** *Partially addressed.* Too compressed ("conventional defense, internal security, expeditionary capability") to enable pipeline interpretation of procurement decisions, exercises, or deployments.

---

### Section 13: History of Dissent & Civil Society Infrastructure

**Review perspective:** Civil society and social movements scholar + democratization/authoritarian resilience scholar

**Criterion 1 — Current organizational capacity vs. historical infrastructure:** *Partially addressed.* Good list of historical dissent-absorbing institutions. Missing: explicit instruction to assess current operational capacity — institutions that channeled opposition historically may be hollowed out, co-opted, or banned.

**Criterion 2 — Co-optation dimension:** *Not adequately addressed.* The prompt focuses on institutions that absorb dissent and on forms of dissent. Missing: GONGOs, patronage absorption, managed opposition, channeling dissent into controlled outlets — often more consequential than repression.

**Criterion 3 — Robust pluralistic civil society:** *Partially addressed.* The framing tilts toward repressive contexts ("where the next revolution would likely be incubated"). Inadequate for established democracies where civil society operates through institutional channels.

**Criterion 4 — Transnational civil society connections:** *Not addressed.* "Diaspora networks" mentioned but international NGO networks, foreign-funded democracy promotion, transnational advocacy networks, and "foreign agent" legislation dynamics are absent.

---

### Section 14: Patron-Client History & Alliance Genealogy

**Review perspective:** Alliance politics scholar + US foreign policy specialist + country-specific diplomatic historian

**Criterion 1 — Granularity of US dependency analysis:** *Partially addressed.* The US-specific paragraph identifies multiple dependency dimensions (security guarantees, trade access, institutional backing, technology transfer) and distinguishes between retrenchment, hostility, and institutional disengagement. Missing: disaggregation into component dimensions with separate vulnerability assessment for each.

**Criterion 2 — Pivot option skepticism:** *Partially addressed.* "Realistic" and "at what cost" push toward hard-nosed assessment. Missing: explicit feasibility test (capability, willingness, institutional infrastructure of alternatives).

**Criterion 3 — Domestic politics of alignment:** *Not adequately addressed.* Focus is almost entirely on external strategic dimension. Missing: which domestic constituencies benefit from current alignment, who would benefit from realignment, and what domestic political costs shifting would incur.

**Criterion 4 — Multi-vector foreign policies:** *Not adequately addressed.* The prompt's patron-client framing assumes binary alignment. Missing: framework for countries (India, Turkey, UAE, Gulf states) that deliberately maintain relationships with competing powers.

---

### Section 15: Constitutional Crises & Regime Transition Patterns

**Review perspective:** Comparative regime transition scholar + country-specific political scientist + leadership analysis specialist

**Criterion 1 — Cyclical pattern specificity:** *Partially addressed.* The prompt asks for cyclical patterns and periodicity but does not force identification of the structural tension driving the cycle, the trigger mechanism, or the current position within the cycle with enough specificity to be predictive.

**Criterion 2 — Leadership environment without psychological speculation:** *Largely addressed.* The calibration note is well-crafted. Minor gap: no explicit two-tier distinction between institutional observables (higher confidence) and behavioral inferences (requiring evidence from multiple episodes).

**Criterion 3 — Succession question:** *Partially addressed.* Buried in a parenthetical list ("succession planning or its absence") alongside health and financial exposure. Deserves dedicated analytical treatment covering institutional mechanisms, candidate identification, factional alignments, and scenario assessment.

**Criterion 4 — Democratic backsliding mechanisms:** *Not addressed.* The prompt's regime transition typology (elections, coups, dynastic succession, negotiated pacts, revolution, state collapse) captures discontinuous transitions but entirely misses gradual authoritarian erosion within formally democratic structures — the most relevant pattern for the democratic middle powers this pipeline monitors.

---

### Section 16: Collective Memory of Humiliation & Grievance

**Review perspective:** Collective memory and nationalism scholar + country-specific historian + strategic culture analyst

**Criterion 1 — Genuinely constraining vs. instrumentally deployed:** *Partially addressed.* "Genuinely popular or elite-manufactured" is the right question but uses a binary frame that misses the spectrum. Missing: assessment of constraint strength in operational terms (what domestic political cost would a leader face for conceding on the associated issue?).

**Criterion 2 — Western analytical blind spot specificity:** *Partially addressed.* The prompt asks the LLM to identify where Western frameworks misread redlines but does not require specific examples, specific explanations of why the misreading occurs, or corrective guidance for the pipeline.

**Criterion 3 — Competing grievance narratives:** *Not adequately addressed.* The prompt uses plural language but implicitly assumes a single dominant national narrative. Missing: explicit requirement to map which factions champion which narratives and what is at stake in the contest.

**Criterion 4 — Grievance-to-geopolitical-positioning interaction:** *Partially addressed.* "How they map onto current geopolitical disputes" is too vague. Missing: explicit causal tracing from historical memory to current alliance behavior, threat perception, and willingness to bear costs for collective action.

---

### Section 17: Cross-Facet Intersection Analysis

**Review perspective:** Senior area studies generalist + complex systems/political risk analyst

**Criterion 1 — Non-obvious vs. self-evident intersections:** *Partially addressed.* "Prioritize non-obvious intersections" stated but no concrete example of target depth or discriminator between obvious and non-obvious. Without an example, the LLM will default to commonly discussed intersections.

**Criterion 2 — Predictive utility for pipeline:** *Partially addressed.* The prompt asks for analytical implications but does not require operational specificity (e.g., "when the pipeline encounters [event type], it should assess [intersection-driven dynamic] rather than [surface interpretation]").

**Criterion 3 — Maximum analytical distance:** *Not adequately addressed.* No structural incentive to range across distant facets. The LLM will gravitate toward adjacent-section connections rather than the cross-domain intersections that constitute the analytical value-add.

---

### Section 18: Key Analytical Judgments

**Review perspective:** Senior intelligence analyst (structured analytical tradecraft) + country specialist

**Criterion 1 — Actual falsifiability:** *Partially addressed.* The prompt specifies falsifiability and temporal bounding but provides no example of the target format. Without an example showing explicit falsification conditions, judgments will be directionally correct but operationally unfalsifiable.

**Criterion 2 — Appropriate confidence calibration:** *Partially addressed.* Confidence markers defined at the general prompt level. Missing: guidance tying confidence levels to evidence quality (converging structural indicators vs. sound logic with gaps vs. analytical inference from structural conditions).

**Criterion 3 — Structurally grounded rather than current-news-driven:** *Adequately addressed, could be reinforced.* "Derived from the facets above, not from current news" is the right instruction. Could benefit from a test: would this judgment remain valid if the specific individuals in power were replaced by different individuals from the same structural position?

---

### Section 19: Watch Indicators

**Review perspective:** Intelligence collection/indicators specialist + OSINT analyst + country specialist

**Criterion 1 — Observable through open sources:** *Partially addressed.* Good example provided ("officer corps purge reaching brigade command level"). Missing: specification of the observation channel — where/how each indicator would become visible (government gazette, central bank reports, opposition media, satellite imagery).

**Criterion 2 — Right sensitivity level:** *Not adequately addressed.* No calibration guidance distinguishing leading indicators (early signals with uncertainty) from confirming indicators (clear signals with less lead time). No trigger thresholds distinguishing signal from noise.

**Criterion 3 — Mapping back to specific sections with mechanism:** *Partially addressed.* The prompt requires section references and description of suggested shift. Missing: mapping to specific STRUCTURAL CLAIMS and mechanistic explanation of what reassessment the pipeline should initiate if the indicator fires.

---

### Section 20: Pipeline Integration Notes

**Review perspective:** NLP/computational social scientist + country-specialist journalist + intelligence fusion analyst

**Criterion 1 — Operationally useful source interpretation guidance:** *Partially addressed.* The right connection to Section 10 is established. Missing: conditional-rule format ("IF article from [source] about [topic], THEN [specific adjustment]") rather than prose discussion of media bias.

**Criterion 2 — Event significance thresholds:** *Adequately addressed, could be strengthened.* 3-5 examples of each is reasonable. Missing: pattern-level rather than instance-level framing so examples remain useful for novel events.

**Criterion 3 — LLM-specific misreading patterns:** *Not addressed.* The prompt asks about common analytical errors by outside observers but does not address LLM-specific tendencies (recency bias, Western-framework imposition, false equivalence, over-weighting dramatic events, under-weighting structural continuity).

**Criterion 4 — Cross-leader connection points:** *Partially addressed.* The right question is asked but "most frequently interact with" is too loose. Missing: structural significance over frequency, routine-vs-significant thresholds, and tension points for each bilateral relationship.

---

## Cross-Cutting Observations

1. **Mechanism specificity is the most consistent gap.** The v2 prompt names the right analytical topics but does not force the LLM to trace causal chains from structural feature to political outcome through specific mechanisms. This produces description rather than analysis across sections 1, 2, 4, 5, 8, and 16.

2. **Forward-looking trajectory analysis is weak.** Sections 7 and 8 especially suffer from backward-looking orientation — they analyze inherited structures and existing conditions but not the trajectory of change or what current investments reveal about future orientation.

3. **Digital dimensions are systematically underrepresented.** Section 7 omits digital infrastructure entirely. Section 10 partially addresses platform dynamics. For a dossier designed to remain relevant through the late 2020s, this is a notable blind spot.

4. **Pipeline operationalization is inconsistent.** Some sections (0, 9, 20) include pipeline-specific guidance. Others (5, 8, 12) do not specify how their analysis should be consumed by the pipeline. The v3 prompt should ensure every section includes enough operational framing for pipeline consumption.

5. **Calibration for country diversity is uneven.** Section 9's escape valve is a model for how to handle variable relevance. Other sections (4, 13) lack similar accommodations for countries where their analytical frame does not apply.

6. **Democratic erosion is the biggest single topical gap.** Given the pipeline's focus on democratic middle powers, the absence of gradual democratic backsliding mechanisms from Section 15 is the most consequential omission.

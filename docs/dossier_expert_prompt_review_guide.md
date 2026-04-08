# Structural Country Dossier — Expert Prompt Review Guide

## Purpose

This document guides expert review of the **prompt itself**, not the output. The question for each reviewer is: **would these instructions elicit the right analysis from an LLM, or are the questions missing, misframed, or pointed at the wrong things?**

Each section below identifies the expert perspective needed and the specific evaluation criteria they should apply to the prompt's instructions for that section.

---

## Section 0: Key Actors & Institutions Primer

**Review perspective:** Country/regional political analyst + political risk analyst

**Evaluate whether the prompt:**

- Specifies enough categories of actors, or whether the suggested categories (state institutions, political parties, security actors, economic actors, non-state/civil society, external actors) miss actor types that are structurally important in certain country contexts. For instance: does the prompt adequately surface religious authorities in countries where they hold constitutional or de facto veto power? Tribal or clan leaders in countries where sub-state governance structures carry more weight than formal institutions? Royal courts or monarchies where they exist as parallel power structures?
- Would produce entries that explain *structural function* rather than just organizational description. The prompt asks for "why it matters structurally" — but does it give the LLM enough guidance to distinguish between an institution's formal mandate and its actual political role? A country's constitutional court might formally exist to adjudicate law but functionally serve as a regime legitimation tool or an opposition veto point — the prompt should force that distinction.
- Accounts for the fact that actor maps are the most rapidly outdated section. Does the prompt instruct the LLM to flag which actors are institutionally stable (will persist across governments) versus which are regime-specific (will change with the next transition)? This distinction matters for a pipeline that will use this glossary for months or years.
- Would produce entries useful for an LLM processing news articles — specifically, would the descriptions allow the pipeline to correctly interpret an article mentioning an actor's name without additional context? If the prompt doesn't specify that alternate names, abbreviations, and media usage patterns should be included, the glossary fails its operational purpose.

---

## Section 1: Formation Trauma & Founding Mythology

**Review perspective:** Historical sociologist specializing in nationalism and collective memory

**Evaluate whether the prompt:**

- Distinguishes between the *historical event* and the *narrative constructed around it*. The prompt asks about founding mythology, but does it sufficiently force the LLM to analyze the gap between what happened and what the state says happened? For many countries, the analytical value lies precisely in that gap — what's suppressed or rewritten reveals more about current political dynamics than the official story.
- Would surface *competing* founding narratives within the same country. Many states have multiple origin stories claimed by different political factions (e.g., France's revolutionary versus monarchist versus Gaullist founding narratives; Turkey's Kemalist founding versus the Ottoman continuity narrative Erdoğan promotes). The prompt mentions "contested" narratives but doesn't explicitly require mapping which political forces champion which version and what's at stake in the contest.
- Asks the right question about *mechanism of transmission*. The prompt mentions "actively maintained, contested, or instrumentalized" — but does it push the LLM to identify the specific institutional channels (school curricula, military training, state media, commemorative calendar, museum curation) through which the narrative reproduces itself? For pipeline purposes, this matters because changes to these channels (e.g., a new government revising school textbooks) are observable indicators of narrative shift.
- Would produce analysis applicable to countries with *multiple formation traumas* layered on top of each other. For post-colonial states with subsequent civil wars, or countries that have been founded, dissolved, and reconstituted (e.g., Poland, the Baltic states), the prompt should force analysis of how these layered traumas interact rather than treating the most recent one as definitive.

---

## Section 2: Geographic Determinism & Persistent Strategic Problems

**Review perspective:** Political geographer + military/defense planner

**Evaluate whether the prompt:**

- Avoids the classic trap of geographic determinism as ideology while still capturing genuine geographic constraints. The prompt asks for "structurally unsolvable" problems, which is the right framing — but does it also ask which problems are *perceived* as geographic constraints but are actually institutional failures? (E.g., a country might frame food insecurity as a geographic problem when it's actually a distribution and governance problem.) The prompt should force the LLM to distinguish between genuine geographic constraints and politically convenient geographic excuses.
- Would surface the *interaction* between geography and technology/infrastructure. Geographic constraints are not static — they're mediated by technology. The English Channel was a defensive moat until air power; pipeline routes transformed energy geography; submarine cables changed information geography. Does the prompt push the LLM to assess which geographic constraints have been partially overcome by infrastructure and which remain binding?
- Adequately addresses the **maritime dimension** for coastal and island states. The prompt mentions "access to maritime trade routes" but doesn't specifically ask about EEZ (Exclusive Economic Zone) claims, maritime boundary disputes, naval chokepoint proximity, or fisheries as a political variable. For many countries (South China Sea claimants, Baltic states, island nations), the maritime dimension is the dominant geographic feature.
- Would produce analysis that captures **proximity to major powers** as a *dynamic* rather than static feature. Being next to Russia means something different in 2026 than it did in 2010. The prompt mentions proximity but doesn't ask the LLM to assess how the strategic implications of that proximity have shifted with changing power dynamics.

---

## Section 3: Imperial Legacy & Institutional Inheritance

**Review perspective:** Comparative colonial institutions scholar + legal historian

**Evaluate whether the prompt:**

- Would surface the **mundane institutional channels** through which imperial legacies persist, not just the political ones. Land registration systems, property law, railway gauge, educational credentialing structures, tax collection models, civil service recruitment patterns — these are often more consequential than the political narratives about imperial legacy because they're invisible and therefore unreformed. Does the prompt push the LLM beyond "the British left parliamentary democracy" to "the British left a specific model of land titling that continues to shape property disputes and agrarian politics"?
- Handles the **temporal layering** problem adequately. The prompt mentions multiple overlapping imperial legacies but doesn't specify how the LLM should analyze their interaction. In practice, later imperial layers don't simply replace earlier ones — they interact. Soviet institutional inheritance in the Baltic states overlays earlier German/Swedish/Russian imperial legacies, and the specific character of post-Soviet state-building was shaped by *which* pre-Soviet institutional memory was available to draw on. The prompt should force analysis of the interaction mechanism, not just the listing of layers.
- Asks about **elite formation pathways** created by imperial systems. Where did the current political elite get educated? What professional networks were established during the imperial period? For post-Soviet states, the question of whether elites were formed through Soviet institutions or through Western-oriented education in the 1990s is structurally significant. The prompt mentions "elite formation" but may not push the LLM to trace specific pathways.
- Would surface cases where the **absence** of institutional inheritance is the relevant feature. Some countries were left with near-zero institutional capacity at independence (e.g., Belgian Congo), and the relevant analysis is about the *gap* rather than the residue. Does the prompt's framing accommodate this?

---

## Section 4: Ethnic, Sectarian & Linguistic Cleavage Structure

**Review perspective:** Comparative ethnic politics scholar + country-specific ethnographer

**Evaluate whether the prompt:**

- Sufficiently guards against the **primordialism trap** — the tendency to treat ethnic and sectarian identities as ancient and fixed rather than politically constructed and historically contingent. The prompt explicitly asks for "how and when they became politically activated," which is the right constructivist framing — but does it push the LLM hard enough to identify the specific *agents* and *mechanisms* of activation? Political entrepreneurs who instrumentalize identity do so through specific institutional channels (party systems, media, patronage networks, census categories), and the prompt should force identification of those channels.
- Would surface **cross-cutting versus reinforcing cleavages**. The political significance of any single cleavage depends on whether other cleavages cut across it (creating complex, coalition-requiring politics) or reinforce it (creating binary, zero-sum politics). Does the prompt ask the LLM to map how cleavages relate to each other, not just to catalog them individually?
- Addresses the **state's institutional response** to cleavage management with sufficient specificity. The prompt mentions "whether the state's institutional design manages or exacerbates them" — but does it push the LLM to identify the specific mechanisms? Federalism, consociationalism, electoral system design, language policy, affirmative action, decentralization — these are concrete institutional choices with specific effects, and the prompt should elicit analysis of which mechanisms are in use and how well they function.
- Would handle countries where the **salient cleavage isn't ethnic, sectarian, or linguistic** at all. In some countries, the dominant political cleavage is urban-rural, class-based, regional, generational, or ideological rather than identity-based. The prompt's framing might inadvertently push the LLM to find ethnic cleavages where the structural analysis should focus elsewhere. Does the prompt allow for the conclusion that identity cleavages are not the primary political fault line?

---

## Section 5: Demographic Tides & Generational Dynamics

**Review perspective:** Political demographer + migration studies scholar

**Evaluate whether the prompt:**

- Would produce analysis that connects demographic structure to **specific political outcomes** rather than generating demographic description. The prompt asks for "political implications" but does it push the LLM to specify *mechanisms*? A youth bulge doesn't automatically produce instability — it produces instability through specific channels (labor market failure, housing unaffordability, frustrated expectations) that depend on the economic and institutional context described in other sections. The prompt should force the LLM to identify those mechanisms rather than asserting demographic determinism.
- Adequately addresses **emigration and brain drain** as a structural feature with political consequences. For many of the countries MPM tracks (Baltic states, Poland), the post-accession emigration wave to Western Europe has had profound demographic, economic, and political effects — labor shortages, remittance dependency, diaspora voting patterns, and the political salience of emigration as a grievance. Does the prompt push the LLM to analyze emigration as a structural force rather than just noting that it occurs?
- Would surface the **political economy of aging** for countries where that's the dominant demographic trend. Pension system sustainability, healthcare cost trajectories, intergenerational fiscal transfers, and the political power of elderly voting blocs are structural features that shape what governments can spend on defense and foreign policy. For European middle powers, the aging demographic is arguably more consequential than any identity cleavage — does the prompt weight it accordingly?
- Asks about **diaspora political influence** as a distinct phenomenon. For some countries (Israel, Ireland, Armenia, Ukraine, Mexico), the diaspora exercises significant political influence through lobbying, remittances, return migration, and voting rights. This is analytically distinct from migration patterns and deserves specific attention — does the prompt surface it?

---

## Section 6: Economic Structure, Financial Architecture & Dependency Patterns

**Review perspective:** Political economist + international financial economist + trade economist

**Evaluate whether the prompt:**

- Would produce analysis that captures the **state-business relationship** with enough specificity to be useful for interpreting events. "Oligarchic capture" and "state capitalism" are useful categories but they describe a spectrum. Does the prompt push the LLM to identify *specific actors and mechanisms* — which firms or conglomerates have political leverage, through what channels (party financing, media ownership, revolving door appointments, regulatory capture), and what policy domains they influence? When the pipeline processes an article about a policy decision, it needs to know who benefits and who loses.
- Handles the **financial architecture** addition with sufficient analytical depth. The prompt now includes central bank independence, currency regime, sovereign debt, and sanctions exposure — but does it push the LLM to explain *how* these create binding constraints rather than just listing features? The analytical value is in statements like "eurozone membership eliminates monetary policy discretion, which means France cannot devalue its way out of competitiveness problems and must instead pursue internal devaluation (wage suppression, austerity) with all the domestic political consequences that entails." Does the prompt force that level of causal specificity?
- Would surface **trade dependency as a geopolitical lever** with enough granularity to be operationally useful. "Key trading partners" is too vague — the prompt should elicit analysis of *specific commodity dependencies* that create leverage (e.g., which countries depend on Russian gas, Chinese rare earths, or American technology access in ways that constrain their foreign policy). The pipeline needs to know which trade relationships are structural constraints and which are merely large.
- Adequately addresses the **informal economy** for countries where it's politically significant. In countries where 30-60% of economic activity is informal, formal economic statistics systematically misrepresent the state-society bargain. Does the prompt push the LLM to assess whether the formal economic structure described is actually representative of how the economy functions?

---

## Section 7: Infrastructural Inheritance & Resource Pathways

**Review perspective:** Infrastructure historian + energy security analyst

**Evaluate whether the prompt:**

- Would surface the **political intentionality** embedded in infrastructure rather than treating it as neutral. The prompt's framing ("who were they built to connect, and for whose benefit?") is the right question — but does it push the LLM to carry this analysis forward to the present? Infrastructure built for colonial extraction often still orients economic flows outward even after political independence. The prompt should force analysis of whether current infrastructure investment is reinforcing or reorienting inherited dependency patterns.
- Adequately addresses **energy infrastructure as a geopolitical variable**. For European countries especially, pipeline routes, LNG terminal capacity, grid interconnections, and nuclear power dependency are among the most consequential structural features shaping foreign policy autonomy. Does the prompt push the LLM to map these dependencies with enough specificity that the pipeline can interpret energy policy events (e.g., a new LNG terminal, a pipeline agreement, a nuclear plant closure) in structural context?
- Would surface **digital infrastructure dependency** as a distinct concern. Submarine cable routes, data center locations, cloud service provider dependency, and telecommunications equipment supply chains (the Huawei question) are increasingly consequential structural features. Does the prompt address this, or does it focus primarily on physical transportation and energy infrastructure?
- Asks about infrastructure as an **indicator of strategic reorientation**. Major infrastructure investments signal long-term strategic intent — a new port facing a different direction, a railway connecting to a new partner, a pipeline bypassing a former patron. The prompt should push the LLM to identify which current infrastructure projects would, if completed, represent structural reorientation versus which merely reinforce existing patterns.

---

## Section 8: Environmental & Climatic Structure

**Review perspective:** Environmental security scholar + climate scientist with regional expertise

**Evaluate whether the prompt:**

- Would produce analysis that connects environmental conditions to **specific political mechanisms** rather than vague assertions about "climate as a threat multiplier." The prompt asks about the relationship between environmental conditions and political stability, but does it push the LLM to identify the specific causal pathways? Water scarcity doesn't automatically produce conflict — it produces conflict through specific mechanisms (competition over irrigation allocation, displacement of pastoral communities, urban migration from failed agricultural areas) that depend on institutional capacity and existing cleavages. The prompt should force identification of those pathways.
- Addresses **transboundary environmental dependencies** with enough specificity. The prompt mentions "transboundary river dependencies" but does it push the LLM to identify the specific upstream-downstream power dynamics, the institutional frameworks (treaty-based or ad hoc) managing shared resources, and the realistic escalation scenarios? For countries where water security is a strategic variable (Central Asia, the Nile basin, the Mekong), this is a structural constraint on par with military geography.
- Would surface **environmental policy as a political variable** in the specific context of middle power coordination. For MPM's purposes, the analytical question isn't just "is this country vulnerable to climate change" but "how does this country's environmental position shape its stance in international climate negotiations, and does climate policy create tensions with other aspects of liberal order defense?" (E.g., a country dependent on fossil fuel exports may be a strong defender of liberal order on security issues but an obstructionist on climate.) Does the prompt elicit this kind of cross-domain tension?
- Avoids **environmental determinism** while still capturing genuine environmental constraints. Does the prompt distinguish between environmental conditions that are genuinely binding (water scarcity in an arid region, sea-level rise for a low-lying island) and environmental conditions that are mediated by institutional capacity (a wealthy country can desalinate water; a poor one cannot)?

---

## Section 9: Illicit Networks & Shadow Governance

**Review perspective:** Organized crime and illicit economies researcher + governance specialist

**Evaluate whether the prompt:**

- Successfully solves the **calibration problem** — preventing the LLM from generating extensive analysis of criminality for countries where it's structurally peripheral while ensuring sufficient depth for countries where it's structurally central. The escape valve ("STRUCTURAL RELEVANCE: LOW") is designed for this, but does the prompt give the LLM sufficient criteria to make that determination? What distinguishes a country where organized crime is a law enforcement problem from one where it's a governance feature? The prompt should provide clearer decision criteria.
- Would surface the **state-criminal integration spectrum** with enough granularity. The prompt lists the spectrum from "hostile enforcement through tolerant coexistence to active symbiosis" — but does it push the LLM to identify where a specific country sits on that spectrum with evidence, rather than asserting it categorically? The difference between "the state tolerates drug trafficking" and "specific military units manage drug logistics for a percentage of profits" is analytically enormous, and the prompt should force that level of specificity where evidence supports it.
- Addresses **illicit financial flows as a structural constraint on foreign policy**. For countries where elite wealth is parked in specific foreign jurisdictions (London real estate, Swiss banking, Dubai property), those financial dependencies create leverage and constrain alignment options. Does the prompt push the LLM to identify these specific transnational financial dependencies?
- Would produce analysis useful for the **pipeline's source interpretation**. Investigative journalism about corruption and organized crime is often politically motivated — anti-corruption campaigns are frequently weapons in intra-elite competition rather than genuine reform efforts. Does the prompt push the LLM to flag this dynamic so the pipeline can interpret corruption-related reporting in political context?

---

## Section 10: Information Ecosystem & Media Structure

**Review perspective:** Comparative media systems scholar (Hallin & Mancini tradition) + press freedom analyst + digital information environment researcher

**Evaluate whether the prompt:**

- Would produce a media system classification that goes beyond the **formal legal framework** to capture how information actually flows. Many countries have constitutionally guaranteed press freedom that is operationally meaningless due to ownership concentration, advertising revenue manipulation, or informal state pressure. Does the prompt push the LLM to analyze the *de facto* information environment rather than the *de jure* one?
- Generates **operationally useful source reliability assessments** for the pipeline. This is the most practically consequential part of the entire section. The prompt asks for assessments of "which outlets are reliably independent, which function as government mouthpieces, which represent specific opposition or factional perspectives" — but does it push the LLM to be specific enough that these assessments can actually inform source weighting? A useful assessment says "Gazeta Wyborcza is editorially independent but has a consistent liberal-cosmopolitan orientation that shapes its coverage of PiS-era judiciary reforms; TVP under PiS management functioned as a government propaganda outlet; Onet occupies a centrist position but is owned by Ringier Axel Springer, introducing specific commercial incentives." Does the prompt elicit that level of specificity?
- Adequately addresses the **platform-specific dynamics** of the digital information environment. The prompt asks about "which platforms dominate political discourse" — but does it push the LLM to analyze *how* platform architecture shapes political information flows? Telegram's encryption and channel structure functions differently from Twitter/X's public discourse model, which functions differently from Facebook group dynamics. For the pipeline, knowing *where* political discourse happens affects where to look for signals.
- Would surface how the **information ecosystem behaves under stress** with enough specificity to be predictive. The prompt asks about crisis behavior, but does it push the LLM to identify specific historical precedents with enough detail that the pipeline can recognize similar patterns in incoming events? "The state imposes information blackouts" is less useful than "during the [specific crisis], the government ordered ISPs to throttle specific platforms within [timeframe], which triggered a shift to [alternative channels], which the diaspora used to [specific function]."

---

## Section 11: International Institutional Commitments & Legal Frameworks

**Review perspective:** International institutional law scholar + foreign policy constraints analyst + regional integration specialist

**Evaluate whether the prompt:**

- Successfully distinguishes between **binding constraints and cheap talk** — which is the core analytical question. The prompt explicitly asks for this distinction, but does it give the LLM sufficient criteria to make the assessment? The difference between a binding constraint and an aspirational commitment often lies in the enforcement mechanism: EU acquis compliance is enforced by the ECJ and the Commission with real sanctions; UN General Assembly resolutions are not. Does the prompt push the LLM to identify the specific enforcement mechanisms (or their absence) for each commitment?
- Would surface the **institutional lock-in effects** that actually constrain behavior. For EU member states, the acquis communautaire constrains policy across dozens of domains — but the constraints are unevenly binding. EU fiscal rules constrain budgets (in theory); EU defense policy barely constrains anything. Does the prompt push the LLM to assess which domains of institutional constraint are actually binding versus which are routinely circumvented or unenforceable?
- Addresses the **defection cost analysis** with sufficient rigor. The prompt asks about defection costs, but does it push the LLM to be specific about *what kinds* of costs? There are economic costs (loss of market access, credit rating downgrade, investment flight), security costs (loss of alliance guarantees), political costs (domestic backlash, loss of international status), and institutional costs (loss of voice and vote in organizations where the country has influence). A useful defection cost analysis disaggregates these rather than treating them as a single variable.
- Would surface the **institutional reform dimension** that's specifically relevant to MPM's thesis. Middle powers defending liberal international order aren't just complying with existing institutions — some are actively trying to reform them to be more effective or to fill gaps left by American withdrawal. Does the prompt push the LLM to identify whether a country is an institutional status quo defender, reformer, or revisionist, and what specific reform positions it champions?
- Handles the **competing institutional frameworks** problem. Some countries are simultaneously embedded in Western institutional frameworks and participating in alternative structures (BRICS, SCO, AIIB). Does the prompt push the LLM to analyze how dual membership creates tensions and constraints, rather than treating institutional memberships as a simple list?

---

## Section 12: Military & Security Sector DNA

**Review perspective:** Civil-military relations scholar + country/regional defense analyst + intelligence services analyst

**Evaluate whether the prompt:**

- Would surface the military's **economic interests** as a distinct analytical dimension. In many countries, the military owns significant economic assets (factories, land, pension funds, commercial enterprises) that create institutional interests independent of and sometimes in tension with the military's security mission. Does the prompt push the LLM to assess the scale and character of military economic activity and how it shapes institutional behavior? A military that owns 15% of the national economy behaves differently under reform pressure than one that subsists on budget allocations.
- Adequately distinguishes between the **conventional military and internal security services**. In many countries, these are distinct institutions with different institutional cultures, political roles, and loyalties. The prompt asks about "military and security services" as a combined category — but does it push the LLM to analyze the relationship *between* these institutions? In countries where the internal security service and the military are institutional rivals (e.g., Iran's IRGC vs. regular military, or the historical tension between intelligence services and armed forces in many post-Soviet states), that rivalry is a structural feature with significant implications.
- Would produce analysis useful for **predicting security sector behavior under stress**. The prompt asks about "likely behavior under regime stress," which is the right question — but does it push the LLM to be specific about what kinds of stress trigger what kinds of behavior? Military intervention in politics is not a binary (coup/no coup) but a spectrum ranging from behind-the-scenes influence through public statements to institutional defection to outright seizure of power. Does the prompt force analysis along this spectrum?
- Addresses **doctrinal orientation** with enough specificity to interpret defense policy events. When the pipeline processes an article about a military exercise, a procurement decision, or a deployment, the dossier should provide context for interpreting what it means. Does the prompt push the LLM to characterize doctrine concretely enough to serve this purpose?

---

## Section 13: History of Dissent & Civil Society Infrastructure

**Review perspective:** Civil society and social movements scholar + democratization/authoritarian resilience scholar

**Evaluate whether the prompt:**

- Would surface the **institutional infrastructure of opposition** rather than just the history of protest events. The prompt asks about "which institutions historically absorb dissent" — but does it push the LLM to analyze the *current* organizational capacity of civil society, not just its historical role? For pipeline purposes, the relevant question is: if a political crisis erupts next month, what organizational infrastructure exists to channel dissent, and who controls it?
- Addresses the **co-optation dimension** — how regimes manage civil society through absorption rather than repression. Many governments create GONGOs (government-organized non-governmental organizations), co-opt opposition leaders into patronage networks, or channel dissent into harmless institutional outlets. Does the prompt push the LLM to map these co-optation mechanisms alongside repressive ones?
- Would handle countries where **civil society is genuinely robust and pluralistic** as well as countries where it's repressed or nascent. The prompt's framing tilts slightly toward contexts where dissent is managed by the state — does it also accommodate analysis of countries (like many European democracies) where civil society infrastructure is extensive, professionalized, and operates through institutional channels (NGOs, think tanks, labor unions, professional associations) rather than through protest mobilization?
- Asks about **transnational civil society connections** — diaspora organizations, international NGO networks, foreign-funded democracy promotion organizations — that function as alternative channels of influence and support. For countries where domestic civil society is constrained, transnational connections often provide resources, protection, and international visibility. Does the prompt surface this?

---

## Section 14: Patron-Client History & Alliance Genealogy

**Review perspective:** Alliance politics scholar + US foreign policy specialist + country-specific diplomatic historian

**Evaluate whether the prompt:**

- Would produce analysis of **American dependency** that is granular enough to assess the impact of different modes of American withdrawal. "American retrenchment" is not monolithic — withdrawal from security guarantees, trade hostility, institutional disengagement, and active undermining of multilateral institutions are distinct dynamics with different impacts on different countries. Does the prompt push the LLM to disaggregate the US dependency relationship into its component parts and assess vulnerability to each mode of withdrawal separately?
- Addresses the **realistic pivot options** question with sufficient skepticism. The prompt asks about who the country "could realign toward, at what cost" — but does it push the LLM to assess whether proposed alternatives are actually viable rather than merely theoretically possible? "Europe could pivot toward China for security" is a common analytical assertion that doesn't survive scrutiny when you examine the actual capability, willingness, and institutional infrastructure required. The prompt should force hard-nosed assessment of pivot feasibility.
- Would surface **the domestic politics of alignment choices**. Alliance shifts are not just strategic calculations — they're domestic political events with winners and losers. Does the prompt push the LLM to analyze which domestic constituencies benefit from the current alignment, which would benefit from realignment, and what the political costs of shifting would be for the government?
- Handles **multi-vector foreign policies** — countries that deliberately maintain relationships with competing powers to maximize autonomy. For countries like India, Turkey, or (potentially) some of the middle powers MPM tracks, the analytical frame isn't "aligned with X" but "maintaining strategic ambiguity between X and Y." Does the prompt accommodate this pattern?

---

## Section 15: Constitutional Crises & Regime Transition Patterns

**Review perspective:** Comparative regime transition scholar + country-specific political scientist + leadership analysis/decision-making specialist

**Evaluate whether the prompt:**

- Would produce analysis of **cyclical patterns** that is specific enough to be predictive. The prompt asks the LLM to "look for cyclical patterns and their periodicity" — but does it push for enough specificity about what drives the cycle? A useful cyclical analysis identifies the specific structural tensions that build toward crisis, the typical triggers that convert latent tension into acute crisis, and the institutional mechanisms that either resolve or escalate the crisis. The prompt should force identification of where in the cycle the current regime sits.
- Handles the **leadership environment analysis** without drifting into psychological speculation. The calibration note is well-designed for this, but does the prompt give the LLM enough concrete guidance about what observable indicators to focus on? "Decision-making centralization" is assessable from institutional structure; "risk appetite" requires inference from past behavior. Does the prompt adequately distinguish between what can be observed and what must be inferred, and does it require appropriate confidence calibration for each?
- Would surface the **succession question** with appropriate analytical rigor. For every leader, the succession scenario is one of the most consequential structural uncertainties — yet it's also one of the most speculative. Does the prompt push the LLM to identify what is actually knowable about succession dynamics (institutional mechanisms, potential successors' positions, factional alignments) versus what is genuinely uncertain, and to flag the uncertainty honestly?
- Addresses the **democratic backsliding** pattern specifically, given MPM's focus on democratic middle powers. Several of the tracked leaders govern countries with recent or ongoing experiences of democratic erosion (Poland's judiciary crisis, Hungary as a regional cautionary tale). Does the prompt push the LLM to analyze the specific mechanisms of democratic erosion and the institutional safeguards (or their absence) that constrain or enable it?

---

## Section 16: Collective Memory of Humiliation & Grievance

**Review perspective:** Collective memory and nationalism scholar + country-specific historian + strategic culture analyst

**Evaluate whether the prompt:**

- Would distinguish between **genuinely constraining** grievance narratives and **instrumentally deployed** ones. This is the hardest analytical challenge in the section. Some national grievances are so deeply embedded that they function as genuine political redlines even leaders can't cross (e.g., the "century of humiliation" narrative in China). Others are cynically deployed when convenient and quietly shelved when inconvenient. Does the prompt push the LLM to assess which category applies, with evidence?
- Addresses the **Western analytical blind spot** problem with enough specificity. The prompt asks the LLM to identify "where Western or external analytical frameworks systematically misread these redlines" — but does it push for specific examples of misreading rather than a vague assertion that the West doesn't understand? A useful analysis says "Western analysts consistently interpret [country's] response to [issue] as strategic bluffing because they discount the [specific narrative] — but the domestic political cost of conceding on this issue is genuinely prohibitive because [mechanism]."
- Would surface **competing grievance narratives** within the same country. Different political factions often mobilize different historical traumas for different purposes. The prompt might lead the LLM to identify a single dominant grievance narrative when the analytically significant feature is the *competition* between narratives. Does the prompt accommodate this?
- Asks about the **interaction between grievance narratives and current geopolitical positioning**. For MPM's purposes, the key question is: how do historical grievance narratives shape this country's stance on current issues of liberal order defense? Does historical humiliation by Russia make a country a more committed NATO ally, or does historical betrayal by Western allies make it skeptical of multilateral commitments? The prompt should force analysis of this connection.

---

## Section 17: Cross-Facet Intersection Analysis

**Review perspective:** Senior area studies generalist + complex systems/political risk analyst

**Evaluate whether the prompt:**

- Would produce **genuinely non-obvious intersections** rather than self-evident ones. The prompt requires "at least five" intersections and asks for non-obvious ones to be prioritized — but does it give the LLM enough guidance to distinguish between a non-obvious intersection and a self-evident one? "Geography affects military strategy" is self-evident; "the specific character of imperial-era land registration systems interacts with current ethnic cleavage activation through property dispute mechanisms" is non-obvious. The prompt might benefit from an example of the target analytical depth.
- Would produce intersections with **predictive utility for the pipeline**. Each intersection should include "what does this tell the pipeline LLM to watch for in incoming events" — but does the prompt push the LLM to be specific enough that the pipeline can actually operationalize it? A useful intersection statement ends with something like "when reporting surfaces on [observable event type], the pipeline should assess whether it represents [intersection-driven dynamic] rather than interpreting it at face value."
- Pushes for intersections that **span the maximum analytical distance**. The most valuable intersections connect facets that analysts typically treat as separate domains — e.g., how demographic aging (Section 5) intersects with military doctrine (Section 12) through recruiting constraints. Does the prompt incentivize cross-domain connections rather than within-domain refinements?

---

## Section 18: Key Analytical Judgments

**Review perspective:** Senior intelligence analyst (structured analytical tradecraft) + country specialist

**Evaluate whether the prompt:**

- Would produce judgments that are actually **falsifiable**. The prompt specifies falsifiability, but does it give the LLM enough guidance about what makes a judgment falsifiable? "Poland will continue to prioritize NATO alliance" is not falsifiable in any useful timeframe. "Poland's defense spending will remain above 3% of GDP through at least 2028, driven by the structural threat perception described in Sections 2 and 16, regardless of which coalition governs" is falsifiable, temporally bounded, and structurally grounded. Does the prompt push toward the latter?
- Would produce judgments with **appropriate confidence calibration**. The intelligence community has well-developed standards for confidence levels (high, moderate, low) tied to evidence quality and analytical agreement. Does the prompt push the LLM to tie its confidence levels to specific evidence quality rather than using them as vague hedges?
- Requires judgments that are **derived from the structural analysis** rather than from current news. The prompt specifies this, but the temptation to smuggle in current-events-driven judgments is strong. Does the prompt provide enough scaffolding to prevent this?

---

## Section 19: Watch Indicators

**Review perspective:** Intelligence collection/indicators specialist + OSINT analyst + country specialist

**Evaluate whether the prompt:**

- Would produce indicators that are **actually observable through open sources**. The prompt specifies "things an analyst or automated pipeline can actually monitor" and gives a good example ("officer corps purge reaching brigade command level" vs. "military becoming politicized"). But does it push the LLM to think about *where* each indicator would become visible? An observable indicator needs a source — a type of publication, dataset, announcement channel, or reporting pattern where the signal would appear. Does the prompt require the LLM to specify the observation channel?
- Would produce indicators calibrated to the **right sensitivity level**. An indicator that triggers on every minor policy fluctuation is useless (too much noise). An indicator that only triggers when structural change is already obvious is also useless (too late). Does the prompt push the LLM to calibrate indicators to detect *early* signals of structural change — things that would be visible before a structural shift is widely recognized?
- Requires indicators that **map back to specific sections** of the dossier. The prompt asks the LLM to specify which sections each indicator relates to, which is the right approach — but does it push the LLM to explain the *mechanism* by which the indicator connects to structural change? "Indicator X relates to Section 12" is less useful than "Indicator X relates to Section 12 because [observable event] would suggest [specific structural change] in the military's institutional posture."

---

## Section 20: Pipeline Integration Notes

**Review perspective:** NLP/computational social scientist + country-specialist journalist + intelligence fusion analyst

**Evaluate whether the prompt:**

- Would produce **source interpretation guidance** that is operationally useful for an LLM processing articles. The prompt asks for systematic biases and framing patterns — but does it push the LLM to express these in terms the pipeline can act on? A useful guidance statement says "articles from [outlet] about [topic] should be interpreted as reflecting [specific perspective] because [ownership/editorial dynamic]; when this outlet reports [event type], the pipeline should [specific adjustment]." Does the prompt elicit this level of operational specificity?
- Would produce **event significance thresholds** that help the pipeline distinguish signal from noise. The prompt asks for examples of structural continuity versus genuine deviation — but does it push for enough examples (3-5 of each) with enough specificity that the pipeline can generalize from them? The examples need to be pattern-level rather than instance-level so they remain useful as new events occur.
- Addresses **common misreading patterns** that are specifically relevant to LLM-based analysis. LLMs have their own systematic biases when processing geopolitical information — they tend to over-weight dramatic events, under-weight structural continuity, and impose Western analytical frameworks on non-Western contexts. Does the prompt push for misreading patterns that account for these LLM-specific tendencies in addition to general analytical pitfalls?
- Would produce **cross-leader connection points** that are useful for the pipeline's multi-leader architecture. The prompt asks which other monitored leaders this country interacts with — but does it push the LLM to explain the *structural dynamics* driving those interactions rather than just listing bilateral relationships? The pipeline needs to know that a Macron-Tusk meeting is significant in a different way than a Macron-Starmer meeting because of the specific structural dynamics (EU defense integration politics vs. post-Brexit bilateral recalibration) at play.

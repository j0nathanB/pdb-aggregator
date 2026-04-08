# AUDIT SUMMARY: LITHUANIA

**Sources assessed:** 17 recommended + 4 excluded + 4 newly identified = 25 total
**Tier 1 (boost=3):** 3 sources
**Tier 2 (boost=2):** 7 sources
**Tier 3 (boost=1):** 5 sources
**Neutral (no rule):** 7 sources
**Discard:** 3 sources
**Overall assessment:** The curation prompt produced a compact, security-heavy whitelist appropriate for a frontline NATO state. Key changes: (1) promoted LRT to Tier 1 as Lithuania's indispensable source — public broadcaster with English service, free, unblocked, and dominant on defense/security; (2) migrated government sources (lrs.lt, kam.lt, urm.lt, vsd.lt, president.lt, lrv.lt) to LAYER 2 at Tier 2; (3) applied non-English domestic premium to Lithuanian-language sources; (4) flagged four blocked domains — `delfi.lt`, `elta.lt`, `lrytas.lt`, and `vz.lt` — which severely constrains the extractable source pool and elevates the importance of unblocked sources; (5) added missing structural roles: Vilnius Institute for Policy Analysis (VIPA) for think tank depth, ERU/Transparency International Lithuania for anti-corruption watchdog, and the Bank of Lithuania (lb.lt) for economic statecraft.

---

## BOOST ASSIGNMENTS

### Tier 1 — `$boost=3`

**LRT (Lithuanian National Radio and Television)** | `lrt.lt` | Type: `paper_of_record` | Status: `EXISTING`
- **Structural role:** Lithuania's public broadcaster and the single most important source in the whitelist. Functions simultaneously as paper of record, defense/security first-mover, and the only major outlet with a full English-language service (lrt.lt/en). In a country where four of seven major domains are blocked by Anthropic's crawler, LRT's unblocked status makes it structurally irreplaceable.
- **Domain coverage:** All five domains — diplomatic alignment, economic/technological statecraft, security/defense autonomy, institutional engagement, domestic constraints
- **Reasoning:** LRT is the pipeline's primary extraction target for Lithuania. It is free, unblocked, publishes in both Lithuanian and English, and has the deepest defense/security beat of any Lithuanian outlet. Its coverage of VSD threat assessments, NATO force posture, Seimas proceedings, and government policy announcements means it touches every analytical domain. In a media landscape where Delfi, ELTA, Lietuvos rytas, and Verslo zinios are all blocked, LRT absorbs an outsized structural load. Non-English domestic premium applies to its Lithuanian-language content.
- **Extraction note:** Free, no paywall. English service at lrt.lt/en provides pipeline-accessible summaries of Lithuanian-language reporting.

**15min.lt** | `15min.lt` | Type: `paper_of_record` | Status: `EXISTING — PROMOTED`
- **Structural role:** Second-largest news portal in Lithuania. With Delfi blocked, 15min becomes the sole unblocked commercial news portal — it must carry the general-news load that would normally be shared with Delfi.
- **Domain coverage:** All five domains — diplomatic alignment, economic/technological statecraft, security/defense autonomy, institutional engagement, domestic constraints
- **Reasoning:** Under normal conditions, 15min would sit at Tier 2 behind Delfi. But Delfi's blocked status creates a structural vacuum: the pipeline needs at least two general-coverage domestic sources, and 15min is the only remaining unblocked broadsheet-equivalent. Centrist-liberal editorial orientation provides a commercial-media counterpoint to LRT's public-broadcaster voice. Non-English domestic premium applies. Free with ads — fully extractable.

**Siena** | `siena.lt` | Type: `investigative` | Status: `EXISTING — PROMOTED`
- **Structural role:** Lithuania's only dedicated investigative journalism center. OCCRP member. Triggered the PM Paluckas crisis (2025-2026) with financial investigations — the single most consequential domestic-politics story in the current cycle.
- **Domain coverage:** Domestic constraints, economic statecraft, security/defense
- **Reasoning:** In a country with no dedicated defense press and limited investigative infrastructure, Siena fills multiple structural roles simultaneously: investigative outlet, anti-corruption watchdog, and the primary source for stories that expose gaps between official government positions and actual conduct. Its role in the Paluckas crisis demonstrates its ability to move the domestic-constraints needle. Grant-funded independence and OCCRP membership provide credibility. Non-English domestic premium applies. Free and unblocked.

---

### Tier 2 — `$boost=2`

**Laisves TV** | `laisvės.tv / YouTube` | Type: `investigative` | Status: `EXISTING`
- **Structural role:** Video-first investigative outlet that collaborates with Siena on major investigations. Crowdfunded independence. Significant domestic reach through YouTube.
- **Domain coverage:** Domestic constraints, security/defense
- **Reasoning:** Laisves TV and Siena form Lithuania's investigative duopoly — they frequently collaborate and co-publish. Tier 2 rather than Tier 1 because its video-first format limits text extraction for the pipeline, and its investigative output overlaps substantially with Siena (which gets Tier 1 as the text-primary partner). But its independent crowdfunding model and YouTube reach make it a genuine signal source for domestic constraints. Non-English domestic premium applies.
- **Extraction note:** Primary content on YouTube — text extraction may be limited. Monitor for article write-ups on the website.

**BNS Lithuania** | `bns.lt` | Type: `paper_of_record` (wire service) | Status: `EXISTING`
- **Structural role:** Pan-Baltic wire service. Breaks diplomatic and defense stories. Feeds into all major Lithuanian outlets — when BNS breaks a story, it propagates across the ecosystem within minutes.
- **Domain coverage:** All five domains (wire service breadth)
- **Reasoning:** Wire services normally sit at Neutral in the Goggle model (available organically). BNS earns Tier 2 because of Lithuania's blocked-domain problem: with Delfi, ELTA, Lietuvos rytas, and Verslo zinios all blocked, the pipeline has fewer extraction targets than normal. BNS fills the gap as a primary news-breaking source that the pipeline can actually reach. Subscription model may limit extraction depth.
- **Extraction note:** Subscription service. Partial extraction likely — headlines and leads may be accessible.

**Seimas (Parliament)** | `lrs.lt` | Type: `legislative_official` | Status: `EXISTING` — **LAYER 2 MIGRATION**
- **Structural role:** Lithuania's parliament. Committee proceedings, draft legislation, voting records. Essential for tracking defense-spending bills, conscription legislation, foreign-policy resolutions, and coalition dynamics.
- **Domain coverage:** Institutional engagement, domestic constraints, diplomatic alignment
- **Reasoning:** Primary fetch via Layer 2 direct polling. Goggle boost at Tier 2 as belt-and-suspenders fallback. Government sources earn Tier 2 per boost principles. The Seimas is where Lithuania's foreign policy consensus gets tested — votes on defense budgets, NATO commitments, and sanctions packages are primary signals.

**Ministry of National Defence** | `kam.lt` | Type: `government_aligned` | Status: `EXISTING` — **LAYER 2 MIGRATION**
- **Structural role:** Defense procurement announcements, NATO cooperation documents, threat-assessment publications, and military exercise schedules. For a frontline NATO state with rapidly scaling defense spending, this is a high-signal government source.
- **Domain coverage:** Security/defense autonomy, diplomatic alignment
- **Reasoning:** Primary fetch via Layer 2 direct polling. Goggle boost at Tier 2 as fallback. Lithuania's defense ministry is unusually active in public communications compared to peer countries — it publishes detailed procurement announcements, allied force rotation updates, and threat briefings. The curation prompt correctly noted the defense-procurement gap; kam.lt partially fills it from the official side.

**Ministry of Foreign Affairs** | `urm.lt` | Type: `government_aligned` | Status: `EXISTING` — **LAYER 2 MIGRATION**
- **Structural role:** Diplomatic statements, EU/NATO position papers, bilateral agreements, sanctions announcements.
- **Domain coverage:** Diplomatic alignment, institutional engagement
- **Reasoning:** Primary fetch via Layer 2 direct polling. Goggle boost at Tier 2 as fallback. Lithuania's MFA is a primary signal source for the country's diplomatic alignment — its statements on Russia/Belarus, China/Taiwan, and EU policy positions are direct expressions of strategic intent.

**VSD (State Security Department)** | `vsd.lt` | Type: `security_defense` | Status: `EXISTING` — **LAYER 2 MIGRATION**
- **Structural role:** Lithuania's civilian intelligence service. Annual threat assessments are landmark documents — among the most transparent intelligence publications in the EU, explicitly naming Russian and Belarusian threat vectors.
- **Domain coverage:** Security/defense autonomy, domestic constraints
- **Reasoning:** Primary fetch via Layer 2 direct polling. Goggle boost at Tier 2 as fallback. VSD annual threat assessments function as Lithuania's strategic-threat baseline — they shape parliamentary debate, media framing, and public discourse on defense for the entire year. Infrequent publication but extremely high signal-to-noise ratio.

**Government Portal / Presidential Office** | `lrv.lt`, `president.lt` | Type: `government_aligned` | Status: `NEW (from lt.yaml)` — **LAYER 2 MIGRATION**
- **Structural role:** Central government portal (lrv.lt) and presidential office (president.lt). Official statements, cabinet decisions, executive orders.
- **Domain coverage:** All five domains (official source)
- **Reasoning:** Primary fetch via Layer 2 direct polling. Goggle boost at Tier 2 as fallback. These were listed in lt.yaml but not in the source intelligence map — adding them to align the Goggle with the pipeline's actual configuration. Lithuania's semi-presidential system means presidential office communications (president.lt) carry distinct signals from government portal communications (lrv.lt), particularly on foreign policy where President Nauseda has occasionally diverged from the governing coalition.

---

### Tier 3 — `$boost=1`

**The Baltic Times** | `baltictimes.com` | Type: `regional` | Status: `EXISTING`
- **Structural role:** English-language monthly covering all three Baltic states. Provides cross-Baltic comparative framing unavailable in domestic Lithuanian media.
- **Domain coverage:** All five domains (summary level)
- **Reasoning:** Tier 3 for supplementary English-language comparative coverage. Publication frequency (monthly) and summary-level depth limit pipeline utility for real-time monitoring, but the cross-Baltic lens is unique. Useful for detecting when a Lithuanian story has pan-Baltic implications (e.g., coordinated NATO posture, joint Baltic sanctions positions, shared energy infrastructure).

**Eastern Europe Studies Centre (EESC)** | `eesc.lt` | Type: `security_defense` / `think_tank` | Status: `EXISTING`
- **Structural role:** Independent think tank publishing analyses on Eastern European security, Russia/Belarus policy, and Lithuanian strategic posture.
- **Domain coverage:** Diplomatic alignment, security/defense
- **Reasoning:** Think tanks earn boost through depth, not speed. EESC provides the structural analysis that daily outlets can't — why Lithuania's threat perception differs from Germany's, how the Suwalki Gap scenario shapes Baltic defense planning, what Belarus's role as a Russian proxy means for border security. Tier 3 because publication frequency is low and domain coverage is narrow, but when EESC publishes, the analytical quality justifies surfacing.

**IQ.lt** | `iq.lt` | Type: `political_specialist` | Status: `EXISTING`
- **Structural role:** Online analysis and opinion platform featuring expert commentary on foreign policy and economic strategy. Functions as Lithuania's accessible policy-commentary outlet.
- **Domain coverage:** Diplomatic alignment, economic statecraft
- **Reasoning:** Fills the policy-commentary niche between academic think tanks and daily news coverage. Liberal-centrist orientation. Non-English domestic premium applies. Tier 3 rather than Tier 2 because its content is primarily opinion/analysis rather than original reporting, and its domain coverage overlaps with LRT's and 15min's foreign-policy beats.

**Veidas** | `veidas.lt` | Type: `political_specialist` | Status: `EXISTING`
- **Structural role:** Lithuania's longest-running political weekly. In-depth political commentary and analysis from a conservative, laissez-faire perspective.
- **Domain coverage:** Domestic constraints, diplomatic alignment
- **Reasoning:** Provides the conservative editorial counterpoint in a media landscape that leans centrist-liberal. Weekly publication rhythm means deeper analysis than dailies. Non-English domestic premium applies. Tier 3 because it's paywalled (limiting extraction) and its weekly cadence means it follows rather than breaks stories. But its conservative voice is structurally important for reading coalition dynamics and opposition sentiment.
- **Extraction note:** Paywalled. Partial extraction likely.

**Vilnius Institute for Policy Analysis (VIPA)** | `vilniusinstitute.lt` | Type: `think_tank` | Status: `NEW`
- **Structural role:** Independent policy think tank focused on Lithuanian foreign and security policy, European integration, and transatlantic relations.
- **Domain coverage:** Diplomatic alignment, security/defense, institutional engagement
- **Reasoning:** Added to fill the think tank gap. The curation prompt included only EESC for analytical depth; VIPA adds a second think tank voice with a more explicitly transatlantic focus. Think tanks earn boost through depth, not speed. Tier 3 for supplementary analytical coverage.

---

### Neutral — no Goggle rule

**Delfi.lt** | `delfi.lt` | Type: `paper_of_record` | Status: `EXISTING → DEMOTED TO NEUTRAL`
- **Why neutral:** Lithuania's most-visited news portal, but **blocked by Anthropic's crawler** (`delfi.lt` in blocked domains list). Brave can still discover and surface Delfi results for ranking, and headlines provide signal even without full-text extraction. Under the Goggle model, organic ranking is appropriate — no need to boost what we can't extract, but no need to discard what Brave might surface for headline-level intelligence.

**ELTA** | `elta.lt` | Type: `paper_of_record` (wire service) | Status: `EXISTING → DEMOTED TO NEUTRAL`
- **Why neutral:** National news agency, but **blocked by Anthropic's crawler** (`elta.lt` in blocked domains list). Additionally, ELTA's acquisition by Ekspress Grupp/Delfi in 2022 means its content substantially overlaps with Delfi (also blocked). Leave at organic ranking — may provide headline-level signal through Brave discovery.

**Lietuvos rytas** | `lrytas.lt` | Type: `paper_of_record` | Status: `EXISTING → DEMOTED TO NEUTRAL`
- **Why neutral:** Remaining major print daily, but **blocked by Anthropic's crawler** (`lrytas.lt` in blocked domains list). Additionally partially paywalled even without the crawler block. Under the Goggle model, organic ranking is appropriate — the source may surface for headline-level signal but full extraction is not possible.

**Verslo zinios** | `vz.lt` | Type: `business_financial` | Status: `EXISTING → DEMOTED TO NEUTRAL`
- **Why neutral:** Lithuania's leading business daily, but **blocked by Anthropic's crawler** (`vz.lt` in blocked domains list). This is a significant loss — no other Lithuanian source provides equivalent economic statecraft depth. The gap is partially mitigated by LRT's economic coverage and Layer 2 polling of government economic data. If Verslo zinios becomes unblocked in a future audit, it should be immediately restored to Tier 2 minimum.

**Alfa.lt** | `alfa.lt` | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Curation exclusion was correct under the hard-filter model — lower readership and largely duplicates Delfi/15min. Under the Goggle model, no reason to actively discard. With Delfi blocked, Alfa.lt's residual coverage may occasionally provide domestic-language signal.

**Kauno diena** | `kaunodiena.lt` | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Regional daily (Kaunas) rarely breaking national-level stories. Under the Goggle model, organic ranking is appropriate — if a Kaunas-specific story becomes nationally relevant, Brave may surface it.

**Lietuvos zinios** | `lietuvoszinios.lt` | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Ceased print publication and limited digital footprint. Under the Goggle model, no reason to actively discard — organic ranking handles marginal sources correctly.

---

### Discard — `$discard`

**Sputnik Lithuania** | `sputniknews.lt` | Status: `NEW DISCARD`
- **Discard reasoning:** Russian state-backed disinformation outlet. EU-sanctioned. Would actively inject Russian-framed narratives designed to undermine Lithuanian strategic consensus. Not a legitimate news source — pure influence operation.

**Baltnews.lt** | `baltnews.lt` | Status: `NEW DISCARD`
- **Discard reasoning:** Affiliated with Russia's Rossiya Segodnya media group. Previously used as a vector for Russian information operations targeting the Baltic states. EU-sanctioned alongside other Russian state media. Would inject adversarial disinformation if surfaced.

**Vakaro zinios** | `vakarozinios.lt` | Status: `NEW DISCARD`
- **Discard reasoning:** Conservative tabloid with limited foreign/security-policy content. Unlike the neutral exclusions (Alfa.lt, Kauno diena), Vakaro zinios actively publishes sensationalized domestic content that would displace higher-signal sources from top results without providing any analytical value for the five monitoring domains.

---

## STRUCTURAL COVERAGE CHECK

| Structural Role | Source(s) | Tier | Notes |
|---|---|---|---|
| Government leak channel / signaling outlet | LRT (via government interviews), lrv.lt, president.lt | T1, T2 | Lithuania's government communicates primarily through LRT interviews and official portals. No single outlet functions as a "preferred leak channel" in the way La Jornada does for Mexico — Lithuania's coalition governments distribute messaging across multiple outlets |
| Opposition voice | 15min.lt (editorial), Veidas | T1, T3 | Lithuania's opposition voices are diffuse. TS-LKD (conservative opposition) communicates through LRT interviews and social media rather than a dedicated aligned outlet. Veidas provides conservative-leaning commentary |
| Defence/security first-mover | LRT, kam.lt, VSD | T1, T2, T2 | LRT's defense beat is the strongest in Lithuanian media. kam.lt and VSD provide official first-hand sources. No dedicated defense press — this is the primary structural gap |
| Policy-elite discourse | IQ.lt, Veidas, EESC, VIPA | T3, T3, T3, T3 | Multiple outlets at Tier 3 — Lithuania's think tank ecosystem is small but active. Policy discourse also runs through LRT's interview programs |
| Domestic-language depth | LRT, 15min, Siena, Laisves TV, IQ.lt, Veidas, BNS | T1–T3 | Non-English domestic premium applied to all Lithuanian-language sources. Critical given that blocked domains (Delfi, Lietuvos rytas, Verslo zinios, ELTA) are all Lithuanian-language, reducing extractable domestic-language coverage |
| Official government source | lrs.lt, kam.lt, urm.lt, vsd.lt, lrv.lt, president.lt | T2 | **LAYER 2 MIGRATION** — all six government domains receive primary fetch via direct polling. Goggle boost as fallback. Lithuania's semi-presidential system means president.lt and lrv.lt carry distinct signals |
| Analytical/think tank depth | EESC, VIPA, IQ.lt | T3 | Thin but adequate for a small country. EESC for Eastern European security; VIPA for transatlantic/EU; IQ.lt for accessible policy commentary |
| Wire service (local bureau) | BNS, Reuters, AP News | T2, Neutral, Neutral | BNS promoted to Tier 2 due to blocked-domain pressure. Reuters is blocked by Anthropic crawler. AP News available organically |
| Investigative/anti-corruption | Siena, Laisves TV | T1, T2 | Lithuania's investigative duopoly. Small but high-impact — the Paluckas crisis demonstrates their ability to drive national political dynamics |

**Gaps identified:**
1. **Defence-industrial and procurement reporting** — Lithuania is rapidly scaling military purchases (Leopard 2 tanks, HIMARS, Boxer IFVs) and preparing to host a permanent German brigade, but no source systematically tracks procurement timelines, industrial offsets, or logistics. Partially mitigated by LRT's defense beat and kam.lt press releases, but this is the primary structural gap.
2. **Business/economic press extraction** — With Verslo zinios blocked, Lithuania has no extractable dedicated business source. LRT's economic coverage and Bank of Lithuania (lb.lt, added to Layer 2) partially compensate, but deep economic statecraft coverage (sanctions compliance, energy market dynamics, FDI screening) is weaker than it should be.
3. **Belarusian border and hybrid warfare coverage** — Real-time border incidents and migration weaponization rarely surface in mainstream media. VSD threat assessments provide annual retrospectives but not real-time monitoring. FRONTEX reports and border guard communiques would help but are not in the Goggle (government layer handles this).
4. **Diaspora media** — Lithuanian emigrant communities (significant in UK, Ireland, Germany) produce media that signals domestic-constraint dynamics through emigrant political engagement. Not included to avoid over-expanding the Goggle, but this is a known blind spot.

---

## REDUNDANCY RESOLUTION

**Portal cluster: Delfi + 15min + ELTA**
All three are general-coverage digital portals. Resolved by extraction reality: Delfi and ELTA are both blocked (Neutral). 15min absorbs the full portal-coverage load (promoted to Tier 1). ELTA's 2022 acquisition by Delfi's parent company (Ekspress Grupp) means its content substantially overlaps with Delfi — blocking both is effectively a single loss.

**Broadsheet/political analysis cluster: Lietuvos rytas + Veidas + IQ.lt**
Lietuvos rytas is blocked (Neutral). Veidas and IQ.lt are differentiated by editorial orientation: Veidas is conservative with deep political memory, IQ.lt is liberal-centrist with a foreign-policy focus. Both at Tier 3 — no redundancy issue at this level.

**Investigative cluster: Siena + Laisves TV**
These two frequently collaborate and co-publish. Resolved by format differentiation: Siena (Tier 1, text-primary, pipeline-extractable) vs. Laisves TV (Tier 2, video-primary, limited extraction). Siena gets the higher tier because the pipeline processes text more effectively than video. The collaboration relationship means boosting both increases the probability of capturing their joint investigations.

**Think tank cluster: EESC + VIPA + IQ.lt**
Three analytical sources at Tier 3 might seem redundant for a small country, but each has a distinct focus: EESC (Eastern European security architecture), VIPA (transatlantic/EU integration), IQ.lt (accessible domestic policy commentary). No redundancy reduction needed — each fills a distinct analytical niche.

**Government sources: lrs.lt + kam.lt + urm.lt + vsd.lt + lrv.lt + president.lt**
Six government domains at Tier 2 is a lot, but each carries distinct signals: Seimas (legislative), Defence Ministry (military), Foreign Affairs (diplomatic), VSD (intelligence), Government Portal (executive/cabinet), Presidential Office (head of state). Lithuania's semi-presidential system means the presidential office and government portal often signal different positions, particularly on EU and NATO policy. All receive Layer 2 direct polling; Goggle boost is fallback only.

---

## QUERY CONFIGURATION

```
country: LT
search_lang: lt
freshness: pw
```

**Multi-language notes:** Lithuania's media ecosystem operates primarily in Lithuanian. English-language sources (LRT English service at lrt.lt/en, Baltic Times, EESC English publications) are supplements. Queries should run primarily in Lithuanian; a secondary English query cycle for security/defense topics would capture LRT English, Baltic Times, and international wire coverage. The pipeline's existing `languages.metadata: en` configuration handles this correctly. Given that four major Lithuanian-language sources are blocked, the English-language secondary cycle becomes more important than usual for maintaining extraction coverage.

**Localized query vocabulary validation:**

The curation prompt's vocabulary is well-constructed. Notes:

- **Domain 1 (Diplomatic):** All terms valid. Add `"Nausėda užsienio politika"` and `"Ruginienė NATO"` as leader-specific patterns. `"Kinija Taivanas"` (China-Taiwan) is missing — Lithuania's diplomatic confrontation with China over the Taiwan representative office remains a live issue. Add `"Suwalki koridorius"` (Suwalki corridor) for NATO deterrence discussions.
- **Domain 2 (Security):** Strong list. Add `"Vokietijos brigada"` (German brigade) — the permanent stationing of a German combat brigade in Lithuania is the single biggest defense development in 2025-2026. `"šauktiniai"` (conscripts) or `"karo prievolė"` (conscription) — Lithuania reintroduced conscription and this is a recurring domestic-constraints story. Add `"HIMARS"` and `"Leopard"` for procurement tracking.
- **Domain 3 (Economic):** Solid. Add `"Ignitis"` — state energy company is central to energy security stories. `"LNG terminalas"` (LNG terminal, the Klaipeda FSRU "Independence") is relevant for energy independence from Russia. Add `"Baltijos jūros vėjo parkai"` (Baltic Sea wind farms) for energy transition coverage. `"puslaidininkiai"` (semiconductors) — Lithuania is positioning for niche semiconductor capacity.
- **Domain 4 (Institutional):** Valid. Add `"Baltijos Asamblėja"` (Baltic Assembly) for trilateral Baltic institutional coordination. `"Bukarešto devynetas"` (Bucharest Nine) — Lithuania is an active member of this NATO eastern-flank grouping. `"Trimarium"` (Three Seas Initiative) for regional infrastructure engagement.
- **Domain 5 (Domestic):** Strong. Add `"Paluckas krizė"` (Paluckas crisis) — the defining domestic political story of 2025-2026. `"Nemuno Aušra"` (Dawn of Nemunas) — junior coalition partner whose populist positions create coalition friction. `"LSDP"` (Social Democrats, governing party). Add `"savivaldybių rinkimai"` (municipal elections) if relevant in cycle.

**Stale/problematic terms:** None are stale. All terms reflect current Lithuanian political vocabulary.

**Suggested topic query patterns:**

1. `Vokietijos brigada Lietuvoje NATO atgrasymas` — German brigade deployment and NATO deterrence
2. `Ruginienė gynybos biudžetas Seimas` — Defense spending under PM Ruginiene
3. `VSD grėsmių vertinimas Rusija Baltarusija` — VSD threat assessment on Russia/Belarus
4. `Paluckas tyrimas Siena LSDP` — Paluckas investigation and LSDP crisis
5. `Ignitis energetinis saugumas LNG terminalas` — Energy security and LNG independence
6. `Suwalki koridorius NATO gynybos planai` — Suwalki Gap defense planning
7. `sankcijos Rusijai eksporto kontrolė` — Russia sanctions and export controls

---

## GOGGLE FILE

```goggle
! name: MPM Lithuania
! description: MPM pipeline source prioritization for Lithuania — boosts high-signal sources, discards noise
! public: false
! author: MPM Pipeline

! --- Tier 1: Essential (boost=3) ---
$boost=3,site=lrt.lt
$boost=3,site=15min.lt
$boost=3,site=siena.lt

! --- Tier 2: Important (boost=2) ---
$boost=2,site=bns.lt
$boost=2,site=lrs.lt
$boost=2,site=kam.lt
$boost=2,site=urm.lt
$boost=2,site=vsd.lt
$boost=2,site=lrv.lt
$boost=2,site=president.lt

! --- Tier 3: Supplementary (boost=1) ---
$boost=1,site=baltictimes.com
$boost=1,site=eesc.lt
$boost=1,site=iq.lt
$boost=1,site=veidas.lt
$boost=1,site=vilniusinstitute.lt

! --- Discard: Noise ---
$discard,site=sputniknews.lt
$discard,site=baltnews.lt
$discard,site=vakarozinios.lt
```

---

## INTERPRETIVE CONTEXT FOR DOSSIER

### Tier 1 Sources

> Articles from **LRT** about defense and security should be interpreted as Lithuania's most authoritative reporting on NATO force posture, VSD threat assessments, and defense procurement — its public-broadcaster status and editorial independence mean it does not amplify government positions uncritically, but its access to defense officials is deeper than any commercial outlet's. LRT's English-language service (lrt.lt/en) provides a curated selection of its Lithuanian reporting; the Lithuanian-language original often contains more detail and nuance.

> Articles from **15min.lt** about domestic politics and EU affairs should be interpreted as centrist-liberal commercial media coverage — its editorial orientation slightly favors pro-European, reformist positions, but its news reporting is professionally neutral. With Delfi blocked, 15min carries a disproportionate share of Lithuania's commercial-media signal; stories that would normally be cross-referenced against Delfi now depend primarily on 15min's framing.

> Articles from **Siena** about political corruption and financial misconduct should be interpreted as Lithuania's most rigorous investigative reporting — its OCCRP membership, grant-funded independence, and track record (the Paluckas crisis) establish it as the pipeline's primary source for stories that expose gaps between official positions and actual conduct. Its investigations are methodical and slow-building; when Siena publishes, the story has been extensively verified.

### Tier 2 Sources

> Articles from **Laisves TV** about political investigations should be interpreted in conjunction with Siena, its frequent collaboration partner — their joint investigations carry the combined weight of both outlets' sourcing. Laisves TV's crowdfunded model means it is responsive to audience interest, which can sometimes prioritize engagement over analytical depth. Its video-first format means the pipeline may capture only summary text rather than full investigative detail.

> Articles from **BNS Lithuania** about diplomatic and defense developments should be interpreted as wire-service reporting — factual, fast, and minimally editorialized. BNS breaks stories that propagate across the Lithuanian media ecosystem; seeing a story first on BNS means it is fresh intelligence that has not yet been framed by editorial outlets. BNS's pan-Baltic scope means it occasionally provides comparative context (Latvia/Estonia parallels) absent from purely Lithuanian outlets.

> Articles from **lrs.lt** (Seimas) should be interpreted as official legislative records — not journalism but primary source material. Committee transcripts, voting records, and draft legislation from this domain represent the actual mechanics of Lithuanian governance. Pay particular attention to defense committee and foreign affairs committee proceedings, which often contain more candid assessments than public government statements.

> Articles from **kam.lt** (Ministry of National Defence) should be interpreted as official military communications — press releases reflect what the defense establishment wants publicly known about procurement, allied force rotations, and threat assessments. What is absent from kam.lt communications is often as informative as what is present — the ministry is notably silent on Suwalki Gap operational specifics and German brigade deployment logistics.

> Articles from **urm.lt** (Ministry of Foreign Affairs) should be interpreted as direct expressions of Lithuanian diplomatic positioning — MFA statements on Russia, Belarus, China, and Taiwan represent official strategic intent. Lithuania's MFA has been unusually outspoken compared to larger EU states, particularly on Taiwan and Belarusian hybrid threats; its statements often lead rather than follow EU consensus positions.

> Articles from **vsd.lt** (VSD) should be interpreted as the Lithuanian intelligence community's public threat assessment — VSD annual reports are landmark documents that shape the entire year's defense and security discourse. Their explicit naming of Russian and Belarusian threat vectors, Chinese intelligence operations, and domestic radicalization risks provides the baseline against which all other security reporting should be calibrated.

> Articles from **lrv.lt** and **president.lt** should be interpreted as distinct voices in Lithuania's semi-presidential system — the government portal (lrv.lt) reflects the prime minister's coalition government position, while the presidential office (president.lt) reflects President Nauseda's occasionally divergent stance, particularly on EU integration pace, relations with Poland, and defense spending priorities. Divergence between these two sources is itself a signal of institutional friction.

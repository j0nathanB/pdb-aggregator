I need to validate the current state of Hungary's media landscape and check for any developments since the April 2026 regime transition mentioned in the document.
Now I have comprehensive information to conduct the audit. Let me also check on 444.hu's English-language section (Insight Hungary) which appeared in my search results.
Now I have enough information to produce the comprehensive audit. Let me compile my findings.

---

#### AUDIT SUMMARY: Hungary

**Sources assessed:** 18 recommended + 7 excluded + 3 newly identified = 28 total
**Tier 1 (boost=3):** 4 sources
**Tier 2 (boost=2):** 8 sources
**Tier 3 (boost=1):** 8 sources
**Neutral (no rule):** 5 sources
**Discard:** 5 sources
**Overall assessment:** The curation prompt produced an exceptionally strong whitelist for Hungary — one of the best-structured source maps I've audited. The tiering is defensible and the analytical framework is sound, reflecting deep knowledge of Hungary's bifurcated media landscape. Key changes: I add VSquare.org (English-language investigative, Tier 2) and Hungarian Conservative (Fidesz-aligned English signal source, Tier 3); promote G7.hu from organic to Tier 3; and re-tier Origo from Tier 3 to Tier 2 given its structural importance as the primary channel through which the now-opposition Fidesz signals its posture. The MTI/Híradó and kormany.hu entries are flagged for Layer 2 migration as specified.

---

#### BOOST ASSIGNMENTS

##### Tier 1 — `$boost=3`

**Telex.hu** | `telex.hu` | Type: `paper_of_record` | Status: `EXISTING`
- **Structural role:** Hungary's de facto paper of record for independent political journalism; largest independent newsroom; 
produces original reporting across all five domains and now publishes substantial English-language content via its English section
, providing both domestic-language depth and direct pipeline accessibility.
- **Domain coverage:** Diplomatic alignment; Domestic constraints; Economic & technological statecraft; Institutional engagement; Security & defense autonomy
- **Reasoning:** Confirmed Tier 1. Telex's election coverage demonstrated unmatched breadth — from live election results to EU diplomatic reactions to economic analysis. Its English section is now producing daily original content, enhancing pipeline extraction.

**HVG (Heti Világgazdaság)** | `hvg.hu` | Type: `business_financial` / `paper_of_record` | Status: `EXISTING`
- **Structural role:** Hungary's leading independent business and political weekly; the outlet policy elites read for economic analysis. 
HVG broke the MTI journalist letter story
, confirming its first-mover status on institutional developments.
- **Domain coverage:** Economic & technological statecraft; Domestic constraints; Diplomatic alignment
- **Reasoning:** Confirmed Tier 1. Irreplaceable for the economic analysis the pipeline needs — EU fund conditionality, fiscal constraints, energy dependency, and forint dynamics. Metered paywall is a flag but not a blocker.

**Direkt36** | `direkt36.hu` | Type: `investigative` | Status: `EXISTING`
- **Structural role:** Hungary's only dedicated investigative outlet with genuine security/intelligence/foreign policy sourcing. 
A non-profit investigative journalism center that devotes all its resources to investigating sensitive stories, having "uncovered the details of the Orbán government's Russian connections, the Pegasus surveillance"
 and more. 
Its most prominent journalist, Szabolcs Panyi, faced politically motivated espionage charges
 for reporting on Russian interference — underscoring Direkt36's unique access to this domain.
- **Domain coverage:** Security & defense autonomy; Diplomatic alignment; Domestic constraints
- **Reasoning:** Confirmed Tier 1. Direkt36's recent investigations — including the "Orbán-gate" IT infiltration story, the Szijjártó-Lavrov communications exposé, and state-funded defense company transfers — are globally significant and reproduced nowhere else in Hungarian media. 
Its Dynasty documentary earned over 3.5 million views in its first month in a country of 9.6 million
, confirming massive domestic reach.

**Magyar Közlöny / kormany.hu** | `kormany.hu` / `magyarkozlony.hu` | Type: `legislative_official` | Status: `EXISTING` | **`LAYER 2 MIGRATION`**
- **Structural role:** Official government gazette and government portal — the primary channel for legislation, decrees, procurement notices, and treaty ratifications. Under the new Magyar government, 
Magyar has outlined four priority reform areas including "joining the European Public Prosecutor's Office, restoring judicial independence, and rebuilding media and academic freedoms"
 — all of which will manifest first in official gazette publications.
- **Domain coverage:** Institutional engagement; Security & defense autonomy; Economic & technological statecraft
- **Reasoning:** Confirmed Tier 1. Maximum evidentiary value for detecting state actions. Flagged for Layer 2 direct-fetch migration; Goggle boost retained as belt-and-suspenders fallback.

##### Tier 2 — `$boost=2`

**444.hu** | `444.hu` | Type: `political_specialist` | Status: `EXISTING`
- **Structural role:** Independent digital news site providing the progressive/opposition-sympathetic perspective; 
covers current affairs with numerous investigative journalism awards, reaching 500,000 daily and 3 million monthly readers
. Also operates Insight Hungary (insighthungary.444.hu) for English-language content.
- **Domain coverage:** Domestic constraints; Diplomatic alignment
- **Reasoning:** Confirmed Tier 2. The Insight Hungary English section adds pipeline value. Not Tier 1 due to substantial overlap with Telex, but its left-liberal editorial lens provides essential contestation perspective.

**Átlátszó** | `atlatszo.hu` | Type: `investigative` | Status: `EXISTING`
- **Structural role:** Nonprofit investigative and data journalism outlet specializing in procurement analysis and corruption tracking; 
forms part of the VSquare network alongside Direkt36 as Hungary's investigative journalism partners
.
- **Domain coverage:** Domestic constraints; Economic & technological statecraft
- **Reasoning:** Confirmed Tier 2. Irreplaceable for tracking NER dismantling, procurement integrity, and EU fund allocation patterns. Its procurement databases and data journalism provide structural evidence no narrative outlet can replicate.

**RTL.hu / RTL Klub** | `rtl.hu` | Type: `paper_of_record` | Status: `EXISTING`
- **Structural role:** The only independent television network with significant national reach, owned by RTL Group (Bertelsmann). Provides the sole broadcast news alternative to MTVA state media, particularly critical during the media restructuring period.
- **Domain coverage:** Domestic constraints; Diplomatic alignment
- **Reasoning:** Confirmed Tier 2. Structural importance is magnified by the incoming government's plan to suspend MTVA news broadcasts — RTL Klub becomes the *only* television news source for rural Hungary during the transition.

**Budapest Business Journal (BBJ)** | `bbj.hu` | Type: `business_financial` | Status: `EXISTING`
- **Structural role:** The only English-language outlet in Hungary producing original business/economic reporting. 
Produces substantive analysis such as OECD productivity assessments contextualized for Hungary
.
- **Domain coverage:** Economic & technological statecraft; Diplomatic alignment
- **Reasoning:** Confirmed Tier 2. Essential English-language niche for economic coverage accessible without translation. Metered paywall flagged for extraction monitoring.

**Honvédelem.hu** | `honvedelem.hu` | Type: `government_aligned` / `security_defense` | Status: `EXISTING` | **`LAYER 2 MIGRATION`**
- **Structural role:** Official MoD/Defence Forces website — the only source for defense procurement announcements, NATO exercise participation, and Zrínyi 2026 program updates in the absence of independent defense press.
- **Domain coverage:** Security & defense autonomy
- **Reasoning:** Confirmed Tier 2. Hungary's defense press gap means this is where procurement decisions and deployment announcements first appear. Flagged for Layer 2 migration; Goggle boost retained as fallback.

**Portfolio.hu** | `portfolio.hu` | Type: `business_financial` | Status: `EXISTING`
- **Structural role:** Hungary's most-read financial news site; provides real-time market, MNB, and energy sector coverage that HVG's weekly rhythm cannot match.
- **Domain coverage:** Economic & technological statecraft; Domestic constraints
- **Reasoning:** Confirmed Tier 2. 
The post-election market reaction — Budapest stock index up nearly 5%, forint strengthening to 364 HUF/EUR from 377, and bond yields dropping from 7.52% to 6.21%
 — is precisely the type of real-time financial signal Portfolio tracks.

**Origo.hu** | `origo.hu` | Type: `government_aligned` → `opposition_aligned` (Fidesz) | Status: `EXISTING — PROMOTED FROM TIER 3`
- **Structural role:** Highest-traffic KESMA outlet; now functions as the primary channel through which Fidesz (now the main opposition) signals its posture. With the regime transition, Origo's counter-narrative function becomes more analytically important.
- **Domain coverage:** Domestic constraints
- **Reasoning:** Promoted from Tier 3 to Tier 2. The pipeline needs to see Fidesz's opposition messaging to track domestic constraints on the Magyar government. Origo is the highest-signal channel for this purpose. **NOT a source of facts** — purely a signal source. Interpretive context must flag this.

**VSquare.org** | `vsquare.org` | Type: `investigative` | Status: `NEW`
- **Structural role:** 
A non-profit, independent, English-language investigative outlet offering "unique cross-border coverage of vital topics" including "Russian influence, disinformation, espionage, Chinese influence, corruption"
 across the Visegrád region. 
Its network includes Átlátszó and Direkt36 from Hungary
. 
Its Budapest-based lead investigative editor Szabolcs Panyi "covers national security, foreign policy, and Russian and Chinese influence"
.
- **Domain coverage:** Security & defense autonomy; Diplomatic alignment; Domestic constraints
- **Reasoning:** NEW — Tier 2. Fills a critical gap: English-language investigative reporting on Hungary's security/intelligence domain. Publishes Direkt36/Átlátszó investigations in English with additional cross-border context. Essential for the pipeline's English query cycle, especially for security and Russian-influence stories.

##### Tier 3 — `$boost=1`

**Hungary Today** | `hungarytoday.hu` | Type: `political_specialist` | Status: `EXISTING`
- **Structural role:** English-language news site providing translations/summaries of Hungarian political developments.
- **Domain coverage:** Domestic constraints; Diplomatic alignment
- **Reasoning:** Confirmed Tier 3. Useful English-language backup when BBJ doesn't cover political developments. Lower original reporting density.

**Partizán** | `partizan.hu` | Type: `political_specialist` | Status: `EXISTING`
- **Structural role:** YouTube-based independent political talk show capturing younger demographic discourse.
- **Domain coverage:** Domestic constraints
- **Reasoning:** Confirmed Tier 3. Extraction flag for video-primary format; limited pipeline text utility, but partizan.hu carries some text.

**Népszava** | `nepszava.hu` | Type: `opposition_aligned` | Status: `EXISTING`
- **Structural role:** Hungary's oldest daily newspaper (founded 1873); left-of-center editorial perspective.
- **Domain coverage:** Domestic constraints
- **Reasoning:** Confirmed Tier 3. Fills the traditional left/labor voice. Declining readership and narrow domain coverage limit tier.

**24.hu** | `24.hu` | Type: `paper_of_record` | Status: `EXISTING`
- **Structural role:** Independent online general-interest news outlet; backup general-news coverage.
- **Domain coverage:** Domestic constraints; Diplomatic alignment
- **Reasoning:** Confirmed Tier 3. Largely redundant with Telex but occasionally breaks local stories.

**Euractiv** | `euractiv.com` | Type: `political_specialist` | Status: `EXISTING`
- **Structural role:** Brussels-based EU policy coverage; provides the Brussels-side perspective on Hungary-EU institutional dynamics.
- **Domain coverage:** Institutional engagement; Diplomatic alignment
- **Reasoning:** Confirmed Tier 3. Irregular publication frequency on Hungary specifically, but fills the Brussels-perspective gap.

**MTI / Híradó** | `hirado.hu` | Type: `wire` / `government_aligned` | Status: `EXISTING` | **`LAYER 2 MIGRATION` (partial)**
- **Structural role:** Hungary's national wire service. 
Nearly 100 MTI journalists wrote a letter demanding that "editorial autonomy of the national news agency should be restored"
, signaling its editorial direction is in active flux during the transition.
- **Domain coverage:** All five domains (baseline event coverage)
- **Reasoning:** Confirmed Tier 3. Wire function is valuable but editorial reliability is uncertain during media restructuring. Layer 2 migration flagged for official dispatches.

**Válasz Online** | `valaszonline.hu` | Type: `political_specialist` / `think_tank` | Status: `EXISTING`
- **Structural role:** Conservative-liberal analytical publication providing the non-Orbán right perspective essential for understanding Tisza coalition tensions.
- **Domain coverage:** Domestic constraints; Diplomatic alignment
- **Reasoning:** Confirmed Tier 3. Unique editorial lens (center-right, anti-Orbán conservative) not replicated by any other source. Moderate publication frequency.

**G7.hu** | `g7.hu` | Type: `business_financial` / `data_journalism` | Status: `PROMOTED FROM ORGANIC`
- **Structural role:** 
An independent online platform in Budapest providing "in-depth, accessible coverage of economic and business topics"
. 
Reaches 550,000-600,000 real users monthly
 with 
around four to five articles per day, prioritizing "quality of its articles over quantity" and "only publishing articles which feature original, independent journalism"
.
- **Domain coverage:** Economic & technological statecraft
- **Reasoning:** PROMOTED to Tier 3. The curation prompt left G7 at organic ranking, noting overlap with Portfolio and HVG. However, G7's data journalism methodology and economic analysis serve as a useful supplement, particularly for longer-form economic structural analysis. Its 12-13 person staff and commitment to original reporting justify a modest boost.

**Hungarian Conservative** | `hungarianconservative.com` | Type: `government_aligned` / `political_specialist` | Status: `NEW`
- **Structural role:** 
An English-language quarterly journal launched by the Batthyány Lajos Foundation, aspiring "to be the foremost English-language voice of twenty-first-century Hungarian conservatism"
, which explicitly celebrates Hungarian conservative political success. 
Has documented links to Orbán and Fidesz funding
.
- **Domain coverage:** Domestic constraints; Diplomatic alignment
- **Reasoning:** NEW — Tier 3. Similar signal function to Origo but in English. Under the regime transition, this outlet will carry the Fidesz-aligned conservative intellectual counter-narrative accessible to international audiences. Not a source of independent analysis — treat as a signal source for Fidesz-conservative messaging. **UNCERTAINTY FLAG:** The outlet's editorial direction post-election is not yet clear; it may moderate or intensify.

##### Neutral — no Goggle rule

**Index.hu** | `index.hu` | Status: `CONFIRMED NEUTRAL`
- **Reasoning:** The curation prompt correctly identified Index's unstable editorial position after the 2020 ownership change. Under the Goggle model, it can surface organically if Brave ranks it highly, which is appropriate — it occasionally produces worthwhile content but its reliability is unpredictable.

**Mérce** | `merce.hu` | Status: `CONFIRMED NEUTRAL`
- **Reasoning:** Left-wing political site with occasional original progressive analysis. Too infrequent on the pipeline's analytical domains to justify a boost, but may surface organically on domestic politics queries.

**Magyar Nemzet** | `magyarnemzet.hu` | Status: `CONFIRMED NEUTRAL`
- **Reasoning:** 
A major Hungarian newspaper that "styled itself as 'close to the current Hungarian government led by Viktor Orbán'"
. KESMA broadsheet now functioning as Fidesz opposition outlet. Editorially redundant with Origo for signal purposes. May surface organically; no need to boost or discard.

**Hír TV** | `hirtv.hu` | Status: `CONFIRMED NEUTRAL`
- **Reasoning:** Conservative television network within the KESMA ecosystem. May carry occasionally relevant Fidesz opposition messaging but is redundant with Origo at Tier 2. Leave at organic.

**Lakmusz** | `lakmusz.hu` | Status: `CONFIRMED NEUTRAL`
- **Reasoning:** Hungarian fact-checking outlet. Occasionally produces original analysis on disinformation campaigns (referenced in Euromaidan Press coverage of election interference). Too narrow and infrequent for a boost, but shouldn't be discarded.

##### Discard — `$discard`

**Blikk** | `blikk.hu` | Status: `CONFIRMED DISCARD`
- **Discard reasoning:** 
Now under government-influenced ownership (Indamedia acquisition)
. Hungary's leading tabloid with primarily entertainment/celebrity/sensationalized content that would displace analytical results.

**Bors** | `bors.hu` | Status: `CONFIRMED DISCARD`
- **Discard reasoning:** Lifestyle/entertainment tabloid with no original political reporting — would consume result slots.

**Ripost** | `ripost.hu` | Status: `CONFIRMED DISCARD`
- **Discard reasoning:** KESMA-affiliated sensationalized tabloid. Less analytically useful than Origo as a signal source; targets low-information audience.

**888.hu** | `888.hu` | Status: `CONFIRMED DISCARD`
- **Discard reasoning:** Fidesz-aligned political attack site producing disinformation-adjacent content. No analytical signal value — tactical attack vehicle only.

**Pesti Srácok** | `pestisracok.hu` | Status: `CONFIRMED DISCARD`
- **Discard reasoning:** Far-right-leaning, conspiratorial framing. Would degrade result quality on any political query.

**Mandiner** | `mandiner.hu` | Status: `DOWNGRADED FROM DISCARD TO NEUTRAL`
- **Reasoning:** The curation prompt discarded Mandiner, but 
Mandiner played a significant role in the Panyi espionage case by publishing the edited recording
, demonstrating it occasionally functions as a government signal channel with unique content. Under the Goggle model, leaving it at neutral (rather than discard) allows it to surface when it carries genuine signal. It should not be actively discarded — but also should not be boosted.

**Propeller.hu** | `propeller.hu` | Status: `CONFIRMED DISCARD`
- **Discard reasoning:** Aggregator/content farm with no original reporting. Would displace higher-value results.

---

#### STRUCTURAL COVERAGE CHECK

| Structural Role | Source(s) | Tier | Notes |
|---|---|---|---|
| Government leak channel / policy kite-flying | kormany.hu (official); MTI/Híradó (wire); Telex (watch for preferred leak channel under Magyar) | Tier 1 / Tier 3 / Tier 1 | **LAYER 2 MIGRATION** for kormany.hu and MTI. Under the Magyar government, the leak channel may shift from state media to independent outlets — monitor Telex for pattern. |
| Opposition voice | Origo (Fidesz opposition messaging); Népszava (left opposition); 444.hu (liberal-progressive); Hungarian Conservative (English-language Fidesz signal) | Tier 2 / Tier 3 / Tier 2 / Tier 3 | Origo promoted to Tier 2 to capture Fidesz's opposition posture as the primary domestic constraint signal. |
| Defence/security first-mover | Honvédelem.hu (official); Direkt36 (investigative); VSquare (English-language investigative) | Tier 2 / Tier 1 / Tier 2 | **LAYER 2 MIGRATION** for Honvédelem.hu. Gap remains: no independent Hungarian defense press. VSquare addition partially fills the English-language security gap. |
| Policy-elite discourse | HVG; Telex; Válasz Online; Portfolio | Tier 1 / Tier 1 / Tier 3 / Tier 2 | Strong coverage. HVG is what economic decision-makers read; Telex is what political decision-makers read. |
| Domestic-language depth | Telex; HVG; 444.hu; Portfolio; Átlátszó; Origo; Népszava; 24.hu; Válasz Online; G7.hu | Tier 1/1/2/2/2/2/3/3/3/3 | Extensive Hungarian-language coverage across the spectrum. |
| Official government source | kormany.hu / Magyar Közlöny; Honvédelem.hu; MTI | Tier 1 / Tier 2 / Tier 3 | **LAYER 2 MIGRATION** for all three. Goggle boosts retained as belt-and-suspenders. Also add parlament.hu to Layer 2 direct monitoring (not in Goggle — not a news source). |
| Analytical/think tank depth | HVG (economic); Válasz Online (political); Euractiv (EU-institutional); G7.hu (data journalism) | Tier 1 / Tier 3 / Tier 3 / Tier 3 | Adequate. No dedicated foreign policy think tank outlet exists in Hungary — this is a structural gap in the ecosystem, not a source selection failure. |
| Wire service (local bureau) | MTI/Híradó (domestic, in flux); Reuters/AFP Budapest (organic) | Tier 3 / Organic | MTI's editorial reliability is actively uncertain during the transition. Reuters and AFP Budapest bureaus surface organically. |

**Gaps identified:**
1. **Defence press gap persists.** No solution available — Hungary has no independent defense publication. Direkt36 + Honvédelem.hu + VSquare is the best available combination.
2. **Rural political dynamics.** No fix through news search — the source set is overwhelmingly Budapest-based. Coverage gap must be flagged in dossier rather than solved through sourcing.
3. **Parliamentary proceedings (parlament.hu).** Should be added to Layer 2 direct monitoring, not the Goggle — it's a government database, not a news source. This is correctly identified in the curation prompt's coverage gap assessment.

---

#### REDUNDANCY RESOLUTION

**Economic cluster (HVG / Portfolio / BBJ / G7):** Resolved through differentiation — HVG leads at Tier 1 (deepest analytical depth, weekly long-form); Portfolio at Tier 2 (real-time financial/market data); BBJ at Tier 2 (English-language niche for foreign business community); G7 at Tier 3 (data journalism supplement). Each fills a distinct frequency/depth/language niche.

**Independent generalist cluster (Telex / 444 / 24.hu / RTL.hu):** Telex leads at Tier 1 (broadest coverage, largest newsroom); 444 at Tier 2 (left-liberal editorial diversity, Insight Hungary English section); RTL at Tier 2 (unique rural broadcast reach); 24.hu at Tier 3 (backup). Telex and 444 overlap on domestic politics but diverge on editorial perspective, justifying both.

**Investigative cluster (Direkt36 / Átlátszó / VSquare):** Direkt36 leads at Tier 1 (security/intelligence sourcing); Átlátszó at Tier 2 (procurement/corruption data); VSquare at Tier 2 (English-language cross-border investigative, partially overlapping with Direkt36 but essential for pipeline accessibility). Minimal redundancy — each has a distinct specialization.

**Fidesz signal cluster (Origo / Hungarian Conservative):** Origo leads at Tier 2 (highest-traffic Hungarian-language Fidesz messaging); Hungarian Conservative at Tier 3 (English-language conservative intellectual framing). Mandiner at neutral (can surface organically; redundant with Origo for signal purposes but occasionally carries unique material).

---

#### QUERY CONFIGURATION

```
country: HU
search_lang: hu
freshness: pw
```

**Multi-language notes:** Hungarian political discourse operates overwhelmingly in Hungarian (`hu`). English-language coverage is produced by BBJ, Hungary Today, Telex English, Insight Hungary (444), VSquare, and international outlets. Run primary queries in Hungarian (`search_lang: hu`). Run a secondary English query cycle (`search_lang: en, country: HU`) focused on: (a) EU institutional developments (EPPO, conditionality); (b) economic/investment stories; (c) security/intelligence investigations (VSquare publishes in English). Hungarian-language queries surface ~80% of analytical needs; English queries catch the Brussels-perspective and investigative-English-language remainder.

**Localized query vocabulary validation:**

The curation prompt's vocabulary is exceptionally well-constructed. Minor adjustments:

- **Diplomatic alignment:** Terms are current and well-calibrated. Note that `"Szijjártó"` should now be used to track Fidesz opposition foreign policy posture (he is no longer FM). Add `"Bóka János"` (likely new FM candidate) or generic `"új külügyminiszter"` (new foreign minister) to track the appointment.
- **Security & Defense:** `"Zrínyi 2026"` remains valid as the program name. Add `"védelmi felülvizsgálat"` (defense review) to capture any post-transition defense policy reassessment.
- **Economic & Technological Statecraft:** Terms are excellent. `"Paks II Rosatom"` is especially critical given 
Magyar's stated intent to "wean Hungary off Russian energy" while nuclear plants "rely on Russia's state-owned Rosatom"
. Add `"szankciók Oroszország"` (Russia sanctions) to track the sanctions posture shift.
- **Institutional Engagement:** `"EPPO"` is the single most important term. Add `"Sulyok lemondás"` (Sulyok resignation) given 
Magyar's demand that President Sulyok resign
. Also add `"médiahatóság"` (media authority) to track the new regulatory body.
- **Domestic Constraints:** Terms are strong. Add `"Orbán reorganizáció"` / `"Fidesz újjászervezés"` to track Fidesz's post-defeat reorganization. Also `"dokumentum megsemmisítés"` (document destruction) given allegations of shredding during the transition period.

**Suggested topic query patterns:**

1. `Péter Magyar EPPO csatlakozás` — PM-elect + EPPO accession; catches the most consequential institutional reform indicator
2. `Paks II Rosatom felülvizsgálat` — Nuclear plant + Russian contractor + review; catches energy infrastructure reassessment
3. `EU források felszabadítás jogállamiság 2026` — EU funds + release + rule of law + year; catches the central fiscal-institutional nexus given the 
August deadline for €16 billion in frozen recovery funding

4. `honvédség NATO hadgyakorlat Zrínyi` — Military + NATO exercise + modernization program; catches defense posture signals
5. `Tisza kormány KESMA médiatörvény` — Tisza government + KESMA + media law; catches media restructuring as an institutional indicator

---

#### GOGGLE FILE

```goggle
! name: MPM Hungary
! description: MPM pipeline source prioritization for Hungary — boosts high-signal sources, discards noise
! public: false
! author: MPM Pipeline

! --- Tier 1: Essential (boost=3) ---
$boost=3,site=telex.hu
$boost=3,site=hvg.hu
$boost=3,site=direkt36.hu
$boost=3,site=kormany.hu
$boost=3,site=magyarkozlony.hu

! --- Tier 2: Important (boost=2) ---
$boost=2,site=444.hu
$boost=2,site=atlatszo.hu
$boost=2,site=rtl.hu
$boost=2,site=bbj.hu
$boost=2,site=honvedelem.hu
$boost=2,site=portfolio.hu
$boost=2,site=origo.hu
$boost=2,site=vsquare.org

! --- Tier 3: Supplementary (boost=1) ---
$boost=1,site=hungarytoday.hu
$boost=1,site=partizan.hu
$boost=1,site=nepszava.hu
$boost=1,site=24.hu
$boost=1,site=euractiv.com
$boost=1,site=hirado.hu
$boost=1,site=valaszonline.hu
$boost=1,site=g7.hu
$boost=1,site=hungarianconservative.com

! --- Discard: Noise ---
$discard,site=blikk.hu
$discard,site=bors.hu
$discard,site=ripost.hu
$discard,site=888.hu
$discard,site=pestisracok.hu
$discard,site=propeller.hu
```

---

#### INTERPRETIVE CONTEXT FOR DOSSIER

**Tier 1 Sources:**

> Articles from **Telex.hu** about diplomatic alignment or domestic political developments should be interpreted as independently reported with a pro-rule-of-law, pro-European editorial frame; Telex will present the Magyar government's EU-integration agenda sympathetically and frame Fidesz opposition critically, but factual reporting is reliable and cross-verifiable through official sources.

> Articles from **Telex.hu** about economic policy should be interpreted as reliable factual reporting but with limited specialist economic depth; cross-reference with HVG or Portfolio for analytical context on fiscal and monetary developments.

> Articles from **HVG** about economic and technological statecraft should be interpreted as Hungary's most rigorous independent economic analysis; editorially sympathetic to market-oriented and EU-integrated economic policy, likely to frame energy dependency on Russia and NER-connected procurement critically, but data and sourcing are among the most reliable in Hungarian media.

> Articles from **HVG** about domestic constraints should be interpreted as centrist-liberal elite discourse — this is what Hungary's policy-making class and urban professionals read; its framing reflects that demographic's priorities rather than rural or working-class perspectives.

> Articles from **Direkt36** about security and defense or diplomatic alignment should be interpreted as high-confidence investigative reporting with deep intelligence/security community sources; if Direkt36 publishes a claim about intelligence cooperation, surveillance, or security-sector dynamics, treat it as the strongest available domestic source on that topic. Note that Direkt36's journalist Szabolcs Panyi faced espionage charges from the Orbán government — these charges should be tracked as a transitional justice indicator under the Magyar government.

> Articles from **kormany.hu / Magyar Közlöny** about any domain should be interpreted as official government output with no independent editorial layer; factual details (dates, signatories, budget figures) are authoritative, but omissions and framing are deliberate policy signals. Under the Magyar government, this source becomes the primary channel for EPPO accession legislation, media law drafts, constitutional amendments, and energy policy decrees — track what is published and what is conspicuously absent.

**Tier 2 Sources:**

> Articles from **444.hu** about domestic constraints should be interpreted as left-liberal editorial perspective; likely to frame Fidesz-era institutional legacies critically and support Magyar government reforms sympathetically, but provides genuine domestic progressive-flank discourse that Telex's centrist positioning doesn't fully capture.

> Articles from **Átlátszó** about economic/technological statecraft or domestic constraints (specifically procurement and corruption) should be interpreted as anti-corruption investigative reporting with strong data-journalism methodology; if Átlátszó publishes procurement analysis, treat the data as reliable but assess whether the framing equally scrutinizes procurement under the new government as it did under the old.

> Articles from **RTL.hu** about domestic constraints should be interpreted as centrist broadcast journalism reflecting what non-Budapest Hungary is hearing; its editorial choices about which stories to lead with signal mainstream narrative formation beyond the digital-media bubble, which becomes especially significant during the MTVA suspension period when RTL will be the only independent broadcast source.

> Articles from **BBJ** about economic and technological statecraft should be interpreted as reflecting the foreign business community's perspective on Hungarian economic policy; emphasizes regulatory predictability, investment climate, and EU market access, potentially underweighting domestic distributional politics.

> Articles from **Honvédelem.hu** about security and defense should be interpreted as official MoD communications; factual details on procurement, exercises, and equipment are reliable, but strategic framing reflects government messaging about defense posture. Under the Magyar government, watch for changes in emphasis regarding NATO cooperation and Russian defense-industrial dependencies — compare with Direkt36 and VSquare for the gap between official narrative and operational reality.

> Articles from **Portfolio.hu** about economic and technological statecraft should be interpreted as market-oriented financial analysis; reliable on financial data, MNB policy, and investor sentiment, but editorially oriented toward market confidence and may underweight structural constraints not reflected in short-term market indicators.

> Articles from **Origo.hu** about any domain should be interpreted as **Fidesz opposition messaging, not independent journalism**. Under the post-transition configuration, Origo functions as the primary channel through which the Fidesz opposition signals what it will attack, what narratives it will promote, and where it sees the Magyar government as vulnerable. Track what Origo attacks to identify politically contested policy areas. **Do not treat any political claim from Origo as factually reliable without cross-verification.**

> Articles from **VSquare.org** about security, intelligence, or diplomatic developments should be interpreted as high-quality English-language investigative journalism produced in collaboration with Direkt36 and Átlátszó, focused on cross-border dimensions of Russian/Chinese influence operations, corruption, and security-sector dynamics in Central Europe. VSquare content on Hungary typically draws on the same sourcing network as Direkt36 but adds Visegrád-regional comparative context.
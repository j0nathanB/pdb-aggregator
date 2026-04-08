# AUDIT SUMMARY: UKRAINE

**Sources assessed:** 18 recommended + 5 excluded + 4 newly identified = 27 total
**Tier 1 (boost=3):** 5 sources
**Tier 2 (boost=2):** 9 sources
**Tier 3 (boost=1):** 5 sources
**Neutral (no rule):** 5 sources
**Discard:** 3 sources
**Overall assessment:** The curation prompt produced an exceptionally strong whitelist reflecting Ukraine's wartime media consolidation — the surviving independent outlets are high-quality and domain-specialized, with the Pravda family (UP, Ekonomichna Pravda, Yevropeiska Pravda) providing unusual structural depth. Key changes: (1) promoted Ekonomichna Pravda and Yevropeiska Pravda to higher tiers than their parent because they fill irreplaceable domain-specific roles; (2) migrated government sources (president.gov.ua, mfa.gov.ua, rada.gov.ua) to Layer 2 at Tier 2; (3) added kmu.gov.ua (Cabinet of Ministers) from the country config as a government source missing from the source map; (4) resolved defense outlet redundancy between Defense Express and Militarnyi; (5) applied non-English domestic premium to Ukrainian-only sources (Ekonomichna Pravda, Texty.org.ua). No blocked domains affect Ukraine's source list — reuters.com is blocked but sits at wire/neutral, not in the boosted tiers.

---

## BOOST ASSIGNMENTS

### Tier 1 — `$boost=3`

**Ukrainska Pravda** | `pravda.com.ua` | Type: `paper_of_record` | Status: `EXISTING`
- **Structural role:** Ukraine's most-read online news outlet and the closest thing to an indispensable single source. Agenda-setter for Kyiv political discourse. Its sub-projects (Ekonomichna Pravda, Yevropeiska Pravda) extend its structural reach into specialized domains.
- **Domain coverage:** Diplomatic alignment, Domestic constraints, Security & defense
- **Reasoning:** Similarweb #1 in Ukraine. Founded by murdered journalist Georgiy Gongadze — institutional independence is foundational to its identity. Known tension with the Office of the President makes its editorial line a live signal of domestic political friction. Breaks presidential and diplomatic leaks consistently. English edition available with 6-12 hour lag. No paywall — fully extractable. The pipeline needs UP surfacing first for any Ukraine query.
- **Non-English premium:** Primary output in Ukrainian. English edition is a summary layer, not a substitute. Ukrainian-language content carries signals that the English edition filters out.

**Dzerkalo Tyzhnia (ZN.UA)** | `zn.ua` | Type: `analytical_weekly` | Status: `EXISTING`
- **Structural role:** Ukraine's most respected analytical publication. Where former officials, security analysts, and policy elites publish long-form assessments that signal elite opinion shifts before they manifest in policy.
- **Domain coverage:** Diplomatic alignment, Domestic constraints, Security & defense
- **Reasoning:** IMI rates it at 100% credibility compliance — the highest mark in Ukrainian media. Publishes expert columns from defense and foreign policy insiders that function as policy trial balloons. Under the Goggle model, ZN.UA's lower publication frequency is offset by its higher signal density per article. When ZN.UA publishes on defense strategy or diplomatic positioning, the pipeline must see it. Limited English section means heavy reliance on Ukrainian-language content.
- **Non-English premium:** Primarily Ukrainian. Limited English edition. Machine translation required for most content, which reinforces the need for boost — the pipeline might otherwise deprioritize non-English results.

**Kyiv Independent** | `kyivindependent.com` | Type: `independent_english` | Status: `EXISTING`
- **Structural role:** Premier English-language source for Ukraine coverage. Founded by ex-Kyiv Post journalists after ownership dispute. Directly pipeline-accessible without translation. Strongest investigative capacity among English-language Ukraine outlets.
- **Domain coverage:** Security & defense, Diplomatic alignment, Domestic constraints
- **Reasoning:** The pipeline's primary zero-translation-cost source for Ukraine. Strong frontline reporting, weapons delivery tracking, and diplomatic coverage. Partial paywall on long-form but news articles free. RSS available. Tier 1 because it is the single source that covers the most domains at the highest quality in the pipeline's native language (English). Not redundant with UP because their editorial selections diverge — KI is shaped for international audiences while UP reflects domestic discourse.

**Defense Express** | `defence-ua.com` | Type: `security_defense` | Status: `EXISTING`
- **Structural role:** Ukraine's leading defense-industry publication. The only source that systematically tracks domestic weapons production, arms deals, foreign military aid deliveries, drone technology, and defense procurement.
- **Domain coverage:** Security & defense autonomy
- **Reasoning:** In a country where defense-industrial autonomy is an existential policy priority, Defense Express fills the structural role that no generalist outlet can. Single-domain but irreplaceable within it — no other source tracks Ukraine's defense-industrial trajectory with comparable granularity. English edition well-maintained. No paywall. Tier 1 because security/defense autonomy is arguably Ukraine's most dynamic analytical domain and Defense Express is the primary source for it.

**Yevropeiska Pravda (European Pravda)** | `eurointegration.com.ua` | Type: `institutional_specialist` | Status: `EXISTING`
- **Structural role:** The only dedicated Ukrainian outlet tracking EU accession benchmarks cluster-by-cluster and NATO relationship dynamics. Irreplaceable for monitoring Ukraine's institutional integration trajectory.
- **Domain coverage:** Diplomatic alignment, Institutional engagement
- **Reasoning:** No other source — domestic or international — covers Ukraine's EU accession negotiations with this granularity. Led by Sergiy Sydorenko. English edition well-maintained. No paywall. Structural uniqueness overrides the narrow domain scope — there is literally no substitute for what Yevropeiska Pravda covers. In a pipeline tracking Ukraine's strategic posture, the EU/NATO integration trajectory is a core analytical axis.

---

### Tier 2 — `$boost=2`

**Ekonomichna Pravda** | `epravda.com.ua` | Type: `business_financial` | Status: `EXISTING`
- **Structural role:** Ukraine's primary outlet for sanctions implementation tracking, reconstruction economics, trade policy, energy sector developments, IMF/World Bank conditionality, and foreign aid flows.
- **Domain coverage:** Economic & technological statecraft
- **Reasoning:** Sole specialized economic outlet on the list. Fills the same structural role El Financiero fills for Mexico — the indispensable economic-domain source. Ukrainian only, which limits pipeline extraction without translation, but machine translation is reliable for structured economic reporting. Tier 2 rather than Tier 1 because single-domain economic coverage is less time-critical than security/diplomatic domains in wartime Ukraine, and the absence of an English edition reduces extraction reliability.
- **Non-English premium applied:** Ukrainian-only source. Boost compensates for the pipeline's tendency to deprioritize non-English results.

**NV (New Voice of Ukraine)** | `nv.ua` | Type: `independent_media` | Status: `EXISTING`
- **Structural role:** Independent media holding with strong opinion section that surfaces elite policy debates. English edition increasingly used for international advocacy monitoring.
- **Domain coverage:** Domestic constraints, Diplomatic alignment, Economic statecraft
- **Reasoning:** Multi-domain coverage with a distinctive opinion section that functions as a forum for policy-elite debate — the closest Ukraine has to a Nexos equivalent. English edition covers major stories. No hard paywall. Tier 2 because its domain coverage overlaps with UP and KI but its opinion-section signal is unique.

**Liga.net** | `liga.net` | Type: `business_political` | Status: `EXISTING`
- **Structural role:** Business/political news portal tracking foreign aid flows, ministry-level policy, tech sector, and reconstruction spending.
- **Domain coverage:** Economic & technological statecraft, Domestic constraints
- **Reasoning:** Complements Ekonomichna Pravda with broader political coverage alongside its business focus. English edition available. No paywall. Tier 2 because its economic coverage partially overlaps with Ekonomichna Pravda, but its political dimension adds value. The config file lists Liga.net as a triage source, confirming its operational importance.

**Ukrinform** | `ukrinform.net` | Type: `state_news_agency` | Status: `EXISTING`
- **Structural role:** Ukraine's national news agency. High-volume wire-service output representing the official state narrative. Divergence between Ukrinform framing and independent outlet framing is itself an analytical signal.
- **Domain coverage:** All five domains (official government line)
- **Reasoning:** Structural role as the state wire service earns Tier 2. The pipeline needs the official narrative baseline to detect divergence. Full English edition. High-volume RSS. No paywall. Not Tier 1 because it is a government mouthpiece, not an independent source — but its structural function (official narrative channel) is essential.

**Interfax-Ukraine** | `interfax.com.ua` | Type: `wire_service` | Status: `EXISTING`
- **Structural role:** Primary wire for economic data releases, business transactions, government tenders, and energy sector reporting. Consistently first to publish GDP, trade, and fiscal data.
- **Domain coverage:** Economic & technological statecraft, Diplomatic alignment
- **Reasoning:** Essential for economic monitoring — the first-mover on structured economic data. English edition comprehensive for economic coverage. Structured data amenable to pipeline extraction. Tier 2 because its wire-service function for economic data is not replicated by any other source on the list.

**President of Ukraine Official Website** | `president.gov.ua` | Type: `official_government` | Status: `EXISTING` — **LAYER 2 MIGRATION**
- **Structural role:** Official decrees, NSDC decisions, international meeting readouts, presidential addresses. Under martial law, presidential communications carry outsized policy weight.
- **Domain coverage:** Diplomatic alignment, Security & defense, Institutional engagement
- **Reasoning:** Primary fetch via Layer 2 direct polling. Goggle boost at Tier 2 as belt-and-suspenders fallback. Under martial law, presidential authority is expanded — this source's structural weight is higher than in peacetime. English version maintained.

**Ministry of Foreign Affairs of Ukraine** | `mfa.gov.ua` | Type: `official_government` | Status: `EXISTING` — **LAYER 2 MIGRATION**
- **Structural role:** Official diplomatic statements, bilateral meeting summaries, multilateral positioning, treaty/agreement announcements.
- **Domain coverage:** Diplomatic alignment, Institutional engagement
- **Reasoning:** Primary source for tracking formal diplomatic posture shifts. Layer 2 primary fetch; Tier 2 Goggle boost as fallback. English edition comprehensive. RSS available.

**Verkhovna Rada Official Site** | `rada.gov.ua` | Type: `legislative_official` | Status: `EXISTING` — **LAYER 2 MIGRATION**
- **Structural role:** Legislative texts, committee hearing records, voting records. Under martial law with elections suspended, parliamentary activity signals reform momentum and EU-related legislation progress.
- **Domain coverage:** Domestic constraints, Institutional engagement
- **Reasoning:** Structural importance amplified by the suspended-elections context — the Rada's legislative output is the primary signal of democratic institutional normalcy. English section limited; legislation in Ukrainian. Bill database at `itd.rada.gov.ua`. Layer 2 primary fetch; Tier 2 Goggle boost as fallback.

**Cabinet of Ministers of Ukraine** | `kmu.gov.ua` | Type: `official_government` | Status: `NEW` — **LAYER 2 MIGRATION**
- **Structural role:** Government policy decisions, cabinet resolutions, economic policy implementation. Present in country config (`ua.yaml`) but absent from the source intelligence map.
- **Domain coverage:** Economic & technological statecraft, Institutional engagement
- **Reasoning:** The source map omitted the Cabinet of Ministers despite its inclusion in the country config. Under Ukraine's constitutional structure, the Cabinet implements economic and reconstruction policy — its resolutions are primary sources for tracking economic statecraft decisions. Layer 2 primary fetch; Tier 2 Goggle boost as fallback.

---

### Tier 3 — `$boost=1`

**Texty.org.ua** | `texty.org.ua` | Type: `data_journalism` / `investigative` | Status: `EXISTING`
- **Structural role:** Ukraine's premier data journalism outlet. Specializes in Telegram influence operation analysis, government spending investigations, and information warfare tracking.
- **Domain coverage:** Domestic constraints, Security & defense
- **Reasoning:** Unique capability — no other source maps coordinated Telegram campaigns or conducts network analysis of information operations at this depth. Their 24-channel anti-NABU campaign exposure is the kind of investigation that reframes understanding of domestic political dynamics. Tier 3 because publication frequency is low and most content is Ukrainian-only with limited English summaries. But when Texty publishes, the signal is high-impact.
- **Non-English premium applied:** Primarily Ukrainian. Boost compensates for pipeline deprioritization of non-English results.

**Razumkov Centre** | `razumkov.org.ua` | Type: `think_tank` | Status: `EXISTING`
- **Structural role:** Ukraine's most established policy think tank. Conducts regular sociological surveys on public attitudes toward NATO, EU, peace negotiations, and trust in institutions.
- **Domain coverage:** All five domains (analytical/polling)
- **Reasoning:** Think tanks earn boost through depth, not speed. Razumkov's polling data is essential for tracking domestic constraint shifts — public opinion on peace negotiations, NATO membership, and institutional trust are core variables for Ukraine's strategic posture. Publishes National Security & Defence journal. English publications available. Tier 3 because think tank output is periodic and analytical, not breaking-news.

**Centre for Economic Strategy (CES)** | `ces.org.ua` | Type: `think_tank` / `economic` | Status: `EXISTING`
- **Structural role:** Publishes the War Economy Tracker — structured, regularly updated dataset on GDP, trade, energy, and fiscal indicators. Reform assessments aligned to EU accession criteria.
- **Domain coverage:** Economic & technological statecraft
- **Reasoning:** The War Economy Tracker is uniquely pipeline-friendly — structured quantitative data that the pipeline can process directly. Tier 3 because output frequency is lower than daily outlets and scope is single-domain (economic), but the structured data format makes it higher-value per publication than most sources.

**Militarnyi** | `militarnyi.com` | Type: `security_defense` | Status: `EXISTING`
- **Structural role:** Military news outlet covering operational developments, equipment deliveries, force structure changes, and military reform.
- **Domain coverage:** Security & defense autonomy
- **Reasoning:** Complements Defense Express (Tier 1, industry-focused) with operational and tactical reporting. Tier 3 rather than higher because Defense Express already covers defense-industrial policy at Tier 1, creating partial redundancy. Militarnyi's operational focus earns it inclusion as supplementary defense coverage. English edition available. Free access.

**UNIAN** | `unian.ua` | Type: `wire_service` | Status: `EXISTING`
- **Structural role:** High-volume wire service with strong political coverage. Rapid detection of diplomatic statements, parliamentary votes, and government personnel changes.
- **Domain coverage:** Diplomatic alignment, Domestic constraints
- **Reasoning:** High volume but lower signal density than UP or KI. Historically linked to Kolomoisky media orbit — currently operating with greater editorial distance, but ownership legacy warrants awareness. Tier 3 because it functions primarily as a speed-of-detection supplement rather than a source of original analysis. English edition available. No paywall.

---

### Neutral — no Goggle rule

**Kyiv Post** | `kyivpost.com` | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Post-2021 ownership change (Adnan Kivan acquisition) caused mass journalist departure and editorial reorientation. Now functions partly as a platform for sponsored content and government-adjacent messaging. Under the Goggle model, no reason to actively discard — it still publishes some original reporting and may surface organically for specific queries. The pipeline's interpretive context handles the editorial caveat. Kyiv Independent fills the structural role Kyiv Post vacated.

**RBC-Ukraine** | `rbc.ua` | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Identified by Texty.org.ua as participating in coordinated information campaigns aligned with OP messaging. This is a credibility concern, not a noise concern — RBC-Ukraine does produce original journalism alongside its problematic coordination patterns. Under Goggle model, organic ranking is appropriate. If it surfaces, the pipeline can process it; no need to waste a discard rule on it. Exclusions default to Neutral, not Discard.

**Censor.net** | `censor.net` | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Butusov's outlet provides frontline commentary with significant reach, but its editorialized, personality-driven format and inconsistent sourcing make it unsuitable for boosting. Under the Goggle model, Censor.net may surface organically for military-related queries where Butusov's frontline access adds value. No need to discard — civil-military friction signals from Butusov's commentary are a useful supplementary input.

**Reuters** | `reuters.com` | Type: `wire_service` | Status: `NEUTRAL`
- **Why neutral:** Not boosted — wire copy surfaces organically. **Blocked by Anthropic's crawler** (`reuters.com` in blocked domains list), which means the pipeline cannot extract full text even if Brave surfaces it. Discovery value only. Interfax-Ukraine and Ukrinform cover wire-service functions domestically.

**AP News** | `apnews.com` | Type: `wire_service` | Status: `NEUTRAL`
- **Why neutral:** International wire service. Not boosted — organic ranking sufficient. Domestic wire services (Ukrinform, Interfax-Ukraine, UNIAN) cover high-volume detection. AP may surface for internationally significant Ukraine events but does not need boost priority over domestic sources.

---

### Discard — `$discard`

**Strana.ua** | `strana.ua` | Status: `CONFIRMED DISCARD`
- **Discard reasoning:** Pro-Russian editorial line; banned under Ukrainian sanctions in 2022. Operates via mirrors and Telegram. Would actively inject Russian-aligned narratives into the pipeline's source ranking, displacing credible sources. Monitoring its narratives has counterintelligence value but that belongs in a separate collection layer, not in the pipeline's boosted whitelist.

**112 Ukraine / NewsOne / ZIK TV** | `112.ua`, `newsone.ua` | Status: `CONFIRMED DISCARD`
- **Discard reasoning:** Banned since 2021 under NSDC sanctions for links to sanctioned oligarch Viktor Medvedchuk. No longer operational in any legal form within Ukraine. Any content surfacing under these domains is either archived, mirror-hosted, or spoofed. Discard to prevent ghost content from occupying result slots.

**Russia Today / TASS / RIA Novosti** | `rt.com`, `tass.com`, `ria.ru` | Status: `NEW DISCARD`
- **Discard reasoning:** Russian state media actively engaged in information warfare against Ukraine. Brave may surface these for Ukraine-related queries due to their high domain authority and volume. Active discard prevents Russian state propaganda from occupying result slots that should go to Ukrainian domestic sources. This is not an editorial judgment — it is a structural decision to prevent adversarial content from displacing pipeline-relevant sources.

---

## STRUCTURAL COVERAGE CHECK

| Structural Role | Source(s) | Tier | Notes |
|---|---|---|---|
| Government leak channel | Ukrainska Pravda | T1 | UP's tension with the Office of the President makes it the outlet where presidential/diplomatic leaks surface. ZN.UA expert columns serve a similar function for security establishment leaks |
| Opposition voice | Dzerkalo Tyzhnia, NV | T1, T2 | Under martial law, formal opposition is muted. ZN.UA's expert columns and NV's opinion section are the primary forums for elite dissent and policy critique |
| Defence/security first-mover | Defense Express, Militarnyi | T1, T3 | Unlike Mexico, Ukraine has dedicated defense press. Defense Express (industry/procurement) and Militarnyi (operational) provide complementary coverage |
| Policy-elite discourse | Dzerkalo Tyzhnia, NV, Razumkov Centre | T1, T2, T3 | ZN.UA is where policy elites publish; NV's opinion section supplements; Razumkov provides polling data on public attitudes |
| Domestic-language depth | Ukrainska Pravda, Ekonomichna Pravda, ZN.UA, Texty.org.ua | T1, T2, T1, T3 | Ukrainian-language sources carry signals filtered out of English editions. Non-English premium applied to Ukrainian-only outlets |
| Official government source | president.gov.ua, mfa.gov.ua, rada.gov.ua, kmu.gov.ua | T2 (all) | **LAYER 2 MIGRATION** — primary fetch via direct polling. Goggle boost as fallback. Covers presidential, diplomatic, legislative, and executive branches |
| Analytical/think tank depth | Razumkov Centre, CES, Texty.org.ua | T3 (all) | Razumkov for polling/policy, CES for economic data, Texty for information warfare analysis |
| Wire service (domestic) | Ukrinform, Interfax-Ukraine, UNIAN | T2, T2, T3 | Domestic wires boosted because international wires (Reuters) are blocked or neutral. Ukrinform doubles as state narrative channel |
| EU/NATO integration specialist | Yevropeiska Pravda | T1 | Irreplaceable single-source structural role. No redundancy |
| Economic statecraft specialist | Ekonomichna Pravda, Liga.net, CES | T2, T2, T3 | Three-source coverage: daily economic news (EP), business-political (Liga), structured data (CES) |
| Data journalism / OSINT | Texty.org.ua | T3 | Unique capability for Telegram network analysis and information warfare tracking |

**Gaps identified:**
1. **Regional political dynamics** beyond Kyiv remain underrepresented. Western Ukraine (Lviv, Ivano-Frankivsk) outlets would add depth on domestic constraint calculations in areas with distinct political orientations, but no single outlet has sufficient pipeline-readiness to add.
2. **Occupied territory information flows** are structurally invisible to the whitelist. Information from occupied Donetsk, Luhansk, Zaporizhzhia, and Kherson oblasts flows primarily through Telegram and Russian-language channels that cannot be whitelisted. This is a known structural limitation.
3. **Non-Western defense-industrial partnerships** (Turkey/Baykar, South Korea, emerging drone supply chains) are covered fragmentarily by Defense Express but may require supplementary monitoring of Turkish and Korean trade press — outside the scope of this country Goggle.
4. **Reconstruction oversight and aid diversion** is flagged as a blind spot in the country config. NABU investigations and EU audit reports would be the signals, but neither has a stable, pipeline-friendly web presence. Mitigated partially by Ekonomichna Pravda's coverage.

---

## REDUNDANCY RESOLUTION

**Pravda family cluster: Ukrainska Pravda + Ekonomichna Pravda + Yevropeiska Pravda**
All three are sub-projects of the same media group, but they function as structurally distinct outlets with non-overlapping domain coverage. UP (general political/diplomatic), EP (economic statecraft), YP (EU/NATO integration). No redundancy — each fills a unique structural role. Tiers differentiated by domain criticality: UP and YP at Tier 1 (their domains are the most dynamic for Ukraine's posture), EP at Tier 2 (economic domain is important but less time-critical in wartime).

**Defense outlet cluster: Defense Express + Militarnyi**
Both cover security/defense. Defense Express leads (Tier 1) because it covers defense-industrial policy, procurement, and arms deals — the structural autonomy dimension. Militarnyi drops to Tier 3 — its operational/tactical focus complements Defense Express but overlaps on equipment deliveries and force structure. Redundancy reduced by tier differentiation.

**Wire service cluster: Ukrinform + Interfax-Ukraine + UNIAN**
Three domestic wire services is a lot, but each has a distinct function. Ukrinform (Tier 2, state narrative channel), Interfax-Ukraine (Tier 2, economic data first-mover), UNIAN (Tier 3, high-volume political detection). UNIAN drops lowest because its signal density is lowest and its Kolomoisky ownership legacy introduces editorial uncertainty.

**English-language cluster: Kyiv Independent + NV English + UNIAN English**
KI leads (Tier 1) as the primary English-language source. NV English (Tier 2) supplements with opinion/policy debate. UNIAN English (Tier 3) is a high-volume supplement. No extraction redundancy — each has a different editorial focus.

**Government source cluster: president.gov.ua + mfa.gov.ua + rada.gov.ua + kmu.gov.ua**
Four government domains but each covers a distinct institutional branch. All at Tier 2 with Layer 2 migration. No redundancy — presidential, diplomatic, legislative, and executive branches each produce distinct policy signals.

---

## QUERY CONFIGURATION

```
country: UA
search_lang: uk
freshness: pw
```

**Multi-language notes:** Ukraine's media operates primarily in Ukrainian, with significant Russian-language consumption persisting in everyday use. The pipeline should run primary queries in Ukrainian. A secondary English query cycle captures Kyiv Independent, Defense Express English, and international wire coverage. The `languages.primary: uk` and `languages.metadata: en` configuration in `ua.yaml` handles this correctly. Russian-language queries are not recommended — the pipeline should not optimize for Russian-language Ukrainian media, as the highest-quality outlets now publish primarily in Ukrainian.

**Localized query vocabulary validation:**

The curation prompt's vocabulary is comprehensive and well-structured. Notes:

- **Domain 1 (Diplomatic):** All terms valid. Add `"Зеленський дипломатія"` (Zelensky diplomacy) as a leader-specific pattern. `"формула миру"` (peace formula) is high-signal — Ukraine's own framework for negotiations. Add `"мирний план"` (peace plan) for broader peace-deal coverage. Consider `"саміт"` (summit) as a generic high-signal term for multilateral events.
- **Domain 2 (Security):** Strong list. Add `"Сирський"` (Syrskyi) as leader-specific for military command decisions. `"дрони"` / `"БПЛА"` (drones/UAVs) is missing — the dominant frame for defense-industrial autonomy since 2023. Add `"далекобійна зброя"` (long-range weapons) for the critical debate on strike capabilities. `"Ф-16"` / `"F-16"` remains relevant for Western equipment integration.
- **Domain 3 (Economic):** Excellent coverage. Add `"заморожені активи"` (frozen assets) — the debate over using Russian frozen assets for reconstruction is a core economic statecraft issue. `"конфіскація активів"` is listed but the frozen-assets framing is more commonly used in current discourse. Add `"грант ЄС"` (EU grant) and `"макрофінансова допомога"` (macro-financial assistance) for EU aid tracking.
- **Domain 4 (Institutional):** Valid. Add `"скринінг"` (screening) — the specific term for the EU accession screening process currently underway. `"переговорний кластер"` is correct but add `"відкриття кластеру"` (cluster opening) for the specific milestone events. Add `"НАБУ"` (NABU — National Anti-Corruption Bureau) as an institutional reform signal.
- **Domain 5 (Domestic):** Strong. Add `"легітимність"` (legitimacy) — the running debate over Zelensky's mandate with elections suspended under martial law. `"демобілізація"` is listed and highly relevant. Add `"ротація"` (rotation) for the military rotation/mobilization debate. Add `"Telegram"` — the platform itself is a political flashpoint (potential bans, influence operations).

**Stale/problematic terms:** None are stale given the ongoing conflict. All five domains remain active and the vocabulary reflects current discourse accurately.

**Suggested topic query patterns:**

1. `Зеленський формула миру саміт дипломатія` — Peace negotiations and diplomatic positioning
2. `оборонно-промисловий комплекс дрони власне виробництво` — Defense-industrial autonomy and drone production
3. `відбудова заморожені активи ЄС макрофінансова допомога` — Reconstruction funding and frozen assets
4. `євроінтеграція скринінг переговорний кластер реформи` — EU accession progress
5. `воєнний стан легітимність демобілізація мобілізація` — Domestic constraints on governance

---

## GOGGLE FILE

```goggle
! name: MPM Ukraine
! description: MPM pipeline source prioritization for Ukraine — boosts high-signal sources, discards noise and adversarial state media
! public: false
! author: MPM Pipeline

! --- Tier 1: Essential (boost=3) ---
$boost=3,site=pravda.com.ua
$boost=3,site=zn.ua
$boost=3,site=kyivindependent.com
$boost=3,site=defence-ua.com
$boost=3,site=eurointegration.com.ua

! --- Tier 2: Important (boost=2) ---
$boost=2,site=epravda.com.ua
$boost=2,site=nv.ua
$boost=2,site=liga.net
$boost=2,site=ukrinform.net
$boost=2,site=interfax.com.ua
$boost=2,site=president.gov.ua
$boost=2,site=mfa.gov.ua
$boost=2,site=rada.gov.ua
$boost=2,site=kmu.gov.ua

! --- Tier 3: Supplementary (boost=1) ---
$boost=1,site=texty.org.ua
$boost=1,site=razumkov.org.ua
$boost=1,site=ces.org.ua
$boost=1,site=militarnyi.com
$boost=1,site=unian.ua

! --- Discard: Noise and adversarial ---
$discard,site=strana.ua
$discard,site=112.ua
$discard,site=newsone.ua
$discard,site=rt.com
$discard,site=tass.com
$discard,site=ria.ru
```

---

## INTERPRETIVE CONTEXT FOR DOSSIER

### Tier 1 Sources

> Articles from **Ukrainska Pravda** about presidential decisions and diplomatic developments should be interpreted as Ukraine's most authoritative independent reporting — its founding by Georgiy Gongadze and ongoing tension with the Office of the President make it the outlet most likely to publish information the government would prefer to suppress. Its editorial line is pro-sovereignty and center-liberal, meaning it supports Ukraine's Western integration but scrutinizes the executive's methods.

> Articles from **Dzerkalo Tyzhnia (ZN.UA)** about defense strategy and diplomatic positioning should be interpreted as reflecting elite policy consensus or emerging elite dissent — its expert columns are written by former officials and security insiders who use ZN.UA as a channel for policy trial balloons and institutional critique. When ZN.UA publishes a critical assessment of military strategy or diplomatic direction, it likely reflects concerns circulating within the security establishment.

> Articles from **Kyiv Independent** about frontline developments and international diplomacy should be interpreted as English-language reporting shaped for international audiences — its editorial decisions reflect what the outlet considers relevant to Western policymakers and donors. This makes it an excellent source for understanding how Ukraine presents itself externally, but it may underweight domestic political dynamics that are not internationally salient.

> Articles from **Defense Express** about weapons systems and defense procurement should be interpreted as defense-industry specialist reporting with a pro-Ukrainian-industry orientation — the outlet supports domestic defense production and may frame foreign military aid as supplementary to rather than substitutive for domestic capability. Its technical reporting on equipment and procurement is highly reliable; its framing of defense-industrial policy reflects an advocacy position for Ukrainian defense autonomy.

> Articles from **Yevropeiska Pravda** about EU accession and NATO engagement should be interpreted as the most granular available tracking of institutional integration milestones — led by Sergiy Sydorenko, it covers cluster-by-cluster negotiation progress that no other outlet monitors. Its editorial orientation is strongly pro-integration, meaning it may underweight obstacles or frame setbacks as temporary. When Yevropeiska Pravda reports negative accession developments, the signal is especially strong because it contradicts the outlet's institutional optimism.

### Tier 2 Sources

> Articles from **Ekonomichna Pravda** about sanctions, reconstruction, and trade should be interpreted as Ukraine's most authoritative specialized economic reporting — it covers IMF conditionality, aid flows, and energy sector developments with the granularity that generalist outlets cannot match. Its framing tends toward reform-oriented economics, meaning it may be critical of state intervention or protectionist measures.

> Articles from **NV (New Voice of Ukraine)** about domestic political dynamics should be interpreted as reflecting the perspective of Ukraine's professional urban middle class — its opinion section surfaces elite policy debates and its editorial line is center-liberal, pro-reform, and pro-Western. NV's English edition is increasingly shaped for international advocacy, which means English-language content may diverge from the Ukrainian-language original in emphasis.

> Articles from **Liga.net** about business policy and reconstruction spending should be interpreted as business-community-oriented reporting with a pragmatic editorial line — it tracks what matters to Ukrainian business interests, including foreign investment, regulatory changes, and tech sector developments. Less ideologically oriented than other outlets, which makes it useful for calibrating against more editorial sources.

> Articles from **Ukrinform** about any topic should be interpreted as the official Ukrainian state narrative — not journalism but the government's chosen public messaging. Ukrinform's framing of military events, diplomatic engagements, and policy decisions represents what the state wants domestic and international audiences to see. Divergence between Ukrinform and independent outlets (especially Ukrainska Pravda) is itself an analytical signal indicating where the government narrative is under strain.

> Articles from **Interfax-Ukraine** about economic data and business transactions should be interpreted as wire-service reporting with minimal editorial filtering — its value is speed and breadth on economic indicators, not analytical depth. First to publish GDP, trade, and fiscal data. Its economic reporting is more reliable than its political coverage.

> Articles from **government sources** (president.gov.ua, mfa.gov.ua, rada.gov.ua, kmu.gov.ua) should be interpreted as official primary source material — not journalism but institutional communications. Presidential readouts of foreign leader meetings, MFA diplomatic statements, Rada legislative records, and Cabinet resolutions represent the government's formal positions. Under martial law, presidential communications carry especially outsized weight relative to other branches. These sources establish what the government says it is doing; independent outlets verify whether it is.

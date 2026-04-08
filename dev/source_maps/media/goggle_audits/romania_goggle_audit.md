# AUDIT SUMMARY: ROMANIA

**Sources assessed:** 17 recommended + 5 excluded + 4 newly identified = 26 total
**Tier 1 (boost=3):** 4 sources
**Tier 2 (boost=2):** 8 sources
**Tier 3 (boost=1):** 5 sources
**Neutral (no rule):** 6 sources
**Discard:** 3 sources
**Overall assessment:** The curation prompt produced a well-structured whitelist with strong coverage of the post-election-annulment political landscape and Romania's NATO Eastern Flank role. Key changes: (1) promoted government sources (Presidency, MApN, MAE) for Layer 2 migration at Tier 2; (2) applied non-English domestic premium to Romanian-language independents (G4Media, Recorder, RISE Project) that carry investigative depth unavailable in English; (3) flagged `libertatea.ro` as blocked by Anthropic's crawler; (4) resolved redundancy between business outlets (ZF vs. Profit.ro) and between English-language aggregation paths (Romania Insider vs. Euronews Romania tag); (5) added missing wire and parliamentary structural roles. The closure of Europa Libera (RFE/RL Romanian) in March 2026 is a material loss — no replacement source fully fills that independent analytical niche.

---

## BOOST ASSIGNMENTS

### Tier 1 — `$boost=3`

**G4Media** | `g4media.ro` | Type: `independent_digital` | Status: `EXISTING`
- **Structural role:** Romania's most influential independent political news outlet. Reader-funded, founded by veteran journalists. Top-5 most-quoted online portal. Functions as Romania's agenda-setter for politically literate audiences — the outlet where coalition dynamics, defense decisions, and EU policy negotiations break first.
- **Domain coverage:** All five domains — strongest on diplomatic alignment, domestic constraints, institutional engagement
- **Reasoning:** G4Media is the closest Romania has to an indispensable single source. Its independence from oligarch ownership (reader-funded model) gives it credibility that Digi24 and HotNews cannot match. Romanian-language primary output earns the non-English domestic premium — this is where the Romanian political class leaks to and reads from. English section covers select articles but the Romanian feed is the primary signal. Free and extractable.
- **Extraction note:** Open access; RSS available; English section provides select translations with delay.

**Digi24** | `digi24.ro` | Type: `broadcaster_portal` | Status: `EXISTING`
- **Structural role:** Largest online news audience in Romania (~9M monthly uniques). Most centrist of the major TV-online platforms. "Least Biased" rating from MBFC. Functions as Romania's mainstream discourse barometer — what Digi24 frames as important shapes public conversation.
- **Domain coverage:** All five domains — broadest mainstream reach
- **Reasoning:** Structural role as Romania's highest-traffic news portal earns Tier 1. Centrist editorial positioning means its framing reflects the mainstream consensus rather than oligarch interests (unlike Antena 3 or Romania TV). Romanian-only video content limits extraction, but text articles are comprehensive and freely accessible. Already designated as `triage_source: true` in ro.yaml, confirming its pipeline priority.

**AGERPRES** | `agerpres.ro` | Type: `state_wire_agency` | Status: `EXISTING`
- **Structural role:** Romania's national news agency. First-mover on all official communiques — presidential statements, MFA readouts, defense ministry announcements. Indispensable for detecting the timing and framing of state posture signals.
- **Domain coverage:** Diplomatic alignment, Security & defense, Institutional engagement
- **Reasoning:** State wire agencies earn Tier 1 because they are the canonical source for official position statements. AGERPRES publishes government-released positions verbatim, making it the pipeline's primary signal for detecting when Romania formally shifts posture. The English feed covers major items with slight delay. Free, RSS available, easily extractable. In a country where the president holds constitutional authority over defense and foreign policy, the wire service that carries presidential and CSAT communiques first is structurally essential.

**Ziarul Financiar** | `zf.ro` | Type: `business_financial` | Status: `EXISTING`
- **Structural role:** Romania's leading business newspaper. The sole specialized business daily with an English edition. Covers FDI flows, energy sector (critical — Romania is the EU's largest gas producer), fiscal policy, EU funds absorption, defense-industrial base, and tech sovereignty.
- **Domain coverage:** Economic & technological statecraft
- **Reasoning:** No other source covers Romania's economic statecraft at this depth — Black Sea gas developments, Three Seas Initiative participation, EU fiscal compliance, nearshoring dynamics, and defense procurement economics all pass through ZF's reporting. English edition (`zfenglish.com`) adds pipeline accessibility. Sole Tier 1 for economic statecraft, analogous to El Financiero's role in the Mexico Goggle. Free for most content.

---

### Tier 2 — `$boost=2`

**HotNews.ro** | `hotnews.ro` | Type: `digital_native` | Status: `EXISTING`
- **Structural role:** Romania's first digital newsroom (est. 2005). Strong on EU affairs, political analysis, and economic policy. English-language section provides translated key articles — valuable for automated pipeline integration.
- **Domain coverage:** Diplomatic alignment, Domestic constraints, Economic statecraft
- **Reasoning:** Already designated as `triage_source: true` in ro.yaml. English section adds pipeline accessibility. Tier 2 rather than Tier 1 because it breaks fewer original stories than G4Media and its 2022 acquisition by Multi Media Est introduces ownership-transparency questions that slightly reduce editorial independence confidence. The EU affairs and political analysis depth earns a strong Tier 2.

**Recorder** | `recorder.ro` | Type: `investigative` | Status: `EXISTING`
- **Structural role:** Romania's premier investigative video journalism outlet. Long-form investigations have exposed political-party media financing deals and procurement irregularities. Reaches ~11% of the Romanian news audience. Investigations frequently trigger parliamentary and judicial responses.
- **Domain coverage:** Domestic constraints, Security & defense (procurement)
- **Reasoning:** Non-English domestic premium applies — Recorder operates exclusively in Romanian and its video investigations surface domestic institutional stress signals unavailable in English. Narrower domain than G4Media but irreplaceable within its niche. Tier 2 rather than Tier 1 because it lacks structured data feeds (video-heavy, YouTube-based), reducing pipeline extraction reliability. But when Recorder publishes, the investigations are high-impact.
- **Extraction note:** Video-heavy; no structured data feed. Pipeline may need to rely on text summaries/articles that accompany video investigations.

**RISE Project** | `riseproject.ro` | Type: `investigative` | Status: `EXISTING`
- **Structural role:** Non-profit investigative journalism, member of OCCRP consortium. Cross-border investigative capability (organized crime, corruption networks, offshore finance). Investigations surface in international media.
- **Domain coverage:** Domestic constraints, Economic statecraft (illicit finance, procurement)
- **Reasoning:** OCCRP membership gives RISE Project unique cross-border investigative reach — sanctions-evasion vectors, elite capture, and defense-sector irregularities relevant to Romania's strategic posture. Non-English domestic premium applies (primarily Romanian). Tier 2 rather than Tier 1 because publication is irregular and domain coverage is narrow. But within its niche (corruption networks, illicit finance), nothing else on the list competes. Some investigations available in English via OCCRP network.

**Președinția României** | `presidency.ro` | Type: `government_primary` | Status: `EXISTING` — **LAYER 2 MIGRATION**
- **Structural role:** The Romanian president holds constitutional authority over defense and foreign policy. Presidential communiques, CSAT (Supreme Defense Council) decisions, and summit readouts are primary signals of strategic posture.
- **Domain coverage:** Diplomatic alignment, Security & defense autonomy
- **Reasoning:** Government sources = Layer 2 migration at Tier 2. Primary fetch via Layer 2 direct polling; Goggle boost as belt-and-suspenders fallback. Under President Nicusor Dan (since May 2025), tracking presidential statements is essential for detecting alignment shifts. English translations of major statements available.

**MApN (Ministry of National Defence)** | `mapn.ro` | Type: `government_primary` | Status: `EXISTING` — **LAYER 2 MIGRATION**
- **Structural role:** Direct source for defense procurement contracts, NATO exercise participation, bilateral military cooperation, airspace incident reports (critical given proximity to Ukraine conflict zone).
- **Domain coverage:** Security & defense autonomy
- **Reasoning:** Government sources = Layer 2 migration at Tier 2. MApN publishes radar-detection communiques for cross-border aerial incidents — a unique primary signal in a country on NATO's Eastern Flank bordering an active war zone. No RSS — requires periodic scraping or polling, making Layer 2 direct polling the correct primary fetch mechanism.

**MAE (Ministry of Foreign Affairs)** | `mae.ro` | Type: `government_primary` | Status: `EXISTING` — **LAYER 2 MIGRATION**
- **Structural role:** Official readouts of bilateral meetings, multilateral positioning (EU Council, NATO summits, OSCE, UN), and consular/diaspora policy.
- **Domain coverage:** Diplomatic alignment, Institutional engagement
- **Reasoning:** Government sources = Layer 2 migration at Tier 2. Key for tracking Romania's posture toward Moldova, Ukraine, Black Sea cooperation, and OECD accession process. English section covers major diplomatic activity. No dedicated RSS — polling required.

**New Strategy Center** | `newstrategycenter.ro` | Type: `think_tank` | Status: `EXISTING`
- **Structural role:** Romania's leading security/defense think tank. Publishes policy papers on NATO Eastern Flank posture, Black Sea security, energy security, cyber/hybrid threats, and Romania-Moldova relations.
- **Domain coverage:** Security & defense autonomy, Diplomatic alignment
- **Reasoning:** Think tanks earn boost through depth, not speed. New Strategy Center outputs often reflect or anticipate elite security-establishment thinking — its analysis provides the structural interpretation layer the pipeline needs to contextualize daily events. English publications available. Tier 2 rather than Tier 1 because low publication frequency limits pipeline utility, but the analytical depth is irreplaceable for understanding Romania's security posture.

**Romania Insider** | `romania-insider.com` | Type: `english_aggregator` | Status: `EXISTING`
- **Structural role:** Most comprehensive English-language daily coverage of Romanian politics, defense, economy, and society. Functions as a translation-and-curation layer over Romanian-language sources.
- **Domain coverage:** All five domains (overview level, via curation)
- **Reasoning:** High utility for automated English-language pipeline ingestion. Its editorial selection functions as a filter — it surfaces what matters to the English-speaking diplomatic and business community. Tier 2 rather than Tier 1 because it's a curation/translation layer, not an original reporting source. But its daily output, RSS availability, and full English-language coverage make it structurally more valuable than a typical aggregator — it's the pipeline's primary English-language signal detector for Romania.

---

### Tier 3 — `$boost=1`

**PressOne** | `pressone.ro` | Type: `investigative_narrative` | Status: `EXISTING`
- **Structural role:** Independent investigative and narrative journalism. Covers institutional dysfunction, judicial independence, civil society, and democratic backsliding concerns. Cluj-Napoca base provides a non-Bucharest perspective.
- **Domain coverage:** Domestic constraints, Institutional engagement
- **Reasoning:** Fills a genuine gap on democratic governance and institutional health — PressOne covers judicial independence and civil society dynamics that the higher-tier investigative outlets (Recorder, RISE Project) don't systematically track. Non-English domestic premium applies (Romanian only). Tier 3 because irregular publication cadence and narrow domain scope limit pipeline utility, but the boost ensures its periodic investigations surface when they appear. Partially fills the gap left by Europa Libera's closure.

**Profit.ro** | `profit.ro` | Type: `business_online` | Status: `EXISTING`
- **Structural role:** Online business/economic news portal. Complements ZF with faster-cycle economic reporting. Strong on energy markets, fiscal deficit tracking, state budget dynamics, and corporate transactions.
- **Domain coverage:** Economic & technological statecraft
- **Reasoning:** Tier 3 rather than Tier 2 because redundant with Ziarul Financiar (Tier 1) on economic statecraft. ZF leads with deeper analysis and an English edition; Profit.ro adds speed and energy-market granularity. Romanian only. Premium content (Profit Insider) behind paywall limits full extraction, but core content is open access. The redundancy reduction principle drops this below ZF, but the energy-market niche (Romania as EU's largest gas producer) earns Tier 3 rather than Neutral.

**Euronews Romania** | `euronews.com/tag/romania` | Type: `international_broadcast` | Status: `EXISTING`
- **Structural role:** Provides external-facing coverage of Romania within the EU framework. Tracks how Romania's positions are perceived and reported at the European level.
- **Domain coverage:** Diplomatic alignment, Institutional engagement, Security & defense
- **Reasoning:** Useful for the pipeline's interpretive layer — shows how Romania's posture appears from Brussels rather than Bucharest. Tier 3 because coverage is episodic and filtered through a pan-European editorial lens that dilutes Romania-specific depth. But the EU-institutional perspective on Schengen accession, common defense, and Council votes is unique among the sources listed.

**Parlamentul României** | `cdep.ro` / `senat.ro` | Type: `legislative_official` | Status: `NEW` — **LAYER 2 MIGRATION**
- **Structural role:** Official parliamentary records — Chamber of Deputies and Senate. Houses legislative texts, committee proceedings, and voting records.
- **Domain coverage:** Domestic constraints, Institutional engagement
- **Reasoning:** Missing structural role in original whitelist. The curation prompt included no legislative source despite Parliament being the venue where coalition dynamics, defense budget votes, and EU treaty ratifications are formally contested. Layer 2 direct polling is the primary fetch mechanism. Goggle boost at Tier 3 as fallback — parliamentary records occasionally surface in Brave for specific legislative queries. Romanian only.

**Expert Forum (EFOR)** | `expertforum.ro` | Type: `think_tank` | Status: `NEW`
- **Structural role:** Romanian good-governance think tank focused on rule of law, anti-corruption policy, public administration reform, and EU integration conditionality. Publishes in Romanian and English.
- **Domain coverage:** Domestic constraints, Institutional engagement
- **Reasoning:** Missing structural role — the original whitelist had only one think tank (New Strategy Center, security-focused). EFOR fills the governance/institutional analysis gap, complementing New Strategy Center's security focus. Think tanks earn boost through depth, not speed. Tier 3 because publication frequency is low and domain scope is narrower than New Strategy Center, but its rule-of-law analysis is essential for interpreting Romania's capacity for external action.

---

### Neutral — no Goggle rule

**Libertatea** | `libertatea.ro` | Type: `general_news` | Status: `EXISTING → DEMOTED TO NEUTRAL`
- **Why neutral:** Large audience reach and useful for tracking populist narratives and public sentiment, but **blocked by Anthropic's crawler** (`libertatea.ro` in blocked domains list). Even if Brave surfaces Libertatea results, the pipeline cannot extract full text. Its domestic-mood coverage niche is partially filled by Digi24 (Tier 1) and Antena 3 (Neutral, for discourse monitoring). Leave neutral — may surface organically and provide headlines even without full extraction.
- **Blocked domain flag:** Yes — `libertatea.ro` confirmed on blocked_domains.md.

**Antena 3 CNN** | `antena3.ro` | Type: `broadcaster_partisan` | Status: `EXISTING → CONFIRMED NEUTRAL (was recommended)`
- **Why neutral:** The curation prompt correctly identified Antena 3 as included "not for reliability but for discourse monitoring." Under the Goggle model, this means Neutral rather than boosted — the pipeline benefits from seeing Antena 3's nationalist-populist framing when it surfaces organically, but should not actively boost it above higher-signal sources. Voiculescu family ownership (Intact Media Group) and centre-right to nationalist-populist editorial line make it essential for detecting counter-discourse, but organic ranking handles this appropriately. Exclusions default to Neutral, not Discard.

**Mediafax** | `mediafax.ro` | Type: `wire_agency` | Status: `EXCLUDED → CONFIRMED NEUTRAL`
- **Why neutral:** Legacy wire agency now subsumed under Dan Sucu's media group. Output largely duplicative of AGERPRES (Tier 1). But under the Goggle model, no reason to actively discard — if Mediafax breaks a story or surfaces in Brave results, the pipeline benefits from seeing it. ZF (same ownership group, Tier 1) is the more analytically useful product.

**Adevaul** | `adevarul.ro` | Type: `national_daily` | Status: `EXCLUDED → CONFIRMED NEUTRAL`
- **Why neutral:** Editorial quality compromised by ownership under Cristian Burci, with documented political entanglements. Coverage duplicative of included sources. But under the Goggle model, exclusions default to Neutral not Discard — declining audience means it rarely surfaces in top results anyway. No active harm from organic ranking.

**Reuters (Romania coverage)** | `reuters.com` | Type: `wire_service` | Status: `CONFIRMED NEUTRAL`
- **Why neutral:** Wire copy available organically. **Blocked by Anthropic's crawler** (`reuters.com` in blocked domains list), which means extraction via pipeline tools will fail even if Brave surfaces it for discovery. Not boosted in Goggle — wire copy from Reuters on Romania is episodic and the pipeline has better primary sources. AP News (not blocked) serves as the accessible international wire fallback.

**AP News** | `apnews.com` | Type: `wire_service` | Status: `CONFIRMED NEUTRAL`
- **Why neutral:** International wire service with occasional Romania coverage. Not boosted because wire copy on Romania is infrequent and the pipeline has dedicated domestic sources. Organic ranking is appropriate — surfaces for major events (NATO summits, elections, incidents).

---

### Discard — `$discard`

**Romania TV (RTV)** | `romaniatv.net` | Status: `CONFIRMED DISCARD`
- **Discard reasoning:** Overtly pro-PSD partisan television channel with low factual reliability and frequent disinformation. The curation prompt correctly excluded it. Unlike Antena 3 (which has discourse-monitoring value as the leading nationalist-populist voice), Romania TV's signal is already captured indirectly through G4Media and Recorder's media-monitoring reporting. Would actively displace higher-signal sources from top results. Pure partisan noise.

**Realitatea TV** | `realitatea.net` | Status: `CONFIRMED DISCARD`
- **Discard reasoning:** Minor news television channel with narrow, politically aligned audience. Signal-to-noise ratio too poor for structured collection. Web presence is minimal — would waste result slots without adding signal.

**B1 TV** | `b1tv.ro` | Status: `CONFIRMED DISCARD`
- **Discard reasoning:** Same logic as Realitatea TV — minor partisan broadcaster with narrow audience and poor signal-to-noise ratio. No original reporting that the pipeline cannot obtain from better sources.

---

## STRUCTURAL COVERAGE CHECK

| Structural Role | Source(s) | Tier | Notes |
|---|---|---|---|
| Government leak channel / signaling outlet | Antena 3 (PSD-adjacent framing) | Neutral | Romania lacks a single government-aligned outlet equivalent to Mexico's La Jornada. PSD messaging surfaces through Antena 3 and Romania TV — Antena 3 at Neutral captures this organically. G4Media (Tier 1) often reports leaked coalition dynamics |
| Opposition voice | G4Media, HotNews, Recorder, RISE Project | T1, T2, T2, T2 | Romania's independent outlets are structurally opposition-adjacent by virtue of anti-corruption investigative mandates. No dedicated "opposition outlet" — the independents collectively fill this role |
| Defence/security first-mover | MApN press office, New Strategy Center | T2, T2 | MApN is the primary source for defense procurement, NATO exercises, and airspace incidents. New Strategy Center provides analytical depth. No dedicated defense press — gap mitigated by Layer 2 polling of MApN |
| Policy-elite discourse | New Strategy Center, Expert Forum | T2, T3 | Think tank coverage split between security (NSC) and governance (EFOR). Thin compared to larger countries but reflects Romania's think tank ecosystem |
| Domestic-language depth | G4Media, Digi24, Recorder, RISE Project, PressOne, Profit.ro | T1–T3 | Romanian-language sources carry the investigative and analytical depth. English sources (Romania Insider, Euronews Romania, HotNews English) are access paths, not substitutes |
| Official government source | Presidency.ro, MApN, MAE, Parlamentul | T2, T2, T2, T3 | **LAYER 2 MIGRATION** — primary fetch via direct polling. Goggle boost as fallback. Covers executive, defense, foreign affairs, and legislative branches |
| Analytical/think tank depth | New Strategy Center, Expert Forum | T2, T3 | NSC for security/defense analysis; EFOR for governance/rule-of-law. Gap: no dedicated economic think tank on the list |
| Wire service (domestic) | AGERPRES | T1 | State wire agency — structural Tier 1 for official position detection. International wires (Reuters, AP) at Neutral for organic supplementation |
| Economic statecraft specialist | Ziarul Financiar, Profit.ro | T1, T3 | ZF leads; Profit.ro supplements with speed and energy-market granularity |
| English-language access layer | Romania Insider, HotNews English, ZF English | T2, T2, T1 | Three English-language pathways ensure pipeline accessibility for non-Romanian queries |

**Gaps identified:**
1. **Black Sea regional security analysis** remains a structural blind spot — coverage of Turkey-Romania bilateral dynamics, trilateral formats with Poland, and sub-regional frameworks (Three Seas Initiative) is scattered across think-tank outputs and occasional press reporting. No single outlet systematically produces this analysis. Partially mitigated by New Strategy Center's Black Sea security papers.
2. **Technology sovereignty and cyber policy** coverage is episodic — Romania hosts the EU's European Cybersecurity Competence Centre (ECCC) in Bucharest, but no source on the list systematically tracks cyber defense, tech sovereignty, or digital infrastructure policy. Business outlets (ZF, Profit.ro) cover this intermittently.
3. **Europa Libera gap** — RFE/RL's Romanian service ceasing operations (March 31, 2026) removes a significant independent analytical voice on democratic institutions and judicial independence. PressOne and G4Media partially fill this gap but neither matches Europa Libera's depth on rule-of-law coverage.
4. **Hungarian-minority media** — Romania's `languages.additional: [hu]` in ro.yaml acknowledges Hungarian as a significant minority language, but no Hungarian-language source is included. For Transylvania-specific dynamics and UDMR (Hungarian minority party) positioning, Hungarian-language outlets like Maszol.ro or Kronika.ro could add signal. Not included to avoid over-expanding the Goggle, but flagged for future consideration.

---

## REDUNDANCY RESOLUTION

**Business press cluster: Ziarul Financiar + Profit.ro**
Both cover economic statecraft. ZF leads (Tier 1) due to deeper analysis, English edition, and broader coverage of FDI, energy, and fiscal policy. Profit.ro drops to Tier 3 — redundant on core economic coverage, but its faster-cycle reporting and energy-market granularity (Black Sea gas, Romania as EU's largest gas producer) earn a supplementary boost rather than Neutral.

**Investigative cluster: Recorder + RISE Project + PressOne**
Three investigative outlets, each with a distinct niche. Recorder (Tier 2, video-format domestic investigations triggering parliamentary responses), RISE Project (Tier 2, cross-border financial and corruption investigations via OCCRP), PressOne (Tier 3, narrative journalism on institutional dysfunction and democratic governance). No redundancy — each covers different vectors of domestic constraint. The pipeline benefits from investigative plurality, particularly in the post-election-annulment political environment.

**English-language access cluster: Romania Insider + Euronews Romania + HotNews English**
Three English-language pathways. Romania Insider (Tier 2, comprehensive daily curation of Romanian news in English — highest utility for pipeline ingestion), HotNews English (Tier 2, translated key articles with original reporting), Euronews Romania tag (Tier 3, EU-institutional perspective, episodic). Romania Insider and HotNews English are differentiated — one curates/translates domestic coverage broadly, the other produces original political analysis. Euronews drops to Tier 3 for its narrow EU-institutional angle. No discard needed.

**Government source cluster: Presidency + MApN + MAE + Parliament**
Four government sources, each covering a distinct constitutional function. No redundancy — the president (defense/foreign policy authority), defense ministry (military operations/procurement), foreign ministry (diplomatic readouts), and parliament (legislation/coalition dynamics) produce non-overlapping primary signals. All designated for Layer 2 migration with Goggle boost as fallback.

**Mainstream broadcaster cluster: Digi24 + Antena 3**
Digi24 (Tier 1, centrist, highest traffic) vs. Antena 3 (Neutral, nationalist-populist). Resolved by structural role differentiation — Digi24 captures mainstream consensus framing, Antena 3 captures nationalist counter-discourse. No redundancy; both signals are needed. Antena 3 at Neutral means organic ranking surfaces it when relevant without displacing Digi24.

---

## QUERY CONFIGURATION

```
country: RO
search_lang: ro
freshness: pw
```

**Multi-language notes:** Romania's media ecosystem operates primarily in Romanian. English-language sources (Romania Insider, HotNews English, ZF English, Euronews Romania tag, New Strategy Center English publications) provide access pathways but the primary signal lives in Romanian. Queries should run primarily in Romanian; a secondary English query cycle for defense/NATO topics and think tank analysis would capture international coverage. The pipeline's existing `languages.metadata: en` configuration handles this correctly. Hungarian (`languages.additional: [hu]`) is relevant for Transylvania-specific dynamics but not included in primary query configuration.

**Localized query vocabulary validation:**

The curation prompt's vocabulary is solid. Notes:

- **Domain 1 (Diplomatic):** All terms valid. Add `"Nicusor Dan politica externa"` as leader-specific pattern (new president since May 2025). `"Republica Moldova integrare"` is correct and high-priority — Romania-Moldova relations are a defining alignment vector. Add `"formatul B9"` (Bucharest Nine) as it appears frequently in Romanian-language press. `"Marea Neagra securitate"` should also pair with `"cooperare trilaterala"` to capture Romania-Poland-Turkey format discussions.
- **Domain 2 (Security):** Strong list. `"CSAT"` is essential and correctly included. Add `"Kogalniceanu baza"` (Mihail Kogalniceanu Air Base — NATO's largest Eastern Flank base expansion). Add `"incident spatiu aerian"` (airspace incident) — critical given drone/missile overflight incidents from Ukraine conflict. `"Flancul Estic NATO"` is correct and high-frequency.
- **Domain 3 (Economic):** Excellent. `"Marea Neagra gaze"` captures Black Sea gas developments correctly. Add `"Neptun Deep"` (the specific offshore gas project — OMV Petrom/Romgaz). Add `"absorbtie fonduri europene"` (EU funds absorption rate — a persistent structural concern). `"deficit bugetar"` is correct and high-signal given Romania's excessive deficit procedure.
- **Domain 4 (Institutional):** Valid. `"aderare OCDE"` is timely — Romania's OECD accession process is active. Add `"MCV"` (Cooperation and Verification Mechanism — though formally lifted, still referenced in rule-of-law discussions). `"presedintia Consiliului UE"` is forward-looking and relevant. Add `"aderare deplina Schengen"` to differentiate from the partial air/sea Schengen accession.
- **Domain 5 (Domestic):** Strong. Add `"anulare alegeri"` (election annulment — the 2024 crisis remains a defining political event). Add `"Georgescu"` (Calin Georgescu — the pro-Russian candidate whose election was annulled). `"dezinformare"` correctly captures the hybrid threat dimension. Add `"coalitie PSD PNL"` for governing coalition tracking.

**Stale/problematic terms:** None are stale. `"referendum"` has low current relevance but remains a valid search term. `"suveranismul"` is increasingly relevant given post-election-annulment nationalist discourse.

**Suggested topic query patterns:**

1. `CSAT decizie aparare Marea Neagra` — CSAT defense decisions on Black Sea posture
2. `Neptun Deep gaze productie Romania` — Black Sea gas production / energy sovereignty
3. `Nicusor Dan NATO summit aliniere` — Presidential NATO/diplomatic alignment signals
4. `coalitie PSD PNL buget aparare` — Coalition dynamics on defense budget
5. `dezinformare Rusia Romania alegeri` — Russian hybrid interference / election security

---

## GOGGLE FILE

```goggle
! name: MPM Romania
! description: MPM pipeline source prioritization for Romania — boosts high-signal sources, discards noise
! public: false
! author: MPM Pipeline

! --- Tier 1: Essential (boost=3) ---
$boost=3,site=g4media.ro
$boost=3,site=digi24.ro
$boost=3,site=agerpres.ro
$boost=3,site=zf.ro

! --- Tier 2: Important (boost=2) ---
$boost=2,site=hotnews.ro
$boost=2,site=recorder.ro
$boost=2,site=riseproject.ro
$boost=2,site=presidency.ro
$boost=2,site=mapn.ro
$boost=2,site=mae.ro
$boost=2,site=newstrategycenter.ro
$boost=2,site=romania-insider.com

! --- Tier 3: Supplementary (boost=1) ---
$boost=1,site=pressone.ro
$boost=1,site=profit.ro
$boost=1,site=euronews.com
$boost=1,site=cdep.ro
$boost=1,site=senat.ro
$boost=1,site=expertforum.ro

! --- Discard: Noise ---
$discard,site=romaniatv.net
$discard,site=realitatea.net
$discard,site=b1tv.ro
```

---

## INTERPRETIVE CONTEXT FOR DOSSIER

### Tier 1 Sources

> Articles from **G4Media** about any domain should be interpreted as Romania's most independent and credible political reporting — its reader-funded model and veteran journalist founders give it editorial independence from the oligarch-owned media ecosystem, and it is the outlet Romania's politically literate class reads first. Its anti-corruption orientation means it frames government actions through a transparency lens, which is editorially valuable but may emphasize institutional failures over policy achievements.

> Articles from **Digi24** about domestic politics and foreign policy should be interpreted as reflecting Romania's mainstream consensus because its "Least Biased" rating and largest online audience make it the barometer of centrist discourse — its coverage reflects what the median politically engaged Romanian considers important. Owned by RCS&RDS (Zoltan Teszari), whose business interests in telecoms are generally orthogonal to editorial content, though monitor for any coverage of telecoms regulation.

> Articles from **AGERPRES** about any domain should be interpreted as official government communications, not journalism — AGERPRES publishes government-released positions verbatim, making it a primary source rather than an analytical one. The timing and framing of AGERPRES dispatches are themselves signals: what the government chooses to announce, when, and in what language reveals posture intent. Delay between Romanian and English publication may be analytically significant.

> Articles from **Ziarul Financiar** about economic policy should be interpreted as reflecting the perspective of Romania's business establishment because its centre-right business orientation means it frames economic policy through an investment-climate and fiscal-discipline lens — owned by Mediafax Group (Dan Sucu), whose business interests in retail and sports may occasionally create conflicts of interest on specific corporate stories, but ZF's economic analysis is Romania's most comprehensive.

### Tier 2 Sources

> Articles from **HotNews.ro** about EU affairs and political analysis should be interpreted as credible centre-liberal reporting with strong EU affairs depth — its 2005 founding makes it Romania's digital journalism pioneer, though its 2022 acquisition by Multi Media Est has introduced ownership-transparency questions. Monitor for editorial shifts under new ownership. English-language section adds accessibility but may editorially filter which stories get translated.

> Articles from **Recorder** about political corruption and institutional dysfunction should be interpreted as high-impact investigative journalism with a pro-transparency, anti-corruption editorial mission — its video investigations are designed for maximum public impact and have repeatedly triggered parliamentary and judicial responses. Its donation-funded model ensures editorial independence, but its adversarial stance toward corrupt actors means it focuses on institutional failures rather than policy analysis.

> Articles from **RISE Project** about corruption networks, illicit finance, and procurement irregularities should be interpreted as cross-border investigative journalism with academic-level methodology — its OCCRP membership gives it international investigative capability that domestic outlets lack. Investigations may take months and focus on structural corruption rather than daily politics, making RISE Project a depth source, not a speed source.

> Articles from **presidency.ro** about defense, foreign policy, and CSAT decisions should be interpreted as official presidential communications — not journalism but primary source material. Under President Nicusor Dan (since May 2025), presidential statements carry particular weight because the Romanian president holds constitutional authority over defense and foreign policy. What the presidency chooses to publish signals strategic priorities; what it omits may be equally significant.

> Articles from **MApN** about defense procurement, NATO exercises, and military cooperation should be interpreted as official defense ministry communications — factual on events (exercise participation, procurement contracts) but will not acknowledge operational failures, readiness gaps, or politically sensitive bilateral tensions. Cross-reference with New Strategy Center analysis for interpretive context.

> Articles from **MAE** about diplomatic activity should be interpreted as the foreign ministry's chosen public position — readouts of bilateral meetings and multilateral statements reflect what Romania wants external audiences to see, which may differ from actual negotiating positions. The timing of MAE readouts relative to counterpart ministry readouts can reveal asymmetries in bilateral relationships.

> Articles from **New Strategy Center** about NATO Eastern Flank posture, Black Sea security, and hybrid threats should be interpreted as reflecting elite security-establishment thinking in Romania — the think tank's pro-Euro-Atlantic orientation and security focus mean its analysis anticipates or reflects the strategic consensus within Romania's defense and intelligence community. Not a neutral academic voice, but an essential window into how Romania's security establishment frames threats and policy options.

> Articles from **Romania Insider** about any domain should be interpreted as an editorial curation layer, not original reporting — its selection of which Romanian-language stories to translate and summarize for English-speaking audiences reflects what the expat, diplomatic, and business community considers important. Useful as a signal detector but always verify against the original Romanian-language source for nuance lost in translation and editorial selection.

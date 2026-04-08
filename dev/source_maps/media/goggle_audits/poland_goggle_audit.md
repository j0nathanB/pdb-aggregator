# AUDIT SUMMARY: POLAND

**Sources assessed:** 17 recommended + 5 excluded + 4 newly identified = 26 total
**Tier 1 (boost=3):** 4 sources
**Tier 2 (boost=2):** 8 sources
**Tier 3 (boost=1):** 5 sources
**Neutral (no rule):** 6 sources
**Discard:** 3 sources
**Overall assessment:** The curation prompt produced a strong whitelist with excellent think tank depth (PISM, OSW) and unusually good polarisation coverage across the liberal-conservative axis. Key changes: (1) resolved redundancy between liberal broadsheets by differentiating Rzeczpospolita (paper of record, Tier 1) from Gazeta Wyborcza (liberal-investigative, Tier 2); (2) promoted government official sources (gov.pl, prezydent.pl, sejm.gov.pl) for Layer 2 migration at Tier 2; (3) added missing wire service PAP to Tier 1 per its structural role as factual baseline; (4) boosted non-English domestic sources at premium per principles — Poland's political discourse operates overwhelmingly in Polish; (5) flagged `onet.pl` as blocked by Anthropic's crawler, demoting it to Neutral despite high domestic reach. Conservative media ecosystem (Fratria group, Republika) retained at Tier 2/3 for opposition-constraint signal despite lower journalistic quality — structural role outweighs quality.

---

## BOOST ASSIGNMENTS

### Tier 1 — `$boost=3`

**Polska Agencja Prasowa (PAP)** | `pap.pl` | Type: `wire_service` | Status: `EXISTING`
- **Structural role:** Poland's national wire service — the factual baseline against which all editorial framing is measured. Lowest-latency source for official government statements, parliamentary votes, and diplomatic communiques.
- **Domain coverage:** All five domains
- **Reasoning:** PAP occupies the unique structural position of factual-first, lowest-latency government action reporting. Every other Polish outlet cites PAP; the pipeline needs PAP surfacing first to establish the factual baseline before editorial outlets frame events. Polish + English feeds, free, RSS available. Non-English domestic premium applies — PAP's Polish-language feed captures nuances lost in English summaries.
- **Extraction note:** Free; English feed at pap.pl/en covers major items. Full extraction expected.

**Rzeczpospolita** | `rp.pl` | Type: `paper_of_record` | Status: `EXISTING`
- **Structural role:** Poland's newspaper of record for legal, economic, and regulatory affairs. The outlet Poland's policy class reads for EU law transposition, trade policy, and constitutional questions.
- **Domain coverage:** Economic & technological statecraft, Institutional engagement, Domestic constraints
- **Reasoning:** Rzeczpospolita is Poland's closest equivalent to a single indispensable broadsheet. Centre-right, business-oriented, editorially independent — it occupies the institutional-trust position that makes it the first source policy elites consult. Metered paywall (~5 free articles/month) limits extraction but Brave indexes headlines. Non-English domestic premium: operates in Polish, which is where the granular regulatory and legal coverage lives.
- **Extraction note:** Metered paywall. Diffbot extraction likely partial. Headlines still discoverable via Brave.

**Defence24** | `defence24.pl` | Type: `security_defense` | Status: `EXISTING`
- **Structural role:** Poland's largest specialist defence portal. The sole dedicated source for procurement decisions, force posture changes, NATO interoperability, and defence-industrial partnerships — all critical for a country spending 4%+ of GDP on defence.
- **Domain coverage:** Security & defence autonomy (primary), Diplomatic alignment (NATO/bilateral)
- **Reasoning:** In a country executing a $48B+ defence procurement programme, a dedicated defence portal at Tier 1 is structurally essential. No other source on the list covers MON policy, arms procurement pipelines, or NATO eastern flank posture at this depth. Bilingual (Polish + English at defence24.com), free, daily newsletter. Poland's defence posture is the single most consequential domain for MPM's shield-tier classification — Defence24 is the primary sensor for it.
- **Extraction note:** Free. English edition covers major items. Full extraction expected.

**TVN24** | `tvn24.pl` | Type: `broadcast_portal` | Status: `EXISTING`
- **Structural role:** Highest-credibility liberal broadcast outlet. Extensive coverage of EU affairs, NATO summits, and government coalition dynamics. Early signal source for intra-coalition tensions.
- **Domain coverage:** Diplomatic alignment, Domestic constraints, Institutional engagement
- **Reasoning:** TVN24 is the liberal-establishment broadcast outlet — pro-EU, broadly sympathetic to Civic Platform coalition, but with genuine journalistic depth on EU institutional coverage and NATO summits. Its structural role as the broadcast-first signal source for coalition dynamics and EU positioning earns Tier 1. Warner Bros. Discovery ownership provides financial independence from Polish political actors. Free online, no hard paywall. Non-English domestic premium: Polish-language broadcast coverage captures coalition dynamics invisible in English-language reporting.
- **Extraction note:** Free online; some video content behind player but text articles extractable.

---

### Tier 2 — `$boost=2`

**PISM (Polish Institute of International Affairs)** | `pism.pl` | Type: `think_tank` | Status: `EXISTING`
- **Structural role:** Poland's premier foreign-policy think tank. Government-affiliated but analytically independent. Bulletins and Strategic Files provide early indicators of diplomatic recalibration.
- **Domain coverage:** Diplomatic alignment (primary), Institutional engagement, Security & defence
- **Reasoning:** Think tanks earn boost through depth, not speed. PISM publishes the structural foreign-policy analysis the pipeline needs to interpret daily events — EU voting pattern shifts, bilateral recalibrations, multilateral positioning. Its annual Yearbook of Polish Foreign Policy is the definitive retrospective source. Bilingual (Polish + English). Not Tier 1 because think tanks don't break news and publication cadence is slower than dailies.
- **Extraction note:** Free; publications in English and Polish at pism.pl/publications. Full extraction expected.

**OSW (Centre for Eastern Studies)** | `osw.waw.pl` | Type: `think_tank` | Status: `EXISTING`
- **Structural role:** Government-funded analytical centre with 50+ research fellows. Indispensable for understanding the threat assessments that drive Polish security posture — Russia, Ukraine, Germany, Baltics, China.
- **Domain coverage:** Diplomatic alignment, Security & defence autonomy (Eastern neighbourhood focus)
- **Reasoning:** OSW's analytical output is the intellectual infrastructure behind Poland's eastern policy. Several hundred analyses per year on Poland's strategic environment. Hawkish on Russia by institutional mandate, which is itself a signal of the policy-elite consensus that shapes Poland's security posture. Bilingual. Not Tier 1 because it provides analytical depth rather than breaking-news speed — but within its niche (Eastern neighbourhood threat assessment), nothing else on the list competes.
- **Extraction note:** Free; all major publications available in English. Full extraction expected.

**Gazeta Wyborcza** | `wyborcza.pl` | Type: `paper_of_record` | Status: `EXISTING`
- **Structural role:** Poland's largest-circulation quality daily. Liberal-establishment voice with strong investigative reporting on government-military relations, intelligence affairs, and civil liberties.
- **Domain coverage:** Diplomatic alignment, Domestic constraints, Institutional engagement
- **Reasoning:** Gazeta Wyborcza is structurally important as the liberal-intelligentsia broadsheet, but it drops to Tier 2 because its editorial space overlaps significantly with TVN24 (same liberal-pro-EU segment) and its investigative niche partially overlaps with OKO.press. Its editorial line — centre-left, pro-EU, pro-rule-of-law — is itself a signal of liberal-establishment posture. Paywall limits extraction. Non-English domestic premium still applies.
- **Extraction note:** Intelligent/metered paywall. Partial extraction likely. Some articles syndicated in English via Worldcrunch.

**Dziennik Gazeta Prawna (DGP)** | `gazetaprawna.pl` | Type: `business_financial` | Status: `EXISTING`
- **Structural role:** Poland's primary business/legal daily. The granular data layer beneath strategic economic decisions — EU regulation transposition, trade policy, energy policy, public procurement.
- **Domain coverage:** Economic & technological statecraft (primary), Institutional engagement (EU regulatory)
- **Reasoning:** DGP fills the specialized business/legal niche that generalist broadsheets cover only at surface level. For a country navigating nuclear power programme decisions, coal transition, gas diversification, and massive EU recovery fund disbursement (KPO), this granular economic coverage is essential. Not Tier 1 because its domain coverage is narrower (primarily economic statecraft) and it doesn't break political stories.
- **Extraction note:** Partial paywall. Extraction may be limited for premium content.

**Notes from Poland** | `notesfrompoland.com` | Type: `english_language_specialist` | Status: `EXISTING`
- **Structural role:** Best single English-language source for Polish current affairs. Independent, non-profit, no paywall. Covers politics, defence, EU relations, judiciary, and society.
- **Domain coverage:** All five domains (curated English-language coverage)
- **Reasoning:** For a pipeline that processes English-language text, Notes from Poland provides essential accessibility without the signal loss of machine translation. Its centrist, editorially independent positioning and Cambridge academic founding give it credibility. Covers all five domains through careful curation of Polish-language developments. Not Tier 1 because it's a secondary English-language lens rather than a primary Polish-language source — but at Tier 2, it ensures the pipeline always has high-quality English text for events that may be hard to extract from paywalled Polish sources.
- **Extraction note:** Free; no paywall; reader-funded. Full extraction expected.

**Fratria Media Group (Do Rzeczy / wPolityce.pl / wPolsce24)** | `dorzeczy.pl` / `wpolityce.pl` / `wpolsce24.pl` | Type: `opposition_aligned` / `conservative_ecosystem` | Status: `EXISTING`
- **Structural role:** Conservative media ecosystem functioning as a single editorial voice. Essential for monitoring opposition framing of foreign/security policy and early warning of nationalist pushback on EU integration.
- **Domain coverage:** Domestic constraints, Diplomatic alignment (from opposition perspective)
- **Reasoning:** Structural role outweighs quality. The pipeline needs to see what the PiS-sympathetic, Eurosceptic segment is being told about NATO commitments, EU negotiations, and bilateral concessions. This trio functions as the primary opposition-aligned media ecosystem — excluding it would create a structural blind spot on ~30-35% of the electorate's information environment. Three domains boosted as a unit. Not Tier 1 because the signal is oppositional framing rather than first-mover factual reporting.
- **Extraction note:** Free online. wPolsce24 broadcast licence under legal dispute. Full text extraction expected for web portals.

**gov.pl / prezydent.pl / sejm.gov.pl** | Type: `government_official` | Status: `NEW` — **LAYER 2 MIGRATION**
- **Structural role:** Central government web portal, Presidential office, and Sejm (parliament) portal. Houses official statements, legislative records, MON bulletins, MFA communiques, and presidential decrees.
- **Domain coverage:** All five domains (official source)
- **Reasoning:** Primary fetch via Layer 2 direct polling. Goggle boost at Tier 2 as belt-and-suspenders fallback. Government press releases occasionally surface in Brave News Search. Per pl.yaml, gov.pl and prezydent.pl are already configured as government sources at Tier 1 — the Goggle audit aligns these to Tier 2 boost because Layer 2 handles the primary fetch, and Goggle boost serves as fallback only.
- **Extraction note:** Free. Official government websites. Full extraction expected.

**RMF24** | `rmf24.pl` | Type: `broadcast_portal` | Status: `EXISTING`
- **Structural role:** Poland's most-quoted media outlet (radio) with a top-5 web news portal. Centrist/mainstream commercial positioning provides a useful benchmark against polarised outlets.
- **Domain coverage:** Domestic constraints, Diplomatic alignment
- **Reasoning:** RMF FM's position as Poland's most-quoted media outlet and RMF24's top-5 web ranking make it structurally significant as a centrist benchmark. Its commercial ownership (Bauer Media + Grupa RMF) insulates it from political pressure. Not Tier 1 because its editorial depth is lower than Rzeczpospolita or TVN24, but its centrist positioning earns Tier 2 as a calibration source.
- **Extraction note:** Free. Full extraction expected.

---

### Tier 3 — `$boost=1`

**Polityka** | `polityka.pl` | Type: `political_specialist` / `weekly_magazine` | Status: `EXISTING`
- **Structural role:** Poland's most influential weekly. Long-form analysis of coalition politics, public opinion trends, and domestic debates shaping Poland's external room for manoeuvre.
- **Domain coverage:** Domestic constraints (primary), Diplomatic alignment
- **Reasoning:** Polityka provides the structural depth on domestic political dynamics that dailies can't — coalition stability analysis, public opinion trend pieces, historical-policy debates. Centre-left, employee-owned cooperative. Tier 3 rather than Tier 2 because weekly publication cadence limits pipeline utility for daily monitoring, and its liberal-intelligentsia niche overlaps with Gazeta Wyborcza (Tier 2). But when it publishes, the analysis quality justifies boost.
- **Extraction note:** Paywall for most content. Extraction may be limited.

**OKO.press** | `oko.press` | Type: `investigative` / `fact_checking` | Status: `EXISTING`
- **Structural role:** Award-winning non-profit fact-checking and investigative journalism. Tracks rule-of-law indicators, judicial independence, and civil liberties metrics.
- **Domain coverage:** Domestic constraints (primary), Institutional engagement (rule of law)
- **Reasoning:** Unique fact-checking capability that no other Polish source replicates. Reader-funded (70% of revenue), which insulates editorial independence. Its rule-of-law tracking is directly relevant for Poland's EU institutional credibility — a key variable in the institutional engagement domain. Tier 3 rather than Tier 2 because domain coverage is narrow (primarily domestic constraints / rule of law) and publication frequency is lower than dailies.
- **Extraction note:** Free. Full extraction expected.

**Republika TV** | `republikatv.pl` | Type: `opposition_aligned` / `conservative_broadcast` | Status: `EXISTING`
- **Structural role:** Top-rated news channel by 2025. Right-populist, strongly pro-PiS. Its narratives set the agenda for approximately 30-35% of the electorate.
- **Domain coverage:** Domestic constraints
- **Reasoning:** Structural role outweighs quality — Republika's rise to top-rated news channel makes it a primary signal source for what the conservative base is being told. Tier 3 rather than Tier 2 because its domain coverage is narrow (primarily domestic constraints), its high polarisation index (56%) means its framing requires heavy discounting, and the Fratria group at Tier 2 already captures the conservative opposition signal. Republika provides redundant conservative-opposition coverage but from the broadcast side.
- **Extraction note:** Free livestream; broadcast licence under legal challenge. Web text extraction expected.

**New Eastern Europe** | `neweasterneurope.eu` | Type: `analytical_magazine` | Status: `EXISTING`
- **Structural role:** English-language bimonthly providing analytical depth on Poland's regional positioning vis-a-vis Visegrad, Three Seas, and Eastern Partnership.
- **Domain coverage:** Diplomatic alignment, Institutional engagement (Central/Eastern European regional lens)
- **Reasoning:** Fills a specific analytical niche — Poland's role as a regional agenda-setter in Central/Eastern Europe. Bimonthly cadence limits daily pipeline utility, but its regional comparative framing is unique on the list. English-language, which aids pipeline extraction. Tier 3 rather than Tier 2 because of low publication frequency and narrow regional focus.
- **Extraction note:** Partial free access online; subscription for full archive. Extraction may be limited.

**Polsat News** | `polsatnews.pl` | Type: `broadcast_portal` | Status: `EXISTING`
- **Structural role:** Second-largest private broadcaster. Centrist/commercial with low polarisation score (19%). Provides commercially-motivated centrism useful as a baseline.
- **Domain coverage:** Domestic constraints, Diplomatic alignment
- **Reasoning:** Polsat News earns Tier 3 as a supplementary centrist broadcast source. Its low polarisation index makes it a useful baseline, but its editorial depth and original reporting rate are lower than TVN24 (Tier 1) and RMF24 (Tier 2). Redundancy with those two higher-tier centrist-to-liberal broadcast sources limits it to Tier 3.
- **Extraction note:** Free online. Full extraction expected.

---

### Neutral — no Goggle rule

**Onet** | `onet.pl` | Type: `web_portal` | Status: `EXISTING → DEMOTED TO NEUTRAL`
- **Why neutral:** Despite being Poland's highest-reach digital news outlet (42% weekly reach), `onet.pl` is **blocked by Anthropic's crawler** (`robots.txt` denial in blocked_domains.md). Even if Brave surfaces Onet results, the pipeline cannot extract full text. Its editorial selection and investigative reporting are strong, but extraction failure makes boosting counterproductive — boosted results that can't be read waste result slots. Under the Goggle model, it can still appear organically and provide headlines. If crawler access is restored, re-evaluate at Tier 2.

**TVP (Telewizja Polska)** | `tvp.pl` | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Curation exclusion was correct — TVP has been in institutional upheaval since the 2023 government transition (liquidation and reconstitution). Its editorial line tracks whoever controls the institution, making it unreliable as a consistent signal source. Under the Goggle model, no reason to actively discard — if TVP stabilises under new management and breaks a story, Brave may surface it organically. Exclusions default to Neutral, not Discard.

**Wprost** | `wprost.pl` | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Curation exclusion was correct — digital-only since 2020, reduced influence, editorial niche captured by Rzeczpospolita + Do Rzeczy combination. Under the Goggle model, organic ranking is appropriate. No reason to discard.

**Newsweek Polska** | `newsweek.pl` | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Liberal weekly whose editorial space overlaps substantially with Polityka and Gazeta Wyborcza. Curation exclusion was correct for minimum-set design. Under Goggle model, leave at organic ranking — may surface for specific queries where its coverage adds incremental value.

**Interia.pl** | `interia.pl` | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Major web portal (Polsat group) that largely aggregates from sources already in the set. Original editorial output thinner than Onet's. Under Goggle model, organic ranking is fine — its aggregation function means it may surface wire copy or syndicated content serendipitously.

**Fakt / Super Express** | `fakt.pl` / `se.pl` | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Poland's two major tabloids. Coverage is overwhelmingly domestic crime, celebrity, and human-interest. Rarely cover foreign policy or defence at pipeline-relevant depth. No reason to actively discard — organic ranking handles these correctly without boosting.

---

### Discard — `$discard`

**niezalezna.pl** | Status: `NEW DISCARD`
- **Discard reasoning:** Partisan commentary portal associated with the Solidarity trade union's right wing. No original reporting, primarily opinion pieces and wire rewrites with strong ideological framing. Would actively displace higher-signal sources from top results without adding factual content. The conservative-opposition signal is already well-captured by Fratria group (Tier 2) and Republika (Tier 3).

**pch24.pl** | Status: `NEW DISCARD`
- **Discard reasoning:** Ultra-conservative Catholic media portal (Polonia Christiana). Mixes religious commentary with political opinion in ways that produce unreliable framing for strategic-posture analysis. No original investigative or policy reporting. Would inject ideological noise without adding signal.

**Sputnik Polska (archived mirrors)** | Status: `NEW DISCARD`
- **Discard reasoning:** Russian state media (banned in EU since 2022 but archived mirrors and social media excerpts persist). Active disinformation vector. Any content surfacing from Sputnik-associated domains should be actively suppressed to prevent contamination of the pipeline's factual baseline.

---

## STRUCTURAL COVERAGE CHECK

| Structural Role | Source(s) | Tier | Notes |
|---|---|---|---|
| Government leak channel / signal | PAP, gov.pl | T1, T2 | PAP tracks governing coalition priorities; gov.pl for official statements. Layer 2 migration handles direct polling. No single "government-aligned daily" equivalent to Mexico's La Jornada — Poland's government signals through PAP wire dispatches and official portals |
| Opposition voice | Fratria group (Do Rzeczy / wPolityce / wPolsce24), Republika TV | T2, T3 | Conservative-opposition ecosystem well-covered. PiS-sympathetic framing captured by two independent outlets. Latinus-equivalent adversarial journalism less developed in Poland |
| Defence/security first-mover | Defence24 | T1 | Unlike Mexico, Poland has a dedicated defence portal — Defence24 is the primary sensor for procurement, force posture, and NATO interoperability. Critical given Poland's $48B+ defence programme and 4%+ GDP spending |
| Policy-elite discourse | PISM, OSW, Rzeczpospolita | T2, T2, T1 | Exceptionally strong think tank coverage. PISM for foreign policy, OSW for eastern neighbourhood threat assessment, Rzeczpospolita for what decision-makers read daily |
| Domestic-language depth | All Polish-language sources (14 of 17 boosted) | T1-T3 | Poland's political discourse operates overwhelmingly in Polish. English sources (Notes from Poland, New Eastern Europe, Defence24 English) are supplements. Non-English domestic premium applied throughout |
| Official government source | gov.pl, prezydent.pl, sejm.gov.pl | T2 | **LAYER 2 MIGRATION** — primary fetch via direct polling. Goggle boost as fallback. Covers MON bulletins, MFA communiques, presidential decrees, legislative records |
| Analytical/think tank depth | PISM, OSW, New Eastern Europe | T2, T2, T3 | PISM for foreign policy; OSW for security/eastern neighbourhood; New Eastern Europe for regional positioning. Think tanks provide depth not speed |
| Wire service (factual baseline) | PAP (domestic), Reuters, AP News | T1, Neutral, Neutral | PAP uniquely boosted to Tier 1 as domestic wire with unmatched latency. International wires left at organic ranking — Reuters is blocked by Anthropic's crawler but Brave can still discover it for headline-level signal |
| Centrist benchmark | RMF24, Polsat News | T2, T3 | Centrist commercial outlets provide a polarisation baseline against which liberal (TVN24) and conservative (Republika) framing can be measured |
| Rule of law / institutional health | OKO.press, Gazeta Wyborcza | T3, T2 | OKO.press for fact-checking and rule-of-law indicators; Gazeta Wyborcza for investigative depth on civil liberties and judicial independence |
| English-language access layer | Notes from Poland, Defence24 (English), New Eastern Europe | T2, T1, T3 | Pipeline accessibility without Polish-language dependence. Notes from Poland is the single best English-language source for Polish current affairs |

**Gaps identified:**
1. **Defence procurement pipeline detail** remains a structural blind spot — Defence24 covers announcements and analysis but the granular delivery schedules, contract modifications, and industrial offset arrangements of Poland's massive acquisition programme are poorly tracked. Mitigated by Layer 2 polling of MON.gov.pl and supplemented by Defence24, but full procurement pipeline visibility requires specialist databases (Jane's Defence, SIPRI) outside the Goggle scope.
2. **Energy-sector specialist source** is missing — Poland's nuclear programme (Westinghouse deal), gas diversification (Baltic Pipe, LNG terminal expansion), and coal transition are major drivers of economic statecraft but covered across multiple generalist outlets rather than a single trackable specialist feed. DGP (Tier 2) provides the best granular coverage but is not energy-specialist.
3. **Regional/local media** from border voivodeships (Podkarpackie, Podlaskie, Lubuskie) could provide early signals of cross-border tensions or migration-related domestic pressure, particularly relevant for Poland's role as a frontline state. Excluded to maintain source ceiling.
4. **Polish-language social media and Telegram channels** increasingly drive the conservative information ecosystem and can surface opposition narratives faster than formal outlets. Outside Goggle scope but noted as a coverage gap.

---

## REDUNDANCY RESOLUTION

**Liberal broadsheet cluster: Rzeczpospolita + Gazeta Wyborcza + TVN24**
All three serve the liberal-to-centrist segment of Poland's media. Resolved by differentiating structural roles: Rzeczpospolita (Tier 1, paper of record, business/legal/regulatory depth), TVN24 (Tier 1, broadcast-first coalition dynamics and EU coverage), Gazeta Wyborcza (Tier 2, investigative depth on civil liberties and intelligence affairs). Gazeta Wyborcza drops below the other two because its editorial space overlaps with both TVN24 (pro-EU liberal framing) and OKO.press (rule-of-law investigations).

**Conservative opposition cluster: Fratria group + Republika TV**
Both serve the PiS-sympathetic conservative segment. Resolved by treating the Fratria group (Do Rzeczy + wPolityce + wPolsce24) as the primary conservative-opposition sensor at Tier 2 (three outlets, single editorial voice, broader coverage) and Republika as supplementary at Tier 3 (broadcast-side signal, narrower domain coverage, higher polarisation index). The pipeline gets conservative-opposition framing from two independent sources without over-weighting the segment.

**Think tank cluster: PISM + OSW + New Eastern Europe**
Three analytical sources could appear redundant, but each has a distinct domain: PISM (foreign policy / diplomatic alignment), OSW (eastern neighbourhood / security threat assessment), New Eastern Europe (regional positioning / Visegrad-Three Seas lens). No overlap reduction needed — each occupies a unique analytical niche.

**Centrist broadcast cluster: RMF24 + Polsat News + TVN24**
Three broadcast outlets. TVN24 leads (Tier 1) as the highest-credibility outlet with genuine editorial depth. RMF24 holds Tier 2 for its most-quoted status and centrist benchmark function. Polsat News drops to Tier 3 — its low polarisation score is useful as a baseline but its original reporting depth is the lowest of the three, creating redundancy with RMF24.

**Web portal: Onet (Neutral due to crawler block)**
Would have been Tier 2 for its 42% weekly reach and investigative team, but crawler block makes boosting counterproductive. No redundancy resolution needed — its demotion to Neutral is driven by extraction reality, not editorial overlap.

---

## QUERY CONFIGURATION

```
country: PL
search_lang: pl
freshness: pw
```

**Multi-language notes:** Poland's media ecosystem operates overwhelmingly in Polish. English-language sources (Notes from Poland, Defence24 English, New Eastern Europe, PISM English publications, OSW English analyses) provide supplementary access. Queries should run primarily in Polish; a secondary English query cycle for defence and foreign-policy topics would capture English-language think tank output and Notes from Poland coverage. The pipeline's existing `languages.metadata: en` configuration handles this correctly.

**Localized query vocabulary validation:**

The curation prompt's vocabulary is solid. Notes:

- **Domain 1 (Diplomatic):** All terms valid. Add `"Tusk polityka zagraniczna"` and `"Nawrocki wizyta"` as leader-specific patterns. `"Trojmorze"` is correct and gaining relevance as Poland positions itself as Three Seas Initiative leader. Add `"szczyt NATO"` (NATO summit) and `"relacje z Niemcami"` (relations with Germany) — the Germany relationship is Poland's single most consequential bilateral dynamic.
- **Domain 2 (Security):** Strong list. Add `"Tarcza Wschod"` (Shield East — Poland's eastern border fortification programme). `"F-35 Polska"` and `"K2 czolg"` (K2 tank) for key procurement tracking. `"Wojska Obrony Terytorialnej"` is correctly included — WOT is a key indicator of territorial defence posture. Add `"Agencja Uzbrojenia"` (Armament Agency — central procurement body).
- **Domain 3 (Economic):** Excellent. Add `"elektrownia jadrowa Westinghouse"` and `"Baltic Pipe"` for energy-sector tracking. `"KPO srodki"` (National Recovery Plan funds) — disbursement tracking is a key EU institutional engagement indicator. Add `"CPK"` (Centralny Port Komunikacyjny — Central Communication Hub mega-project).
- **Domain 4 (Institutional):** Valid. `"praworzadnosc"` (rule of law) is essential. Add `"KRS reforma"` (National Council of the Judiciary reform) and `"Bodnar"` (Justice Minister Adam Bodnar, architect of judicial reform). `"artykul siodmy"` is correct but declining — Article 7 procedure is being wound down as Poland returns to EU institutional compliance. Add `"kamienie milowe KPO"` (KPO milestones) for conditionality tracking.
- **Domain 5 (Domestic):** Strong. Add `"wybory prezydenckie 2025"` (presidential election — recently concluded, Nawrocki victory). `"koalicja 15 pazdziernika"` or `"koalicja rzadowa Tusk"` for governing coalition stability queries. Add `"Konfederacja sondaze"` — Confederation party polling is a key indicator of right-wing populist pressure. `"Mentzen"` as the new Confederation leader is important.

**Stale/problematic terms:** `"partnerstwo wschodnie"` (Eastern Partnership) may be declining in relevance as the EU's Eastern Partnership framework has been effectively replaced by bilateral Ukraine-EU dynamics. Still valid for Moldova/Georgia tracking but less central than pre-2022.

**Suggested topic query patterns:**

1. `Tusk NATO szczyt wydatki obronne` — Defence spending and NATO positioning under Tusk
2. `modernizacja armii F-35 K2 Agencja Uzbrojenia` — Key procurement programme tracking
3. `praworzadnosc reforma sadownictwa Bodnar KRS` — Judicial reform implementation
4. `elektrownia jadrowa Westinghouse bezpieczenstwo energetyczne` — Nuclear/energy programme
5. `Nawrocki prezydent polityka zagraniczna` — Presidential foreign policy positioning
6. `KPO kamienie milowe fundusze UE` — EU recovery fund disbursement
7. `Tarcza Wschod granica wschodnia` — Eastern border fortification programme
8. `Konfederacja Mentzen sondaze opozycja` — Right-wing populist opposition pressure

---

## GOGGLE FILE

```goggle
! name: MPM Poland
! description: MPM pipeline source prioritization for Poland — boosts high-signal sources, discards noise
! public: false
! author: MPM Pipeline

! --- Tier 1: Essential (boost=3) ---
$boost=3,site=pap.pl
$boost=3,site=rp.pl
$boost=3,site=defence24.pl
$boost=3,site=tvn24.pl

! --- Tier 2: Important (boost=2) ---
$boost=2,site=pism.pl
$boost=2,site=osw.waw.pl
$boost=2,site=wyborcza.pl
$boost=2,site=gazetaprawna.pl
$boost=2,site=notesfrompoland.com
$boost=2,site=dorzeczy.pl
$boost=2,site=wpolityce.pl
$boost=2,site=wpolsce24.pl
$boost=2,site=gov.pl
$boost=2,site=prezydent.pl
$boost=2,site=sejm.gov.pl
$boost=2,site=rmf24.pl

! --- Tier 3: Supplementary (boost=1) ---
$boost=1,site=polityka.pl
$boost=1,site=oko.press
$boost=1,site=republikatv.pl
$boost=1,site=neweasterneurope.eu
$boost=1,site=polsatnews.pl

! --- Discard: Noise ---
$discard,site=niezalezna.pl
$discard,site=pch24.pl
$discard,site=sputnik.pl
```

---

## INTERPRETIVE CONTEXT FOR DOSSIER

### Tier 1 Sources

> Articles from **PAP (Polska Agencja Prasowa)** about any domain should be interpreted as the factual baseline — PAP is Poland's national wire service and its reporting reflects official government positions with minimal editorial framing. Its editorial line tracks governing coalition priorities, so what PAP emphasises (and what it omits) is itself a signal of government communication strategy. Treat PAP reporting as the factual starting point against which all other outlets' framing should be measured.

> Articles from **Rzeczpospolita** about economic policy, EU regulation, or constitutional matters should be interpreted as reflecting Poland's business-establishment perspective — its centre-right, editorially independent positioning means it frames EU regulatory compliance, trade policy, and fiscal decisions through a market-efficiency and rule-of-law lens. Negative coverage of government economic interventionism reflects business-class concerns, not necessarily policy failure.

> Articles from **Defence24** about procurement, force posture, or NATO interoperability should be interpreted as pro-defence-establishment reporting with genuine analytical depth — it is not party-aligned but its institutional orientation favours strong defence spending and close NATO integration. Critical coverage of procurement delays or capability gaps reflects real military-industrial concerns, not political opposition. Defence24 is the single most reliable source for understanding what Poland's defence establishment actually thinks.

> Articles from **TVN24** about EU affairs, NATO summits, or coalition politics should be interpreted as filtered through a liberal, pro-EU editorial lens — its Warner Bros. Discovery ownership and Civic Platform-sympathetic positioning mean it frames European integration positively and government coalition instability as newsworthy. TVN24's coverage of opposition (PiS) activities tends toward critical framing, which should be calibrated against conservative sources (Fratria group, Republika) for balance.

### Tier 2 Sources

> Articles from **PISM** about foreign policy and diplomatic positioning should be interpreted as reflecting the mainstream Polish foreign-policy consensus — state-funded but analytically independent, PISM's analysis represents what Poland's diplomatic establishment considers important. Its framing of bilateral relationships and multilateral positioning maps closely to the government's own strategic thinking, making it an indicator of diplomatic intent.

> Articles from **OSW** about Russia, Ukraine, or Eastern neighbourhood security should be interpreted as the analytical foundation of Poland's eastern policy — hawkish on Russia by institutional mandate, OSW's threat assessments directly influence the security-policy debates that shape defence spending and NATO positioning. Its framing of Russian actions as threatening reflects genuine analytical conviction, not political bias, but analysts should note that OSW's institutional perspective may over-weight eastern threats relative to other strategic challenges.

> Articles from **Gazeta Wyborcza** about civil liberties, judicial independence, or intelligence affairs should be interpreted as liberal-establishment investigative journalism — its centre-left, pro-EU, pro-rule-of-law orientation means it frames government failures on democratic standards as particularly newsworthy. Founded by Adam Michnik, its institutional identity is bound to Poland's democratic transition, making it especially sensitive to rule-of-law backsliding signals.

> Articles from **Dziennik Gazeta Prawna** about EU regulation transposition, energy policy, or public procurement should be interpreted as professional, non-partisan business reporting — its business/legal focus means it provides granular policy detail that generalist outlets miss, particularly on the technical dimensions of EU compliance, trade agreements, and industrial policy.

> Articles from **Notes from Poland** about any domain should be interpreted as carefully curated English-language coverage with centrist editorial positioning — its academic founding (Cambridge) and non-profit structure give it editorial independence, but analysts should note that its curation reflects what an English-speaking audience needs to know about Poland, which may differ from what is most salient in Polish-language domestic discourse.

> Articles from **Fratria group (Do Rzeczy / wPolityce / wPolsce24)** about EU integration, NATO commitments, or bilateral concessions should be interpreted as PiS-sympathetic opposition framing — their national-conservative, Eurosceptic-leaning editorial line means they frame EU conditionality as sovereignty infringement and government foreign-policy concessions as weakness. This framing is essential for understanding the domestic constraint environment that limits Poland's room for manoeuvre on EU integration and bilateral negotiations. What Fratria outlets oppose is a signal of the political cost of policy choices.

> Articles from **gov.pl / prezydent.pl / sejm.gov.pl** should be interpreted as official government communications — not journalism but primary source material. Press releases, legislative records, and presidential statements represent the state's chosen public position, which may differ from actual policy implementation or internal deliberation.

> Articles from **RMF24** about domestic politics or foreign affairs should be interpreted as centrist/mainstream commercial coverage — its consistent trust rankings among Polish audiences and commercial ownership (Bauer Media) make it a useful polarisation baseline. Where RMF24's framing diverges from TVN24 (liberal) or Republika (conservative), the divergence itself is a signal of how politically charged an issue has become.

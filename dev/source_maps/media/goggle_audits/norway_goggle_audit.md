# AUDIT SUMMARY: NORWAY

**Sources assessed:** 18 recommended + 5 excluded + 4 newly identified = 27 total
**Tier 1 (boost=3):** 4 sources
**Tier 2 (boost=2):** 9 sources
**Tier 3 (boost=1):** 6 sources
**Neutral (no rule):** 5 sources
**Discard:** 3 sources
**Overall assessment:** The curation prompt produced a strong whitelist with excellent defense/security coverage — unusual depth for a small-state map, reflecting Norway's strategic position on NATO's northern flank. Key changes: (1) promoted Norwegian-language domestic sources with boost premium over English-language alternatives; (2) migrated government sources (regjeringen.no, stortinget.no) to Tier 2 for Layer 2 migration; (3) resolved redundancy in the broadsheet/tabloid cluster by differentiating editorial roles; (4) added missing think tank (FFI) and wire service coverage; (5) no Norwegian domains appear on the blocked domains list — all sources are extractable by Anthropic's crawler.

---

## BOOST ASSIGNMENTS

### Tier 1 — `$boost=3`

**NRK** | `nrk.no` | Type: `paper_of_record` | Status: `EXISTING`
- **Structural role:** Norway's public broadcaster and default agenda-setter for the entire Norwegian political discourse. Highest-trust news brand in the country. Free, no paywall — maximum extraction reliability.
- **Domain coverage:** Diplomatic alignment, Security & defense, Domestic constraints, Institutional engagement
- **Reasoning:** NRK is the single indispensable source for Norway. It sets the national agenda, broadcasts Storting debates live, runs the investigative unit Brennpunkt, and has the deepest foreign-affairs desk in Norwegian media. Free access means perfect extraction. Norwegian-language primary content earns the non-English domestic boost premium. No other source has this breadth and reliability combined.
- **Extraction note:** Free; RSS feeds available. English articles sparse but exist.

**Aftenposten** | `aftenposten.no` | Type: `paper_of_record` | Status: `EXISTING`
- **Structural role:** Norway's newspaper of record for foreign-policy and institutional coverage. Editorials are the primary signal of establishment-right thinking on NATO, EU/EEA relations, and transatlantic alignment.
- **Domain coverage:** Diplomatic alignment, Institutional engagement, Domestic constraints
- **Reasoning:** Aftenposten is where Norwegian policy elites — particularly on the centre-right — publish and read. Its editorial page is the closest thing to an establishment consensus barometer on alliance questions. Schibsted paywall limits extraction, but key articles are indexed by Google/Brave. Norwegian-language boost premium applies. Alongside NRK, forms the essential duo for understanding mainstream elite discourse.
- **Extraction note:** Metered paywall (Schibsted bundle). Headline + lead extraction likely; full text partial.

**Dagens Naeringsliv (DN)** | `dn.no` | Type: `business_financial` | Status: `EXISTING`
- **Structural role:** Norway's principal financial daily and sole Tier 1 source for economic statecraft — petroleum fund (NBIM/Oljefondet) decisions, energy-sector policy, sanctions compliance, and sovereign-wealth positioning.
- **Domain coverage:** Economic & technological statecraft, Diplomatic alignment
- **Reasoning:** No other source covers the intersection of Norway's energy wealth and its foreign-policy implications at this depth. GPFG investment and exclusion decisions are geopolitically significant, and DN tracks them systematically. Hard paywall limits extraction, but the pipeline needs DN surfacing first for economic queries. Norwegian-language boost premium applies.
- **Extraction note:** Hard paywall. Diffbot extraction likely partial. E24 at Tier 2 provides free-access supplement for faster-cycle economic stories.

**Klassekampen** | `klassekampen.no` | Type: `opposition_aligned` | Status: `EXISTING`
- **Structural role:** Principal voice of Norway's left flank. The primary channel for opposition to NATO cost-sharing, US basing agreements, EU integration, arms exports, and petroleum policy.
- **Domain coverage:** Domestic constraints, Diplomatic alignment, Institutional engagement
- **Reasoning:** Structural role outweighs extraction difficulty. Klassekampen's op-ed pages are the leading indicator of red-green coalition fault lines — the pipeline cannot detect domestic contestation of Norway's strategic posture without this source. In a consensus-oriented polity, the left opposition voice is structurally essential at Tier 1. Norwegian-language boost premium applies. Press-subsidy funded, which sustains its independence.
- **Extraction note:** Paywall; digital subscription. Extraction likely partial.

---

### Tier 2 — `$boost=2`

**VG** | `vg.no` | Type: `paper_of_record` | Status: `EXISTING`
- **Structural role:** Norway's highest-circulation newspaper. Rapid-cycle breaking news on defense incidents, political crises, and public opinion polling (Respons Analyse, Norstat).
- **Domain coverage:** Security & defense, Domestic constraints
- **Reasoning:** VG's speed makes it the first-mover for breaking Norwegian news. Its polling coverage is the primary gauge of domestic political constraints on government action. Tier 2 rather than Tier 1 because its tabloid format means lower analytical depth than NRK/Aftenposten, and its domain coverage is narrower (primarily security + domestic constraints). Partial paywall — breaking news free.

**Forsvarets forum** | `forsvaretsforum.no` | Type: `security_defense` | Status: `EXISTING`
- **Structural role:** Norway's dedicated defense press — the structural equivalent that many countries lack entirely. Published by the Norwegian Armed Forces with editorial independence.
- **Domain coverage:** Security & defense autonomy
- **Reasoning:** Single-domain but irreplaceable within it. Best source for tracking Norwegian military posture changes, procurement signals, exercise schedules, and NATO interoperability. English section available. Free access — perfect extraction. Tier 2 rather than Tier 1 because single-domain coverage and institutional affiliation (published by Forsvaret) introduce a structural bias toward official military perspective.

**E24** | `e24.no` | Type: `business_financial` | Status: `EXISTING`
- **Structural role:** Free-access complement to DN for business/economy coverage. Faster-cycle, digital-native. Schibsted-owned.
- **Domain coverage:** Economic & technological statecraft
- **Reasoning:** Fills the extraction gap left by DN's hard paywall. When the pipeline can't get full DN text, E24 provides the free-access economic signal. Tracks energy prices, sovereign-wealth fund moves, and corporate signals relevant to sanctions and export controls. Tier 2 rather than Tier 1 because it's less analytically deep than DN and its editorial voice is less distinctive.

**Regjeringen.no (Norwegian Government)** | `regjeringen.no` | Type: `government_aligned` | Status: `EXISTING` — **LAYER 2 MIGRATION**
- **Structural role:** Central government web portal. Publishes press releases, white papers (stortingsmeldinger), the annual foreign-policy address to the Storting, official strategies, and treaty texts. Unusually complete English-language section.
- **Domain coverage:** All five domains (official source)
- **Reasoning:** Primary fetch via Layer 2 direct polling. Goggle boost at Tier 2 as belt-and-suspenders fallback. Government official sources = Tier 2 per audit principles. The English-language section is unusually comprehensive for a mid-sized state, making official posture signals directly accessible to the pipeline. Free; RSS feeds available.

**Stortinget.no (Norwegian Parliament)** | `stortinget.no` | Type: `legislative_official` | Status: `EXISTING` — **LAYER 2 MIGRATION**
- **Structural role:** Official parliamentary record — committee hearings, voting records, written questions (skriftlige sporsmal), interpellations, Web TV of plenary sessions.
- **Domain coverage:** Institutional engagement, Domestic constraints
- **Reasoning:** Primary fetch via Layer 2 direct polling. Goggle boost at Tier 2 as fallback. Essential for tracking parliamentary constraints on executive action — defense budgets, EU/EEA legislation adoption, arms-export decisions. Government official sources = Tier 2 per audit principles.

**NUPI** | `nupi.no` | Type: `political_specialist` / `think_tank` | Status: `EXISTING`
- **Structural role:** Norway's leading foreign-policy think tank. Government-funded (Ministry of Education and Research). Publications preview policy-elite thinking and frequently feed directly into government strategy documents.
- **Domain coverage:** Diplomatic alignment, Security & defense autonomy, Institutional engagement
- **Reasoning:** Think tanks earn boost through depth, not speed. NUPI publishes the structural analysis the pipeline needs to interpret daily events — Arctic strategy, NATO posture, Nordic cooperation frameworks, and Russia-Norway dynamics. Researchers are regular media commentators, meaning NUPI analysis often prefigures mainstream coverage. Tier 2 for analytical depth. Not Tier 1 because it doesn't break news and publishes less frequently than dailies. Bilingual (Norwegian + English) — publications freely available.

**Aldrimer.no** | `aldrimer.no` | Type: `security_defense` | Status: `EXISTING`
- **Structural role:** Independent investigative defense outlet. Has broken stories on Russian military activity near Norway and gaps in defense readiness. Higher-risk, higher-reward source.
- **Domain coverage:** Security & defense autonomy, Diplomatic alignment
- **Reasoning:** Complements Forsvarets forum with an independent, investigative lens on the same domain. While Forsvarets forum provides the institutional perspective, Aldrimer.no surfaces what the defense establishment would prefer not to discuss — capability gaps, intelligence failures, and security threats. Tier 2 rather than Tier 1 because partially paywalled and narrower domain coverage.

**Morgenbladet** | `morgenbladet.no` | Type: `political_specialist` | Status: `EXISTING`
- **Structural role:** Norway's premier weekly for long-form political, cultural, and foreign-affairs analysis. Pieces by academics, former diplomats, and policy insiders preview elite-debate shifts before they appear in daily media.
- **Domain coverage:** Diplomatic alignment, Institutional engagement, Domestic constraints
- **Reasoning:** Think-tank-adjacent weekly that provides the interpretive depth the pipeline needs. Elite discourse often surfaces here before it reaches NRK or Aftenposten. Tier 2 for depth. Not Tier 1 because weekly publication cadence limits pipeline utility for time-sensitive detection, and paywall constrains extraction.

---

### Tier 3 — `$boost=1`

**High North News** | `highnorthnews.com` | Type: `regional` | Status: `EXISTING`
- **Structural role:** Dedicated Arctic/High North coverage — the government's stated top strategic priority. Tracks military activity, Svalbard governance, fisheries disputes, energy infrastructure, and Russia-Norway border dynamics.
- **Domain coverage:** Security & defense autonomy, Diplomatic alignment, Economic & technological statecraft
- **Reasoning:** Narrow geographic scope limits it to Tier 3, but within the High North niche, nothing else on the list competes at this level of systematic coverage. Full English-language edition increases pipeline accessibility. Free access — full extraction. Tier 3 rather than Tier 2 because Arctic-specific stories are a subset of Norway's strategic posture, and the major outlets (NRK, Aftenposten, Forsvarets forum) cover significant Arctic developments anyway.

**Minerva** | `minerva.no` | Type: `opposition_aligned` | Status: `EXISTING`
- **Structural role:** Primary idea-magazine of the Norwegian political right. Counterweight to Klassekampen on the ideological spectrum.
- **Domain coverage:** Domestic constraints, Diplomatic alignment
- **Reasoning:** Provides the conservative-liberal intellectual perspective on defense spending, transatlantic relations, EU accession, and market reforms. Tier 3 rather than Tier 2 because publication frequency is lower (quarterly print + online), domain coverage is narrower than Klassekampen's, and the centre-right perspective is already partially captured by Aftenposten's editorial line. Norwegian-language boost premium applies but doesn't override frequency limitations.

**Dagbladet** | `dagbladet.no` | Type: `paper_of_record` | Status: `EXISTING`
- **Structural role:** Second-largest tabloid. Progressive/social-liberal editorial lens on foreign intervention, refugee policy, and climate diplomacy.
- **Domain coverage:** Domestic constraints, Diplomatic alignment
- **Reasoning:** Complements VG with a more progressive editorial frame. Co-founder of Faktisk.no. Tier 3 rather than Tier 2 because substantial editorial overlap with VG (both tabloids, both breaking news) and the progressive voice is already well-represented by Klassekampen at Tier 1. Partial paywall — breaking news free.

**Energi og Klima** | `energiogklima.no` | Type: `political_specialist` | Status: `EXISTING`
- **Structural role:** Specialist outlet at the intersection of energy policy, climate diplomacy, and economic statecraft — central to Norway as a major petroleum/gas exporter navigating the green transition.
- **Domain coverage:** Economic & technological statecraft, Institutional engagement
- **Reasoning:** Unique coverage niche: EU regulatory alignment (EEA/Green Deal), carbon-border mechanisms, sovereign-wealth fund ESG decisions. No other source covers this intersection at equivalent depth. Tier 3 because narrow domain scope and lower publication frequency than dailies. Free access including English articles.

**Filter Nyheter** | `filternyheter.no` | Type: `investigative` | Status: `EXISTING`
- **Structural role:** Specialist investigative outlet focused on extremism, security threats, and disinformation. Unique coverage niche for hybrid-threat detection.
- **Domain coverage:** Security & defense autonomy, Domestic constraints
- **Reasoning:** Has exposed domestic extremist networks and foreign influence operations — a unique niche no other source on the list fills. Tier 3 because publication frequency is lower, domain scope is narrow, and the security beat is well-covered at higher tiers by Forsvarets forum and Aldrimer.no. Partially paywalled; receives press subsidies since 2023.

**FFI (Forsvarets forskningsinstitutt)** | `ffi.no` | Type: `think_tank` / `security_defense` | Status: `NEW`
- **Structural role:** Norwegian Defence Research Establishment. Government-funded research institute producing technical and strategic analysis on defense technology, capability planning, and threat assessments.
- **Domain coverage:** Security & defense autonomy, Economic & technological statecraft
- **Reasoning:** Added to fill the technology/cyber statecraft gap identified in the coverage assessment. FFI publications cover semiconductor policy, data sovereignty, digital infrastructure, and defense-technology dimensions that no other source systematically tracks. Complements NUPI (foreign policy focus) with a defense-technology lens. Tier 3 because publication frequency is low and content is often technical. Free; publications at ffi.no.

---

### Neutral — no Goggle rule

**Nettavisen** | `nettavisen.no` | Type: `opposition_aligned` | Status: `EXISTING → DEMOTED TO NEUTRAL`
- **Why neutral:** Captures right-populist and FrP-adjacent discourse, but the pipeline's domestic constraints coverage is already well-served by Klassekampen (left opposition, Tier 1) and Minerva (right intellectual, Tier 3). Nettavisen's populist-right signal is real but its content is high-volume, low-depth aggregation. Under the Goggle model, organic ranking is appropriate — it may surface for specific queries about FrP or immigration policy without displacing higher-signal sources. Free and extractable if it surfaces.

**Stavanger Aftenblad** | `aftenbladet.no` | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Important regional paper in the petroleum capital, but energy-sector statecraft is adequately covered by DN (Tier 1), E24 (Tier 2), and Energi og Klima (Tier 3). Under the Goggle model, no reason to actively discard — organic ranking lets it surface for Stavanger-specific energy stories without boosting. Exclusions default to Neutral not Discard.

**Bergens Tidende** | `bt.no` | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Major regional daily (Bergen) with strong local reporting on naval shipbuilding and defense industry. National-strategic coverage replicates NRK/Aftenposten. Under the Goggle model, organic ranking is appropriate — it may surface for Bergen-specific defense-industry stories. Exclusions default to Neutral not Discard.

**Faktisk.no** | `faktisk.no` | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Collaborative fact-checking service (NRK, VG, Dagbladet). Useful for verification but does not produce original strategic-posture reporting. Monitoring parent outlets captures the signal. Under the Goggle model, organic ranking lets it surface for misinformation/verification queries without displacing primary sources.

**Nordlys** | `nordlys.no` | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Tromso-based regional paper with Nordnorsk debatt forum. Arctic coverage is handled more efficiently through High North News (Tier 3). Under the Goggle model, organic ranking lets it surface for Tromso-specific stories. Exclusions default to Neutral not Discard.

---

### Discard — `$discard`

**The Local Norway** | `thelocal.no` | Status: `NEW DISCARD`
- **Discard reasoning:** English-language expatriate outlet with derivative content. Not a primary source for posture shifts — would inject rewritten wire copy and lifestyle content that displaces actual Norwegian sources from top results. Curation prompt correctly excluded it; under Goggle model, active discard is warranted because its English-language content would rank competitively with boosted sources for English-language queries, crowding out substantive English-language content from High North News, NUPI, and Forsvarets forum's English section.

**Norway Today** | `norwaytoday.info` | Status: `NEW DISCARD`
- **Discard reasoning:** Same logic as The Local Norway. English-language expatriate news aggregator with no original reporting. Would displace substantive English-language sources in pipeline results.

**Resett** | `resett.no` | Status: `NEW DISCARD`
- **Discard reasoning:** Far-right alternative media outlet repeatedly sanctioned by the Norwegian Press Complaints Commission (PFU). No original reporting of strategic value — primarily commentary, culture-war framing, and conspiracy-adjacent content. Would inject noise and displace legitimate right-of-centre sources (Minerva, Nettavisen) from results. Active discard warranted.

---

## STRUCTURAL COVERAGE CHECK

| Structural Role | Source(s) | Tier | Notes |
|---|---|---|---|
| Government leak channel | Klassekampen, NRK | T1, T1 | Klassekampen for left-government coalition signals; NRK Brennpunkt for investigative leaks from within the state apparatus |
| Opposition voice | Klassekampen (left), Minerva (right), Nettavisen (populist-right) | T1, T3, Neutral | Left opposition is strongest at Tier 1; right opposition is distributed across Tier 3 and Neutral. Aftenposten editorials also carry centre-right opposition signals |
| Defence/security first-mover | Forsvarets forum, Aldrimer.no, VG | T2, T2, T2 | Norway has unusually strong dedicated defense press. Forsvarets forum for institutional perspective, Aldrimer.no for investigative, VG for breaking incidents |
| Policy-elite discourse | NUPI, Morgenbladet, Aftenposten | T2, T2, T1 | NUPI for think-tank depth; Morgenbladet for intellectual-elite debate; Aftenposten for what decision-makers read daily |
| Domestic-language depth | NRK, Aftenposten, DN, Klassekampen, VG, + all Norwegian-language sources | T1-T3 | Norway's media operates primarily in Norwegian. English sources (High North News English edition, NUPI English publications, Forsvarets forum English section) are supplements. Non-English domestic sources receive boost premium |
| Official government source | regjeringen.no, stortinget.no | T2, T2 | **LAYER 2 MIGRATION** — primary fetch via direct polling. Goggle boost as fallback. Includes regjeringen.no subdomains (utenriksdepartementet, forsvarsdepartementet) |
| Analytical/think tank depth | NUPI, FFI, Energi og Klima, Morgenbladet | T2, T3, T3, T2 | NUPI for foreign policy; FFI for defense technology; Energi og Klima for energy/climate statecraft; Morgenbladet for elite intellectual analysis |
| Wire service (local bureau) | Reuters, AP News, France24 | Neutral | Not boosted in Goggle — wire copy is available organically. Reuters is blocked by Anthropic crawler but Brave can still surface it for discovery. Listed in no.yaml wire section |
| Arctic/High North specialist | High North News | T3 | Dedicated niche coverage of Norway's stated top strategic priority. Supplemented by NRK, Aftenposten, Forsvarets forum for major Arctic developments |

**Gaps identified:**
1. **Technology/cyber statecraft** lacks a dedicated Norwegian-language source — coverage of semiconductor policy, data sovereignty, and digital infrastructure is distributed across DN, E24, and government white papers. FFI (newly added at Tier 3) partially mitigates this for defense-technology, and NUPI's cyber-security research stream supplements. But no single source systematically tracks Norway's digital-infrastructure and technology-transfer policy.
2. **Sami-policy and indigenous-rights dimensions** of resource extraction and Arctic sovereignty (relevant after the Fosen wind-farm Supreme Court ruling) are underrepresented. Klassekampen and NRK Sapmi provide partial coverage, but no specialist outlet focuses on the intersection of indigenous rights and strategic posture. This is a known gap with no clean mitigation.
3. **Norwegian-language social media discourse** (X/Twitter, Facebook groups used by military personnel, defense commentators, and party activists) is not captured by traditional outlet monitoring. Separate collection methodology required.
4. **Sovereign wealth fund ethical exclusions** — GPFG divestment decisions carry geopolitical implications. DN covers these, but the primary source (NBIM annual reports, Council on Ethics recommendations) should be polled via Layer 2 direct fetch rather than relying on media coverage.

---

## REDUNDANCY RESOLUTION

**Broadsheet/tabloid cluster: NRK + Aftenposten + VG + Dagbladet**
All four are high-reach general-interest outlets. Resolved by differentiating structural roles: NRK (Tier 1, public broadcaster, agenda-setter, free), Aftenposten (Tier 1, newspaper of record, establishment-right, foreign policy depth), VG (Tier 2, breaking news speed + polling, tabloid format), Dagbladet (Tier 3, progressive editorial lens, overlaps with both VG on format and Klassekampen on ideology). VG drops below the broadsheet leaders because tabloid format means lower analytical depth. Dagbladet drops to Tier 3 because it is redundant with VG on speed and with Klassekampen on progressive perspective.

**Business press cluster: DN + E24**
Both cover economic statecraft. DN leads (Tier 1) due to greater analytical depth and editorial distinctiveness. E24 at Tier 2 as the free-access extraction complement — when DN's hard paywall blocks the pipeline, E24 provides the fallback signal. No need to demote either further; different access models justify different tiers without true redundancy.

**Defense/security cluster: Forsvarets forum + Aldrimer.no + Filter Nyheter**
Three security-focused outlets. Resolved by niche differentiation: Forsvarets forum (Tier 2, institutional military perspective, procurement/exercises), Aldrimer.no (Tier 2, independent investigative, capability gaps/intelligence), Filter Nyheter (Tier 3, extremism/hybrid threats/disinformation). No true redundancy — each covers different aspects of the security domain.

**Think tank/depth cluster: NUPI + FFI + Morgenbladet + Energi og Klima**
Four analytical/specialist sources. Resolved by domain differentiation: NUPI (Tier 2, foreign policy/diplomacy), FFI (Tier 3, defense technology), Morgenbladet (Tier 2, elite intellectual discourse across domains), Energi og Klima (Tier 3, energy/climate statecraft). No overlap — each fills a distinct analytical niche.

**Opposition cluster: Klassekampen + Minerva + Nettavisen**
Three ideological outlets spanning left to right. Resolved by structural importance: Klassekampen (Tier 1, left opposition — dominant voice against NATO/EU/basing policy), Minerva (Tier 3, conservative intellectual — lower frequency, narrower domain), Nettavisen (Neutral, populist-right — high volume, low depth, FrP-adjacent). Klassekampen's Tier 1 status reflects that left-opposition discourse is more structurally consequential for Norway's strategic posture than right-populist discourse (the latter is primarily about immigration, not alliance or defense policy).

---

## QUERY CONFIGURATION

```
country: NO
search_lang: no
freshness: pw
```

**Multi-language notes:** Norway's media ecosystem operates primarily in Norwegian (Bokmal dominates; some Nynorsk). English-language content is available from regjeringen.no, High North News, NUPI, and Forsvarets forum but is supplementary. Queries should run primarily in Norwegian; a secondary English query cycle for defense/Arctic topics captures English-language specialist content. The pipeline's existing `languages.metadata: en` configuration handles this correctly.

**Localized query vocabulary validation:**

The curation prompt's vocabulary is solid. Notes:

- **Domain 1 (Diplomatic):** All terms valid. Add `"Stoere utenrikspolitikk"` and `"Barth Eide"` as leader-specific patterns. `"nordomrader"` (northern areas) is the key framing term for Norway's strategic priority — should appear in most diplomatic queries. Consider adding `"nordisk forsvarssamarbeid"` (Nordic defense cooperation) given NORDEFCO and Nordic NATO integration.
- **Domain 2 (Security):** Strong list. Add `"Finnmark"` as a geographic signal term — most Russia-adjacent military activity stories reference Finnmark. `"totalforsvar"` (total defense) is correct and increasingly used since 2022. Add `"F-35"` and `"ubat"` (submarine) for procurement-specific queries. Add `"Fokus-rapporten"` for E-tjenesten's annual threat assessment.
- **Domain 3 (Economic):** Excellent. `"Oljefondet"` and `"Statens pensjonsfond utland"` are correct for GPFG. Add `"NBIM"` (Norges Bank Investment Management) for sovereign-wealth fund operational queries. `"gronn omstilling"` (green transition) is the dominant frame for energy-policy debate. Add `"havvind"` (offshore wind) — major emerging statecraft domain. Add `"Equinor"` as a named-entity query term.
- **Domain 4 (Institutional):** Valid. Add `"NORDEFCO"` for Nordic defense cooperation. `"nordisk samarbeid"` is correct. Add `"EOS-utvalget"` (parliamentary intelligence oversight committee) — relevant for institutional checks on security services. `"stortingsmelding"` is the key document type for detecting policy shifts.
- **Domain 5 (Domestic):** Strong. Add `"forsvarsforliket"` (defense settlement/cross-party defense agreement) — the defining domestic constraint on defense spending. Add `"Hurdalsplattformen"` (the current coalition agreement). `"EU-medlemskap"` remains relevant as a latent domestic debate. Add `"Stortingsvalget 2025"` or current electoral cycle terms.

**Stale/problematic terms:** None are stale. `"folkeavstemning"` (referendum) is low-frequency but valid — Norway's 1994 EU referendum remains a reference point in EU-membership debate.

**Suggested topic query patterns:**

1. `Stoere NATO forsvarsbudsjett tooprosentmalet` — Defense spending / NATO 2% target
2. `nordomrader Russland Finnmark beredskap` — High North / Russia / military readiness
3. `Oljefondet NBIM utelukkelse sanksjoner` — Sovereign wealth fund exclusions / sanctions
4. `EOS-avtalen EU-tilpasning gronn omstilling` — EEA alignment / green transition
5. `totalforsvar langtidsplan Forsvaret` — Total defense / long-term defense plan

---

## GOGGLE FILE

```goggle
! name: MPM Norway
! description: MPM pipeline source prioritization for Norway — boosts high-signal sources, discards noise
! public: false
! author: MPM Pipeline

! --- Tier 1: Essential (boost=3) ---
$boost=3,site=nrk.no
$boost=3,site=aftenposten.no
$boost=3,site=dn.no
$boost=3,site=klassekampen.no

! --- Tier 2: Important (boost=2) ---
$boost=2,site=vg.no
$boost=2,site=forsvaretsforum.no
$boost=2,site=e24.no
$boost=2,site=regjeringen.no
$boost=2,site=stortinget.no
$boost=2,site=nupi.no
$boost=2,site=aldrimer.no
$boost=2,site=morgenbladet.no

! --- Tier 3: Supplementary (boost=1) ---
$boost=1,site=highnorthnews.com
$boost=1,site=minerva.no
$boost=1,site=dagbladet.no
$boost=1,site=energiogklima.no
$boost=1,site=filternyheter.no
$boost=1,site=ffi.no

! --- Discard: Noise ---
$discard,site=thelocal.no
$discard,site=norwaytoday.info
$discard,site=resett.no
```

---

## INTERPRETIVE CONTEXT FOR DOSSIER

### Tier 1 Sources

> Articles from **NRK** about any domain should be interpreted as Norway's most trusted and structurally neutral reporting — its public-service mandate and highest-trust-brand status mean its coverage reflects the mainstream Norwegian consensus. When NRK frames a development as significant, the Norwegian political class treats it as significant. Its Brennpunkt investigative unit produces the most impactful Norwegian investigative journalism.

> Articles from **Aftenposten** about foreign policy and institutional affairs should be interpreted as filtered through a centre-right establishment lens because its historical links to Hoyre (Conservative Party) and Schibsted ownership place it at the core of Norway's foreign-policy establishment — its editorial page reflects what NATO-aligned, transatlantic-oriented Norwegian elites think, which may overstate consensus on alliance commitment and understate domestic opposition.

> Articles from **Dagens Naeringsliv** about economic policy and sovereign wealth should be interpreted as reflecting the perspective of Norway's business and financial establishment because its pro-market, economically liberal orientation means it frames petroleum policy, GPFG decisions, and green transition through an investment-climate lens — critical coverage of regulatory intervention does not necessarily mean the policy is failing, only that it concerns market participants.

> Articles from **Klassekampen** about NATO, defense spending, EU/EEA alignment, and arms exports should be interpreted as Norway's principal left-opposition voice because it self-identifies as "venstresidas dagsavis" (the Left's daily) and its op-ed pages are the primary forum for critiquing transatlantic alignment, US basing agreements, and petroleum policy — essential for detecting domestic contestation that may constrain government action, but not representative of majority Norwegian opinion on alliance questions.

### Tier 2 Sources

> Articles from **VG** about defense incidents and political crises should be interpreted as the fastest-cycle Norwegian news source with tabloid editorial instincts — it will break stories before other outlets but may amplify drama. Its polling coverage (Respons Analyse, Norstat) is the most reliable public barometer of domestic political constraints.

> Articles from **Forsvarets forum** about military procurement, exercises, and force structure should be interpreted as institutionally informed but structurally biased toward the Norwegian Armed Forces' perspective — it is editorially independent but published by Forsvaret, meaning it will present military capability and readiness through a lens that may understate resource gaps or institutional failures that Aldrimer.no would surface.

> Articles from **E24** about energy markets and economic developments should be interpreted as faster-cycle, less analytically deep coverage than DN — useful for real-time economic signals but lacking the editorial depth and exclusive sourcing that make DN the primary economic-statecraft source.

> Articles from **regjeringen.no** and **stortinget.no** should be interpreted as official government and parliamentary communications — not journalism but primary source material. Press releases, white papers, and parliamentary records represent the state's chosen public position, which may differ from actual policy implementation or internal debate.

> Articles from **NUPI** about foreign policy, security, and institutional engagement should be interpreted as Norway's most authoritative non-governmental analytical voice — its government funding (Ministry of Education and Research) does not compromise editorial independence, but its researchers operate within the Norwegian foreign-policy establishment consensus, meaning NUPI analysis may understate genuinely heterodox policy options.

> Articles from **Aldrimer.no** about defense readiness and security threats should be interpreted as independent investigative reporting that deliberately surfaces what the defense establishment prefers not to discuss — capability gaps, intelligence operations, and Russian military activity. Editor Kjetil Stormark's sourcing within defense/intelligence circles is deep, but the outlet's adversarial stance toward official readiness narratives means it may frame ambiguous situations more alarmingly than warranted.

> Articles from **Morgenbladet** about political and foreign-affairs developments should be interpreted as intellectual-elite discourse rather than news reporting — its weekly cadence and Le Monde diplomatique-style format mean it provides interpretive frameworks rather than breaking information. When former diplomats and academics publish in Morgenbladet, they are signaling elite-debate shifts before those shifts appear in daily media.

# AUDIT SUMMARY: TAIWAN

**Sources assessed:** 18 recommended + 5 excluded + 4 newly identified = 27 total
**Tier 1 (boost=3):** 5 sources
**Tier 2 (boost=2):** 8 sources
**Tier 3 (boost=1):** 5 sources
**Neutral (no rule):** 5 sources
**Discard:** 4 sources
**Overall assessment:** The curation prompt produced a strong whitelist with excellent cross-strait polarization mapping — both pan-green and pan-blue editorial lines are well-represented, enabling the convergence-detection methodology described in the source map. Key changes: (1) resolved redundancy among the three English-language pan-green outlets by differentiating tiers; (2) promoted government official sources (MOFA, MND, Presidential Office, Executive Yuan) for Layer 2 migration at Tier 2; (3) added missing DigiTimes for semiconductor supply-chain coverage and CSIS for external analytical depth; (4) applied non-English domestic boost premium to Mandarin-only sources (Liberty Times, UDN, Storm Media, SET News) that carry signals unavailable in English; (5) downgraded China Times from recommended to Neutral with interpretive flagging given documented PRC editorial influence. No Taiwan domains appear on the Anthropic blocked domains list — all sources are extractable.

---

## BOOST ASSIGNMENTS

### Tier 1 — `$boost=3`

**Focus Taiwan (CNA English)** | `focustaiwan.tw` | Type: `wire_service` | Status: `EXISTING`
- **Structural role:** Taiwan's national wire service English edition. The fastest English-language source for all official government statements, MOFA press releases, and defense ministry announcements. Functions as the primary triage source for the pipeline.
- **Domain coverage:** Diplomatic alignment, Security & defense, Economic statecraft, Institutional engagement
- **Reasoning:** Focus Taiwan is the single indispensable English-language source for Taiwan. It carries every official statement, every diplomatic development, and every defense announcement before any other English outlet. Its government-funded status means it reflects incumbent framing (currently DPP), but it is the wire — the pipeline needs it surfacing first. Fully open, no paywall, easily extractable.

**Liberty Times (自由時報)** | `ltn.com.tw` | Type: `paper_of_record` | Status: `EXISTING`
- **Structural role:** Taiwan's largest-circulation daily. The pan-green editorial anchor and primary barometer for the pro-sovereignty policy establishment.
- **Domain coverage:** Diplomatic alignment, Security & defense, Domestic constraints
- **Reasoning:** Non-English domestic boost premium applies — Liberty Times operates in Mandarin (Traditional Chinese) and carries signals that never surface in English translation. Its editorials function as a direct barometer of DPP-aligned elite opinion on defense spending, conscription reform, and cross-strait friction. When Liberty Times and UDN converge on an issue, it signals genuine bipartisan consensus — a critical posture-shift indicator. The pipeline needs LTN at maximum boost to ensure Mandarin-language domestic signals are not drowned out by English wire copy.
- **Extraction note:** Chinese-language only. Pipeline must handle Traditional Chinese extraction.

**Taipei Times** | `taipeitimes.com` | Type: `paper_of_record` | Status: `EXISTING`
- **Structural role:** Taiwan's only remaining English-language daily. Sister publication to Liberty Times. Primary English-language source for Legislative Yuan debates and domestic political dynamics.
- **Domain coverage:** Diplomatic alignment, Security & defense, Domestic constraints, Institutional engagement
- **Reasoning:** Irreplaceable structural role as the only English daily. Translates and contextualizes key LTN reporting, making pan-green domestic signals accessible to the English-language pipeline. Strong editorial page with expert op-eds on defense, diplomacy, and cross-strait policy. Despite pan-green editorial orientation, its translation function means it captures reporting that would otherwise be invisible to the pipeline. Fully open, no paywall.

**United Daily News (聯合報)** | `udn.com` | Type: `paper_of_record` | Status: `EXISTING`
- **Structural role:** Taiwan's principal pan-blue daily. Essential counterweight to Liberty Times. When UDN and LTN agree, the pipeline has its strongest posture-shift signal.
- **Domain coverage:** Diplomatic alignment, Domestic constraints, Security & defense
- **Reasoning:** Non-English domestic boost premium applies. UDN is the editorial anchor of the pan-blue establishment — its editorials reflect KMT/opposition perspective on defense spending, US relations, and cross-strait policy. Structural role as the opposition broadsheet outweighs quality concerns about its partially paywalled model. The convergence-detection methodology described in the source map depends entirely on having both LTN and UDN at maximum boost. Coverage of opposition legislative tactics (e.g., blocking the special defense budget) is unmatched.
- **Extraction note:** Partially paywalled (UDN Premium). Core news content is free. Diffbot extraction likely partial for premium content.

**CommonWealth Magazine (天下雜誌)** | `cw.com.tw` | Type: `business_financial` / `policy_magazine` | Status: `EXISTING`
- **Structural role:** Taiwan's most trusted news brand (Reuters Institute). Premier source for semiconductor policy, CPTPP dynamics, supply-chain restructuring, and economic diplomacy.
- **Domain coverage:** Economic & technological statecraft, Institutional engagement, Domestic constraints
- **Reasoning:** No other source covers TSMC supply-chain decisions, CPTPP accession dynamics, nearshoring, and tech-statecraft at this depth. Centrist-independent editorial orientation and data-driven methodology give it credibility that partisan outlets lack. English edition at `english.cw.com.tw` makes key content accessible. Policymaker readership is high — what CommonWealth publishes shapes elite economic policy discourse. Tier 1 for its unique economic statecraft coverage that no other source replicates.
- **Extraction note:** Paywalled for premium content. English edition has more open access.

---

### Tier 2 — `$boost=2`

**INDSR (國防安全研究院)** | `indsr.org.tw` | Type: `think_tank` / `security_defense` | Status: `EXISTING`
- **Structural role:** Taiwan's top military think tank. MND-affiliated. Publishes the Defense Security Brief and research on PLA activities, cognitive warfare, cybersecurity, and regional security architecture.
- **Domain coverage:** Security & defense, Diplomatic alignment, Institutional engagement
- **Reasoning:** Think tanks earn boost through depth, not speed. INDSR research outputs signal MND analytical priorities and threat assessments — when INDSR publishes on a topic, it reflects what the defense establishment considers important. English-language publications available. Tier 2 rather than Tier 1 because it doesn't break news and publishes on an institutional timeline, but its analytical depth on defense topics is unmatched by any media outlet.

**Prospect Foundation (遠景基金會)** | `pf.org.tw` | Type: `think_tank` / `foreign_policy` | Status: `EXISTING`
- **Structural role:** Government-affiliated foreign policy think tank. Hosts Track 1.5/2 dialogues including Taiwan-US-Japan Trilateral Security Dialogue.
- **Domain coverage:** Diplomatic alignment, Institutional engagement, Security & defense
- **Reasoning:** Think tanks earn boost through depth, not speed. Prospect Foundation's "Prospects & Perspectives" policy briefs signal official foreign policy thinking and diplomatic priorities. Its Track 1.5/2 dialogue hosting means it surfaces elite diplomatic signals before they appear in media coverage. Tier 2 for analytical depth on diplomatic alignment — the domain where Taiwan's posture shifts are most consequential.

**The News Lens (關鍵評論網)** | `thenewslens.com` | Type: `digital_independent` | Status: `EXISTING`
- **Structural role:** Bilingual (Mandarin/English) analytical platform with strong explainer content. Bridges the gap between wire brevity and academic publishing timelines.
- **Domain coverage:** Diplomatic alignment, Security & defense, Economic statecraft, Institutional engagement
- **Reasoning:** Bilingual coverage across all four external domains makes it uniquely versatile. English international edition at `international.thenewslens.com` is accessible to the pipeline. Centrist-independent editorial orientation provides a less polarized analytical lens than the pan-green/pan-blue dailies. Tier 2 rather than Tier 1 because it synthesizes and analyzes rather than breaks news, and its audience skews younger — less policymaker-driven than CommonWealth.

**Storm Media (風傳媒)** | `storm.mg` | Type: `digital_independent` / `commentary_platform` | Status: `EXISTING`
- **Structural role:** High-traffic digital platform with robust opinion section featuring retired military officers, diplomats, and policy commentators. Acquired The Journalist magazine (新新聞), adding investigative capacity.
- **Domain coverage:** Domestic constraints, Diplomatic alignment, Security & defense
- **Reasoning:** Non-English domestic boost premium applies. Storm Media's opinion section is where retired generals, ex-diplomats, and policy insiders publish commentary that surfaces elite opinion shifts before they manifest in official policy. Center-right/pan-blue lean, but publishes diverse commentary. The Journalist acquisition adds investigative depth. Tier 2 for its elite-opinion barometer function.
- **Extraction note:** Chinese-language only. Open access.

**The Reporter (報導者)** | `twreporter.org` | Type: `investigative` | Status: `EXISTING`
- **Structural role:** Taiwan's premier investigative outlet. Nonprofit, donation-funded, editorially independent. Produces deep-dive reporting on defense procurement, military reform, and economic policy implementation.
- **Domain coverage:** Domestic constraints, Security & defense, Economic statecraft
- **Reasoning:** Non-English domestic boost premium applies. The Reporter fills the investigative-depth gap that daily outlets cannot — defense procurement corruption, cross-strait economic dependencies, and military reform implementation are covered with sourcing depth unavailable elsewhere. Slow-cycle but high-signal. Tier 2 rather than Tier 1 because publication frequency is low and it doesn't break fast-moving diplomatic stories. Fully open, no paywall.

**MOFA (外交部)** | `mofa.gov.tw` | Type: `government_official` | Status: `EXISTING` — **LAYER 2 MIGRATION**
- **Structural role:** Ministry of Foreign Affairs. Direct primary source for diplomatic statements, ally-count changes, bilateral agreements, and international organization participation bids.
- **Domain coverage:** Diplomatic alignment, Institutional engagement
- **Reasoning:** Government sources = Layer 2 migration at Tier 2. Primary fetch via Layer 2 direct polling. Goggle boost at Tier 2 as belt-and-suspenders fallback. MOFA press releases are often the first signal of diplomatic posture shifts. English site well-maintained at `en.mofa.gov.tw`.

**MND (國防部)** | `mnd.gov.tw` | Type: `government_official` | Status: `EXISTING` — **LAYER 2 MIGRATION**
- **Structural role:** Ministry of National Defense. Publishes the biennial National Defense Report, PLA activity reports (ADIZ intrusion data), defense budget documents, and procurement announcements.
- **Domain coverage:** Security & defense
- **Reasoning:** Government sources = Layer 2 migration at Tier 2. Primary fetch via Layer 2 direct polling. Goggle boost at Tier 2 as belt-and-suspenders fallback. The 2025 NDR and NT$1.25 trillion special defense budget are current critical documents. English site at `eng.mnd.gov.tw`. Includes both `mnd.gov.tw` and `eng.mnd.gov.tw`.

**Presidential Office / Executive Yuan** | `president.gov.tw` / `ey.gov.tw` | Type: `government_official` | Status: `NEW (from tw.yaml)` — **LAYER 2 MIGRATION**
- **Structural role:** Central executive primary sources. Presidential Office for head-of-state communications; Executive Yuan for cabinet-level policy announcements.
- **Domain coverage:** All five domains (official source)
- **Reasoning:** Government sources = Layer 2 migration at Tier 2. Listed in tw.yaml at Tier 1 for direct polling but not included in the source intelligence map's recommended list. Added here for Goggle belt-and-suspenders coverage. Presidential statements and Executive Yuan announcements occasionally surface in Brave News Search.

---

### Tier 3 — `$boost=1`

**TVBS News** | `news.tvbs.com.tw` | Type: `broadcast_online` | Status: `EXISTING`
- **Structural role:** Highest-rated TV news channel with Taiwan's most-cited polling unit (TVBS Poll Center). Pan-blue leaning.
- **Domain coverage:** Domestic constraints, Security & defense, Diplomatic alignment
- **Reasoning:** TVBS Poll Center data is independently valuable for tracking domestic constraint shifts — public opinion on defense spending, conscription reform, and cross-strait posture. Tier 3 rather than Tier 2 because broadcast-first outlets produce web content that is often video-centric and wire-derived, reducing text extraction utility. But its polling function justifies a boost above Neutral.
- **Extraction note:** Website and YouTube open. Limited English section.

**Ketagalan Media** | `ketagalanmedia.com` | Type: `commentary_platform` | Status: `EXISTING`
- **Structural role:** English-language analysis focused on Taiwan politics, identity, and international positioning. Fills the gap between wire brevity and academic timelines for English-language audiences.
- **Domain coverage:** Diplomatic alignment, Domestic constraints, Institutional engagement
- **Reasoning:** Tier 3 because it's commentary/analysis rather than original reporting, and its pro-sovereignty editorial orientation overlaps with Taipei Times. But it provides rapid English-language interpretation of domestic political events (Legislative Yuan dynamics, civil society movements) that Taipei Times' daily format cannot match in analytical depth. Fully open.

**Taiwan News** | `taiwannews.com.tw` | Type: `aggregator` / `digital_news` | Status: `EXISTING`
- **Structural role:** High-volume English-language aggregator covering defense, diplomacy, and cross-strait developments. Rapid translation/summarization of Chinese-language breaking news.
- **Domain coverage:** Security & defense, Diplomatic alignment, Economic statecraft
- **Reasoning:** Tier 3 because it's primarily an aggregator with limited original reporting depth. But its high SEO visibility means it is often the first English result for Taiwan news events, and its rapid translation function provides early English-language signals from Chinese-language sources. Useful as a first-pass alert layer. Not higher than Tier 3 because it's derivative — Taipei Times and Focus Taiwan provide the same information with more editorial rigor.

**New Bloom Magazine (破土)** | `newbloommag.net` | Type: `activist_media` | Status: `EXISTING`
- **Structural role:** Rare English-language source covering Taiwan's social movements, youth politics, civil-military relations, and protest dynamics. Born from the 2014 Sunflower Movement.
- **Domain coverage:** Domestic constraints, Diplomatic alignment
- **Reasoning:** Fills a genuine gap on civil society constraints on foreign/defense policy that mainstream outlets undercover — Sunflower/Bluebird movement dynamics, youth political attitudes, PRC influence operations. Tier 3 because narrow scope and activist framing limit pipeline utility, but the civil society constraint signal is structurally important and unavailable elsewhere in English.

**DigiTimes** | `digitimes.com` | Type: `industry_specialist` | Status: `NEW`
- **Structural role:** Taiwan-based semiconductor and electronics industry publication. Covers TSMC supply-chain decisions, fab-location diplomacy, export control compliance, and chip industry dynamics at operational tempo.
- **Domain coverage:** Economic & technological statecraft
- **Reasoning:** The source intelligence map explicitly flagged a coverage gap in semiconductor/tech-statecraft granularity. DigiTimes fills this gap — it tracks TSMC capacity allocation, advanced node decisions, US CHIPS Act compliance, and fab construction timelines that CommonWealth covers only at the policy level. Single-domain but structurally essential for Taiwan's most consequential economic statecraft dimension. Tier 3 because narrow scope, but within its niche nothing else on the list competes.
- **Extraction note:** Partially paywalled. Headlines and summaries accessible.

---

### Neutral — no Goggle rule

**China Times (中國時報)** | `chinatimes.com` | Type: `narrative_indicator` | Status: `EXISTING → DEMOTED TO NEUTRAL`
- **Why neutral:** The source map correctly identifies China Times as a narrative indicator rather than a reliable factual source — documented PRC editorial influence via the Want Want Group and Taiwan Affairs Office. Under the hard-filter model, it was included as a recommended source for detecting PRC-preferred framing shifts. Under the Goggle model, no boost is needed — China Times content will surface organically in Brave results for cross-strait queries, and the interpretive context tells the LLM how to handle it. Boosting it would displace higher-signal sources. The exclusion principle says exclusions default to Neutral, not Discard — China Times still carries structural signal (PRC messaging strategy) even though it's factually unreliable.

**SET News (三立新聞)** | `setn.com` | Type: `broadcast_online` | Status: `EXISTING → DEMOTED TO NEUTRAL`
- **Why neutral:** Pan-green television counterpart to TVBS. Strongly DPP-aligned. Under the Goggle model, its structural signal (pro-sovereignty broadcast framing) is adequately captured by Liberty Times and Taipei Times at Tier 1. Broadcast-first web content is video-heavy and largely wire-derived. No reason to actively discard — if SET breaks a story, Brave may surface it organically.

**CTiTV (中天新聞)** | `ctitv.com.tw` | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Broadcast license revoked by NCC in 2020 for PRC influence. Now YouTube-only. Curation exclusion was correct under the hard-filter model. Under the Goggle model, no reason to actively discard — it's unlikely to surface in Brave News Search given its deplatforming, and China Times (Neutral) serves as a more useful proxy for the same editorial line.

**ETtoday (東森新媒體)** | `ettoday.net` | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Extremely high traffic but dominated by clickbait and sensationalism. Low signal-to-noise for strategic analysis. Under the Goggle model, organic ranking is appropriate — ETtoday may surface for high-traffic breaking events and the pipeline benefits from seeing mass-audience framing even if analytical depth is low. No reason to actively discard.

**Mirror Media (鏡週刊)** | `mirrormedia.mg` | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Investigative tabloid with occasional useful scoops on political scandals and defense procurement. Inconsistent coverage and tabloid framing reduce analytical utility compared to The Reporter (Tier 2). Under the Goggle model, leave at organic ranking — when Mirror Media breaks a procurement scandal, Brave will surface it without a boost.

---

### Discard — `$discard`

**Want Want China Times TV (中天亞洲台/旺旺中時媒體集團 YouTube channels)** | Various YouTube channels | Status: `NEW DISCARD`
- **Discard reasoning:** Want Want Group's YouTube-only broadcast channels post PRC-influenced commentary with no editorial accountability. China Times (Neutral) already captures the structural signal of PRC-preferred narratives in text form. YouTube commentary channels would inject noise and displace higher-signal sources.

**Taiwan People News (民報)** | `peoplenews.tw` | Status: `NEW DISCARD`
- **Discard reasoning:** Hyper-partisan deep-green outlet with no original reporting staff. Republishes commentary and opinion that duplicates Liberty Times' editorial line without LTN's reporting infrastructure. Would waste result slots.

**Newtalk (新頭殼)** | `newtalk.tw` | Status: `NEW DISCARD`
- **Discard reasoning:** High-volume digital platform that primarily aggregates wire copy and republishes press releases with minimal editorial added value. Pan-green lean duplicates Liberty Times/Taipei Times coverage without original reporting depth. Would displace higher-signal sources.

**Talk Show Clip Aggregators** | Various YouTube channels | Status: `NEW DISCARD`
- **Discard reasoning:** Political talk show clips (政論節目) from channels like PTV, 54新觀點, etc. are YouTube-only, lack text extraction paths, and produce commentary noise rather than reportable facts. The signals from these shows that matter will be reflected in the text-based sources already on the list.

---

## STRUCTURAL COVERAGE CHECK

| Structural Role | Source(s) | Tier | Notes |
|---|---|---|---|
| Government signaling channel | Focus Taiwan (CNA) | T1 | State-funded wire reflects incumbent (DPP) framing. Liberty Times editorials track DPP-aligned elite opinion. La Jornada equivalent for Taiwan. |
| Opposition voice | UDN, TVBS, Storm Media | T1, T3, T2 | UDN is the pan-blue editorial anchor; TVBS captures broadcast-audience pan-blue sentiment; Storm Media hosts retired military/diplomatic commentators |
| Defence/security first-mover | Focus Taiwan, MND (Layer 2), INDSR | T1, T2, T2 | CNA breaks MND announcements first; INDSR provides analytical depth; MND direct polling captures ADIZ data and procurement announcements |
| Policy-elite discourse | CommonWealth, Prospect Foundation, INDSR | T1, T2, T2 | CommonWealth for economic policy elite; Prospect Foundation for diplomatic elite; INDSR for defense elite |
| Domestic-language depth | Liberty Times, UDN, Storm Media, The Reporter | T1, T1, T2, T2 | Non-English domestic boost premium applied. These four Mandarin-only sources carry signals invisible to English-language monitoring |
| Official government source | MOFA, MND, president.gov.tw, ey.gov.tw | T2 | **LAYER 2 MIGRATION** — primary fetch via direct polling. Goggle boost as fallback |
| Analytical/think tank depth | INDSR, Prospect Foundation, CommonWealth | T2, T2, T1 | INDSR for defense analysis; Prospect Foundation for diplomatic analysis; CommonWealth for economic policy analysis |
| Investigative depth | The Reporter | T2 | Taiwan's sole dedicated investigative outlet. Slower cycle but high-impact reporting on defense procurement and economic dependencies |
| Wire service (international) | Reuters, AP News, France24 | Neutral | Listed in tw.yaml. Not boosted — wire copy surfaces organically. Reuters blocked by Anthropic crawler but Brave can still surface for discovery |
| Semiconductor/tech statecraft | CommonWealth, DigiTimes | T1, T3 | CommonWealth for policy level; DigiTimes for operational/industry level. Partially addresses the coverage gap flagged in the source map |
| Cross-strait narrative indicator | China Times | Neutral | PRC-preferred framing barometer. Surfaces organically — no boost needed, interpretive context handles editorial discount |
| Bilingual bridge | The News Lens, Taipei Times | T2, T1 | These outlets make Mandarin-language signals accessible in English for the pipeline |

**Gaps identified:**
1. **Real-time Hokkien-language discourse** remains a structural blind spot as flagged in the source map. Political talk shows on FTV and SET broadcast in Hokkien carry grassroots sentiment signals that do not reliably surface in text-based sources. No mitigation available in the Goggle model — this requires a separate monitoring capability.
2. **Local-level political dynamics** — county/city government positioning on military base expansion, port access agreements, and civil defense exercises are underrepresented in national outlets. No regional newspaper was added to avoid over-expanding the Goggle.
3. **PLA activity analytical overlay** — while MND (Layer 2) provides raw ADIZ intrusion data, the analytical overlay (satellite imagery analysis, order-of-battle tracking) depends on external sources like CSIS and IISS that are not Taiwan-specific and are better handled through the international analytical layer rather than the country Goggle.

---

## REDUNDANCY RESOLUTION

**Pan-green English cluster: Taipei Times + Taiwan News + Ketagalan Media + New Bloom**
Four English-language outlets with pro-sovereignty editorial orientation. Resolved by structural function: Taipei Times (Tier 1, only English daily, translates LTN), Taiwan News (Tier 3, aggregator/alert layer), Ketagalan Media (Tier 3, analytical commentary), New Bloom (Tier 3, civil society niche). Taipei Times is the only one with daily reporting infrastructure; the others are supplements that each fill a distinct sub-niche.

**Pan-blue broadsheet cluster: UDN + China Times**
Both pan-blue dailies. Resolved by PRC influence: UDN (Tier 1, editorially independent pan-blue voice) vs. China Times (Neutral, documented PRC editorial influence). UDN's opposition-voice structural role is essential; China Times' signal is available organically without boosting. The convergence-detection methodology requires UDN at maximum boost — it does not require China Times.

**Broadcast-online cluster: TVBS + SET News**
Both 24-hour cable news with web presence. Resolved by editorial differentiation and polling value: TVBS (Tier 3, pan-blue, TVBS Poll Center) vs. SET News (Neutral, pan-green, duplicates LTN signal). TVBS earns a boost for its polling unit; SET News' pro-sovereignty broadcast framing is already captured by LTN and Taipei Times at Tier 1.

**Think tank cluster: INDSR + Prospect Foundation**
Two government-affiliated think tanks. No redundancy — distinct domains. INDSR covers security/defense; Prospect Foundation covers diplomacy/institutional engagement. Both at Tier 2 for analytical depth.

**Economic statecraft cluster: CommonWealth + DigiTimes**
Both cover economic/tech statecraft. No redundancy — distinct granularity levels. CommonWealth (Tier 1, policy-level economic diplomacy) vs. DigiTimes (Tier 3, operational-level semiconductor industry). CommonWealth answers "what is Taiwan's CPTPP strategy?"; DigiTimes answers "where is TSMC building its next fab?"

---

## QUERY CONFIGURATION

```
country: TW
search_lang: zh
freshness: pw
```

**Multi-language notes:** Taiwan's media ecosystem operates in Traditional Chinese (繁體字) — NOT Simplified Chinese. The pipeline must use Traditional Chinese characters for all zh-language queries. English-language sources (Focus Taiwan, Taipei Times, The News Lens International, Ketagalan Media, New Bloom, Taiwan News) provide a robust English supplement layer unusual for an Asian country. Queries should run primarily in Traditional Chinese; a secondary English query cycle captures the strong English-language ecosystem. The pipeline's `languages.metadata: en` configuration handles this correctly.

**Localized query vocabulary validation:**

The curation prompt's vocabulary is comprehensive and correctly uses Traditional Chinese throughout. Notes:

- **Domain 1 (Diplomatic):** All terms valid. Add `"賴清德外交"` (Lai Ching-te diplomacy) as a leader-specific pattern. `"邦交國"` (diplomatic allies) is critical given Taiwan's ally count as a key posture metric. Add `"全球合作暨訓練架構"` (GCTF — Global Cooperation and Training Framework) — Taiwan's primary multilateral engagement mechanism.
- **Domain 2 (Security):** Strong list. Add `"顧立雄"` (Wellington Koo, Defense Minister) — the face of current defense policy. `"潛艦國造"` (indigenous submarine program) is a major current procurement story. Add `"萬安演習"` (Wan'an civil defense exercise) — increasingly prominent since 2024. `"共軍擾臺"` (PLA harassment) is correct and high-frequency.
- **Domain 3 (Economic):** Excellent. Add `"台積電亞利桑那"` (TSMC Arizona) — the most-covered tech-statecraft story. `"晶片法案"` (CHIPS Act) is correct. Add `"護國神山"` (sacred mountain protecting the nation — colloquial for TSMC's strategic importance) — frequently used in media and policy discourse.
- **Domain 4 (Institutional):** Valid. `"世界衛生大會"` (WHA) is critical — annual push for WHA observer status is Taiwan's highest-profile multilateral engagement. Add `"台美21世紀貿易倡議"` (US-Taiwan Initiative on 21st-Century Trade) — the primary bilateral economic institutional framework.
- **Domain 5 (Domestic):** Strong. Add `"藍白合"` is correct for KMT-TPP coalition dynamics. Add `"覆議"` (executive veto / reconsideration motion) — relevant to recent Legislative Yuan confrontations. Add `"大法官釋憲"` (Constitutional Court interpretation) — critical given recent rulings on legislative power.

**Stale/problematic terms:** None are stale. `"九二共識"` (1992 Consensus) has declining relevance under DPP governance but remains a valid search term as it is still invoked by KMT and PRC actors.

**Suggested topic query patterns:**

1. `賴清德 國防特別預算 立法院` — Defense special budget legislative dynamics
2. `台積電 晶片法案 供應鏈 出口管制` — TSMC / CHIPS Act / supply chain controls
3. `共軍擾臺 防空識別區 國防部` — PLA activity / ADIZ intrusions / MND response
4. `邦交國 外交承認 斷交` — Diplomatic ally count changes
5. `CPTPP 台灣 加入 貿易` — CPTPP accession bid
6. `藍白合 立法院 少數政府 覆議` — KMT-TPP coalition / minority government dynamics

---

## GOGGLE FILE

```goggle
! name: MPM Taiwan
! description: MPM pipeline source prioritization for Taiwan — boosts high-signal sources, discards noise
! public: false
! author: MPM Pipeline

! --- Tier 1: Essential (boost=3) ---
$boost=3,site=focustaiwan.tw
$boost=3,site=ltn.com.tw
$boost=3,site=taipeitimes.com
$boost=3,site=udn.com
$boost=3,site=cw.com.tw

! --- Tier 2: Important (boost=2) ---
$boost=2,site=indsr.org.tw
$boost=2,site=pf.org.tw
$boost=2,site=thenewslens.com
$boost=2,site=storm.mg
$boost=2,site=twreporter.org
$boost=2,site=mofa.gov.tw
$boost=2,site=mnd.gov.tw
$boost=2,site=president.gov.tw
$boost=2,site=ey.gov.tw

! --- Tier 3: Supplementary (boost=1) ---
$boost=1,site=news.tvbs.com.tw
$boost=1,site=ketagalanmedia.com
$boost=1,site=taiwannews.com.tw
$boost=1,site=newbloommag.net
$boost=1,site=digitimes.com

! --- Discard: Noise ---
$discard,site=peoplenews.tw
$discard,site=newtalk.tw
```

---

## INTERPRETIVE CONTEXT FOR DOSSIER

### Tier 1 Sources

> Articles from **Focus Taiwan (CNA)** about any domain should be interpreted as Taiwan's official English-language wire service — its government-funded status means it reflects the incumbent DPP administration's framing of events, particularly on cross-strait relations and diplomatic achievements. It is fast and comprehensive but not editorially independent. When Focus Taiwan leads with a diplomatic development, the framing reflects what the government wants the international audience to see.

> Articles from **Liberty Times (自由時報)** about defense and cross-strait policy should be interpreted as reflecting the pro-sovereignty policy establishment's position because it is Taiwan's largest-circulation daily with strong DPP editorial alignment — its editorials on defense spending, conscription reform, and sovereignty issues function as a barometer of where the green camp's policy elite stands, not necessarily where the median voter stands.

> Articles from **Taipei Times** about domestic politics and legislative dynamics should be interpreted as the English-language translation of the pan-green editorial line — as Liberty Times' sister publication, it shares the same editorial orientation but performs the critical function of making domestic Mandarin-language debates accessible in English. Its op-ed page features defense and diplomatic experts who write for an international policy audience.

> Articles from **United Daily News (聯合報)** about cross-strait relations and defense policy should be interpreted as reflecting the pan-blue opposition establishment's position — its editorials on US arms sales, defense spending levels, and engagement with the PRC represent what the KMT-aligned policy class believes, making it essential for detecting opposition constraints on government policy. When UDN and Liberty Times agree on a defense or diplomatic issue, this convergence is a strong signal of genuine bipartisan consensus and likely policy durability.

> Articles from **CommonWealth Magazine (天下雜誌)** about economic policy and trade should be interpreted as Taiwan's most credible and data-driven economic analysis — its centrist-independent orientation and high trust rating mean its coverage of semiconductor policy, CPTPP dynamics, and supply-chain restructuring reflects technocratic rather than partisan analysis. Negative framing of economic policy from CommonWealth carries more weight than similar framing from partisan outlets.

### Tier 2 Sources

> Articles from **INDSR (國防安全研究院)** about defense and security should be interpreted as reflecting the MND's analytical priorities — as an MND-affiliated think tank, its research topics and threat assessments signal what the defense establishment considers important. When INDSR publishes on a new threat vector (e.g., cognitive warfare, undersea cable vulnerability), it indicates the defense establishment is actively studying the issue, which may precede policy or procurement shifts.

> Articles from **Prospect Foundation (遠景基金會)** about diplomacy and multilateral engagement should be interpreted as signaling Taiwan's official foreign policy thinking — its government affiliation and Track 1.5/2 dialogue hosting mean its publications reflect where the foreign policy establishment is directing attention. "Prospects & Perspectives" briefs on specific bilateral relationships or multilateral initiatives indicate active diplomatic engagement in those areas.

> Articles from **The News Lens (關鍵評論網)** about cross-strait and regional security should be interpreted as centrist analytical content aimed at an educated, younger audience — its bilingual format and independent editorial line make it a useful bridge between partisan domestic framing and English-language international analysis. Less authoritative than CommonWealth but broader in topical scope.

> Articles from **Storm Media (風傳媒)** about defense and foreign policy should be interpreted with awareness that its commentary section functions as a forum for retired military officers and ex-diplomats — opinion pieces from these contributors often signal elite thinking that precedes formal policy shifts, particularly on defense procurement and cross-strait engagement. The outlet's center-right/pan-blue lean means its commentary on defense spending tends to be skeptical of DPP government figures.

> Articles from **The Reporter (報導者)** about defense procurement and economic dependencies should be interpreted as Taiwan's highest-quality investigative journalism — its nonprofit, donation-funded model gives it editorial independence that advertising-dependent outlets lack. When The Reporter publishes a defense procurement investigation or a deep-dive on cross-strait economic exposure, the sourcing and methodology are typically rigorous. Slow publication cycle means its content is structural analysis, not breaking news.

> Articles from **MOFA**, **MND**, **president.gov.tw**, and **ey.gov.tw** should be interpreted as official government communications — not journalism but primary source material. Press releases and statements represent the government's chosen public position. MOFA statements on diplomatic recognition changes are factual first-party reports; MND ADIZ intrusion data is authoritative primary data. Framing and emphasis in these communications are themselves signals of government priorities.
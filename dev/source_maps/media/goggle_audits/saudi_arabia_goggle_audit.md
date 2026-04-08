# AUDIT SUMMARY: SAUDI ARABIA

**Sources assessed:** 17 recommended + 4 excluded + 5 newly identified = 26 total
**Tier 1 (boost=3):** 4 sources
**Tier 2 (boost=2):** 8 sources
**Tier 3 (boost=1):** 5 sources
**Neutral (no rule):** 6 sources
**Discard:** 3 sources
**Overall assessment:** The curation prompt produced a well-structured whitelist that correctly identifies the core challenge of Saudi OSINT: all domestic media is state-aligned, so analytical value comes from reading variation across outlets with different royal-family affiliations and regional bases, not from finding independent voices. Key changes: (1) promoted Arabic-language domestic sources (Al-Riyadh, Sabq, Al-Watan, Al-Eqtisadiah) with boost premium for non-English domestic signal; (2) migrated government official sources (SPA, MFA, Vision 2030 portal) to Layer 2 at Tier 2; (3) resolved redundancy among the three business/financial outlets by differentiating tiers; (4) added missing structural roles (wire services, defense-specialist think tank, diaspora critical voice); (5) flagged `reuters.com` as blocked by Anthropic's crawler. No Saudi domestic domains appear on the blocked list.

---

## BOOST ASSIGNMENTS

### Tier 1 -- `$boost=3`

**Arab News** | `arabnews.com` | Type: `paper_of_record` | Status: `EXISTING`
- **Structural role:** Saudi Arabia's flagship English-language daily and the kingdom's primary interface for communicating strategic posture to international audiences. SRMG-owned (royal family-linked). Functions as the international agenda-setter for Saudi government messaging.
- **Domain coverage:** Diplomatic alignment, Economic statecraft, Institutional engagement
- **Reasoning:** Arab News is the single most important source for understanding how Riyadh wants the outside world to interpret its actions. Vision 2030 coverage is extensive and early. English-language output makes it fully extractable by the pipeline. Its editorial line directly reflects the MBS modernization narrative -- what Arab News emphasizes signals government priorities; what it omits signals sensitivity. Tier 1 because it is the pipeline's most reliable, highest-frequency Saudi signal in the metadata language.

**Asharq Al-Awsat** | `aawsat.com` | Type: `paper_of_record` | Status: `EXISTING`
- **Structural role:** The premier pan-Arab broadsheet, printed in 14 cities. Saudi royal family-owned. Its editorial line on regional conflicts (Yemen, Syria, Iran) is the most reliable indicator of Saudi strategic consensus among Arabic-language papers.
- **Domain coverage:** Diplomatic alignment, Security & defense, Institutional engagement
- **Reasoning:** Asharq Al-Awsat fills the structural role that Arab News cannot: Arabic-language depth on regional security and diplomacy, read by Arab decision-makers across the Middle East. English edition at `english.aawsat.com` provides pipeline-accessible coverage. When Asharq Al-Awsat's framing on Iran or Yemen shifts, it signals real policy movement. Tier 1 because it is the Arabic broadsheet with the widest pan-Arab reach and the closest alignment to Saudi strategic consensus. Non-English domestic source boost premium applies.
- **Extraction note:** English edition available at english.aawsat.com; Arabic edition at aawsat.com. Both should be boosted under the same domain.

**Al-Eqtisadiah** | `aleqt.com` | Type: `business_financial` | Status: `EXISTING`
- **Structural role:** Saudi Arabia's only dedicated economic daily. SRMG-owned. Essential for tracking Vision 2030 implementation, PIF investments, NEOM progress, privatization, and trade diversification metrics.
- **Domain coverage:** Economic statecraft, Diplomatic alignment
- **Reasoning:** No other source covers Saudi economic statecraft at this depth. PIF portfolio moves, Tadawul developments, NEOM milestones, privatization timelines, and non-oil revenue targets all appear in Al-Eqtisadiah first or with the most granularity. Arabic-only, which means the pipeline must handle Arabic extraction, but the non-English domestic source boost premium applies. Sole Tier 1 for economic statecraft.
- **Extraction note:** Arabic only. Pipeline must support Arabic text extraction.

**Al-Monitor Saudi Desk** | `al-monitor.com` | Type: `regional` / `analytical` | Status: `EXISTING`
- **Structural role:** The only English-language analytical outlet with original sourcing from Riyadh that covers angles domestic Saudi media cannot: normalization debates, MBS succession dynamics, China hedging, Iran rapprochement.
- **Domain coverage:** All five domains
- **Reasoning:** Al-Monitor fills the structural gap created by Saudi Arabia's total absence of independent domestic media. It is the closest thing to an independent Saudi policy analysis source -- Washington-based, with original Saudi sourcing. For the pipeline, it is the primary source of interpretive analysis that goes beyond official framing. Tier 1 because it is structurally irreplaceable: no other source combines English accessibility, original Riyadh sourcing, and editorial independence on Saudi affairs.
- **Extraction note:** Partial paywall. Diffbot may not extract all articles. Headlines and ledes are typically accessible.

---

### Tier 2 -- `$boost=2`

**Saudi Press Agency (SPA)** | `spa.gov.sa` | Type: `government_aligned` | Status: `EXISTING` -- **LAYER 2 MIGRATION**
- **Structural role:** The definitive signal of Saudi government posture. Royal decrees, Council of Ministers decisions, official diplomatic statements, and defense agreements all flow through SPA first.
- **Domain coverage:** All five domains (official source)
- **Reasoning:** Government sources = Layer 2 migration at Tier 2. Primary fetch via Layer 2 direct polling. Goggle boost at Tier 2 as belt-and-suspenders fallback. SPA is not journalism -- it is the official record of Saudi state action. The pipeline needs it for what it is: primary source material for government decisions and diplomatic positions. Tier 2 rather than Tier 1 because Layer 2 direct polling is the primary ingestion path; Goggle boost is fallback.

**Ministry of Foreign Affairs** | `mfa.gov.sa` | Type: `government_aligned` | Status: `NEW (from sa.yaml)` -- **LAYER 2 MIGRATION**
- **Structural role:** Official diplomatic communications, bilateral meeting readouts, treaty announcements, and Saudi positions on multilateral forums.
- **Domain coverage:** Diplomatic alignment, Institutional engagement
- **Reasoning:** Layer 2 migration at Tier 2. MFA statements are the authoritative source for Saudi diplomatic posture -- when Prince Faisal bin Farhan makes a statement, it appears here first. Goggle boost as fallback for Brave discovery.

**Al-Riyadh** | `alriyadh.com` | Type: `paper_of_record` | Status: `EXISTING`
- **Structural role:** Long-running Arabic daily based in the capital. Reflects the Riyadh establishment perspective. Covers Shura Council proceedings, ministerial appointments, and domestic governance.
- **Domain coverage:** Domestic constraints, Diplomatic alignment, Institutional engagement
- **Reasoning:** Al-Riyadh fills a structural role that Arab News and Asharq Al-Awsat do not: capital-city establishment perspective on domestic governance. Shura Council coverage is thin across all Saudi media, but Al-Riyadh provides the most consistent reporting. Arabic-only; non-English domestic source boost premium applies. Tier 2 because its coverage overlaps substantially with Arab News on diplomacy, but its Riyadh-establishment domestic lens is unique.
- **Extraction note:** Arabic only.

**Okaz / Saudi Gazette** | `okaz.com.sa` / `saudigazette.com.sa` | Type: `paper_of_record` | Status: `EXISTING`
- **Structural role:** Hejaz/western region perspective (Jeddah-based). Okaz (Arabic) and its English sister Saudi Gazette represent subtle editorial differences from Riyadh-based papers that can signal regional dynamics.
- **Domain coverage:** Diplomatic alignment, Domestic constraints
- **Reasoning:** In a state-managed media environment, regional variation between Riyadh-based and Jeddah-based papers is one of the few available signals of internal differentiation. Okaz/Saudi Gazette provides the Hejaz angle -- different emphasis on Hajj governance, Red Sea economic zone, and western region development. Tier 2 for this structural differentiation role. Both domains should be boosted.
- **Extraction note:** Okaz is Arabic-only; Saudi Gazette is English.

**Sabq** | `sabq.org` | Type: `paper_of_record` / `digital_native` | Status: `EXISTING`
- **Structural role:** Saudi Arabia's most-visited digital news platform. High-speed breaking news with massive domestic readership. Indicator of what narratives gain traction with the Saudi public.
- **Domain coverage:** Domestic constraints, Diplomatic alignment
- **Reasoning:** Sabq is the closest thing Saudi Arabia has to a mass-audience digital-native outlet. Its editorial choices reflect what the government believes resonates with the Saudi public -- a distinct signal from what appears in the elite-oriented broadsheets. Arabic-only; non-English domestic source boost premium applies. Tier 2 because its speed and domestic reach make it valuable for catching breaking Saudi stories, but its analytical depth is lower than the Tier 1 sources.
- **Extraction note:** Arabic only.

**Al Arabiya** | `alarabiya.net` | Type: `regional` | Status: `EXISTING`
- **Structural role:** Saudi-owned pan-Arab broadcast network (MBC Group). Saudi Arabia's answer to Al Jazeera. English edition provides pipeline-friendly coverage of Saudi foreign policy, GCC dynamics, Iran tensions, and regional security.
- **Domain coverage:** Diplomatic alignment, Security & defense, Institutional engagement
- **Reasoning:** Al Arabiya is the broadcast complement to Asharq Al-Awsat's print coverage. Its editorial line reliably reflects Saudi strategic consensus on regional issues, particularly Iran, Yemen, and GCC dynamics. English edition makes it fully extractable. Tier 2 rather than Tier 1 because it overlaps substantially with Asharq Al-Awsat on regional coverage, and its broadcast-first model means web content is sometimes thinner than print equivalents.

**Argaam** | `argaam.com` | Type: `business_financial` | Status: `EXISTING`
- **Structural role:** Real-time Saudi financial market data, IPO tracking, Tadawul analysis, and corporate news. Captures economic statecraft signals that newspapers cover only retrospectively.
- **Domain coverage:** Economic statecraft
- **Reasoning:** Argaam fills the real-time financial data niche that Al-Eqtisadiah's daily newspaper format cannot. PIF investment moves, Aramco quarterly results, and Tadawul fluctuations appear on Argaam first. Single-domain (economic statecraft) but uniquely time-sensitive within it. English section available. Tier 2 because it complements Al-Eqtisadiah (Tier 1) with speed rather than depth.

**Gulf Research Center (GRC)** | `grc.net` | Type: `political_specialist` / `think_tank` | Status: `EXISTING`
- **Structural role:** Independent research center based in Jeddah producing analysis on Saudi foreign policy drivers, strategic autonomy, and Gulf security architecture.
- **Domain coverage:** Diplomatic alignment, Security & defense, Economic statecraft
- **Reasoning:** Think tanks earn boost through depth, not speed. GRC is the only Jeddah-based think tank on the list and its publications signal elite Saudi policy debates that do not surface in state-aligned media. Its location inside Saudi Arabia gives it access to Saudi policy circles that international think tanks lack. Tier 2 for analytical depth on Saudi strategic posture.

---

### Tier 3 -- `$boost=1`

**Chatham House MENA Programme** | `chathamhouse.org` | Type: `political_specialist` / `think_tank` | Status: `EXISTING`
- **Structural role:** Authoritative international think tank analysis on Saudi multipolarity strategy, OPEC+ dynamics, and Saudi institutional engagement. Recent 2025 report on Saudi management of multipolarity is directly pipeline-relevant.
- **Domain coverage:** Diplomatic alignment, Institutional engagement
- **Reasoning:** Think tanks = depth not speed. Chatham House provides the structural interpretive framework for understanding Saudi foreign policy evolution. Not Saudi-specific (covers all of MENA), so Tier 3. But when it publishes Saudi analysis, the quality and sourcing are first-rate. Domain is broad (chathamhouse.org covers all regions) -- boost benefits Saudi queries but may also surface non-Saudi results.

**CSIS Middle East Program** | `csis.org` | Type: `political_specialist` / `think_tank` | Status: `EXISTING`
- **Structural role:** Washington-based think tank covering Saudi defense modernization, military spending trends, US-Saudi security relationship, and strategic vision. Quantitative defense analysis.
- **Domain coverage:** Security & defense, Diplomatic alignment, Economic statecraft
- **Reasoning:** CSIS fills the defense-analytical gap that is the most critical structural weakness in Saudi media coverage. Saudi Arabia has no specialist defense press; CSIS provides the closest equivalent for tracking SAMI progress, defense procurement, and US-Saudi security cooperation. Tier 3 because the domain is broad (csis.org covers all regions) and publication frequency on Saudi-specific topics is irregular.

**Al-Watan** | `alwatan.com.sa` | Type: `political_specialist` | Status: `EXISTING`
- **Structural role:** Historically the most liberal Saudi newspaper. Under Jamal Khashoggi's former editorship, it pushed boundaries on women's rights and religious reform. Still occasionally surfaces internal debates that other outlets avoid.
- **Domain coverage:** Domestic constraints, Institutional engagement
- **Reasoning:** In a media ecosystem with no independent press, Al-Watan is the closest thing to an internal reformist voice. Its willingness to occasionally surface debates on social reform and religious authority makes it a valuable domestic-constraints signal. Arabic-only; non-English boost premium applies. Tier 3 rather than Tier 2 because its reformist edge has dulled since Khashoggi's departure and its current output frequently overlaps with other state-aligned dailies.
- **Extraction note:** Arabic only.

**Maaal** | `maaal.com` | Type: `business_financial` | Status: `EXISTING`
- **Structural role:** Independent business news portal covering Saudi business, finance, and economic policy. Complements Argaam with more narrative business journalism and SME-sector coverage.
- **Domain coverage:** Economic statecraft
- **Reasoning:** Third business source after Al-Eqtisadiah (Tier 1) and Argaam (Tier 2). Redundancy reduces boost. Maaal's SME-sector and narrative business journalism niche is genuinely differentiated from Argaam's market-data focus and Al-Eqtisadiah's macro policy coverage. Tier 3 because the economic statecraft domain is already well-served by two higher-tier sources.

**Middle East Eye** | `middleeasteye.net` | Type: `regional` / `investigative` | Status: `EXISTING`
- **Structural role:** Independent English-language outlet that publishes investigative pieces on Saudi military operations, human rights, and diplomatic maneuvering that domestic media will not cover. Blocked inside Saudi Arabia.
- **Domain coverage:** Security & defense, Domestic constraints, Diplomatic alignment
- **Reasoning:** MEE fills the critical structural role of adversarial/independent coverage of Saudi affairs -- the domestic diaspora-critical voice that the curation map correctly identifies as absent from inside the kingdom. Its investigative reporting on Khashoggi aftermath, Saudi military operations in Yemen, and MBS consolidation provides counter-narratives essential for analytical balance. Tier 3 rather than Tier 2 because its editorial orientation is consistently critical of Saudi policy, which introduces systematic framing bias, and the pipeline's interpretive context must calibrate accordingly. Blocked inside KSA but not blocked by Anthropic's crawler.

---

### Neutral -- no Goggle rule

**Al Jazeera Arabic/English** | `aljazeera.com` | Type: excluded -> `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Curation exclusion cited Qatar-owned adversarial editorial line toward Riyadh. Correct assessment, but under the Goggle model, exclusions default to Neutral not Discard. Al Jazeera has the largest Arabic-language news audience globally and its Saudi coverage -- while adversarial -- surfaces stories that Saudi domestic media suppresses. The pipeline benefits from seeing Al Jazeera results at organic ranking for specific queries (e.g., Yemen conflict, Saudi-Qatar relations). Interpretive context handles the bias. No reason to actively discard the largest Arabic news operation.

**Iran International** | `iranintl.com` | Type: excluded -> `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Saudi-funded Farsi/English channel focused on Iran. Tangentially relevant to Saudi-Iran dynamics but not a Saudi posture source. Under Goggle model, leave at organic ranking -- may surface for Saudi-Iran normalization queries and provide the Saudi-funded perspective on Iranian affairs. No reason to boost or discard.

**Al-Madina** | `al-madina.com` | Type: excluded -> `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Arabic daily that the curation map correctly identifies as duplicating Al-Riyadh and Okaz coverage. Under Goggle model, no reason to actively discard -- it may surface organically for Medina-region-specific queries. Redundancy with boosted sources means organic ranking will naturally suppress it.

**ALQST** | `alqst.org` | Type: excluded -> `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Diaspora human rights monitoring organization, not a news outlet. Curation exclusion was reasonable under hard-filter model. Under Goggle model, leave at organic ranking -- ALQST reports occasionally surface in Brave for Saudi human rights queries and provide data points unavailable elsewhere. Not a news source, so no boost, but not noise either.

**Reuters** | `reuters.com` | Type: `wire` | Status: `NEUTRAL` -- **BLOCKED BY ANTHROPIC CRAWLER**
- **Why neutral:** Wire services are not boosted in the Goggle -- wire copy is available organically. **reuters.com is blocked by Anthropic's crawler** (robots.txt denial), which means extraction via pipeline tools will fail even if Brave surfaces it. Brave can still discover Reuters results for ranking signal, but full-text extraction is unreliable. AP News (`apnews.com`) is the unblocked wire alternative.

**AP News** | `apnews.com` | Type: `wire` | Status: `NEUTRAL`
- **Why neutral:** Wire service at organic ranking. Not boosted because wire copy duplicates across outlets. Available as an extraction-reliable wire source since Reuters is blocked.

---

### Discard -- `$discard`

**Middle East Monitor (MEMO)** | `middleeastmonitor.com` | Status: `NEW DISCARD`
- **Discard reasoning:** London-based outlet with documented editorial alignment to the Muslim Brotherhood and Qatar-adjacent funding. While it covers Saudi affairs, its systematic ideological framing would inject consistent bias that is harder to calibrate than Al Jazeera's (which has institutional credibility despite bias). Would actively displace higher-signal sources from top results without adding structural value not already provided by MEE and Al Jazeera at organic ranking.

**Rai al-Youm** | `raialyoum.com` | Status: `NEW DISCARD`
- **Discard reasoning:** London-based pan-Arab opinion platform run by former Al-Quds Al-Arabi editor Abdel Bari Atwan. Primarily commentary, not reporting. Consistently adversarial to Saudi and Gulf governments. Would inject opinion noise into results without adding investigative or analytical value not already provided by MEE (Tier 3) or Al Jazeera (Neutral).

**Saudi Leaks** | `saudi-leaks.com` | Status: `NEW DISCARD`
- **Discard reasoning:** Unattributed opposition website publishing leaked documents and allegations. No editorial accountability, no verifiable sourcing chain, and content authenticity is unverifiable. Would inject unverified claims that could contaminate the pipeline's event extraction. Genuine leaked material, when significant, is typically reported by MEE or Al-Monitor with editorial verification.

---

## STRUCTURAL COVERAGE CHECK

| Structural Role | Source(s) | Tier | Notes |
|---|---|---|---|
| Government signaling channel | SPA, Arab News | T2, T1 | SPA is the official record; Arab News is the preferred English-language framing outlet. Both reflect government intent -- SPA for decrees, Arab News for narrative |
| Opposition/critical voice | Middle East Eye, Al-Monitor | T3, T1 | No domestic opposition press exists. MEE (external investigative) and Al-Monitor (analytical independence) fill this gap. Al Jazeera at Neutral provides additional adversarial coverage |
| Defence/security specialist | CSIS, Asharq Al-Awsat | T3, T1 | No Saudi defence press exists. CSIS provides quantitative defence analysis; Asharq Al-Awsat covers regional security dynamics. SPA communiques (Layer 2) are the only source for Saudi military operational statements |
| Policy-elite discourse | GRC, Chatham House | T2, T3 | GRC for internal Saudi elite debates; Chatham House for how Saudi strategy is interpreted by the international policy community |
| Domestic-language depth | Al-Eqtisadiah, Al-Riyadh, Sabq, Al-Watan, Okaz, Asharq Al-Awsat | T1-T3 | Arabic-language sources are essential for capturing domestic framing that English outlets sanitize for international audiences. Non-English boost premium applied |
| Official government source | SPA, MFA | T2, T2 | **LAYER 2 MIGRATION** -- primary fetch via direct polling. Goggle boost as fallback. Includes spa.gov.sa and mfa.gov.sa |
| Analytical/think tank depth | GRC, Chatham House, CSIS, Al-Monitor | T2, T3, T3, T1 | Four-source analytical bench covering Saudi strategic posture (GRC), multipolarity (Chatham House), defence (CSIS), and policy analysis (Al-Monitor) |
| Wire service (local bureau) | Reuters, AP News | Neutral | Not boosted. Reuters is blocked by Anthropic crawler. AP News is the extraction-reliable wire alternative |
| Economic statecraft specialist | Al-Eqtisadiah, Argaam, Maaal | T1, T2, T3 | Three-source economic bench covering macro policy (Al-Eqtisadiah), real-time markets (Argaam), and SME/narrative business (Maaal) |
| Regional differentiation | Al-Riyadh (capital), Okaz/Saudi Gazette (Hejaz), Al-Watan (reformist) | T2, T2, T3 | In a state-managed media environment, regional and editorial variation between outlets is the primary available signal for internal differentiation |

**Gaps identified:**
1. **Defence procurement and military operations** remain a critical structural blind spot. Saudi Arabia has no specialist defence press, no SAMI transparency mechanism, and military operations (Yemen, regional deployments) are reported only through SPA communiques. CSIS and international defence publications (Jane's, Defense News) provide partial coverage but are not Saudi-specific enough to boost. Layer 2 polling of SPA bulletins is the best available mitigation.
2. **Royal succession dynamics** are structurally opaque. No Saudi source -- domestic or international -- has reliable sourcing on internal Al Saud family politics. Al-Monitor and Chatham House provide the best analytical inference, but this is a permanent blind spot in the absence of leaked diplomatic cables or insider accounts.
3. **Shura Council proceedings** receive minimal detailed coverage across all Saudi media. No equivalent of parliamentary reporting exists. Al-Riyadh provides the most consistent coverage but it is thin. This limits the pipeline's ability to track legislative constraints on executive action.
4. **Vision 2030 implementation gaps** -- mega-project delays, FDI shortfalls, and fiscal pressures -- are systematically underreported in state-aligned media. IMF Article IV reports (Layer 2), Al-Monitor analysis, and international financial press provide the only counter-signal.

---

## REDUNDANCY RESOLUTION

**Broadsheet cluster: Arab News + Asharq Al-Awsat + Al-Riyadh + Okaz/Saudi Gazette + Sabq**
Five state-aligned news outlets is typical for Saudi Arabia's media structure but requires tier differentiation. Resolved by structural role: Arab News (Tier 1, English-language international interface), Asharq Al-Awsat (Tier 1, Arabic pan-Arab strategic consensus), Al-Riyadh (Tier 2, capital establishment + Shura Council), Okaz/Saudi Gazette (Tier 2, Hejaz regional differentiation), Sabq (Tier 2, digital-native mass audience signal). The top two are irreplaceable; the bottom three earn Tier 2 for regional and audience differentiation within the state-aligned ecosystem.

**Business/financial cluster: Al-Eqtisadiah + Argaam + Maaal**
Three economic statecraft sources. Al-Eqtisadiah leads (Tier 1) as the only dedicated economic daily with the deepest Vision 2030 and PIF coverage. Argaam (Tier 2) provides real-time market data that a daily newspaper format cannot. Maaal drops to Tier 3 -- redundant with both higher-tier sources, though its SME-sector niche is genuinely differentiated. Redundancy reduces boost.

**Think tank cluster: GRC + Chatham House + CSIS**
Three think tanks with distinct niches. GRC (Tier 2, Saudi-based, elite policy debates), Chatham House (Tier 3, multipolarity and institutional engagement), CSIS (Tier 3, defence and security quantitative analysis). No redundancy -- each covers different domains from different geographic perspectives. GRC earns the highest boost for its location advantage inside Saudi Arabia.

**Critical/independent cluster: Al-Monitor + MEE + Al Jazeera**
Three external sources providing coverage domestic media cannot. Al-Monitor (Tier 1, analytical independence with original Riyadh sourcing), MEE (Tier 3, investigative/adversarial), Al Jazeera (Neutral, adversarial but high-audience). Differentiated by editorial approach: Al-Monitor is analytical, MEE is investigative, Al Jazeera is broadcast-adversarial. No true redundancy.

---

## QUERY CONFIGURATION

```
country: SA
search_lang: ar
freshness: pw
```

**Multi-language notes:** Saudi Arabia's domestic media operates primarily in Arabic, but a significant portion of policy-relevant output is published in English (Arab News, English editions of Asharq Al-Awsat and Al Arabiya, Al-Monitor, think tank publications). The `languages.metadata: en` configuration in sa.yaml is correct. Queries should run primarily in Arabic for domestic signal; a secondary English query cycle captures Al-Monitor, think tank analysis, and English editions of Saudi outlets. The Goggle boost for Arabic-only sources (Al-Eqtisadiah, Al-Riyadh, Sabq, Okaz, Al-Watan) ensures these are not drowned out by English-language results.

**Localized query vocabulary validation:**

The curation prompt's vocabulary is strong across all five domains. Notes:

- **Domain 1 (Diplomatic):** All terms valid. `ta'addudiyyat al-aqtab` (multipolarity) is increasingly relevant as Saudi BRICS membership deepens. Add `"Mohammed bin Salman diplomacy"` and `"Faisal bin Farhan"` as leader-specific English patterns. Add `"تقارب سعودي إيراني"` (Saudi-Iranian rapprochement) -- the dominant diplomatic frame since the 2023 Beijing-brokered deal. Add `"اتفاقيات أبراهام"` (Abraham Accords) for normalization tracking.
- **Domain 2 (Security):** Solid list. `tawtin al-sina'a al-difa'iyya` (defense localization) is the key Vision 2030 defense term. Add `"SAMI"` (Saudi Arabian Military Industries) and `"الصناعات العسكرية السعودية"` for defense procurement tracking. Add `"خالد بن سلمان"` (Khalid bin Salman) as the defense minister pattern. Add `"الحوثيين"` (Houthis) and `"أمن البحر الأحمر"` (Red Sea security) -- dominant security frames since late 2023.
- **Domain 3 (Economic):** Excellent. `ru'ya 2030` is the anchor term. Add `"نيوم"` (NEOM) and `"ذا لاين"` (The Line) for megaproject tracking. Add `"أرامكو طرح"` (Aramco offering/IPO) and `"تداول"` (Tadawul) for capital markets. Add `"الهيدروجين الأخضر"` (green hydrogen) -- increasingly central to Saudi energy transition narrative. `"PIF"` is used as-is in Arabic press and should be included alongside the Arabic full form.
- **Domain 4 (Institutional):** Valid. `BRICS` and `OPEC+` are used as-is in Arabic press -- correct. Add `"مجموعة العشرين"` (G20) -- Saudi Arabia hosted in 2020 and remains active. `"مجلس الشورى"` is correct but may need pairing with specific committee names for deeper queries. Add `"منظمة شنغهاي للتعاون"` (Shanghai Cooperation Organisation) -- Saudi Arabia gained dialogue partner status.
- **Domain 5 (Domestic):** Strong. Add `"هيئة الترفيه"` (General Entertainment Authority) -- key signal for social liberalization pace. Add `"توظيف المرأة"` (women's employment) and `"نطاقات"` (Nitaqat -- Saudization quotas system). `"ولي العهد"` (Crown Prince) is the essential domestic-power term. Add `"التحول الوطني"` (National Transformation) as the broader reform-program frame.

**Stale/problematic terms:** `hay'at al-amr bil-ma'ruf` (religious police/CPVPV) has declining relevance as the Commission has been dramatically curtailed since 2016, but remains a valid search term for tracking the residual tension between religious establishment and modernization.

**Suggested topic query patterns:**

1. `محمد بن سلمان رؤية 2030 تنويع اقتصادي` -- MBS Vision 2030 economic diversification
2. `السعودية إيران تطبيع بكين` -- Saudi-Iran normalization / Beijing deal
3. `صندوق الاستثمارات العامة استثمار خارجي` -- PIF foreign investment moves
4. `خالد بن سلمان وزارة الدفاع توطين` -- KBS defense ministry localization
5. `نيوم مشاريع تأخير تمويل` -- NEOM project delays and financing
6. `السعودية بريكس أوبك تعددية` -- Saudi BRICS/OPEC+ multipolarity
7. `أمن البحر الأحمر الحوثيين` -- Red Sea security / Houthi dynamics

---

## GOGGLE FILE

```goggle
! name: MPM Saudi Arabia
! description: MPM pipeline source prioritization for Saudi Arabia -- boosts high-signal sources, discards noise
! public: false
! author: MPM Pipeline

! --- Tier 1: Essential (boost=3) ---
$boost=3,site=arabnews.com
$boost=3,site=aawsat.com
$boost=3,site=aleqt.com
$boost=3,site=al-monitor.com

! --- Tier 2: Important (boost=2) ---
$boost=2,site=spa.gov.sa
$boost=2,site=mfa.gov.sa
$boost=2,site=alriyadh.com
$boost=2,site=okaz.com.sa
$boost=2,site=saudigazette.com.sa
$boost=2,site=sabq.org
$boost=2,site=alarabiya.net
$boost=2,site=argaam.com
$boost=2,site=grc.net

! --- Tier 3: Supplementary (boost=1) ---
$boost=1,site=chathamhouse.org
$boost=1,site=csis.org
$boost=1,site=alwatan.com.sa
$boost=1,site=maaal.com
$boost=1,site=middleeasteye.net

! --- Discard: Noise ---
$discard,site=middleeastmonitor.com
$discard,site=raialyoum.com
$discard,site=saudi-leaks.com
```

---

## INTERPRETIVE CONTEXT FOR DOSSIER

### Tier 1 Sources

> Articles from **Arab News** about any domain should be interpreted as the Saudi government's preferred English-language framing for international audiences -- its SRMG ownership (linked to the royal family) and close alignment with Vision 2030 messaging mean its coverage directly reflects what MBS's communication apparatus wants the world to see. What Arab News emphasizes signals government priorities; what it omits signals sensitivity. It is not independent journalism but it is the most reliable signal of official Saudi posture in English.

> Articles from **Asharq Al-Awsat** about regional security and diplomacy should be interpreted as reflecting the Saudi strategic consensus among Arabic-language decision-makers -- its pan-Arab reach (printed in 14 cities) and royal family ownership mean its editorial line on Iran, Yemen, Syria, and GCC dynamics is the closest available proxy for how Saudi strategic thinking is communicated to the Arab world. When Asharq Al-Awsat's framing shifts on a regional issue, it signals genuine policy movement rather than journalistic independence.

> Articles from **Al-Eqtisadiah** about economic policy and Vision 2030 implementation should be interpreted as authoritative reporting filtered through government-aligned framing -- as the kingdom's only dedicated economic daily, it has unmatched granularity on PIF investments, privatization timelines, and non-oil revenue metrics, but it will systematically underreport implementation failures, fiscal pressures, and project delays. Cross-reference with Al-Monitor and international financial press for counter-signal.

> Articles from **Al-Monitor** about Saudi policy should be interpreted as the most analytically independent English-language source with original Riyadh sourcing -- its Washington base and editorial independence allow it to cover succession dynamics, normalization debates, and China-hedging strategies that no Saudi domestic outlet will touch. Its analytical framing may reflect Washington policy community assumptions, but its Saudi-specific sourcing is deeper than any other English-language outlet.

### Tier 2 Sources

> Articles from **SPA** should be interpreted as official government communications -- not journalism but primary source material. Royal decrees, Council of Ministers decisions, and diplomatic statements from SPA represent the Saudi government's chosen public position. The analytical value lies in timing (what is announced when), emphasis (what receives detailed treatment), and omission (what is absent from the official record).

> Articles from **MFA** should be interpreted as official diplomatic posture statements -- Prince Faisal bin Farhan's communications and ministry readouts represent Saudi Arabia's formal diplomatic positions, which may differ from actual strategic calculations. Cross-reference with Al-Monitor analysis and think tank assessments for the gap between stated and actual positions.

> Articles from **Al-Riyadh** about domestic governance and Shura Council should be interpreted as the Riyadh establishment perspective -- its capital-city base and government alignment mean it reflects what the central government apparatus considers important for domestic consumption. Subtle differences in framing between Al-Riyadh and Jeddah-based Okaz can signal regional dynamics within the kingdom.

> Articles from **Okaz/Saudi Gazette** about domestic affairs should be interpreted through their Hejaz/western region lens -- Jeddah-based, these outlets reflect the commercial and cosmopolitan perspective of the Hejaz, which may differ from Riyadh establishment views on social reform pace, economic development priorities, and religious authority. Saudi Gazette (English) is more accessible but Okaz (Arabic) carries more domestic weight.

> Articles from **Sabq** about breaking news should be interpreted as the Saudi digital mass-audience signal -- what Sabq leads with reflects what the government believes resonates with ordinary Saudis, which may differ from what Arab News frames for international elites or what Al-Riyadh presents for the establishment. Its speed makes it valuable for catching breaking stories, but its analytical depth is minimal.

> Articles from **Al Arabiya** about regional affairs should be interpreted as the Saudi-aligned broadcast perspective on Middle East dynamics -- owned by MBC Group (Saudi-linked), its editorial line on Iran, Yemen, and Gulf security reliably reflects Saudi strategic preferences. Its English edition is more accessible than Asharq Al-Awsat's Arabic coverage but provides less analytical depth.

> Articles from **Argaam** about financial markets and corporate activity should be interpreted as real-time market intelligence rather than analytical journalism -- its data-first approach captures PIF moves, Tadawul fluctuations, and corporate announcements faster than Al-Eqtisadiah's daily format, but without the contextual analysis. Treat as a signal detector, not an analytical source.

> Articles from **GRC** about Saudi foreign policy and Gulf security should be interpreted as elite Saudi policy-community analysis -- its Jeddah base gives it access to Saudi policy circles that international think tanks lack, making its publications a proxy for debates within the Saudi foreign policy establishment. Its analysis tends to be more sympathetic to Saudi strategic rationale than international think tanks, which should be calibrated accordingly.
# AUDIT SUMMARY: SOUTH KOREA

**Sources assessed:** 18 recommended + 5 excluded + 3 newly identified = 26 total
**Tier 1 (boost=3):** 4 sources
**Tier 2 (boost=2):** 9 sources
**Tier 3 (boost=1):** 5 sources
**Neutral (no rule):** 6 sources
**Discard:** 2 sources
**Overall assessment:** The curation prompt produced a strong whitelist with unusually good English-language coverage for an Asian middle power — South Korea's major outlets all publish substantive English editions, which is a structural advantage. Key changes: (1) resolved redundancy among four English-language dailies by differentiating editorial roles and tiers; (2) promoted government official sources for Layer 2 migration; (3) boosted Korean-language-primary sources (Chosun Ilbo) with non-English domestic premium despite crawler block; (4) flagged `yna.co.kr` and `chosun.com` as blocked by Anthropic's crawler, which affects extraction even though Brave can still discover them; (5) added missing structural roles for presidential office and National Assembly; (6) differentiated think tanks by independence vs. government affiliation.

---

## BOOST ASSIGNMENTS

### Tier 1 — `$boost=3`

**Yonhap News Agency** | `en.yna.co.kr` / `www.yna.co.kr` | Type: `wire_service` | Status: `EXISTING`
- **Structural role:** National wire service. The single highest-volume, lowest-latency ingestion point for Korean political, diplomatic, and economic news. Carries verbatim government statements, National Assembly proceedings, and official data releases.
- **Domain coverage:** Diplomatic alignment; Security & defense; Economic statecraft; Institutional engagement; Domestic constraints
- **Reasoning:** Yonhap is structurally irreplaceable — it is the upstream source for most Korean news. Every other domestic outlet republishes or reacts to Yonhap copy. The pipeline needs Yonhap surfacing first for speed. English edition (`en.yna.co.kr`) provides accessible ingestion; Korean edition (`www.yna.co.kr`) provides deeper domestic signals.
- **Extraction note:** **`yna.co.kr` is blocked by Anthropic's crawler** (`robots.txt` denial). Brave can still surface Yonhap URLs for ranking/discovery, but full-text extraction via pipeline tools will fail. Consider RSS ingestion (`en.yna.co.kr/RSS/news.xml`) as primary extraction path, bypassing web crawling.

**The Korea Herald** | `www.koreaherald.com` | Type: `paper_of_record` | Status: `EXISTING`
- **Structural role:** South Korea's largest English-language daily and sole Asia News Network member. Functions as the primary English-language agenda-setter — frequently the first English outlet to carry translated Blue House/government statements.
- **Domain coverage:** Diplomatic alignment; Economic statecraft; Domestic constraints
- **Reasoning:** The Korea Herald is the closest thing to a default English-language source for South Korean political news. Its centrist-conservative positioning and Herald Corporation ownership provide establishment-adjacent but editorially independent coverage. Free, no paywall, RSS available — maximum extractability. The pipeline's English-language entry point for South Korea.

**Korea Pro** | `koreapro.org` | Type: `political_specialist` / `analytical` | Status: `EXISTING`
- **Structural role:** Purpose-built analytical journalism for professional analysts. Fills the critical gap between wire copy and think-tank papers. Sibling to NK News, giving it unique editorial infrastructure for peninsula-focused analysis.
- **Domain coverage:** Diplomatic alignment; Security & defense; Economic statecraft; Domestic constraints
- **Reasoning:** Korea Pro covers all four non-institutional domains with analyst-grade depth. Its coverage of the post-martial-law political landscape and the Lee Jae-myung transition has been exceptionally detailed — exactly the kind of structural analysis the pipeline needs for dossier synthesis. Tier 1 because no other source combines this breadth with this analytical depth for South Korea specifically.
- **Extraction note:** Freemium model — limited free articles per month. Institutional subscription recommended for full pipeline access.

**Chosun Ilbo** | `www.chosun.com` / `english.chosun.com` | Type: `paper_of_record` | Status: `EXISTING`
- **Structural role:** Highest-circulation Korean newspaper. The conservative establishment bellwether — when Chosun Ilbo shifts tone on the US alliance, North Korea, or China engagement, it signals a broader elite realignment. Functions as the domestic-language paper of record.
- **Domain coverage:** Diplomatic alignment; Security & defense; Domestic constraints
- **Reasoning:** Non-English domestic premium applies. Chosun Ilbo is the single most important Korean-language newspaper for detecting conservative establishment positioning. Its editorial line is a proxy for People Power Party / conservative bloc thinking, which is essential for triangulating government posture under the progressive Lee Jae-myung administration. English edition is thin — Korean-language ingestion is where the signal lives.
- **Extraction note:** **`chosun.com` is blocked by Anthropic's crawler** (`robots.txt` denial). Brave can still surface URLs for discovery. Machine translation of Korean originals recommended. English edition (`english.chosun.com`) may have separate `robots.txt` — test independently.

---

### Tier 2 — `$boost=2`

**Korea JoongAng Daily** | `koreajoongangdaily.joins.com` | Type: `paper_of_record` | Status: `EXISTING`
- **Structural role:** English-language daily of the JoongAng Ilbo / NYT partnership. Provides the conservative establishment perspective with higher editorial standards than other English editions due to NYT affiliation.
- **Domain coverage:** Diplomatic alignment; Security & defense; Economic statecraft; Domestic constraints
- **Reasoning:** Strong across all four non-institutional domains, but redundant with Korea Herald at the English-language daily level and with Chosun Ilbo at the conservative establishment level. The NYT partnership differentiates it on international affairs framing. Tier 2 rather than Tier 1 because the Korea Herald covers the English-language paper-of-record role, and Chosun Ilbo covers the conservative establishment role — JoongAng Daily sits in between without being indispensable in either niche.

**Hankyoreh English** | `english.hani.co.kr` | Type: `opposition_aligned` / `progressive` | Status: `EXISTING`
- **Structural role:** Essential progressive counterweight. The only English-language source providing systematic coverage of inter-Korean engagement advocacy, civil society opposition to defense policies (THAAD, GSOMIA debates), and labor/social movements constraining foreign policy.
- **Domain coverage:** Diplomatic alignment; Security & defense; Domestic constraints
- **Reasoning:** Opposition-aligned sources earn Tier 2 minimum — the pipeline needs to see domestic contestation from both sides. Under the Lee Jae-myung administration, Hankyoreh shifts from opposition voice to government-sympathetic outlet, which is itself a valuable signal: its framing of government initiatives will indicate how the progressive base perceives policy execution. Structurally essential for ideological triangulation against Chosun Ilbo (Tier 1) and JoongAng Daily (Tier 2).

**NK News** | `www.nknews.org` | Type: `security_defense` / `specialist` | Status: `EXISTING`
- **Structural role:** Indispensable specialist source for the DPRK threat environment that drives ROK security posture. NK Pro's satellite imagery analysis, ship tracking, and leadership monitoring provide structured data unavailable elsewhere.
- **Domain coverage:** Security & defense; Diplomatic alignment
- **Reasoning:** Single-domain dominance (security/defense as it relates to the North Korea threat). Changes in North Korean behavior are primary drivers of ROK defense spending, alliance demands, and diplomatic positioning. No overlap with any domestic source — NK News provides the external threat layer. Tier 2 rather than Tier 1 because it covers the threat environment, not ROK policy itself. The pipeline needs NK News for context, not for detecting ROK government actions.
- **Extraction note:** NK News freemium; NK Pro requires institutional subscription.

**38 North** | `www.38north.org` | Type: `security_defense` / `think_tank` | Status: `EXISTING`
- **Structural role:** Gold-standard open-source satellite imagery analysis of DPRK military sites. Stimson Center-backed analytical depth.
- **Domain coverage:** Security & defense; Diplomatic alignment
- **Reasoning:** Think tanks earn boost through depth, not speed. 38 North complements NK News with deeper technical analysis — when 38 North publishes a new assessment of DPRK capability, it directly shapes the analytical frame for ROK defense posture. Tier 2 for analytical depth. Not Tier 1 because publication frequency is lower and it covers the threat environment rather than ROK policy directly. Free and fully extractable.

**Korea Economic Daily (KED Global)** | `www.kedglobal.com` / `www.hankyung.com` | Type: `business_financial` | Status: `EXISTING`
- **Structural role:** South Korea's principal specialized business daily. Best single source for semiconductor supply chain policy, trade negotiations, FTA developments, and chaebol investment decisions with geopolitical implications.
- **Domain coverage:** Economic & technological statecraft
- **Reasoning:** Sole Tier 1 candidate for economic statecraft, but placed at Tier 2 because its domain coverage is single-domain. In a country where semiconductor policy (Samsung/SK Hynix China operations under US export controls, K-CHIPS Act) is a primary geopolitical lever, KED Global's coverage is structurally essential. English edition at `kedglobal.com` is free and extractable. Korean edition (`hankyung.com`) provides deeper domestic business signals.

**Asan Institute for Policy Studies** | `en.asaninst.org` / `asaninst.org` | Type: `think_tank` | Status: `EXISTING`
- **Structural role:** South Korea's most prominent independent think tank. Publishes the Asan Forum (bi-monthly analytical journal) and regular polling on Korean public opinion toward alliances and foreign policy.
- **Domain coverage:** Diplomatic alignment; Security & defense; Institutional engagement
- **Reasoning:** Think tanks earn boost through depth, not speed. Asan's public opinion polling data is uniquely valuable for the "domestic constraints" domain — no other source systematically tracks Korean attitudes toward the US alliance, China, and North Korea engagement. Independent of government (though Hyundai-affiliated founding introduces a chaebol lens). Tier 2 for analytical depth and polling data.

**MOFA / Korea.net** | `www.mofa.go.kr/eng` / `www.korea.net` | Type: `government_official` | Status: `EXISTING` — **LAYER 2 MIGRATION**
- **Structural role:** Primary source for bilateral/multilateral meeting readouts, treaty actions, summit statements, and UN voting explanations. Korea.net aggregates across ministries. Essential ground truth.
- **Domain coverage:** Diplomatic alignment; Institutional engagement (all five domains via official source)
- **Reasoning:** Primary fetch via Layer 2 direct polling. Goggle boost at Tier 2 as belt-and-suspenders fallback. Government press releases occasionally surface in Brave News Search. The kr.yaml already lists `mofa.go.kr` as a Tier 1 government source — in the Goggle model, government official sources sit at Tier 2 boost with Layer 2 as the primary ingestion path.

**Presidential Office** | `president.go.kr` | Type: `government_official` | Status: `NEW` — **LAYER 2 MIGRATION**
- **Structural role:** Official presidential communications, executive orders, summit readouts, and policy announcements. Listed in kr.yaml as Tier 1 government source.
- **Domain coverage:** All five domains (official source)
- **Reasoning:** Primary fetch via Layer 2 direct polling. Goggle boost at Tier 2 as fallback. Under the Lee Jae-myung administration, presidential office communications are the primary signal for foreign policy direction, particularly on inter-Korean engagement and alliance management.

---

### Tier 3 — `$boost=1`

**The Korea Times** | `www.koreatimes.co.kr` | Type: `paper_of_record` | Status: `EXISTING`
- **Structural role:** Third English-language daily. Strong op-ed section featuring Korean academics and retired diplomats — early-signal detector for elite opinion shifts.
- **Domain coverage:** Diplomatic alignment; Domestic constraints; Institutional engagement
- **Reasoning:** Redundancy reduces boost. The Korea Herald (Tier 1) already covers the English-language daily role, and JoongAng Daily (Tier 2) provides the second English perspective. Korea Times' centrist-liberal editorial orientation and engagement-sympathetic framing provide a useful third data point, but it breaks fewer stories than the Herald and has less editorial distinction than JoongAng Daily's NYT partnership. Tier 3 for the op-ed signal and editorial triangulation value. Free and extractable.

**The Diplomat** | `thediplomat.com` | Type: `regional` / `analytical` | Status: `EXISTING`
- **Structural role:** Regional contextualization of ROK actions within Indo-Pacific dynamics. Provides the external perception layer — how ROK posture is read by regional observers.
- **Domain coverage:** Diplomatic alignment; Security & defense; Institutional engagement
- **Reasoning:** Not South Korea-specific (covers all of Indo-Pacific), so Tier 3. But when it publishes South Korea analysis, the regional comparative framing is unique — Quad-adjacent positioning, ASEAN engagement, AUKUS implications. Useful for detecting how Seoul's actions are perceived regionally, which feeds back into ROK calculations.

**IFANS** | `www.ifans.go.kr` | Type: `think_tank` (government-affiliated) | Status: `EXISTING`
- **Structural role:** MOFA's institutional think tank. Publications are the closest available proxy for Foreign Ministry analytical thinking.
- **Domain coverage:** Diplomatic alignment; Institutional engagement; Economic statecraft
- **Reasoning:** Government-affiliated think tanks sit below independent think tanks (Asan, Tier 2) because their analytical independence is constrained. IFANS publications signal how MOFA frames emerging issues — valuable as a leading indicator of official positions, but not as independent analysis. Tier 3 for the government-signaling function. English section available but Korean-language portal navigation may be required.

**KIEP** | `www.kiep.go.kr/eng` | Type: `think_tank` (government-affiliated) | Status: `EXISTING`
- **Structural role:** Government-funded economic policy research institute. Publishes on FTAs, supply chain resilience, economic security frameworks, and ROK positioning in multilateral economic institutions.
- **Domain coverage:** Economic & technological statecraft; Institutional engagement
- **Reasoning:** Same logic as IFANS — government-affiliated, so Tier 3 rather than Tier 2. Policy briefs signal government thinking on economic statecraft before formal announcements (RCEP, CPTPP, IPEF positioning). Complements KED Global's journalistic coverage with the policy-research layer. English publications available.

**Seoul Economic Daily** | `en.sedaily.com` | Type: `business_financial` | Status: `EXISTING`
- **Structural role:** Second major business daily with English edition. Covers industrial policy, trade friction, and technology sector regulation.
- **Domain coverage:** Economic & technological statecraft
- **Reasoning:** Redundancy with KED Global (Tier 2) reduces boost. Seoul Economic Daily is useful for triangulation on economic statecraft signals — particularly semiconductor and battery supply chain developments — but it breaks fewer stories than KED Global and has less editorial distinction. Tier 3 for supplementary economic coverage.

---

### Neutral — no Goggle rule

**KIDA** | `www.kida.re.kr` | Type: `think_tank` (government-affiliated) | Status: `EXISTING → NEUTRAL`
- **Why neutral:** Korean-language dominant with only intermittent English publications. Its MND-affiliated analytical perspective is valuable for defense-autonomy tracking, but the pipeline's ability to systematically ingest KIDA output is limited without robust Korean-language processing. Under the Goggle model, KIDA publications may surface organically for defense-specific queries. If Korean-language ingestion capacity improves, re-evaluate at Tier 3.

**DAPA** | `www.dapa.go.kr/dapa_en` | Type: `government_official` | Status: `EXISTING → NEUTRAL`
- **Why neutral:** Defense procurement agency with English portal, but content is primarily press releases on procurement decisions and arms exports. Signal is real but low-frequency and highly specialized. Under the Goggle model, DAPA pages will surface organically when defense procurement queries run. Layer 2 polling is the appropriate ingestion path — Goggle boost adds little value for such a narrow, low-frequency source.

**Kyunghyang Shinmun** | excluded | Type: `progressive_daily` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Curation exclusion was justified — no English edition, and Hankyoreh English largely captures the progressive editorial space. Under the Goggle model, no reason to actively discard. If Korean-language ingestion capacity grows, Kyunghyang adds progressive-spectrum granularity beyond Hankyoreh. May surface organically for Korean-language queries.

**Dong-a Ilbo** | excluded | Type: `conservative_daily` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Third member of the "Chojoongdong" conservative bloc. Signal is substantially redundant with Chosun Ilbo (Tier 1) and JoongAng Daily (Tier 2). Minimal English-language output. Under the Goggle model, organic ranking is appropriate — no need to boost, no need to discard. May surface for specific conservative-establishment queries.

**MBC / KBS / SBS** | excluded | Type: `broadcast` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Television networks' text output is largely derivative of Yonhap wire copy. Broadcast transcripts are harder to ingest programmatically. Under the Goggle model, no reason to actively discard — if a broadcast network breaks a major story (e.g., leaked NIS briefing on KBS), Brave may surface it. Leave at organic ranking.

**Maeil Business Newspaper** | excluded | Type: `business_financial` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Major business daily but signal is largely covered by KED Global (Tier 2) and Seoul Economic Daily (Tier 3) in the English-language space. Korean-only ingestion would add marginal value. Organic ranking is appropriate.

---

### Discard — `$discard`

**Korea Economic Institute of America (KEIA)** | `keia.org` | Status: `NEW DISCARD`
- **Discard reasoning:** US-based institute providing an outside-in perspective on ROK policy. Would inject Washington's framing of South Korean policy into results, displacing indigenous signal sources. The pipeline needs to see how Seoul frames its own actions, not how Washington interprets them. KEIA analysis is useful as background reading but would actively displace domestic and regional sources from Brave results.

**The Korea Observer** | `koreaobserver.com` | Status: `NEW DISCARD`
- **Discard reasoning:** Low-quality English-language aggregator that republishes wire copy and press releases without original reporting or editorial value. Would consume result slots without adding signal. Brave may rank it for English-language Korean news queries due to keyword density — discard prevents displacement of higher-signal sources.

---

## STRUCTURAL COVERAGE CHECK

| Structural Role | Source(s) | Tier | Notes |
|---|---|---|---|
| Government signaling channel | Hankyoreh English (under Lee admin) | T2 | Under progressive Lee Jae-myung presidency, Hankyoreh shifts from opposition to government-sympathetic. Watch for government trial balloons surfacing here first. Chosun Ilbo (T1) fills the conservative opposition signaling role |
| Opposition voice | Chosun Ilbo, Korea JoongAng Daily | T1, T2 | Under Lee administration, the conservative press becomes the opposition signal. Chosun Ilbo editorial line is now the primary indicator of conservative establishment resistance to government initiatives |
| Defence/security specialist | NK News, 38 North | T2, T2 | Peninsula-specific threat environment coverage. No dedicated ROK defence press equivalent — KIDA (Neutral) and DAPA (Neutral) fill the gap via Layer 2 polling |
| Policy-elite discourse | Korea Pro, Asan Institute | T1, T2 | Korea Pro for daily analytical depth; Asan for structural analysis and public opinion polling |
| Domestic-language depth | Chosun Ilbo, Yonhap (Korean edition) | T1, T1 | Non-English domestic premium applied. Korean-language originals are essential for depth on domestic political dynamics, conservative establishment positioning, and progressive blogosphere signals |
| Official government source | MOFA/Korea.net, Presidential Office | T2, T2 | **LAYER 2 MIGRATION** — primary fetch via direct polling. Goggle boost as fallback. kr.yaml already lists both as Tier 1 government sources |
| Analytical/think tank depth | Asan Institute, IFANS, KIEP | T2, T3, T3 | Asan for independent analysis + polling; IFANS for MOFA institutional thinking; KIEP for economic statecraft signaling |
| Economic statecraft specialist | KED Global, Seoul Economic Daily | T2, T3 | Semiconductor supply chain, trade negotiations, chaebol-government dynamics. Two sources for triangulation on economic statecraft |
| Wire service coverage | Reuters, AP News, France24 | Neutral | Per kr.yaml wire configuration. Not boosted in Goggle — wire copy is available organically. Reuters is blocked by Anthropic crawler but Brave can still surface for discovery |

**Gaps identified:**
1. **Progressive domestic political discourse** beyond Hankyoreh English remains underrepresented. Kyunghyang Shinmun (Neutral) has no English edition, and the progressive blogosphere/YouTube ecosystem (51% YouTube news share per Reuters Institute) has no text equivalent in the pipeline. Korean-language ingestion or translation is needed to fully capture civil society constraints on government action.
2. **Defence-industrial signals** from Hanwha Aerospace, Korea Aerospace Industries, and Hyundai Rotem are best tracked through Korean-language corporate disclosures and trade press (Defense Times Korea / Kukbang Ilbo) that lack English editions. DAPA (Neutral) provides official procurement announcements but not the industrial strategy layer.
3. **National Assembly proceedings** lack a dedicated source. Yonhap covers Assembly votes and committee hearings, but no source systematically tracks legislative dynamics (bill status, committee hearings, interpellation sessions) in the way a parliamentary monitoring service would. Layer 2 polling of the National Assembly website (`assembly.go.kr`) should be considered.

---

## REDUNDANCY RESOLUTION

**English-language daily cluster: Korea Herald + JoongAng Daily + Korea Times + Hankyoreh English**
Four English-language dailies covering South Korean politics. Resolved by differentiating editorial roles: Korea Herald (Tier 1, largest English daily, centrist-conservative, agenda-setter), JoongAng Daily (Tier 2, NYT partnership, conservative establishment with higher editorial standards), Hankyoreh English (Tier 2, progressive counterweight, essential for ideological triangulation), Korea Times (Tier 3, op-ed signal and elite opinion detection, least distinctive of the four). The pipeline benefits from ideological plurality — the top three English dailies span the conservative-progressive spectrum.

**Conservative establishment cluster: Chosun Ilbo + JoongAng Daily + (Dong-a Ilbo)**
Three "Chojoongdong" outlets. Chosun Ilbo leads (Tier 1) as highest-circulation Korean newspaper and conservative bellwether — its editorial shifts are signals in themselves. JoongAng Daily (Tier 2) is differentiated by its NYT partnership and English-language accessibility. Dong-a Ilbo drops to Neutral — redundant with both, minimal English output.

**Business press cluster: KED Global + Seoul Economic Daily + (Maeil Business)**
Three business dailies. KED Global leads (Tier 2) due to strongest English edition and deepest semiconductor/supply chain coverage. Seoul Economic Daily (Tier 3) provides triangulation. Maeil Business (Neutral) — redundant, Korean-only.

**North Korea / security specialist cluster: NK News + 38 North**
Both at Tier 2, but with distinct niches. NK News provides daily monitoring (satellite imagery, ship tracking, leadership analysis). 38 North provides periodic deep technical analysis (missile tests, nuclear sites). No redundancy — complementary within the same domain.

**Government-affiliated think tank cluster: IFANS + KIEP + KIDA**
Three government-funded research institutes. IFANS (Tier 3) for MOFA analytical signaling. KIEP (Tier 3) for economic statecraft signaling. KIDA (Neutral) — Korean-language dominant, limited pipeline extractability. Each covers a distinct policy domain, so redundancy is minimal despite shared government affiliation.

---

## QUERY CONFIGURATION

```
country: KR
search_lang: ko
freshness: pw
```

**Multi-language notes:** South Korea's media ecosystem has unusually strong English-language coverage for an Asian middle power. Primary queries should run in Korean for domestic political depth (Chosun Ilbo, Yonhap Korean); secondary English queries will capture Korea Herald, JoongAng Daily, Korea Pro, NK News, 38 North, and international wire coverage. The pipeline's existing `languages.metadata: en` configuration handles this correctly, but Korean-language query cycles are essential for sources where the English edition is thin or nonexistent (Chosun Ilbo, Kyunghyang, defense trade press).

**Localized query vocabulary validation:**

The curation prompt's vocabulary is strong and well-structured. Notes:

- **Domain 1 (Diplomatic):** All terms valid. Add `"이재명 외교"` (Lee Jae-myung diplomacy) and `"한미 정상회담"` (ROK-US summit) as leader-specific patterns. `"인도태평양 전략"` is correct and increasingly relevant as Seoul recalibrates its Indo-Pacific posture under Lee. Consider adding `"한중 수교"` (ROK-China diplomatic normalization anniversary framing) — China relations reframing is a live issue.
- **Domain 2 (Security):** Strong list. Add `"한반도 비핵화"` (Korean Peninsula denuclearization) — the dominant frame for inter-Korean security diplomacy. `"KF-21"` should be added as a romanized term — Korea's indigenous fighter program is a primary defense-autonomy indicator. Add `"핵잠수함"` (nuclear submarine) — the nuclear-powered submarine debate is active. `"워싱턴 선언"` (Washington Declaration) is relevant for extended deterrence discussions.
- **Domain 3 (Economic):** Excellent list. Add `"칩4"` / `"Chip 4"` (Chip 4 alliance framing). `"이차전지"` (secondary battery / EV battery) is critical — battery supply chain is as geopolitically significant as semiconductors for ROK. Add `"IRA 보조금"` (IRA subsidies) for tracking US Inflation Reduction Act impacts on Korean EV/battery manufacturers.
- **Domain 4 (Institutional):** Valid. Add `"IPEF"` (Indo-Pacific Economic Framework) — ROK's multilateral economic engagement. `"MIKTA"` (Mexico-Indonesia-Korea-Turkey-Australia) is still nominally active but declining. Add `"글로벌 중추국가"` (global pivotal state) — the Lee administration's framing of ROK's international role.
- **Domain 5 (Domestic):** Strong. `"탄핵"` (impeachment) remains live — the Yoon Suk Yeol impeachment aftermath continues to shape politics. Add `"비상계엄"` (emergency martial law) — the December 2024 crisis is a defining reference point. Add `"국회 청문회"` (National Assembly hearing) for tracking legislative constraint signals. `"여소야대"` (small ruling party, large opposition) may become relevant if parliamentary dynamics shift.

**Stale/problematic terms:** None are stale. All terms reflect active political dynamics as of March 2026. The martial law crisis and subsequent political realignment have made nearly every term on the list more relevant, not less.

**Suggested topic query patterns:**

1. `이재명 한미동맹 정상회담` — Lee Jae-myung ROK-US alliance summit
2. `반도체 수출통제 삼성 SK하이닉스` — Semiconductor export controls Samsung SK Hynix
3. `전작권 전환 한미연합훈련 2026` — OPCON transfer combined exercises 2026
4. `탈중국 공급망 이차전지` — De-China supply chain EV battery
5. `탄핵 이후 여야 갈등 국회` — Post-impeachment ruling-opposition conflict National Assembly

---

## GOGGLE FILE

```goggle
! name: MPM South Korea
! description: MPM pipeline source prioritization for South Korea — boosts high-signal sources, discards noise
! public: false
! author: MPM Pipeline

! --- Tier 1: Essential (boost=3) ---
$boost=3,site=en.yna.co.kr
$boost=3,site=www.yna.co.kr
$boost=3,site=koreaherald.com
$boost=3,site=koreapro.org
$boost=3,site=chosun.com
$boost=3,site=english.chosun.com

! --- Tier 2: Important (boost=2) ---
$boost=2,site=koreajoongangdaily.joins.com
$boost=2,site=english.hani.co.kr
$boost=2,site=nknews.org
$boost=2,site=38north.org
$boost=2,site=kedglobal.com
$boost=2,site=hankyung.com
$boost=2,site=en.asaninst.org
$boost=2,site=asaninst.org
$boost=2,site=mofa.go.kr
$boost=2,site=korea.net
$boost=2,site=president.go.kr

! --- Tier 3: Supplementary (boost=1) ---
$boost=1,site=koreatimes.co.kr
$boost=1,site=thediplomat.com
$boost=1,site=ifans.go.kr
$boost=1,site=kiep.go.kr
$boost=1,site=en.sedaily.com

! --- Discard: Noise ---
$discard,site=keia.org
$discard,site=koreaobserver.com
```

---

## INTERPRETIVE CONTEXT FOR DOSSIER

### Tier 1 Sources

> Articles from **Yonhap News Agency** about any domain should be interpreted as institutional wire copy with legally mandated impartiality — Yonhap is government-funded but editorially independent by statute. Its reporting represents the factual baseline against which all other sources' framing can be measured. When Yonhap's framing of an event differs from a newspaper's, the newspaper is editorializing.

> Articles from **The Korea Herald** about diplomacy and government policy should be interpreted as centrist-conservative establishment journalism — its Herald Corporation ownership and position as the largest English-language daily mean it reflects mainstream elite thinking. It is not opposition press, but neither is it a government mouthpiece. Its translations of Blue House statements are typically faithful but selection of what to translate reflects editorial judgment about what matters to the English-speaking policy community.

> Articles from **Korea Pro** about South Korean politics and foreign policy should be interpreted as analyst-grade journalism explicitly designed for professional consumers — its non-partisan framing and sibling relationship with NK News give it unusual editorial rigor for a subscription publication. Korea Pro analysis can be treated as a secondary analytical layer alongside think tank output, with the advantage of daily publication frequency.

> Articles from **Chosun Ilbo** about the US alliance, North Korea policy, or China engagement should be interpreted as the conservative establishment bellwether — South Korea's highest-circulation newspaper whose editorial shifts are themselves signals of broader elite realignment. Under the progressive Lee Jae-myung administration, Chosun Ilbo functions as the primary opposition voice. Its hawkishness on North Korea and pro-alliance stance mean it will frame any diplomatic engagement skeptically — this is not noise but a structural signal of conservative resistance that constrains government action.

### Tier 2 Sources

> Articles from **Korea JoongAng Daily** about international affairs and defense should be interpreted as conservative-establishment analysis elevated by its NYT partnership — the partnership imposes editorial standards that make its international coverage more analytically rigorous than other Korean English-language outlets, but its parent JoongAng Ilbo's "Chojoongdong" membership means its domestic political framing leans conservative.

> Articles from **Hankyoreh English** about inter-Korean relations, civil society movements, and defense policy should be interpreted as progressive/center-left journalism that — under the Lee Jae-myung administration — has shifted from opposition voice to government-sympathetic outlet. Its coverage of inter-Korean engagement will be more favorable than conservative outlets, and its framing of defense policies (THAAD, GSOMIA, cost-sharing) will emphasize civil society opposition. This is not bias but a structural signal of progressive base sentiment that enables or constrains government action.

> Articles from **NK News** about North Korean military capabilities, leadership dynamics, or provocations should be interpreted as specialist analytical journalism with the best open-source monitoring infrastructure for DPRK activities — satellite imagery, ship tracking, leadership appearance databases. NK News assessments of North Korean behavior should be treated as the factual baseline for the threat environment driving ROK security decisions.

> Articles from **38 North** about DPRK nuclear/missile capabilities should be interpreted as the gold standard for open-source technical assessment — Stimson Center-backed analysis with deep expertise in satellite imagery interpretation. When 38 North publishes a new capability assessment, it shapes the analytical frame that ROK defense planners and alliance managers operate within.

> Articles from **KED Global** about semiconductor policy, trade negotiations, and chaebol investment decisions should be interpreted as reflecting South Korea's business establishment perspective — its pro-business, free-market conservative orientation means it frames industrial policy and export controls through an investment-climate lens. Negative coverage of government economic intervention does not mean the policy is failing, only that it is unpopular with the chaebol-adjacent business community.

> Articles from **Asan Institute** about alliance attitudes, China perceptions, or public opinion should be interpreted as South Korea's most rigorous independent polling and analysis — centrist-realist positioning with Hyundai-affiliated founding. Asan polling data on Korean public attitudes toward the US alliance, nuclear armament, and China should be treated as the most reliable quantitative indicator of domestic constraint dynamics.

> Articles from **MOFA / Korea.net** and **Presidential Office** should be interpreted as official government communications — not journalism but primary source material. Press releases, readouts, and statements represent the government's chosen public position, which may differ from actual policy implementation or internal deliberations. What the government chooses to publicize (and what it omits) is itself a signal.

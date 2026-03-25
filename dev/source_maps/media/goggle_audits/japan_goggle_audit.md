# AUDIT SUMMARY: JAPAN

**Sources assessed:** 18 recommended + 5 excluded + 4 newly identified = 27 total
**Tier 1 (boost=3):** 4 sources
**Tier 2 (boost=2):** 9 sources
**Tier 3 (boost=1):** 5 sources
**Neutral (no rule):** 6 sources
**Discard:** 3 sources
**Overall assessment:** The curation prompt produced a strong whitelist anchored by Japan's unusually rich English-language media infrastructure — five national dailies with English editions, two domestic wire services, and a public broadcaster with full English output. Key changes: (1) boosted non-English domestic sources (Tokyo Shimbun, Nikkei Japanese) for domestic-language depth premium; (2) migrated government sources (Kantei, MOFA, MOD) to Layer 2 with Tier 2 Goggle fallback; (3) resolved broadsheet redundancy across five national dailies by differentiating editorial-spectrum roles; (4) flagged five blocked domains affecting Japan sources — `asahi.com`, `japan-forward.com`, `sankei.com`, `yomiuri.co.jp`, and `reuters.com` — which constrains extraction even when Brave surfaces them; (5) added missing structural roles for Diet proceedings and Okinawa regional coverage.

---

## BOOST ASSIGNMENTS

### Tier 1 — `$boost=3`

**Kyodo News** | `english.kyodonews.net` / `kyodonews.jp` | Type: `wire_service` | Status: `EXISTING`
- **Structural role:** Japan's primary wire service — nonprofit cooperative owned by member newspapers. Highest-velocity English-language feed on Japanese political events. The domestic equivalent of AP/Reuters.
- **Domain coverage:** Diplomatic alignment, Security & defense, Domestic constraints, Economic & technological statecraft, Institutional engagement
- **Reasoning:** Kyodo is the indispensable baseline wire for Japan coverage. It breaks government policy announcements, Diet proceedings, diplomatic meetings, and SDF deployments faster than any other English-language source. Cooperative ownership insulates it from single-proprietor editorial drift. Free headlines; full articles may require subscription but Brave indexes extensively. Japanese-language parent site (`kyodonews.jp`) adds domestic-language depth. Tier 1 for velocity, breadth, and structural centrality.
- **Extraction note:** English consumer site rebranded to "Japan Wire" from July 2025. RSS available. Japanese site free.

**NHK World-Japan** | `www3.nhk.or.jp` | Type: `public_broadcaster` | Status: `EXISTING`
- **Structural role:** Japan's public broadcaster — the most-watched news program in Japan domestically, with a comprehensive English international service. Covers all five analytical domains.
- **Domain coverage:** All five domains
- **Reasoning:** NHK is the broadest single source for Japanese political coverage in English. Real-time text and broadcast coverage of PM press conferences, SDF operations, economic policy, and diplomacy. Public broadcaster status means editorially cautious and government-proximate but not propagandistic — its value is comprehensiveness and speed, not critical perspective. Fully free, RSS available, live stream available. No paywall, no crawler blocks. Tier 1 for structural breadth and extraction reliability.

**Nikkei Asia** | `asia.nikkei.com` | Type: `business_financial` | Status: `EXISTING`
- **Structural role:** English international edition of Japan's premier business daily (Nihon Keizai Shimbun). FT partnership. The single indispensable source for Japan's economic statecraft.
- **Domain coverage:** Economic & technological statecraft, Institutional engagement, Diplomatic alignment
- **Reasoning:** No other English-language source covers Japan's economic statecraft at this depth — semiconductor strategy, CPTPP dynamics, export controls, supply chain resilience, development finance, nearshoring. Owns the Financial Times, which adds global financial data integration. Metered paywall but most content extractable via Diffbot. Tier 1 because economic statecraft is a defining domain for Japan's middle-power posture and Nikkei Asia is the sole specialist.
- **Extraction note:** Metered paywall (~$15/month). Some articles free. RSS available.

**The Japan Times** | `www.japantimes.co.jp` | Type: `paper_of_record` | Status: `EXISTING`
- **Structural role:** Japan's oldest English-language newspaper (est. 1897). Broadest English-language original reporting on Japanese politics with dedicated defense, diplomacy, and political beats.
- **Domain coverage:** All five domains
- **Reasoning:** The Japan Times is the only English-language outlet producing substantial original reporting (not translations) across all five domains. Its commentary section features both Japanese and international analysts, providing interpretive depth beyond wire reports. Center-liberal editorial orientation provides a critical counterweight to the establishment-leaning wire services. Metered paywall but partially extractable. Tier 1 for original English-language analytical depth that no other source replicates.
- **Extraction note:** Metered paywall (~5-10 free articles/month). RSS available.

---

### Tier 2 — `$boost=2`

**Jiji Press** | `jen.jiji.com` / `jiji.com` | Type: `wire_service` | Status: `EXISTING`
- **Structural role:** Japan's second wire service. Employee-owned corporation with close ties to government press clubs. Provides redundancy against Kyodo and catches stories Kyodo may deprioritize.
- **Domain coverage:** Diplomatic alignment, Security & defense, Domestic constraints
- **Reasoning:** Wire redundancy is structurally valuable in a press-club system where access determines what gets reported. Jiji's slightly establishment-leaning orientation means it picks up bureaucratic and parliamentary stories that Kyodo's broader consumer orientation may underplay. English output thinner than Kyodo, which prevents Tier 1. Free.

**Asahi Shimbun (Asia & Japan Watch)** | `www.asahi.com/ajw` | Type: `paper_of_record` (center-left) | Status: `EXISTING`
- **Structural role:** Essential counterpoint to conservative outlets. Japan's leading center-left national daily. When Asahi shifts toward supporting a security measure, it signals genuine cross-spectrum consensus — this is the single most important editorial-line indicator in the Japanese press.
- **Domain coverage:** Domestic constraints, Diplomatic alignment, Security & defense
- **Reasoning:** Asahi's structural role as the left-of-center consensus marker is irreplaceable. Its editorials opposing defense expansion and constitutional revision are the baseline against which to measure genuine policy shifts. English AJW site provides selected translations, free access. **However, `asahi.com` is blocked by Anthropic's crawler**, which means extraction will fail even when Brave surfaces results. AJW's free English translations are the primary access path — the pipeline should target the `/ajw` subdirectory. Tier 2 rather than Tier 1 due to crawler block reducing extraction reliability and English output being selective (not comprehensive).
- **Blocked domain flag:** `asahi.com` blocked. AJW English translations may still be accessible via different subdomain handling — test required.

**The Japan News (Yomiuri Shimbun)** | `the-japan-news.com` | Type: `paper_of_record` (conservative) | Status: `EXISTING`
- **Structural role:** English edition of the world's largest-circulation newspaper. Editorials closely track LDP establishment thinking. When Yomiuri criticizes a government defense or diplomatic initiative, it signals intra-conservative dissent.
- **Domain coverage:** Security & defense, Diplomatic alignment, Domestic constraints
- **Reasoning:** The Japan News (English) is free with no paywall — the best extraction profile of any Japanese broadsheet. Provides direct translations of Yomiuri editorials and reporting, making LDP-establishment thinking accessible to the pipeline. `the-japan-news.com` is NOT blocked (only `yomiuri.co.jp` is blocked). Tier 2 because its editorial line overlaps with the government's own communications (Kantei) on most security/alliance issues, reducing its independent signal value compared to Asahi's oppositional marker role.
- **Note:** Japanese parent site `yomiuri.co.jp` is blocked. Route all Yomiuri extraction through `the-japan-news.com`.

**Tokyo Shimbun** | `www.tokyo-np.co.jp` | Type: `regional` (progressive) | Status: `EXISTING`
- **Structural role:** Marks the left boundary of mainstream Japanese press opinion. Aggressive reporting on government accountability for defense spending and SDF operations. Japanese-language only.
- **Domain coverage:** Domestic constraints, Security & defense
- **Reasoning:** Non-English domestic sources earn a boost premium. Tokyo Shimbun is the strongest editorial opposition voice to constitutional revision and Article 9 reinterpretation — its reporting on defense accountability is structurally essential for detecting domestic constraint signals that English-language sources miss entirely. Japanese-only limits pipeline extraction to headline/snippet analysis, but Brave indexes Japanese pages and the pipeline's `languages.primary: ja` configuration should surface these. Tier 2 for domestic-language depth on constraint signals.
- **Language note:** Japanese only. Requires Japanese-language query cycle.

**Nippon.com** | `www.nippon.com/en` | Type: `explainer` / `context` | Status: `EXISTING`
- **Structural role:** Multilingual web magazine that translates and contextualizes key opinion pieces from across the Japanese political spectrum. Publishes in-depth English explainers on elections, constitutional debates, and policy shifts.
- **Domain coverage:** All five domains (explainer/context function)
- **Reasoning:** Nippon.com fills a unique structural niche — it doesn't break news, but it provides the interpretive layer the pipeline needs to contextualize signals from wire feeds and newspapers. Translates diverse Japanese commentators into English, giving the pipeline access to the full editorial spectrum without requiring Japanese-language processing. Fully free, no paywall, RSS available. Tier 2 for analytical depth and translation bridge function.

**Prime Minister's Office (Kantei)** | `japan.kantei.go.jp` / `kantei.go.jp` | Type: `government_official` | Status: `EXISTING` — **LAYER 2 MIGRATION**
- **Structural role:** Chief Cabinet Secretary press conferences (twice daily) are the primary channel for official government positions. PM press conferences after summits are the definitive source for stated posture.
- **Domain coverage:** Diplomatic alignment, Security & defense, Economic & technological statecraft
- **Reasoning:** Primary fetch via Layer 2 direct polling. Goggle boost at Tier 2 as belt-and-suspenders fallback. Government sources = Layer 2 migration at Tier 2 per audit principles. English transcripts published with short delay. Free.

**Ministry of Foreign Affairs (MOFA)** | `www.mofa.go.jp` | Type: `government_official` | Status: `EXISTING` — **LAYER 2 MIGRATION**
- **Structural role:** Press releases on bilateral meetings, treaty negotiations, UN voting records, sanctions implementation, and ODA. Foreign Minister press conference transcripts. Diplomatic Bluebook.
- **Domain coverage:** Diplomatic alignment, Institutional engagement
- **Reasoning:** Primary fetch via Layer 2 direct polling. Goggle boost at Tier 2 as fallback. Comprehensive English section with same-day press releases. Essential for tracking shifts in diplomatic language toward specific countries. Free.

**Ministry of Defense (MOD)** | `www.mod.go.jp` | Type: `government_official` | Status: `EXISTING` — **LAYER 2 MIGRATION**
- **Structural role:** Defense Minister press conferences, SDF operational reports, annual "Defense of Japan" white paper, Joint Staff press releases on PLA/Russian military activity near Japan.
- **Domain coverage:** Security & defense autonomy
- **Reasoning:** Primary fetch via Layer 2 direct polling. Goggle boost at Tier 2 as fallback. Joint Staff press releases on intercepts/scrambles are the fastest official signal of military tensions in the East China Sea and Sea of Japan — these are published in English. Free.

**Nikkei Shimbun (Japanese edition)** | `www.nikkei.com` | Type: `business_financial` (Japanese) | Status: `EXISTING`
- **Structural role:** Japanese-language parent of Nikkei Asia. Carries deeper reporting on industrial policy, export controls, semiconductor strategy, economic security legislation, and trade negotiations than the English edition.
- **Domain coverage:** Economic & technological statecraft, Domestic constraints
- **Reasoning:** Non-English domestic sources earn a boost premium. Nikkei Japanese publishes economic statecraft reporting that never appears in the English Nikkei Asia edition — particularly on economic security legislation implementation, export control lists, and BOJ policy details. Metered paywall limits extraction but Brave indexes headlines. Tier 2 for domestic-language economic depth.
- **Language note:** Japanese only. Metered paywall.

---

### Tier 3 — `$boost=1`

**NIDS (National Institute for Defense Studies)** | `www.nids.mod.go.jp` | Type: `think_tank` (government) | Status: `EXISTING`
- **Structural role:** MOD-affiliated think tank publishing the annual "East Asian Strategic Review" and "NIDS China Security Report." Research papers signal evolving strategic thinking before it becomes policy.
- **Domain coverage:** Security & defense autonomy, Diplomatic alignment
- **Reasoning:** Think tanks earn boost through depth, not speed. NIDS publications are leading indicators of how Japan's defense establishment assesses regional threats — changes in threat characterization in the East Asian Strategic Review foreshadow shifts in the National Defense Strategy. Publication frequency is low (annual reports, periodic papers), which limits Tier placement. Tier 3 for periodic high-value analytical depth. Free.

**JIIA (Japan Institute of International Affairs)** | `www.jiia.or.jp` | Type: `think_tank` (MOFA-affiliated) | Status: `EXISTING`
- **Structural role:** MOFA's principal external think tank. Commentaries and policy briefs signal diplomatic establishment thinking on alliance management, multilateral engagement, and regional order.
- **Domain coverage:** Diplomatic alignment, Institutional engagement, Economic & technological statecraft
- **Reasoning:** Think tanks = depth not speed. JIIA is the closest thing to a direct window into MOFA's analytical framework. Strategic Yearbook and track-1.5 dialogue summaries are valuable but infrequent. Tier 3 for periodic strategic depth. Free.

**Sasakawa Peace Foundation / Sasakawa USA** | `www.spf.org` / `spfusa.org` | Type: `think_tank` (private) | Status: `EXISTING`
- **Structural role:** Privately funded (Nippon Foundation) but highly influential in Japan-US alliance discourse. Sasakawa USA monitors defense cooperation, arms exports, and burden-sharing.
- **Domain coverage:** Security & defense autonomy, Diplomatic alignment, Institutional engagement
- **Reasoning:** Provides the most detailed English-language analysis of US-Japan alliance mechanics — burden-sharing debates, defense technology transfer, and joint operational planning. Private funding (not government) gives slightly more analytical independence than NIDS or JIIA. Tier 3 for periodic analytical depth on alliance dynamics. Free.

**House of Representatives / House of Councillors** | `shugiin.go.jp` / `sangiin.go.jp` | Type: `legislative_official` | Status: `NEW`
- **Structural role:** Official Diet proceeding records. Committee debates and interpellations where opposition parties probe government security and diplomatic positions.
- **Domain coverage:** Domestic constraints, Security & defense
- **Reasoning:** The source intelligence map identifies Diet proceedings as a primary coverage gap. Adding legislative websites at Tier 3 provides a Goggle fallback for when Brave indexes committee transcripts or press releases from parliamentary sessions. Layer 2 direct polling is the primary access path. Japanese-language only. Tier 3 for supplementary structural coverage of the domestic constraint domain.
- **Language note:** Japanese only. Limited English content.

**Okinawa Times** | `www.okinawatimes.co.jp` | Type: `regional` | Status: `NEW`
- **Structural role:** Primary regional newspaper covering US military base politics, SOFA friction, and base realignment — the defining subnational defense issue in Japan.
- **Domain coverage:** Security & defense autonomy, Domestic constraints
- **Reasoning:** The jp.yaml config identifies "Okinawa base realignment" as a blind spot. Okinawa Times is the most authoritative source for local opposition to US military presence, base relocation disputes, and SOFA-related incidents. Japanese-language only, which limits extraction but earns the non-English domestic source premium. Tier 3 for structural gap coverage. The pipeline's blind_spots configuration already identifies this signal source.
- **Language note:** Japanese only.

---

### Neutral — no Goggle rule

**Sankei Shimbun / JAPAN Forward** | `japan-forward.com` / `sankei.com` | Type: `paper_of_record` (right-conservative) | Status: `EXISTING → DEMOTED TO NEUTRAL`
- **Why neutral:** Structurally valuable as the right boundary of mainstream Japanese opinion, but **both domains are blocked by Anthropic's crawler** — `japan-forward.com` and `sankei.com` appear on the blocked domains list. Extraction will fail even when Brave surfaces results. The right-conservative editorial niche is partially covered by Yomiuri/The Japan News (Tier 2), which shares Sankei's pro-alliance, pro-defense-buildup orientation, though Yomiuri is less hawkish on China/Korea. Leave neutral — may surface organically for headlines. If crawler access changes, re-evaluate at Tier 2.
- **Blocked domain flag:** Both `japan-forward.com` and `sankei.com` blocked.

**Reuters Japan** | `reuters.com` | Type: `international_wire` | Status: `EXISTING → DEMOTED TO NEUTRAL`
- **Why neutral:** Provides the external-observer lens, but **`reuters.com` is blocked by Anthropic's crawler**. Wire copy is available organically through Brave without boosting. The external-lens function is partially served by Kyodo's international reporting and by The Japan Times' international analyst commentary. Leave neutral — Brave can still surface for discovery even without extraction.
- **Blocked domain flag:** `reuters.com` blocked.

**Mainichi Shimbun** | `mainichi.jp` | Type: `paper_of_record` (center-left) | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Curation exclusion was correct under the hard-filter model — limited English output ("The Mainichi") and paywall. Under the Goggle model, no reason to actively discard. Its center-left niche is covered by Asahi (Tier 2) and Tokyo Shimbun (Tier 2), but if Mainichi breaks a story, Brave may surface it. Organic ranking is appropriate.

**Fuji News Network / FNN** | `fnn.jp` | Type: `broadcast` (conservative) | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Curation exclusion was correct — broadcast-first, web content mostly video. Fujisankei Group alignment means JAPAN Forward already captures this perspective (though JAPAN Forward is itself blocked). Under Goggle model, leave at organic ranking. May surface for specific breaking broadcast events.

**Toyo Keizai Online** | `toyokeizai.net` | Type: `business_financial` (Japanese) | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Strong Japanese-language business journalism with occasional security/industrial policy scoops, but Nikkei (both editions) covers economic statecraft more comprehensively. Curation exclusion was correct under hard-filter. Under Goggle model, organic ranking lets it surface serendipitously without displacing boosted sources.

**Japan Today** | `japantoday.com` | Type: `aggregator` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** English-language aggregator relying on wire content already captured by Kyodo and Jiji. Minimal original reporting. Curation exclusion was correct. Under Goggle model, organic ranking is appropriate — may surface for specific queries where its aggregation captures a wire story faster than the source wire's own site.

---

### Discard — `$discard`

**JapanBuzz** | `japanbuzz.info` | Status: `NEW DISCARD`
- **Discard reasoning:** Clickbait aggregation site repackaging viral Japanese social media content as "news." No editorial structure, no original political reporting. Would actively displace higher-signal sources from top results.

**Sora News 24 / RocketNews24** | `soranews24.com` | Status: `NEW DISCARD`
- **Discard reasoning:** Viral/entertainment content about Japan framed as news. Zero political, diplomatic, or security coverage. Would inject pure noise into search results and waste result slots.

**Japan Insider** | `japaninsider.com` | Status: `NEW DISCARD`
- **Discard reasoning:** SEO-optimized content farm producing thin, derivative articles about Japan. No original reporting, no editorial accountability. Would displace genuine sources from search results.

---

## STRUCTURAL COVERAGE CHECK

| Structural Role | Source(s) | Tier | Notes |
|---|---|---|---|
| Government signaling channel | Kantei, MOFA, MOD | T2 | **LAYER 2 MIGRATION** — primary fetch via direct polling. Goggle boost as fallback. Twice-daily Chief Cabinet Secretary pressers are the key signal |
| LDP establishment voice | The Japan News (Yomiuri) | T2 | Editorials track LDP mainstream thinking. Free English translations. When Yomiuri criticizes government policy, it signals intra-conservative dissent |
| Left-of-center consensus marker | Asahi Shimbun (AJW) | T2 | The single most important editorial indicator: when Asahi supports a security measure, cross-spectrum consensus exists. Blocked domain reduces extraction reliability |
| Progressive opposition voice | Tokyo Shimbun | T2 | Left boundary of mainstream press. Japanese-only but structurally essential for domestic constraint signals |
| Right-conservative boundary | Sankei / JAPAN Forward | Neutral | Right boundary of mainstream opinion. **Both blocked by crawler** — structural gap. Partially mitigated by Yomiuri (less hawkish) |
| Defence/security first-mover | MOD Joint Staff, Kyodo | T2, T1 | Joint Staff press releases on intercepts/scrambles are fastest signal. Kyodo breaks policy announcements. NIDS for analytical depth |
| Economic statecraft specialist | Nikkei Asia, Nikkei (JP) | T1, T2 | Sole specialist pair for semiconductor strategy, export controls, economic security legislation |
| Policy-elite discourse | Nippon.com, JIIA, Sasakawa | T2, T3, T3 | Nippon.com for translated political spectrum; JIIA for diplomatic establishment; Sasakawa for alliance mechanics |
| Domestic-language depth | Tokyo Shimbun, Nikkei (JP), Kyodo (JP), Okinawa Times | T2, T2, T1, T3 | Japanese-language query cycle captures signals that never reach English outlets — Diet faction dynamics, bureaucratic maneuvering, pacifist opposition framing |
| Wire service (baseline) | Kyodo, Jiji Press | T1, T2 | Dual wire coverage through Japan's press-club system. Cooperative vs. employee-owned gives slightly different access patterns |
| Analytical/think tank depth | NIDS, JIIA, Sasakawa | T3, T3, T3 | Defense establishment (NIDS), diplomatic establishment (JIIA), alliance mechanics (Sasakawa). All publish in English. Depth not speed |
| Subnational/regional | Okinawa Times | T3 | Covers the defining subnational defense issue — US base politics. Addresses blind spot identified in jp.yaml |
| Legislative proceedings | shugiin.go.jp, sangiin.go.jp | T3 | Diet committee debates — primary gap identified in source intelligence map. Japanese-only |
| Context/explainer bridge | Nippon.com, The Japan Times | T2, T1 | Translate and interpret signals for English-language pipeline processing |

**Gaps identified:**
1. **Right-conservative voice degraded:** Both Sankei and JAPAN Forward are blocked by Anthropic's crawler, leaving the right boundary of Japanese opinion structurally weak. Yomiuri/The Japan News partially mitigates but is less hawkish. This means the pipeline may underweight nationalist-hawkish pressure signals on defense and China policy. Mitigation: monitor crawler status quarterly; if access restores, promote Sankei/JAPAN Forward to Tier 2.
2. **Social media political signaling** remains unaddressed — Japanese politicians and commentators use X heavily for policy signaling, but this requires dedicated social media monitoring tools, not Goggle configuration.
3. **Nuclear latency debate** (identified as blind spot in jp.yaml) has no dedicated source — signals live in Diet committee transcripts (newly added at Tier 3), CSIS/RAND external analyses (not boosted, organic ranking), and Yomiuri defense reporting (Tier 2). This is a structural limitation of the public media landscape, not an audit gap.

---

## REDUNDANCY RESOLUTION

**Broadsheet cluster: Asahi + Yomiuri + Sankei + Mainichi**
Japan's national dailies form a clear left-right editorial spectrum. Resolved by editorial-spectrum differentiation: Asahi (Tier 2, left-of-center consensus marker — blocked but AJW partially accessible), Yomiuri/The Japan News (Tier 2, conservative establishment voice — English edition NOT blocked), Sankei/JAPAN Forward (Neutral — both blocked, partially redundant with Yomiuri), Mainichi (Neutral — partially redundant with Asahi, limited English output). Each occupies a distinct editorial position; blocking status determines tier within the spectrum.

**Wire service pair: Kyodo + Jiji**
Both cover the same domains through the press-club system. Kyodo leads (Tier 1) due to higher English-language output, broader topical coverage, and cooperative ownership insulating from editorial drift. Jiji at Tier 2 provides redundancy — critical in a system where press-club access determines story access. No further reduction warranted because wire redundancy is structurally valuable.

**Economic press cluster: Nikkei Asia + Nikkei (JP) + Toyo Keizai**
Nikkei Asia leads (Tier 1) as the indispensable English economic statecraft source. Nikkei Japanese (Tier 2) adds domestic-language depth on stories the English edition doesn't translate. Toyo Keizai (Neutral) is redundant with Nikkei and doesn't add enough differentiation to warrant boosting.

**Think tank cluster: NIDS + JIIA + Sasakawa**
Three think tanks but each fills a distinct niche: NIDS (defense establishment threat assessment), JIIA (diplomatic establishment foreign policy framing), Sasakawa (alliance mechanics and burden-sharing). No redundancy — all Tier 3 because they publish infrequently but each is the sole source for its analytical niche.

**Government source cluster: Kantei + MOFA + MOD**
All three are government official sources at Tier 2 with Layer 2 migration. No redundancy — each covers a distinct policy domain (executive coordination, diplomacy, defense). All warrant Tier 2 for Goggle fallback.

---

## QUERY CONFIGURATION

```
country: JP
search_lang: ja
freshness: pw
```

**Multi-language notes:** Japan's media ecosystem is bifurcated — unusually rich English-language output from major outlets (NHK World, Nikkei Asia, Japan Times, Kyodo English, Jiji English, The Japan News, AJW, Nippon.com) but the deepest political reporting remains Japanese-only. Queries should run in **both Japanese and English**: Japanese primary cycle for domestic constraint signals, Diet dynamics, and bureaucratic maneuvering; English secondary cycle for international-facing diplomatic, security, and economic statecraft coverage. The pipeline's `languages.primary: ja` / `languages.metadata: en` configuration handles this correctly.

**Localized query vocabulary validation:**

The curation prompt's vocabulary is strong and well-organized. Notes:

- **Domain 1 (Diplomatic):** All terms valid. `日米同盟` (Japan-US alliance) is the single highest-signal term. Add `"Takaichi gaikō"` / `"高市外交"` as leader-specific pattern. `自由で開かれたインド太平洋` (FOIP) remains the dominant regional framework term. Consider adding `"日中関係"` (Japan-China relations) and `"日韓関係"` (Japan-Korea relations) as bilateral-specific high-frequency patterns. Add `"Quad"` / `"クアッド"` — Japan's Quad engagement is a defining diplomatic signal.
- **Domain 2 (Security):** Excellent list. `反撃能力` (counterstrike capability) is the most politically charged current term. Add `"台湾有事"` (Taiwan contingency) — the dominant frame for Japan's security planning since 2022. `"防衛装備移転"` (defense equipment transfer) is correct and increasingly relevant given arms export policy liberalization. Add `"統合作戦司令部"` is already included — good. Consider `"日米共同訓練"` (US-Japan joint exercises) for operational tempo monitoring.
- **Domain 3 (Economic):** Strong. Add `"ラピダス"` (Rapidus — Japan's flagship semiconductor fab project) and `"TSMC熊本"` (TSMC Kumamoto plant) as high-signal specific terms. `"セキュリティクリアランス"` (security clearance) is correct and timely given the 2024 legislation. Add `"レアアース"` (rare earths) and `"重要鉱物"` (critical minerals) for supply chain statecraft.
- **Domain 4 (Institutional):** Valid. `"常任理事国入り"` (permanent UNSC seat bid) is perennial. Add `"IPEF"` (Indo-Pacific Economic Framework) and `"AUKUS pillar 2"` — Japan's potential engagement with AUKUS technology pillar is an emerging signal. `"G7議長国"` may need updating as Japan's 2023 presidency has ended — shift to `"G7サミット"` as generic.
- **Domain 5 (Domestic):** Strong. `"憲法改正"` (constitutional amendment) and `"第九条"` (Article 9) are the dominant domestic constraint terms. Add `"政治資金"` (political funds) — LDP slush fund scandal continues to shape coalition dynamics. Add `"Takaichi naikaku"` / `"高市内閣"` for cabinet-specific tracking. `"内閣支持率"` (cabinet approval rating) is correctly included.

**Stale/problematic terms:** `"G7議長国"` (G7 presidency) is stale as Japan's 2023 presidency has concluded — replace with `"G7"` generically. `"戦略的互恵関係"` (mutually beneficial strategic relationship with China) may be declining in official usage as Japan-China relations deteriorate, but remains a valid search term for detecting whether Japan revives conciliatory framing.

**Suggested topic query patterns:**

1. `高市 防衛費 GDP 2パーセント` — Takaichi defense spending / 2% GDP target
2. `台湾有事 日米同盟 反撃能力` — Taiwan contingency / alliance / counterstrike capability
3. `経済安全保障 半導体 輸出管理` — Economic security / semiconductors / export controls
4. `憲法改正 第九条 国民投票` — Constitutional revision / Article 9 / referendum
5. `防衛装備移転 次期戦闘機 GCAP` — Defense equipment transfer / next-gen fighter / GCAP

---

## GOGGLE FILE

```goggle
! name: MPM Japan
! description: MPM pipeline source prioritization for Japan — boosts high-signal sources, discards noise
! public: false
! author: MPM Pipeline

! --- Tier 1: Essential (boost=3) ---
$boost=3,site=english.kyodonews.net
$boost=3,site=kyodonews.jp
$boost=3,site=www3.nhk.or.jp
$boost=3,site=asia.nikkei.com
$boost=3,site=www.japantimes.co.jp

! --- Tier 2: Important (boost=2) ---
$boost=2,site=jen.jiji.com
$boost=2,site=jiji.com
$boost=2,site=www.asahi.com
$boost=2,site=the-japan-news.com
$boost=2,site=www.tokyo-np.co.jp
$boost=2,site=www.nippon.com
$boost=2,site=japan.kantei.go.jp
$boost=2,site=kantei.go.jp
$boost=2,site=www.mofa.go.jp
$boost=2,site=www.mod.go.jp
$boost=2,site=www.nikkei.com

! --- Tier 3: Supplementary (boost=1) ---
$boost=1,site=www.nids.mod.go.jp
$boost=1,site=www.jiia.or.jp
$boost=1,site=www.spf.org
$boost=1,site=spfusa.org
$boost=1,site=shugiin.go.jp
$boost=1,site=sangiin.go.jp
$boost=1,site=www.okinawatimes.co.jp

! --- Discard: Noise ---
$discard,site=japanbuzz.info
$discard,site=soranews24.com
$discard,site=japaninsider.com
```

---

## INTERPRETIVE CONTEXT FOR DOSSIER

### Tier 1 Sources

> Articles from **Kyodo News** about any domain should be interpreted as Japan's most authoritative wire service reporting — its cooperative ownership by member newspapers means it reflects the journalistic consensus of the Japanese press corps rather than any single editorial line. Kyodo breaks stories fastest in English and its framing of government announcements is the baseline against which other outlets' spin should be measured.

> Articles from **NHK World-Japan** about government policy should be interpreted as the official public broadcaster's coverage — editorially cautious, comprehensive, and government-proximate. NHK will not break critical stories about the government but will cover everything the government says and does. Its value is completeness and speed on official events, not critical analysis. When NHK gives unusual prominence to a diplomatic or security development, it signals the government considers it significant enough for public messaging.

> Articles from **Nikkei Asia** about economic policy, trade, and technology should be interpreted as reflecting the perspective of Japan's business and financial establishment — pro-trade liberalization, globally oriented, and focused on investment climate implications. Negative coverage of government economic intervention reflects business-sector concern, not necessarily policy failure. Its FT partnership means it frames Japan's economic statecraft in global comparative terms unavailable elsewhere.

> Articles from **The Japan Times** about defense and diplomacy should be interpreted as Japan's most independent English-language broadsheet reporting — its center-liberal editorial orientation means it frames security expansion with measured skepticism and gives voice to both Japanese and international critics. Its commentary section is the best single source for understanding how English-speaking analysts interpret Japanese political developments.

### Tier 2 Sources

> Articles from **Jiji Press** about government decisions should be interpreted as establishment-proximate wire reporting — its close ties to government press clubs mean it surfaces bureaucratic and parliamentary stories that Kyodo may deprioritize, but also that its framing tends to reflect official characterizations. Cross-check against Kyodo for editorial balance.

> Articles from **Asahi Shimbun (AJW)** about defense and constitutional matters should be interpreted as Japan's leading center-left editorial voice — when Asahi opposes a security measure, it represents expected liberal-opposition framing; when Asahi supports or acquiesces to a security measure, it signals genuine cross-spectrum consensus that the policy has become politically normalized. This is the single most important editorial-line indicator in the Japanese press. Note: extraction may be unreliable due to crawler block on `asahi.com`.

> Articles from **The Japan News (Yomiuri)** about US-Japan alliance and defense policy should be interpreted as reflecting LDP establishment thinking — Yomiuri is the world's largest-circulation newspaper and the closest major daily to the ruling party mainstream. Its editorials supporting defense buildup and constitutional revision represent the conservative-establishment baseline. When Yomiuri criticizes a government security or diplomatic initiative, it signals intra-conservative dissent worth investigating.

> Articles from **Tokyo Shimbun** about defense spending and SDF operations should be interpreted as Japan's most aggressive pacifist-progressive media voice — its opposition to Article 9 reinterpretation and defense expansion is consistent and principled, making it the left boundary of mainstream press opinion. Its reporting on defense accountability (cost overruns, readiness gaps, SOFA incidents) provides oversight journalism that establishment outlets underplay. Japanese-language only — signals from this source are inherently filtered through translation/summary.

> Articles from **Nippon.com** about political developments should be interpreted as curated English-language explainers drawing from across the Japanese political spectrum — not breaking news but contextual depth. Its editorial selection of which Japanese commentators to translate signals what the Nippon Foundation considers important for international audiences to understand about Japanese politics.

> Articles from **government sources** (Kantei, MOFA, MOD) should be interpreted as official communications — not journalism but primary source material. Press releases and transcripts represent the government's chosen public position. Chief Cabinet Secretary pressers are particularly important: evasive or formulaic language ("We are closely watching the situation with a sense of urgency") signals the government is aware of a problem but has not yet formulated a response. Shifts in diplomatic language toward specific countries (e.g., dropping "mutually beneficial strategic relationship" for China) are leading indicators of posture change.

> Articles from **Nikkei Shimbun (Japanese)** about industrial policy and economic security legislation should be interpreted as deeper domestic-language reporting that may not appear in the English Nikkei Asia edition — particularly implementation details of the Economic Security Promotion Act, specific export control list changes, and BOJ policy committee deliberations. The Japanese edition's business-establishment perspective is the same as Nikkei Asia's but the reporting is more granular.

### Tier 3 Sources

> Articles from **NIDS** about regional security threats should be interpreted as semi-official defense establishment assessments — changes in threat characterization in NIDS publications (e.g., upgrading China from "concern" to "strategic challenge" to "greatest threat") foreshadow shifts in official defense policy documents by 6-12 months.

> Articles from **JIIA** about diplomatic strategy should be interpreted as MOFA-adjacent analytical framing — JIIA commentaries signal how the diplomatic establishment thinks about alliance management and multilateral engagement, providing advance indicators of diplomatic posture shifts before they appear in official press releases.

> Articles from **Sasakawa Peace Foundation / Sasakawa USA** about US-Japan alliance dynamics should be interpreted as detailed analysis of alliance mechanics — burden-sharing, technology transfer, and joint operational planning — from a pro-alliance but analytically rigorous perspective. Sasakawa USA specifically provides the most granular English-language tracking of US-Japan defense cooperation developments.

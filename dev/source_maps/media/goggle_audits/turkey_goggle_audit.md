# AUDIT SUMMARY: TURKEY

**Sources assessed:** 19 recommended + 5 excluded + 5 newly identified = 29 total
**Tier 1 (boost=3):** 5 sources
**Tier 2 (boost=2):** 8 sources
**Tier 3 (boost=1):** 6 sources
**Neutral (no rule):** 6 sources
**Discard:** 4 sources
**Overall assessment:** The curation prompt produced a strong whitelist with unusual depth on opposition and investigative outlets — critical for a country where 90% of mainstream media is government-controlled. Key changes: (1) resolved redundancy between Hurriyet and Hurriyet Daily News by splitting tiers, and between AA and Daily Sabah by differentiating structural signals; (2) promoted government official sources (Resmi Gazete, TBMM, tccb.gov.tr, mfa.gov.tr) for Layer 2 migration at Tier 2; (3) added missing sources: Ahval News (opposition diaspora), TEPAV and EDAM (think tanks), and Karar (centrist-conservative voice); (4) applied non-English domestic premium — Turkish-language sources with no English edition receive boost uplift; (5) flagged `reuters.com` as blocked by Anthropic's crawler, affecting wire extraction. No Turkish domestic domains are blocked.

---

## BOOST ASSIGNMENTS

### Tier 1 — `$boost=3`

**Anadolu Agency (AA)** | `anadolu.com.tr` | Type: `government_aligned` | Status: `EXISTING`
- **Structural role:** State news agency; the single most authoritative signal of Ankara's intended messaging. What AA publishes, emphasizes, or omits is itself an intelligence signal.
- **Domain coverage:** Diplomatic alignment, Security & defense autonomy, Economic & technological statecraft, Institutional engagement
- **Reasoning:** Structural role outweighs journalistic independence. AA is how the Turkish state communicates to domestic and international audiences — its framing choices reveal official posture on NATO, Syria, the Kurdish issue, defense exports, and Russia relations. Bilingual (Turkish + English) maximizes pipeline extraction. No domestic substitute. In a media landscape where government intent is the hardest signal to decode from noise, AA is the primary decoder ring.
- **Non-English premium:** Applies — Turkish-language output provides deeper, faster signal than English edition.

**Cumhuriyet** | `cumhuriyet.com.tr` | Type: `opposition_aligned` | Status: `EXISTING`
- **Structural role:** Turkey's oldest continuously published newspaper (est. 1924). The primary Kemalist-secular voice in Turkish media. Where CHP-aligned foreign policy critique surfaces.
- **Domain coverage:** Diplomatic alignment, Domestic constraints, Institutional engagement
- **Reasoning:** In a country where 90% of media is government-aligned, opposition voice sources earn maximum structural premium. Cumhuriyet provides the most consistent, institutionally grounded critique of AKP foreign and security policy. Its secular-Kemalist lens surfaces NATO posture debates, EU accession arguments, and opposition positions on Kurdish peace process that government-aligned outlets suppress. Turkish-only publication triggers non-English domestic premium. No consistent English edition — the pipeline must process Turkish text, which increases the source's structural scarcity value.
- **Non-English premium:** Applies — Turkish-only, no English edition.

**T24** | `t24.com.tr` | Type: `investigative` | Status: `EXISTING`
- **Structural role:** Highest editorial quality among surviving independent digital outlets. Long-form analysis across all five analytical domains. Fills the structural role of independent analytical hub that no other Turkish outlet occupies.
- **Domain coverage:** All five domains
- **Reasoning:** T24 is the closest Turkey has to an independent, analytically rigorous outlet covering the full domain spectrum. In a media environment where independents have been crushed (Gazete Duvar shut down in 2025, others lost 70-90% of traffic), T24's survival and continued analytical depth make it structurally irreplaceable. Covers foreign policy, economic policy, institutional erosion, and defense with original analysis rather than wire rewrites. Turkish-only triggers non-English premium.
- **Non-English premium:** Applies — Turkish-only.
- **Extraction note:** Google algorithm changes reduced traffic by 70-90% for independent Turkish outlets. Monitor for viability.

**Bloomberg HT** | `bloomberght.com` | Type: `business_financial` | Status: `EXISTING`
- **Structural role:** Turkey's only dedicated business/financial media platform. Sole source for systematic coverage of central bank policy, trade agreements, sanctions exposure, FDI flows, and defense-industry economics.
- **Domain coverage:** Economic & technological statecraft, Diplomatic alignment
- **Reasoning:** No other Turkish source systematically covers economic statecraft. Bloomberg HT tracks TCMB rate decisions, lira dynamics, energy import dependencies (Russian gas, Azerbaijani pipelines), defense-industry export economics, and trade agreement negotiations. In a country where monetary policy independence is a known blind spot and where economic statecraft (sanctions navigation, energy corridor positioning) is a defining feature of middle-power behavior, this source is irreplaceable. Turkish-language triggers non-English premium.
- **Non-English premium:** Applies — Turkish-language, Bloomberg International partnership adds data layer.

**Al-Monitor Turkey** | `al-monitor.com/turkey` | Type: `regional` | Status: `EXISTING`
- **Structural role:** Best English-language source with a dedicated Turkey desk, original Ankara-based reporting, and analysis bridging Turkish domestic politics to regional posture.
- **Domain coverage:** All five domains
- **Reasoning:** Al-Monitor occupies a unique structural position: it has original reporting from inside Turkey (not wire rewrites), covers all five analytical domains, and publishes in English — making it the highest-signal English-language Turkey source for pipeline extraction. Its Washington-based editorial team provides the U.S./Western policy frame that domestic Turkish outlets cannot. Partial paywall limits some extraction, but most analytical pieces are accessible. Tier 1 because no other single source bridges the domestic-international analytical gap this effectively.
- **Extraction note:** Partial paywall — Brave can surface for discovery; Diffbot extraction may be partial on premium content.

---

### Tier 2 — `$boost=2`

**Hurriyet** | `hurriyet.com.tr` | Type: `paper_of_record` | Status: `EXISTING`
- **Structural role:** Turkey's highest-circulation newspaper. Post-2018 government-aligned editorial line under Demiroren Group ownership, but retains analytical depth on economics and reflects the government-business consensus.
- **Domain coverage:** Diplomatic alignment, Economic & technological statecraft, Domestic constraints
- **Reasoning:** Tier 2 rather than Tier 1 because post-2018 editorial alignment with government reduces its independent signal value — AA and Daily Sabah already cover official posture, and Cumhuriyet covers opposition. Hurriyet's unique value is the government-business nexus: how corporate Turkey interprets and responds to policy. Turkish-language edition is the primary product; English edition (Hurriyet Daily News) is separated below.
- **Non-English premium:** Applies — Turkish-language primary edition.

**Sozcu** | `sozcu.com.tr` | Type: `opposition_aligned` | Status: `EXISTING`
- **Structural role:** High-circulation secular-nationalist opposition paper. Covers protest movements, judicial independence, and CHP policy positions on foreign affairs. Subject to RTUK broadcast bans (Sozcu TV).
- **Domain coverage:** Domestic constraints, Diplomatic alignment
- **Reasoning:** Fills the nationalist-opposition niche distinct from Cumhuriyet's Kemalist-intellectual opposition. Sozcu's mass-market readership makes it a better gauge of popular opposition sentiment. RTUK broadcast bans on Sozcu TV are themselves an intelligence signal. Tier 2 rather than Tier 1 because domain coverage is narrower (primarily domestic constraints) and it breaks fewer stories than Cumhuriyet. Turkish-only triggers non-English premium.
- **Non-English premium:** Applies — Turkish-only.

**Medyascope** | `medyascope.tv` | Type: `investigative` | Status: `EXISTING`
- **Structural role:** Video-first independent digital platform featuring panel discussions with academics and former diplomats. Uniquely covers issues mainstream media avoids.
- **Domain coverage:** Domestic constraints, Diplomatic alignment, Economic & technological statecraft
- **Reasoning:** Medyascope's panel format surfaces expert analysis from former diplomats, economists, and security analysts who cannot publish in government-aligned outlets. This makes it a unique channel for elite dissent and informed analysis. YouTube-based distribution makes it more resilient to domain blocking than text-based independents. Tier 2 rather than Tier 1 because video-first format limits text extraction for the pipeline — the signal is high but extraction is harder.
- **Extraction note:** YouTube-based. Pipeline text extraction will be limited to descriptions and transcripts if available. Consider monitoring X account for text summaries.

**Bianet** | `bianet.org` | Type: `investigative` | Status: `EXISTING`
- **Structural role:** Independent rights-based outlet covering press freedom, minority rights, judicial proceedings, and EU accession benchmarks. English section makes it pipeline-friendly.
- **Domain coverage:** Domestic constraints, Institutional engagement
- **Reasoning:** Bianet is the go-to source for EU-Turkey relations benchmarks, press freedom tracking, and minority rights monitoring — institutional engagement and domestic constraints coverage that no other outlet systematically provides. English section availability is a significant practical advantage. Tier 2 because domain coverage is narrower than T24 but depth within its niche is unmatched.

**Government Official Sources** | `tccb.gov.tr`, `mfa.gov.tr`, `resmigazete.gov.tr`, `tbmm.gov.tr` | Type: `legislative_official` | Status: `EXISTING (map) + EXISTING (yaml: tccb, mfa)` — **LAYER 2 MIGRATION**
- **Structural role:** Primary government communications: Presidential office, Foreign Ministry, Official Gazette, Parliament. Publishes laws, decrees, defense procurement notices, trade agreements, committee proceedings, and foreign policy statements.
- **Domain coverage:** All five domains (official source)
- **Reasoning:** Primary fetch via Layer 2 direct polling. Goggle boost at Tier 2 as belt-and-suspenders fallback. Resmi Gazete is essential for detecting policy shifts before media coverage — presidential decrees, defense procurement, and trade agreements appear here first. TBMM committee hearings reveal intra-coalition tensions. The YAML already includes `tccb.gov.tr` and `mfa.gov.tr` at Tier 1 as government sources; the Goggle treats all four at Tier 2 because Layer 2 is the primary fetch mechanism.

**Middle East Eye** | `middleeasteye.net` | Type: `regional` | Status: `EXISTING`
- **Structural role:** Strong investigative reporting on Turkey's Syria policy, Libya engagement, and Kurdish peace process. English-language.
- **Domain coverage:** Diplomatic alignment, Security & defense autonomy, Domestic constraints
- **Reasoning:** MEE fills a critical niche: English-language investigative reporting on Turkey's regional military and diplomatic posture that domestic outlets either can't cover (censorship) or won't (government alignment). Its Syria, Libya, and Kurdish peace process coverage is deeper than any wire service. Accused of Qatar affinity, which the interpretive context handles. Tier 2 rather than Tier 1 because it's external to Turkey and doesn't cover economic statecraft or institutional engagement systematically.

**SETA (Insight Turkey)** | `setav.org` | Type: `political_specialist` | Status: `EXISTING`
- **Structural role:** AKP-proximate think tank. Publications reveal the intellectual framework behind government foreign and security policy.
- **Domain coverage:** Diplomatic alignment, Security & defense autonomy
- **Reasoning:** Think tanks earn boost through depth, not speed. SETA publications expose the ideological and strategic logic behind AKP policy — why Turkey pursues a specific NATO posture, how it frames defense autonomy, what "strategic depth" means in practice. Insight Turkey journal is peer-reviewed. Government-aligned bias is a feature, not a bug: it reveals the ruling party's intellectual self-understanding. Tier 2 for analytical depth.

---

### Tier 3 — `$boost=1`

**Hurriyet Daily News** | `hurriyetdailynews.com` | Type: `paper_of_record` | Status: `EXISTING`
- **Structural role:** Primary English-language window into Turkish domestic coverage. Useful for English keyword monitoring.
- **Domain coverage:** Diplomatic alignment, Economic & technological statecraft
- **Reasoning:** Tier 3 rather than Tier 2 because it's derivative of Hurriyet (already at Tier 2) and Al-Monitor (Tier 1) provides better English-language analytical coverage. Redundancy with parent publication reduces boost. But it remains useful as a quick English-language signal detector when the pipeline can't process Turkish text. The boost ensures it surfaces above generic English-language results about Turkey.

**Daily Sabah** | `dailysabah.com` | Type: `government_aligned` | Status: `EXISTING`
- **Structural role:** Pro-government English-language outlet close to AKP. Reflects how Ankara wants international audiences to perceive its posture.
- **Domain coverage:** All five domains
- **Reasoning:** Tier 3 rather than higher because AA already provides the authoritative government signal at Tier 1, and Daily Sabah adds the English-language international-messaging layer. Divergences between Daily Sabah and AA are interesting signals (internal messaging debates), but those are rare enough that Tier 3 suffices. The YAML has Daily Sabah at Tier 3 with triage_source=true, which aligns.

**BirGun** | `birgun.net` | Type: `opposition_aligned` | Status: `EXISTING`
- **Structural role:** Left-progressive outlet covering labor, social movements, and leftist critique of defense spending and Western alignment.
- **Domain coverage:** Domestic constraints, Security & defense autonomy, Economic & technological statecraft
- **Reasoning:** Fills the left-flank opposition niche distinct from Cumhuriyet (Kemalist) and Sozcu (secular-nationalist). BirGun surfaces domestic constraints from labor, environmental, and anti-militarist perspectives that other outlets ignore. Tier 3 because its audience and institutional weight are smaller than the other opposition outlets, and domain coverage overlaps partially with Cumhuriyet.
- **Non-English premium:** Applies — Turkish-only.

**Defence Turkey / C4Defence** | `defenceturkey.com` / `c4defence.com` | Type: `security_defense` | Status: `EXISTING`
- **Structural role:** Specialist defense-industry publications covering procurement, indigenous production (KAAN, Bayraktar, MILGEM), defense exports, and NATO interoperability.
- **Domain coverage:** Security & defense autonomy, Economic & technological statecraft
- **Reasoning:** The only dedicated defense press in the Turkish media ecosystem. Industry-aligned, which means sourcing is good for procurement and production but weak on military operations and human rights dimensions. Bilingual (Turkish + English). Tier 3 because industry alignment limits analytical independence and because defense/security stories that matter for the dossier will also surface in Tier 1-2 sources. But the niche is otherwise uncovered.

**Duvar English** | `duvarenglish.com` | Type: `investigative` | Status: `EXISTING`
- **Structural role:** English-language edition of former Gazete Duvar team. Covers stories that government-aligned outlets suppress.
- **Domain coverage:** Domestic constraints, Diplomatic alignment
- **Reasoning:** Pipeline-friendly English-language independent coverage. Tier 3 because the parent outlet (Gazete Duvar) ceased operations in 2025 and the English edition's future viability is uncertain. While operational, it fills a genuine niche: English-language independent Turkish journalism. Redundancy with Bianet (also English, also independent) is mitigated by different editorial focus — Duvar English covers broader politics while Bianet focuses on rights and EU benchmarks.

**Ahval News** | `ahvalnews.com` | Type: `opposition_aligned` / `diaspora` | Status: `NEW` (from YAML, not in source map)
- **Structural role:** Diaspora-based opposition outlet. Provides critical analysis from Turkish journalists operating outside Turkish jurisdiction. Present in YAML at Tier 2 with triage_source=true.
- **Domain coverage:** Domestic constraints, Diplomatic alignment, Security & defense autonomy
- **Reasoning:** Ahval occupies the diaspora-independent niche: Turkish analysts and journalists who cannot publish freely inside Turkey write here. This makes it a unique channel for informed criticism that faces no domestic censorship pressure. Tier 3 rather than the YAML's Tier 2 because diaspora outlets lack real-time domestic sourcing — they analyze and critique rather than break news. The YAML's triage_source=true is appropriate for discovery, but the Goggle boost should be lower than domestic independents (T24, Medyascope) who have on-the-ground sources.

---

### Neutral — no Goggle rule

**Sabah** | `sabah.com.tr` | Type: `government_aligned` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Government-aligned paper of record, but AA and Daily Sabah already cover the official posture signal. Sabah adds volume without differentiated intelligence. Under the Goggle model, no reason to actively discard — if Sabah breaks a story, Brave may surface it organically. Exclusions default to Neutral, not Discard.

**TRT World** | `trtworld.com` | Type: `government_aligned` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** State broadcaster's English channel provides polished government messaging, but AA already serves this function with faster, more granular output. Under Goggle model, TRT World may surface organically for international-audience queries. No reason to discard — organic ranking is appropriate.

**Yeni Safak** | `yenisafak.com` | Type: `government_aligned` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Hardline pro-government daily useful for tracking AKP's nationalist flank. Largely redundant with SETA for analytical purposes and AA for news. Under Goggle model, organic ranking lets it surface when its nationalist-hardline framing is the most relevant result. No reason to discard.

**Rudaw** | `rudaw.net` | Type: `regional` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Kurdistan Region (Iraq)-based, KDP-aligned. Valuable for KRG perspective on Turkey-KRG relations, but not a direct window into Turkey's domestic Kurdish dynamics — Mezopotamya Agency serves that role. May surface organically for cross-border Kurdish stories. No reason to discard.

**Gazete Duvar** | `gazeteduvar.com.tr` | Type: `investigative` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Ceased operations in 2025 due to financial collapse. Duvar English continues independently (listed at Tier 3). Archived content may still surface in Brave. No reason to discard — defunct but harmless.

**Reuters** | `reuters.com` | Type: `wire` | Status: `EXISTING (YAML wire) → NEUTRAL`
- **Why neutral:** Listed in YAML as a wire source. Not boosted in Goggle — wire copy is available organically. **Blocked by Anthropic's crawler** (`robots.txt` denial), which means extraction via pipeline tools will fail even if Brave surfaces it. Under the Goggle model, it can still appear organically for specific queries. AP News and France24 (also YAML wire sources) are not blocked and remain available organically.

---

### Discard — `$discard`

**Yeni Akit** | `yeniakit.com.tr` | Status: `NEW DISCARD`
- **Discard reasoning:** Ultra-nationalist, Islamist daily with a track record of publishing conspiracy theories, hate speech targeting minorities, and fabricated quotes attributed to foreign leaders. Would actively displace higher-signal sources from top results and inject noise into the pipeline. No structural role not already covered by SETA (for Islamist-conservative intellectual framing) and AA (for official posture).

**OdaTV** | `odatv.com` | Status: `NEW DISCARD`
- **Discard reasoning:** Ultranationalist website associated with the Ergenekon network. Publishes sensationalized content, conspiracy theories about foreign powers, and unverifiable "intelligence" claims. Would inject disinformation noise into security/defense queries. Sozcu and Cumhuriyet already cover the secular-nationalist opposition perspective with institutional accountability.

**Haber7** | `haber7.com` | Status: `NEW DISCARD`
- **Discard reasoning:** Click-driven government-aligned news aggregator with no original reporting and high noise-to-signal ratio. Would waste result slots without providing differentiated intelligence. AA, Daily Sabah, and Hurriyet already cover the government-aligned spectrum.

**Takvim** | `takvim.com.tr` | Status: `NEW DISCARD`
- **Discard reasoning:** Sensationalist pro-government tabloid. Publishes inflammatory headlines, unverified claims, and nationalist clickbait. No original reporting or analytical value. Would actively displace higher-signal sources.

---

## STRUCTURAL COVERAGE CHECK

| Structural Role | Source(s) | Tier | Notes |
|---|---|---|---|
| Government posture signal | Anadolu Agency (AA) | T1 | State news agency — what AA publishes or omits is itself intelligence. Daily Sabah (T3) adds the international-messaging layer |
| Opposition voice (secular) | Cumhuriyet, Sozcu | T1, T2 | Cumhuriyet for Kemalist-intellectual critique; Sozcu for mass-market nationalist opposition |
| Opposition voice (left) | BirGun | T3 | Left-progressive flank. Weaker institutionally but covers labor/social dimensions others miss |
| Opposition voice (diaspora) | Ahval News | T3 | Diaspora-based critical analysis free from domestic censorship |
| Opposition voice (Kurdish) | Mezopotamya Agency (MA) | T2* | *See note below on domain instability. Essential for Kurdish political dynamics |
| Independent analytical hub | T24 | T1 | Highest editorial quality among surviving independents. Covers all five domains |
| Independent investigative | Medyascope, Bianet, Duvar English | T2, T2, T3 | Medyascope for elite-expert panels; Bianet for rights/EU; Duvar English for English-language independent coverage |
| Defence/security specialist | Defence Turkey / C4Defence | T3 | Only dedicated defense press. Industry-aligned — good on procurement, weak on operations |
| Financial/economic specialist | Bloomberg HT | T1 | Sole dedicated business platform. Irreplaceable for TCMB, trade, FDI, energy economics |
| Government-business nexus | Hurriyet | T2 | Post-2018 alignment reflects government-business consensus |
| Policy-elite discourse | SETA (Insight Turkey) | T2 | AKP-proximate think tank — reveals intellectual framework behind policy |
| Paper of record (English) | Hurriyet Daily News | T3 | Derivative of Hurriyet; Al-Monitor is the better English analytical source |
| Regional analytical lens | Al-Monitor, Middle East Eye | T1, T2 | Al-Monitor for comprehensive Turkey desk; MEE for Syria/Libya/Kurdish investigative depth |
| Official government source | tccb.gov.tr, mfa.gov.tr, resmigazete.gov.tr, tbmm.gov.tr | T2 | **LAYER 2 MIGRATION** — primary fetch via direct polling. Goggle boost as fallback |
| Domestic-language depth | All Turkish-language sources | T1–T3 | Non-English domestic premium applied. Pipeline must process Turkish text for highest-value sources |
| Wire service | Reuters, AP News, France24 | Neutral | Not boosted. Reuters is blocked by Anthropic crawler; AP News and France24 available organically |

**Note on Mezopotamya Agency (MA):** Domain rotates due to court blocks (currently `mezopotamyaajansi42.com`). This makes Goggle boosting unreliable — the domain in the Goggle file will go stale when the next block forces a rotation. **Recommended approach:** Boost current known domain at Tier 2; monitor via X accounts `@maturkce2` and `@makurdi0` for domain changes; update Goggle file when domain rotates. The pipeline should flag MA domain changes as a maintenance task.

**Gaps identified:**
1. **Independent defense-analytical coverage** is structurally absent — Defence Turkey and C4Defence are industry-aligned, and no Turkish equivalent of Jane's or IISS exists. Mitigated partly by T24's analytical coverage and MEE's investigative work on military operations, but procurement corruption and arms import/export dynamics lack an independent analytical source.
2. **Kurdish-language domestic coverage** is critically fragile — if Mezopotamya Agency is permanently suppressed, there is no replacement for pipeline monitoring of Kurdish political dynamics in Turkish. Rudaw (Neutral) covers KRG-side dynamics but not Turkey's domestic Kurdish politics.
3. **Political economy of defense procurement corruption and sanctions evasion** has no systematic source. Bloomberg HT covers markets but not the shadow economy of defense procurement. This is a known blind spot across Turkey's entire media ecosystem.
4. **Think tank diversity** is limited — SETA is the only think tank source, and it's government-aligned. Added TEPAV and EDAM as suggestions below, but neither has the publication frequency to justify boosting.

**Suggested additions for future audits:**
- **TEPAV** (`tepav.org.tr`) — Moderate/technocratic think tank with strong economic policy analysis. Could fill the non-government think tank gap.
- **EDAM** (`edam.org.tr`) — Foreign policy and security think tank with transatlantic focus. Could complement SETA's government-aligned lens.
- **Karar** (`karar.com`) — Centrist-conservative daily, Davutoglu-affiliated. Fills the AKP-dissident conservative niche not covered by secular opposition outlets.

---

## REDUNDANCY RESOLUTION

**Government posture cluster: Anadolu Agency + Daily Sabah + Hurriyet**
All three are government-aligned post-2018. Resolved by differentiating structural signals: AA (Tier 1, authoritative state voice, fastest and most granular), Hurriyet (Tier 2, government-business nexus, analytical depth on economics), Daily Sabah (Tier 3, international-messaging layer, English-language AKP framing). Sabah dropped to Neutral — adds volume without differentiated signal.

**Opposition cluster: Cumhuriyet + Sozcu + BirGun + Ahval News**
Four opposition outlets, each representing a distinct ideological flank. Cumhuriyet (Tier 1, Kemalist-intellectual), Sozcu (Tier 2, secular-nationalist mass-market), BirGun (Tier 3, left-progressive), Ahval (Tier 3, diaspora-independent). No true redundancy — each covers a different opposition constituency, which is structurally important in a country with suppressed media pluralism.

**Independent/investigative cluster: T24 + Medyascope + Bianet + Duvar English**
Four surviving independents. T24 (Tier 1, broadest domain coverage, analytical depth), Medyascope (Tier 2, expert-panel format, video-first), Bianet (Tier 2, rights/EU niche, English section), Duvar English (Tier 3, English-language independent, uncertain viability). Investigative plurality is critical in Turkey's constrained media environment — losing any one of these outlets would create a genuine coverage gap.

**English-language Turkey cluster: Al-Monitor + Hurriyet Daily News + Daily Sabah + Duvar English + Bianet (English section)**
Five English-language sources. Resolved by analytical quality: Al-Monitor (Tier 1, original reporting, full-domain coverage), Bianet (Tier 2, rights/EU niche), Daily Sabah (Tier 3, government framing), Hurriyet Daily News (Tier 3, derivative of parent), Duvar English (Tier 3, independent). Al-Monitor is the clear English-language leader; the others fill specific niches at lower tiers.

**Regional analytical cluster: Al-Monitor + Middle East Eye**
Both are English-language external outlets covering Turkey's regional posture. No redundancy — Al-Monitor has a dedicated Turkey desk with comprehensive coverage; MEE specializes in investigative reporting on Syria/Libya/Kurdish dimensions. Al-Monitor (Tier 1) for breadth; MEE (Tier 2) for regional security depth.

---

## QUERY CONFIGURATION

```
country: TR
search_lang: tr
freshness: pw
```

**Multi-language notes:** Turkey's media ecosystem operates primarily in Turkish, with Kurdish as a secondary language for Kurdish political dynamics. English-language sources (Al-Monitor, Hurriyet Daily News, Daily Sabah, Bianet English, Duvar English) are analytically important but supplementary to Turkish-language originals. Queries should run primarily in Turkish; a secondary English query cycle captures Al-Monitor, MEE, and international wire coverage. A tertiary Kurdish query cycle for security/Kurdish peace process topics would capture Mezopotamya Agency signal. The pipeline's existing `languages.metadata: en` and `languages.additional: [ku]` configuration handles this correctly.

**Localized query vocabulary validation:**

The curation prompt's vocabulary is solid. Notes:

- **Domain 1 (Diplomatic):** All terms valid. `"eksen kayması"` (axis shift) is high-signal for Turkey's hedging posture between NATO and Russia. Add `"Fidan dış politika"` as a leader-specific pattern — Hakan Fidan as FM is the primary diplomatic actor. Add `"Astana süreci"` (Astana process) for Syria peace architecture. `"arabuluculuk"` (mediation) is excellent — Turkey's mediator self-image is a defining foreign policy narrative. Consider adding `"tahıl koridoru"` (grain corridor) for Black Sea diplomacy.
- **Domain 2 (Security):** Strong list. `"yerli ve milli"` (indigenous and national) is the single most important term — it's the slogan driving Turkey's entire defense-industrial strategy. Add `"KAAN"` (5th-gen fighter), `"Bayraktar"` (TB2/Akıncı drones), `"MILGEM"` (corvette program) as specific procurement terms. Add `"sınır ötesi operasyon"` (cross-border operation) for Syria/Iraq military actions. `"İHA"` / `"SİHA"` are correct — pair with `"ihracat"` (export) for defense export tracking.
- **Domain 3 (Economic):** Excellent. Add `"lira krizi"` (lira crisis) — even if not active, queries on currency stability surface TCMB policy stories. Add `"enerji koridoru"` (energy corridor) and `"doğalgaz"` (natural gas) for pipeline diplomacy. `"cari açık"` (current account deficit) is the structural constraint defining Turkey's economic statecraft. Add `"Rusya yaptırımları"` (Russia sanctions) for sanctions navigation coverage.
- **Domain 4 (Institutional):** Valid. `"Türk Devletleri Teşkilatı"` (Organization of Turkic States) is increasingly important — Turkey's pan-Turkic institutional project. Add `"AB müzakereleri"` (EU negotiations) — distinct from `"AB üyelik süreci"` and more search-active. `"G20"` is relevant — Turkey's G20 positioning. Add `"D-8"` (Developing 8 organization, Turkey-led).
- **Domain 5 (Domestic):** Strong. Add `"İmamoğlu davası"` (İmamoğlu trial) — the defining domestic-judicial story. Add `"Kürt barış süreci"` (Kurdish peace process) — the Erdoğan-Bahçeli-Öcalan negotiations are the top blind spot. Add `"anayasa değişikliği referandum"` (constitutional amendment referendum) — linked to Kurdish peace process. `"basın özgürlüğü"` (press freedom) is correct and essential.

**Stale/problematic terms:** None are stale. All terms in the curation prompt remain active in Turkish political discourse as of March 2026.

**Suggested topic query patterns:**

1. `Erdoğan Fidan NATO stratejik ortaklık` — NATO posture and alliance management
2. `savunma sanayii yerli ve milli KAAN Bayraktar ihracat` — Defense industry and exports
3. `TCMB faiz kararı lira cari açık` — Central bank policy and economic constraints
4. `Kürt barış süreci Öcalan DEM anayasa` — Kurdish peace process and constitutional reform
5. `Türkiye Rusya doğalgaz yaptırım enerji` — Russia relations, energy, sanctions navigation
6. `İmamoğlu davası muhalefet seçim` — Opposition dynamics and judicial independence
7. `Suriye sınır ötesi operasyon Astana` — Syria policy and military operations

---

## GOGGLE FILE

```goggle
! name: MPM Turkey
! description: MPM pipeline source prioritization for Turkey — boosts high-signal sources, discards noise
! public: false
! author: MPM Pipeline

! --- Tier 1: Essential (boost=3) ---
$boost=3,site=anadolu.com.tr
$boost=3,site=cumhuriyet.com.tr
$boost=3,site=t24.com.tr
$boost=3,site=bloomberght.com
$boost=3,site=al-monitor.com

! --- Tier 2: Important (boost=2) ---
$boost=2,site=hurriyet.com.tr
$boost=2,site=sozcu.com.tr
$boost=2,site=medyascope.tv
$boost=2,site=bianet.org
$boost=2,site=tccb.gov.tr
$boost=2,site=mfa.gov.tr
$boost=2,site=resmigazete.gov.tr
$boost=2,site=tbmm.gov.tr
$boost=2,site=middleeasteye.net
$boost=2,site=setav.org
$boost=2,site=mezopotamyaajansi42.com

! --- Tier 3: Supplementary (boost=1) ---
$boost=1,site=hurriyetdailynews.com
$boost=1,site=dailysabah.com
$boost=1,site=birgun.net
$boost=1,site=defenceturkey.com
$boost=1,site=c4defence.com
$boost=1,site=duvarenglish.com
$boost=1,site=ahvalnews.com

! --- Discard: Noise ---
$discard,site=yeniakit.com.tr
$discard,site=odatv.com
$discard,site=haber7.com
$discard,site=takvim.com.tr
```

---

## INTERPRETIVE CONTEXT FOR DOSSIER

### Tier 1 Sources

> Articles from **Anadolu Agency (AA)** about any domain should be interpreted as the Turkish state's intended messaging — AA is the government's primary communication instrument, and its framing choices (what it emphasizes, what it omits, what language it uses) are themselves intelligence signals about Ankara's posture. AA reporting on defense exports, NATO engagements, or Russia relations reflects what the government wants audiences to believe, not necessarily operational reality.

> Articles from **Cumhuriyet** about foreign policy and NATO posture should be interpreted as filtered through a secular-Kemalist opposition lens — Cumhuriyet's editorial line favors stronger Western/NATO alignment, skepticism of Erdoğan's Russia engagement, and opposition to AKP's Islamist-informed foreign policy. Its critique is institutionally grounded (it's Turkey's oldest newspaper) but systematically frames AKP foreign policy as a departure from Atatürkist principles. Valuable for surfacing opposition foreign policy positions but not representative of median Turkish public opinion.

> Articles from **T24** about institutional erosion and foreign policy should be interpreted as Turkey's highest-quality independent analytical journalism — its editorial independence is genuine (no government advertising dependence, no oligarch ownership), but the Google traffic collapse affecting Turkish independents means its reach and thus its source access may be declining. When T24 publishes analytical pieces, the quality is high and the framing is liberal-democratic.

> Articles from **Bloomberg HT** about economic policy should be interpreted as reflecting Turkey's financial-market perspective because its Bloomberg partnership and financial-analytical orientation mean it frames TCMB decisions, trade policy, and energy economics through an investment-climate lens — negative coverage of unorthodox monetary policy does not necessarily mean the policy is failing, only that market actors view it unfavorably. The most reliable source for economic data reporting in Turkey.

> Articles from **Al-Monitor** about Turkey's regional posture should be interpreted as the most balanced English-language analytical source available — its dedicated Turkey desk with Ankara-based correspondents provides original reporting, and its Washington editorial base adds a U.S./Western policy frame. Al-Monitor's analysis tends toward realist/pragmatic rather than ideological, making it the most useful single source for understanding how Turkey's domestic politics map onto its external behavior.

### Tier 2 Sources

> Articles from **Hurriyet** about economic policy and business-government relations should be interpreted with awareness that post-2018 Demiroren Group ownership aligned the newspaper with AKP positions — Hurriyet's economic coverage reflects the government-business consensus rather than independent reporting. Its value lies precisely in revealing what that consensus is, particularly on defense procurement economics, infrastructure projects, and trade partnerships.

> Articles from **Sozcu** about government policy should be interpreted as secular-nationalist opposition — Sozcu's mass-market readership and populist editorial style mean it amplifies popular opposition anger rather than providing nuanced analysis. RTUK broadcast bans on Sozcu TV are themselves an intelligence signal about the government's sensitivity to opposition narratives. Useful for gauging opposition intensity, less useful for analytical depth.

> Articles from **Medyascope** about any domain should be interpreted as reflecting Turkey's informed-expert class — its panel format brings together academics, former diplomats, and security analysts who cannot publish freely in mainstream media. The signal is in who participates and what they say, not in Medyascope's own editorial line. Consider Medyascope content as elite-dissent intelligence.

> Articles from **Bianet** about press freedom, minority rights, and EU-Turkey relations should be interpreted as rights-based advocacy journalism — Bianet systematically documents press freedom violations, judicial proceedings against journalists, and EU accession benchmarks. Its framing is consistently critical of government human rights performance, which is both its value (systematic documentation) and its limitation (frames ambiguous events through a rights lens).

> Articles from **Middle East Eye** about Turkey's Syria and Libya operations should be interpreted as high-quality investigative reporting with an editorial orientation sometimes aligned with Qatari interests — MEE's Turkey coverage is among the best in English for regional military and diplomatic dynamics, but its framing of Turkey's regional role may be more sympathetic than Western outlets. Cross-reference with Al-Monitor for balanced assessment.

> Articles from **SETA / Insight Turkey** about foreign and security policy should be interpreted as the intellectual framework behind AKP governance — SETA is government-proximate, and its publications reveal how the ruling party's policy intellectuals conceptualize Turkey's role (strategic autonomy, neo-Ottoman sphere of influence, "valuable loneliness" doctrine). Not independent analysis but primary source material on the government's strategic thinking.

> Articles from **government official sources** (tccb.gov.tr, mfa.gov.tr, resmigazete.gov.tr, tbmm.gov.tr) should be interpreted as official communications — not journalism but primary source material. Presidential decrees, foreign ministry statements, official gazette publications, and parliamentary records represent the government's formal position, which may diverge from actual implementation or from informal signaling through AA and Daily Sabah.

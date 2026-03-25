# AUDIT SUMMARY: INDONESIA

**Sources assessed:** 17 recommended + 5 excluded + 4 newly identified = 26 total
**Tier 1 (boost=3):** 4 sources
**Tier 2 (boost=2):** 8 sources
**Tier 3 (boost=1):** 5 sources
**Neutral (no rule):** 6 sources
**Discard:** 3 sources
**Overall assessment:** The curation prompt produced a strong whitelist with excellent structural coverage across all five posture domains, including the critical Islamic-constituency channel (Republika) that many country maps would miss. Key changes: (1) resolved redundancy in the economic/business press cluster (CNBC Indonesia, Kontan, Bisnis Indonesia) by differentiating tiers based on domain uniqueness; (2) promoted government official sources (Kemlu, Setkab, Kemhan) for Layer 2 migration at Tier 2; (3) applied non-English domestic boost premium to Bahasa Indonesia sources that provide depth inaccessible in English; (4) added missing structural roles (regional analytical platform, parliamentary monitor); (5) confirmed no Indonesian domains appear on the blocked domains list — clean extraction across the full whitelist. The `reuters.com` wire in `id.yaml` is blocked by Anthropic's crawler but this only affects wire fallback, not core domestic sourcing.

---

## BOOST ASSIGNMENTS

### Tier 1 — `$boost=3`

**Kompas / Kompas.id** | `kompas.id` / `kompas.com` | Type: `paper_of_record` | Status: `EXISTING`
- **Structural role:** Indonesia's newspaper of record and most trusted print brand (~65% trust rating). Functions as the barometer of elite consensus on foreign policy. Columnists include former diplomats and senior academics.
- **Domain coverage:** All five domains; strongest on diplomatic alignment, domestic constraints
- **Reasoning:** Kompas is the indispensable source for Indonesia. Its editorials and op-eds set the terms of policy debate within the Indonesian establishment. The `kompas.id` premium edition is the higher-value target (paywalled), but `kompas.com` (free portal) provides supplementary volume coverage. Both domains get Tier 1 to ensure either path surfaces. Non-English domestic boost premium applies — Kompas's Bahasa Indonesia coverage contains signals invisible in English-language outlets.
- **Extraction note:** `kompas.id` is paywalled; Diffbot extraction may be partial. `kompas.com` is free but lower quality. Both domains boosted to capture whichever is extractable.

**Tempo / Tempo.co** | `tempo.co` / `en.tempo.co` | Type: `investigative` | Status: `EXISTING`
- **Structural role:** Indonesia's only outlet that consistently publishes investigative series on defense procurement corruption, intelligence agency activities, and elite political maneuvering. Twice banned under Suharto; continues to face physical threats (severed animal heads delivered to newsroom in 2024).
- **Domain coverage:** Domestic constraints, Security & defense, Diplomatic alignment
- **Reasoning:** Tempo fills the dual role of investigative outlet and newsmagazine of record — there is no Indonesian equivalent. Its reporting reveals friction and dissent invisible in wire copy or portal coverage. The English edition (`en.tempo.co`) provides translated summaries but the Bahasa Indonesian edition is the primary intelligence source. Non-English domestic boost premium applies. Metered paywall — partial extraction likely.

**Antara** | `antaranews.com` / `en.antaranews.com` | Type: `state_wire` | Status: `EXISTING`
- **Structural role:** Indonesia's sole state wire service and the first-mover channel for presidential statements, MFA communiques, defense procurement announcements, and ASEAN positioning. Changes in Antara's language and emphasis are themselves posture indicators.
- **Domain coverage:** Diplomatic alignment, Security & defense, Institutional engagement
- **Reasoning:** Structural role outweighs quality per boost principles. Antara's wire copy reflects official government framing — what appears there is what the state wants disseminated. The pipeline needs this signal to detect posture shifts at the source. Free and easily extractable in both Indonesian and English. The English feed lags Indonesian by hours, but both are pipeline-viable. Note: Xinhua partnership means some republished Chinese state content appears — the interpretive context handles this.

**The Jakarta Post** | `thejakartapost.com` | Type: `english_language_daily` | Status: `EXISTING`
- **Structural role:** Primary English-language source for Indonesian foreign policy discourse. Op-ed page regularly features serving and former diplomats, CSIS Jakarta fellows, and ASEAN policy figures. Co-owned by Kompas (25%) and Tempo (15%).
- **Domain coverage:** All five domains; strongest on diplomatic alignment, economic statecraft, institutional engagement
- **Reasoning:** The Jakarta Post is the gateway source for the English-language pipeline layer. Its op-ed page is where Indonesian policy elites communicate with the international community — what appears there signals how Indonesia wants to be understood externally. Soft paywall; limited free articles per month. Tier 1 because it is the single indispensable English-language source and the pipeline's `languages.metadata: en` configuration depends on it.

---

### Tier 2 — `$boost=2`

**CNN Indonesia** | `cnnindonesia.com` | Type: `mainstream_portal` | Status: `EXISTING`
- **Structural role:** Provides structured political news coverage with regular interviews of cabinet ministers and military officials. Higher editorial standard than Detik within the same Trans Media / CT Corp corporate family. CNN branding lends international credibility.
- **Domain coverage:** Diplomatic alignment, Domestic constraints, Security & defense
- **Reasoning:** CNN Indonesia occupies the sweet spot between Detik's speed and Kompas's depth. Its international desk covers bilateral relationships and multilateral positioning with more structure than portal competitors. Tier 2 rather than Tier 1 because it breaks fewer stories than Kompas or Tempo and shares Trans Media ownership with Detik (Chairul Tanjung / CT Corp), creating structural caution on business-government stories.

**CNBC Indonesia** | `cnbcindonesia.com` | Type: `business_financial` | Status: `EXISTING`
- **Structural role:** Best single source for economic statecraft signals: commodity export controls (nickel, palm oil), investment screening, digital economy regulation, sovereign wealth fund (Danantara) activity, and trade agreement implementation.
- **Domain coverage:** Economic & technological statecraft
- **Reasoning:** CNBC Indonesia is the Tier 1 candidate for economic statecraft but drops to Tier 2 because its single-domain coverage limits structural breadth. Within the economic statecraft domain, it is the first-mover — market reactions to policy changes surface here before they appear in Kompas or Kontan. Free and extractable.

**Tirto.id** | `tirto.id` | Type: `independent_digital` / `fact_check` | Status: `EXISTING`
- **Structural role:** Data-driven, fact-check oriented independent outlet. First Indonesian member of IFCN. Fills the analytical gap between wire-speed portals and Tempo's investigative work. Targeted by cyberattacks, indicating its reporting generates official discomfort.
- **Domain coverage:** Domestic constraints, Diplomatic alignment, Institutional engagement
- **Reasoning:** Tirto's long-form, data-backed reporting is structurally unique in the Indonesian ecosystem — no other outlet combines fact-checking rigor with policy analysis at this depth. Strong on legislative tracking and debunking official narratives. Tier 2 for analytical depth. Not Tier 1 because it is newer (founded 2016), smaller, and its reach is limited to younger educated readers. Non-English domestic boost premium applies.

**Republika** | `republika.co.id` | Type: `constituency_outlet` → `islamic_constituency` | Status: `EXISTING`
- **Structural role:** Essential for monitoring the Islamic constituency's influence on foreign policy — Indonesia's largest domestic constraint channel. Provides coverage of Palestine, OIC engagement, relations with Saudi Arabia/Turkey/Iran, and domestic Islamist political mobilization.
- **Domain coverage:** Domestic constraints, Diplomatic alignment (OIC, Palestine, Muslim-majority bilateral relations)
- **Reasoning:** The curation prompt typed this as an Islamic-oriented news portal, but its actual structural function is as a **constituency signal channel**. What Republika covers — and how it frames it — reveals the preferences and red lines of Indonesia's largest political constituency (mainstream Muslim organizations). This is a domestic constraint signal unavailable in secular outlets. Tier 2 because structural role outweighs editorial quality per boost principles. Non-English domestic boost premium applies.

**Kemlu.go.id (Ministry of Foreign Affairs)** | `kemlu.go.id` | Type: `government_primary` | Status: `EXISTING` — **LAYER 2 MIGRATION**
- **Structural role:** Direct access to press releases, ministerial speeches, annual foreign policy statements, and treaty/agreement announcements. The Annual Press Statement of the Minister for Foreign Affairs is a key annual posture document.
- **Domain coverage:** Diplomatic alignment, Institutional engagement
- **Reasoning:** Primary fetch via Layer 2 direct polling. Goggle boost at Tier 2 as belt-and-suspenders fallback. Government sources earn Tier 2 per audit principles. Changes in diplomatic language, partner-country prioritization, and issue framing are detectable through systematic monitoring.

**Setkab.go.id (Cabinet Secretariat)** | `setkab.go.id` | Type: `government_primary` | Status: `EXISTING` — **LAYER 2 MIGRATION**
- **Structural role:** Publishes presidential regulations (Perpres), cabinet meeting outcomes, and official readouts of bilateral/multilateral summits. Defense budget decisions, trade policy directives, and institutional reform mandates appear here before media coverage.
- **Domain coverage:** All five domains (presidential directives, cabinet decisions)
- **Reasoning:** Primary fetch via Layer 2 direct polling. Goggle boost at Tier 2 as belt-and-suspenders fallback. Setkab is where executive-level posture decisions appear first — before Antara, before Kompas. English section available at `setkab.go.id/en/`.

**Kemhan.go.id (Ministry of Defense)** | `kemhan.go.id` | Type: `government_primary` | Status: `EXISTING` — **LAYER 2 MIGRATION**
- **Structural role:** Primary source for defense white papers, procurement regulations, military exercise announcements, and defense cooperation agreements. Indonesia's $125B modernization plan, Rafale and Scorpene acquisitions, and defense industry indigenization policies are documented here.
- **Domain coverage:** Security & defense autonomy
- **Reasoning:** Primary fetch via Layer 2 direct polling. Goggle boost at Tier 2 as belt-and-suspenders fallback. Single-domain but irreplaceable within it — procurement regulation changes signal shifts in supplier diversification strategy. Indonesian language only; limited structured data.

**CSIS Jakarta** | `csis.or.id` | Type: `think_tank` | Status: `EXISTING`
- **Structural role:** Indonesia's premier foreign policy think tank, ranked #1 in Southeast Asia/Pacific. Founded 1971. Researchers frequently advise government; analyses often preview policy shifts before they become official. Produces the annual "Indonesia and the World" survey.
- **Domain coverage:** Diplomatic alignment, Security & defense, Institutional engagement
- **Reasoning:** Think tanks earn boost through depth, not speed. CSIS publications and policy briefs are leading indicators of elite foreign policy debate — what CSIS Jakarta publishes today often becomes government policy within months. Tier 2 for analytical depth. Not Tier 1 because it doesn't break news and publishes less frequently than dailies. Bilingual (Indonesian and English) output is a practical advantage.

---

### Tier 3 — `$boost=1`

**Kontan** | `kontan.co.id` | Type: `business_financial` | Status: `EXISTING`
- **Structural role:** Financial daily with granular coverage of fiscal policy, state-owned enterprise reform, downstream industrial policy (critical minerals processing mandates), and banking sector developments. Part of Kompas Gramedia group but editorially distinct.
- **Domain coverage:** Economic & technological statecraft
- **Reasoning:** Complements CNBC Indonesia with deeper financial detail but creates redundancy within the economic statecraft domain. Tier 3 rather than Tier 2 because its coverage overlaps significantly with CNBC Indonesia (which has faster turnaround) and Bisnis Indonesia (which has broader industrial policy coverage). Partially paywalled — extraction may be partial.

**Bisnis Indonesia** | `bisnis.com` | Type: `business_financial` | Status: `EXISTING`
- **Structural role:** Covers downstream industrial policy (nickel export bans, smelter mandates), sovereign wealth fund (Danantara) activities, digital economy regulation, and bilateral trade negotiations with granular detail.
- **Domain coverage:** Economic & technological statecraft
- **Reasoning:** Provides the supply-chain and industrial-policy layer that CNBC Indonesia covers at headline level. Tier 3 rather than Tier 2 because three economic statecraft sources at Tier 2+ would over-weight the domain in search results. Bisnis provides supplementary depth when CNBC Indonesia's headline coverage is insufficient. Partially paywalled.

**Jakarta Globe** | `jakartaglobe.id` | Type: `english_language_digital` | Status: `EXISTING`
- **Structural role:** Second English-language perspective with faster turnaround on economic policy and business diplomacy. Lippo Group ownership lends pro-market orientation.
- **Domain coverage:** Economic statecraft, Diplomatic alignment, Security & defense
- **Reasoning:** Tier 3 rather than Tier 2 because it is less editorially independent than The Jakarta Post (Lippo Group ownership) and its original reporting rate is lower. Useful for triangulating against Jakarta Post framing, but not essential. Free and extractable, which keeps it practically useful despite the lower boost.

**Fulcrum / ISEAS-Yusof Ishak Institute** | `fulcrum.sg` / `iseas.edu.sg` | Type: `regional_think_tank` | Status: `EXISTING`
- **Structural role:** Publishes the annual "State of Southeast Asia" survey — the single best structured dataset on Indonesia's alignment preferences. Singapore-based, English-language, providing analytical depth on Indonesia's ASEAN posture and great-power hedging that domestic outlets cannot safely publish.
- **Domain coverage:** All five domains (external analytical perspective)
- **Reasoning:** External analytical perspective fills the self-censorship gap in domestic media. Tier 3 rather than Tier 2 because it is not Indonesia-specific (covers all of Southeast Asia) and its publication frequency is lower than CSIS Jakarta. But when it publishes Indonesia analysis, the quality and independence are unmatched. Both `fulcrum.sg` and `iseas.edu.sg` domains boosted.

**Presidenri.go.id (Presidential Office)** | `presidenri.go.id` | Type: `government_primary` | Status: `FROM id.yaml` — **LAYER 2 MIGRATION**
- **Structural role:** Presidential office website. Houses presidential speeches, state visit readouts, and executive communications. Listed in `id.yaml` as a Tier 1 government source but not in the source intelligence map.
- **Domain coverage:** All five domains (presidential-level)
- **Reasoning:** Present in `id.yaml` but absent from the source intelligence map — added here for completeness. Primary fetch via Layer 2 direct polling. Goggle boost at Tier 3 (lower than other government sources because Setkab provides more structured cabinet-level output and Antara picks up presidential statements faster). Belt-and-suspenders fallback.

---

### Neutral — no Goggle rule

**Detik.com** | `detik.com` / `news.detik.com` | Type: `high_volume_portal` | Status: `EXISTING → DEMOTED TO NEUTRAL`
- **Why neutral:** Detik is Indonesia's #1 news site (~180M daily visits) and surfaces breaking developments faster than any competitor. But its value is as an event-detection layer, not an analytical source — "Mostly Factual" MBFC rating due to sourcing weaknesses, minimal editorial depth, and Chairul Tanjung ownership creates structural caution. Under the Goggle model, Detik will surface organically for any Indonesian news query due to its massive traffic and domain authority. Boosting it would displace higher-signal analytical sources from top results. Neutral allows it to appear organically without crowding out Kompas, Tempo, and Tirto.

**VIVAnews / tvOne (Bakrie Group)** | `vivanews.com` | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Curation exclusion was correct under the hard-filter model — Golkar-party alignment and patron-driven coverage introduce more noise than signal. Under the Goggle model, no reason to actively discard. VIVAnews may surface organically for specific Golkar or coalition politics queries, and party-aligned framing is itself a signal when the interpretive context tells the LLM how to read it.

**Media Indonesia (Surya Paloh / NasDem)** | `mediaindonesia.com` | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Same logic as VIVAnews. Directly owned by the NasDem party founder, making its coverage instrumentalized for party positioning. But under the Goggle model, exclusions default to Neutral not Discard. If Media Indonesia breaks a NasDem foreign policy position, the pipeline benefits from seeing it organically.

**Kumparan** | `kumparan.com` | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Digital-native aggregation platform with significant traffic but limited original reporting. User-generated and AI-curated content model makes it unreliable for authoritative sourcing. But high traffic means Brave may surface it for trending Indonesian stories. Neutral allows organic discovery without displacing boosted sources.

**Coconuts Jakarta** | `coconuts.co/jakarta/` | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** English-language lifestyle/alternative news site. Lacks policy depth for strategic posture monitoring. But under the Goggle model, no reason to actively discard — it may surface for niche cultural-political stories. Organic ranking is appropriate.

**BenarNews / Radio Free Asia** | `benarnews.org` | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Shut down in May 2025 following Trump administration defunding. No longer an active source. Neutral rather than Discard because archived content may still surface for historical context queries. No reason to actively suppress a defunct outlet.

---

### Discard — `$discard`

**El Chapucero-style commentary channels** — No known Indonesian equivalents identified at this time. Indonesia's noise sources are more likely to be aggregation platforms (handled at Neutral) than YouTube-based commentary channels.

**Tribunnews** | `tribunnews.com` | Status: `NEW DISCARD`
- **Discard reasoning:** Indonesia's highest-traffic news aggregator (Kompas Gramedia subsidiary) that relies almost entirely on clickbait rewrites, wire aggregation, and SEO-optimized content farming. Despite sharing the Kompas Gramedia parent company, Tribunnews has no editorial relationship with Kompas.id — it is a separate product designed for traffic maximization. Its massive domain authority means it would crowd out genuine Kompas content in search results if not discarded. Active suppression is warranted because its SEO optimization would otherwise dominate Indonesian-language query results.

**Suara.com** | `suara.com` | Status: `NEW DISCARD`
- **Discard reasoning:** High-traffic digital portal relying on clickbait headlines and aggregated content with minimal original reporting on foreign policy or defense. Would waste result slots that should go to substantive sources. Similar structural profile to Tribunnews — SEO-optimized content farming.

**Merdeka.com** | `merdeka.com` | Status: `NEW DISCARD`
- **Discard reasoning:** Another high-traffic portal in the clickbait aggregation category. Its coverage of politics is primarily personality-driven gossip rather than policy analysis. Would inject noise and displace analytical sources from top results.

---

## STRUCTURAL COVERAGE CHECK

| Structural Role | Source(s) | Tier | Notes |
|---|---|---|---|
| Government signal channel | Antara | T1 | State wire service reflects official framing. Changes in Antara's language are posture indicators. Xinhua partnership content requires filtering |
| Opposition voice | Tempo, Tirto.id | T1, T2 | No dedicated opposition outlet (PDI-P lacks a media vehicle). Tempo and Tirto provide independent critical coverage that surfaces elite dissent |
| Defence/security first-mover | Tempo, Kemhan.go.id | T1, T2 | No dedicated defence press in Indonesia. Tempo is the only outlet that intermittently penetrates military/intelligence dynamics. Kemhan for official procurement and exercise announcements |
| Policy-elite discourse | Kompas, CSIS Jakarta, The Jakarta Post | T1, T2, T1 | Kompas editorials for domestic elite consensus; CSIS Jakarta for foreign policy debate; Jakarta Post op-eds for how elites communicate externally |
| Domestic-language depth | Kompas, Tempo, Tirto, Republika, Antara, CNN Indonesia, CNBC Indonesia, Kontan, Bisnis | T1–T3 | Bahasa Indonesia is the primary language of political discourse. English sources (Jakarta Post, Jakarta Globe, Fulcrum) are supplements, not substitutes. Non-English domestic boost premium applied |
| Official government source | Kemlu, Setkab, Kemhan, Presidenri | T2–T3 | **LAYER 2 MIGRATION** — primary fetch via direct polling. Goggle boost as fallback. Covers foreign affairs, cabinet decisions, defense, and presidential communications |
| Analytical/think tank depth | CSIS Jakarta, Fulcrum/ISEAS | T2, T3 | CSIS Jakarta for domestic policy debate; ISEAS/Fulcrum for external comparative analysis and the "State of Southeast Asia" survey |
| Economic statecraft specialist | CNBC Indonesia, Kontan, Bisnis Indonesia | T2, T3, T3 | Three-source cluster differentiated by speed (CNBC), financial depth (Kontan), and industrial policy (Bisnis) |
| Islamic constituency signal | Republika | T2 | Unique structural role — no other source captures the preferences and red lines of Indonesia's largest political constituency on foreign policy |
| Wire service (international) | Reuters, AP News, France24 | Neutral | Listed in `id.yaml` wire section. Not boosted in Goggle — wire copy available organically. Reuters is blocked by Anthropic crawler but Brave can still surface it for discovery |

**Gaps identified:**
1. **Military and intelligence community internal dynamics** remain a structural blind spot — all Indonesian media practice self-censorship due to legal constraints (ITE law, revised penal code) and physical threats. Tempo is the only outlet that intermittently penetrates this space, and even its coverage is episodic. No mitigation available through additional sourcing — this is a systemic media-freedom constraint.
2. **Sub-national and outer-island perspectives** on border security (Papua, Natuna, North Kalimantan) and maritime domain awareness are underserved by Jakarta-centric national media. Local outlets in these regions lack the reach and editorial capacity to be pipeline-viable. Supplementation from Lowy Institute's "The Interpreter" and IISS reporting recommended for external assessments.
3. **Parliamentary monitoring** is weak — no source systematically tracks DPR committee proceedings, ratification debates, or defense budget deliberations at the granular level needed for domestic constraint detection. Kompas and Tempo cover major parliamentary events but not committee-level proceedings.
4. **Danantara sovereign wealth fund governance** — identified as a blind spot in `id.yaml`. The ~$570B SOE consolidation under political management has minimal independent oversight. Tempo and Kompas investigative coverage is the best available but episodic.

---

## REDUNDANCY RESOLUTION

**Economic statecraft cluster: CNBC Indonesia + Kontan + Bisnis Indonesia**
Three sources covering economic statecraft creates redundancy risk. Resolved by differentiating speed vs. depth: CNBC Indonesia (Tier 2, market-speed coverage, first-mover on policy reactions), Kontan (Tier 3, granular financial data, fiscal policy detail), Bisnis Indonesia (Tier 3, supply-chain and industrial policy depth). The pipeline gets headline economic signals from CNBC Indonesia and supplementary detail from Kontan/Bisnis when deeper analysis is needed. Boosting all three at Tier 2 would over-weight economic statecraft in search results at the expense of other domains.

**English-language cluster: Jakarta Post + Jakarta Globe**
Both are English-language dailies covering similar domains. Jakarta Post leads (Tier 1) due to editorial independence (co-owned by Kompas and Tempo), op-ed quality (serving diplomats and CSIS fellows), and deeper policy coverage. Jakarta Globe drops to Tier 3 — Lippo Group ownership reduces editorial independence, and its original reporting rate is lower. The pipeline gets English-language access primarily through Jakarta Post; Jakarta Globe provides triangulation and faster turnaround on business stories.

**Government source cluster: Kemlu + Setkab + Kemhan + Presidenri**
Four government sources could create redundancy, but each covers a distinct institutional domain: Kemlu (foreign affairs), Setkab (cabinet decisions), Kemhan (defense procurement), Presidenri (presidential communications). All at Tier 2–3 with Layer 2 migration — primary fetch via direct polling, Goggle boost as fallback. No redundancy reduction needed because institutional separation is clean.

**Portal cluster: Detik + CNN Indonesia**
Both belong to Trans Media / CT Corp (Chairul Tanjung). Resolved by differentiating editorial quality: CNN Indonesia (Tier 2, structured political coverage, ministerial interviews) vs. Detik (Neutral, high-volume event detection only). Boosting both would double-count the same corporate editorial filter. CNN Indonesia gets the boost because it produces more analytical content; Detik surfaces organically due to massive traffic.

**Investigative/independent cluster: Tempo + Tirto.id**
Both provide independent, critical coverage, but their methods differ: Tempo (Tier 1, long-form investigative series, institutional memory, security/defense depth) vs. Tirto (Tier 2, data-driven fact-checking, policy explainers, legislative tracking). No redundancy — complementary approaches to independent journalism.

---

## QUERY CONFIGURATION

```
country: ID
search_lang: id
freshness: pw
```

**Multi-language notes:** Indonesia's political discourse operates primarily in Bahasa Indonesia. English-language sources (Jakarta Post, Jakarta Globe, Fulcrum/ISEAS) provide essential access for the pipeline's metadata layer but miss signals available only in Indonesian. Queries should run primarily in Indonesian; a secondary English query cycle captures Jakarta Post analysis and international think tank coverage. The pipeline's existing `languages.primary: id` and `languages.metadata: en` configuration handles this correctly.

**Localized query vocabulary validation:**

The curation prompt's vocabulary is strong. Notes:

- **Domain 1 (Diplomatic):** All terms valid. `"politik luar negeri bebas aktif"` is the foundational doctrinal formula — essential for detecting any departure from Indonesia's non-aligned posture. Add `"Prabowo diplomasi"` and `"Retno Marsudi"` (if still serving) or current foreign minister as leader-specific patterns. `"poros maritim"` is a Jokowi-era term — may be declining under Prabowo. Consider adding `"kemitraan komprehensif"` (comprehensive partnership) for bilateral upgrade signals and `"ASEAN outlook Indo-Pasifik"` (ASEAN Outlook on the Indo-Pacific).
- **Domain 2 (Security):** Strong list. Add `"Prabowo pertahanan"` (Prabowo defense) as a leader-specific pattern. `"alutsista"` is the essential term — Indonesia-specific acronym for major weapons systems. Add `"Rafale"` and `"Scorpene"` for active procurement tracking. Add `"Natuna"` for South China Sea territorial dynamics. `"keamanan maritim"` is good but consider pairing: `"keamanan maritim Laut China Selatan"` for specificity.
- **Domain 3 (Economic):** Excellent. `"hilirisasi"` (downstream processing) is the signature economic statecraft term — Indonesia's nickel export ban and smelter mandates are the defining case study. Add `"Danantara"` for sovereign wealth fund tracking. Add `"nikel"` (nickel) and `"kelapa sawit"` (palm oil) as commodity-specific terms. `"ekonomi digital"` is correct — add `"Starlink"` and `"data center"` for tech statecraft tracking.
- **Domain 4 (Institutional):** Valid. `"keketuaan ASEAN"` and `"sentralitas ASEAN"` are essential Indonesia-specific terms. Add `"G20"` (Indonesia hosted 2022, ongoing engagement). Add `"MIKTA"` (Mexico-Indonesia-Korea-Turkey-Australia grouping). `"hukum laut internasional"` is important for UNCLOS/South China Sea framing.
- **Domain 5 (Domestic):** Strong. Add `"Danantara kontrol"` for sovereign wealth fund governance concerns. Add `"revisi UU ITE"` (ITE law revision) — the defining press freedom constraint. Add `"koalisi gemuk"` (fat coalition) for Prabowo's governing coalition dynamics. `"ormas Islam"` is essential — add `"Muhammadiyah"` and `"Nahdlatul Ulama"` as specific organization terms. Add `"ibu kota nusantara"` / `"IKN"` for capital relocation tracking.

**Stale/problematic terms:** `"poros maritim"` (maritime axis) is a Jokowi-era concept that may be declining under Prabowo's presidency — monitor for continued usage. All other terms remain active.

**Suggested topic query patterns:**

1. `Prabowo alutsista modernisasi TNI Rafale` — Defense modernization and procurement
2. `hilirisasi nikel larangan ekspor investasi asing` — Downstream processing policy and foreign investment
3. `politik luar negeri bebas aktif ASEAN Laut China Selatan` — Non-aligned posture and South China Sea
4. `Danantara BUMN tata kelola` — Sovereign wealth fund and SOE governance
5. `koalisi pemerintah DPR ratifikasi anggaran pertahanan` — Coalition dynamics and defense budget
6. `kemitraan strategis bilateral Prabowo` — Bilateral partnership upgrades under Prabowo
7. `ormas Islam Muhammadiyah Nahdlatul Ulama kebijakan luar negeri` — Islamic constituency foreign policy influence

---

## GOGGLE FILE

```goggle
! name: MPM Indonesia
! description: MPM pipeline source prioritization for Indonesia — boosts high-signal sources, discards noise
! public: false
! author: MPM Pipeline

! --- Tier 1: Essential (boost=3) ---
$boost=3,site=kompas.id
$boost=3,site=kompas.com
$boost=3,site=tempo.co
$boost=3,site=en.tempo.co
$boost=3,site=antaranews.com
$boost=3,site=en.antaranews.com
$boost=3,site=thejakartapost.com

! --- Tier 2: Important (boost=2) ---
$boost=2,site=cnnindonesia.com
$boost=2,site=cnbcindonesia.com
$boost=2,site=tirto.id
$boost=2,site=republika.co.id
$boost=2,site=kemlu.go.id
$boost=2,site=setkab.go.id
$boost=2,site=kemhan.go.id
$boost=2,site=csis.or.id

! --- Tier 3: Supplementary (boost=1) ---
$boost=1,site=kontan.co.id
$boost=1,site=bisnis.com
$boost=1,site=jakartaglobe.id
$boost=1,site=fulcrum.sg
$boost=1,site=iseas.edu.sg
$boost=1,site=presidenri.go.id

! --- Discard: Noise ---
$discard,site=tribunnews.com
$discard,site=suara.com
$discard,site=merdeka.com
```

---

## INTERPRETIVE CONTEXT FOR DOSSIER

### Tier 1 Sources

> Articles from **Kompas** about any domain should be interpreted as reflecting Indonesian elite consensus — its centrist-nationalist editorial line and Catholic-founded but broadly secular identity make it the most trusted barometer of establishment thinking. Kompas editorials featuring former diplomats and senior academics signal where the foreign policy elite has converged. If Kompas is cautious on a topic, it likely reflects a real political sensitivity.

> Articles from **Tempo** about military and security affairs should be interpreted as Indonesia's most authoritative investigative reporting on the security apparatus — its reform-oriented editorial stance means it frames military expansion and intelligence overreach critically, but its sourcing within the defense establishment is deeper than any other outlet's. Tempo investigations that survive legal and physical threats (the outlet continues to face intimidation) carry high credibility precisely because of the cost of publishing them.

> Articles from **Antara** about foreign policy and defense should be interpreted as official government framing — not independent journalism but a primary source for how the Indonesian state wants its posture understood. Changes in Antara's language, emphasis, or partner-country coverage order are themselves posture indicators. Note: Xinhua partnership means some content republished from Chinese state media appears on the site — verify attribution before treating as Indonesian government positioning.

> Articles from **The Jakarta Post** about diplomatic and institutional affairs should be interpreted as how Indonesia's policy elite communicates with the international community — its op-ed contributors (serving diplomats, CSIS Jakarta fellows, ASEAN figures) are writing for a foreign audience, which means their framing may be more candid about alignment preferences than what appears in Indonesian-language domestic outlets. Co-ownership by Kompas and Tempo lends editorial credibility.

### Tier 2 Sources

> Articles from **CNN Indonesia** about domestic politics and security should be interpreted as mainstream, structured political coverage with awareness of Trans Media / CT Corp ownership — Chairul Tanjung (former Coordinating Minister for Economics) controls both CNN Indonesia and Detik, creating structural caution on stories involving business-government relations. CNN Indonesia's ministerial interviews are useful as indicators of what officials want to communicate publicly.

> Articles from **CNBC Indonesia** about economic policy should be interpreted as reflecting the perspective of Indonesia's business and investment community — its market-oriented framing means negative coverage of government economic intervention (nickel export bans, downstream mandates) reflects investor sentiment, not necessarily policy failure. Essential for detecting economic statecraft signals but should be calibrated against Kompas and government sources for policy intent.

> Articles from **Tirto.id** about government policy and institutional affairs should be interpreted as data-driven independent analysis — its IFCN-certified fact-checking methodology distinguishes it from opinion-driven outlets. When Tirto contradicts official narratives with data, the divergence is itself a signal. Its targeting by cyberattacks indicates that its reporting generates official discomfort, lending credibility to its most uncomfortable findings.

> Articles from **Republika** about foreign policy involving Muslim-majority states should be interpreted as reflecting the preferences and red lines of Indonesia's mainstream Islamic constituency — what Republika covers (Palestine, OIC, Saudi/Turkey/Iran relations) and how it frames it reveals the domestic political constraints on Indonesia's diplomatic positioning that secular outlets underreport. Republika's editorial positions are not fringe — they reflect Muhammadiyah/NU-adjacent mainstream Muslim opinion.

> Articles from **Kemlu.go.id**, **Setkab.go.id**, and **Kemhan.go.id** should be interpreted as official government communications — not journalism but primary source material. Press releases, regulations, and diplomatic statements from these domains represent the government's chosen public position, which may differ from actual policy implementation. Systematic monitoring of language changes in these sources detects posture shifts before they appear in media coverage.

> Articles from **CSIS Jakarta** about foreign policy and regional security should be interpreted as elite policy analysis that often previews government thinking — CSIS researchers advise government, and their publications frequently anticipate policy shifts by months. The think tank's independence is real but its proximity to power means its analyses reflect what is thinkable within the establishment, not dissenting views. Its annual "Indonesia and the World" survey is the best structured dataset on Indonesian elite foreign policy preferences.

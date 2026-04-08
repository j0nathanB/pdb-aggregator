# AUDIT SUMMARY: INDIA

**Sources assessed:** 19 recommended + 5 excluded + 4 newly identified = 28 total
**Tier 1 (boost=3):** 5 sources
**Tier 2 (boost=2):** 8 sources
**Tier 3 (boost=1):** 6 sources
**Neutral (no rule):** 5 sources
**Discard:** 4 sources
**Overall assessment:** India presents the most severe blocked-domain problem of any country audited so far — 7 of 19 recommended sources are blocked by Anthropic's crawler (thehindu.com, indianexpress.com, hindustantimes.com, economictimes.indiatimes.com, livemint.com, jagran.com, bhaskar.com). This means the pipeline's extraction layer will fail on most of India's premier English-language press and both Hindi-language dailies. Brave can still surface these for discovery/headlines, but full-text extraction requires alternative methods. Key changes: (1) promoted Hindi-language sources to maximum feasible tier with non-English boost premium despite blocked status; (2) elevated ThePrint to Tier 1 as the only extractable high-quality digital-native outlet; (3) migrated government sources (mea.gov.in, pib.gov.in, pmindia.gov.in, sansadtv.nic.in) to Layer 2 with Tier 2 Goggle fallback; (4) resolved think tank redundancy across five outlets by differentiating analytical niches; (5) flagged in.yaml config discrepancy — ndtv.com is listed as domestic Tier 2 triage source despite being explicitly excluded in the intelligence map. Config also omits most recommended sources.

**Config alignment issues (in.yaml):**
- `ndtv.com` is listed as domestic Tier 2 triage source but was excluded in the intelligence map due to Adani acquisition and editorial capture. **Recommend removal from config or demotion to non-triage.**
- `thehindu.com` and `indianexpress.com` are listed as domestic sources but both are blocked by Anthropic's crawler. Triage source designation for thehindu.com will fail at extraction.
- `pmindia.gov.in` is in config but not in the intelligence map; `pib.gov.in` is in the map but not config. Both should be present.
- The config's `sources.domestic` list omits ThePrint, The Wire, Hindustan Times, Economic Times, LiveMint, and all Hindi-language dailies.

---

## BOOST ASSIGNMENTS

### Tier 1 — `$boost=3`

**ThePrint** | `theprint.in` | Type: `digital_native` | Status: `EXISTING`
- **Structural role:** India's best digital-native outlet for defense and national security reporting. Free, fully extractable, publishes in both English and Hindi. In a landscape where every legacy broadsheet is behind either a paywall or a crawler block, ThePrint becomes the pipeline's most reliable high-frequency source.
- **Domain coverage:** Security & defense autonomy, Diplomatic alignment, Domestic constraints
- **Reasoning:** ThePrint's defense vertical (`theprint.in/defence/`) is the strongest among digital outlets. Shekhar Gupta's "Cut the Clutter" provides rapid strategic context. Crucially, it is **not blocked** and **not paywalled** — making it the only high-quality daily source the pipeline can reliably extract full text from. This extraction reality alone justifies Tier 1. Hindi edition enables cross-language framing comparison.
- **Non-English premium:** Hindi edition available — boost justified.
- **Extraction note:** Free access. No crawler block. Full extraction viable.

**The Hindu** | `thehindu.com` | Type: `paper_of_record` | Status: `EXISTING`
- **Structural role:** India's most analytically rigorous English daily for foreign affairs. The outlet that retired diplomats, strategic affairs commentators, and the MEA press corps read and write for. Sets the analytical agenda on India-China, multilateral negotiations, and defense procurement.
- **Domain coverage:** Diplomatic alignment, Security & defense autonomy, Institutional engagement
- **Reasoning:** Structural role outweighs extraction difficulty. The Hindu is to India's foreign policy discourse what Reforma is to Mexico's political class — the indispensable broadsheet. **Blocked by Anthropic's crawler**, which severely limits extraction, but Brave will still surface headlines and the boost ensures those headlines rank high. The pipeline gets the signal even without full text.
- **Extraction note:** Metered paywall + blocked by Anthropic crawler. Brave discovery only. Consider RSS feed polling as Layer 2 supplement.

**The Indian Express** | `indianexpress.com` | Type: `paper_of_record` | Status: `EXISTING`
- **Structural role:** India's strongest investigative broadsheet. Uniquely positioned to surface domestic political dynamics constraining foreign policy — defense procurement scandals, intelligence leaks, coalition politics. "Explained" section provides accessible strategic context.
- **Domain coverage:** Security & defense autonomy, Domestic constraints on external action
- **Reasoning:** The Indian Express fills the adversarial/investigative niche that no other legacy outlet covers as well. Its editorial independence from government (center-right liberal) makes it the primary source for stories the government would prefer not to see. **Blocked by Anthropic's crawler** — same extraction limitation as The Hindu, same reasoning for retaining Tier 1.
- **Extraction note:** Metered paywall + blocked by Anthropic crawler. Brave discovery only.

**Observer Research Foundation (ORF)** | `orfonline.org` | Type: `think_tank` | Status: `EXISTING`
- **Structural role:** India's most prolific think tank on strategic affairs, and the closest proxy for BJP establishment strategic thinking. Government-adjacent positioning makes it a reliable signal of official intent — what ORF publishes often prefigures policy.
- **Domain coverage:** All five domains
- **Reasoning:** Think tanks earn boost through depth, not speed — but ORF is the exception: its daily expert commentary (`orfonline.org/expert-speak/`) publishes at near-journalistic frequency. Proximity to government + Reliance funding means editorial line tracks ruling party strategic consensus, which is precisely the signal the pipeline needs. **Not blocked, fully open, RSS available.** Hindi output enables domestic-framing detection. Tier 1 because it is both analytically deep and practically extractable — a rare combination in this landscape.
- **Non-English premium:** Hindi edition available — boost justified.
- **Extraction note:** Fully open. No crawler block. Full extraction viable.

**Dainik Jagran** | `jagran.com` | Type: `hindi_daily` | Status: `EXISTING`
- **Structural role:** India's highest-circulation newspaper (any language). The primary window into how foreign policy events are framed for the Hindi-speaking mass electorate — the voters who determine outcomes in UP, MP, Bihar, Rajasthan, and other key states.
- **Domain coverage:** Domestic constraints on external action
- **Reasoning:** Non-English domestic sources receive boost premium per audit principles. Dainik Jagran's editorial positions on Pakistan, China, and U.S. relations are the single best indicator of mass-electorate sentiment constraining government diplomatic flexibility. Single-domain (domestic constraints) but irreplaceable within it. **Blocked by Anthropic's crawler** — extraction will fail, but the Brave discovery signal (Hindi headlines on border incidents, military casualties, trade impacts on agriculture) is itself analytically valuable.
- **Non-English premium:** Hindi-language — maximum boost premium applied.
- **Extraction note:** Blocked by Anthropic crawler. Brave headline discovery only. Automated Hindi-language processing required.

---

### Tier 2 — `$boost=2`

**Hindustan Times** | `hindustantimes.com` | Type: `paper_of_record` | Status: `EXISTING`
- **Structural role:** Establishment-centrist broadsheet with strong MoD and South Block sourcing. Reads as the government-friendly counterpart to Indian Express's adversarial posture.
- **Domain coverage:** Diplomatic alignment, Security & defense autonomy
- **Reasoning:** Strong defense and diplomacy beat reporters, but editorially less distinctive than The Hindu or Indian Express — it generally reinforces establishment consensus rather than challenging it. Birla family ownership is stable and professional but not independent in the same way. **Blocked by Anthropic's crawler.** Tier 2 rather than Tier 1 because its editorial role (establishment confirmation) is less structurally essential than The Hindu's (agenda-setting) or Indian Express's (adversarial investigation).
- **Extraction note:** Free access but blocked by Anthropic crawler. Brave discovery only.

**Dainik Bhaskar** | `bhaskar.com` | Type: `hindi_daily` | Status: `EXISTING`
- **Structural role:** Second-largest Hindi daily. Complements Dainik Jagran with broader central/western India geographic reach (MP, Rajasthan, Gujarat, Chhattisgarh). Better economic reporting than Jagran.
- **Domain coverage:** Domestic constraints on external action, Economic & technological statecraft
- **Reasoning:** Non-English boost premium applies. The 2021 tax raid (after critical COVID coverage) signals a degree of editorial independence unusual among Hindi outlets — this is analytically useful because Bhaskar occasionally diverges from the Jagran/government consensus. **Blocked by Anthropic's crawler.** Tier 2 rather than Tier 1 because Jagran already occupies the Hindi-daily structural slot and Bhaskar's geographic overlap is partial.
- **Non-English premium:** Hindi-language — boost premium applied.
- **Extraction note:** Blocked by Anthropic crawler. English edition at bhaskar.com/english may be partially accessible.

**The Wire** | `thewire.in` | Type: `digital_native_independent` | Status: `EXISTING`
- **Structural role:** India's primary left-liberal adversarial voice. Strongest outlet for tracking civil liberties, minority rights, and democratic governance issues that generate international friction. Hindi edition reaches beyond the English-language elite.
- **Domain coverage:** Domestic constraints on external action, Institutional engagement
- **Reasoning:** Critical counterpoint to ORF's government-adjacent position. The Wire surfaces the stories that generate foreign government statements on Indian domestic politics — precisely the friction points the dossier needs to track. **Not blocked, free access.** The 2022 Meta/Tek Fog retraction damaged credibility, which prevents Tier 1. But the structural role (adversarial left voice) is essential for the pipeline's ideological plurality.
- **Non-English premium:** Hindi edition available — boost justified.
- **Extraction note:** Free, reader-supported. Not blocked. Full extraction viable. Verify claims independently per credibility note.

**MP-IDSA** | `idsa.in` | Type: `think_tank` (government-funded) | Status: `EXISTING`
- **Structural role:** India's oldest and most authoritative defense think tank. Ministry of Defence-funded, staffed by retired military/diplomatic officers. Content often prefigures MoD policy.
- **Domain coverage:** Security & defense autonomy, Diplomatic alignment
- **Reasoning:** Think tanks earn boost through depth, not speed. MP-IDSA's issue briefs and Strategic Analysis journal provide early indicators of doctrinal shifts and defense procurement priorities that daily outlets won't detect until they become policy. Tier 2 rather than Tier 1 because publication frequency is lower and domain coverage is narrower than ORF's. **Not blocked, fully open.**
- **Extraction note:** Fully open. No crawler block. Full extraction viable.

**Ministry of External Affairs** | `mea.gov.in` | Type: `government_primary` | Status: `EXISTING` — **LAYER 2 MIGRATION**
- **Structural role:** Definitive record of India's stated diplomatic positions. Joint statements, bilateral communiques, spokesperson briefings. The gap between MEA language and actual policy is itself an analytical signal.
- **Domain coverage:** Diplomatic alignment, Institutional engagement
- **Reasoning:** Government sources = Layer 2 migration at Tier 2 per audit principles. Primary fetch via direct polling (press releases at mea.gov.in/press-releases.htm, spokesperson transcripts published same-day). Goggle boost as belt-and-suspenders fallback. **Not blocked.**
- **Extraction note:** Fully open. No RSS — requires scrape or poll for Layer 2.

**Press Information Bureau** | `pib.gov.in` | Type: `government_primary` | Status: `EXISTING` — **LAYER 2 MIGRATION**
- **Structural role:** Central clearinghouse for all Indian government press releases including Cabinet decisions on defense, trade, sanctions compliance, and multilateral commitments. Captures inter-ministerial signals that MEA alone does not.
- **Domain coverage:** All five domains (cross-cutting government communication)
- **Reasoning:** Layer 2 migration. PIB's multi-language releases (English, Hindi, 12 regional languages) allow cross-checking of Hindi-vs-English framing differences — a unique analytical capability. RSS feeds available for Layer 2 polling. **Not blocked.**
- **Extraction note:** Fully open. RSS available. Multi-language output.

**Prime Minister's Office** | `pmindia.gov.in` | Type: `government_primary` | Status: `FROM CONFIG` — **LAYER 2 MIGRATION**
- **Structural role:** Official PMO communications. Leaders-level statements, joint communiques from bilateral summits, Mann ki Baat transcripts. The highest-level signal of India's stated strategic direction.
- **Domain coverage:** Diplomatic alignment, Economic & technological statecraft
- **Reasoning:** Listed in in.yaml as government Tier 1 but absent from the intelligence map. Added here for completeness — PMO statements are the most authoritative signal of strategic intent. Layer 2 primary fetch with Tier 2 Goggle fallback. **Not blocked.**
- **Extraction note:** Fully open.

**Sansad TV / Parliamentary Records** | `sansadtv.nic.in` | Type: `legislative_official` | Status: `EXISTING` — **LAYER 2 MIGRATION**
- **Structural role:** Direct access to parliamentary debates on defense budgets, treaty ratifications, and foreign policy. Rajya Sabha debates searchable at rsdebate.nic.in.
- **Domain coverage:** Domestic constraints on external action, Institutional engagement
- **Reasoning:** Parliamentary proceedings are primary source material for detecting opposition positions and intra-coalition tensions on foreign policy. "India's World" program covers foreign affairs specifically. Layer 2 migration for direct polling; Tier 2 Goggle boost as fallback. Includes subdomain rsdebate.nic.in. **Not blocked.**
- **Extraction note:** Free streaming and archives. Transcripts in Hindi and English.

---

### Tier 3 — `$boost=1`

**Carnegie India** | `carnegieindia.org` | Type: `think_tank` (international) | Status: `EXISTING`
- **Structural role:** Highest-quality long-form analysis on India's technology statecraft, nuclear policy, and U.S.-India strategic partnership. International network provides comparative framing domestic think tanks lack.
- **Domain coverage:** Economic & technological statecraft, Diplomatic alignment, Institutional engagement
- **Reasoning:** Think tanks earn boost through depth, not speed. Carnegie India publishes less frequently than ORF or MP-IDSA but at higher analytical depth per piece. Tier 3 rather than Tier 2 because its international framing duplicates what wire services and international outlets provide, and its publication cadence is too low for daily pipeline use. **Not blocked, fully open.**
- **Extraction note:** Fully open. No crawler block.

**Gateway House** | `gatewayhouse.in` | Type: `think_tank` | Status: `EXISTING`
- **Structural role:** Mumbai-based geo-economics think tank. Unique niche connecting business community perspectives with foreign policy. Strongest Indian think tank on trade corridors, supply chain diversification, energy security, and IMEC.
- **Domain coverage:** Economic & technological statecraft, Diplomatic alignment
- **Reasoning:** Narrow but unique niche — no other source provides the Mumbai business-community lens on foreign policy. Tier 3 because domain coverage is limited and publication frequency is lower than ORF. But when Gateway House publishes on IMEC, nearshoring, or energy corridors, the analysis is distinctive. **Not blocked, fully open.**
- **Extraction note:** Fully open. No crawler block.

**Takshashila Institution** | `takshashila.org.in` | Type: `think_tank` | Status: `EXISTING`
- **Structural role:** Bangalore-based policy school producing concise, operationally useful briefs on defense technology, cybersecurity, and Indo-Pacific strategy. Represents non-Delhi strategic thinking.
- **Domain coverage:** Security & defense autonomy, Economic & technological statecraft
- **Reasoning:** Tier 3 for supplementary depth. Younger-generation analysts and Bangalore base provide a different analytical perspective than Delhi-centric think tanks. Discussion Document series and "All Things Policy" podcast are rapid-turnaround. But narrow scope and limited institutional weight compared to ORF/MP-IDSA cap it at Tier 3. **Not blocked, fully open.**
- **Extraction note:** Fully open. Newsletter available.

**FORCE Magazine** | `forceindia.net` | Type: `security_defense` | Status: `EXISTING`
- **Structural role:** India's most substantive specialist defense publication. Covers procurement decisions, indigenous manufacturing (Tejas, INS Vikrant-class), joint exercises, arms import diversification, and military doctrine.
- **Domain coverage:** Security & defense autonomy
- **Reasoning:** Single-domain but fills a genuine structural gap — no other source provides this level of granularity on defense procurement and indigenous manufacturing progress. Tier 3 because publication frequency is low (monthly magazine with some web articles) and single-domain scope limits pipeline utility. But the boost ensures its periodic deep analyses surface when they appear. **Not blocked.**
- **Extraction note:** Partially paywalled. Some articles open-access.

**Economic and Political Weekly** | `epw.in` | Type: `academic_journal` | Status: `EXISTING`
- **Structural role:** India's premier left-progressive academic weekly. Indispensable for tracking domestic political economy constraining external action — agrarian distress, labor politics, federalism tensions.
- **Domain coverage:** Domestic constraints on external action, Institutional engagement
- **Reasoning:** Think tank/academic sources earn boost through depth. EPW's 75-year publication history and editorial independence make it the authoritative academic voice on India's domestic constraints. Tier 3 because publication cadence is weekly, content is paywalled (institutional access via JSTOR), and it doesn't break news. But editorials are often open-access and serve as early indicators of left-intellectual opposition. **Not blocked.**
- **Extraction note:** Paywalled; institutional access via JSTOR. Editorials often open-access.

**South Asian Voices** | `southasianvoices.org` | Type: `think_tank` / `regional_analytical` | Status: `NEW`
- **Structural role:** Stimson Center initiative publishing emerging scholars from across South Asia on regional security, nuclear dynamics, and India-Pakistan/India-China relations. Fills the regional comparative lens gap.
- **Domain coverage:** Security & defense autonomy, Diplomatic alignment
- **Reasoning:** Added to fill the missing structural role of regional comparative analysis. Indian domestic sources lack perspective on how India's actions are perceived by neighbors. South Asian Voices publishes Pakistani, Bangladeshi, Sri Lankan, and Nepali analysts alongside Indian ones — unique for the pipeline. Tier 3 because publication frequency is low and it's not India-specific. **Not blocked, fully open.**
- **Extraction note:** Fully open.

---

### Neutral — no Goggle rule

**NDTV** | `ndtv.com` | Type: excluded → `neutral` | Status: `INTELLIGENCE MAP EXCLUSION → CONFIRMED NEUTRAL`
- **Why neutral:** Explicitly excluded in the intelligence map due to Adani Group acquisition (December 2022, 64.7% stake) and departure of senior journalists. The curation prompt's exclusion was correct under the hard-filter model. Under the Goggle model, no reason to actively discard — NDTV still has the largest English-language television audience in India, and if it breaks a major story, Brave may surface it. But boosting would amplify government-aligned framing. **Note: in.yaml lists ndtv.com as domestic Tier 2 triage source — this should be corrected in config.**

**The Economic Times** | `economictimes.indiatimes.com` | Type: `business_daily` | Status: `EXISTING → DEMOTED TO NEUTRAL`
- **Why neutral:** Redundant with LiveMint for economic statecraft coverage (LiveMint has sharper policy analysis). **Blocked by Anthropic's crawler**, making extraction unreliable even if Brave surfaces it. Part of Times Group conglomerate, which introduces ownership-concentration risk. Under Goggle model, may surface organically for specific economic queries — no need to boost, no need to discard.

**LiveMint** | `livemint.com` | Type: `business_daily` | Status: `EXISTING → DEMOTED TO NEUTRAL`
- **Why neutral:** Superior to Economic Times for policy analysis on trade negotiations and technology regulation. However, **hard paywall** and **blocked by Anthropic's crawler** create a double extraction barrier. The pipeline cannot reliably get full text. Under Goggle model, Brave may surface headlines for high-signal stories on UPI/Aadhaar digital infrastructure exports. Leave at organic ranking — if extraction improves (e.g., via Factiva Layer 2), re-evaluate for Tier 2.

**Scroll.in** | `scroll.in` | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Curation exclusion noted lack of foreign policy depth and redundancy with The Wire. Under Goggle model, no reason to actively discard — Scroll.in's domestic governance coverage occasionally surfaces foreign policy friction points (e.g., visa restrictions, foreign funding regulation). Organic ranking is appropriate.

**Firstpost / News18** | `firstpost.com` / `news18.com` | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Reliance-owned, compromised editorial independence per intelligence map. Under Goggle model, no reason to actively discard — high traffic means Brave may rank them for breaking news queries. The pipeline's interpretive context can handle ownership bias. Organic ranking is fine.

---

### Discard — `$discard`

**Republic TV** | `republicworld.com` | Status: `CONFIRMED DISCARD`
- **Discard reasoning:** Polemical, entertainment-driven coverage of international affairs per intelligence map. Would actively displace higher-signal sources from top results. Arnab Goswami's programming is performative rather than analytical — pure noise for pipeline purposes.

**Times Now** | `timesnownews.com` | Status: `CONFIRMED DISCARD`
- **Discard reasoning:** Same as Republic TV — television-first outlet producing sensationalist coverage of strategic affairs. Web content is largely video clips and wire rewrites. Would waste result slots that should go to analytical sources.

**OpIndia** | `opindia.com` | Status: `CONFIRMED DISCARD`
- **Discard reasoning:** Right-wing digital outlet producing derivative commentary rather than original reporting per intelligence map. Ideological signal is better captured via Dainik Jagran editorials (Tier 1) and ORF publications (Tier 1). OpIndia would inject partisan noise without adding original intelligence.

**Swarajya** | `swarajya.in` | Status: `CONFIRMED DISCARD`
- **Discard reasoning:** Same as OpIndia — Hindutva nationalist perspective that is derivative rather than original. The structural niche (right-nationalist viewpoint) is already filled by ORF and Dainik Jagran at higher analytical quality. Discarding prevents displacement of higher-signal sources.

---

## STRUCTURAL COVERAGE CHECK

| Structural Role | Source(s) | Tier | Notes |
|---|---|---|---|
| Government leak channel / signaling | ORF, Hindustan Times | T1, T2 | ORF publishes what the BJP strategic establishment wants amplified. HT's South Block sourcing provides official-adjacent reporting. No single outlet serves as a dedicated government signaling channel the way La Jornada does for Mexico — the signal is distributed |
| Opposition voice | The Indian Express, The Wire | T1, T2 | Indian Express for investigative adversarial reporting; The Wire for left-liberal critique. Both are extractable, which is critical given blocked-domain problems elsewhere |
| Defence/security first-mover | ThePrint, FORCE Magazine | T1, T3 | ThePrint's defense vertical is the fastest digital outlet for security breaks. FORCE Magazine for specialist depth on procurement and doctrine. MP-IDSA (T2) for analytical early indicators |
| Policy-elite discourse | The Hindu, ORF, Carnegie India | T1, T1, T3 | The Hindu is what diplomats and strategic commentators read. ORF is where they publish. Carnegie India provides the international-comparative frame |
| Domestic-language depth | Dainik Jagran, Dainik Bhaskar, ThePrint (Hindi), The Wire (Hindi), ORF (Hindi), PIB (multilingual) | T1, T2, T1, T2, T1, T2 | Six sources with Hindi output. Both Hindi dailies are blocked — the pipeline's Hindi-language capability is severely constrained by crawler blocks. ThePrint, The Wire, and ORF Hindi editions are the extractable alternatives |
| Official government source | mea.gov.in, pib.gov.in, pmindia.gov.in, sansadtv.nic.in | T2 (all) | **LAYER 2 MIGRATION** — primary fetch via direct polling. Goggle boost as fallback. All are unblocked and fully open |
| Analytical/think tank depth | ORF, MP-IDSA, Carnegie India, Gateway House, Takshashila, EPW | T1, T2, T3, T3, T3, T3 | Five think tanks + one academic journal. Differentiated by niche: ORF (strategic consensus), MP-IDSA (defense doctrine), Carnegie (tech statecraft), Gateway House (geo-economics), Takshashila (defense tech/cyber), EPW (political economy) |
| Business/economic statecraft | Economic Times, LiveMint | Neutral, Neutral | **Major gap:** Both business dailies are blocked by Anthropic's crawler and one is hard-paywalled. No extractable dedicated business source. Gateway House (T3) and ORF (T1) partially cover economic statecraft but cannot substitute for daily business press. Consider Factiva/Layer 2 polling for LiveMint content |
| Wire service (international) | Reuters, AP News, France24 | Neutral | Per in.yaml config. Reuters is blocked by Anthropic crawler but Brave can surface for discovery. Not boosted — wire copy available organically |
| Regional comparative | South Asian Voices | T3 | Newly added. Fills gap on how India's actions are perceived by South Asian neighbors |

**Gaps identified:**
1. **Business/economic statecraft extraction** is the most critical gap. Both Economic Times and LiveMint are blocked by Anthropic's crawler, leaving no extractable dedicated business source. Gateway House and ORF partially compensate, but daily economic intelligence (FDI flows, trade policy shifts, rupee internationalization, semiconductor policy) will be thin. **Mitigation:** Investigate Factiva/Layer 2 pipeline for LiveMint; consider adding Business Standard (`business-standard.com`) if unblocked.
2. **Regional-language press** (Tamil, Telugu, Kannada, Bengali, Assamese) is absent per the intelligence map's own coverage gap assessment. Southern and northeastern India perspectives on defense installations, port access agreements, and connectivity projects are invisible. This is a known limitation — automated processing of 6+ Indian languages is beyond current pipeline scope.
3. **Hindi-language extraction** is crippled by crawler blocks on both Dainik Jagran and Dainik Bhaskar. The pipeline's ability to detect mass-electorate sentiment on foreign policy is limited to ThePrint Hindi, The Wire Hindi, ORF Hindi, and PIB Hindi — all of which are elite-facing outlets that don't represent grassroots Hindi-belt opinion. **Mitigation:** Investigate RSS feed polling for jagran.com and bhaskar.com as Layer 2 workaround.
4. **India-Pakistan military dynamics** (including Operation Sindoor / post-Pahalgam escalation noted in in.yaml blind spots) lack a dedicated source. FORCE Magazine covers defense broadly, but the real-time crisis reporting gap is filled by ThePrint and wire services. Cross-border verification requires Pakistan ISPR releases and international assessments (SIPRI/IISS) — neither is in the Goggle.

---

## REDUNDANCY RESOLUTION

**Broadsheet cluster: The Hindu + Indian Express + Hindustan Times**
All three are English-language legacy broadsheets covering national affairs. Resolved by differentiating editorial roles: The Hindu (Tier 1, foreign affairs agenda-setter, analytically rigorous), Indian Express (Tier 1, investigative/adversarial, domestic constraints specialist), Hindustan Times (Tier 2, establishment-centrist, MoD/South Block sourcing). HT drops below the other two because it breaks fewer exclusive stories and its editorial role (confirming establishment consensus) is less structurally essential than agenda-setting or adversarial investigation. All three are blocked by Anthropic's crawler — tier differentiation is based on structural role, not extraction viability.

**Business press cluster: Economic Times + LiveMint**
Both cover economic statecraft. Both are blocked by Anthropic's crawler. LiveMint has sharper policy analysis (WSJ partnership) but harder paywall. Economic Times has broader coverage but is part of the Times Group conglomerate. Neither can be reliably extracted. Both demoted to Neutral — redundancy is moot when neither is extractable. If extraction improves for either, LiveMint should return at Tier 2 and Economic Times at Tier 3.

**Think tank cluster: ORF + MP-IDSA + Carnegie India + Gateway House + Takshashila**
Five think tanks is appropriate for India's unusually rich policy research ecosystem, and each has a distinct niche. ORF (Tier 1, government-adjacent strategic consensus, highest publication frequency), MP-IDSA (Tier 2, MoD institutional perspective, defense doctrine), Carnegie India (Tier 3, international-comparative technology statecraft), Gateway House (Tier 3, Mumbai geo-economics), Takshashila (Tier 3, Bangalore defense tech/cyber). No genuine redundancy — each covers different domains from different institutional vantage points. ORF earns Tier 1 because it is both the most prolific and the most politically proximate. MP-IDSA earns Tier 2 for its MoD proximity and doctrinal authority. The remaining three are differentiated at Tier 3 by niche.

**Hindi-language cluster: Dainik Jagran + Dainik Bhaskar**
Both are Hindi dailies covering domestic constraints. Resolved by geographic and editorial differentiation: Jagran (Tier 1, highest circulation, Hindi heartland — UP/Bihar/MP), Bhaskar (Tier 2, central/western India — MP/Rajasthan/Gujarat, better economic reporting, demonstrated editorial independence via 2021 tax raid). Jagran gets the Tier 1 slot because it reaches more voters in more electorally decisive states. Both are blocked — tier differentiation is for Brave discovery ranking.

**Digital-native cluster: ThePrint + The Wire**
Both are digital-native, both have Hindi editions, both are unblocked. Resolved by editorial niche: ThePrint (Tier 1, defense/national security specialist, center-right), The Wire (Tier 2, left-liberal adversarial, civil liberties/governance). No redundancy — they occupy opposite ends of the editorial spectrum and cover different domains. Both are essential for ideological plurality.

---

## QUERY CONFIGURATION

```
country: IN
search_lang: hi
freshness: pw
```

**Multi-language notes:** India's media ecosystem is bifurcated between English (elite/policy/strategic discourse) and Hindi (mass-electorate political sentiment). Queries should run in both Hindi and English. Hindi queries are essential for detecting domestic constraints that shape foreign policy — the intelligence map explicitly flags this. A secondary English query cycle captures the analytical/strategic discourse from English-language dailies and think tanks. The pipeline's existing `languages.primary: hi` and `languages.metadata: en` configuration handles this correctly, but the severity of Hindi-source crawler blocks means English queries will disproportionately drive results in practice.

**Localized query vocabulary validation:**

The curation prompt's vocabulary is comprehensive and accurate. Notes:

- **Domain 1 (Diplomatic):** All terms valid. Add `"Jaishankar"` as a high-signal leader-specific term — the External Affairs Minister's name co-occurs with virtually all diplomatic developments. `"सामरिक स्वायत्तता"` (strategic autonomy) is the correct doctrinal term. Add `"वसुधैव कुटुम्बकम"` (Vasudhaiva Kutumbakam / "One Earth, One Family") — Modi's G20 theme that continues to frame India's multilateral rhetoric. `"Quad"` and `"क्वाड"` are both needed — used interchangeably in Hindi press.
- **Domain 2 (Security):** Strong list. Add `"Operation Sindoor"` / `"ऑपरेशन सिंदूर"` — the post-Pahalgam military operation noted in in.yaml blind spots. `"Agnipath"` / `"अग्निपथ"` (military recruitment reform) is generating domestic political friction that constrains defense posture. `"LAC"` is used as-is in Hindi media alongside the full form. Add `"S-400"` for tracking the Russia defense procurement that generates U.S. CAATSA sanctions friction.
- **Domain 3 (Economic):** Excellent. `"आत्मनिर्भर भारत"` (Atmanirbhar Bharat) is the essential frame. Add `"PLI"` (Production-Linked Incentive) — the core policy instrument for manufacturing statecraft. `"IMEC"` / `"India-Middle East-Europe Corridor"` is increasingly relevant. `"UPI"` is used as-is in Hindi — add for digital public infrastructure tracking. Add `"चीन प्लस वन"` (China Plus One) for supply chain diversification coverage.
- **Domain 4 (Institutional):** Valid. Add `"UNSC सुधार"` pairing for UN Security Council reform tracking. `"Global South"` / `"वैश्विक दक्षिण"` (Vaishvik Dakshin) — India's positioning as Global South leader is a defining institutional narrative. Add `"SCO"` / `"शंघाई सहयोग संगठन"` (Shanghai Cooperation Organisation).
- **Domain 5 (Domestic):** Strong. Add `"INDIA alliance"` / `"इंडिया गठबंधन"` (opposition coalition). `"NDA"` for ruling coalition dynamics. `"CAA"` / `"नागरिकता संशोधन"` (Citizenship Amendment Act) — generates international friction. Add `"अग्निपथ"` (Agnipath) here as well — military recruitment reform is both a defense and a domestic constraint issue.

**Stale/problematic terms:** None are stale. `"गुटनिरपेक्षता"` (non-alignment) is historically relevant but declining in active policy usage — `"बहु-संरेखण"` (multi-alignment) is the contemporary replacement. Both should remain as search terms since non-alignment is still invoked rhetorically.

**Suggested topic query patterns:**

1. `Modi Jaishankar विदेश नीति सामरिक स्वायत्तता` — Strategic autonomy / foreign policy direction
2. `LAC सीमा गतिरोध चीन भारत` — India-China border dynamics
3. `आत्मनिर्भर भारत रक्षा खरीद स्वदेशी` — Indigenous defense manufacturing / Atmanirbhar Bharat
4. `BRICS SCO Quad भारत बहुपक्षवाद` — Multilateral institutional positioning
5. `Operation Sindoor पाकिस्तान रक्षा` — India-Pakistan military dynamics
6. `UPI digital public infrastructure IMEC` — Technology/economic statecraft
7. `किसान आंदोलन मुक्त व्यापार समझौता` — Domestic constraints on trade liberalization
8. `UNSC सुधार Global South भारत` — UN reform and Global South leadership

---

## GOGGLE FILE

```goggle
! name: MPM India
! description: MPM pipeline source prioritization for India — boosts high-signal sources, discards noise. Note: 7 boosted sources are blocked by Anthropic crawler (thehindu.com, indianexpress.com, hindustantimes.com, economictimes.indiatimes.com, livemint.com, jagran.com, bhaskar.com) — boost affects Brave ranking only, extraction requires alternative methods.
! public: false
! author: MPM Pipeline

! --- Tier 1: Essential (boost=3) ---
$boost=3,site=theprint.in
$boost=3,site=thehindu.com
$boost=3,site=indianexpress.com
$boost=3,site=orfonline.org
$boost=3,site=jagran.com

! --- Tier 2: Important (boost=2) ---
$boost=2,site=hindustantimes.com
$boost=2,site=bhaskar.com
$boost=2,site=thewire.in
$boost=2,site=idsa.in
$boost=2,site=mea.gov.in
$boost=2,site=pib.gov.in
$boost=2,site=pmindia.gov.in
$boost=2,site=sansadtv.nic.in

! --- Tier 3: Supplementary (boost=1) ---
$boost=1,site=carnegieindia.org
$boost=1,site=gatewayhouse.in
$boost=1,site=takshashila.org.in
$boost=1,site=forceindia.net
$boost=1,site=epw.in
$boost=1,site=southasianvoices.org

! --- Discard: Noise ---
$discard,site=republicworld.com
$discard,site=timesnownews.com
$discard,site=opindia.com
$discard,site=swarajya.in
```

---

## INTERPRETIVE CONTEXT FOR DOSSIER

### Tier 1 Sources

> Articles from **ThePrint** about defense and national security should be interpreted as India's most accessible and frequently updated digital reporting on military affairs — Shekhar Gupta's center-right, pro-reform editorial orientation means defense reporting tends to frame indigenous capability positively and view strategic partnerships (especially with the U.S.) favorably, but the defense correspondents' armed forces sourcing is strong and the reporting is factually reliable.

> Articles from **The Hindu** about diplomatic developments and multilateral negotiations should be interpreted as India's most analytically rigorous foreign affairs reporting — its historically sympathetic orientation toward non-alignment and strategic autonomy means it frames India's Western-alignment moves more cautiously than ThePrint, but its international affairs desk provides the deepest sourcing on India-China dynamics, multilateral treaty negotiations, and defense procurement. **Extraction caveat: blocked by Anthropic crawler — pipeline receives headlines/discovery only, not full text.**

> Articles from **The Indian Express** about government policy and domestic political dynamics should be interpreted as filtered through a strong investigative, editorially independent lens — its center-right liberal orientation and tradition of adversarial reporting mean it surfaces stories the government would prefer not to see (defense procurement scandals, intelligence community leaks, coalition friction). This makes it essential for detecting domestic constraints on foreign policy but means negative framing of government initiatives is the editorial default. **Extraction caveat: blocked by Anthropic crawler.**

> Articles from **ORF** about any strategic domain should be interpreted as reflecting the BJP establishment's strategic consensus — its proximity to government (partly Reliance-funded, government-adjacent analysts) means its publications often preview or rationalize official positions. This is a feature, not a bug: ORF tells the pipeline what the ruling strategic establishment is thinking. When ORF publishes on a topic, it signals that the government considers it strategically relevant. When ORF's framing diverges from MEA statements, the gap is itself analytically significant.

> Articles from **Dainik Jagran** about border incidents, Pakistan, China, or military affairs should be interpreted as reflecting Hindi-belt mass-electorate sentiment — its center-right nationalist editorial orientation and UP/Bihar/MP readership base mean it frames international events through a lens of national pride and security anxiety. What Jagran's editorials demand constrains the government's diplomatic flexibility in ways that English-language sources cannot detect. **Extraction caveat: blocked by Anthropic crawler; Hindi-language processing required.**

### Tier 2 Sources

> Articles from **Hindustan Times** about defense and diplomacy should be interpreted as establishment-centrist coverage reflecting South Block consensus — its Birla family ownership and strong MoD sourcing mean it generally confirms rather than challenges the government's strategic direction. Useful for reading what the defense establishment wants communicated, but unlikely to break adversarial stories.

> Articles from **Dainik Bhaskar** about economic and trade policy should be interpreted with awareness of its demonstrated editorial independence — the 2021 tax raid after critical COVID coverage signals willingness to diverge from government messaging. Its central/western India readership base (MP, Rajasthan, Gujarat) provides a geographic complement to Jagran's Hindi heartland. **Extraction caveat: blocked by Anthropic crawler; Hindi-language processing required.**

> Articles from **The Wire** about civil liberties, minority rights, and governance should be interpreted as left-liberal adversarial reporting — its explicitly critical stance toward the BJP government means it surfaces friction points that generate international attention (CAA, press freedom, minority rights) but frames ambiguous developments negatively for the ruling party. The 2022 Meta/Tek Fog retraction damaged credibility — verify specific claims independently before incorporating into dossier analysis.

> Articles from **MP-IDSA** about defense doctrine and procurement should be interpreted as reflecting the Ministry of Defence's institutional perspective — staffed by retired military and diplomatic officers, its publications often prefigure MoD policy shifts. When MP-IDSA publishes on a doctrinal question, it signals that the defense establishment is actively deliberating the issue. Not journalism — primary analytical source material.

> Articles from **mea.gov.in**, **pib.gov.in**, **pmindia.gov.in**, and **sansadtv.nic.in** should be interpreted as official government communications — not journalism but primary source material. The gap between official language and actual policy is an analytical signal. Cross-check MEA statements against PIB releases for inter-ministerial consistency. Hindi-language PIB releases may frame the same policy differently than English versions — the framing gap is analytically significant.

### Tier 3 Sources

> Articles from **Carnegie India** about technology statecraft and U.S.-India relations should be interpreted as reflecting a global-integrationist analytical perspective — its position within the Carnegie Endowment network means it frames India's choices through the lens of international order, which may overstate India's alignment with Western positions. High analytical quality but low publication frequency.

> Articles from **Gateway House** about trade corridors, energy security, and IMEC should be interpreted as reflecting the Mumbai business community's foreign policy perspective — its geo-economic focus and corporate membership base mean it frames India's strategic choices through commercial opportunity, which provides a valuable complement to Delhi's security-centric think tanks.

> Articles from **FORCE Magazine** about defense procurement, indigenous manufacturing, and military exercises should be interpreted as specialist defence reporting with strong armed forces sourcing — contributors include serving and retired military officers, which gives it access that generalist outlets lack but also means coverage tends to reflect the military's institutional preferences on procurement and doctrine.

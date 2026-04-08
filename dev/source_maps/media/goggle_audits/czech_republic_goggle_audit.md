# AUDIT SUMMARY: CZECH REPUBLIC

**Sources assessed:** 19 recommended + 5 excluded + 4 newly identified = 28 total
**Tier 1 (boost=3):** 4 sources
**Tier 2 (boost=2):** 9 sources
**Tier 3 (boost=1):** 5 sources
**Neutral (no rule):** 7 sources
**Discard:** 3 sources
**Overall assessment:** The curation prompt produced a strong whitelist with excellent think-tank depth and an unusually robust public-broadcaster pair — a distinctive Czech advantage. Key changes: (1) resolved redundancy between the two public broadcasters by differentiating speed vs. investigative depth; (2) promoted government official sources for Layer 2 migration at Tier 2; (3) applied non-English domestic premium — Czech-language sources receive a structural boost because the pipeline's English-language bias systematically underweights the language in which Czech political discourse actually operates; (4) added missing presidential office and parliament sources; (5) no Czech domains appear on the blocked domains list, which is a significant operational advantage over many European country configurations.

---

## BOOST ASSIGNMENTS

### Tier 1 — `$boost=3`

**CTK (Ceska tiskova kancelar)** | `ctk.eu` | Type: `wire_service` | Status: `EXISTING`
- **Structural role:** Sole national wire service. Upstream supplier to virtually all Czech newsrooms. Ground-truth layer for government decisions, parliamentary votes, MFA statements, and defense procurement.
- **Domain coverage:** All five domains — baseline factual feed
- **Reasoning:** CTK is the Czech Republic's indispensable first-mover source. Every other Czech outlet rewrites CTK dispatches. In a country with a single national wire, that wire is Tier 1 by definition. Commercial subscription limits full-feed access, but headlines and selected stories are free on ctk.eu and Brave indexes them. The pipeline needs CTK surfacing first for any breaking government action.
- **Extraction note:** Commercial subscription required for full feed. Free headlines on ctk.eu are indexable. English-language service available, which aids pipeline ingestion.

**iROZHLAS.cz (Cesky rozhlas)** | `irozhlas.cz` | Type: `public_broadcaster` / `investigative` | Status: `EXISTING`
- **Structural role:** Public broadcaster news portal combining high-volume daily coverage with deep investigative capacity. Data journalism team produces structured datasets. Breaks stories on corruption, foreign-influence operations, and defense procurement.
- **Domain coverage:** All five domains; particularly strong on security, domestic constraints, and investigative pieces
- **Reasoning:** iROZHLAS combines CT24's public-service reliability with investigative teeth — it is both a daily news source and a periodic investigation breaker. 2.7 million unique users make it high-reach. Free, no paywall, Czech-language — ticks the non-English domestic premium. The data journalism team's structured output is uniquely pipeline-friendly. Tier 1 over CT24 because it produces original investigative reporting, not just broadcast coverage.
- **Non-English premium:** Czech-language source covering domestic political discourse in the language it actually occurs in.

**Denik N** | `denikn.cz` | Type: `independent_daily` | Status: `EXISTING`
- **Structural role:** Subscription-funded independent daily free of oligarchic ownership. The outlet Czech elites read for analytical depth on foreign policy, EU affairs, and political-party dynamics. Functions as the signal source when government-adjacent media may self-censor.
- **Domain coverage:** All five domains; particularly strong on diplomatic alignment and domestic constraints
- **Reasoning:** In a media landscape structurally distorted by oligarchic ownership (Babis/Agrofert/MAFRA history), Denik N's ownership independence is itself a structural asset. 28,000+ subscribers demonstrate market validation of its independence. Produces the analytical long-form pieces the pipeline needs to interpret daily events. Hard paywall limits extraction, but Brave indexes paywalled headlines for ranking. Tier 1 because independence + analytical depth + all-domain coverage is an irreplaceable combination.
- **Extraction note:** Hard paywall. Diffbot extraction likely partial. Brave headline indexing still provides ranking signal.
- **Non-English premium:** Czech-language analytical depth unavailable in any English-language source.

**Seznam Zpravy** | `seznamzpravy.cz` | Type: `investigative` / `digital_native` | Status: `EXISTING`
- **Structural role:** Highest-reach digital-native news outlet in Czechia. Backed by Seznam.cz (domestic tech platform, second only to Google in CZ). Aggressive investigative posture with video-first format.
- **Domain coverage:** All five domains; strong investigative and video journalism
- **Reasoning:** Reach + independence + investigative capacity. Seznam Zpravy survived a 2024 editorial-independence crisis, reinforcing credibility. Free, no paywall, Czech-language — maximally extractable. Known for high-profile investigations (arms industry, political corruption). Video-first format means the pipeline captures digital write-ups of stories that may break on video first. Tier 1 because it is the most accessible (free) high-signal Czech-language source with all-domain coverage.
- **Non-English premium:** Czech-language source; free and fully extractable.

---

### Tier 2 — `$boost=2`

**CT24 (Ceska televize)** | `ct24.ceskatelevize.cz` | Type: `public_broadcaster` | Status: `EXISTING`
- **Structural role:** Most-trusted news brand in Czechia. Public broadcaster with 24-hour news channel. Live coverage of parliamentary debates, government pressers, and EU/NATO summits.
- **Domain coverage:** Diplomatic alignment, domestic constraints, institutional engagement
- **Reasoning:** CT24 is Czechia's most trusted source, but its structural role is broadcast-first with web as secondary output. It covers events broadly but breaks fewer stories than iROZHLAS or Seznam Zpravy. Tier 2 rather than Tier 1 because the pipeline captures text, and CT24's text output — while reliable — is less distinctive than iROZHLAS's investigative/data journalism output. Still essential as the trust anchor.
- **Non-English premium:** Czech-language only; auto-translate viable for monitoring.

**Radio Prague International** | `english.radio.cz` | Type: `public_international_broadcaster` | Status: `EXISTING`
- **Structural role:** Primary English-language source produced inside the Czech public-media system. Foreign-policy section covers NATO, EU, bilateral relations.
- **Domain coverage:** Diplomatic alignment, institutional engagement, domestic constraints
- **Reasoning:** The only English-language source that is both domestically produced and institutionally credible. Essential for the English-language pipeline layer. However, it is a translation/adaptation service, not an original reporting outlet — the original reporting happens in Czech at iROZHLAS and CT24. Tier 2 because it serves a unique structural function (English-language access to Czech public media perspective) but is derivative of Czech-language reporting.

**Hospodarske noviny (HN)** | `hn.cz` | Type: `business_financial` | Status: `EXISTING`
- **Structural role:** Czechia's leading business daily. Read by policy and corporate elites. Essential for trade policy, industrial strategy, energy diversification, defense-budget negotiations, and EU economic governance positions.
- **Domain coverage:** Economic & technological statecraft, institutional engagement (EU single market, trade), domestic constraints (budget politics)
- **Reasoning:** Sole Tier-eligible source for economic statecraft depth. Economia ownership (Zdenek Bakala) is stable and non-governmental. Covers the USMCA-equivalent for Czech Republic — EU single market dynamics, trade policy, energy security — with a depth no other Czech outlet matches. Tier 2 rather than Tier 1 because its domain coverage is narrower (primarily economic) and it doesn't break political or security stories. Soft/metered paywall means partial extraction is viable.
- **Non-English premium:** Czech-language business coverage of domestic economic policy debates.

**Respekt** | `respekt.cz` | Type: `political_weekly` | Status: `EXISTING`
- **Structural role:** Czechia's premier political weekly. Deep investigative and analytical coverage of foreign policy, intelligence affairs, defense posture, and political scandals.
- **Domain coverage:** Diplomatic alignment, security & defense autonomy, domestic constraints
- **Reasoning:** Think tanks earn boost through depth, not speed — Respekt operates on the same principle as a weekly magazine. Its long-form tempo allows detection of slower-moving strategic shifts that daily outlets miss. Read by the educated professional class and political elite. Tier 2 rather than Tier 1 because weekly publication frequency limits its utility as a daily-cycle source, and its analytical depth overlaps partly with Denik N.
- **Non-English premium:** Czech-language analytical depth on foreign policy and security.

**vlada.gov.cz (Government Portal)** | `vlada.gov.cz` | Type: `official_government` | Status: `EXISTING` — **LAYER 2 MIGRATION**
- **Structural role:** Central hub for cabinet-level decisions: coalition agreements, budget approvals, defense-spending commitments, EU Council mandates.
- **Domain coverage:** All five domains (official source)
- **Reasoning:** Primary fetch via Layer 2 direct polling. Goggle boost at Tier 2 as belt-and-suspenders fallback. Government press releases occasionally surface in Brave News Search. English section limited but functional.

**mzv.gov.cz (Ministry of Foreign Affairs)** | `mzv.gov.cz` | Type: `official_government` | Status: `EXISTING` — **LAYER 2 MIGRATION**
- **Structural role:** Primary source for foreign-policy concept documents, bilateral statements, sanctions lists, travel advisories, and diplomatic appointments.
- **Domain coverage:** Diplomatic alignment, institutional engagement, security policy
- **Reasoning:** Layer 2 migration source. Published the 2025 Foreign Policy Concept. English-language press releases enable direct pipeline ingestion. RSS available. Goggle boost as fallback for Brave surfacing.

**mo.gov.cz (Ministry of Defence)** | `mo.gov.cz` | Type: `official_government` | Status: `EXISTING` — **LAYER 2 MIGRATION**
- **Structural role:** Primary source for defense-budget data, procurement contracts, NATO deployment decisions, bilateral military cooperation agreements, and arms-export notifications.
- **Domain coverage:** Security & defense autonomy
- **Reasoning:** Layer 2 migration source. Essential for procurement and NATO commitment tracking. English pages available but less comprehensive than Czech. Goggle boost as fallback.

**hrad.cz (Prague Castle — Presidential Office)** | `hrad.cz` | Type: `official_government` | Status: `NEW (from cz.yaml)` — **LAYER 2 MIGRATION**
- **Structural role:** Presidential office portal. President Petr Pavel's statements on foreign policy, defense, and institutional matters. Presidential veto and appointment powers make this a primary signal source.
- **Domain coverage:** Diplomatic alignment, security & defense autonomy, institutional engagement
- **Reasoning:** Present in cz.yaml as a Tier 1 government source but missing from the source intelligence map. Pavel is a former NATO Military Committee chair — his foreign-policy and defense statements carry unusual weight for a Czech president. Layer 2 migration with Tier 2 Goggle fallback.

---

### Tier 3 — `$boost=1`

**Aktualne.cz** | `aktualne.cz` | Type: `online_news_portal` | Status: `EXISTING`
- **Structural role:** Top-3 most-visited Czech news site. High-volume daily political and economic coverage. Strong opinion section capturing elite commentary.
- **Domain coverage:** Domestic constraints, economic statecraft, institutional engagement
- **Reasoning:** High traffic and elite opinion section are valuable, but Aktualne.cz's coverage overlaps heavily with Denik N, Seznam Zpravy, and HN. Economia group ownership (same as HN) means editorial overlap is structural, not accidental. Tier 3 because redundancy with higher-tier sources reduces its marginal value, but its volume and opinion-section framing still serve as supplementary signal.
- **Non-English premium:** Czech-language.

**HlidaciPes.org** | `hlidacipes.org` | Type: `investigative_nonprofit` | Status: `EXISTING`
- **Structural role:** Non-profit watchdog founded specifically to counter media oligarchisation. Award-winning investigations on Chinese (CEFC) and Russian influence operations.
- **Domain coverage:** Domestic constraints, economic statecraft (corruption, state contracts), security (foreign influence operations)
- **Reasoning:** Not a daily-news source — high-signal investigative supplement that publishes periodically. When it publishes, the investigations are high-impact (4.8 million users in 2023). Tier 3 because the pipeline can't depend on regular output, but the boost ensures its periodic investigations surface when they appear. Fills a unique niche on foreign-influence investigations.
- **Non-English premium:** Czech-language investigative depth.

**CZDEFENCE** | `czdefence.com` | Type: `defense_trade_press` | Status: `EXISTING`
- **Structural role:** Only dedicated Czech defense-sector publication. Detailed reporting on procurement programs (Gripen lease, CAESAR howitzers, SPYDER air defense), defense-industry exports, and military capability development.
- **Domain coverage:** Security & defense autonomy
- **Reasoning:** Single-domain (defense) but irreplaceable within it — no other Czech source systematically tracks procurement, modernization, and NATO interoperability at this depth. Bilingual (Czech + English) content makes it pipeline-accessible. Tier 3 because narrow domain scope and trade-press format limit broader analytical utility, but within defense it is the only game in town.

**AMO (Association for International Affairs)** | `amo.cz` | Type: `think_tank` | Status: `EXISTING`
- **Structural role:** Preeminent independent foreign-policy think tank. Publishes the annual "Agenda for Czech Foreign Policy" — the single most comprehensive yearly assessment of Czech strategic posture. Runs MapInfluenCE and CHOICE programs tracking Russian/Chinese influence.
- **Domain coverage:** All five domains
- **Reasoning:** Think tanks earn boost through depth, not speed. AMO's annual "Agenda" is the benchmark document for Czech foreign-policy posture assessment. MapInfluenCE and CHOICE provide structured analytical output on influence operations across CEE. Tier 3 rather than Tier 2 because publication frequency is low and the pipeline primarily needs daily-cycle sources. But when AMO publishes, the analytical depth is high-value.

**EUROPEUM** | `europeum.org` | Type: `think_tank` | Status: `EXISTING`
- **Structural role:** EU-focused think tank producing policy briefs on Czech-EU policy nexus — Council positions, cohesion-fund politics, EU foreign-policy coordination.
- **Domain coverage:** Institutional engagement, economic statecraft, diplomatic alignment (EU dimension)
- **Reasoning:** Complements AMO's broader scope with EU-specific depth. Tier 3 because its domain is narrower (EU only) and publication frequency is periodic. But for EU institutional engagement — the domain where Czech Republic's middle-power positioning is most active — EUROPEUM provides the analytical layer daily outlets lack. English publications available.

---

### Neutral — no Goggle rule

**Pravo / Novinky.cz** | `novinky.cz` | Type: `daily_broadsheet` / `news_portal` | Status: `EXISTING → NEUTRAL`
- **Why neutral:** Novinky.cz is the single most-visited news site in Czechia, but its coverage overlaps heavily with CT24, iROZHLAS, and Seznam Zpravy at higher tiers. Pravo's centre-left editorial line provides a useful counterweight, but the independent outlets (Denik N, Seznam Zpravy) already cover the spectrum. Under the Goggle model, Novinky.cz's massive traffic means Brave will rank it organically for most Czech queries — no boost needed, but no reason to discard. If a left-of-centre framing signal is needed, it will surface naturally.

**IIR (Institute of International Relations Prague)** | `iir.cz` | Type: `think_tank` | Status: `EXISTING → NEUTRAL`
- **Why neutral:** Valuable foreign-policy research institute (MFA-linked), but its structural proximity to the MFA establishment means it partially duplicates the government source layer. AMO and EUROPEUM at Tier 3 already provide the independent think-tank analytical function. IIR's "Czech Foreign Policy Analysis" annual series is high-value but low-frequency. Under Goggle model, organic ranking is appropriate — when IIR publishes major analysis, Brave will surface it without boost.

**European Values Center for Security Policy** | `europeanvalues.cz` | Type: `think_tank` | Status: `EXISTING → NEUTRAL`
- **Why neutral:** Hawkish transatlanticist security think tank with a unique Taiwan/China focus. Jakub Janda's output is high-profile but represents a specific ideological position (the hawkish end of Czech security-policy spectrum). Three think tanks at Tier 3 (AMO, EUROPEUM, CZDEFENCE-as-trade-press) already provide analytical depth. Adding a fourth boosted think tank over-weights the analytical layer relative to daily news. Leave at organic ranking — its hawkish framing will surface naturally for China/Russia/Taiwan queries.

**iDNES.cz / MF DNES / Lidove noviny (MAFRA group)** | `idnes.cz` | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Curation exclusion was correct under the hard-filter model — MAFRA's ownership history (Agrofert/Babis until 2023, Kaprain Group, then Babis re-acquisition of Agrofert in October 2025) creates structural editorial-independence concerns. Under the Goggle model, no reason to actively discard. iDNES.cz is among the most-visited Czech sites; if it breaks a major story, Brave will surface it and the pipeline benefits from seeing it. The dossier's interpretive context tells the LLM how to discount ownership-compromised sources.

**Blesk (Czech News Centre)** | `blesk.cz` | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Highest-circulation Czech tabloid. Covers politics superficially with no meaningful foreign-policy or defense analysis. Under the hard-filter model, exclusion was correct. Under the Goggle model, no reason to actively discard — its noise-to-signal ratio is high, but Brave's organic ranking will place it below boosted sources anyway. Occasional political splash stories may carry signal about populist framing.

**Expats.cz / Prague Morning / Brno Daily** | `expats.cz`, `praguemonitor.com`, `brnodaily.cz` | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** English-language expat portals that aggregate and simplify Czech-language reporting. Radio Prague International at Tier 2 already covers the English-language public-media function. No original reporting value, but no reason to actively discard — they won't outrank boosted sources in Brave.

**Reflex** | `reflex.cz` | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Weekly magazine with declining relevance and populist editorial drift. Superseded by Respekt and Denik N. Under Goggle model, organic ranking is fine — won't displace boosted sources.

---

### Discard — `$discard`

**Parlamentni listy** | `parlamentnilisty.cz` | Status: `CONFIRMED DISCARD`
- **Discard reasoning:** High-traffic aggregator that amplifies fringe, pro-Russian, and conspiratorial voices. Not a news outlet — functions as a platform for unvetted commentary that would actively displace higher-signal sources from top results. The curation prompt correctly identified this as a disinformation-amplification vector. Would inject noise and potentially misleading framing into the pipeline's event extraction.

**AC24.cz** | `ac24.cz` | Status: `NEW DISCARD`
- **Discard reasoning:** Conspiracy and disinformation site masquerading as alternative news. Amplifies anti-Western, pro-Russian narratives and COVID/vaccine conspiracy content. High traffic in Czech web ecosystem means Brave may surface it for political queries. Active discard prevents it from consuming result slots.

**Sputnik CZ / CZ24 News** | `cz24.news` | Status: `NEW DISCARD`
- **Discard reasoning:** Pro-Russian disinformation outlet operating under Czech-language branding. Part of the broader Russian state media ecosystem targeting Czech audiences. Active discard essential to prevent contamination of pipeline results.

---

## STRUCTURAL COVERAGE CHECK

| Structural Role | Source(s) | Tier | Notes |
|---|---|---|---|
| Government leak channel / signaling | vlada.gov.cz, Novinky.cz (Pravo) | T2, Neutral | Pravo's centre-left tradition makes it the occasional channel for social-democratic/left-leaning government signals. Under Babis, watch MAFRA outlets (iDNES — Neutral) for government-sympathetic framing |
| Opposition voice | Denik N, Seznam Zpravy, HlidaciPes | T1, T1, T3 | Czech opposition media is structurally strong — independent outlets emerged specifically in reaction to oligarchisation. SPOLU/ODS voices surface primarily through Denik N and Respekt |
| Defence/security first-mover | CZDEFENCE, mo.gov.cz, iROZHLAS | T3, T2, T1 | CZDEFENCE is the only dedicated defense press. MoD portal for procurement data. iROZHLAS breaks defense investigations |
| Policy-elite discourse | Respekt, Denik N, AMO | T2, T1, T3 | Respekt for weekly analytical depth; Denik N for daily elite reading; AMO's annual "Agenda" for benchmark posture assessment |
| Domestic-language depth | All Czech-language sources | T1–T3 | Czech political discourse operates primarily in Czech. English sources (Radio Prague International, CZDEFENCE English) are supplements, not substitutes. Non-English premium applied |
| Official government source | vlada.gov.cz, mzv.gov.cz, mo.gov.cz, hrad.cz | T2 | **LAYER 2 MIGRATION** — primary fetch via direct polling. Goggle boost as fallback. hrad.cz added from cz.yaml (missing in source map) |
| Analytical/think tank depth | AMO, EUROPEUM, IIR, European Values | T3, T3, Neutral, Neutral | Four think tanks is strong for a country of Czechia's size. AMO and EUROPEUM boosted; IIR and European Values at organic ranking to avoid over-weighting analytical layer |
| Wire service (international) | reuters.com, apnews.com, france24.com | Neutral | Per cz.yaml. Reuters is **blocked by Anthropic's crawler** but Brave can still surface it for discovery. AP News and France24 unblocked |
| Presidential foreign-policy signal | hrad.cz | T2 | Pavel's NATO background makes presidential statements unusually significant for defense/foreign policy. Added from cz.yaml |

**Gaps identified:**
1. **Czech arms-industry and defense-export intelligence** beyond CZDEFENCE's trade-press level remains thin. Monitoring Czech ammunition flows (particularly the ammunition initiative for Ukraine) may require supplementing with SIPRI, EU arms-export reports, or specialized OSINT feeds. The source map correctly identified this gap.
2. **Sub-national political dynamics** (regional governors, Senate composition) that can constrain foreign-policy mandates are underrepresented. CT24 and CTK partially cover this, but no dedicated regional-politics source is boosted.
3. **Parliament (psp.cz)** — the Chamber of Deputies portal is not in the source map or cz.yaml. Should be added to Layer 2 direct polling for legislative tracking (vote records, committee hearings on defense and foreign affairs).
4. **Czech National Bank (cnb.cz)** — present in cz.yaml actors (Ales Michl) but no CNB source is in the whitelist. For economic statecraft monitoring (monetary policy, sanctions compliance, FX intervention), CNB communications are primary source material. Consider adding to Layer 2.

---

## REDUNDANCY RESOLUTION

**Public broadcaster cluster: iROZHLAS + CT24 + Radio Prague International**
All three are Cesky rozhlas/Ceska televize public media. Resolved by differentiating structural function: iROZHLAS (Tier 1, investigative + data journalism + daily news), CT24 (Tier 2, broadcast trust anchor + live parliamentary coverage), Radio Prague International (Tier 2, English-language access path). iROZHLAS leads because it produces original investigative reporting the other two don't. Radio Prague International is derivative but serves the unique English-language pipeline function.

**Independent daily cluster: Denik N + Seznam Zpravy + Aktualne.cz**
Three digital-native outlets covering Czech politics. Resolved by ownership independence and reach: Denik N (Tier 1, subscription-funded independence + analytical depth), Seznam Zpravy (Tier 1, highest reach + investigative teeth + free extraction), Aktualne.cz (Tier 3, high traffic but Economia ownership overlap with HN + less distinctive editorial voice). Aktualne.cz drops because its coverage is structurally redundant with both Denik N (analytical) and HN (economic, same ownership group).

**Think tank cluster: AMO + EUROPEUM + IIR + European Values**
Four think tanks is generous for a single country. Resolved by domain differentiation and independence: AMO (Tier 3, broadest scope + flagship annual assessment), EUROPEUM (Tier 3, EU-specific depth), IIR (Neutral, MFA-linked establishment voice — partially duplicates government source layer), European Values (Neutral, hawkish security niche — ideologically distinctive but narrow). Two boosted, two organic prevents over-weighting the analytical layer.

**Government source cluster: vlada.gov.cz + mzv.gov.cz + mo.gov.cz + hrad.cz**
Four government portals all at Tier 2. No redundancy issue — each covers a distinct institutional function (cabinet, foreign affairs, defense, presidency). All marked for Layer 2 migration with Goggle boost as fallback.

---

## QUERY CONFIGURATION

```
country: CZ
search_lang: cs
freshness: pw
```

**Multi-language notes:** Czech political discourse operates overwhelmingly in Czech. English-language sources (Radio Prague International, CZDEFENCE English pages, think tank English publications) are supplements. Queries should run primarily in Czech (`cs`); a secondary English query cycle for defense, NATO, and EU topics would capture Radio Prague International, CZDEFENCE, and international wire coverage. The pipeline's existing `languages.metadata: en` configuration handles this correctly.

**Localized query vocabulary validation:**

The curation prompt's vocabulary is strong. Notes:

- **Domain 1 (Diplomatic):** All terms valid. Add `"Babis zahranicni politika"` and `"Pavel NATO"` as leader-specific patterns. `"Viseградska ctyrka"` is correct but V4 cohesion has weakened — consider adding `"Three Seas Initiative"` / `"Trimori"` as an alternative regional frame. Add `"Cina"` (China) and `"Tchaj-wan"` (Taiwan) given Czech-Taiwan relations are a distinctive foreign-policy signal.
- **Domain 2 (Security):** Strong list. Add `"Vrbeticе"` (Vrbetice ammunition depot explosion — ongoing Russia-related case). `"municni iniciativa"` is excellent and unique to Czech Republic's Ukraine support role. Add `"BIS"` (Security Information Service) — its annual reports are primary signals for hybrid threat assessment. Add `"SPYDER"` and `"Gripen"` as procurement-specific terms.
- **Domain 3 (Economic):** Valid. Add `"CEZ"` / `"jaderna elektrarna"` (nuclear power plant) — the Dukovany nuclear plant expansion is a major economic/security statecraft decision (Westinghouse vs. KHNP). Add `"Skoda"` for industrial policy tracking. `"energeticka bezpecnost"` is correct and high-priority given Czech gas diversification from Russia.
- **Domain 4 (Institutional):** Valid. `"predsednictvi Rady EU"` is historically relevant (Czech presidency in 2022) but less current. Add `"rozsireni EU"` (EU enlargement) — Czech Republic is an active supporter of Ukraine/Western Balkans accession. Add `"Bukurestsky format"` (Bucharest Nine / B9) as a relevant NATO sub-grouping.
- **Domain 5 (Domestic):** Strong. Add `"ANO"` and `"SPOLU"` as party-specific terms that signal coalition/opposition dynamics. Add `"Okamura SPD"` for far-right domestic constraint monitoring. `"vladni krize"` is valid. Add `"duchodova reforma"` (pension reform) as a current domestic constraint on fiscal space for defense spending.

**Stale/problematic terms:** `"predsednictvi Rady EU"` is backward-looking (2022 presidency) but still valid for institutional memory queries. No terms are actively misleading.

**Suggested topic query patterns:**

1. `Babis zahranicni politika NATO Ukrajina` — Babis government's NATO/Ukraine posture
2. `obranný rozpocet Ceska republika NATO 2%` — Defense spending and NATO 2% target
3. `Dukovany jaderna elektrarna Westinghouse KHNP` — Nuclear energy procurement decision
4. `BIS vyrocni zprava hybridni hrozby Rusko` — BIS annual report on Russian hybrid threats
5. `municni iniciativa Ceska republika Ukrajina` — Czech ammunition initiative for Ukraine
6. `Pavel Tchaj-wan Cina diplomaticke vztahy` — Presidential Taiwan/China policy signaling

---

## GOGGLE FILE

```goggle
! name: MPM Czech Republic
! description: MPM pipeline source prioritization for Czech Republic — boosts high-signal sources, discards noise
! public: false
! author: MPM Pipeline

! --- Tier 1: Essential (boost=3) ---
$boost=3,site=ctk.eu
$boost=3,site=irozhlas.cz
$boost=3,site=denikn.cz
$boost=3,site=seznamzpravy.cz

! --- Tier 2: Important (boost=2) ---
$boost=2,site=ct24.ceskatelevize.cz
$boost=2,site=english.radio.cz
$boost=2,site=hn.cz
$boost=2,site=respekt.cz
$boost=2,site=vlada.gov.cz
$boost=2,site=mzv.gov.cz
$boost=2,site=mo.gov.cz
$boost=2,site=hrad.cz
$boost=2,site=vlada.cz

! --- Tier 3: Supplementary (boost=1) ---
$boost=1,site=aktualne.cz
$boost=1,site=hlidacipes.org
$boost=1,site=czdefence.com
$boost=1,site=amo.cz
$boost=1,site=europeum.org

! --- Discard: Noise ---
$discard,site=parlamentnilisty.cz
$discard,site=ac24.cz
$discard,site=cz24.news
```

---

## INTERPRETIVE CONTEXT FOR DOSSIER

### Tier 1 Sources

> Articles from **CTK** about any domain should be interpreted as factual wire-service dispatches — CTK has no editorial line to discount. It is the baseline truth layer for what the Czech government officially announced, how parliament voted, and what the MFA stated. Discrepancies between CTK's factual dispatch and other outlets' framing are themselves analytical signals.

> Articles from **iROZHLAS** about security and domestic politics should be interpreted as Czechia's most authoritative public-media investigative reporting — its editorial independence is protected by law, and its data journalism team produces structured analysis unavailable elsewhere. When iROZHLAS breaks an investigation on corruption or foreign-influence operations, the story is credible and well-sourced. Its public-service mandate means it does not have an opposition or government-aligned frame — it is genuinely centrist-investigative.

> Articles from **Denik N** about foreign policy and EU affairs should be interpreted as reflecting the perspective of Czechia's liberal-democratic, pro-EU professional class — its subscription-funded independence from oligarchic ownership is a structural asset, but its editorial orientation is centre-liberal and pro-Western. Coverage critical of Babis government positions reflects genuine editorial independence, not opposition alignment per se, but the outlet's readership skews toward SPOLU/liberal-democratic constituencies. Essential for understanding how the educated urban elite frames Czech foreign-policy debates.

> Articles from **Seznam Zpravy** about political investigations and government accountability should be interpreted as aggressive, editorially independent investigative journalism — its 2024 editorial-independence crisis (and survival) reinforced its credibility. Backed by the domestic tech company Seznam.cz, it has no political-party alignment. Its video-first format means stories may surface as confrontational political interviews before written analysis. When Seznam Zpravy publishes an investigation, the source-access is typically strong.

### Tier 2 Sources

> Articles from **CT24** about parliamentary debates and government policy should be interpreted as the most trusted institutional news voice in Czechia — its public-service mandate and legal editorial independence make it the broadcast equivalent of a wire service. CT24 does not editorialize in its news coverage. Its framing of political events reflects mainstream Czech political center.

> Articles from **Radio Prague International** about Czech foreign policy should be interpreted as the Czech state's English-language information service — professionally independent but operating under a public-media mandate to explain Czech positions to international audiences. Its framing tends to be explanatory rather than critical, making it useful for understanding how Prague wants its foreign policy understood abroad. Not a substitute for Czech-language independent reporting.

> Articles from **Hospodarske noviny** about economic policy and trade should be interpreted as reflecting the Czech business establishment's perspective — its centre-right, pro-market editorial orientation means it frames economic policy through an investment-climate and EU single-market lens. Critical coverage of government economic intervention reflects private-sector preferences, not necessarily policy failure. Essential for understanding how economic elites view trade, energy, and industrial policy decisions.

> Articles from **Respekt** about security affairs and political analysis should be interpreted as Czechia's premier long-form analytical journalism — its centre-right liberal, pro-Western editorial orientation is comparable to The Economist. Respekt's weekly tempo means it provides structural interpretation rather than breaking news. Its intelligence and defense sourcing is strong, particularly on Russia-related security matters. Read by political elites and the educated professional class.

> Articles from **government portals** (vlada.gov.cz, mzv.gov.cz, mo.gov.cz, hrad.cz) should be interpreted as official government communications — not journalism but primary source material. Press releases, policy concept documents, and procurement announcements represent the government's chosen public position. Note the distinction between vlada.gov.cz (cabinet/PM — Babis) and hrad.cz (presidency — Pavel), which may diverge on foreign-policy and defense matters given Babis's more transactional and Pavel's more firmly transatlanticist orientations.

### Key Interpretive Dynamic

> The most important interpretive context for Czech Republic dossier construction is the **Babis-Pavel tension axis**. Prime Minister Babis (ANO) returned to office in late 2025 with a more pragmatic, occasionally Euro-skeptic posture, while President Pavel (former NATO Military Committee chair) represents firmly transatlanticist, pro-Ukrainian positions. Sources close to the government (vlada.gov.cz, and to a lesser extent MAFRA outlets at Neutral) will reflect Babis framing. Sources in the independent/liberal ecosystem (Denik N, Respekt, Seznam Zpravy) will tend to align more with Pavel's foreign-policy positions. Neither frame is "correct" — the dossier should present both and identify the tension as itself a structural feature of Czech foreign policy under divided executive authority.

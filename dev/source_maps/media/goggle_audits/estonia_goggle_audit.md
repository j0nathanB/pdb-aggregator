# AUDIT SUMMARY: ESTONIA

**Sources assessed:** 16 recommended + 3 excluded + 3 newly identified = 22 total
**Tier 1 (boost=3):** 3 sources
**Tier 2 (boost=2):** 7 sources
**Tier 3 (boost=1):** 5 sources
**Neutral (no rule):** 4 sources
**Discard:** 3 sources
**Overall assessment:** The curation prompt produced a compact, well-structured whitelist that reflects Estonia's small but highly digitized media market. The dominant structural feature is a three-source domestic core (ERR, Postimees, Delfi) that covers nearly all domains, supplemented by strong security/defense specialist outlets (ICDS, Diplomaatia, Propastop) appropriate for a frontline NATO state. Key changes: (1) promoted ERR to Tier 1 with a non-English domestic source premium — its Estonian- and Russian-language services make it the single most structurally important source in the ecosystem; (2) migrated government sources (valitsus.ee, riigikogu.ee, vm.ee, kaitseministeerium.ee) to Layer 2 with Tier 2 Goggle fallback; (3) flagged `aripaev.ee`, `delfi.ee`, and `ohtuleht.ee` as blocked by Anthropic's crawler — a severe constraint given that three of Estonia's top seven media sources are affected; (4) added BNS and ERR Russian Service as distinct boost entries to address the Baltic wire gap and the Russian-language monitoring imperative; (5) moved curation exclusions (Objektiiv, Postimees na Russkom, Telegram) to Neutral rather than Discard per audit principles.

---

## BOOST ASSIGNMENTS

### Tier 1 — `$boost=3`

**ERR (Eesti Rahvusringhääling)** | `err.ee` | Type: `paper_of_record` | Status: `EXISTING`
- **Structural role:** Estonia's public broadcaster and most trusted news source. Operates in Estonian, Russian (rus.err.ee / ETV+), and English — the only outlet spanning all three language communities. Dedicated defense section. Functions as Estonia's national agenda-setter and the authoritative voice during security crises.
- **Domain coverage:** All five domains
- **Reasoning:** ERR is the indispensable source for Estonia. It is the only outlet that simultaneously addresses the Estonian-speaking majority, the Russian-speaking minority (critical for a frontline state monitoring Kremlin-narrative penetration), and the international English-speaking audience. Non-English domestic source premium applies: ERR's Estonian- and Russian-language content captures signals invisible to English-only sources. Free and fully extractable, no paywall, no crawler blocks. In a small media market, ERR functions as paper of record, defense monitor, and minority-language bridge simultaneously.
- **Extraction note:** Free. Multiple language subdirectories: `news.err.ee` (Estonian), `rus.err.ee` (Russian), `news.err.ee/eng` (English). All extractable.

**Postimees** | `postimees.ee` | Type: `paper_of_record` | Status: `EXISTING`
- **Structural role:** Estonia's oldest (1857) and most-read daily newspaper. Sets the national political agenda alongside ERR. English edition at `news.postimees.ee` provides international accessibility.
- **Domain coverage:** All five domains
- **Reasoning:** Postimees and ERR together form the essential broadsheet pair for Estonian domestic coverage. Postimees occupies the center-right editorial position and its front-page framing drives political debate. Ownership by Margus Linnamäe's Postimees Grupp has raised editorial-independence concerns — this is a known bias the interpretive context must address — but structural role outweighs editorial quality concerns. Partially paywalled but headlines and lead paragraphs are accessible for ranking purposes.
- **Extraction note:** Partially paywalled. Diffbot may get partial text. Not blocked by Anthropic's crawler.

**ICDS (International Centre for Defence and Security)** | `icds.ee` | Type: `security_defense` | Status: `EXISTING`
- **Structural role:** Estonia's premier defense and security think tank. Publishes the journal Diplomaatia, hosts the annual Lennart Meri Conference, and produces policy briefs that directly shape Estonian and Baltic security policy discourse.
- **Domain coverage:** Security & defense autonomy, Diplomatic alignment
- **Reasoning:** For a frontline NATO state where security/defense is the dominant analytical domain, ICDS is structurally essential at the highest tier. Think tanks normally earn boost through depth not speed, but ICDS occupies a unique dual role: it publishes Diplomaatia (the country's only foreign-affairs journal) AND produces the policy analysis that Estonian decision-makers cite. The `icds.ee` domain captures both the think tank's own publications and Diplomaatia content (which also appears at `diplomaatia.ee`). In a media ecosystem with no dedicated defense press, ICDS is the closest equivalent to a Jane's for Estonian strategic thinking. Free and fully extractable.

---

### Tier 2 — `$boost=2`

**Delfi Estonia** | `delfi.ee` | Type: `paper_of_record` | Status: `EXISTING` — **BLOCKED**
- **Structural role:** Most-visited news portal in Estonia. Russian-language version (`rus.delfi.ee`) is a key monitor for Russian-speaking audience sentiment. Ekspress Grupp ownership.
- **Domain coverage:** All five domains
- **Reasoning:** Delfi would merit Tier 1 on traffic and domain breadth alone, but two factors push it to Tier 2: (1) **blocked by Anthropic's crawler** (`delfi.ee` in blocked domains list), meaning extraction will fail even when Brave surfaces it; (2) its commercially centrist editorial orientation and aggregation-heavy model mean it breaks fewer stories than ERR or Postimees. The Goggle boost at Tier 2 ensures Brave still discovers Delfi URLs (useful as signal even without full extraction), while the tier reduction reflects extraction unreliability. Russian-language `rus.delfi.ee` is structurally critical for monitoring Russophone sentiment — the blocked status is a significant pipeline limitation.
- **Extraction note:** **BLOCKED by Anthropic crawler.** Brave can discover but pipeline cannot extract. Consider monitoring Delfi headlines via Layer 2 RSS fallback.

**Eesti Päevaleht** | `epl.delfi.ee` | Type: `paper_of_record` | Status: `EXISTING`
- **Structural role:** Second national daily. Center-liberal orientation (Ekspress Grupp). Strong on domestic politics, coalition dynamics, and parliamentary reporting.
- **Domain coverage:** Diplomatic alignment, Domestic constraints
- **Reasoning:** Fills the center-liberal editorial niche that balances Postimees's center-right orientation. Coalition dynamics reporting is essential for a country where government formation directly drives defense and foreign policy. Paywalled, which limits extraction, but its role as the second daily earns Tier 2. Hosted on `epl.delfi.ee` subdomain — note that `delfi.ee` is blocked, which may affect this subdomain's extractability.
- **Extraction note:** Paywalled. Subdomain of blocked `delfi.ee` — extraction may be affected.

**Eesti Ekspress** | `ekspress.delfi.ee` | Type: `investigative` | Status: `EXISTING`
- **Structural role:** Estonia's premier investigative weekly. Breaks corruption, defense-procurement, and national-security stories. Ekspress Grupp.
- **Domain coverage:** Domestic constraints, Security & defense autonomy, Economic & technological statecraft
- **Reasoning:** In a small media market, the premier investigative outlet earns Tier 2 for its unique ability to break stories that daily outlets cannot. Defense procurement and cybersecurity investigations are its highest-value beats for the pipeline. Paywalled and hosted on an `ekspress.delfi.ee` subdomain (potentially affected by `delfi.ee` block), but the investigative depth is structurally irreplaceable.
- **Extraction note:** Paywalled. Subdomain of blocked `delfi.ee` — extraction may be affected.

**ERR Russian Service** | `rus.err.ee` | Type: `paper_of_record` | Status: `EXISTING` — separate boost entry
- **Structural role:** Primary reliable Russian-language news source for Estonia's Russian-speaking minority (~25% of population). Monitors how official policy reaches the Russophone audience.
- **Domain coverage:** Domestic constraints, Security & defense autonomy
- **Reasoning:** Given a separate Tier 2 boost entry (distinct from ERR's Tier 1 `err.ee` entry) because the Russian-language service fills a structurally distinct role — it is the primary monitor for how Kremlin counter-narratives penetrate or fail to penetrate Estonia's Russophone community. Non-English domestic source premium applies doubly: this is a Russian-language source in a country where Russian-language media monitoring is a national security priority. The curation prompt's coverage gap assessment explicitly flagged independent Russian-language journalism as the ecosystem's main blind spot — ERR's Russian service is the best available mitigation. Free and extractable.

**valitsus.ee (Government Portal)** | `valitsus.ee` | Type: `government_aligned` | Status: `NEW` — **LAYER 2 MIGRATION**
- **Structural role:** Central government web portal. Prime Minister's communications, cabinet decisions, policy announcements.
- **Domain coverage:** All five domains (official source)
- **Reasoning:** Primary fetch via Layer 2 direct polling. Goggle boost at Tier 2 as belt-and-suspenders fallback. The `ee.yaml` config lists `valitsus.ee` as the government portal at Tier 1 — in the Goggle model, government official sources migrate to Layer 2 for direct polling with Tier 2 Goggle fallback. Not boosted to Tier 1 because government press releases are primary source material, not journalism.

**Ministry of Foreign Affairs** | `vm.ee` | Type: `government_aligned` | Status: `EXISTING` — **LAYER 2 MIGRATION**
- **Structural role:** Official foreign ministry communications. Press releases, foreign minister statements, Estonian positions on EU/NATO issues.
- **Domain coverage:** Diplomatic alignment, Institutional engagement
- **Reasoning:** Layer 2 migration — primary fetch via direct polling, Tier 2 Goggle fallback. For a frontline NATO state, MFA communications are high-signal primary sources for tracking diplomatic positioning.

**Ministry of Defence** | `kaitseministeerium.ee` | Type: `government_aligned` | Status: `EXISTING` — **LAYER 2 MIGRATION**
- **Structural role:** Defense budget documents, procurement announcements, host-nation support agreements, NATO exercise communiqués.
- **Domain coverage:** Security & defense autonomy
- **Reasoning:** Layer 2 migration — primary fetch via direct polling, Tier 2 Goggle fallback. Defense ministry releases are the first-mover source for procurement, conscription changes, and allied force presence decisions. In a country where defense spending is ~3% of GDP and rising, this is structurally critical.

---

### Tier 3 — `$boost=1`

**Äripäev** | `aripaev.ee` | Type: `business_financial` | Status: `EXISTING` — **BLOCKED**
- **Structural role:** Estonia's leading business daily (fully digital since 2022). Covers trade policy, sanctions, fintech, EU economic regulation, and the digital economy.
- **Domain coverage:** Economic & technological statecraft, Institutional engagement
- **Reasoning:** Would merit Tier 2 as the sole business/financial specialist, but **blocked by Anthropic's crawler** (`aripaev.ee` in blocked domains list). Extraction will fail even when Brave surfaces it. Demoted to Tier 3 — the boost ensures Brave still discovers Äripäev URLs (headline signal), but the pipeline cannot depend on it for full-text extraction. Also paywalled, compounding the extraction problem. Estonia's economic statecraft coverage becomes a partial blind spot. ERR's and Postimees's economic sections must compensate.
- **Extraction note:** **BLOCKED by Anthropic crawler.** Also paywalled. Double extraction barrier.

**Õhtuleht** | `ohtuleht.ee` | Type: `paper_of_record` | Status: `EXISTING` — **BLOCKED**
- **Structural role:** Third-largest daily. Tabloid/populist-centrist. Mass-market readership makes it a barometer of popular sentiment on defense spending, NATO, and immigration.
- **Domain coverage:** Domestic constraints
- **Reasoning:** Tabloid-format populist barometer — useful for gauging mass sentiment that elite broadsheets miss. However, **blocked by Anthropic's crawler** (`ohtuleht.ee` in blocked domains list), and its domestic-constraints-only coverage limits structural importance. Tier 3 provides discovery boost without pipeline dependency.
- **Extraction note:** **BLOCKED by Anthropic crawler.** Partially paywalled.

**Propastop** | `propastop.org` | Type: `security_defense` | Status: `EXISTING`
- **Structural role:** Disinformation monitoring blog run by Estonian Defence League (Kaitseliit) volunteers. Tracks Russian information warfare targeting Estonia and the Baltic states.
- **Domain coverage:** Security & defense autonomy (information warfare focus)
- **Reasoning:** Unique niche — no other source on the list systematically monitors Russian disinformation targeting Estonia. For a frontline state where hybrid threats are a primary security concern, this fills a real structural gap. Tier 3 rather than Tier 2 because publication frequency is irregular, the volunteer editorial model limits consistency, and its narrow focus (information warfare only) constrains domain coverage. But within its niche, nothing on the whitelist competes.
- **Extraction note:** Free. Extractable.

**Riigikogu (Parliament)** | `riigikogu.ee` | Type: `legislative_official` | Status: `EXISTING` — **LAYER 2 MIGRATION**
- **Structural role:** Parliamentary committee transcripts, legislative tracking, government oversight documentation. Estonia's unicameral parliament is the primary arena for coalition politics.
- **Domain coverage:** Institutional engagement, Domestic constraints
- **Reasoning:** Layer 2 migration — primary fetch via direct polling. Tier 3 Goggle fallback (lower than the executive-branch government sources because parliamentary documents surface less frequently in news search). Committee transcripts are valuable for tracking defense-budget debates and EU-policy positions but are slow-cycle documents, not breaking news.

**Maaleht** | `maaleht.ee` | Type: `regional` | Status: `EXISTING`
- **Structural role:** Largest rural weekly. Monitors agricultural policy, EU subsidy debates, and rural sentiment that constrains government flexibility on trade and climate diplomacy.
- **Domain coverage:** Domestic constraints
- **Reasoning:** Narrow scope (rural/agricultural) but fills a structural gap — no other source on the list captures rural Estonia's political sentiment, which matters for coalition politics (Centre Party and EKRE draw heavily from rural constituencies). Partially paywalled. Tier 3 for supplementary domestic-constraints depth.

---

### Neutral — no Goggle rule

**Objektiiv** | `objektiiv.ee` | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Curation prompt excluded for sharing content from unreliable sources (InfoWars, Breitbart). Under Goggle model, exclusions default to Neutral not Discard. Objektiiv occupies the conservative-Christian editorial niche in Estonian media — a voice that exists in the political ecosystem even if journalistic standards are lower. If it surfaces organically for a query, the pipeline benefits from seeing the conservative framing. No boost, but no active suppression either.

**Postimees na Russkom** | `rus.postimees.ee` | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Curation prompt noted this has been significantly scaled back and that `rus.delfi.ee` and `rus.err.ee` provide better Russian-language coverage. Correct assessment — but under Goggle model, no reason to actively discard. If it surfaces organically, it provides a supplementary Russian-language signal. No boost because `rus.err.ee` (Tier 2) already covers the Russian-language monitoring role with better reliability.

**BNS (Baltic News Service)** | `bns.ee` | Type: `paper_of_record` (wire) | Status: `EXISTING → NEUTRAL`
- **Why neutral:** Pan-Baltic wire service and primary breaking-news source. Subscription-only, which limits extraction. Wire services are not boosted in the Goggle — wire copy is available organically and typically feeds into other outlets (ERR, Postimees, Delfi all carry BNS dispatches). If BNS surfaces directly in Brave results, it provides value; but its signal is already captured through the boosted outlets it feeds. No boost, no discard.

**Diplomaatia** | `diplomaatia.ee` | Type: `security_defense` | Status: `EXISTING → NEUTRAL`
- **Why neutral:** Published by ICDS, which is already boosted at Tier 1 via `icds.ee`. Content from Diplomaatia also appears on `icds.ee`. Boosting both domains would be redundant. If Brave surfaces a `diplomaatia.ee` URL directly, the pipeline benefits — but the Tier 1 boost on `icds.ee` already captures this content. Neutral avoids double-counting.

---

### Discard — `$discard`

**Sputnik Estonia** | `sputnik-news.ee` (and variants) | Status: `NEW DISCARD`
- **Discard reasoning:** Russian state-sponsored media outlet. Estonia banned Sputnik's Estonian operations in 2019, but cached and mirrored content may still surface in search results. Active suppression prevents Kremlin propaganda from consuming result slots that should go to legitimate Estonian sources.

**Baltnews** | `baltnews.ee` | Status: `NEW DISCARD`
- **Discard reasoning:** Rossiya Segodnya-affiliated Baltic-focused outlet. Russian state-media proxy targeting Baltic Russian-speakers. Same rationale as Sputnik — active suppression of state-sponsored disinformation sources.

**Rubaltic.ru** | `rubaltic.ru` | Status: `NEW DISCARD`
- **Discard reasoning:** Russian-language outlet focused on Baltic states with documented ties to Russian information operations. Frames Baltic security policy through a Kremlin-aligned lens. Would inject hostile-narrative noise and displace legitimate sources.

---

## STRUCTURAL COVERAGE CHECK

| Structural Role | Source(s) | Tier | Notes |
|---|---|---|---|
| Government communication channel | ERR, Postimees | T1, T1 | ERR is the primary outlet for government press conferences and crisis communication. Postimees carries government messaging through its news coverage. |
| Opposition voice | Eesti Ekspress, Eesti Päevaleht | T2, T2 | Investigative reporting on government failures. EKRE opposition narratives surface through Õhtuleht (T3, blocked) and Objektiiv (Neutral). |
| Defence/security first-mover | ICDS, ERR (defense section), Propastop | T1, T1, T3 | ICDS for analytical depth; ERR's defense section for breaking military news; Propastop for information-warfare monitoring. Kaitseministeerium.ee (T2, Layer 2) for official releases. |
| Policy-elite discourse | ICDS, Diplomaatia | T1, Neutral | ICDS publications and the Lennart Meri Conference shape elite security-policy debate. Diplomaatia neutral due to redundancy with `icds.ee`. |
| Domestic-language depth | ERR, Postimees, Eesti Päevaleht, Eesti Ekspress, Äripäev, Õhtuleht, Maaleht | T1–T3 | Estonian-language sources dominate the whitelist. Non-English domestic source premium applied to ERR (T1) and ERR Russian Service (T2). English-language content is supplementary (ICDS English publications, Postimees English edition). |
| Russian-language monitoring | ERR Russian Service, (Delfi Russian — blocked) | T2, (T2 blocked) | Critical structural role for a frontline state. ERR Russian Service is the reliable monitor; Delfi Russian is blocked by crawler. Main ecosystem blind spot per curation prompt. |
| Official government source | valitsus.ee, vm.ee, kaitseministeerium.ee, riigikogu.ee | T2, T2, T2, T3 | **LAYER 2 MIGRATION** — primary fetch via direct polling. Goggle boost as fallback. |
| Analytical/think tank depth | ICDS | T1 | ICDS is the sole think tank but covers security, defense, and diplomatic alignment comprehensively. No domestic economic-policy think tank on the list (Praxis would be a candidate but was not in the curation prompt). |
| Wire service | BNS, Reuters, AP News | Neutral | BNS is subscription-only; Reuters is blocked by Anthropic crawler. Wire signal is captured through the domestic outlets BNS feeds into. |
| Economic/business specialist | Äripäev | T3 (blocked) | **Significant gap.** Äripäev is the sole business specialist but is blocked by Anthropic's crawler and paywalled. Economic statecraft coverage depends on ERR and Postimees general-interest economic sections. |

**Gaps identified:**
1. **Economic statecraft specialist** is effectively a blind spot. Äripäev is blocked and paywalled. No alternative domestic business publication exists in Estonia's small market. Mitigation: ERR's economic reporting and Postimees's business section carry some signal, but neither provides the depth of a dedicated business daily. Consider Layer 2 RSS monitoring of Äripäev as a workaround.
2. **Independent Russian-language investigative journalism** remains the ecosystem's structural gap as flagged by the curation prompt. Since the closure of Russian-language print dailies, only ERR's Russian service provides reliable Russian-language journalism from within Estonia. `rus.delfi.ee` would help but is blocked.
3. **Regional/local government coverage** is absent. Estonia is small enough that national outlets cover most local issues, but municipal politics in Tallinn (where the Centre Party historically dominated with Russian-speaking voter support) and Narva (border city, overwhelmingly Russian-speaking) are under-monitored.
4. **Cyber/digital policy specialist** — Estonia is a global leader in e-governance and cyber defense (NATO CCDCOE is based in Tallinn), but no specialist technology outlet appears on the list. ICDS covers cybersecurity from a defense perspective; RIA (Information System Authority) press releases via Layer 2 would strengthen this.

---

## REDUNDANCY RESOLUTION

**Broadsheet cluster: ERR + Postimees + Delfi + Eesti Päevaleht + Õhtuleht**
Estonia's five major general-news outlets. Resolved by differentiating structural roles: ERR (Tier 1, public broadcaster, multi-language, most trusted), Postimees (Tier 1, agenda-setter, center-right daily), Delfi (Tier 2, highest traffic but blocked and more aggregation-heavy), Eesti Päevaleht (Tier 2, center-liberal second daily), Õhtuleht (Tier 3, populist barometer but blocked). ERR and Postimees form the essential pair; the remaining three are supplementary with extraction constraints reducing their effective value.

**Security/defense cluster: ICDS + Diplomaatia + Propastop**
Three security-focused sources in a country where security is the dominant analytical domain. Resolved by consolidating: ICDS at Tier 1 (captures both think-tank analysis and Diplomaatia content since the latter is published by ICDS), Diplomaatia moved to Neutral (redundant with `icds.ee`), Propastop at Tier 3 (unique niche in information-warfare monitoring that ICDS does not cover). No redundancy — each serves a distinct function within the security domain.

**Government official cluster: valitsus.ee + vm.ee + kaitseministeerium.ee + riigikogu.ee**
Four government domains. All migrated to Layer 2 with Goggle fallback. Differentiated by Goggle tier: executive-branch sources (valitsus.ee, vm.ee, kaitseministeerium.ee) at Tier 2 fallback because they publish more frequently and are more likely to surface in news search; parliamentary source (riigikogu.ee) at Tier 3 because committee transcripts and legislative documents surface less frequently in Brave.

**Russian-language cluster: ERR Russian Service + Delfi Russian**
Two Russian-language outlets. ERR Russian Service gets its own Tier 2 entry for structural importance. Delfi Russian is covered by the Delfi Tier 2 entry (same domain). The blocked status of `delfi.ee` means ERR Russian Service carries the full weight of Russian-language monitoring.

**Ekspress Grupp cluster: Delfi + Eesti Päevaleht + Eesti Ekspress + Maaleht**
Four outlets under the same ownership group. Differentiated by function: Delfi (Tier 2, portal/aggregator), Eesti Päevaleht (Tier 2, second daily), Eesti Ekspress (Tier 2, investigative weekly), Maaleht (Tier 3, rural weekly). Same ownership does not mean same editorial function. Note that three of four are hosted on `delfi.ee` subdomains, meaning the `delfi.ee` crawler block may affect `epl.delfi.ee` and `ekspress.delfi.ee` extraction.

---

## QUERY CONFIGURATION

```
country: EE
search_lang: et
freshness: pw
```

**Multi-language notes:** Estonia's media ecosystem operates in three languages: Estonian (primary), Russian (minority community, ~25% of population), and English (think tank publications, international-facing content). Queries should run primarily in Estonian; a secondary Russian query cycle for security/defense and domestic-constraints topics captures ERR Russian Service and `rus.delfi.ee` signals. A tertiary English query for security/defense captures ICDS English-language publications and international wire coverage. The pipeline's existing `languages.primary: et`, `languages.additional: [ru]`, `languages.metadata: en` configuration handles this correctly.

**Localized query vocabulary validation:**

The curation prompt's vocabulary is solid. Notes:

- **Domain 1 (Diplomatic):** All terms valid. Add `"Michal välispoliitika"` and `"Tsahkna"` as leader-specific patterns. `"Balti koostöö"` and `"Põhjamaade koostöö"` are particularly high-value — Estonia's diplomatic identity is defined by its Baltic-Nordic positioning. Consider adding `"Hiina"` (China) — Estonia's evolving China stance (post-Three Seas, post-Huawei) is an undermonitored diplomatic signal.
- **Domain 2 (Security):** Strong list. Add `"Pevkur"` (current Defence Minister, face of defense policy). `"eFP"` (enhanced Forward Presence) and `"Tapa"` (location of NATO battlegroup) are essential for tracking allied troop presence. `"CCDCOE"` (Cooperative Cyber Defence Centre of Excellence) for cyber-defense coverage. `"mobilisatsioon"` (mobilization) — relevant given Estonia's conscription expansion debates. Add `"Vene piir"` (Russian border) for border-security monitoring.
- **Domain 3 (Economic):** Good base. Add `"e-residentsus"` (e-Residency) — Estonia's signature digital governance program. `"Rail Baltic"` / `"Rail Baltica"` — the major infrastructure project connecting Baltic states to Europe. `"LNG terminal"` for energy security. `"Eesti Energia"` for state energy company coverage. `"startup"` — Estonia's tech startup ecosystem is policy-relevant for economic statecraft.
- **Domain 4 (Institutional):** Valid. Add `"kolme mere algatus"` (Three Seas Initiative) — important multilateral framework for Estonia. `"EL eesistuja"` (EU presidency) for tracking Estonia's EU engagement. `"OSCE"` for institutional engagement monitoring.
- **Domain 5 (Domestic):** Strong. Add `"Reformierakond"` (Reform Party — governing party, essential for coalition monitoring). `"Keskerakond"` (Centre Party — historically dominant among Russian-speakers). `"EKRE"` is already covered in the ee.yaml actors list. Add `"pensionireform"` (pension reform) and `"keelereform"` (language reform — the Russian-language school transition is a major domestic constraint). `"kohalikud valimised"` (local elections).

**Russian-language query terms validation:**
The five Russian terms in the curation prompt (оборона, НАТО, санкции, кибербезопасность, внешняя политика) are a good core. Add:
- `"эстонское гражданство"` (Estonian citizenship) — hot topic in Russophone community
- `"языковая реформа"` (language reform) — Russian school transition
- `"Нарва"` (Narva) — border city, bellwether for Russian-speaking community issues
- `"мобилизация"` (mobilization) — defense debates as perceived by Russian speakers

**Stale/problematic terms:** None are stale. All terms remain relevant for a frontline NATO state in the current security environment.

**Suggested topic query patterns:**

1. `Michal kaitsekulutused NATO eelarve` — Defense spending and NATO burden-sharing
2. `Pevkur ajateenistus mobilisatsioon Kaitsevägi` — Conscription reform and military readiness
3. `Tsahkna EL sanktsioonid Venemaa` — EU sanctions policy and Russia relations
4. `EKRE Reformierakond koalitsioon Riigikogu` — Coalition politics and opposition dynamics
5. `küberjulgeolek CCDCOE hübriidohud` — Cybersecurity and hybrid threat response
6. `Rail Baltic energiajulgeolek LNG` — Infrastructure and energy security
7. `keelereform vene kool haridus` — Russian-language school reform (domestic constraint)

---

## GOGGLE FILE

```goggle
! name: MPM Estonia
! description: MPM pipeline source prioritization for Estonia — boosts high-signal sources, discards Kremlin-linked noise
! public: false
! author: MPM Pipeline

! --- Tier 1: Essential (boost=3) ---
$boost=3,site=err.ee
$boost=3,site=postimees.ee
$boost=3,site=icds.ee

! --- Tier 2: Important (boost=2) ---
$boost=2,site=delfi.ee
$boost=2,site=epl.delfi.ee
$boost=2,site=ekspress.delfi.ee
$boost=2,site=rus.err.ee
$boost=2,site=valitsus.ee
$boost=2,site=vm.ee
$boost=2,site=kaitseministeerium.ee

! --- Tier 3: Supplementary (boost=1) ---
$boost=1,site=aripaev.ee
$boost=1,site=ohtuleht.ee
$boost=1,site=propastop.org
$boost=1,site=riigikogu.ee
$boost=1,site=maaleht.ee

! --- Discard: Kremlin-linked noise ---
$discard,site=sputnik-news.ee
$discard,site=baltnews.ee
$discard,site=rubaltic.ru
```

---

## INTERPRETIVE CONTEXT FOR DOSSIER

### Tier 1 Sources

> Articles from **ERR** about any domain should be interpreted as Estonia's most trusted and editorially independent news source — as the public broadcaster, ERR's reporting reflects institutional Estonia's consensus view on security and foreign policy, which skews strongly pro-NATO and pro-EU. This is not bias in the journalistic sense but reflects genuine national consensus in a frontline state. ERR's defense section (`news.err.ee/k/defense`) is the first-mover for military and security developments. Its Russian-language service (`rus.err.ee`) provides the only reliable window into how Estonian policy is communicated to the Russophone minority.

> Articles from **Postimees** about government policy and coalition politics should be interpreted with awareness that owner Margus Linnamäe's business interests (healthcare, retail, media) create potential conflicts of interest on economic regulation and healthcare policy. The editorial-independence concerns raised since Linnamäe's ownership consolidation mean Postimees's framing of business regulation and competition policy should be cross-checked against ERR and Eesti Päevaleht. On security and foreign policy, Postimees's center-right orientation aligns with national consensus and its coverage is reliable.

> Articles from **ICDS** about security policy and NATO affairs should be interpreted as reflecting Estonia's pro-Euro-Atlantic security establishment consensus — ICDS analysts are deeply embedded in NATO and EU policy networks, and their analysis reflects the perspective of Estonia's defense policy elite. This is the perspective of people who shape policy, not external critics. ICDS publications are authoritative for understanding Estonian strategic thinking but should not be mistaken for neutral academic analysis — they advocate for specific policy positions (increased defense spending, stronger deterrence, tighter sanctions on Russia).

### Tier 2 Sources

> Articles from **Delfi** about any topic should be interpreted as commercially driven news coverage with broad reach — Delfi is Estonia's most-visited portal, meaning its editorial selection reflects what drives clicks in the Estonian market. Its Russian-language edition (`rus.delfi.ee`) is commercially motivated but structurally valuable for monitoring what narratives gain traction in the Russophone community. **Note: Delfi is blocked by Anthropic's crawler — any Delfi content in the pipeline comes from Brave discovery only, not full extraction.**

> Articles from **Eesti Päevaleht** about domestic politics and coalition dynamics should be interpreted as center-liberal analysis from Ekspress Grupp — its editorial orientation provides a counterbalance to Postimees's center-right framing. On coalition politics, EPL's reporting is particularly strong for understanding internal party dynamics and government formation negotiations.

> Articles from **Eesti Ekspress** about corruption, defense procurement, or national security should be interpreted as Estonia's most credible investigative journalism — when Eesti Ekspress publishes an investigation, it has typically been through rigorous editorial review. Its Ekspress Grupp ownership introduces no meaningful bias on security/defense topics. Investigations appearing here are high-confidence signals.

> Articles from **ERR Russian Service** about Estonian policy as experienced by the Russian-speaking community should be interpreted as the Estonian state's most direct communication channel to Russophone citizens — ERR Russian is editorially independent but its existence is itself a policy instrument. What it chooses to cover and how it frames Estonian government decisions for Russian speakers reveals the state's integration and communication strategy. Absence of coverage on a topic may signal deliberate editorial avoidance of sensitive community issues.

> Articles from **valitsus.ee**, **vm.ee**, and **kaitseministeerium.ee** should be interpreted as official government communications — not journalism but primary source material. These represent the government's chosen public position. For Estonia, defense ministry communications are particularly high-signal because procurement announcements and allied-force hosting decisions often appear here before media coverage. Foreign ministry statements reveal Estonia's diplomatic positioning on EU and NATO issues with precision that media coverage may simplify.

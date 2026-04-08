# AUDIT SUMMARY: GERMANY

**Sources assessed:** 17 recommended + 5 excluded + 4 newly identified = 26 total
**Tier 1 (boost=3):** 4 sources
**Tier 2 (boost=2):** 8 sources
**Tier 3 (boost=1):** 5 sources
**Neutral (no rule):** 5 sources
**Discard:** 4 sources
**Overall assessment:** The curation prompt produced a structurally sound whitelist with excellent think-tank and broadsheet coverage for a major European power. Key challenges: (1) **8 of 17 recommended sources are blocked by Anthropic's crawler** (`faz.net`, `sueddeutsche.de`, `zeit.de`, `spiegel.de`, `n-tv.de`, `dw.com`, `fr.de`, `politico.eu`), making Germany one of the hardest countries for extraction — Brave can still discover these for ranking, but full-text extraction will fail; (2) resolved broadsheet redundancy by differentiating editorial function rather than quality; (3) promoted government official sources for Layer 2 migration; (4) added missing defense-specialist and wire coverage; (5) applied non-English domestic-language boost premium — German-language sources with extractable content get priority over blocked German sources with equivalent coverage.

**Blocked domain impact:** Germany is severely affected by Anthropic crawler blocks. The six papers of record / major outlets that are blocked (FAZ, SZ, Die Zeit, Der Spiegel, n-tv, Politico EU) represent the core of the quality press. The pipeline must rely on Brave discovery + headline-level signals from these sources while depending on extractable sources (Handelsblatt, Tagesspiegel, taz, Die Welt, think tanks) for full-text analytical depth. This makes extractable German-language sources disproportionately valuable.

---

## BOOST ASSIGNMENTS

### Tier 1 — `$boost=3`

**Handelsblatt** | `handelsblatt.com` | Type: `business_financial` | Status: `EXISTING`
- **Structural role:** Germany's premier business daily and the most structurally important *extractable* German-language source. Obligatory reading for the Frankfurt financial community and the industrial policy establishment.
- **Domain coverage:** Economic & technological statecraft, Diplomatic alignment, Security & defense autonomy
- **Reasoning:** In a country where FAZ and SZ are both blocked by Anthropic's crawler, Handelsblatt becomes the highest-value extractable broadsheet-equivalent. Its coverage of sanctions implementation, export controls, defense procurement economics, Industriepolitik, and energy transition directly serves all five analytical domains. Hard paywall limits extraction depth, but Handelsblatt Today (English newsletter) provides daily summaries. German-language content earns the non-English domestic boost premium.
- **Extraction note:** Hard paywall for most content. Diffbot extraction likely partial. Handelsblatt Today English newsletter provides free daily summaries.

**Der Tagesspiegel** | `tagesspiegel.de` | Type: `regional` / `political_specialist` | Status: `EXISTING → PROMOTED TO TIER 1`
- **Structural role:** Berlin's quality daily with unmatched proximity to the Bundestag, Chancellery, and Berlin diplomatic community. The Tagesspiegel Background newsletters are read across the federal policy apparatus.
- **Domain coverage:** Domestic constraints, Diplomatic alignment, Institutional engagement, Security & defense autonomy
- **Reasoning:** With FAZ, SZ, and Spiegel all blocked, Tagesspiegel becomes the most important extractable source for domestic political signals. Its Berlin-insider sourcing fills the political-intelligence gap left by blocked papers of record. Metered paywall means most content is extractable. Not blocked by Anthropic's crawler — this alone justifies promotion from the curation prompt's implicit Tier 2. German-language, earning the non-English boost premium.
- **Extraction note:** Metered paywall. Tagesspiegel Background verticals require separate subscription but main site content is largely extractable.

**SWP (Stiftung Wissenschaft und Politik)** | `swp-berlin.org` | Type: `security_defense` / `political_specialist` | Status: `EXISTING → PROMOTED TO TIER 1`
- **Structural role:** Germany's most influential foreign and security policy research institute. Directly advises the Bundestag and federal government. SWP publications frequently pre-figure government policy shifts.
- **Domain coverage:** Security & defense autonomy, Diplomatic alignment, Institutional engagement
- **Reasoning:** Think tanks earn boost through depth, not speed — and SWP is the single most important analytical source for understanding German strategic thinking. All publications are freely available (no paywall, no crawler block). In a landscape where quality press extraction is severely constrained, SWP's open-access, high-depth publications become even more critical. When SWP publishes on a topic, it signals that Germany's policy establishment is processing a strategic question. German and English bilingual output.
- **Extraction note:** All publications freely available. Excellent extractability.

**Frankfurter Allgemeine Zeitung (FAZ)** | `faz.net` | Type: `paper_of_record` | Status: `EXISTING`
- **Structural role:** Germany's newspaper of record for the policy-making class. Sets the agenda for coalition-internal debates; read across ministries, the Bundestag, and the Frankfurt financial community.
- **Domain coverage:** Diplomatic alignment, Economic & technological statecraft, Domestic constraints
- **Reasoning:** Structural role outweighs extraction difficulty. FAZ is Germany's single most important newspaper — the pipeline must boost it even though Anthropic's crawler is blocked. Brave can still discover and rank FAZ headlines, and headline-level signals from Germany's agenda-setter are worth more than full-text from lesser sources. The pipeline gets partial signal (headlines, summaries, re-reporting by extractable outlets) rather than no signal.
- **Extraction note:** **BLOCKED by Anthropic crawler** (`faz.net` in blocked_domains.md). Metered paywall compounds extraction difficulty. Pipeline will rely on Brave discovery + headline-level signals. Critical stories will be re-reported by extractable outlets (Tagesspiegel, Handelsblatt).

---

### Tier 2 — `$boost=2`

**Süddeutsche Zeitung (SZ)** | `sueddeutsche.de` | Type: `paper_of_record` | Status: `EXISTING`
- **Structural role:** Germany's largest quality broadsheet by circulation. Essential centre-left counterweight to FAZ. Strong investigative tradition (Panama Papers partner).
- **Domain coverage:** Diplomatic alignment, Domestic constraints, Institutional engagement
- **Reasoning:** Indispensable paper of record, but drops to Tier 2 because it is **blocked by Anthropic's crawler** — the pipeline cannot extract full text. Brave can still surface SZ headlines for ranking. Tier 2 rather than Tier 1 because the extraction block means the pipeline gets headline-level signal only, and the centre-left political perspective is partially covered by extractable sources (taz, Tagesspiegel, IPG).
- **Extraction note:** **BLOCKED by Anthropic crawler** (`sueddeutsche.de` in blocked_domains.md). Metered paywall. Headline-level signals only.

**Der Spiegel** | `spiegel.de` | Type: `investigative` | Status: `EXISTING`
- **Structural role:** Germany's most prominent investigative newsweekly. Investigations force policy reversals and ministerial accountability. Spiegel International provides English-language access.
- **Domain coverage:** Domestic constraints, Diplomatic alignment, Security & defense autonomy
- **Reasoning:** Structural importance is Tier 1-level, but drops to Tier 2 because it is **blocked by Anthropic's crawler**. Spiegel International (English) may have different crawler treatment than spiegel.de — worth testing. Even at headline level, Spiegel stories are high-signal because they often break coalition-fracturing revelations. Brave will surface these prominently.
- **Extraction note:** **BLOCKED by Anthropic crawler** (`spiegel.de` in blocked_domains.md). Spiegel International (English select articles) may be accessible — test separately. Metered paywall.

**Die Welt / Welt am Sonntag** | `welt.de` | Type: `opposition_aligned` | Status: `EXISTING`
- **Structural role:** Captures the right flank of mainstream German discourse. Axel Springer ownership. Platform for conservative-nationalist perspectives. Essential for monitoring how right-wing pressures shape coalition positioning.
- **Domain coverage:** Domestic constraints, Diplomatic alignment, Security & defense autonomy
- **Reasoning:** Opposition-aligned sources earn Tier 2 minimum per boost principles. Die Welt fills the unique structural role of surfacing AfD-adjacent and conservative-hawkish pressures that constrain Merz's grand coalition from the right. Not blocked by Anthropic's crawler — making it one of the more extractable mainstream outlets. German-language, earning non-English boost premium. The Welt am Sonntag Musk/AfD editorial incident (Jan 2025) illustrates its role as a fault-line outlet.
- **Extraction note:** Metered paywall (WELTplus). Not blocked. Extractable.

**taz (Die Tageszeitung)** | `taz.de` | Type: `opposition_aligned` | Status: `EXISTING`
- **Structural role:** Left-green progressive voice. Cooperatively owned. Represents the Green/left critique constraining coalition action on defense spending, arms exports, and climate-security trade-offs.
- **Domain coverage:** Domestic constraints, Institutional engagement, Diplomatic alignment
- **Reasoning:** Opposition-aligned sources earn Tier 2 minimum. taz captures Green base dissatisfaction that can fracture governing coalitions — critical in a grand coalition where the Greens are in opposition but still shape discourse. Largely free (voluntary subscription) and not blocked by Anthropic's crawler — one of the most extractable quality sources in the German landscape. German-language, earning non-English boost premium. The extractability advantage alone would justify Tier 2.
- **Extraction note:** Largely free (voluntary subscription model). Not blocked. Excellent extractability.

**DGAP / Internationale Politik Quarterly (IPQ)** | `dgap.org` / `internationalepolitik.de` | Type: `security_defense` / `political_specialist` | Status: `EXISTING`
- **Structural role:** Germany's Council on Foreign Relations equivalent. IP/IPQ provides long-form foreign policy analysis authored by and for the foreign-policy establishment.
- **Domain coverage:** Diplomatic alignment, Institutional engagement, Security & defense autonomy
- **Reasoning:** Think tanks earn boost through depth. DGAP policy briefs track the intellectual framework behind German diplomatic positioning — essential for understanding *why* Berlin takes positions, not just *what* positions it takes. All publications freely available, not blocked. English-language IPQ provides accessible analytical depth. Complements SWP at Tier 1 with a slightly more transatlanticist and public-facing orientation.
- **Extraction note:** DGAP publications free online. IPQ (English) partially free. Not blocked. Good extractability.

**Bundesregierung.de / Auswärtiges Amt** | `bundesregierung.de` / `auswaertiges-amt.de` | Type: `legislative_official` | Status: `EXISTING` — **LAYER 2 MIGRATION**
- **Structural role:** Sole authoritative source for official government positions, coalition statements, BPK transcripts, and foreign-policy declarations. Not journalism — primary source material.
- **Domain coverage:** All five domains (official source)
- **Reasoning:** Primary fetch via Layer 2 direct polling. Goggle boost at Tier 2 as belt-and-suspenders fallback. Government press releases occasionally surface in Brave News Search. BPK (Bundespressekonferenz) transcripts are particularly valuable for detecting rhetorical shifts. Includes both `bundesregierung.de` and `auswaertiges-amt.de`.
- **Extraction note:** Fully free. English-language section available. Not blocked. Excellent extractability.

**Bundestag.de** | `bundestag.de` | Type: `legislative_official` | Status: `FROM de.yaml` — **LAYER 2 MIGRATION**
- **Structural role:** Parliamentary records, committee proceedings, Parlamentsvorbehalt documentation for military deployments. Listed in `de.yaml` as Tier 1 government source.
- **Domain coverage:** Domestic constraints, Institutional engagement, Security & defense autonomy
- **Reasoning:** The `de.yaml` config lists `bundestag.de` as a Tier 1 government source, but the curation prompt omitted it. Parliamentary records are essential for tracking Bundesrat votes on defense spending, Parlamentsvorbehalt debates, and committee hearings on foreign/security policy. Primary fetch via Layer 2 direct polling. Goggle Tier 2 as belt-and-suspenders.
- **Extraction note:** Fully free. Not blocked. Good extractability.

**IPG (Internationale Politik und Gesellschaft) — Friedrich-Ebert-Stiftung** | `ipg-journal.de` | Type: `political_specialist` | Status: `EXISTING`
- **Structural role:** Social-democratic intellectual framework for foreign and security policy. SPD-linked foundation. With SPD as coalition partner, IPG articles signal internal party thinking.
- **Domain coverage:** Diplomatic alignment, Institutional engagement, Domestic constraints
- **Reasoning:** Think tanks earn boost through depth. IPG provides the SPD's intellectual wing on alliance policy, EU reform, and development cooperation — essential for a grand coalition where SPD is the junior partner. Free, bilingual (German/English), not blocked. Fills the centre-left analytical slot that SZ would occupy if extractable.
- **Extraction note:** Fully free. English-language edition available. Not blocked. Excellent extractability.

---

### Tier 3 — `$boost=1`

**Die Zeit** | `zeit.de` | Type: `paper_of_record` | Status: `EXISTING → DEMOTED TO TIER 3`
- **Structural role:** Germany's leading weekly. Long-form political analyses and guest commentaries by senior politicians signal elite consensus shifts.
- **Domain coverage:** Diplomatic alignment, Domestic constraints, Institutional engagement
- **Reasoning:** Tier 3 despite high editorial quality because (1) **blocked by Anthropic's crawler**, (2) weekly cadence limits breaking-news utility, and (3) the elite-consensus-signaling function is partially covered by extractable think tanks (SWP, DGAP) and Tagesspiegel. Still worth boosting at Tier 3 because Brave may surface Zeit headlines for ranking and the pipeline benefits from seeing them even at headline level.
- **Extraction note:** **BLOCKED by Anthropic crawler** (`zeit.de` in blocked_domains.md). Metered paywall. Weekly cadence. Zeit Online updates daily but also blocked.

**WirtschaftsWoche** | `wiwo.de` | Type: `business_financial` | Status: `EXISTING`
- **Structural role:** Weekly business analytical depth on structural economic issues — supply chain de-risking, China exposure, tech sovereignty.
- **Domain coverage:** Economic & technological statecraft, Domestic constraints
- **Reasoning:** Complements Handelsblatt with analytical depth on macroeconomic issues, but same parent company (Holzbrinck) introduces editorial redundancy. Weekly cadence limits real-time utility. Not blocked by Anthropic's crawler — extractable, which is valuable. Tier 3 because Handelsblatt at Tier 1 covers the same economic statecraft domain with higher frequency and original reporting rate.
- **Extraction note:** Metered paywall. Not blocked. Extractable. Weekly cadence.

**Deutsche Welle (DW)** | `dw.com` | Type: `government_aligned` | Status: `EXISTING → DEMOTED TO TIER 3`
- **Structural role:** Germany's international broadcaster. Provides the clearest window into how Germany presents its foreign-policy positions internationally. State-funded but editorially independent by statute.
- **Domain coverage:** Diplomatic alignment, Institutional engagement, Security & defense autonomy
- **Reasoning:** **Blocked by Anthropic's crawler** despite being a free, open-access broadcaster — a significant extraction loss. DW's English-language output would otherwise be highly valuable for the pipeline. Tier 3 rather than Tier 2 because (1) blocked, (2) the government-messaging function is covered by Layer 2 direct polling of bundesregierung.de, and (3) its framing may reflect government messaging priorities (state-funded flag from curation prompt). Still worth Tier 3 boost because Brave may surface DW results and headline-level government framing signals are useful.
- **Extraction note:** **BLOCKED by Anthropic crawler** (`dw.com` in blocked_domains.md). Fully free content. English and German.

**Defense News** | `defensenews.com` | Type: `security_defense` | Status: `NEW`
- **Structural role:** The curation prompt's Coverage Gap Assessment explicitly identified the lack of a domestic defense-industry specialist source. Defense News provides the closest equivalent for Bundeswehr procurement, European defense-industrial developments, and NATO capability stories.
- **Domain coverage:** Security & defense autonomy
- **Reasoning:** Added to fill the structural gap identified in the curation prompt. Germany lacks a domestic Jane's equivalent, and defense procurement execution is listed as a blind spot in `de.yaml`. Defense News covers Bundeswehr modernization, FCAS/MGCS procurement, and European defense integration with dedicated correspondent coverage. English-language, which limits domestic-signal capture but provides the analytical depth missing elsewhere. Tier 3 because it's not a German domestic source and covers a single domain.
- **Extraction note:** Metered paywall. Not blocked. English-language.

**Konrad-Adenauer-Stiftung (KAS)** | `kas.de` | Type: `political_specialist` / `think_tank` | Status: `NEW`
- **Structural role:** CDU-affiliated political foundation. With CDU/CSU leading the governing coalition under Merz, KAS publications signal internal party thinking on foreign, security, and European policy.
- **Domain coverage:** Diplomatic alignment, Institutional engagement, Security & defense autonomy
- **Reasoning:** Added for structural completeness — the audit includes IPG (SPD-linked FES foundation) at Tier 2, so the governing party's foundation should also be represented. KAS foreign-policy publications often preview CDU strategic thinking before it becomes coalition policy. Tier 3 rather than Tier 2 because think-tank publications are slower and less frequent than media sources, and the CDU's governing positions are already reflected through Handelsblatt and Tagesspiegel coverage.
- **Extraction note:** Publications freely available. Not blocked. German and English. Good extractability.

---

### Neutral — no Goggle rule

**Frankfurter Rundschau** | `fr.de` | Type: `opposition_aligned` | Status: `EXISTING → DEMOTED TO NEUTRAL`
- **Why neutral:** Provides SPD-left/trade-union perspective, but (1) **blocked by Anthropic's crawler** (`fr.de` in blocked_domains.md), making extraction unreliable, and (2) the social-democratic analytical niche is covered by extractable sources (IPG at Tier 2, taz at Tier 2 for left-progressive critique). Under curation-exclusion-to-neutral principle, no reason to actively discard — may surface organically in Brave for specific queries and provide headline-level signals.

**n-tv.de** | `n-tv.de` | Type: `paper_of_record` (digital-first news channel) | Status: `EXISTING → DEMOTED TO NEUTRAL`
- **Why neutral:** High-frequency breaking-news source, but (1) **blocked by Anthropic's crawler** (`n-tv.de` in blocked_domains.md), and (2) its structural role as a fast-breaking news aggregator is less critical for a pipeline focused on analytical depth. Wire services (Reuters, AP) fill the speed-of-signal role. n-tv may surface organically in Brave — no need to boost, no need to discard.

**Politico Europe** | `politico.eu` | Type: `political_specialist` | Status: `EXISTING → DEMOTED TO NEUTRAL`
- **Why neutral:** Berlin Playbook is read by Germany's EU-engaged policy class and uniquely links Berlin domestic politics to Brussels institutional dynamics. However, **blocked by Anthropic's crawler** (`politico.eu` in blocked_domains.md). The EU-institutional lens is partially covered by DGAP/IPQ (Tier 2) and SWP (Tier 1). The Berlin Playbook newsletter is distributed via email rather than web — the pipeline's web-search layer wouldn't capture it regardless. Leave neutral for organic Brave discovery.

**Bild** | `bild.de` | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Curation exclusion was correct under the hard-filter model — tabloid, sensationalist, unreliable sourcing on policy matters. Under the Goggle model, no reason to actively discard. Bild has genuine political influence on public opinion (highest circulation in Germany) and its occasional policy scoops do move the news cycle. If Brave surfaces a Bild story, it's likely because other outlets haven't yet covered the topic. Organic ranking handles this correctly.

**Focus Online** | `focus.de` | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Curation exclusion noted the pivot to clickbait and aggregated content. Under Goggle model, no reason to actively discard — if it surfaces organically, the pipeline's interpretive layer can assess quality. Low risk of displacing boosted sources.

---

### Discard — `$discard`

**RT Deutsch** | `de.rt.com` | Status: `CONFIRMED DISCARD`
- **Discard reasoning:** Russian state propaganda outlet operating in German. No original journalistic value. Would actively inject state-directed disinformation into the pipeline, displacing legitimate sources. Meets the "actively harmful" threshold for $discard.

**Junge Freiheit** | `jungefreiheit.de` | Status: `NEW DISCARD`
- **Discard reasoning:** Right-wing weekly with AfD-adjacent editorial line. The curation prompt correctly excluded it — its content is not original enough to warrant inclusion, and the far-right discourse it amplifies is trackable through Die Welt's right-flank coverage (Tier 2). Including it would waste result slots and introduce a disproportionate far-right signal that doesn't reflect Germany's mainstream policy discourse.

**Compact Magazin** | `compact-online.de` | Status: `NEW DISCARD`
- **Discard reasoning:** Far-right magazine banned by the German interior ministry in July 2024 (ban partially overturned by courts, but the publication's editorial direction is explicitly anti-constitutional-order). Meets the "actively harmful" threshold. Would inject extremist framing and displace legitimate sources.

**Sputnik Deutschland** | `snanews.de` / `de.sputniknews.com` | Status: `NEW DISCARD`
- **Discard reasoning:** Russian state media operating in German. Same reasoning as RT Deutsch — state-directed disinformation with no original journalistic value. EU sanctions have restricted its distribution but web content may still surface in Brave.

---

## STRUCTURAL COVERAGE CHECK

| Structural Role | Source(s) | Tier | Notes |
|---|---|---|---|
| Government leak channel / preferred signaling | Bundesregierung.de, DW | T2, T3 | Official channels via Layer 2 direct polling. DW reflects international messaging priorities (but blocked). Grand coalition signaling split: CDU priorities surface through FAZ/Handelsblatt, SPD through IPG/taz |
| Opposition voice (right) | Die Welt | T2 | Conservative-nationalist critique of coalition from the right. AfD-adjacent commentary provides far-right pressure signals |
| Opposition voice (left) | taz, Frankfurter Rundschau | T2, Neutral | taz captures Green/left-progressive critique. FR is blocked but covers SPD-left/trade-union perspective organically |
| Defence/security specialist | SWP, Defense News | T1, T3 | No domestic defence press equivalent to Jane's. SWP provides strategic analytical depth. Defense News fills procurement/capability gap. Spiegel (T2, blocked) breaks defence scandals |
| Policy-elite discourse | FAZ, SWP, DGAP, Tagesspiegel | T1, T1, T2, T1 | FAZ is what decision-makers read (but blocked). SWP/DGAP provide the analytical framework. Tagesspiegel's Berlin proximity gives insider political intelligence |
| Domestic-language depth | All German-language sources | T1–T3 | Germany's policy discourse operates primarily in German. English sources (DW English, Defense News, IPQ English, KAS English) are supplements. Non-English boost premium applied |
| Official government source | bundesregierung.de, auswaertiges-amt.de, bundestag.de | T2 | **LAYER 2 MIGRATION** — primary fetch via direct polling. Goggle boost as fallback |
| Analytical/think tank depth | SWP, DGAP/IPQ, IPG, KAS | T1, T2, T2, T3 | SWP for security/strategy; DGAP for transatlantic/EU; IPG for social-democratic framework; KAS for CDU governing-party perspective |
| Business/economic statecraft | Handelsblatt, WirtschaftsWoche | T1, T3 | Handelsblatt is the primary economic source. WiWo supplements with weekly analytical depth. Same parent company introduces minor redundancy |
| Wire service (international) | Reuters, AP News, France24 | Neutral | Listed in de.yaml wire section. Not boosted — wire copy available organically. Reuters is blocked by Anthropic crawler |

**Gaps identified:**
1. **Defence procurement execution** remains a structural blind spot — confirmed by both the curation prompt and de.yaml's blind_spots. No German source systematically tracks Bundeswehr readiness, FCAS/MGCS timelines, or Sondervermögen spending execution. Mitigated by SWP (Tier 1), Defense News (Tier 3), and Layer 2 polling of BMVg press releases, but this is a known weakness.
2. **AfD internal dynamics in eastern states** — confirmed blind spot from de.yaml. National media covers AfD primarily through the lens of Berlin politics. State-level dynamics in Thuringia, Saxony, and Brandenburg (where AfD holds significant power) are underrepresented. Regional outlets (MDR, Freie Presse) could fill this gap but were not added to avoid over-expanding the Goggle.
3. **Bundesrat/Länder-level dynamics** — the curation prompt's Coverage Gap Assessment flagged this. When Bundesrat votes become critical for defense spending or EU treaty ratification, the pipeline may need supplementary regional sources (e.g., WDR/WAZ for NRW industrial interests).

---

## REDUNDANCY RESOLUTION

**Broadsheet cluster: FAZ + SZ + Die Zeit + Tagesspiegel + Die Welt + taz + n-tv + FR**
Eight sources from the quality press is substantial, but the blocked-domains problem resolves most redundancy naturally. FAZ (Tier 1, blocked but indispensable), Tagesspiegel (Tier 1, extractable Berlin-insider), Die Welt (Tier 2, extractable right-flank), taz (Tier 2, extractable left-green). SZ drops to Tier 2 (blocked), Die Zeit to Tier 3 (blocked + weekly), n-tv to Neutral (blocked + aggregator), FR to Neutral (blocked + redundant with IPG/taz). The extractable sources differentiate by editorial orientation: Tagesspiegel (centrist-insider), Welt (conservative-hawkish), taz (left-green).

**Business press cluster: Handelsblatt + WirtschaftsWoche**
Same parent company (Holzbrinck). Handelsblatt leads (Tier 1) as daily with broader coverage and English newsletter. WiWo drops to Tier 3 — weekly cadence, analytical supplement, editorial overlap. Redundancy is real but manageable because both are extractable.

**Think-tank cluster: SWP + DGAP/IPQ + IPG + KAS**
Four think tanks is generous but each maps to a distinct structural role. SWP (Tier 1, government advisory, security-focused), DGAP (Tier 2, transatlanticist, foreign-policy establishment), IPG (Tier 2, SPD coalition-partner signaling), KAS (Tier 3, CDU governing-party signaling). The party-foundation pair (IPG + KAS) directly mirrors the grand coalition structure. No redundancy — each occupies a distinct intellectual lane.

**Government sources: bundesregierung.de + auswaertiges-amt.de + bundestag.de**
All three are Layer 2 migration targets. No redundancy — federal government, foreign ministry, and parliament serve different constitutional functions. Combined Tier 2 boost as belt-and-suspenders.

---

## QUERY CONFIGURATION

```
country: DE
search_lang: de
freshness: pw
```

**Multi-language notes:** Germany's policy discourse operates overwhelmingly in German. English-language sources (DW, Spiegel International, IPQ, KAS English, Handelsblatt Today, Defense News) are supplements. Queries should run primarily in German; a secondary English query cycle for defense/security and EU-institutional topics would capture think-tank English output and international wire coverage. The pipeline's existing `languages.metadata: en` configuration handles this correctly.

**Localized query vocabulary validation:**

The curation prompt's vocabulary is comprehensive and well-structured. Notes:

- **Domain 1 (Diplomatic Alignment):** All terms valid. `Zeitenwende` remains in active use under Merz as the framing for continued defense acceleration. Add `"Merz Außenpolitik"` and `"Wadephul Diplomatie"` as leader-specific patterns. Consider adding `"China-Strategie"` — Germany's China strategy document (2023) continues to frame bilateral recalibration. Add `"Scholz"` only in historical-context queries — Merz has been chancellor since May 2025.
- **Domain 2 (Security & Defense):** Strong list. `Sondervermögen` is essential — the €100B defense fund's spending execution is the central defense-policy story. Add `"Pistorius Bundeswehr"` (defense minister). Add `"FCAS"` (Future Combat Air System) and `"MGCS"` (Main Ground Combat System) — the two flagship Franco-German procurement programs. Add `"Zwei-Prozent-Ziel"` (2% GDP target). `"Europäische Verteidigungsunion"` is correct but consider also `"EU-Verteidigungsfonds"` (EU Defence Fund).
- **Domain 3 (Economic & Technological Statecraft):** Excellent list. `De-Risking` used as loanword is correct — confirmed in German press usage. Add `"Halbleiter"` (semiconductors) — critical for TSMC Dresden fab and European Chips Act. Add `"Energiewende"` (energy transition) — still central to economic statecraft. Consider `"China-Abhängigkeit"` (China dependency) as a high-signal compound. `"Standortwettbewerb"` is perfect but very high-frequency — pair with `"Standort Deutschland"` for more targeted results.
- **Domain 4 (Institutional Engagement):** Valid. Add `"EU-Erweiterung Ukraine"` (EU enlargement Ukraine) — the dominant institutional engagement story. `"G7-Präsidentschaft"` is valid but Germany's G7 presidency was 2022 — update to current G7/G20 context terms. Add `"Vereinte Nationen Sicherheitsrat Reform"` (UN Security Council reform — Germany's long-standing bid).
- **Domain 5 (Domestic Constraints):** Strong. Add `"Merz Koalitionsvertrag"` (Merz coalition agreement — the foundational governance document). Add `"AfD Umfrage"` (AfD polls) — critical for tracking far-right pressure. `"Schuldenbremse"` is essential — the debt brake remains the central fiscal constraint. Add `"Haushaltsdebatte"` (budget debate). Consider adding `"Verfassungsschutz AfD"` (domestic intelligence monitoring of AfD) for tracking the state's response to far-right pressures.

**Stale/problematic terms:** `"G7-Präsidentschaft"` is dated — Germany held the G7 presidency in 2022. Replace with generic `"G7 Deutschland"` or remove. All other terms are current.

**Suggested topic query patterns:**

1. `Merz Zeitenwende Verteidigungspolitik Sondervermögen` — Defence spending acceleration under Merz
2. `De-Risking China Lieferketten Industriepolitik` — China de-risking and supply chain restructuring
3. `Koalitionskrise CDU SPD Schuldenbremse` — Grand coalition fiscal tensions
4. `FCAS MGCS Rüstungspolitik Bundeswehr Modernisierung` — Defence procurement programs
5. `EU-Reform Erweiterung Ukraine Deutschland` — Germany's EU institutional positioning

---

## GOGGLE FILE

```goggle
! name: MPM Germany
! description: MPM pipeline source prioritization for Germany — boosts high-signal sources, discards noise. Heavy crawler-block mitigation: extractable sources promoted.
! public: false
! author: MPM Pipeline

! --- Tier 1: Essential (boost=3) ---
$boost=3,site=handelsblatt.com
$boost=3,site=tagesspiegel.de
$boost=3,site=swp-berlin.org
$boost=3,site=faz.net

! --- Tier 2: Important (boost=2) ---
$boost=2,site=sueddeutsche.de
$boost=2,site=spiegel.de
$boost=2,site=welt.de
$boost=2,site=taz.de
$boost=2,site=dgap.org
$boost=2,site=internationalepolitik.de
$boost=2,site=bundesregierung.de
$boost=2,site=auswaertiges-amt.de
$boost=2,site=bundestag.de
$boost=2,site=ipg-journal.de

! --- Tier 3: Supplementary (boost=1) ---
$boost=1,site=zeit.de
$boost=1,site=wiwo.de
$boost=1,site=dw.com
$boost=1,site=defensenews.com
$boost=1,site=kas.de

! --- Discard: Noise ---
$discard,site=de.rt.com
$discard,site=jungefreiheit.de
$discard,site=compact-online.de
$discard,site=snanews.de
$discard,site=de.sputniknews.com
```

---

## INTERPRETIVE CONTEXT FOR DOSSIER

### Tier 1 Sources

> Articles from **Handelsblatt** about economic and industrial policy should be interpreted as reflecting the perspective of Germany's business and financial establishment — its ordoliberal editorial orientation and Frankfurt-centric readership mean it frames economic policy through a competitiveness and market-confidence lens. Negative coverage of government industrial intervention reflects private-sector concerns, not necessarily policy failure. Its defence-industry and sanctions coverage has improved significantly since Zeitenwende.

> Articles from **Der Tagesspiegel** about coalition politics and federal government decisions should be interpreted as Berlin-insider political intelligence — its physical and editorial proximity to the Bundestag, Chancellery, and Berlin diplomatic community gives it sourcing depth that no other extractable German outlet matches. Its liberal-centrist orientation means it generally frames coalition dynamics through a pragmatic governance lens rather than ideological critique.

> Articles from **SWP** about foreign and security policy should be interpreted as the analytical framework Germany's policy establishment uses to process strategic questions — SWP directly advises the Bundestag and federal government, and its publications often pre-figure policy shifts by months. When SWP publishes on a topic, it signals that Germany's strategic class is actively debating that question. Its non-partisan stance means it frames issues as strategic trade-offs rather than political positions.

> Articles from **FAZ** about any policy domain should be interpreted as Germany's most influential newspaper of record setting the agenda for the policy-making class — its conservative-liberal, pro-market, Atlanticist editorial line shapes how CDU/CSU, the financial community, and ministerial bureaucracies frame policy debates. **Note: blocked by Anthropic crawler — pipeline receives headline-level signals only. Treat FAZ headlines as high-confidence agenda indicators even without full text.**

### Tier 2 Sources

> Articles from **Süddeutsche Zeitung** about domestic politics and investigative matters should be interpreted as centre-left quality journalism with Germany's strongest investigative tradition (Panama Papers partner) — its editorial line provides the essential counterweight to FAZ's conservative framing. **Note: blocked by Anthropic crawler — headline-level signals only.**

> Articles from **Der Spiegel** about government misconduct, coalition tensions, or defence policy should be interpreted as Germany's premier adversarial investigative journalism — Spiegel investigations have forced ministerial resignations and policy reversals across all governments. Its left-liberal orientation means it frames power critically regardless of party. **Note: blocked by Anthropic crawler — headline-level signals only, but Spiegel headlines are high-signal because they often indicate imminent political crises.**

> Articles from **Die Welt** about defence, migration, or transatlantic relations should be interpreted as filtered through Axel Springer's conservative-hawkish editorial orientation — Die Welt platforms the most assertive positions on defense spending increases, NATO commitment, and migration restriction within mainstream German discourse. It provides the essential signal for how right-of-centre pressure constrains or enables Merz's coalition from the conservative flank. The AfD-adjacent commentary it occasionally platforms should be read as indicator of far-right mainstreaming, not Welt's own editorial position.

> Articles from **taz** about defense spending, arms exports, or climate-security trade-offs should be interpreted as the Green/left-progressive critique that defines the outer boundary of acceptable discourse on Germany's left — its cooperative ownership structure makes it genuinely editorially independent, and its framing shows where Green base dissatisfaction could crystallize into political constraint on coalition action.

> Articles from **DGAP/IPQ** about transatlantic relations, EU strategic autonomy, or multilateral engagement should be interpreted as reflecting the foreign-policy establishment's consensus framework — DGAP is Germany's equivalent of the Council on Foreign Relations, and its publications represent the analytical mainstream of German strategic thinking, with a moderately transatlanticist orientation.

> Articles from **IPG (Friedrich-Ebert-Stiftung)** about foreign policy, European integration, or development cooperation should be interpreted as signaling SPD intellectual positions — as the junior coalition partner's affiliated foundation, IPG publications often preview social-democratic positions on alliance policy and EU reform before they appear in coalition negotiations. The multilateralist, social-solidarity framing is genuine editorial orientation, not propaganda.

> Articles from **bundesregierung.de**, **auswaertiges-amt.de**, and **bundestag.de** should be interpreted as official government and parliamentary communications — not journalism but primary source material. Press releases and BPK transcripts represent the government's chosen public position, which may differ from actual policy implementation. Rhetorical shifts in BPK language are high-signal indicators of policy evolution.

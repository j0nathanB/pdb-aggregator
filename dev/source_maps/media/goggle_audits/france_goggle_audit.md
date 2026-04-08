# AUDIT SUMMARY: FRANCE

**Sources assessed:** 17 recommended + 5 excluded + 5 newly identified = 27 total
**Tier 1 (boost=3):** 4 sources
**Tier 2 (boost=2):** 8 sources
**Tier 3 (boost=1):** 5 sources
**Neutral (no rule):** 7 sources
**Discard:** 3 sources
**Overall assessment:** France presents the most severe crawler-blockage problem of any country audited so far: 12 of 17 recommended sources block Anthropic's crawler, including both papers of record (Le Monde, Le Figaro), the leading business daily (Les Echos), all investigative outlets, and both specialist newsletters (Intelligence Online, La Lettre A). The Goggle can still boost these domains — Brave will surface and rank them — but the pipeline cannot extract full text via WebFetch. This makes France heavily dependent on the small number of unblocked sources (France 24, Contexte, Revue Défense Nationale, IFRI, Public Sénat/LCP) plus government Layer 2 polling. Key changes: (1) promoted government official sources for Layer 2 migration; (2) added Africa Intelligence and Fondation pour la Recherche Stratégique (FRS) to fill structural gaps; (3) differentiated the blocked broadsheet cluster by tier to preserve ranking signal even without extraction; (4) elevated France 24 to Tier 1 as the only extractable high-volume French news source.

---

## BOOST ASSIGNMENTS

### Tier 1 — `$boost=3`

**France 24** | `france24.com` | Type: `government_aligned` | Status: `EXISTING`
- **Structural role:** France's only freely accessible, high-volume news source covering all five analytical domains in both French and English. State-funded international broadcaster operated by France Médias Monde.
- **Domain coverage:** Diplomatic alignment, Security & defense autonomy, Institutional engagement, Economic & technological statecraft, Domestic constraints
- **Reasoning:** Under normal circumstances a government-aligned broadcaster would not earn Tier 1. But France 24 is structurally essential for two reasons: (1) it is the only major French news source NOT blocked by Anthropic's crawler, meaning it is the pipeline's primary extractable domestic signal; (2) its bilingual output (French and English) makes it the most pipeline-friendly source in the entire map. RSS feeds are comprehensive and open. The dossier's interpretive context tells the LLM to read France 24 as reflecting French state perspective, not independent journalism.
- **Extraction note:** Fully free, no paywall, no anti-scraping barriers. Best extraction reliability of any source on this list.
- **FLAG:** Government-funded — interpretive context must explicitly note this.

**Le Monde** | `lemonde.fr` | Type: `paper_of_record` | Status: `EXISTING`
- **Structural role:** France's newspaper of record. The agenda-setter for French foreign policy discourse. Élysée and Quai d'Orsay officials use Le Monde for signaling.
- **Domain coverage:** Diplomatic alignment, Institutional engagement, Domestic constraints
- **Reasoning:** Indispensable as the primary agenda-setter regardless of extraction constraints. Brave indexes and ranks Le Monde headlines even behind the paywall, which provides the pipeline with headline-level signal detection. The Goggle must surface Le Monde first — even a headline and lede from Brave's snippet is more valuable than full text from a lower-signal source.
- **Extraction note:** **BLOCKED by Anthropic crawler.** Hard paywall + `robots.txt` denial. Pipeline will get headline + snippet from Brave only. No full-text extraction possible.

**Le Figaro** | `lefigaro.fr` | Type: `paper_of_record` | Status: `EXISTING`
- **Structural role:** Right-of-center paper of record. Dassault Group ownership provides deep defense sourcing. Represents the Gaullist/sovereigntist policy establishment.
- **Domain coverage:** Diplomatic alignment, Security & defense autonomy, Domestic constraints
- **Reasoning:** Essential counterweight to Le Monde's center-left framing. Defense coverage is uniquely deep due to Dassault ownership (which is also a bias vector — the dossier notes this). Together with Le Monde, forms the indispensable broadsheet pair for headline detection.
- **Extraction note:** **BLOCKED by Anthropic crawler.** Metered paywall + `robots.txt` denial. Headline + snippet only via Brave.

**Les Echos** | `lesechos.fr` | Type: `business_financial` | Status: `EXISTING`
- **Structural role:** France's leading business daily. Sole primary source for economic statecraft — trade policy, industrial strategy, EU single market, tech sovereignty, sanctions impact.
- **Domain coverage:** Economic & technological statecraft, Institutional engagement
- **Reasoning:** No other French source covers Bercy decisions, EU trade negotiations, and industrial policy at this depth. Comparable to the Financial Times for France. Tier 1 for economic statecraft despite extraction limitations because no substitute exists.
- **Extraction note:** **BLOCKED by Anthropic crawler.** Hard paywall + `robots.txt` denial. Headline + snippet only.

---

### Tier 2 — `$boost=2`

**Mediapart** | `mediapart.fr` | Type: `investigative` | Status: `EXISTING`
- **Structural role:** France's premier investigative outlet. Subscriber-funded nonprofit with 245,000+ subscribers. Breaks stories on political corruption, intelligence operations, arms deals, and government misconduct.
- **Domain coverage:** Domestic constraints, Diplomatic alignment
- **Reasoning:** Irreplaceable for investigations that reshape domestic constraints on foreign policy. Its independence (no advertising, no billionaire owner) is unique in the French media landscape. Tier 2 rather than Tier 1 because (a) blocked by Anthropic's crawler — only headline-level detection possible, and (b) investigative cadence is slower than daily broadsheets.
- **Extraction note:** **BLOCKED by Anthropic crawler.** Hard paywall + `robots.txt` denial.

**Libération** | `liberation.fr` | Type: `opposition_aligned` | Status: `EXISTING`
- **Structural role:** Left-progressive national daily. Provides the domestic left-wing lens on foreign policy — critical on arms exports, migration, Françafrique legacy.
- **Domain coverage:** Domestic constraints, Diplomatic alignment
- **Reasoning:** Essential for understanding left-progressive constraints on external action. Non-profit endowment structure since 2020 supports editorial independence. Tier 2 because its domain coverage is narrower than Le Monde/Le Figaro and it breaks fewer foreign policy stories. Provides the opposition voice from the left that Le Figaro provides from the right.
- **Extraction note:** **BLOCKED by Anthropic crawler.** Metered paywall + `robots.txt` denial.

**IFRI / Politique étrangère** | `ifri.org` | Type: `political_specialist` / `think_tank` | Status: `EXISTING`
- **Structural role:** France's leading foreign policy think tank. Politique étrangère is the oldest French IR journal (founded 1936). Closely connected to Quai d'Orsay and defense establishment.
- **Domain coverage:** Diplomatic alignment, Security & defense autonomy, Institutional engagement
- **Reasoning:** Think tanks earn boost through depth, not speed. IFRI publications preview or frame policy changes weeks before official announcements. Bilingual (French/English) output is pipeline-friendly. Policy briefs are freely accessible — one of the few high-value French sources with reliable extraction. Tier 2 for analytical depth and extraction reliability.
- **Extraction note:** Freely accessible policy briefs at ifri.org. No anti-scraping issues. Some Politique étrangère articles paywalled via Cairn.info.

**Intelligence Online** | `intelligenceonline.com` | Type: `security_defense` | Status: `EXISTING`
- **Structural role:** Unique niche — systematic coverage of intelligence service operations, defense contracts, and covert diplomatic activity. Bilingual (French/English). Published by Indigo Publications.
- **Domain coverage:** Security & defense autonomy, Diplomatic alignment
- **Reasoning:** No other French-language outlet provides this type of coverage. Essential for detecting security posture shifts invisible in mainstream press. Tier 2 despite extraction block because its niche is irreplaceable — even headline-level detection of an Intelligence Online story about DGSE operations or defense contract maneuvering is high-signal.
- **Extraction note:** **BLOCKED by Anthropic crawler.** Hard paywall + `robots.txt` denial. Premium subscription pricing.

**Élysée / Gouvernement portals** | `elysee.fr` / `gouvernement.fr` | Type: `legislative_official` | Status: `NEW` — **LAYER 2 MIGRATION**
- **Structural role:** Official government communication channels. Élysée for presidential communications; gouvernement.fr for prime ministerial and cross-ministerial policy.
- **Domain coverage:** All five domains (official source)
- **Reasoning:** Primary fetch via Layer 2 direct polling. Goggle boost at Tier 2 as belt-and-suspenders fallback. Government press releases occasionally surface in Brave News Search. Already listed in `fr.yaml` as government sources at tier 1 for direct polling — Goggle Tier 2 is the complementary search-layer boost.

**Ministère de l'Europe et des Affaires étrangères** | `diplomatie.gouv.fr` | Type: `legislative_official` | Status: `NEW` — **LAYER 2 MIGRATION**
- **Structural role:** Quai d'Orsay official communications — treaty announcements, diplomatic statements, travel advisories, sanctions implementation.
- **Domain coverage:** Diplomatic alignment, Institutional engagement
- **Reasoning:** Direct government source for diplomatic posture. Layer 2 primary fetch with Goggle Tier 2 fallback. Communiqués surface in Brave and provide authoritative confirmation of diplomatic moves reported by media.

**Public Sénat / LCP** | `publicsenat.fr` / `lcp.fr` | Type: `legislative_official` | Status: `EXISTING`
- **Structural role:** Parliamentary television channels covering Senate and National Assembly proceedings — committee hearings, debates, investigations.
- **Domain coverage:** Domestic constraints, Institutional engagement
- **Reasoning:** Direct access to parliamentary discourse on foreign affairs, defense budgets, treaty ratification. Free, extractable, and unblocked — a rare combination in the French source map. Committee hearings on arms exports and military operations provide primary-source signal. Tier 2 for structural importance as the only extractable source of parliamentary proceedings.
- **Extraction note:** Free access. No paywall or anti-scraping barriers.

**Fondation pour la Recherche Stratégique (FRS)** | `frstrategie.org` | Type: `security_defense` / `think_tank` | Status: `NEW`
- **Structural role:** France's principal defense and security think tank. Covers nuclear deterrence, arms control, defense industrial base, and military strategy. Authors include former defense officials and military officers.
- **Domain coverage:** Security & defense autonomy, Diplomatic alignment
- **Reasoning:** Fills a structural gap alongside IFRI — while IFRI covers broad foreign policy, FRS is focused specifically on defense and security analysis. Publications are freely accessible. Provides the doctrinal and strategic depth that daily press cannot. Tier 2 for analytical depth in the defense domain.
- **Extraction note:** Freely accessible publications at frstrategie.org. No known anti-scraping measures.

---

### Tier 3 — `$boost=1`

**Revue Défense Nationale** | `defnat.com` | Type: `security_defense` | Status: `EXISTING`
- **Structural role:** Institutional voice of the French defense community. Monthly journal founded 1939, housed at the École militaire. Authors include serving officers, defense officials, and academics.
- **Domain coverage:** Security & defense autonomy, Diplomatic alignment
- **Reasoning:** Provides early signals of doctrinal shifts and strategic reassessments from inside the defense establishment. Tier 3 rather than Tier 2 because of monthly publication cadence — the pipeline can't depend on it for timely signal. But when it publishes, the content is uniquely authoritative. Some content freely accessible.
- **Extraction note:** Some content freely accessible on defnat.com. Full archive requires subscription. No known anti-scraping measures.

**Contexte** | `contexte.com` | Type: `political_specialist` | Status: `EXISTING`
- **Structural role:** Subscription-only policy intelligence service covering French and EU public policy across verticals (energy, defense, digital, agriculture). Comparable to Politico for the French policy world.
- **Domain coverage:** Institutional engagement, Economic & technological statecraft, Security & defense autonomy
- **Reasoning:** Unmatched granularity on legislative and regulatory processes. Tier 3 rather than Tier 2 because (a) hard institutional paywall with no free tier makes extraction uncertain, and (b) niche audience means content rarely surfaces in Brave search results. But when it does surface, the signal is high-value.
- **Extraction note:** Hard paywall, institutional pricing. No free access tier. Limited public RSS. Extraction reliability unknown — likely low.

**L'Opinion** | `lopinion.fr` | Type: `political_specialist` | Status: `EXISTING`
- **Structural role:** Liberal, pro-business, pro-European daily. Voice of French economic liberalism and Macronist-adjacent centrism.
- **Domain coverage:** Diplomatic alignment, Economic & technological statecraft, Domestic constraints
- **Reasoning:** Well-connected to the centrist policy establishment but overlaps significantly with Le Figaro (business perspective) and Les Echos (economic coverage). Tier 3 because it adds a centrist-liberal editorial lens but doesn't break stories the top-tier broadsheets miss. Blocked by crawler — headline detection only.
- **Extraction note:** **BLOCKED by Anthropic crawler.** Metered paywall + `robots.txt` denial.

**Africa Intelligence** | `africaintelligence.com` | Type: `security_defense` / `investigative` | Status: `NEW`
- **Structural role:** Indigo Publications outlet covering Francophone Africa — defense, diplomacy, and political dynamics across the Sahel, West Africa, and Central Africa. Fills the Françafrique/overseas territory gap identified in the whitelist's coverage gap assessment.
- **Domain coverage:** Security & defense autonomy, Diplomatic alignment
- **Reasoning:** The whitelist explicitly identified "Francophone Africa and overseas territories" as the primary coverage gap. Africa Intelligence is the natural fill — same publisher as Intelligence Online, same investigative methodology, focused on the geographic region where French strategic posture is most contested (Sahel withdrawal, naval base network, influence competition with Russia/Wagner). Tier 3 because it covers a specific geographic subset, but within that subset it's irreplaceable.
- **Extraction note:** Hard paywall, premium subscription. Extraction reliability unknown — likely low. Bilingual (French/English).

**Le Monde diplomatique** | `monde-diplomatique.fr` | Type: `political_specialist` | Status: `EXISTING`
- **Structural role:** Leading French-language venue for structuralist and critical analysis of international relations. Influential among academic and left-intellectual policy community.
- **Domain coverage:** Diplomatic alignment, Institutional engagement
- **Reasoning:** Provides the counter-hegemonic analytical frame that surfaces in parliamentary debates via LFI and parts of the PS. Monthly publication cadence limits timeliness. Tier 3 because analytical depth is high but publication frequency is low and domain coverage is narrow. English edition available.
- **Extraction note:** **BLOCKED by Anthropic crawler.** Monthly publication. Metered paywall + `robots.txt` denial.

---

### Neutral — no Goggle rule

**La Croix** | `la-croix.com` | Type: `paper_of_record` | Status: `EXISTING → DEMOTED TO NEUTRAL`
- **Why neutral:** Humanist-Catholic editorial lens provides a distinct perspective on migration, development, and multilateralism. However, **blocked by Anthropic's crawler** and its editorial niche overlaps with France 24's coverage of the same topics (both emphasize global South and multilateral perspectives). Under the Goggle model, it can still appear organically — no need to boost, but no need to discard either. If France 24 becomes unavailable, La Croix should be re-evaluated.

**La Lettre A** | `lalettre.fr` | Type: `political_specialist` | Status: `EXISTING → DEMOTED TO NEUTRAL`
- **Why neutral:** Valuable insider newsletter on political and business maneuvering, but **blocked by Anthropic's crawler** and its niche (elite circulation, ministerial power dynamics) overlaps partially with Intelligence Online at Tier 2. Newsletter format with hard paywall means it rarely surfaces in Brave search results. No reason to discard — organic ranking is appropriate.

**Le Parisien** | `leparisien.fr` | Type: `regional` | Status: `EXISTING → DEMOTED TO NEUTRAL`
- **Why neutral:** Useful as a public opinion barometer but **blocked by Anthropic's crawler**. Its mainstream opinion-tracking function is partially served by France 24 (which covers domestic politics). Under LVMH ownership (shared with Les Echos), its editorial distinctiveness is limited. Organic ranking is fine.

**Ouest-France** | `ouest-france.fr` | Type: `regional` | Status: `EXISTING → DEMOTED TO NEUTRAL`
- **Why neutral:** France's highest-circulation daily, valuable for provincial sentiment. But **blocked by Anthropic's crawler** and its foreign policy coverage is minimal — primarily a domestic/regional outlet. The Brest naval base reporting niche is real but too narrow to justify a boost given extraction impossibility. Organic ranking is appropriate.

**BFM TV / RMC** | `bfmtv.com` | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Curation exclusion was correct under the hard-filter model — 24-hour TV news focused on breaking domestic news and talk-show debate. Under the Goggle model, no reason to actively discard. BFM occasionally breaks domestic political stories (cabinet reshuffles, crisis events) that matter for domestic constraints analysis. CMA CGM acquisition (Rodolphe Saadé) may shift editorial direction — monitor.

**20 Minutes** | `20minutes.fr` | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Free commuter daily primarily aggregating AFP wire copy. No original foreign/security policy analysis. But under the Goggle model, organic ranking is harmless — it won't displace boosted sources.

**HuffPost France** | `huffingtonpost.fr` | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Primarily aggregates and repackages content. Under the Goggle model, organic ranking is appropriate — no reason to actively discard a source that occasionally surfaces policy-relevant content from its contributor network.

---

### Discard — `$discard`

**CNews** | `cnews.fr` | Status: `CONFIRMED DISCARD`
- **Discard reasoning:** Right-wing opinion-driven TV channel owned by Vivendi/Bolloré. Entertainment-format political commentary, not original reporting. Deliberately provocative framing would inject noise into event extraction. The Bolloré media empire's editorial direction (nationalist, anti-immigration) produces content designed to generate engagement, not inform policy analysis. Would actively displace higher-signal sources from top results.

**Valeurs Actuelles** | `valeursactuelles.com` | Status: `CONFIRMED DISCARD`
- **Discard reasoning:** Right-nationalist weekly magazine. Primarily ideological commentary rather than original reporting on strategic posture. Has been convicted of racial provocation. Content would inject partisan noise — the right-flank analytical perspective it claims to offer is better sourced through Le Figaro's editorial pages and RN-adjacent columnists elsewhere.

**RT France** | `francais.rt.com` | Status: `NEW DISCARD`
- **Discard reasoning:** Russian state media in French. Operations suspended in France following EU sanctions (March 2022), but archived content and affiliated channels still surface in search results. Would inject state propaganda framing. Any Russia-related analysis should come from French domestic sources, not from Russia's own information operations targeting French audiences.

---

## STRUCTURAL COVERAGE CHECK

| Structural Role | Source(s) | Tier | Notes |
|---|---|---|---|
| Government leak/signaling channel | France 24, Le Monde | T1, T1 | France 24 reflects state perspective directly; Le Monde is where Élysée/Quai d'Orsay officials place signals. Both essential but serve different functions |
| Opposition voice (left) | Libération, Mediapart | T2, T2 | Libération for daily left-progressive coverage; Mediapart for investigative revelations. Le Monde diplomatique (T3) for intellectual left critique |
| Opposition voice (right) | Le Figaro | T1 | Right-of-center establishment voice. CNews discarded — Le Figaro provides the right-flank perspective with actual journalistic rigor |
| Defence/security first-mover | Intelligence Online, Le Figaro | T2, T1 | Intelligence Online for covert/intelligence operations; Le Figaro for defense-industrial via Dassault ownership. FRS and Revue Défense Nationale for analytical depth |
| Policy-elite discourse | IFRI, Le Monde, Les Echos | T2, T1, T1 | IFRI for think-tank framing; Le Monde for what the political class reads; Les Echos for what the business/economic policy class reads |
| Domestic-language depth | All French-language sources | T1–T3 | **Non-English boost premium applies.** French-language sources dominate the map correctly — political discourse occurs overwhelmingly in French. France 24 English is the primary English-language bridge |
| Official government source | elysee.fr, gouvernement.fr, diplomatie.gouv.fr | T2 | **LAYER 2 MIGRATION** — primary fetch via direct polling. Goggle boost as fallback. Public Sénat/LCP (T2) for parliamentary proceedings |
| Analytical/think tank depth | IFRI, FRS, Revue Défense Nationale | T2, T2, T3 | IFRI for broad foreign policy; FRS for defense/security; Revue Défense Nationale for military-doctrinal |
| Wire service (local bureau) | Reuters, AP News | Neutral | Not boosted — wire copy is available organically. Reuters is blocked by Anthropic crawler. AP News is unblocked and provides fallback wire coverage |
| Francophone Africa/overseas | Africa Intelligence | T3 | Fills the primary coverage gap identified by the whitelist. Sahel, West Africa, Indo-Pacific territory coverage |

**Gaps identified:**
1. **Extraction crisis:** 12 of 17 recommended sources are blocked by Anthropic's crawler. The pipeline is heavily dependent on France 24, IFRI, FRS, Public Sénat/LCP, Revue Défense Nationale, and government Layer 2 polling for actual full-text extraction. Headline-level detection from blocked sources via Brave is valuable but insufficient for deep analysis. This is a systemic risk for France dossier quality.
2. **Trade union and social movement perspectives** remain underrepresented — no dedicated labor/union press is included. These views surface through Libération and Mediapart but are filtered through those outlets' editorial priorities.
3. **Indo-Pacific territorial coverage** (New Caledonia, Réunion, French Polynesia) is thin — Africa Intelligence covers the African dimension but the Pacific/Indian Ocean strategic posture is covered only episodically by France 24 and Le Monde.
4. **Real-time defense procurement** at the contract/program level is only partially covered. La Tribune (latribune.fr) has a defense vertical that could strengthen this, but its extraction status is uncertain and it overlaps with Les Echos.

---

## REDUNDANCY RESOLUTION

**Broadsheet cluster: Le Monde + Le Figaro + Libération + La Croix + Le Parisien + Ouest-France**
Six national/regional dailies is manageable because they divide cleanly by editorial function: Le Monde (Tier 1, center-left agenda-setter), Le Figaro (Tier 1, center-right defense-connected), Libération (Tier 2, left-progressive opposition), La Croix (Neutral, blocked + niche overlap with France 24), Le Parisien (Neutral, blocked + public opinion barometer role is secondary), Ouest-France (Neutral, blocked + minimal foreign policy content). All four Neutral sources are blocked by Anthropic's crawler, which naturally resolves the redundancy — they can't be extracted, so organic ranking is appropriate.

**Policy specialist cluster: Contexte + L'Opinion + Le Monde diplomatique**
Three political specialists serve distinct niches: Contexte (Tier 3, legislative/regulatory process), L'Opinion (Tier 3, centrist-liberal establishment), Le Monde diplomatique (Tier 3, left-intellectual counter-hegemonic). No redundancy — each covers different analytical territory. All three are at Tier 3, which is appropriate for their supplementary roles.

**Security/defense cluster: Intelligence Online + Revue Défense Nationale + FRS**
Three defense-focused sources with clear differentiation: Intelligence Online (Tier 2, investigative intelligence-grade reporting), FRS (Tier 2, analytical think-tank depth on deterrence/arms control), Revue Défense Nationale (Tier 3, doctrinal/institutional military voice with monthly cadence). No redundancy — each occupies a distinct position on the speed-vs-depth spectrum.

**Think tank cluster: IFRI + FRS + Revue Défense Nationale**
IFRI covers broad foreign policy and strategic posture; FRS covers defense and security specifically; Revue Défense Nationale covers military doctrine from inside the establishment. Differentiation is by domain scope, not quality. IFRI and FRS at Tier 2; Revue Défense Nationale at Tier 3 for lower publication frequency.

**Indigo Publications cluster: Intelligence Online + La Lettre A + Africa Intelligence**
Same publisher, different niches: Intelligence Online (Tier 2, intelligence/defense), La Lettre A (Neutral, domestic political insider — blocked, niche overlaps with IO), Africa Intelligence (Tier 3, Francophone Africa coverage gap fill). La Lettre A drops to Neutral to avoid over-representing one publisher at boosted tiers.

---

## QUERY CONFIGURATION

```
country: FR
search_lang: fr
freshness: pw
```

**Multi-language notes:** France's media ecosystem operates overwhelmingly in French. English-language sources are limited to France 24 English, IFRI English publications, Intelligence Online English edition, and international wire pickups. Queries should run primarily in French; a secondary English query cycle for defense/security and think-tank topics would capture IFRI, FRS (some English output), and France 24 English. The pipeline's existing `languages.metadata: en` configuration handles this correctly. **Non-English domestic sources get boost premium** — the French-language sources should be weighted heavily in Goggle construction because French political discourse does not translate well into English search terms.

**Localized query vocabulary validation:**

The curation prompt's vocabulary is strong and well-calibrated to French political discourse. Notes:

- **Domain 1 (Diplomatic):** All terms valid and well-chosen. `"Quai d'Orsay"` is the correct metonym — used universally in French political journalism. Add `"Macron politique étrangère"` as a leader-specific pattern. `"autonomie stratégique"` is the single most important French diplomatic concept — consider using it as a standing query term. Add `"Indo-Pacifique"` — France's Indo-Pacific strategy (via overseas territories) is a major axis of diplomatic alignment distinct from the Franco-German/EU focus. Add `"AUKUS"` — the Australian submarine deal fallout continues to shape French attitudes toward Anglophone alliances.
- **Domain 2 (Security):** Excellent list. `"BITD"` is correct insider acronym that will surface specialist content. Add `"DGSE"` (external intelligence) and `"DGSI"` (internal security) — intelligence service mentions are high-signal for security posture shifts. Add `"Barkhane"` / `"forces françaises"` for overseas military operations (even though Barkhane ended, the term remains in discourse about Sahel withdrawal). Consider adding `"char Leclerc"` and `"Rafale"` as major procurement program markers.
- **Domain 3 (Economic):** Solid. `"Bercy"` metonym is correct. Add `"plan France 2030"` — the flagship industrial strategy. Add `"IPCEI"` (Important Projects of Common European Interest) — relevant for semiconductor and battery/hydrogen industrial policy with EU dimension. `"taxe carbone"` (carbon tax) for energy/climate statecraft. Add `"sanctions Russie"` for sanctions-specific coverage.
- **Domain 4 (Institutional):** Valid. Add `"présidence française"` when France holds EU Council presidency rotations. `"Francophonie"` is correctly included. Add `"G7"` and `"G20"` — France's participation in summit diplomacy is a core institutional engagement signal. Add `"aide publique au développement"` (ODA — official development assistance) for development policy institutional dimension.
- **Domain 5 (Domestic):** Strong. Add `"49.3"` — the constitutional article for forcing legislation without a vote, extremely high-signal for domestic institutional crisis. Add `"dissolution"` — relevant given recent precedent. `"Rassemblement National"` / `"RN"` should be standing search terms given RN's role as the largest single party. Add `"Nouveau Front Populaire"` / `"NFP"` for the left coalition domestic constraint.

**Stale/problematic terms:** None are stale. All vocabulary reflects current French political discourse accurately. `"cohabitation"` may become more relevant if RN gains power — currently a theoretical scenario but the term is correct to include.

**Suggested topic query patterns:**

1. `Macron autonomie stratégique Europe défense` — French push for European strategic autonomy
2. `loi de programmation militaire BITD exportations` — Defense budget and industrial base
3. `Quai d'Orsay Sahel forces françaises` — French military withdrawal and Sahel posture
4. `Bercy souveraineté industrielle France 2030` — Industrial sovereignty and economic statecraft
5. `Assemblée nationale 49.3 budget défense RN` — Parliamentary constraints on defense spending

---

## GOGGLE FILE

```goggle
! name: MPM France
! description: MPM pipeline source prioritization for France — boosts high-signal sources, discards noise
! public: false
! author: MPM Pipeline

! --- Tier 1: Essential (boost=3) ---
$boost=3,site=france24.com
$boost=3,site=lemonde.fr
$boost=3,site=lefigaro.fr
$boost=3,site=lesechos.fr

! --- Tier 2: Important (boost=2) ---
$boost=2,site=mediapart.fr
$boost=2,site=liberation.fr
$boost=2,site=ifri.org
$boost=2,site=intelligenceonline.com
$boost=2,site=elysee.fr
$boost=2,site=gouvernement.fr
$boost=2,site=diplomatie.gouv.fr
$boost=2,site=publicsenat.fr
$boost=2,site=lcp.fr
$boost=2,site=frstrategie.org

! --- Tier 3: Supplementary (boost=1) ---
$boost=1,site=defnat.com
$boost=1,site=contexte.com
$boost=1,site=lopinion.fr
$boost=1,site=africaintelligence.com
$boost=1,site=monde-diplomatique.fr

! --- Discard: Noise ---
$discard,site=cnews.fr
$discard,site=valeursactuelles.com
$discard,site=francais.rt.com
```

---

## INTERPRETIVE CONTEXT FOR DOSSIER

### Tier 1 Sources

> Articles from **France 24** about any domain should be interpreted as reflecting the French state's preferred framing of international events because it is a government-funded international broadcaster operated by France Médias Monde — editorially independent by statute but structurally aligned with French diplomatic messaging. Its coverage of French military operations, EU negotiations, and bilateral summits should be read as the version of events France wants an international audience to see. Particularly valuable when France 24 framing diverges from Le Monde or Le Figaro framing — the divergence itself is a signal of internal policy debate.

> Articles from **Le Monde** about diplomatic alignment and institutional engagement should be interpreted as France's most authoritative independent broadsheet reporting — its center-left editorial line and strong editorial independence charter (journalist veto rights) make it the closest thing France has to a newspaper that elites trust and officials use for signaling. When a Quai d'Orsay shift appears in Le Monde, it is likely deliberate. Xavier Niel's majority ownership through the Fund for Press Independence creates potential blind spots on telecoms and tech policy but does not demonstrably affect foreign policy coverage.

> Articles from **Le Figaro** about defense and security matters should be interpreted with awareness that the Dassault Group (major defense contractor) is the owner — this creates uniquely deep sourcing on defense procurement, arms exports, and military-industrial matters, but also means coverage of Dassault-related contracts (Rafale sales, combat aviation programs) is structurally conflicted. Its center-right to right, pro-Atlanticist editorial line provides the essential counterweight to Le Monde's center-left framing on NATO, European defense, and transatlantic relations.

> Articles from **Les Echos** about economic policy and trade should be interpreted as reflecting the perspective of France's business and financial establishment — owned by LVMH (Bernard Arnault), its liberal-economic editorial line frames industrial sovereignty and trade policy through an investment-climate lens. Negative coverage of protectionist or state-interventionist measures does not necessarily mean the policy is failing, only that it is unpopular with the private sector. The sole authoritative source for Bercy decision-making at granular level.

### Tier 2 Sources

> Articles from **Mediapart** about government misconduct and arms deals should be interpreted as France's most rigorous investigative journalism — its subscriber-funded nonprofit model (no advertising, no billionaire owner, 245,000+ subscribers) makes it structurally the most independent outlet in French media. Edwy Plenel's left-leaning editorial orientation means it frames government actions critically by default, but its investigative methodology is consistently rigorous. When Mediapart breaks a defense or diplomacy scandal, the story is typically well-sourced and consequential.

> Articles from **Libération** about arms exports, migration, and Françafrique legacy should be interpreted as filtered through a left-progressive editorial lens — its non-profit endowment structure supports independence, but its editorial orientation means it will frame French military operations abroad and arms sales critically. Valuable for surfacing domestic left-wing constraints that the center-right sources (Le Figaro, Les Echos) will not emphasize.

> Articles from **IFRI** about strategic posture and diplomatic alignment should be interpreted as reflecting the mainstream French foreign policy establishment's analytical consensus — not government policy but the intellectual framework within which policy is debated. IFRI's proximity to the Quai d'Orsay means its publications often preview or rationalize policy shifts. When IFRI publishes a major brief reconsidering an alliance or strategic doctrine, it is a leading indicator of possible official repositioning.

> Articles from **Intelligence Online** about intelligence services and defense contracts should be interpreted as investigative intelligence-grade reporting with no peer in French-language media — Indigo Publications' independence (no government, party, or investor ties) and niche focus produce content that is unavailable elsewhere. Its revelations about DGSE operations, defense contractor maneuvering, and covert diplomatic activity should be treated as high-signal regardless of the publication's low public profile.

> Articles from **Public Sénat / LCP** should be interpreted as primary-source parliamentary material — not journalism but direct records of committee hearings, floor debates, and legislative investigations. Committee proceedings on arms exports, defense budgets, and treaty ratification are factual inputs, not editorial positions. The pipeline should use these as authoritative evidence of what was said in Parliament, not as analytical sources.

> Articles from **Élysée / gouvernement.fr / diplomatie.gouv.fr** should be interpreted as official government communications — not journalism but primary source material representing the government's chosen public position. Presidential statements, diplomatic communiqués, and ministerial announcements from these domains are authoritative for what the government *says* it is doing, which may diverge from what it is actually doing.

> Articles from **FRS** about nuclear deterrence, arms control, and defense strategy should be interpreted as analytically rigorous think-tank output from France's principal defense research institution — its proximity to the defense establishment provides deep technical expertise but also means its analytical frames align with defense community assumptions. Particularly authoritative on nuclear deterrence policy, where FRS expertise is recognized internationally.

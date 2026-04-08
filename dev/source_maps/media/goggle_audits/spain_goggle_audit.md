# AUDIT SUMMARY: SPAIN

**Sources assessed:** 18 recommended + 5 excluded + 4 newly identified = 27 total
**Tier 1 (boost=3):** 4 sources
**Tier 2 (boost=2):** 8 sources
**Tier 3 (boost=1):** 5 sources
**Neutral (no rule):** 6 sources
**Discard:** 4 sources
**Overall assessment:** The curation prompt produced a well-balanced whitelist with strong ideological spectrum coverage and genuine depth on economic statecraft — three dedicated business dailies is unusual for a European country map. Key changes: (1) resolved redundancy in the business press cluster by tiering Expansion above the other two financial titles; (2) promoted government official sources for Layer 2 migration; (3) added missing structural roles (public broadcaster RTVE, Royal Household); (4) flagged **7 recommended sources** as blocked by Anthropic's crawler — the heaviest blockade of any audited country so far. Spain's legacy media is severely crawler-hostile, which makes the unblocked digital-native sources (elDiario.es, El Espanol, Infodefensa, Atalayar) disproportionately valuable for extraction. Non-English domestic-language sources receive a boost premium throughout — Spain's political discourse operates in Spanish and the pipeline must prioritize extractable Spanish-language sources over English-language summaries.

---

## BOOST ASSIGNMENTS

### Tier 1 — `$boost=3`

**elDiario.es** | `eldiario.es` | Type: `investigative` | Status: `EXISTING`
- **Structural role:** Spain's leading progressive investigative outlet and the highest-signal extractable source on the whitelist. Reader-funded model produces genuinely independent coverage of left-flank constraints on government foreign policy.
- **Domain coverage:** Domestic constraints, Diplomatic alignment, Institutional engagement
- **Reasoning:** With 7 of the 18 recommended sources blocked by Anthropic's crawler, extraction feasibility becomes a decisive tiebreaker. elDiario.es is fully open access (no paywall, no crawler block), publishes in Spanish (boost premium), and fills the critical structural role of surfacing coalition tensions within the PSOE-Sumar government on defense spending, NATO, arms exports, and Palestine. Its member-funded model insulates it from the commercial pressures that shape the blocked legacy broadsheets. In a normal media ecosystem this would be Tier 2 behind El Pais, but Spain's crawler blockade elevates it.
- **Extraction note:** Open access, no paywall, no crawler block. Full text extractable.

**El Espanol** | `elespanol.com` | Type: `paper_of_record` | Status: `EXISTING`
- **Structural role:** Largest digital-only newspaper by unique visitors (~20M/month). The primary extractable broadsheet-equivalent on the list.
- **Domain coverage:** Domestic constraints, Security/defense, Diplomatic alignment
- **Reasoning:** With El Pais, El Mundo, and ABC all blocked by Anthropic's crawler, El Espanol becomes the pipeline's best extractable generalist source. Center-right editorial line (Pedro J. Ramirez) provides the opposition-adjacent framing that El Mundo and ABC would normally supply. Its growing defense/security vertical and aggressive political coverage make it the closest functional replacement for the blocked legacy trio. Spanish-language, mostly open access — the pipeline needs this surfacing first.
- **Extraction note:** Mostly open access. Not blocked by crawler.

**Infodefensa** | `infodefensa.com` | Type: `security_defense` | Status: `EXISTING`
- **Structural role:** Spain's only dedicated defense and security digital newspaper. Irreplaceable for the security/defense domain — no other source systematically covers procurement, PESCO, FCAS, arms exports, and military operations.
- **Domain coverage:** Security/defense autonomy, Economic/technological statecraft
- **Reasoning:** Structural monopoly in its domain demands Tier 1. Spain lacks a robust military OSINT community, making Infodefensa the single point of failure for defense reporting. Open access, no paywall, no crawler block, Spanish-language — all extraction advantages apply. The source intelligence map correctly identifies that Spanish defense-specialist coverage is thin compared to other European middle powers; this makes Infodefensa's unique position even more valuable.
- **Extraction note:** Open access, no paywall, no crawler block. Full text extractable.

**Agencia EFE** | `efe.com` | Type: `government_aligned` | Status: `EXISTING` | **BLOCKED**
- **Structural role:** Spain's national news agency and the world's fourth-largest wire service. The raw feed that most Spanish outlets build upon. Official government statements, diplomatic communiques, and military deployment announcements appear here first.
- **Domain coverage:** Diplomatic alignment, Institutional engagement, Security/defense
- **Reasoning:** Structural role outweighs extraction difficulty. EFE is the first-mover for official Spanish government communications — its dispatches are the baseline against which all other coverage is written. State-owned wire services in middle powers are essential pipeline sources because they signal government intent before editorial interpretation. **Blocked by Anthropic's crawler**, which limits extraction, but Brave can still surface EFE dispatches for discovery, and EFE content is widely syndicated across unblocked outlets. The pipeline needs EFE appearing in top results even if full extraction requires fallback to syndicated versions.
- **Extraction note:** Blocked by Anthropic crawler. Brave can discover; extraction via syndication fallback.

---

### Tier 2 — `$boost=2`

**El Pais** | `elpais.com` | Type: `paper_of_record` | Status: `EXISTING` | **BLOCKED**
- **Structural role:** Spain's newspaper of record. Primary venue for elite foreign-policy debate, op-eds by former ministers, and detailed EU summit coverage. Largest international desk in Spanish-language media.
- **Domain coverage:** Diplomatic alignment, Institutional engagement, Domestic constraints
- **Reasoning:** Would be Tier 1 in any extraction-unconstrained scenario — El Pais is the single most important Spanish news source for foreign policy analysis. **Blocked by Anthropic's crawler**, which forces demotion to Tier 2. Brave can still surface El Pais for discovery and headlines, and the freemium paywall means some articles may be partially accessible through alternative extraction paths. The boost ensures it ranks above organic when Brave finds it, but the pipeline cannot depend on consistent full-text extraction.
- **Extraction note:** Blocked by Anthropic crawler. Freemium paywall. Partial extraction may be possible via Diffbot for non-premium articles.

**El Mundo** | `elmundo.es` | Type: `paper_of_record` | Status: `EXISTING` | **BLOCKED**
- **Structural role:** Spain's second-largest daily and principal counterweight to El Pais. Essential for detecting opposition framing of government foreign policy and defense decisions.
- **Domain coverage:** Domestic constraints, Diplomatic alignment, Security/defense
- **Reasoning:** Center-right editorial line is structurally necessary — the pipeline needs to see how PP-aligned media frames government decisions on NATO, defense spending, Morocco, and EU integration. **Blocked by Anthropic's crawler**, limiting extraction. El Espanol at Tier 1 partially compensates (similar editorial positioning), but El Mundo's investigative tradition and institutional weight justify maintaining Tier 2 boost for discovery.
- **Extraction note:** Blocked by Anthropic crawler. Dynamic paywall (~163K subscribers).

**La Vanguardia** | `lavanguardia.com` | Type: `regional` | Status: `EXISTING` | **BLOCKED**
- **Structural role:** Essential for monitoring Catalan territorial politics and their constraint on central government foreign policy. Also Spain's strongest international news desk.
- **Domain coverage:** Domestic constraints, Diplomatic alignment, Institutional engagement
- **Reasoning:** Fills a unique structural role that no other source can replicate — the intersection of Catalan politics and Spanish foreign policy. Barcelona's economic weight, Mediterranean orientation, and post-amnesty dynamics make La Vanguardia irreplaceable for detecting how territorial politics constrain Madrid's external posture. **Blocked by Anthropic's crawler**, but Brave can surface it for discovery. No other blocked-source substitute exists for this niche.
- **Extraction note:** Blocked by Anthropic crawler. Metered paywall (~100K subscribers).

**Expansion** | `expansion.com` | Type: `business_financial` | Status: `EXISTING` | **BLOCKED**
- **Structural role:** Spain's leading business daily. Primary source for trade policy, industrial strategy, FDI flows, tech regulation, and EU single-market positioning.
- **Domain coverage:** Economic/technological statecraft, Institutional engagement
- **Reasoning:** Leads the three-business-daily cluster due to editorial focus and Ibex-35 corporate coverage with geopolitical dimensions (Telefonica, Indra, Navantia). **Blocked by Anthropic's crawler**, which limits extraction. El Economista (unblocked, see Tier 3) provides partial fallback for economic statecraft. Tier 2 rather than Tier 1 because the blocked status makes it unreliable for consistent full-text extraction.
- **Extraction note:** Blocked by Anthropic crawler. Hard paywall for most content.

**Real Instituto Elcano** | `realinstitutoelcano.org` | Type: `political_specialist` / `think_tank` | Status: `EXISTING`
- **Structural role:** Spain's flagship foreign-policy think tank. Publishes the only regular survey of Spanish public opinion on foreign policy (Barometro del Real Instituto Elcano). Annual "Espana en el Mundo" report anticipates government positioning.
- **Domain coverage:** All five domains
- **Reasoning:** Think tanks earn boost through depth, not speed. Elcano's policy briefs (Comentarios Elcano, ARI papers) provide the structural analysis the pipeline needs to interpret daily events — why Spain's defense spending target matters, what FCAS delays mean for European strategic autonomy, how Spanish public opinion constrains Mediterranean policy. Fully open access, no crawler block. Tier 2 because it doesn't break news but its analytical output is unique and extractable.
- **Extraction note:** Fully open access, no paywall, no crawler block. Full text extractable.

**Politica Exterior** | `politicaexterior.com` | Type: `political_specialist` | Status: `EXISTING`
- **Structural role:** Spain's preeminent foreign-affairs journal — equivalent of Foreign Affairs. Platform for serving and former diplomats, military officers, and academics to signal strategic thinking.
- **Domain coverage:** Diplomatic alignment, Security/defense autonomy, Institutional engagement
- **Reasoning:** Think tanks earn boost through depth, not speed. Politica Exterior is where doctrinal shifts in Spanish foreign policy are first articulated. Not breaking news, but essential for detecting elite consensus formation on strategic questions (European defense, Mediterranean security, Latin American engagement). Subscription model limits extraction, but some content is open on the website. Tier 2 for analytical depth.
- **Extraction note:** Subscription required for most content. Some articles open on website. Not blocked by crawler.

**La Moncloa** | `lamoncloa.gob.es` | Type: `legislative_official` | Status: `EXISTING` — **LAYER 2 MIGRATION**
- **Structural role:** Official seat of government communications. Council of Ministers decisions, presidential statements on defense spending, EU summits, and bilateral diplomacy appear here first.
- **Domain coverage:** Diplomatic alignment, Security/defense, Institutional engagement
- **Reasoning:** Primary fetch via Layer 2 direct polling. Goggle boost at Tier 2 as belt-and-suspenders fallback. Government press releases occasionally surface in Brave News Search. Essential baseline for government-stated positions.
- **Extraction note:** Fully open access, no crawler block.

**Congreso de los Diputados** | `congreso.es` | Type: `legislative_official` | Status: `EXISTING` — **LAYER 2 MIGRATION**
- **Structural role:** Parliamentary records document committee debates on defense budgets, treaty ratifications, troop deployments, and foreign affairs. Comision de Asuntos Exteriores and Comision de Defensa proceedings are primary sources for detecting partisan constraints.
- **Domain coverage:** Domestic constraints, Institutional engagement, Security/defense
- **Reasoning:** Primary fetch via Layer 2 direct polling. Goggle boost at Tier 2 as fallback. Parliamentary records are essential for understanding domestic constraints on executive action — the investiture pacts that sustain Sanchez's minority government create veto points on defense and foreign policy that only appear in committee records.
- **Extraction note:** Fully open access, searchable archive, no crawler block.

---

### Tier 3 — `$boost=1`

**El Confidencial** | `elconfidencial.com` | Type: `investigative` | Status: `EXISTING` | **BLOCKED**
- **Structural role:** Spain's leading digital-native investigative outlet. Regularly breaks stories on defense procurement, energy deals, sovereign wealth flows, and political corruption.
- **Domain coverage:** Economic/technological statecraft, Domestic constraints, Diplomatic alignment
- **Reasoning:** High-quality investigative source with strong signal-to-noise ratio, but **blocked by Anthropic's crawler**. In an unblocked world this would be Tier 2 minimum. The crawler block forces demotion to Tier 3 — Brave can still discover El Confidencial articles for headline-level awareness, but the pipeline cannot depend on full-text extraction. Its investigative niche overlaps partially with El Espanol (Tier 1) and elDiario.es (Tier 1), which are both extractable.
- **Extraction note:** Blocked by Anthropic crawler. Metered paywall but substantial free content.

**Atalayar** | `atalayar.com` | Type: `political_specialist` | Status: `EXISTING`
- **Structural role:** Only Spanish-language outlet dedicated to Spain's southern strategic flank — Morocco, Sahel, Mediterranean migration, energy transit.
- **Domain coverage:** Diplomatic alignment, Security/defense, Institutional engagement
- **Reasoning:** Fills a genuine structural gap — the Morocco-Spain bilateral relationship is Spain's most sensitive and consequential bilateral tie, and no generalist outlet covers it with comparable depth. Open access, no crawler block, publishes in Spanish (with French and English editions). Tier 3 rather than Tier 2 because it covers a narrow geographic niche and the pipeline can capture most Morocco-related breaking news from generalist sources, using Atalayar for analytical depth.
- **Extraction note:** Open access, no paywall, no crawler block. Full text extractable.

**El Economista** | `eleconomista.es` | Type: `business_financial` | Status: `EXISTING`
- **Structural role:** Largest digital audience among Spanish business titles (~10.7M unique users). Broader topical scope than Expansion or Cinco Dias.
- **Domain coverage:** Economic/technological statecraft, Institutional engagement
- **Reasoning:** Redundant with Expansion (Tier 2) for core economic statecraft, but serves as the extractable fallback given Expansion is blocked by Anthropic's crawler. Broader topical scope (energy policy, defense industry economics) provides supplementary depth. Tier 3 because the redundancy with Expansion reduces its marginal value, but its extraction accessibility makes it worth boosting slightly above organic.
- **Extraction note:** Mixed access; much content freely available. Not blocked by crawler (note: `eleconomista.es` is distinct from `eleconomista.com.mx` which is blocked).

**Voz Populi** | `vozpopuli.com` | Type: `opposition_aligned` | Status: `EXISTING`
- **Structural role:** Digital-native outlet representing the right-of-center opposition perspective. Surfaces how PP frames critiques of government foreign policy, defense posture, and economic diplomacy.
- **Domain coverage:** Domestic constraints, Economic/technological statecraft
- **Reasoning:** Opposition-aligned sources are structurally necessary for detecting domestic contestation. Voz Populi fills the center-right to right opposition niche with original reporting and leaked documents. Tier 3 rather than Tier 2 because El Espanol (Tier 1) already provides strong center-right coverage, and ABC (Neutral, blocked) would normally fill this slot but cannot be extracted. Open access, no crawler block.
- **Extraction note:** Open access, no paywall, no crawler block. Full text extractable.

**RTVE** | `rtve.es` | Type: `public_broadcaster` | Status: `NEW`
- **Structural role:** Spain's public broadcaster. Largest broadcast audience in the country. Web content includes written articles alongside video.
- **Domain coverage:** Diplomatic alignment, Domestic constraints, Security/defense
- **Reasoning:** Missing from the original curation — a structural gap. Public broadcasters in European democracies serve as the baseline for mainstream political discourse and carry official government press conferences, parliamentary coverage, and diplomatic events. RTVE.es publishes written news articles (not just video) that are extractable. Tier 3 because its web content tends toward wire-rewrite rather than original analysis, but the structural role of a public broadcaster in a European middle power warrants inclusion. Listed in `es.yaml` as a domestic source.
- **Extraction note:** Open access, no paywall. Not blocked by crawler. Some content is video-only (not extractable).

---

### Neutral — no Goggle rule

**ABC** | `abc.es` | Type: `opposition_aligned` | Status: `EXISTING → DEMOTED TO NEUTRAL` | **BLOCKED**
- **Why neutral:** Conservative monarchist daily that fills the constitutional-right niche, but **blocked by Anthropic's crawler**. Its editorial line is partially covered by El Espanol (Tier 1) and Voz Populi (Tier 3), both of which are extractable. Exclusions default to Neutral not Discard — ABC may surface organically in Brave for specific queries and provide headline-level signal even without full extraction. If the crawler block is lifted, re-evaluate at Tier 2.

**Cinco Dias** | `cincodias.elpais.com` | Type: `business_financial` | Status: `EXISTING → DEMOTED TO NEUTRAL`
- **Why neutral:** Redundant with Expansion (Tier 2) and El Economista (Tier 3) for economic statecraft. Hosted on a subdomain of `elpais.com`, which is **blocked by Anthropic's crawler**. Three business dailies in the active Goggle is excessive when two are already covering the domain. Cinco Dias's tech/startup niche is the least relevant for strategic posture monitoring. Organic ranking sufficient.

**La Razon** | `larazon.es` | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)` | **BLOCKED**
- **Why neutral:** Curation exclusion was correct — declining circulation, editorial line duplicates ABC. Under the Goggle model, no reason to actively discard. Also **blocked by Anthropic's crawler**, making the question moot for extraction. May surface organically for specific queries.

**Publico** | `publico.es` | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Left-wing digital outlet that duplicates elDiario.es from a similar ideological position with lower rigor. Under the Goggle model, no reason to actively discard. May surface organically and provide supplementary left-progressive signal.

**Libertad Digital** | `libertaddigital.com` | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Right-libertarian outlet with limited original foreign-policy reporting. Its positions on defense and diplomacy are derivative of PP messaging already captured via El Espanol and Voz Populi. No reason to actively discard under Goggle model — organic ranking is appropriate.

**20 Minutos** | `20minutos.es` | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)` | **BLOCKED**
- **Why neutral:** High-traffic free newspaper with minimal original defense/diplomacy reporting. Also **blocked by Anthropic's crawler**. No reason to discard — organic ranking sufficient, though extraction would fail regardless.

---

### Discard — `$discard`

**OKDIARIO** | `okdiario.com` | Status: `CONFIRMED DISCARD`
- **Discard reasoning:** Rated far-right with persistent factual reliability concerns (Media Bias/Fact Check rates it Right-Far Right). Adversarial editorial style and frequent use of unverified claims would actively displace higher-signal sources from top results. The opposition-aligned slot is better served by El Espanol, Voz Populi, and ABC. Pure noise for strategic analysis.

**Caso Aislado** | `casoaislado.com` | Status: `NEW DISCARD`
- **Discard reasoning:** Clickbait aggregator with sensationalist framing and minimal original reporting. No editorial accountability. Would waste result slots displacing real sources.

**Periodista Digital** | `periodistadigital.com` | Status: `NEW DISCARD`
- **Discard reasoning:** Right-wing commentary blog masquerading as journalism. Known for inflammatory headlines, conspiracy content, and minimal fact-checking. Would inject noise and confuse event extraction.

**Hispanidad** | `hispanidad.com` | Status: `NEW DISCARD`
- **Discard reasoning:** Far-right Catholic nationalist commentary outlet with no original foreign-policy reporting. Editorial content is ideological commentary, not news. Would actively displace boosted sources.

---

## STRUCTURAL COVERAGE CHECK

| Structural Role | Source(s) | Tier | Notes |
|---|---|---|---|
| Government leak channel / signaling | Agencia EFE, La Moncloa | T1, T2 | EFE functions as the government's preferred dissemination channel; La Moncloa for official statements. LAYER 2 MIGRATION for La Moncloa |
| Opposition voice | El Espanol, Voz Populi | T1, T3 | El Espanol (center-right, Ramirez) and Voz Populi (right, PP-adjacent). ABC at Neutral provides fallback if crawler block lifts |
| Defence/security first-mover | Infodefensa | T1 | Structural monopoly — Spain's only dedicated defense press. No redundancy, no substitute |
| Policy-elite discourse | Real Instituto Elcano, Politica Exterior | T2, T2 | Elcano for empirical research and public opinion data; Politica Exterior for strategic doctrine. Think tank depth, not speed |
| Domestic-language depth | All Spanish-language sources | T1-T3 | Spain's political discourse operates in Spanish. English-language Elcano publications are supplements. Catalan, Basque, Galician coverage is a known gap (see below) |
| Official government source | La Moncloa, Congreso de los Diputados | T2, T2 | **LAYER 2 MIGRATION** — primary fetch via direct polling. Goggle boost as fallback |
| Analytical/think tank depth | Real Instituto Elcano, Politica Exterior, Atalayar | T2, T2, T3 | Elcano for cross-domain analysis; Politica Exterior for strategic debate; Atalayar for Mediterranean/North Africa depth |
| Wire service (domestic) | Agencia EFE | T1 | Boosted at T1 due to structural role as national wire despite crawler block. Syndication ensures content appears in extractable outlets |
| Business/economic statecraft | Expansion, El Economista | T2, T3 | Expansion leads but is blocked; El Economista is extractable fallback |
| Regional/territorial constraints | La Vanguardia | T2 | Blocked but irreplaceable for Catalan-Madrid dynamic. No extractable substitute |
| Public broadcaster | RTVE | T3 | Newly added. Baseline mainstream discourse and official event coverage |
| Left-flank coalition constraint | elDiario.es | T1 | Surfaces PSOE-Sumar tensions on defense, NATO, arms exports, Palestine |
| Investigative/accountability | El Confidencial, elDiario.es | T3, T1 | El Confidencial blocked; elDiario.es extractable. Pipeline leans on elDiario.es for investigative function |

**Gaps identified:**
1. **Basque and Galician regional perspectives** remain a structural blind spot. El Correo (Basque Country) and La Voz de Galicia cover regional politics but their foreign-policy signal is weaker than La Vanguardia's. Not included to avoid over-expanding the Goggle, but if PNV coalition dynamics become critical to government survival, El Correo should be added at Tier 3.
2. **Real-time military operational reporting** is thin. Spain lacks independent mil-blogging or OSINT community comparable to France or the UK. Infodefensa and Ministry of Defense channels carry outsized share with limited adversarial verification. Mitigated by Layer 2 polling of official sources.
3. **EU-level Spanish-language coverage** from Brussels correspondents is distributed across generalist outlets rather than concentrated in a dedicated Brussels bureau publication. No single source isolates Spain-specific EU positioning signals. Partially mitigated by Elcano's EU analysis.
4. **Crawler blockade severity** — 7 of 18 recommended sources are blocked by Anthropic's crawler. This is the heaviest blockade in any audited country and creates systemic extraction risk. The audit compensates by elevating extractable sources, but the pipeline should monitor for crawler policy changes.

---

## REDUNDANCY RESOLUTION

**Broadsheet cluster: El Pais + El Mundo + El Espanol + ABC**
Four generalist national outlets spanning the ideological spectrum. Resolved primarily by extraction reality: El Pais and El Mundo are both blocked, so El Espanol (Tier 1, extractable, center-right) becomes the primary broadsheet. El Pais (Tier 2, blocked, center-left) and El Mundo (Tier 2, blocked, center-right) retain boost for discovery but cannot be depended on for extraction. ABC drops to Neutral — blocked and editorially redundant with El Espanol and El Mundo.

**Business press cluster: Expansion + Cinco Dias + El Economista**
Three dedicated business dailies is unusual redundancy. Expansion leads (Tier 2) due to editorial focus on Ibex-35 geopolitics, but is blocked. El Economista (Tier 3) serves as extractable fallback with broader topical scope. Cinco Dias drops to Neutral — hosted on blocked elpais.com subdomain and editorially the least distinctive of the three. Pipeline relies on El Economista for day-to-day economic statecraft extraction, with Expansion for discovery.

**Investigative cluster: El Confidencial + elDiario.es**
Two digital-native investigative outlets with different editorial orientations. elDiario.es (Tier 1, progressive, extractable) leads because it is open access and covers the left-flank coalition constraints uniquely. El Confidencial (Tier 3, liberal-centrist, blocked) provides supplementary investigative depth when discoverable. No true redundancy — different editorial perspectives and domain emphases.

**Opposition cluster: El Espanol + Voz Populi + ABC**
Three center-right to right outlets. El Espanol (Tier 1, extractable, largest audience) leads. Voz Populi (Tier 3, extractable, right-of-center scoops) provides supplementary opposition signal. ABC (Neutral, blocked) falls off the active Goggle. Differentiated by extraction reality and audience scale.

**Think tank cluster: Real Instituto Elcano + Politica Exterior**
No redundancy — different structural roles. Elcano produces empirical research and public opinion data; Politica Exterior hosts strategic debate among practitioners. Both Tier 2 for analytical depth.

---

## QUERY CONFIGURATION

```
country: ES
search_lang: es
freshness: pw
```

**Multi-language notes:** Spain's political discourse operates primarily in Spanish. Regional languages (Catalan, Basque, Galician) carry some political signal but foreign-policy content is overwhelmingly in Castilian Spanish. English-language content from Real Instituto Elcano and Atalayar's English edition are supplements. Queries should run primarily in Spanish; a secondary English query cycle for defense/security and think tank content would capture Elcano English publications and international wire coverage. The pipeline's existing `languages.metadata: en` configuration handles this correctly.

**Localized query vocabulary validation:**

The curation prompt's vocabulary is solid. Notes:

- **Domain 1 (Diplomatic):** All terms valid. Add `"Sanchez cumbre"` and `"Albares"` (Foreign Minister Jose Manuel Albares) as leader-specific patterns. `"cumbre iberoamericana"` is correct and important — Spain's Ibero-American diplomacy is a unique middle-power lever. Add `"Marruecos"` (Morocco) as a high-signal bilateral term.
- **Domain 2 (Security):** Strong list. Add `"Robles"` or `"ministra de Defensa"` (if Margarita Robles still holds the post — verify against current cabinet). `"FCAS"` and `"PESCO"` are correct and high-signal. Add `"Ceuta Melilla"` — Spain's North African enclaves are permanent security flashpoints. `"dos por ciento PIB defensa"` (2% GDP defense target) for defense spending stories.
- **Domain 3 (Economic):** Excellent. `"fondos europeos"` and `"Next Generation"` are high-signal for Spain's economic recovery architecture. Add `"Telefonica participacion estatal"` — the government's stake acquisition in Telefonica via SEPI is a live economic statecraft story. Add `"transicion energetica hidrogeno"` for Spain's green hydrogen ambitions. `"semiconductores"` is increasingly relevant for EU Chips Act implementation in Spain.
- **Domain 4 (Institutional):** Valid. Add `"Comunidad Politica Europea"` which is already in the vocabulary. `"presidencia del Consejo"` is important — Spain held the EU Council presidency in H2 2023 and its legacy shapes current positioning. Add `"G20"` — Spain is not a G20 member but lobbies for inclusion, which is a recurring diplomatic storyline.
- **Domain 5 (Domestic):** Strong. Add `"amnistia"` (amnesty law for Catalan independence leaders — the defining domestic constraint story of 2024-2026). `"pactos de investidura"` is excellent — the deals Sanchez struck with Catalan and Basque parties to secure investiture create binding foreign-policy constraints. Add `"Puigdemont"` as a high-signal name. `"Sumar PSOE tension"` for coalition dynamics.

**Stale/problematic terms:** None are stale. `"no alineamiento"` (non-alignment) is low-probability for Spain given firm NATO/EU anchoring — it will return noise. Consider dropping or pairing with a qualifier like `"no alineamiento debate Espana"`.

**Suggested topic query patterns:**

1. `Sanchez politica exterior OTAN defensa` — PM's defense/NATO positioning
2. `FCAS caza europeo industria defensa Espana` — FCAS fighter program / defense industry
3. `Marruecos Espana migracion Ceuta Melilla` — Morocco bilateral / migration / enclaves
4. `fondos europeos Next Generation Espana inversiones` — EU recovery funds implementation
5. `amnistia Cataluna pactos investidura politica exterior` — Catalan amnesty constraining foreign policy
6. `gasto defensa dos por ciento PIB presupuesto` — Defense spending toward 2% target
7. `Telefonica SEPI participacion estatal soberania tecnologica` — State economic intervention / tech sovereignty

---

## GOGGLE FILE

```goggle
! name: MPM Spain
! description: MPM pipeline source prioritization for Spain — boosts high-signal sources, discards noise
! public: false
! author: MPM Pipeline

! --- Tier 1: Essential (boost=3) ---
$boost=3,site=eldiario.es
$boost=3,site=elespanol.com
$boost=3,site=infodefensa.com
$boost=3,site=efe.com

! --- Tier 2: Important (boost=2) ---
$boost=2,site=elpais.com
$boost=2,site=elmundo.es
$boost=2,site=lavanguardia.com
$boost=2,site=expansion.com
$boost=2,site=realinstitutoelcano.org
$boost=2,site=politicaexterior.com
$boost=2,site=lamoncloa.gob.es
$boost=2,site=congreso.es

! --- Tier 3: Supplementary (boost=1) ---
$boost=1,site=elconfidencial.com
$boost=1,site=atalayar.com
$boost=1,site=eleconomista.es
$boost=1,site=vozpopuli.com
$boost=1,site=rtve.es

! --- Discard: Noise ---
$discard,site=okdiario.com
$discard,site=casoaislado.com
$discard,site=periodistadigital.com
$discard,site=hispanidad.com
```

---

## INTERPRETIVE CONTEXT FOR DOSSIER

### Tier 1 Sources

> Articles from **elDiario.es** about defense spending and NATO commitments should be interpreted as filtered through a progressive editorial lens that is sympathetic to social justice and human rights framing of foreign policy — its member-funded model produces genuinely independent journalism, but its editorial orientation means it frames military spending increases and arms exports critically. Coverage of PSOE-Sumar coalition tensions is especially valuable because elDiario.es has the best sourcing within Sumar and left-coalition circles, making it the first outlet to surface left-flank dissent on defense, Palestine, and migration policy.

> Articles from **El Espanol** about government policy should be interpreted as filtered through a center-right constitutionalist lens — founder Pedro J. Ramirez (formerly of El Mundo) built the outlet as an opposition-adjacent digital broadsheet critical of the Sanchez government. Its political coverage reliably surfaces PP and centrist criticism of government foreign policy. Useful for detecting opposition red lines on territorial integrity, Morocco relations, and defense posture, but likely to frame ambiguous government decisions negatively.

> Articles from **Infodefensa** about defense procurement and military operations should be interpreted as sector-specialist reporting that is industry-embedded — close relationships with the Ministry of Defense and defense contractors (Indra, Navantia, Airbus Spain) mean it has the best sourcing on procurement, FCAS, PESCO projects, and military exercises, but its coverage tends to reflect the defense establishment's perspective. Critical assessments of procurement failures or cost overruns may be muted compared to what an adversarial outlet would produce.

> Articles from **Agencia EFE** about diplomatic events and government positions should be interpreted as state-owned wire service output — officially neutral but subject to government influence. EFE dispatches represent what the Spanish state wants the public record to show. They are primary source material rather than journalism: accurate on facts of record (who said what, where, when) but unreliable for detecting what the government is concealing or downplaying. Trade union concerns about editorial independence (raised in 2025) warrant monitoring.

### Tier 2 Sources

> Articles from **El Pais** about EU integration and foreign policy should be interpreted as reflecting Spain's liberal-internationalist establishment consensus — its center-left orientation, PRISA group ownership, and historically close relationship with PSOE mean its foreign-policy coverage amplifies multilateralist and pro-European framing. The largest international desk in Spanish media makes its EU summit and diplomatic reporting the most detailed available, but the editorial lens consistently favors deeper integration and institutional engagement.

> Articles from **El Mundo** about government defense and foreign policy decisions should be interpreted as the principal opposition broadsheet's critique — its center-right editorial line, Unidad Editorial ownership, and editorial alignment with PP positions mean it frames government foreign policy decisions through an adversarial lens. Particularly valuable for surfacing what the conservative establishment considers government failures or capitulations, but likely to overstate the severity of policy missteps by the PSOE-Sumar coalition.

> Articles from **La Vanguardia** about Catalan politics and their foreign-policy implications should be interpreted as centrist Catalanist coverage — its moderate positioning on territorial questions, Barcelona base, and pragmatic editorial line make it the most reliable source for understanding how Catalan demands constrain Madrid's freedom of action on EU policy, Mediterranean engagement, and bilateral relationships. Its extensive network of foreign correspondents also makes its international coverage uniquely strong for a regional outlet.

> Articles from **Expansion** about trade policy and industrial strategy should be interpreted as reflecting the perspective of Spain's business establishment — its pro-business, market-liberal orientation and Unidad Editorial ownership mean it frames economic statecraft through an investment-climate and corporate-strategy lens. Coverage of Ibex-35 firms with geopolitical dimensions (Telefonica, Indra, Navantia) is especially valuable but tends to favor market-friendly policy outcomes.

> Articles from **Real Instituto Elcano** about any domain should be interpreted as establishment centrist analysis — its board includes representatives from major parties, business, and academia, producing a broadly pro-European and Atlanticist analytical orientation. Its Barometro surveys are the only regular data source on Spanish public opinion regarding foreign policy, making them essential for the Domestic Constraints domain. Policy briefs frequently anticipate government positioning, suggesting institutional proximity to the foreign policy establishment.

> Articles from **Politica Exterior** about strategic doctrine should be interpreted as elite consensus signaling — as Spain's equivalent of Foreign Affairs, it publishes serving and former diplomats, military officers, and academics, meaning its content reflects what the foreign policy establishment is thinking rather than what it is doing. Bimonthly publication cycle means it cannot break news, but doctrinal shifts articulated in Politica Exterior often precede policy changes by months.

> Articles from **La Moncloa** and **Congreso de los Diputados** should be interpreted as official government and parliamentary records — not journalism but primary source material. La Moncloa represents the executive's chosen public position; congressional records document the legislative constraints (investiture pacts, committee debates, opposition interpellations) that shape what the executive can actually do. The gap between the two is itself a signal.
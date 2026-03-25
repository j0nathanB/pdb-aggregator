# AUDIT SUMMARY: CHILE

**Sources assessed:** 18 recommended + 5 excluded + 3 newly identified = 26 total
**Tier 1 (boost=3):** 4 sources
**Tier 2 (boost=2):** 8 sources
**Tier 3 (boost=1):** 5 sources
**Neutral (no rule):** 6 sources
**Discard:** 3 sources
**Overall assessment:** The curation prompt produced a well-balanced whitelist that correctly identifies the Edwards/Copesa duopoly dominance and compensates with strong independent digital coverage. Key changes: (1) promoted domestic Spanish-language outlets that provide non-English depth, applying the non-English domestic source premium; (2) migrated government sources (Cancilleria, SUBREI) to Layer 2 at Tier 2; (3) resolved redundancy between the two legacy broadsheets by differentiating editorial roles rather than boosting both equally; (4) flagged `reuters.com` as blocked by Anthropic's crawler — critical because Reuters Santiago bureau was the sole English-language wire in the whitelist; (5) added missing structural roles (defense procurement trade press, regional wire). Chile's thin defense-journalism ecosystem and the Kast transition make investigative and think tank sources structurally overweighted relative to a typical country map — this is intentional.

---

## BOOST ASSIGNMENTS

### Tier 1 — `$boost=3`

**La Tercera** | `latercera.com` | Type: `paper_of_record` | Status: `EXISTING`
- **Structural role:** Chile's strongest political desk among legacy papers. The outlet most likely to break policy-relevant stories first, with regular foreign-policy analysis and systematic Cancilleria/Congreso beat coverage.
- **Domain coverage:** Diplomatic alignment, Domestic constraints, Economic statecraft
- **Reasoning:** La Tercera functions as Chile's agenda-setter for the political class. Its Pulso business supplement tracks trade and investment policy, giving it dual political-economic utility that El Mercurio lacks in digital form. Metered paywall means most articles are extractable via social-media referral. Spanish-language domestic source — receives non-English premium.
- **Extraction note:** Metered paywall; most political articles accessible. RSS available.

**El Mostrador** | `elmostrador.cl` | Type: `opposition_voice` / `digital_native` | Status: `EXISTING`
- **Structural role:** Chile's most-read independent digital paper (~3.5M monthly users). Essential counter-perspective to the Edwards/Copesa duopoly. Under Kast, this becomes the primary channel for opposition-sourced leaks and parliamentary analysis surfacing domestic constraints on foreign policy.
- **Domain coverage:** Domestic constraints, Diplomatic alignment, Institutional engagement
- **Reasoning:** Structural role outweighs editorial orientation per boost principles. With a right-wing government in power, El Mostrador is where the opposition signal lives — it publishes what the legacy duopoly undercovers. Free and easily extractable. The pipeline needs this counter-narrative to understand domestic constraints on Kast's foreign policy. Spanish-language — receives non-English premium.

**CIPER Chile** | `ciperchile.cl` | Type: `investigative` | Status: `EXISTING`
- **Structural role:** Chile's premier investigative outlet and the country's only member of the Global Investigative Network. Breaks stories on defense procurement irregularities, intelligence agency conduct, and opacity in state mining/lithium policy.
- **Domain coverage:** Domestic constraints, Security & defense, Economic statecraft (corruption/procurement)
- **Reasoning:** In a media landscape dominated by two conglomerates with center-right to right editorial orientations, CIPER is the structurally indispensable adversarial voice — non-partisan, investigative, and adversarial to all governments. Under Kast, CIPER's defense procurement and intelligence coverage becomes even more critical as the security apparatus expands. Free, non-profit funded. Lower publication frequency than dailies, but when CIPER publishes, it moves the conversation. Spanish-language — receives non-English premium.

**Diario Financiero** | `df.cl` | Type: `business_financial` | Status: `EXISTING`
- **Structural role:** Chile's equivalent of the Financial Times. The sole source covering trade-agreement negotiations, FDI flows, lithium/copper policy, sanctions compliance, and SUBREI announcements at depth.
- **Domain coverage:** Economic & technological statecraft, Institutional engagement (APEC, OECD, Pacific Alliance, CPTPP)
- **Reasoning:** No other source on the whitelist covers economic statecraft with this granularity. Chile's position as the world's top copper producer and a major lithium player makes economic statecraft the country's most consequential middle-power lever. Diario Financiero is the only outlet systematically tracking US-Chile critical-minerals agreements, Chinese mining investment, and CPTPP/Pacific Alliance trade dynamics. Hard paywall limits extraction, but Brave indexes headlines for ranking. Spanish-language — receives non-English premium.
- **Extraction note:** Hard paywall. Diffbot extraction likely partial. Justify subscription for economic-statecraft domain.

---

### Tier 2 — `$boost=2`

**El Mercurio / EMOL** | `emol.com` | Type: `paper_of_record` | Status: `EXISTING`
- **Structural role:** Chile's newspaper of record. Op-ed page is the primary venue where establishment foreign-policy and defense voices publish. Sunday editorial signals elite consensus or fractures.
- **Domain coverage:** Diplomatic alignment, Domestic constraints, Security & defense
- **Reasoning:** El Mercurio is the establishment voice — what the Edwards family publishes reflects what Chile's economic and political elite want amplified. Under Kast, this is a government-adjacent signal channel (historically conservative, pro-US alignment). Tier 2 rather than Tier 1 because: (1) `elmercurio.com` is behind a hard paywall and the free portal `emol.com` carries less analytical depth; (2) editorial overlap with La Tercera on center-right positioning means boosting both at Tier 1 would over-represent the duopoly at the expense of independent sources; (3) La Tercera's political desk is editorially stronger. EMOL domain is used for monitoring. Spanish-language — receives non-English premium.

**Ex-Ante** | `ex-ante.cl` | Type: `political_specialist` | Status: `EXISTING`
- **Structural role:** Chile's Politico equivalent — fast, condensed political intelligence on executive decision-making, cabinet dynamics, and legislative negotiations. Morning newsletter format is pipeline-friendly.
- **Domain coverage:** Diplomatic alignment, Domestic constraints, Institutional engagement
- **Reasoning:** Founder Cristian Bofill's deep access to both right and centrist political networks makes Ex-Ante the best source for insider political intelligence under the Kast government. Tier 2 rather than Tier 1 because its domain coverage is narrower (primarily domestic politics) and it doesn't break investigative stories. But within its niche — fast political intelligence — nothing else competes. Free and structured for daily monitoring. Spanish-language — receives non-English premium.

**Radio Cooperativa** | `cooperativa.cl` | Type: `broadcast_digital` | Status: `EXISTING`
- **Structural role:** Highest-trust news brand in Chile per Reuters Institute surveys. Political interview programs surface positions from across the spectrum. Web portal publishes full transcripts and wire content.
- **Domain coverage:** Domestic constraints, Diplomatic alignment
- **Reasoning:** Trust premium matters for pipeline signal quality. Cooperativa's center-left orientation and historically anti-authoritarian stance make it a natural counterweight to the duopoly under a right-wing government. Free, well-structured for extraction. Tier 2 rather than Tier 1 because its original reporting rate is lower than La Tercera or CIPER — it often amplifies rather than breaks. Spanish-language — receives non-English premium.

**BioBioChile** | `biobiochile.cl` | Type: `broadcast_digital` / `regional` | Status: `EXISTING`
- **Structural role:** Largest news network in Chile by geographic reach (40 radio frequencies). Strongest coverage of regional security — southern border, Araucania conflict, migration.
- **Domain coverage:** Domestic constraints, Security & defense (regional security, borders)
- **Reasoning:** Geographic reach fills a structural gap that Santiago-centric outlets miss. Araucania and southern border dynamics are increasingly relevant under Kast's security-first agenda. Breaking-news velocity is high. Free, high-volume output. Tier 2 rather than Tier 1 because much of its content is wire aggregation rather than original reporting, and its foreign-policy coverage is thin. Spanish-language — receives non-English premium.

**Infodefensa (Chile edition)** | `infodefensa.com` | Type: `security_defense` | Status: `EXISTING`
- **Structural role:** The sole dedicated defense-procurement source covering Chile. Tracks arms acquisitions, joint exercises with US/regional partners, bilateral defense agreements, and FIDAE coverage.
- **Domain coverage:** Security & defense autonomy (procurement, exercises, bilateral military cooperation)
- **Reasoning:** Chile has no domestic defense beat journalism — this is the coverage gap assessment's most significant finding. Infodefensa is the only source on the whitelist systematically tracking defense procurement, which is a primary signal for security-autonomy posture. Spanish-language trade press based in Spain. Tier 2 rather than Tier 1 because publication frequency is moderate and its scope is single-domain (defense procurement only). But within that domain, it is irreplaceable.

**Cancilleria de Chile** | `minrel.gob.cl` | Type: `government_official` | Status: `EXISTING` — **LAYER 2 MIGRATION**
- **Structural role:** Primary source for communiques, bilateral meeting readouts, treaty actions, multilateral voting positions, and ambassadorial appointments.
- **Domain coverage:** Diplomatic alignment, Institutional engagement
- **Reasoning:** Government sources = Layer 2 migration at Tier 2. Primary fetch via Layer 2 direct polling. Goggle boost at Tier 2 as belt-and-suspenders fallback. Under Kast, watch for shifts in tone toward Venezuela, China infrastructure projects, and US alignment signals. Press-release format — official state position, not journalism.

**SUBREI** | `subrei.gob.cl` | Type: `government_official` | Status: `EXISTING` — **LAYER 2 MIGRATION**
- **Structural role:** Publishes FTA negotiation updates, trade-statistics bulletins, APEC/OECD/WTO positions, and ProChile export-promotion priorities. The critical-minerals and lithium-supply-chain dossier sits here.
- **Domain coverage:** Economic & technological statecraft, Institutional engagement
- **Reasoning:** Government sources = Layer 2 migration at Tier 2. Under Kast's appointee Paula Estevez, watch for US-aligned trade-security framing. SUBREI is where lithium supply-chain policy and critical-minerals agreements are announced before they appear in media. Layer 2 direct polling primary; Goggle boost as fallback.

**gob.cl (Government Portal)** | `gob.cl` | Type: `government_official` | Status: `FROM YAML` — **LAYER 2 MIGRATION**
- **Structural role:** Central government web portal. Houses presidential communications, ministerial bulletins, and legislative records. Includes `bcn.cl` (Biblioteca del Congreso Nacional) per YAML config.
- **Domain coverage:** All five domains (official source)
- **Reasoning:** The cl.yaml config lists `gob.cl` and `bcn.cl` as Tier 1 government sources. Under Goggle audit principles, government sources migrate to Layer 2 at Tier 2. Primary fetch via direct polling. Goggle boost as fallback. BCN (Congressional Library) provides legislative tracking — ratification votes, committee proceedings, and constitutional reform processes.

---

### Tier 3 — `$boost=1`

**Interferencia** | `interferencia.cl` | Type: `investigative` | Status: `EXISTING`
- **Structural role:** Left-perspective adversarial investigative outlet. Breaks stories on security-sector conduct, intelligence operations, and political financing.
- **Domain coverage:** Domestic constraints, Security & defense
- **Reasoning:** Fills the adversarial-investigative niche from the left — under a right-wing Kast government, this becomes a primary friction detector between the security apparatus and civil society. Tier 3 rather than Tier 2 because domain coverage overlaps with CIPER (both investigative, both adversarial) and publication frequency is lower. CIPER has broader sourcing and institutional credibility; Interferencia provides the complementary left-lens. Spanish-language — receives non-English premium. Reader-funded, mostly free.

**Pauta** | `pauta.cl` | Type: `business_specialist` | Status: `EXISTING`
- **Structural role:** Long-form analysis on economic policy, infrastructure, and energy. Ownership by the Construction Chamber gives privileged access to infrastructure-investment and public-works policy circles.
- **Domain coverage:** Economic & technological statecraft, Domestic constraints
- **Reasoning:** Tier 3 rather than Tier 2 because it overlaps with Diario Financiero on economic statecraft but with narrower scope (infrastructure/construction focus vs. DF's broader trade/FDI/minerals coverage). Its Construction Chamber ownership is both a strength (insider access) and a limitation (business-sector framing). Useful for tracking industrial policy and public investment signals that DF covers less granularly. Free. Spanish-language.

**AthenaLab** | `athenalab.org` | Type: `think_tank` | Status: `EXISTING`
- **Structural role:** Chile's leading independent civil-society forum on defense and foreign affairs. Publishes policy briefs, hosts events with senior military/diplomatic figures.
- **Domain coverage:** Security & defense autonomy, Diplomatic alignment
- **Reasoning:** Think tanks earn boost through depth, not speed. AthenaLab publishes the structural analysis the pipeline needs to interpret defense and foreign-policy events — why a particular arms acquisition matters strategically, what a bilateral defense agreement signals about alignment. Center-right realist orientation aligns with Kast government's worldview, making it a window into policy-elite defense thinking. English-language output aids cross-referencing. Tier 3 because publication frequency is low (monthly monitoring) and it doesn't break news. Director's RUSI affiliation adds transatlantic analytical depth.

**Americas Quarterly** | `americasquarterly.org` | Type: `think_tank` / `regional_analytical` | Status: `EXISTING`
- **Structural role:** Best English-language analytical lens on Chile's regional positioning. Council of the Americas publication providing the external-perception layer that domestic sources miss.
- **Domain coverage:** Diplomatic alignment, Economic statecraft, Institutional engagement
- **Reasoning:** Think tank outlet providing structural depth on Chile's regional positioning — Pacific Alliance dynamics, APEC engagement, comparative middle-power analysis. Not Chile-specific (covers all of Latin America), so Tier 3. English-language, which limits its domestic-signal value but provides the international-audience framing the pipeline needs.

**BNamericas** | `bnamericas.com` | Type: `business_intelligence` | Status: `EXISTING`
- **Structural role:** Authoritative source for Chile's lithium, copper, and energy-infrastructure sectors — the material backbone of economic statecraft.
- **Domain coverage:** Economic & technological statecraft (critical minerals, energy, infrastructure)
- **Reasoning:** Tracks US-Chile critical-minerals agreements, Chinese investment in mining, and regulatory changes. Tier 3 rather than Tier 2 because it overlaps with Diario Financiero on economic statecraft, and its investor-oriented framing is narrower than DF's policy coverage. Paywalled — some free articles. English and Spanish bilingual, which increases pipeline accessibility.

---

### Neutral — no Goggle rule

**T13 (Canal 13)** | `t13.cl` | Type: `broadcast_digital` | Status: `EXISTING → DEMOTED TO NEUTRAL`
- **Why neutral:** Redundant with Cooperativa and BioBioChile for broadcast-origin political coverage. Luksic ownership introduces business-elite framing that overlaps with El Mercurio's center-right positioning. Under the Goggle model, T13 can still appear organically for breaking political events — no need to boost, but no reason to discard either. Highest-traffic TV news site means Brave will surface it naturally for major stories.

**El Libero** | `ellibero.cl` | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Curation exclusion was justified under the hard-filter model — right-wing opinion-heavy content duplicative of El Mercurio editorials. Under the Goggle model, exclusions default to Neutral not Discard. El Libero may surface intra-right coalition dynamics (Partido Republicano vs. Chile Vamos tensions) that the legacy duopoly undercovers. Organic ranking is appropriate — if it surfaces, the pipeline benefits from seeing intra-coalition friction.

**The Clinic** | `theclinic.cl` | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Satirical/cultural-political magazine with minimal foreign-policy coverage. Excluded from whitelist correctly, but under Goggle model no reason to actively discard. Organic ranking lets it surface for major domestic political stories where its center-left cultural framing adds color.

**CNN Chile** | `cnnchile.com` | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Editorial-direction uncertainty following 2025 ownership change, limited text-based output. Same logic as broadcast exclusions in Mexico audit — under Goggle model, no reason to actively discard. If CNN Chile breaks a story, Brave surfaces it organically.

**Diario Estrategia** | `diarioestrategia.cl` | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Business daily inferior to Diario Financiero for economic-statecraft coverage. Redundant but not harmful — organic ranking is appropriate.

**TVN (Television Nacional)** | `tvn.cl` | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Public broadcaster with thinner online output than T13 or Cooperativa. Under Goggle model, public-service media should not be actively discarded — it may surface official government communications or legislative broadcast content.

---

### Discard — `$discard`

**Reuters (Santiago bureau)** | `reuters.com` | Status: `BLOCKED — FLAGGED`
- **Discard reasoning:** **Blocked by Anthropic's crawler** (`reuters.com` appears on blocked_domains.md with Chile listed as an affected country). Cannot be used with Claude's `WebSearch(allowed_domains=[...])` parameter. Brave can still discover and surface Reuters headlines for ranking, but the pipeline cannot extract full text. Do not boost — boosting a blocked domain wastes result slots on content the pipeline cannot read. Wire copy is available organically via other channels (AP News, France24 per cl.yaml). **Not a true discard — flagged as blocked. Remove from Goggle entirely rather than $discard to avoid suppressing headline-level signal from Brave.**
- **Mitigation:** Rely on AP News and France24 (per cl.yaml wire config) for English-language wire coverage. Consider adding `apnews.com` at Tier 3 if English-language wire signal is consistently insufficient.

**Gamba** | `gamba.cl` | Status: `NEW DISCARD`
- **Discard reasoning:** Hyper-partisan left-wing commentary site with no editorial structure and no original reporting. Content is primarily opinion/outrage commentary that would displace higher-signal investigative sources (CIPER, Interferencia) from results. Pure commentary noise.

**El Ciudadano** | `elciudadano.com` | Status: `NEW DISCARD`
- **Discard reasoning:** Outlet with history of publishing unverified claims and conspiracy-adjacent content. Frequently cited in misinformation tracking reports. Would inject noise into the pipeline and potentially contaminate event extraction with unreliable claims.

---

## STRUCTURAL COVERAGE CHECK

| Structural Role | Source(s) | Tier | Notes |
|---|---|---|---|
| Government leak channel / signaling | El Mercurio (EMOL) | T2 | Under Kast, the Edwards group is the establishment-aligned signaling channel. Op-ed page signals government intent. El Libero (Neutral) provides secondary intra-right signal |
| Opposition voice | El Mostrador, Interferencia | T1, T3 | El Mostrador is the primary opposition-sourced outlet; Interferencia provides left-adversarial investigative complement |
| Defence/security first-mover | Infodefensa, CIPER | T2, T1 | No domestic defence beat — Infodefensa (Spanish trade press) covers procurement; CIPER breaks security-sector misconduct. AthenaLab (T3) for analytical depth |
| Policy-elite discourse | Ex-Ante, La Tercera | T2, T1 | Ex-Ante for insider political intelligence; La Tercera for what decision-makers read daily |
| Domestic-language depth | All Spanish-language sources | T1-T3 | Chile's media operates overwhelmingly in Spanish. English sources (Americas Quarterly, BNamericas, AthenaLab English output) are supplements. Non-English domestic premium applied across tiers |
| Official government source | gob.cl, minrel.gob.cl, subrei.gob.cl | T2 | **LAYER 2 MIGRATION** — primary fetch via direct polling. Goggle boost as fallback. Includes bcn.cl for legislative tracking |
| Analytical/think tank depth | AthenaLab, Americas Quarterly, BNamericas | T3, T3, T3 | AthenaLab for defense/foreign affairs; Americas Quarterly for regional positioning; BNamericas for critical minerals/energy sector. Think tanks = depth not speed |
| Wire service (local bureau) | AP News, France24 | Neutral | Not boosted in Goggle — wire copy available organically. Reuters blocked by Anthropic crawler — flagged, not boosted |
| Business/economic specialist | Diario Financiero, Pauta | T1, T3 | DF for broad economic statecraft; Pauta for infrastructure/construction niche |
| Broadcast/real-time signal | Cooperativa, BioBioChile | T2, T2 | Cooperativa for highest-trust political interviews; BioBioChile for geographic reach and regional security |

**Gaps identified:**
1. **Dedicated Chilean military/defense journalism** remains the most significant structural blind spot — no domestic outlet maintains a specialized defense beat. Mitigated by Infodefensa (Spanish trade press) and AthenaLab (think tank), but neither provides daily operational coverage. FIDAE (biennial air show) generates a burst of defense coverage that no outlet sustains between events.
2. **Multilateral-institution coverage** — Chile's positions in UN votes, OAS proceedings, and Pacific Alliance negotiations are rarely reported in real time by domestic media. Mitigated by Cancilleria Layer 2 polling and wire services, but analytical coverage of multilateral positioning is thin.
3. **Chinese-language sourcing on China-Chile relations** — Xinhua Santiago, People's Daily coverage of bilateral meetings, and CGTN Spanish-language content would strengthen detection of Beijing's framing of the lithium/critical-minerals relationship. Falls outside Spanish/English pipeline scope.
4. **Mapuche/indigenous media** — Mapuexpress and other indigenous media outlets cover the Araucania conflict from perspectives unavailable in mainstream media. Not included because pipeline scope is foreign-policy/statecraft, but the blind_spots section of cl.yaml correctly identifies this gap for domestic-constraint analysis.

---

## REDUNDANCY RESOLUTION

**Legacy broadsheet cluster: La Tercera + El Mercurio/EMOL**
Both are legacy conglomerates covering the same center-right editorial space. Resolved by differentiating editorial roles: La Tercera (Tier 1, stronger political desk, digital-first, more moderate) vs. El Mercurio/EMOL (Tier 2, newspaper of record, establishment op-ed venue, harder paywall). La Tercera leads because its political reporting is more systematic and its paywall is more permeable. Boosting both at Tier 1 would over-represent the duopoly relative to independent sources.

**Investigative cluster: CIPER + Interferencia**
Both are investigative outlets adversarial to government, but from different positions. CIPER (Tier 1, non-partisan, Global Investigative Network member, broadest sourcing) vs. Interferencia (Tier 3, left-leaning, narrower scope, lower frequency). CIPER is structurally indispensable; Interferencia supplements with a left-adversarial lens that becomes more valuable under a right-wing government. No true redundancy — differentiated by institutional credibility and publication frequency.

**Broadcast-digital cluster: Cooperativa + BioBioChile + T13**
Three broadcast-origin outlets with digital portals. Resolved: Cooperativa (Tier 2, highest trust, center-left, political interviews), BioBioChile (Tier 2, widest geographic reach, regional security), T13 (Neutral, redundant with the other two, Luksic ownership framing overlaps with El Mercurio). Two broadcast sources at Tier 2 provides breaking-news velocity without over-saturating results.

**Economic statecraft cluster: Diario Financiero + BNamericas + Pauta**
Three outlets covering economic/business territory. Diario Financiero (Tier 1, broadest economic coverage, trade/FDI/minerals), BNamericas (Tier 3, mining/energy specialist, investor-oriented), Pauta (Tier 3, infrastructure/construction niche). DF is the generalist leader; BNamericas and Pauta fill sector-specific niches without competing with DF for the same stories.

**Government source cluster: gob.cl + minrel.gob.cl + subrei.gob.cl**
All three are official government sources at Tier 2. No redundancy — they cover distinct institutional domains (general government, foreign ministry, trade/economic relations). All migrate to Layer 2 with Goggle boost as fallback.

---

## QUERY CONFIGURATION

```
country: CL
search_lang: es
freshness: pw
```

**Multi-language notes:** Chile's media ecosystem operates overwhelmingly in Spanish. English-language sources (Americas Quarterly, BNamericas, AthenaLab English output) are supplements. Queries should run primarily in Spanish; a secondary English query cycle for defense/economic-statecraft topics would capture AthenaLab, Americas Quarterly, and BNamericas. The pipeline's existing `languages.metadata: en` configuration handles this correctly.

**Localized query vocabulary validation:**

The curation prompt's vocabulary is solid. Notes:

- **Domain 1 (Diplomatic):** All terms valid. Add `"Kast politica exterior"` and `"Canciller Van Klaveren"` (or Kast's appointee — verify current FM) as leader-specific patterns. `"equidistancia"` is particularly high-signal for Chile — the traditional equidistance doctrine between US and China is the defining diplomatic-alignment question under Kast. Add `"cumbre APEC"` — Chile's APEC membership makes summits a recurring high-signal event.
- **Domain 2 (Security):** Strong list. `"FIDAE"` is correctly included but fires only biennially — pair with `"adquisicion militar"` and `"ejercicio conjunto"` for continuous signal. Add `"Comando Jungla"` (Kast's Araucania security escalation) and `"frontera norte migracion"` (northern border migration, increasingly relevant). `"Ley Reservada del Cobre"` is excellent — tracks the legacy defense-funding mechanism.
- **Domain 3 (Economic):** Excellent. `"litio"` and `"cobre"` are correct but very high-frequency — pair: `"litio Chile politica"` or `"litio nacionalizacion"` to filter for policy rather than commodity price noise. Add `"CPTPP"` / `"TPP-11"` — Chile's CPTPP ratification and implementation is a live trade-policy story. `"cable submarino"` is high-signal given US-China competition over Humboldt cable. Add `"Codelco gobernanza"` for state-mining-company governance stories.
- **Domain 4 (Institutional):** Valid. `"Alianza del Pacifico"` is correct. Add `"PROSUR"` (Kast may re-emphasize this Pinera-era initiative over CELAC). `"OCDE Chile"` for OECD compliance/review stories. `"COP clima Chile"` for climate-diplomacy positioning.
- **Domain 5 (Domestic):** Strong. Add `"Tribunal Constitucional reforma"` (TC is a live institutional battleground). `"Contraloria"` is excellent — the Comptroller General's audits constrain executive action and generate stories. Add `"encuesta Cadem"` (Chile's most-cited weekly poll, drives media narrative on presidential approval). `"coalicion Kast"` / `"Partido Republicano Chile Vamos"` for intra-coalition dynamics.

**Stale/problematic terms:** None are stale. `"proceso constituyente"` may be declining — the 2023 constitutional process concluded, but residual constitutional-reform debates persist. Keep but deprioritize.

**Suggested topic query patterns:**

1. `Kast politica exterior China Estados Unidos` — Diplomatic alignment under new administration
2. `litio Chile CPTPP minerales criticos` — Critical minerals and trade agreements
3. `cable submarino Humboldt Chile` — US-China undersea cable competition
4. `Araucania seguridad Fuerzas Armadas Kast` — Security operations in southern Chile
5. `Codelco litio gobernanza nacionalizacion` — State mining company and lithium policy
6. `Alianza del Pacifico cumbre Chile APEC` — Regional and multilateral positioning

---

## GOGGLE FILE

```goggle
! name: MPM Chile
! description: MPM pipeline source prioritization for Chile — boosts high-signal sources, discards noise
! public: false
! author: MPM Pipeline

! --- Tier 1: Essential (boost=3) ---
$boost=3,site=latercera.com
$boost=3,site=elmostrador.cl
$boost=3,site=ciperchile.cl
$boost=3,site=df.cl

! --- Tier 2: Important (boost=2) ---
$boost=2,site=emol.com
$boost=2,site=ex-ante.cl
$boost=2,site=cooperativa.cl
$boost=2,site=biobiochile.cl
$boost=2,site=infodefensa.com
$boost=2,site=minrel.gob.cl
$boost=2,site=subrei.gob.cl
$boost=2,site=gob.cl

! --- Tier 3: Supplementary (boost=1) ---
$boost=1,site=interferencia.cl
$boost=1,site=pauta.cl
$boost=1,site=athenalab.org
$boost=1,site=americasquarterly.org
$boost=1,site=bnamericas.com

! --- Discard: Noise ---
$discard,site=gamba.cl
$discard,site=elciudadano.com
```

---

## INTERPRETIVE CONTEXT FOR DOSSIER

### Tier 1 Sources

> Articles from **La Tercera** about domestic politics and foreign policy should be interpreted as Chile's most rigorous political desk reporting — its center to center-right editorial orientation and Copesa group ownership mean it frames economic and trade policy through a pro-business lens, but its news coverage is consistently the most systematic and best-sourced among legacy papers. Under Kast, La Tercera is editorially sympathetic to the government's economic agenda but maintains enough editorial independence to report cabinet friction and policy failures.

> Articles from **El Mostrador** about government policy should be interpreted as filtered through a center-left to progressive editorial lens that is structurally critical of right-wing administrations — under Kast, El Mostrador is where opposition-sourced leaks, parliamentary resistance, and civil-society pushback surface first. Its 3.5M monthly readership makes it the most widely read independent digital outlet, and its editorial selection reflects what the opposition wants amplified. Essential for detecting domestic constraints on Kast's foreign policy, but likely to frame ambiguous government actions negatively.

> Articles from **CIPER Chile** about defense procurement, intelligence operations, or mining policy should be interpreted as Chile's most authoritative investigative reporting — non-partisan and structurally adversarial to all governments. CIPER breaks stories that no other outlet will touch, particularly on defense procurement irregularities and opacity in state mining/lithium policy. Its non-profit structure insulates it from both government and corporate pressure. When CIPER publishes on a topic, the underlying investigation is typically deep and well-sourced, even if infrequent.

> Articles from **Diario Financiero** about trade agreements, FDI, and minerals policy should be interpreted as reflecting the perspective of Chile's business and financial establishment — its pro-market, center-right orientation means it frames economic policy through an investment-climate and trade-liberalization lens. Negative coverage of government regulation does not necessarily mean the policy is failing, only that it is unpopular with the private sector. But for tracking CPTPP implementation, lithium policy details, APEC positioning, and SUBREI announcements, no other source provides comparable depth.

### Tier 2 Sources

> Articles from **El Mercurio / EMOL** about foreign policy and defense should be interpreted as reflecting Chile's conservative establishment consensus — the Edwards family's historically pro-US, pro-business orientation means El Mercurio's op-ed page functions as the primary venue for defense and foreign-policy establishment voices. Under Kast, this outlet is editorially aligned with the government. What appears on El Mercurio's Sunday editorial page signals what the security and business elite want amplified.

> Articles from **Ex-Ante** about executive decision-making and coalition dynamics should be interpreted as insider political intelligence with a center-right framing — founder Cristian Bofill's access to right and centrist political networks makes this the fastest source for cabinet reshuffles, legislative negotiations, and intra-coalition tensions. Concise, newsletter-format reporting optimized for political insiders.

> Articles from **Radio Cooperativa** about political developments should be interpreted as high-credibility, center-left reporting — Cooperativa's anti-authoritarian institutional history and Reuters Institute trust rankings make it a reliable baseline source, though its editorial orientation means it is more likely to amplify opposition voices and civil-society concerns than government achievements.

> Articles from **BioBioChile** about regional security and border issues should be interpreted as reflecting Chile's widest geographic news coverage — its 40-station radio network captures Araucania conflict, southern border, and migration dynamics that Santiago-centric outlets miss. Centrist and explicitly independent, but high-volume output includes significant wire aggregation alongside original reporting.

> Articles from **Infodefensa** about defense procurement and military exercises should be interpreted as industry-oriented trade reporting — neutral-descriptive, not analytical. Infodefensa reports what is being acquired, by whom, and at what cost, but does not analyze strategic implications. The pipeline needs AthenaLab or CIPER to interpret what Infodefensa reports factually.

> Articles from **gob.cl**, **minrel.gob.cl**, and **subrei.gob.cl** should be interpreted as official government communications — not journalism but primary source material. Press releases, communiques, and trade bulletins represent the government's chosen public position, which may differ from actual policy implementation. Under Kast's new administration, watch for tonal shifts in Cancilleria communiques regarding Venezuela, China, and US alignment.

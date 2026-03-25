# AUDIT SUMMARY: BRAZIL

**Sources assessed:** 18 recommended + 5 excluded + 4 newly identified = 27 total
**Tier 1 (boost=3):** 4 sources
**Tier 2 (boost=2):** 8 sources
**Tier 3 (boost=1):** 6 sources
**Neutral (no rule):** 6 sources
**Discard:** 3 sources
**Overall assessment:** The curation prompt produced a strong whitelist with excellent coverage of Brazil's concentrated broadsheet market and solid think tank representation. Key changes: (1) resolved redundancy within the broadsheet trio (Folha, O Globo, Estadao) by differentiating editorial roles and flagging Estadao as blocked; (2) promoted government official sources (gov.br, planalto.gov.br) for Layer 2 migration at Tier 2; (3) added missing domestic digital outlets and wire service coverage; (4) applied Portuguese-language boost premium — all domestic Portuguese-language sources receive structural preference over English-language equivalents; (5) flagged `estadao.com.br` as blocked by Anthropic's crawler, which affects extraction even though Brave can still discover it.

---

## BOOST ASSIGNMENTS

### Tier 1 — `$boost=3`

**Folha de S.Paulo** | `folha.uol.com.br` | Type: `paper_of_record` | Status: `EXISTING`
- **Structural role:** Brazil's highest-circulation quality daily and the single most important source for detecting policy-relevant shifts. Agenda-setter for political, economic, and foreign-policy debates among Brazil's elite.
- **Domain coverage:** Diplomatic alignment, Economic & technological statecraft, Domestic constraints
- **Reasoning:** Folha is Brazil's Reforma — the outlet elites read first, the one most likely to break stories that move the policy debate. Its Mundo, Mercado, and Poder sections together cover three of five analytical domains with original reporting. Strong investigative desk adds accountability coverage. Metered paywall allows partial extraction. Portuguese-language domestic source — receives structural boost premium over English equivalents.
- **Extraction note:** Metered paywall (~5 free articles/month). RSS feeds available at feeds.folha.uol.com.br. Diffbot extraction likely partial for premium content.

**O Globo** | `oglobo.globo.com` | Type: `paper_of_record` | Status: `EXISTING`
- **Structural role:** Flagship of Grupo Globo, Brazil's most powerful media conglomerate. Rio-based but national in reach. Strong foreign-affairs columnists signal elite consensus shifts.
- **Domain coverage:** Diplomatic alignment, Domestic constraints, Institutional engagement
- **Reasoning:** O Globo's center-right editorial orientation provides essential counterweight to Folha's center-left framing. Its opinion pages are where establishment consensus forms and fractures become visible. Grupo Globo's institutional weight means government actors respond to its framing — what O Globo editorializes about foreign policy shapes the debate. Metered paywall, mostly extractable.

**Valor Economico** | `valor.globo.com` | Type: `business_financial` | Status: `EXISTING`
- **Structural role:** Brazil's equivalent of the Financial Times. The sole Tier 1 source for economic and technological statecraft. Co-owned by Grupo Globo and Grupo Folha — read by policymakers and market actors.
- **Domain coverage:** Economic & technological statecraft, Institutional engagement (trade/multilateral)
- **Reasoning:** No other source covers BNDES industrial policy, Mercosur-EU trade negotiations, BRICS NDB dynamics, commodity statecraft, and technology/innovation policy at this depth. Irreplaceable for economic statecraft detection. Hard paywall limits extraction, but Brave indexes headlines for ranking and the pipeline needs Valor surfacing first for economic queries. Portuguese-language boost premium applies.
- **Extraction note:** Hard paywall. Subscription required. Diffbot extraction will be limited. Consider monitoring Valor's social media for headline signals.

**Poder360** | `poder360.com.br` | Type: `political_specialist` | Status: `EXISTING`
- **Structural role:** Brasilia-based digital-native outlet with granular coverage of congressional votes, executive decrees, and polling. Its "Poder Diplomatico" vertical tracks foreign-policy decisions specifically.
- **Domain coverage:** Domestic constraints, Diplomatic alignment, Institutional engagement
- **Reasoning:** Poder360 fills a structural role no broadsheet matches — rapid-cycle Brasilia insider coverage with data orientation. Its proximity to the executive and legislative branches gives it breaking coverage of cabinet reshuffles, decree publications, and legislative maneuvers that constrain foreign action. The Poder Diplomatico vertical is unique in Brazilian digital media. Mostly free access maximizes extraction reliability. Portuguese-language boost premium applies.

---

### Tier 2 — `$boost=2`

**Metropoles** | `metropoles.com` | Type: `digital_native` | Status: `EXISTING`
- **Structural role:** Among Brazil's top 3 most-read digital news sites (~60M unique monthly users). Brasilia proximity gives it strong executive-branch sourcing for breaking political news.
- **Domain coverage:** Domestic constraints, Security & defense autonomy (breaking news)
- **Reasoning:** Metropoles functions as Brazil's fast-breaking political news channel — cabinet reshuffles, civil-military friction, and crisis events surface here first. Free and easily extractable, which increases practical pipeline value. Tier 2 rather than Tier 1 because its analytical depth is shallower than the broadsheets and Poder360, but its speed and reach make it essential.

**JOTA** | `jota.info` | Type: `legal_regulatory` | Status: `EXISTING`
- **Structural role:** Brazil's leading legal-affairs news site. Essential for tracking STF (Supreme Court) rulings, regulatory changes, and constitutional disputes that shape the boundaries of executive foreign-policy authority.
- **Domain coverage:** Domestic constraints, Institutional engagement
- **Reasoning:** No other source covers the legal-institutional architecture of Brazilian governance with JOTA's specialist depth. STF rulings increasingly constrain executive foreign-policy action (e.g., environmental treaty compliance, indigenous rights obligations, tech regulation). JOTA provides the analytical layer the pipeline needs to interpret why certain policy moves are blocked or enabled. Freemium model — core coverage extractable.

**DefesaNet** | `defesanet.com.br` | Type: `security_defense` | Status: `EXISTING`
- **Structural role:** Brazil's most established defense-focused news site. The closest thing to a Jane's equivalent in the Brazilian media ecosystem.
- **Domain coverage:** Security & defense autonomy
- **Reasoning:** In a media landscape where defense coverage is structurally thin, DefesaNet is irreplaceable. Covers procurement, force modernization, military exercises, defense-industrial base, and geopolitical analysis from a security perspective. Single-domain but no other source competes within that domain. Pro-defense establishment orientation is a feature, not a bug — it captures what the defense community itself considers important. Mostly free; English section available.

**Agencia Brasil** | `agenciabrasil.ebc.com.br` | Type: `state_news_agency` | Status: `EXISTING` — **LAYER 2 MIGRATION**
- **Structural role:** Official state news wire operated by EBC (Empresa Brasil de Comunicacao). Publishes presidential statements, ministerial announcements, and official positions verbatim.
- **Domain coverage:** Diplomatic alignment, Institutional engagement, Economic statecraft
- **Reasoning:** Government-aligned sources earn Tier 2 per Layer 2 migration principles. Agencia Brasil is not editorially independent but is indispensable for capturing the government's declared posture. Primary fetch via Layer 2 direct polling; Goggle boost as belt-and-suspenders fallback. Fully free and easily extractable. English-language section available at agenciabrasil.ebc.com.br/en.

**gov.br / planalto.gov.br (Government Portal)** | `gov.br` + `planalto.gov.br` | Type: `government_official` | Status: `EXISTING (from br.yaml)` — **LAYER 2 MIGRATION**
- **Structural role:** Central government web portal and presidential office. Houses Itamaraty (MRE) press releases, ministerial communications, and official positions on international affairs.
- **Domain coverage:** All five domains (official source)
- **Reasoning:** Primary fetch via Layer 2 direct polling. Goggle boost at Tier 2 as fallback. Includes subdomains: gov.br/mre (Itamaraty), gov.br/defesa (Ministry of Defense). The curation prompt's separate entry for "Itamaraty Press Releases" at gov.br/mre is structurally captured by boosting the gov.br parent domain.

**Agencia Senado / Agencia Camara** | `senado.leg.br` + `camara.leg.br` | Type: `legislative_official` | Status: `EXISTING` — **LAYER 2 MIGRATION**
- **Structural role:** Legislative news wires providing verbatim coverage of committee hearings (especially CRE — Comissao de Relacoes Exteriores), floor votes on treaties, defense budgets, and trade agreements.
- **Domain coverage:** Domestic constraints, Institutional engagement
- **Reasoning:** Essential for tracking legislative constraints on executive foreign-policy action. Treaty ratification votes, defense budget appropriations, and CRE hearings are primary signals. Government/legislative sources earn Tier 2 per Layer 2 migration principles. Fully free with RSS feeds. Primary fetch via Layer 2 direct polling; Goggle boost as fallback.

**The Brazilian Report** | `brazilian.report` | Type: `analytical_newsletter` | Status: `EXISTING`
- **Structural role:** The highest-quality English-language source dedicated to Brazilian affairs. Used by diplomats, investors, and journalists.
- **Domain coverage:** All five domains (general strategic-affairs lens)
- **Reasoning:** Tier 2 rather than Tier 1 because English-language sources receive no Portuguese-language boost premium — and the pipeline's primary intake should be Portuguese. But The Brazilian Report is unique: it synthesizes across all five domains with analytical density unavailable from any wire service. When Portuguese-language monitoring flags an event, The Brazilian Report provides rapid English-language context. Subscription paywall limits extraction.
- **Extraction note:** Hard paywall (~$200/year). Newsletter-based delivery may limit Brave indexing. Consider email ingestion as supplementary access path.

---

### Tier 3 — `$boost=1`

**Congresso em Foco** | `congressoemfoco.com.br` | Type: `legislative_specialist` | Status: `EXISTING`
- **Structural role:** Specialist outlet covering congressional proceedings, voting records, and legislative politics. Watchdog orientation on bancada (caucus) dynamics.
- **Domain coverage:** Domestic constraints
- **Reasoning:** Supplements Agencia Senado/Camara with editorial analysis of legislative dynamics — not just what Congress did but why and what it means for executive authority. Single-domain (domestic constraints) limits it to Tier 3, but within that domain it provides unique depth on bancada ruralista, bancada evangelica, and coalition arithmetic that shapes foreign-policy votes. Mostly free.

**Defesa em Foco** | `defesaemfoco.com.br` | Type: `security_defense` | Status: `EXISTING`
- **Structural role:** Complements DefesaNet with coverage of armed forces operations, military aviation, and defense industry developments.
- **Domain coverage:** Security & defense autonomy
- **Reasoning:** Tier 3 rather than Tier 2 because it overlaps significantly with DefesaNet and has a more enthusiast/community orientation. But in a media ecosystem where defense coverage is thin, a second defense source provides triangulation value. Free access maximizes extraction.

**CEBRI** | `cebri.org` | Type: `think_tank` | Status: `EXISTING`
- **Structural role:** Brazil's premier foreign-policy think tank. Close to Itamaraty networks. CEBRI Journal publishes analysis on BRICS, multilateral strategy, and "active non-alignment."
- **Domain coverage:** Diplomatic alignment, Institutional engagement, Economic statecraft
- **Reasoning:** Think tanks earn boost through depth, not speed. CEBRI publications signal the thinking of Brazil's foreign-policy elite and often preview or rationalize government positioning. Tier 3 because publication frequency is low and it doesn't break news, but when CEBRI publishes, the analytical quality is high and the proximity to Itamaraty makes it a leading indicator. Bilingual (PT/EN).

**Instituto Igarape** | `igarape.org.br` | Type: `think_tank` | Status: `EXISTING`
- **Structural role:** Leading Brazilian think tank on security, climate, and technology governance. Produces data-driven reports cited in policy debates.
- **Domain coverage:** Security & defense autonomy, Institutional engagement (climate, digital governance)
- **Reasoning:** Fills a genuine gap on non-traditional security dimensions — defense spending analysis, arms flows, cyber policy, environmental security — that no media outlet covers with equivalent rigor. Think tank depth, not speed. Tier 3 because output is periodic rather than continuous. Bilingual.

**Americas Quarterly** | `americasquarterly.org` | Type: `regional_policy_magazine` | Status: `EXISTING`
- **Structural role:** Council of the Americas publication. Provides the regional comparative lens and the Washington policy community's reading of Brazil's moves.
- **Domain coverage:** Diplomatic alignment, Economic & technological statecraft, Institutional engagement
- **Reasoning:** Not Brazil-specific (covers all of Latin America), so Tier 3. But when it publishes Brazil analysis, the quality is high and the U.S. policy-community framing is unique. English-language — no Portuguese boost premium, but its structural role (how Brazil is perceived in Washington) cannot be filled by a domestic source.

**Dialogo Americas** | `dialogo-americas.com` | Type: `security_defense` | Status: `EXISTING`
- **Structural role:** U.S. SOUTHCOM-affiliated security magazine. Provides the U.S. military lens on Brazilian defense cooperation.
- **Domain coverage:** Security & defense autonomy, Diplomatic alignment (defense cooperation)
- **Reasoning:** Tier 3 as a counterpoint source — the pipeline needs to see how U.S. SOUTHCOM perceives Brazil's defense posture, which is different from how Brazil's own defense press frames it. Published in Portuguese, English, and Spanish. Narrow domain coverage limits it to Tier 3 but the U.S. defense-establishment perspective is structurally unique.

---

### Neutral — no Goggle rule

**O Estado de S. Paulo (Estadao)** | `estadao.com.br` | Type: `paper_of_record` | Status: `EXISTING → DEMOTED TO NEUTRAL`
- **Why neutral:** Valuable center-right counterweight to Folha, but **blocked by Anthropic's crawler** (`estadao.com.br` in blocked domains list). Even if Brave surfaces Estadao results, the pipeline cannot extract full text. Its editorial niche (pro-market, conservative-liberal) is partially covered by O Globo's center-right positioning and Valor Economico's business coverage. Leave neutral — may surface organically and provide headlines even without full extraction. If the crawler block is lifted, re-evaluate at Tier 2.

**Revista Piaui** | `revistapiaui.com.br` | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Curation exclusion cited monthly publication cadence as too slow for pipeline monitoring. Correct under hard-filter model. Under Goggle model, no reason to actively discard — when Piaui publishes long-form investigations on foreign-policy or institutional dynamics, Brave may surface them and the pipeline benefits. Organic ranking is appropriate.

**Carta Capital** | `cartacapital.com.br` | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Left-leaning weekly with advocacy orientation. Curation exclusion noted editorial stance and duplication with Folha/Agencia Brasil. Under Goggle model, exclusions default to Neutral, not Discard. Carta Capital's left-populist framing of alignment questions (BRICS enthusiasm, South-South solidarity) may surface signals about left-wing base sentiment that other outlets filter out. Organic ranking sufficient.

**Globo News / TV Globo** | `globonews.globo.com` | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Broadcast-first content is difficult to ingest programmatically and reporting is substantially captured by O Globo print/digital. Under Goggle model, no reason to actively discard — if Globo News publishes digital summaries of breaking broadcast coverage, Brave may surface them.

**UOL Noticias** | `noticias.uol.com.br` | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Major digital portal functioning primarily as aggregator. Original foreign-policy content is limited. Under Goggle model, organic ranking is appropriate — its high traffic means Brave may rank it for specific queries, and aggregated content can provide headline-level signal without displacing boosted sources.

**Reuters / AFP Brazil wires** | `reuters.com` + `apnews.com` + `france24.com` | Type: `wire_service` | Status: `CONFIRMED NEUTRAL (from br.yaml)`
- **Why neutral:** Wire services provide non-Brazilian editorial lens. The pipeline's Portuguese-language intake captures the same events with Brazilian framing. Not boosted in Goggle — wire copy is available organically. Note: `reuters.com` is blocked by Anthropic's crawler but Brave can still surface it for discovery.

---

### Discard — `$discard`

**Brasil 247** | `brasil247.com` | Status: `NEW DISCARD`
- **Discard reasoning:** Pro-government commentary blog with minimal original reporting and no editorial structure. Functions as a Lula/PT amplification channel. Would actively displace higher-signal sources from top results. Pure commentary noise — the government-signaling function is already captured by Agencia Brasil (official wire) and, to a lesser extent, by Folha's coverage of government positions.

**Terça Livre** | `tercalivre.com.br` | Status: `NEW DISCARD`
- **Discard reasoning:** Far-right pro-Bolsonaro commentary outlet with no original reporting. Subject to judicial investigations for disinformation. Would inject noise and potentially disinformation into the pipeline. The opposition-narrative function is better served by mainstream outlets (O Globo, Estadao) with actual editorial standards.

**Jornal da Cidade Online** | `jornaldacidadeonline.com.br` | Status: `NEW DISCARD`
- **Discard reasoning:** Identified by Brazilian fact-checkers and the TSE (Superior Electoral Tribunal) as a systematic source of political disinformation. No original reporting — aggregates and reframes content with conspiratorial framing. Would contaminate pipeline signal quality.

---

## STRUCTURAL COVERAGE CHECK

| Structural Role | Source(s) | Tier | Notes |
|---|---|---|---|
| Government leak channel / signaling | Agencia Brasil, gov.br | T2 | Official state wire + government portal capture declared posture. La Jornada-equivalent function — Agencia Brasil publishes what the government wants amplified |
| Opposition voice | O Globo, Estadao (Neutral) | T1, N | O Globo's center-right editorial line and opinion pages surface elite opposition narratives. Estadao blocked but may surface organically |
| Defence/security first-mover | DefesaNet, Defesa em Foco | T2, T3 | Thin defense press — these two are the only dedicated sources. Metropoles for breaking civil-military friction |
| Policy-elite discourse | Folha, CEBRI, Valor Economico | T1, T3, T1 | Folha for what decision-makers read; CEBRI for foreign-policy intellectual debate; Valor for economic policy elite |
| Domestic-language depth | All Portuguese-language sources | T1–T3 | Brazil's media operates primarily in Portuguese. English sources (Brazilian Report, Americas Quarterly, Dialogo Americas) are supplements, not substitutes. Portuguese-language boost premium applied throughout |
| Official government source | gov.br, planalto.gov.br, Agencia Brasil | T2 | **LAYER 2 MIGRATION** — primary fetch via direct polling. Goggle boost as fallback. Includes gov.br/mre (Itamaraty), gov.br/defesa (MOD) |
| Legislative constraint tracking | Agencia Senado, Agencia Camara, Congresso em Foco, JOTA | T2, T2, T3, T2 | Strong coverage — official wires + specialist watchdog + legal-institutional analysis |
| Analytical/think tank depth | CEBRI, Instituto Igarape, Americas Quarterly | T3, T3, T3 | CEBRI for diplomatic alignment; Igarape for non-traditional security; AQ for regional comparative framing |
| Wire service (local bureau) | Reuters, AP News, France24 | Neutral | Not boosted — wire copy available organically. Reuters blocked by Anthropic crawler |
| Legal/institutional constraint | JOTA | T2 | Unique niche — STF rulings, regulatory changes, constitutional disputes |

**Gaps identified:**
1. **Cyber and space policy** remains a structural blind spot — Brazil's satellite and cyber-defense programs lack a dedicated specialist source. DefesaNet covers episodically but without systematic depth. No mitigation available within the current source universe.
2. **Military intelligence / ABIN coverage** is structurally opaque — no open source reliably covers intelligence activities beyond occasional investigative reports in broadsheets. The br.yaml correctly identifies ABIN as an actor but no source systematically covers it.
3. **Subnational foreign-policy actors** (state governors conducting trade diplomacy, Amazon-border security dynamics) are underrepresented. No single national outlet covers these systematically. Partially mitigated by Metropoles' Brasilia-based political coverage, which occasionally picks up federal-state friction.
4. **Opposition-aligned investigative outlet** is missing — unlike Mexico's Latinus or Proceso, Brazil lacks a dedicated adversarial investigative outlet focused on the current government. O Globo and Estadao serve this function partially through their editorial lines, but there is no Brazilian equivalent of single-purpose adversarial investigation.

---

## REDUNDANCY RESOLUTION

**Broadsheet cluster: Folha + O Globo + Estadao**
All three are national broadsheets with overlapping coverage of politics, economics, and foreign affairs. Resolved by editorial differentiation: Folha (Tier 1, center-left, highest circulation, agenda-setter), O Globo (Tier 1, center-right, Grupo Globo institutional weight, foreign-affairs columnists), Estadao (Neutral — would be Tier 2 for its pro-market conservative-liberal counterweight, but blocked by Anthropic's crawler, making extraction unreliable). Two Tier 1 broadsheets is justified because Folha and O Globo occupy genuinely different editorial positions and triangulation between them is essential for posture detection.

**Government source cluster: Agencia Brasil + gov.br + planalto.gov.br + Agencia Senado + Agencia Camara**
Five government/official sources appears redundant but each serves a distinct structural function: Agencia Brasil (executive wire — what happened), gov.br/planalto.gov.br (official documents — what was declared), Agencia Senado/Camara (legislative wire — what Congress did). All at Tier 2 per Layer 2 migration principles. No redundancy reduction needed — these are primary sources, not editorial competitors.

**Defense press cluster: DefesaNet + Defesa em Foco + Dialogo Americas**
Three defense sources in a country with thin defense coverage. DefesaNet leads (Tier 2, most established, broadest coverage). Defesa em Foco (Tier 3, triangulation value but overlaps with DefesaNet). Dialogo Americas (Tier 3, unique U.S. SOUTHCOM perspective — no overlap with domestic defense press on editorial lens). Redundancy is minimal because defense coverage is so thin that multiple sources add rather than duplicate.

**Think tank cluster: CEBRI + Instituto Igarape + Americas Quarterly**
No redundancy — each covers different domains from different institutional bases. CEBRI (diplomatic alignment, Itamaraty-adjacent), Igarape (non-traditional security, climate, tech governance), AQ (regional comparative, Washington lens). All at Tier 3.

**Digital-native political cluster: Poder360 + Metropoles + Congresso em Foco**
All three are Brasilia-based digital-native outlets. Resolved by structural role: Poder360 (Tier 1, data-oriented political coverage + unique diplomatic vertical), Metropoles (Tier 2, breaking-news speed + mass reach), Congresso em Foco (Tier 3, specialist legislative watchdog). Each occupies a distinct niche despite geographic overlap.

---

## QUERY CONFIGURATION

```
country: BR
search_lang: pt
freshness: pw
```

**Multi-language notes:** Brazil's media ecosystem operates overwhelmingly in Portuguese. English-language sources (The Brazilian Report, Americas Quarterly, Dialogo Americas) are supplements. Queries should run primarily in Portuguese; a secondary English query cycle for defense and diplomatic topics would capture English-language think tank and wire coverage. The pipeline's existing `languages.metadata: en` configuration handles this correctly. Portuguese-language boost premium is structurally embedded in the tier assignments.

**Localized query vocabulary validation:**

The curation prompt's vocabulary is strong. Notes:

- **Domain 1 (Diplomatic):** All terms valid. Add `"Lula politica externa"` and `"Mauro Vieira"` (Foreign Minister) as leader-specific patterns. `"BRICS"` and `"G20"` are correct and high-priority given Brazil's 2024 G20 presidency legacy and BRICS engagement. Add `"Sul Global"` (Global South) — the dominant frame for Lula's diplomatic positioning. `"nao-alinhamento ativo"` is the key doctrinal term.
- **Domain 2 (Security):** Strong list. Add `"Jose Mucio"` or current Defense Minister name as leader-specific pattern. `"Amazonia Azul"` (Blue Amazon — maritime domain) is missing and relevant for naval defense posture. Add `"PROANTAR"` (Antarctic program) for polar security. `"fronteira"` (border) should be paired: `"fronteira amazonica"` or `"fronteira tríplice"` to avoid noise.
- **Domain 3 (Economic):** Excellent coverage. Add `"Haddad politica fiscal"` as leader-specific pattern. `"pre-sal"` (pre-salt oil reserves) is missing and remains central to energy statecraft. Add `"Novo PAC"` (new Growth Acceleration Program) for industrial policy tracking. `"minerais criticos"` (critical minerals) is increasingly relevant for Brazil's lithium/niobium/rare earths positioning.
- **Domain 4 (Institutional):** Valid. `"reforma da governanca global"` is the key frame. Add `"assento permanente"` (permanent seat — on UNSC) as a recurring Brazilian aspiration signal. `"COP"` and `"acordo climatico"` for climate institutional engagement. `"Novo Banco de Desenvolvimento"` (NDB) alongside the existing `"banco dos BRICS"`.
- **Domain 5 (Domestic):** Strong. Add `"STF Moraes"` (Alexandre de Moraes, key STF minister) as leader-specific pattern. `"bancada ruralista"` and `"bancada evangelica"` are correctly included — these are the two most powerful congressional caucuses constraining foreign-policy action. Add `"impeachment"` and `"CPI"` (parliamentary inquiry commission) as high-signal institutional crisis terms. `"eleicoes 2026"` is correctly included and will become increasingly relevant.

**Stale/problematic terms:** None are stale. All terms reflect active Brazilian political discourse as of early 2026.

**Suggested topic query patterns:**

1. `Lula politica externa BRICS Sul Global` — Diplomatic alignment and Global South positioning
2. `Haddad BNDES politica industrial neoindustrializacao` — Economic statecraft and industrial policy
3. `Forcas Armadas defesa nacional fronteira amazonica` — Defense posture and border security
4. `STF Congresso CRE tratado ratificacao` — Legislative/judicial constraints on foreign policy
5. `Mercosul UE acordo comercial` — Mercosur-EU trade agreement dynamics
6. `Petrobras pre-sal transicao energetica` — Energy statecraft
7. `ABIN inteligencia seguranca nacional` — Intelligence and national security

---

## GOGGLE FILE

```goggle
! name: MPM Brazil
! description: MPM pipeline source prioritization for Brazil — boosts high-signal sources, discards noise
! public: false
! author: MPM Pipeline

! --- Tier 1: Essential (boost=3) ---
$boost=3,site=folha.uol.com.br
$boost=3,site=oglobo.globo.com
$boost=3,site=valor.globo.com
$boost=3,site=poder360.com.br

! --- Tier 2: Important (boost=2) ---
$boost=2,site=metropoles.com
$boost=2,site=jota.info
$boost=2,site=defesanet.com.br
$boost=2,site=agenciabrasil.ebc.com.br
$boost=2,site=gov.br
$boost=2,site=planalto.gov.br
$boost=2,site=senado.leg.br
$boost=2,site=camara.leg.br
$boost=2,site=brazilian.report

! --- Tier 3: Supplementary (boost=1) ---
$boost=1,site=congressoemfoco.com.br
$boost=1,site=defesaemfoco.com.br
$boost=1,site=cebri.org
$boost=1,site=igarape.org.br
$boost=1,site=americasquarterly.org
$boost=1,site=dialogo-americas.com

! --- Discard: Noise ---
$discard,site=brasil247.com
$discard,site=tercalivre.com.br
$discard,site=jornaldacidadeonline.com.br
```

---

## INTERPRETIVE CONTEXT FOR DOSSIER

### Tier 1 Sources

> Articles from **Folha de S.Paulo** about any domain should be interpreted as Brazil's most rigorous independent broadsheet reporting — its center-left editorial line and claim of nonpartisanship mean it provides critical coverage of both government and opposition, and it is the outlet Brazilian political elites read first. Its Mundo section's framing of diplomatic events is the closest proxy for how Brazil's informed public understands foreign-policy moves.

> Articles from **O Globo** about foreign policy and institutional dynamics should be interpreted as reflecting the perspective of Brazil's center-right establishment because Grupo Globo's institutional liberalism and the newspaper's Rio-based editorial tradition produce coverage that is skeptical of left-populist diplomatic ventures (BRICS enthusiasm, South-South solidarity rhetoric) while supportive of trade liberalization and institutional reform — valuable for surfacing elite criticism of government positioning but likely to frame non-alignment as indecisiveness.

> Articles from **Valor Economico** about economic policy should be interpreted as reflecting the perspective of Brazil's financial and business establishment because its co-ownership by Grupo Globo and Grupo Folha and its Financial Times-equivalent positioning mean it frames economic statecraft through an investment-climate and market-efficiency lens — negative coverage of industrial policy or BNDES intervention does not necessarily mean the policy is failing, only that it is unpopular with the private sector and orthodox economists.

> Articles from **Poder360** about legislative and executive dynamics should be interpreted as data-driven Brasilia insider reporting — its centrist, nonpartisan orientation and proximity to the executive and legislative branches make it the most reliable single source for granular political intelligence (voting counts, decree publications, coalition arithmetic), though its rapid-cycle format means analytical depth is sacrificed for speed.

### Tier 2 Sources

> Articles from **Metropoles** about political crises and security events should be interpreted as fast-breaking Brasilia-sourced reporting — its centrist-populist orientation and massive digital reach mean it surfaces stories before they appear in broadsheets, but its analytical depth is shallower and its framing tends toward the dramatic. Useful for detection, less useful for interpretation.

> Articles from **JOTA** about judicial and regulatory developments should be interpreted as specialist legal analysis rather than political commentary — its nonpartisan, institutional orientation and specialist legal expertise distinguish it from general-news outlets covering the same STF rulings or regulatory changes. JOTA's analysis of constitutional boundaries on executive authority is the most technically rigorous available.

> Articles from **DefesaNet** about military affairs and defense procurement should be interpreted as reflecting the perspective of Brazil's defense establishment because its pro-military editorial orientation and specialist/technical audience mean it frames defense spending increases positively and military modernization uncritically — valuable for understanding what the defense community itself prioritizes but requiring calibration against civilian sources for assessments of civil-military dynamics.

> Articles from **Agencia Brasil** about government policy should be interpreted as official government communications — not independent journalism but the state's own wire service. What Agencia Brasil publishes represents the government's chosen public position. Useful as a primary source for declared posture, but its omissions are as significant as its coverage — what the government does not announce through Agencia Brasil is worth investigating.

> Articles from **gov.br** and **planalto.gov.br** should be interpreted as primary source government documents — press releases, presidential communications, and ministerial bulletins represent official positions, not journalistic analysis. Treat as evidence of declared posture, not as assessments of actual policy implementation.

> Articles from **Agencia Senado** and **Agencia Camara** should be interpreted as institutional legislative reporting — verbatim coverage of committee proceedings and floor votes, not editorial analysis. Essential for tracking what Congress actually did (treaty ratification votes, defense budget decisions, CRE hearings) rather than what journalists interpret Congress as doing.

> Articles from **The Brazilian Report** about any domain should be interpreted as high-quality English-language synthesis targeting an international professional audience — its analytical density is unmatched among English-language Brazil sources, but its framing reflects what international investors, diplomats, and journalists consider important, which may differ from domestic political priorities. Useful for rapid English-language context after Portuguese-language monitoring flags an event.

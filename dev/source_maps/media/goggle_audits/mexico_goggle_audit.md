# AUDIT SUMMARY: MEXICO

**Sources assessed:** 18 recommended + 5 excluded + 6 newly identified = 29 total
**Tier 1 (boost=3):** 5 sources
**Tier 2 (boost=2):** 8 sources
**Tier 3 (boost=1):** 6 sources
**Neutral (no rule):** 6 sources
**Discard:** 4 sources
**Overall assessment:** The curation prompt produced a strong whitelist with excellent investigative and opposition coverage — unusual for a Latin American country map. Key changes: (1) resolved redundancy between the two business dailies and four investigative outlets by differentiating tiers; (2) promoted government official sources for Layer 2 migration; (3) added missing wire services and think tank coverage; (4) flagged `eleconomista.com.mx` and `elpais.com` as blocked by Anthropic's crawler, which affects extraction even though Brave can still discover them.

---

## BOOST ASSIGNMENTS

### Tier 1 — `$boost=3`

**Reforma** | `reforma.com` | Type: `paper_of_record` | Status: `EXISTING`
- **Structural role:** Mexico's most-cited independent newspaper; the outlet most likely to break policy-relevant stories first. Functions as the agenda-setter for Mexico's political class.
- **Domain coverage:** Diplomatic alignment, Economic & technological statecraft, Domestic constraints, Security & defense autonomy
- **Reasoning:** Reforma is the closest thing Mexico has to a single indispensable source. Its paywall limits extraction (Diffbot may not get full text), but Brave indexes paywalled headlines for ranking. The pipeline needs Reforma surfacing first. Mexico Today (`mexicotoday.com`) provides free English summaries but should not be treated as a substitute — it's an access workaround, not an equivalent source.
- **Extraction note:** Hard paywall since 2003. Diffbot extraction likely partial. Consider `mexicotoday.com` as supplementary English-language access path (add at Tier 3).

**El Universal** | `eluniversal.com.mx` | Type: `paper_of_record` | Status: `EXISTING`
- **Structural role:** Highest-traffic news website in Mexico. Opposition-adjacent critical voice with the broadest topical coverage of any single outlet.
- **Domain coverage:** Diplomatic alignment, Security & defense autonomy, Domestic constraints, Economic & technological statecraft
- **Reasoning:** Metered paywall means most content is extractable. Covers all five analytical domains with original reporting. Carlos Loret de Mola's column presence means it surfaces opposition narratives alongside news reporting. Alongside Reforma, forms the essential broadsheet pair.

**El Financiero** | `elfinanciero.com.mx` | Type: `business_financial` | Status: `EXISTING`
- **Structural role:** Mexico's principal specialized business daily. Bloomberg partnership adds international data layer unavailable elsewhere in the Mexican press.
- **Domain coverage:** Economic & technological statecraft, Institutional engagement
- **Reasoning:** No other source covers USMCA/T-MEC dynamics, Banxico decisions, nearshoring, FDI screening, and critical minerals policy at this depth. Sole Tier 1 for economic statecraft. Metered paywall — mostly extractable.

**Proceso** | `proceso.com.mx` | Type: `political_specialist` → `security_defense` / `investigative` | Status: `EXISTING`
- **Structural role:** Mexico's premier investigative newsweekly. Fills the defense/security specialist gap in a country with no dedicated defense press. Unmatched institutional memory on military affairs and organized crime.
- **Domain coverage:** Security & defense autonomy, Domestic constraints
- **Reasoning:** The curation prompt typed this as `political_specialist` but its actual structural function is closer to `security_defense` + `investigative`. Proceso is where SEDENA/SEMAR leaks surface, where military human rights abuses are documented, and where cartel-state dynamics are analyzed with the deepest sourcing. In a media ecosystem with no Jane's equivalent, Proceso is the closest thing. Metered paywall — partial extraction likely.

**La Jornada** | `jornada.com.mx` | Type: `government_aligned` | Status: `EXISTING`
- **Structural role:** Mexico's primary government-aligned national daily. Functions as the preferred channel for 4T/Morena policy signaling, particularly on Latin American diplomatic solidarity and South-South engagement.
- **Domain coverage:** Diplomatic alignment, Institutional engagement, Domestic constraints
- **Reasoning:** Structural role outweighs journalistic quality per boost principles. La Jornada's front-page framing is a primary signal of government intent — what appears there reflects what the ruling coalition wants the public to see. Free and easily extractable, which increases its practical value. The pipeline needs this signal to understand the government's own narrative, and the dossier's interpretive context tells the LLM how to discount it.

---

### Tier 2 — `$boost=2`

**Milenio** | `milenio.com` | Type: `paper_of_record` | Status: `EXISTING`
- **Structural role:** Centrist national daily with strong northern/border regional coverage from its Monterrey base. Provides a pragmatic middle ground between El Universal and La Jornada.
- **Domain coverage:** Security & defense autonomy, Domestic constraints, Economic & technological statecraft
- **Reasoning:** Centrist positioning and Monterrey base make it uniquely valuable for border security, northern industrial corridor, and cross-border trade stories. Not Tier 1 because its original reporting rate is lower than El Universal or Reforma — it sometimes follows rather than breaks. But its regional depth and moderate editorial line earn a strong Tier 2.

**Animal Político** | `animalpolitico.com` | Type: `investigative` | Status: `EXISTING`
- **Structural role:** Mexico's leading data-journalism outlet with the country's only certified fact-checking unit (El Sabueso). Pioneer of fiscal oversight through data-driven reporting.
- **Domain coverage:** Domestic constraints, Institutional engagement
- **Reasoning:** Unique fact-checking and data-journalism capabilities that no other source replicates. USAID funding freeze risk is real — if grant funding collapses, output may decline. But current output justifies Tier 2. Not Tier 1 because domain coverage is narrower (primarily domestic constraints) and it doesn't break security/defense stories.

**Aristegui Noticias** | `aristeguinoticias.com` | Type: `investigative` | Status: `EXISTING`
- **Structural role:** Multi-platform investigative outlet (radio + digital) led by Carmen Aristegui. Breaks stories before print media through radio-first publishing. Cross-administration independence provides continuity.
- **Domain coverage:** Domestic constraints, Security & defense autonomy
- **Reasoning:** Radio-first model means Aristegui often publishes digital write-ups of stories that broke on air hours earlier — the pipeline captures the digital trail. Her cross-administration track record (fired under Calderón, broke Casa Blanca under Peña Nieto, critical of 4T) makes this a reliable independent voice. Tier 2 rather than 1 because domain coverage overlaps heavily with Proceso and El Universal.

**InSight Crime** | `insightcrime.org` | Type: `security_defense` | Status: `EXISTING`
- **Structural role:** The premier English-language analytical outlet for organized crime in Latin America. Academic rigor with journalistic accessibility. Original data (GameChangers, homicide roundups).
- **Domain coverage:** Security & defense autonomy
- **Reasoning:** No overlap with any domestic source — InSight Crime provides the analytical layer that daily Mexican outlets can't. Single-domain (security) but irreplaceable within it. English-language, which is both a strength (pipeline accessibility) and a limitation (won't capture domestic-language-only signals).

**Nexos** | `nexos.com.mx` | Type: `political_specialist` | Status: `EXISTING`
- **Structural role:** Mexico's premier intellectual/policy magazine. Where policy elites debate institutional design, constitutional reform, and the ideological underpinnings of 4T governance.
- **Domain coverage:** Domestic constraints, Institutional engagement
- **Reasoning:** Think tanks earn boost through depth, not speed. Nexos publishes the structural analysis the pipeline needs to interpret daily events — why Morena's judicial reform matters constitutionally, what INAI's dissolution means for transparency architecture. Tier 2 for analytical depth. Not Tier 1 because it doesn't break news and publishes less frequently than dailies.

**Excélsior** | `excelsior.com.mx` | Type: `paper_of_record` | Status: `EXISTING`
- **Structural role:** Fourth major national daily. Moderate, business-friendly. Multimedia integration (TV, radio, print) gives broad reach. Ownership transition after Vázquez Raña death in March 2025 introduces uncertainty.
- **Domain coverage:** Diplomatic alignment, Domestic constraints
- **Reasoning:** Fills the centrist-business editorial niche between El Universal's sharper criticism and La Jornada's government alignment. Free and extractable. Tier 2 rather than Tier 1 because it breaks fewer stories than El Universal or Reforma and its editorial orientation overlaps with Milenio. Ownership transition warrants monitoring — may shift tier in future audit.

**gob.mx (Government Portal)** | `gob.mx` | Type: `legislative_official` | Status: `NEW` — **LAYER 2 MIGRATION**
- **Structural role:** Central government web portal. Houses SEDENA/SEMAR bulletins, SRE press releases, presidential communications, and legislative records.
- **Domain coverage:** All five domains (official source)
- **Reasoning:** Primary fetch via Layer 2 direct polling. Goggle boost at Tier 2 as belt-and-suspenders fallback. Government press releases occasionally surface in Brave News Search. Includes subdomains: `sre.gob.mx`, `senado.gob.mx`, `diputados.gob.mx`.

**Latinus** | `latinus.us` | Type: `opposition_aligned` | Status: `EXISTING`
- **Structural role:** Primary vehicle for adversarial anti-4T investigations. Carlos Loret de Mola's platform for organized opposition narratives and anti-corruption reporting targeting the ruling party.
- **Domain coverage:** Domestic constraints
- **Reasoning:** Opposition-aligned sources earn Tier 2 minimum per boost principles — the pipeline needs to see domestic contestation. Latinus fills the unique niche of conducting adversarial investigations specifically targeting Morena. Single-domain but structurally essential. The FGR investigations against Loret are themselves a signal of government-media dynamics. Free and extractable.

---

### Tier 3 — `$boost=1`

**Semanario Zeta** | `zetatijuana.com` | Type: `regional` | Status: `EXISTING`
- **Structural role:** Irreplaceable for U.S.-Mexico border security dynamics in Baja California. Founded by an assassinated journalist; continues under threat.
- **Domain coverage:** Security & defense autonomy
- **Reasoning:** Narrow geographic and domain scope limits it to Tier 3, but within its niche (Tijuana/Baja California border security, cartel dynamics in the northwest), nothing else on the list competes. Site availability concerns (DDoS attacks) reduce reliability for pipeline dependency.

**Pie de Página** | `piedepagina.mx` | Type: `investigative` | Status: `EXISTING`
- **Structural role:** Human security coverage — forced disappearances, migration, indigenous rights, environmental conflict. Grassroots civil society perspective unavailable elsewhere.
- **Domain coverage:** Domestic constraints, Security & defense autonomy
- **Reasoning:** Fills a genuine gap on human security dimensions, but publication frequency and narrow scope limit pipeline utility. Tier 3 for supplementary depth on domestic constraints that the higher-tier investigative outlets (Proceso, Animal Político, Aristegui) don't cover from a grassroots perspective.

**Quinto Elemento Lab** | `quintoelab.org` | Type: `investigative` | Status: `EXISTING`
- **Structural role:** Slow-journalism investigative lab producing high-impact, periodic investigations (narco airstrips, cross-border financial tracing).
- **Domain coverage:** Security & defense autonomy, Domestic constraints
- **Reasoning:** Not a daily news source — publishes periodically. But when it publishes, the investigations are high-impact and often cited by other outlets. Tier 3 because the pipeline can't depend on regular output, but the boost ensures its periodic investigations surface when they appear.

**Mexico News Daily** | `mexiconewsdaily.com` | Type: `regional` → `aggregator` | Status: `EXISTING`
- **Structural role:** English-language aggregator/summarizer of Spanish-language Mexican media. Reflects what the English-speaking diplomatic and business community considers important.
- **Domain coverage:** Diplomatic alignment, Economic & technological statecraft, Domestic constraints (all via aggregation, not original reporting)
- **Reasoning:** Tier 3 rather than neutral because its editorial selection functions as a filter — it surfaces what matters to the English-speaking policy community. But it's an aggregator, not a primary source, so it can't earn Tier 2. Useful as a low-cost English-language signal detector.

**Mexico Today** | `mexicotoday.com` | Type: `aggregator` | Status: `NEW`
- **Structural role:** English-language summaries of Reforma reporting. Access workaround for Reforma's hard paywall.
- **Domain coverage:** Same as Reforma (via summary)
- **Reasoning:** Added as a Tier 3 supplement specifically because Reforma's hard paywall may limit Diffbot extraction. When the pipeline can't get full Reforma text, Mexico Today summaries provide a fallback signal. Not higher than Tier 3 because it's derivative, not original.

**Americas Quarterly** | `americasquarterly.org` | Type: `political_specialist` / `think_tank` | Status: `NEW`
- **Structural role:** Council of the Americas publication covering Latin American politics, economics, and policy. Provides the regional comparative lens that domestic outlets lack.
- **Domain coverage:** Diplomatic alignment, Economic & technological statecraft, Institutional engagement
- **Reasoning:** Think tank outlet that provides structural depth on Mexico's regional positioning — CELAC dynamics, Pacific Alliance trade, nearshoring in regional context. Not Mexico-specific (covers all of Latin America), so Tier 3. But when it publishes Mexico analysis, the quality is high and the comparative framing is unique.

---

### Neutral — no Goggle rule

**El Economista** | `eleconomista.com.mx` | Type: `business_financial` | Status: `EXISTING → DEMOTED TO NEUTRAL`
- **Why neutral:** Redundant with El Financiero at Tier 1 for economic statecraft coverage. Less editorially distinctive. **Also blocked by Anthropic's crawler** (`robots.txt` denial), which means extraction via pipeline tools will fail even if Brave surfaces it. Under the Goggle model, it can still appear organically for specific queries — no need to boost, but no need to discard either. If El Financiero becomes unavailable, this should be re-evaluated.

**El País México** | `elpais.com/mexico/` | Type: `paper_of_record` | Status: `EXISTING → DEMOTED TO NEUTRAL`
- **Why neutral:** Valuable for its Latin American comparative lens, but **blocked by Anthropic's crawler** (`elpais.com` in blocked domains list). Even if Brave surfaces El País results, the pipeline cannot extract full text. Its comparative-framing niche is partially filled by Americas Quarterly (newly added at Tier 3). Leave neutral — may surface organically and provide headlines even without full extraction.

**Televisa / N+ (Noticieros Televisa)** | `noticieros.televisa.com` | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Curation exclusion was correct under the hard-filter model — broadcast-first, web content is mostly video clips and wire rewrites. Under the Goggle model, no reason to actively discard. If Televisa breaks a major story (it has the largest broadcast audience in Mexico), Brave may surface it and the pipeline benefits from seeing it.

**TV Azteca (Azteca Noticias)** | `aztecnoticias.com.mx` | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Same logic as Televisa. Salinas Pliego's ownership introduces bias, but the pipeline's interpretive context can handle that. No reason to actively discard — leave at organic ranking.

**SDP Noticias** | `sdpnoticias.com` | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Aggregation + commentary, little original reporting. But pro-government columnists occasionally signal 4T talking points before they appear in official channels. Under Goggle model, organic ranking is appropriate — the source may surface serendipitously without displacing boosted sources.

**Infobae México** | `infobae.com/mexico/` | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Primarily aggregates wire copy, but its Argentine ownership gives it a different editorial selection algorithm than domestic aggregators. High traffic means Brave may rank it for specific queries. No reason to discard — organic ranking is fine.

---

### Discard — `$discard`

**El Chapucero** | `elchapucero.com` | Status: `CONFIRMED DISCARD`
- **Discard reasoning:** YouTube-based pro-4T commentary channel with no editorial structure, no original reporting, and no institutional accountability. Would actively displace higher-signal sources from top results. Pure commentary noise.

**Sin Censura** | `sincensura.com.mx` | Status: `CONFIRMED DISCARD`
- **Discard reasoning:** Same as El Chapucero — non-institutionalized YouTube commentary. No original reporting, pure political commentary that would waste result slots.

**El Deforma** | `eldeforma.com` | Status: `NEW DISCARD`
- **Discard reasoning:** Satire/parody news site (Mexico's "The Onion"). Headlines are designed to be mistaken for real news. Would inject noise and confuse the pipeline's event extraction.

**La Opinión** | `laopinion.com` | Status: `NEW DISCARD`
- **Discard reasoning:** Los Angeles-based Spanish-language daily targeting U.S. Latino audience. Not a Mexican domestic source — would inject U.S. Latino community news framed as Mexican news, displacing actual Mexican sources from results.

---

## STRUCTURAL COVERAGE CHECK

| Structural Role | Source(s) | Tier | Notes |
|---|---|---|---|
| Government leak channel | La Jornada | T1 | 4T/Morena preferred signaling outlet. Also watch for Proceso (leaks from security apparatus specifically) |
| Opposition voice | Latinus, El Universal | T2, T1 | Latinus is explicitly adversarial; El Universal is opposition-adjacent through columnists |
| Defence/security first-mover | Proceso, Aristegui Noticias | T1, T2 | No dedicated defence press — these outlets break security stories first. InSight Crime for analytical depth |
| Policy-elite discourse | Nexos, Reforma | T2, T1 | Nexos for intellectual/policy debate; Reforma for what decision-makers read daily |
| Domestic-language depth | All Spanish-language sources | T1–T3 | Mexico's media operates primarily in Spanish. English sources (InSight Crime, Mexico News Daily, Mexico Today, Americas Quarterly) are supplements, not substitutes |
| Official government source | gob.mx (+ subdomains) | T2 | **LAYER 2 MIGRATION** — primary fetch via direct polling. Goggle boost as fallback. Includes sre.gob.mx, senado.gob.mx, diputados.gob.mx |
| Analytical/think tank depth | Nexos, InSight Crime, Americas Quarterly | T2, T2, T3 | Nexos for domestic institutional analysis; InSight Crime for security; Americas Quarterly for regional positioning |
| Wire service (local bureau) | Reuters, AP News | Neutral | Not boosted in Goggle — wire copy is available organically. Reuters is blocked by Anthropic crawler but Brave can still surface it for discovery |

**Gaps identified:**
1. **Defence procurement** remains a structural blind spot — no source systematically tracks SEDENA/SEMAR procurement, military infrastructure projects (Felipe Ángeles airport operations, Tren Maya military management), or arms imports. Mitigated partly by Proceso's security beat and by Layer 2 polling of gob.mx bulletins, but this is a known weakness.
2. **State-level political dynamics** beyond Baja California (covered by Zeta) are underrepresented. Sources like El Norte (Monterrey, Grupo Reforma) and outlets in Guadalajara/Jalisco could add regional depth but were not included to avoid over-expanding the Goggle.
3. **Migration policy coverage** from the southern border perspective is thin — Pie de Página covers it from a human rights angle but no source systematically tracks Guatemala/Honduras/Belize border dynamics from the Mexican side.

---

## REDUNDANCY RESOLUTION

**Broadsheet cluster: El Universal + Reforma + Excélsior + Milenio**
All four are national dailies covering domestic politics and general news. Resolved by differentiating editorial roles: Reforma (Tier 1, agenda-setter, hardest paywall), El Universal (Tier 1, highest traffic, opposition-adjacent), Milenio (Tier 2, centrist + northern regional), Excélsior (Tier 2, business-moderate). Milenio and Excélsior drop below the broadsheet leaders because they break fewer stories and have more editorial overlap with each other than with the top two.

**Business press cluster: El Financiero + El Economista**
Both cover economic statecraft. El Financiero leads (Tier 1) due to Bloomberg partnership, sharper editorial voice, and more original analysis. El Economista drops to Neutral — redundant, and also blocked by Anthropic's crawler, making extraction unreliable.

**Investigative cluster: Proceso + Aristegui + Animal Político + Quinto Elemento + Pie de Página**
Five investigative/watchdog outlets is a lot, but each has a distinct niche. Proceso (Tier 1, security/defense specialist), Aristegui (Tier 2, multi-platform speed + cross-administration independence), Animal Político (Tier 2, data journalism + fact-checking), Quinto Elemento (Tier 3, periodic high-impact slow journalism), Pie de Página (Tier 3, human security grassroots). The pipeline benefits from investigative plurality in a country where journalist safety is compromised.

**International lens cluster: El País México + Americas Quarterly + InSight Crime**
Resolved by extraction reality: El País is blocked (Neutral), Americas Quarterly is new (Tier 3, regional comparative), InSight Crime is unique in its security niche (Tier 2). No redundancy — each covers different domains from different perspectives.

---

## QUERY CONFIGURATION

```
country: MX
search_lang: es
freshness: pw
```

**Multi-language notes:** Mexico's media ecosystem operates overwhelmingly in Spanish. English-language sources (InSight Crime, Mexico News Daily, Americas Quarterly) are supplements. Queries should run primarily in Spanish; a secondary English query cycle for security/defense topics would capture InSight Crime and international wire coverage. The pipeline's existing `languages.metadata: en` configuration handles this correctly.

**Localized query vocabulary validation:**

The curation prompt's vocabulary is solid. Notes:

- **Domain 1 (Diplomatic):** All terms valid. Add `"Sheinbaum política exterior"` and `"De la Fuente ONU"` as leader-specific patterns. `"CELAC"` is correct but declining in relevance — Mexico's CELAC engagement has cooled under Sheinbaum. Consider adding `"cumbre"` (summit) as a generic high-signal term.
- **Domain 2 (Security):** Strong list. Add `"García Harfuch"` (current SSPC secretary, the face of security policy). `"operativo"` is good but very high-frequency — will return noise. Consider pairing: `"operativo SEDENA"` or `"operativo Guardia Nacional"`. Add `"fentanilo"` (fentanyl) — the dominant frame for U.S.-Mexico security cooperation since 2024.
- **Domain 3 (Economic):** Excellent. `"nearshoring"` used as-is in Mexican press is correct. Add `"semiconductores"` (semiconductors) — increasingly relevant for nearshoring/tech statecraft. `"litio"` is correct but may need pairing with `"litio México"` to avoid Chilean lithium results.
- **Domain 4 (Institutional):** Valid. `"BRICS"` is relevant — Mexico has been publicly flirting with BRICS engagement under Sheinbaum. Add `"MIKTA"` if still active (Mexico-Indonesia-Korea-Turkey-Australia grouping). `"voto en la ONU"` is good.
- **Domain 5 (Domestic):** Strong. Add `"SCJN reforma"` (Supreme Court reform — the defining domestic institutional battle of 2025–2026). `"INE"` (National Electoral Institute) is missing — relevant for electoral oversight and Morena's institutional capture narrative. Add `"presupuesto"` (budget) for fiscal constraint stories.

**Stale/problematic terms:** None are stale. `"consulta popular"` may be declining in relevance as Morena's supermajority reduces the need for referendum mechanisms, but it's still a valid search term.

**Suggested topic query patterns:**

1. `Sheinbaum SEDENA presupuesto defensa` — Defence spending under Sheinbaum
2. `T-MEC aranceles Trump México` — USMCA/tariff friction with U.S.
3. `García Harfuch operativo fentanilo` — Security operations / fentanyl enforcement
4. `Morena reforma constitucional SCJN` — Judicial reform / institutional capture
5. `nearshoring inversión extranjera semiconductores México` — Nearshoring and tech investment

---

## GOGGLE FILE

```goggle
! name: MPM Mexico
! description: MPM pipeline source prioritization for Mexico — boosts high-signal sources, discards noise
! public: false
! author: MPM Pipeline

! --- Tier 1: Essential (boost=3) ---
$boost=3,site=reforma.com
$boost=3,site=eluniversal.com.mx
$boost=3,site=elfinanciero.com.mx
$boost=3,site=proceso.com.mx
$boost=3,site=jornada.com.mx

! --- Tier 2: Important (boost=2) ---
$boost=2,site=milenio.com
$boost=2,site=animalpolitico.com
$boost=2,site=aristeguinoticias.com
$boost=2,site=insightcrime.org
$boost=2,site=nexos.com.mx
$boost=2,site=excelsior.com.mx
$boost=2,site=gob.mx
$boost=2,site=latinus.us

! --- Tier 3: Supplementary (boost=1) ---
$boost=1,site=zetatijuana.com
$boost=1,site=piedepagina.mx
$boost=1,site=quintoelab.org
$boost=1,site=mexiconewsdaily.com
$boost=1,site=mexicotoday.com
$boost=1,site=americasquarterly.org

! --- Discard: Noise ---
$discard,site=elchapucero.com
$discard,site=sincensura.com.mx
$discard,site=eldeforma.com
$discard,site=laopinion.com
```

---

## INTERPRETIVE CONTEXT FOR DOSSIER

### Tier 1 Sources

> Articles from **Reforma** about any domain should be interpreted as Mexico's most independent and trusted broadsheet reporting — its editorial line is centre-right but its news coverage is consistently rigorous, and it is the outlet Mexican elites read first.

> Articles from **El Universal** about government policy should be interpreted as filtered through a consistently critical, opposition-adjacent editorial lens because the Ealy Ortiz family ownership and Carlos Loret de Mola's column presence align the outlet with anti-Morena narratives — valuable for surfacing government failures but likely to frame ambiguous events negatively for the ruling party.

> Articles from **El Financiero** about economic policy should be interpreted as reflecting the perspective of Mexico's business establishment because its Bloomberg partnership and centre-right business orientation mean it frames economic policy through an investment-climate lens — negative coverage of government economic intervention does not necessarily mean the policy is failing, only that it is unpopular with the private sector.

> Articles from **Proceso** about military and security affairs should be interpreted as Mexico's most authoritative investigative reporting on the security apparatus — its left-of-centre orientation means it frames military expansion critically, but its sourcing within SEDENA/SEMAR is deeper than any other outlet's.

> Articles from **La Jornada** about foreign policy and diplomatic initiatives should be interpreted as reflecting the 4T government's preferred framing because the outlet's financial dependence on government advertising (~1.3B pesos under AMLO) and left/pro-Morena editorial line mean its foreign policy coverage amplifies official narratives — particularly on Latin American solidarity and South-South engagement. What La Jornada chooses to front-page signals what the government wants amplified.

### Tier 2 Sources

> Articles from **Milenio** about security and border issues should be interpreted as centrist/pragmatic coverage shaped by its Monterrey base — its proximity to the northern border and Grupo Multimedios' regional roots give it better sourcing on border security and industrial corridor stories than Mexico City-based outlets.

> Articles from **Animal Político** about public spending and institutional accountability should be interpreted as data-driven fiscal oversight rather than political commentary — its El Sabueso fact-checking unit and data journalism methodology distinguish it from opinion-driven outlets.

> Articles from **Aristegui Noticias** about government misconduct should be interpreted as credible independent investigation with a left-of-centre editorial frame — Aristegui's track record of breaking major corruption stories across multiple administrations (PAN, PRI, Morena) demonstrates genuine independence, though her framing tends toward institutional critique.

> Articles from **InSight Crime** about organized crime and security operations should be interpreted as analytical rather than breaking-news coverage — its academic methodology and English-language framing make it the most reliable single source for understanding structural dynamics in Mexico's criminal landscape, though it may lag daily Mexican outlets on breaking events.

> Articles from **Nexos** about institutional reform and constitutional change should be interpreted as reflecting the perspective of Mexico's liberal-intellectual opposition — originally left-wing, it has become the primary forum for anti-4T institutional critique, making it essential for understanding elite opposition arguments but not representative of broader public sentiment.

> Articles from **Excélsior** about domestic politics should be interpreted with awareness of its ownership transition — the Vázquez Raña family's business interests historically produced moderate, business-friendly coverage, but the March 2025 ownership transition to Olegario Vázquez Aldír may shift editorial direction. Monitor for changes.

> Articles from **Latinus** about Morena/4T corruption should be interpreted as explicitly adversarial opposition journalism — Carlos Loret de Mola's outlet exists to conduct investigations targeting the ruling party, making it essential for surfacing opposition narratives but requiring calibration against sources with less partisan missions. The FGR's legal pressure on Latinus is itself a signal of government-media dynamics.

> Articles from **gob.mx** (and subdomains) should be interpreted as official government communications — not journalism but primary source material. Press releases, bulletins, and legislative records from this domain represent the government's chosen public position, which may differ from actual policy implementation.

# AUDIT SUMMARY: SWEDEN

**Sources assessed:** 17 recommended + 4 excluded + 3 newly identified = 24 total
**Tier 1 (boost=3):** 4 sources
**Tier 2 (boost=2):** 7 sources
**Tier 3 (boost=1):** 5 sources
**Neutral (no rule):** 5 sources
**Discard:** 3 sources
**Overall assessment:** The curation prompt produced a structurally sound whitelist with excellent coverage of Sweden's concentrated media duopoly (Bonnier/Schibsted) and public service broadcasters. Key changes: (1) promoted SVT as the uncontested Tier 1 anchor — it is both the most trusted and most extractable Swedish-language source; (2) migrated government sources (government.se, riksdagen.se) to Tier 2 as Layer 2 migration candidates; (3) applied non-English domestic boost premium to Swedish-language sources that are extractable; (4) **flagged 7 of 17 recommended domains as blocked by Anthropic's crawler** (aftonbladet.se, di.se, dn.se, expressen.se, omni.se, svd.se, sydsvenskan.se) — this is an exceptionally high block rate that fundamentally shapes tier assignments; (5) added missing structural roles for wire access, English-language analytical depth, and Nordic-comparative coverage; (6) downtiered think tanks per "depth not speed" principle.

---

## BOOST ASSIGNMENTS

### Tier 1 — `$boost=3`

**Sveriges Television (SVT)** | `svt.se` | Type: `paper_of_record` | Status: `EXISTING`
- **Structural role:** Sweden's most trusted and most-used news source across the political spectrum. Public broadcaster with statutory mandate covering all five analytical domains. The single indispensable source for the Swedish pipeline.
- **Domain coverage:** Diplomatic alignment, Security & defense autonomy, Economic & technological statecraft, Institutional engagement, Domestic constraints
- **Reasoning:** SVT is the uncontested top source for Sweden. Editorially independent, free to access, and extractable. Its statutory mandate means it covers government, defense, foreign policy, and parliamentary affairs systematically rather than selectively. In a country where 7 of the top 10 commercial media domains are blocked by Anthropic's crawler, SVT's accessibility makes it even more critical. Swedish-language primary output earns the non-English domestic premium.
- **Extraction note:** Free. No paywall. Swedish-language content is extractable.

**Sveriges Radio (SR)** | `sverigesradio.se` | Type: `paper_of_record` | Status: `EXISTING`
- **Structural role:** Public radio broadcaster. Ekot (news service) is Sweden's most important radio news program and frequently breaks major political stories before print media. P1 hosts in-depth foreign policy and security programming.
- **Domain coverage:** Diplomatic alignment, Domestic constraints, Security & defense autonomy
- **Reasoning:** SR's Ekot functions as a wire service for Swedish domestic politics — it breaks stories that DN, SvD, and SVT then follow up on. Radio Sweden provides English-language summaries, but the Swedish-language output is the primary signal. Free and extractable. Combined with SVT, the two public broadcasters form a reliable, extractable backbone for the Swedish pipeline in the face of massive commercial media blocking. Non-English domestic premium applies.
- **Extraction note:** Free. English summaries via Radio Sweden. Digital write-ups of radio-first stories are extractable.

**Dagens Nyheter (DN)** | `dn.se` | Type: `paper_of_record` | Status: `EXISTING` — **BLOCKED**
- **Structural role:** Sweden's prestige morning broadsheet. Sets elite discourse on foreign policy, NATO integration, and EU affairs. The paper Swedish decision-makers read first. "Independently liberal" editorial line (center-right by Swedish standards).
- **Domain coverage:** Diplomatic alignment, Security & defense autonomy, Economic & technological statecraft, Institutional engagement, Domestic constraints
- **Reasoning:** Structural role outweighs extraction difficulty. DN is Sweden's agenda-setting newspaper — what appears on DN's front page shapes the national conversation. Even though `dn.se` is **blocked by Anthropic's crawler**, Brave can still discover and index DN headlines for ranking purposes. The pipeline needs DN surfacing in results to detect story salience even if full-text extraction fails. Paywalled AND blocked — double extraction barrier — but irreplaceable structurally. Non-English domestic premium applies to the structural role even though extraction is impaired.
- **Extraction note:** Paywalled. **Blocked by Anthropic's crawler.** Brave indexes headlines but full-text extraction will fail. Pipeline must tolerate headline-only signal from this source.

**Aftonbladet** | `aftonbladet.se` | Type: `opposition_aligned` | Status: `EXISTING` — **BLOCKED**
- **Structural role:** Sweden's largest newspaper by readership. Editorial page is the primary barometer of Social Democratic and trade-union positions on defense, NATO, and migration. Owned by Schibsted with LO (trade union confederation) holding the editorial page.
- **Domain coverage:** Domestic constraints, Security & defense autonomy, Diplomatic alignment
- **Reasoning:** Opposition-aligned sources earn Tier 1 minimum when they are the dominant opposition voice and the largest newspaper by circulation. Aftonbladet is both. Its editorial page is the single most important channel for understanding Social Democratic positioning on NATO, defense spending, and migration policy — the three issues defining Swedish coalition politics. **Blocked by Anthropic's crawler**, but Brave still surfaces headlines. The pipeline cannot afford to miss the Social Democratic signal that Aftonbladet uniquely provides. Structural role outweighs extraction limitation.
- **Extraction note:** Free with ads. **Blocked by Anthropic's crawler.** Headline-only signal likely.

---

### Tier 2 — `$boost=2`

**Svenska Dagbladet (SvD)** | `svd.se` | Type: `paper_of_record` | Status: `EXISTING` — **BLOCKED**
- **Structural role:** Second national broadsheet. Strong on defense, security, and conservative-government perspective. "Independently moderate/conservative" editorial line aligned with the Moderate Party tradition (Schibsted).
- **Domain coverage:** Diplomatic alignment, Security & defense autonomy, Domestic constraints, Institutional engagement
- **Reasoning:** SvD's editorial orientation makes it the natural mirror to Aftonbladet — where Aftonbladet signals Social Democratic positions, SvD signals the conservative-liberal coalition's perspective. Strong defense and security beat. However, it is both paywalled and **blocked by Anthropic's crawler**, creating a double extraction barrier. Tier 2 rather than Tier 1 because DN already fills the prestige broadsheet role with similar domain coverage, and the extraction barrier is severe. Redundancy with DN reduces its marginal value.
- **Extraction note:** Paywalled. **Blocked by Anthropic's crawler.** Headline-only signal.

**Expressen** | `expressen.se` | Type: `paper_of_record` | Status: `EXISTING` — **BLOCKED**
- **Structural role:** Second tabloid. Aggressive political reporting with a liberal editorial line (Bonnier). Expressen's investigative team has broken several major political scandals.
- **Domain coverage:** Domestic constraints, Security & defense autonomy
- **Reasoning:** Expressen provides the liberal-right editorial complement to Aftonbladet's social-democratic line. Its investigative team is genuinely strong. However, **blocked by Anthropic's crawler** and partially redundant with DN (same Bonnier ownership, same "independently liberal" orientation). Tier 2 because its tabloid format means faster news cycles and broader readership than SvD, but the blocking and redundancy with DN prevent Tier 1.
- **Extraction note:** Free with ads. **Blocked by Anthropic's crawler.** Headline-only signal.

**Dagens Industri (DI)** | `di.se` | Type: `business_financial` | Status: `EXISTING` — **BLOCKED**
- **Structural role:** Sweden's leading financial daily. Essential for tracking defense-industrial procurement (Saab, BAE Hägglunds), sanctions impact, trade policy, and tech investment. The coverage gap assessment identified defense-trade journalism as a blind spot — DI is the closest approximation.
- **Domain coverage:** Economic & technological statecraft, Security & defense autonomy (defense industry)
- **Reasoning:** No other Swedish source covers economic statecraft with DI's depth. The defense-industrial coverage is structurally unique — Sweden's large defense-export sector (Saab, Bofors/BAE) generates significant economic statecraft signals that only DI tracks systematically. **Blocked by Anthropic's crawler** and paywalled, but the structural uniqueness in economic/defense-industrial coverage justifies Tier 2. Non-English domestic premium applies to the structural role.
- **Extraction note:** Paywalled. **Blocked by Anthropic's crawler.** Headline-only signal.

**Regeringskansliet (Government Offices)** | `government.se` | Type: `government_aligned` | Status: `EXISTING` — **LAYER 2 MIGRATION**
- **Structural role:** Central government web portal. Press releases, policy documents, ministerial speeches. Primary for tracking official posture on NATO, EU, defense strategy. English and Swedish content.
- **Domain coverage:** All five domains (official source)
- **Reasoning:** Primary fetch via Layer 2 direct polling. Goggle boost at Tier 2 as belt-and-suspenders fallback. Government press releases occasionally surface in Brave News Search. Bilingual (Swedish/English) output increases extraction reliability. Government sources = Layer 2 migration at Tier 2 per audit principles.
- **Extraction note:** Free. Bilingual. Extractable.

**Riksdag Official** | `riksdagen.se` | Type: `legislative_official` | Status: `EXISTING` — **LAYER 2 MIGRATION**
- **Structural role:** Parliamentary bills, committee reports, plenary protocols, voting records. The primary source for tracking legislative dynamics, including Tidö Agreement implementation and defense budget votes.
- **Domain coverage:** Institutional engagement, Domestic constraints
- **Reasoning:** Layer 2 migration candidate alongside government.se. Structured data (voting records, committee reports) is highly pipeline-friendly. Goggle boost at Tier 2 as fallback. Essential for tracking Riksdag dynamics that the se.yaml blind spot assessment identifies as critical (Tidö Agreement implementation).
- **Extraction note:** Free. Structured data. Extractable.

**FOI (Swedish Defence Research Agency)** | `foi.se` | Type: `security_defense` | Status: `EXISTING`
- **Structural role:** Europe's leading defense research institute. Publishes open analyses on Russian military capability, Baltic security, and strategic trends. Government research agency with non-partisan mandate.
- **Domain coverage:** Security & defense autonomy, Diplomatic alignment
- **Reasoning:** Think tanks earn boost through depth, not speed. FOI is not a think tank in the usual sense — it is a government research agency producing peer-reviewed defense analysis. Its analyses of Russian military capability and Baltic security dynamics are cited by NATO defense ministries. Tier 2 for irreplaceable analytical depth on security/defense. Bilingual (Swedish/English) output aids extraction. Not Tier 1 because it doesn't break news and publishes periodically.
- **Extraction note:** Free publications. Bilingual. Extractable.

**UI (Swedish Institute of International Affairs)** | `ui.se` | Type: `security_defense` → `think_tank` | Status: `EXISTING`
- **Structural role:** Sweden's oldest foreign policy institute. Publishes Internationella Studier and policy briefs on multilateral engagement. Independent think tank providing the analytical layer for diplomatic alignment and institutional engagement.
- **Domain coverage:** Diplomatic alignment, Institutional engagement
- **Reasoning:** Think tanks = depth not speed. UI fills the analytical gap on Sweden's multilateral positioning — EU policy, Nordic cooperation, and the post-neutrality diplomatic adjustment. Tier 2 for structural depth. Not Tier 1 because publication frequency is low and it doesn't break news. Bilingual output aids extraction.
- **Extraction note:** Free. Bilingual. Extractable.

---

### Tier 3 — `$boost=1`

**Altinget Sverige** | `altinget.se` | Type: `legislative_official` | Status: `EXISTING`
- **Structural role:** Granular coverage of Riksdag proceedings, committee work, and policy process. Modeled on the Danish original (Altinget Group). Fills the niche between daily media coverage and official riksdagen.se records.
- **Domain coverage:** Institutional engagement, Domestic constraints
- **Reasoning:** Unique legislative-process journalism that no other Swedish outlet provides at this depth. However, narrow domain scope (parliament-focused) and partial paywall limit it to Tier 3. Partially redundant with riksdagen.se for official records, but Altinget adds journalistic interpretation and committee-level sourcing. Non-English domestic premium applies but scope limits the tier.
- **Extraction note:** Free registration; some premium content. Swedish-language.

**Fokus** | `fokus.se` | Type: `political_specialist` | Status: `EXISTING`
- **Structural role:** Weekly news magazine (41 issues/year). In-depth political analysis and foreign policy features. Centrist, editorially unbound.
- **Domain coverage:** Diplomatic alignment, Domestic constraints
- **Reasoning:** Weekly publication cadence limits pipeline utility — by the time Fokus publishes, daily outlets have already covered the news. Its value is in analytical depth, not speed. Tier 3 because the analytical niche overlaps significantly with UI and FOI for foreign/security policy, and with DN/SvD for domestic political analysis. But its centrist, editorially unbound positioning provides a distinct analytical voice.
- **Extraction note:** Paywalled. Swedish-language. Not blocked.

**Kvartal** | `kvartal.se` | Type: `political_specialist` | Status: `EXISTING`
- **Structural role:** Online publication with podcasts and long-form societal journalism. Hosts security-policy debate and expert commentary. Politically independent.
- **Domain coverage:** Diplomatic alignment, Security & defense autonomy, Institutional engagement
- **Reasoning:** Kvartal's security-policy debate content fills a distinct niche — it hosts the expert commentary layer that sits between daily journalism and formal think tank publications. Tier 3 because it doesn't break news and its podcast-heavy format means the pipeline captures only the digital articles, not the full output. But when Kvartal publishes written security analysis, it's high-quality and well-sourced.
- **Extraction note:** Free. Swedish-language. Extractable.

**Göteborgs-Posten** | `gp.se` | Type: `regional` | Status: `EXISTING`
- **Structural role:** Western Sweden's paper of record. Gothenburg is Sweden's industrial and port hub — relevant for defense-industrial (Saab Gothenburg) and trade coverage. "Independently liberal" (Stampen Group).
- **Domain coverage:** Domestic constraints, Economic & technological statecraft
- **Reasoning:** Regional depth on Sweden's industrial heartland. Gothenburg is home to Saab's naval division, Volvo, and Sweden's largest port — making GP uniquely positioned for defense-industrial and trade stories. Tier 3 because its regional scope limits broad pipeline utility, but within its niche it's the only source. Paywalled but not blocked. Non-English domestic premium applies but scope limits tier.
- **Extraction note:** Paywalled. Swedish-language. Not blocked.

**The Stockholm Center for Eastern European Studies (SCEEUS)** | `sceeus.se` | Type: `think_tank` | Status: `NEW`
- **Structural role:** Swedish government-funded research center focused on Eastern Europe, Russia, and the post-Soviet space. Provides the analytical depth on Russia/Baltic security dynamics that is central to Sweden's strategic posture.
- **Domain coverage:** Diplomatic alignment, Security & defense autonomy
- **Reasoning:** Sweden's strategic posture is fundamentally shaped by Russia and Baltic security dynamics. SCEEUS fills the analytical gap on Russia-specific analysis that FOI covers from a military-technical angle but not from a political/diplomatic perspective. English-language output (many publications in English) aids extraction. Tier 3 because it's narrow (Eastern Europe focus) and publishes periodically, but the Russia/Baltic analytical niche is structurally essential for understanding Sweden's defense and diplomatic positioning.
- **Extraction note:** Free. Primarily English. Extractable.

---

### Neutral — no Goggle rule

**Omni** | `omni.se` | Type: `paper_of_record` (aggregator) | Status: `EXISTING → DEMOTED TO NEUTRAL` — **BLOCKED**
- **Why neutral:** Omni is an aggregator, not a primary source — it aggregates across the Swedish media spectrum. Useful for detecting story salience, but derivative by design. **Blocked by Anthropic's crawler**, which eliminates its practical value for the pipeline. Under the Goggle model, it can still appear organically, but there's no reason to boost an aggregator that can't be extracted. If Omni becomes unblocked, re-evaluate at Tier 3.

**Sydsvenskan** | `sydsvenskan.se` | Type: `regional` | Status: `EXISTING → DEMOTED TO NEUTRAL` — **BLOCKED**
- **Why neutral:** Southern Sweden/Malmö paper of record covering the Oresund region and Danish-Swedish cooperation. Regionally valuable, but paywalled AND **blocked by Anthropic's crawler** — double extraction barrier. Its regional niche (Oresund/Baltic) is partially covered by GP (western Sweden industry) and by the national broadsheets for major Danish-Swedish security stories. Exclusions default to Neutral, not Discard.

**ETC** | `etc.se` | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Left-wing daily valuable for tracking Green/Left critique of the Kristersson government's defense and migration policies. Narrow readership and limited foreign-policy depth justify exclusion from the curated list, but under the Goggle model, no reason to actively discard. If ETC surfaces organically for a query about Green Party opposition to NATO spending, the pipeline benefits from seeing it.

**The Local Sweden** | `thelocal.se` | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** English-language expatriate outlet. Lacks depth and sourcing for operational OSINT, but provides accessible English-language summaries of Swedish domestic news. Under the Goggle model, organic ranking is appropriate — no reason to discard a benign English-language source that might surface for specific queries.

**Arbetet** | `arbetet.se` | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** LO trade-union news outlet. Redundant with Aftonbladet's editorial line for foreign/security coverage, but useful for labor-market policy signals that occasionally intersect with economic statecraft (e.g., strike actions affecting defense-industrial production). Organic ranking is appropriate.

---

### Discard — `$discard`

**Nya Dagbladet** | `nyadagbladet.se` | Status: `CONFIRMED DISCARD`
- **Discard reasoning:** Right-populist alternative media outlet associated with conspiracy theories and disinformation. No editorial accountability, no original reporting of the kind the pipeline needs. Would actively displace higher-signal sources from top results. Pure noise for strategic-posture analysis.

**Samnytt** | `samnytt.se` | Status: `CONFIRMED DISCARD`
- **Discard reasoning:** Right-populist/alternative media. Anti-immigration framing without original sourcing or institutional accountability. Relevant only for domestic radicalization monitoring, which is outside the scope of the MPM pipeline's strategic-posture analysis. Would inject noise.

**Fria Tider** | `friatider.se` | Status: `NEW DISCARD`
- **Discard reasoning:** Far-right alternative media site with a history of publishing misleading content. No editorial structure, no original reporting on defense/foreign policy. Would displace legitimate sources from results. Discarding prevents contamination of the pipeline's source ranking.

---

## STRUCTURAL COVERAGE CHECK

| Structural Role | Source(s) | Tier | Notes |
|---|---|---|---|
| Government signaling channel | SVT, SR, government.se | T1, T1, T2 | Sweden's government communicates primarily through public broadcasters and government.se. Unlike Mexico's La Jornada model, Sweden has no government-aligned commercial newspaper — the signal comes through official channels and public service media |
| Opposition voice | Aftonbladet | T1 | Aftonbladet's editorial page is the primary vehicle for Social Democratic opposition. **Blocked** — headline-only signal. ETC (Neutral) provides Green/Left opposition signal organically |
| Coalition-government perspective | SvD, Expressen | T2, T2 | Both "independently liberal/moderate" outlets aligned with the governing coalition's ideological base. Both **blocked** — headline-only signal |
| Defence/security first-mover | SVT, SR, FOI | T1, T1, T2 | SVT/SR break defense stories first via broadcast; FOI provides analytical depth. No dedicated defense press in Sweden — the coverage gap assessment notes this. DI (T2, blocked) covers defense-industrial procurement |
| Defence-industrial coverage | DI, GP | T2, T3 | DI for national defense industry; GP for Gothenburg/Saab naval. Both fill the identified gap in defense-trade journalism. DI is **blocked** |
| Policy-elite discourse | DN, SvD, Fokus | T1, T2, T3 | DN is what Swedish elites read. Both DN and SvD are **blocked** — Fokus (not blocked, paywalled) provides a fallback analytical voice |
| Domestic-language depth | SVT, SR, Aftonbladet, DN, SvD, Expressen, DI, GP, Altinget, Fokus, Kvartal | T1–T3 | Swedish-language sources dominate. Non-English domestic boost premium applies. Critical that the two extractable Tier 1 sources (SVT, SR) are both Swedish-language |
| Official government source | government.se, riksdagen.se | T2, T2 | **LAYER 2 MIGRATION** — primary fetch via direct polling. Goggle boost as fallback. Bilingual content aids extraction |
| Analytical/think tank depth | FOI, UI, SCEEUS | T2, T2, T3 | FOI for defense-military analysis; UI for foreign policy/multilateral; SCEEUS for Russia/Eastern Europe. Three distinct analytical niches with minimal overlap |
| Wire service (local bureau) | Reuters, AP News, France24 | Neutral | Listed in se.yaml as wire sources. Not boosted — wire copy is available organically. Reuters is **blocked** by Anthropic's crawler |
| Nordic-comparative lens | Altinget Sverige | T3 | Danish Altinget Group's Swedish edition provides Nordic-comparative perspective on parliamentary process. Unique structural role |

**Gaps identified:**
1. **Defence-trade journalism** remains a structural blind spot — Sweden has a major defense-export sector (Saab, BAE Hägglunds, Bofors) but no standalone defense-trade publication. DI and FOI together approximate this, but DI is blocked. GP provides partial Gothenburg/Saab coverage.
2. **Extraction crisis:** 7 of 17 recommended sources are blocked by Anthropic's crawler, including the two top broadsheets (DN, SvD), both tabloids (Aftonbladet, Expressen), the financial daily (DI), the top aggregator (Omni), and one regional paper (Sydsvenskan). The pipeline for Sweden is heavily dependent on the two public broadcasters (SVT, SR) and official government sources for reliable full-text extraction. This is a known architectural constraint.
3. **Sami and minority-language media** covering Arctic sovereignty and indigenous-rights issues relevant to Nordic defense cooperation remain outside the pipeline scope, consistent with the coverage gap assessment.
4. **Sweden Democrats signaling** — despite SD's informal influence through the Tidö Agreement, there is no SD-aligned media outlet on the list. SD communicates primarily through social media and Riksdag interventions (captured via riksdagen.se). Monitoring SD positioning relies on SVT/SR coverage and Riksdag records.

---

## REDUNDANCY RESOLUTION

**Broadsheet cluster: DN + SvD**
Both are national broadsheets covering all five domains. Resolved by editorial orientation: DN (Tier 1, "independently liberal," Bonnier, agenda-setter) leads because it is the prestige paper and sets elite discourse. SvD (Tier 2, "independently moderate/conservative," Schibsted) provides the conservative-coalition perspective that DN's liberal line doesn't fully capture. Both are blocked — the tier differential reflects DN's greater structural importance, not extraction advantage.

**Tabloid cluster: Aftonbladet + Expressen**
Both are mass-circulation tabloids with strong political coverage. Resolved by structural role: Aftonbladet (Tier 1, social-democratic, opposition-aligned) is structurally essential as the opposition voice and largest newspaper by readership. Expressen (Tier 2, liberal, Bonnier) provides the liberal-right complement but overlaps editorially with DN (same ownership group, same "independently liberal" label). Aftonbladet's unique opposition-signaling role earns it the tier advantage.

**Public broadcaster cluster: SVT + SR**
Not redundant — SVT is television-first (visual, breaking news, longer features) while SR is radio-first (Ekot breaking stories, P1 in-depth programming). Both are extractable and free, making them the pipeline's most reliable Swedish-language sources. Both earn Tier 1 because together they form the extractable backbone of the Swedish pipeline.

**Think tank cluster: FOI + UI + SCEEUS**
Three think tanks/research institutes, each with a distinct analytical niche: FOI (defense-military technical analysis), UI (foreign policy/multilateral engagement), SCEEUS (Russia/Eastern Europe political analysis). No redundancy — each covers different aspects of Sweden's strategic posture. FOI and UI at Tier 2 for established institutional depth; SCEEUS at Tier 3 as a newer, narrower addition.

**Regional cluster: GP + Sydsvenskan**
Both are regional papers. GP (Tier 3, Gothenburg, defense-industrial) is extractable and covers Sweden's industrial heartland. Sydsvenskan (Neutral, Malmö, blocked) is demoted because it's blocked AND its Oresund/Baltic niche is partially covered by national sources for major stories. No redundancy at the tier level.

---

## QUERY CONFIGURATION

```
country: SE
search_lang: sv
freshness: pw
```

**Multi-language notes:** Sweden's media ecosystem operates overwhelmingly in Swedish. English-language content is available from government.se, FOI, UI, and SCEEUS, but the primary signal lives in Swedish-language sources. Queries should run primarily in Swedish (`sv`); a secondary English query cycle for security/defense and think tank coverage would capture FOI, UI, SCEEUS, and international wire output. The pipeline's existing `languages.metadata: en` configuration handles this correctly. The non-English domestic boost premium is critical for Sweden — the most important sources publish primarily in Swedish.

**Localized query vocabulary validation:**

The curation prompt's vocabulary is strong. Notes:

- **Domain 1 (Diplomatic):** All terms valid. `"alliansfrihet"` (non-alignment) remains historically important but is now obsolete as a policy descriptor since NATO accession — retain for historical analysis but add `"NATO-medlemskap"` (NATO membership) and `"NATO-integration"` as current-state terms. Add `"Kristersson utrikespolitik"` and `"Malmer Stenergard"` as leader-specific patterns. Add `"arktisk politik"` (Arctic policy) — increasingly relevant for Nordic defense cooperation.
- **Domain 2 (Security):** Excellent list. Add `"Gotland"` — the strategically critical island is a key signal term for Baltic defense. Add `"Pål Jonson"` (Defense Minister) as a person-specific term. `"totalförsvar"` is the defining concept for Sweden's defense posture. Add `"NATO-övning"` (NATO exercise) and `"Aurora"` (major Swedish military exercise series). Add `"ubåtsjakt"` (submarine hunting) — perennial Swedish security concern.
- **Domain 3 (Economic):** Valid. Add `"Saab"` and `"försvarsexport"` (defense export) — Sweden's defense-industrial sector is a major economic statecraft vector. Add `"grön omställning"` (green transition) alongside `"energiomställning"`. Add `"Wallenberg"` — the family's industrial sphere (~40% of Stockholm Stock Exchange per se.yaml) makes it a relevant economic signal term.
- **Domain 4 (Institutional):** Valid. Add `"Tidöavtalet"` (Tidö Agreement) — the defining institutional arrangement of the current government, where SD exercises informal policy influence. Add `"EU-ordförandeskap"` (EU presidency) for historical reference and `"Arktiska rådet"` (Arctic Council). `"biståndsbudget"` is correct and increasingly contested.
- **Domain 5 (Domestic):** Strong. Add `"Tidöavtalet"` here as well — it is the central domestic constraint mechanism. Add `"Åkesson"` and `"Sverigedemokraterna"` (Sweden Democrats) as essential actor-specific terms. Add `"migrationsdebatten"` (migration debate) — the dominant frame for Swedish domestic politics. Add `"kärnkraft"` (nuclear power) — a coalition-defining policy issue.

**Stale/problematic terms:** `"alliansfrihet"` is historically important but no longer describes current policy. Retain but deprioritize in query construction. All other terms remain current.

**Suggested topic query patterns:**

1. `Kristersson NATO totalförsvar försvarsbudget` — Defense spending and NATO integration under Kristersson
2. `Tidöavtalet Sverigedemokraterna migrationspolitik` — Tidö Agreement implementation and SD influence
3. `Saab försvarsexport försvarsindustri` — Defense-industrial procurement and export
4. `Malmer Stenergard utrikespolitik EU-samarbete` — Foreign Minister and EU/diplomatic positioning
5. `Gotland militärt samarbete NATO-övning` — Gotland military buildup and NATO exercises
6. `Riksbank ekonomisk politik sanktioner` — Central bank policy and sanctions impact

---

## GOGGLE FILE

```goggle
! name: MPM Sweden
! description: MPM pipeline source prioritization for Sweden — boosts high-signal sources, discards noise
! public: false
! author: MPM Pipeline

! --- Tier 1: Essential (boost=3) ---
$boost=3,site=svt.se
$boost=3,site=sverigesradio.se
$boost=3,site=dn.se
$boost=3,site=aftonbladet.se

! --- Tier 2: Important (boost=2) ---
$boost=2,site=svd.se
$boost=2,site=expressen.se
$boost=2,site=di.se
$boost=2,site=government.se
$boost=2,site=riksdagen.se
$boost=2,site=foi.se
$boost=2,site=ui.se

! --- Tier 3: Supplementary (boost=1) ---
$boost=1,site=altinget.se
$boost=1,site=fokus.se
$boost=1,site=kvartal.se
$boost=1,site=gp.se
$boost=1,site=sceeus.se

! --- Discard: Noise ---
$discard,site=nyadagbladet.se
$discard,site=samnytt.se
$discard,site=friatider.se
```

---

## INTERPRETIVE CONTEXT FOR DOSSIER

### Tier 1 Sources

> Articles from **SVT** about any domain should be interpreted as Sweden's most trusted news reporting — its public service mandate requires impartiality across the political spectrum, making it the closest thing to a neutral baseline in Swedish media. SVT's editorial decisions about what to cover and how prominently signal national salience. It does not have a partisan editorial page.

> Articles from **Sveriges Radio (SR/Ekot)** about government policy and security affairs should be interpreted as independent public service journalism with a radio-first publication model — Ekot frequently breaks stories before print media, meaning SR digital write-ups may be the first text signal of developments that SVT and the broadsheets then follow up on. Like SVT, SR has no partisan editorial line.

> Articles from **Dagens Nyheter** about foreign policy and defense should be interpreted as reflecting Sweden's liberal-establishment perspective because its "independently liberal" editorial line aligns with the internationalist, pro-EU, pro-NATO center-right — DN frames Sweden's post-neutrality positioning positively and is skeptical of populist/SD influence on policy. DN's editorial page is distinct from its news coverage; the news reporting is professional and sourced, but editorial framing on foreign policy tilts toward liberal internationalism.

> Articles from **Aftonbladet** about defense spending, NATO policy, and migration should be interpreted as reflecting Social Democratic and trade-union positions because the LO trade union confederation controls its editorial page and the outlet's "independent social-democratic" orientation means it frames defense spending increases, NATO commitments, and restrictive migration policy through a center-left lens — critical coverage of the Kristersson government's security posture does not necessarily mean the policy is failing, but rather that it conflicts with Social Democratic priorities. Aftonbladet's editorial page is the single best signal of where the Social Democrats will position themselves on security and foreign policy.

### Tier 2 Sources

> Articles from **Svenska Dagbladet** about defense and security policy should be interpreted as reflecting the conservative-moderate establishment perspective because its "independently moderate/conservative" editorial line aligns with the Moderate Party tradition — SvD is where the governing coalition's ideological base sees its worldview reflected, particularly on defense spending, law enforcement, and transatlantic alignment.

> Articles from **Expressen** about political scandals and security affairs should be interpreted as aggressive, investigative tabloid journalism with a liberal editorial orientation — its Bonnier ownership and "independently liberal" label mean it shares DN's ideological space but operates at tabloid speed. Expressen breaks political scandals before the broadsheets due to its faster news cycle.

> Articles from **Dagens Industri** about defense procurement, trade policy, and economic statecraft should be interpreted as reflecting Sweden's business establishment perspective — its coverage of Saab contracts, sanctions impact, and trade policy is framed through an investment-climate and industrial-competitiveness lens. Negative DI coverage of government economic intervention signals business-community concern, not necessarily policy failure.

> Articles from **government.se** and **riksdagen.se** should be interpreted as official communications — not journalism but primary source material. Press releases, ministerial speeches, committee reports, and voting records represent the government's and parliament's chosen public positions, which may differ from actual policy dynamics. These sources are essential for establishing the official baseline against which journalistic coverage can be calibrated.

> Articles from **FOI** about military capability and Baltic security should be interpreted as authoritative government-funded defense research — FOI analyses are peer-reviewed and cited across NATO defense establishments. Its assessments of Russian military capability and Baltic security dynamics represent the closest thing to a consensus Swedish defense-analytical view. FOI does not editorialize; its conclusions reflect technical analysis, not political positioning.

> Articles from **UI (Swedish Institute of International Affairs)** about multilateral engagement and diplomatic positioning should be interpreted as independent foreign-policy analysis from Sweden's oldest international affairs institute — UI provides the structural context for understanding why Sweden takes particular positions in EU, UN, and Nordic forums. Its analysis tends toward the internationalist mainstream, reflecting Sweden's traditional multilateral orientation.

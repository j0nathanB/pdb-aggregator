# AUDIT SUMMARY: AUSTRALIA

**Sources assessed:** 17 recommended + 5 excluded + 4 newly identified = 26 total
**Tier 1 (boost=3):** 4 sources
**Tier 2 (boost=2):** 8 sources
**Tier 3 (boost=1):** 5 sources
**Neutral (no rule):** 6 sources
**Discard:** 3 sources
**Overall assessment:** The curation prompt produced an unusually strong whitelist, reflecting Australia's deep bench of open-access think tank platforms and transparent parliamentary infrastructure. Key changes: (1) resolved redundancy among the four think tank platforms (Lowy, ASPI, USSC, East Asia Forum) by differentiating tiers based on domain coverage and structural role; (2) promoted government official sources (DFAT, Defence, Parliament) for Layer 2 migration at Tier 2; (3) flagged three critical blocked domains — `abc.net.au`, `theaustralian.com.au`, and `theguardian.com` — which removes three of the top five media sources from extraction, dramatically increasing pipeline dependence on think tank platforms and SBS; (4) added missing Pacific Islands and regional lens sources to address the coverage gap identified in the source map. Australia is an English-primary country, so no non-English domestic boost applies.

---

## BOOST ASSIGNMENTS

### Tier 1 — `$boost=3`

**The Lowy Institute — The Interpreter** | `lowyinstitute.org` | Type: `think_tank` | Status: `EXISTING`
- **Structural role:** Australia's single most important open-access source for foreign policy analysis. Daily publication cadence with direct policymaker readership and contribution. Produces the Lowy Institute Poll (benchmark public opinion dataset) and the Asia Power Index.
- **Domain coverage:** Diplomatic alignment, Institutional engagement, Security & defense autonomy
- **Reasoning:** In a media landscape where three of the top five outlets are blocked by Anthropic's crawler, The Interpreter becomes the pipeline's primary high-signal source. Fully free, clean HTML, RSS available. Think tanks normally earn boost through depth not speed, but The Interpreter publishes daily and is read directly by policymakers — it functions as quasi-media, not a slow-publishing academic journal. Former DFAT officials and regional experts contribute, making it the closest thing to insider analysis that's openly accessible.
- **Extraction note:** Fully free. No paywall. RSS feed available. Clean HTML structure ideal for automated ingestion.

**ASPI — The Strategist** | `aspistrategist.org.au` | Type: `think_tank` / `security_defense` | Status: `EXISTING`
- **Structural role:** Australia's premier defence and security analytical platform. Daily publication. The International Cyber Policy Centre is a global leader on tech-statecraft (disinformation, critical minerals, supply chains). Partially Defence-funded, which shapes but does not discredit its editorial orientation.
- **Domain coverage:** Security & defense autonomy, Economic & technological statecraft (cyber, critical tech)
- **Reasoning:** No other Australian source covers defence capability, cyber policy, critical technology, and Indo-Pacific security architecture at this depth and cadence. ASPI reports are cited in parliamentary debate and allied-government policy documents. With The Australian and ABC both blocked, ASPI becomes the primary extractable source for defence posture analysis. Tier 1 because it fills a structural role (defence specialist) that no remaining extractable media outlet covers at comparable depth.
- **Extraction note:** Fully free. RSS feed available. Reports downloadable as PDF.

**Australian Financial Review (AFR)** | `afr.com` | Type: `paper_of_record` / `business_financial` | Status: `EXISTING`
- **Structural role:** Australia's newspaper of record for policy-elite discourse on defence, foreign affairs, and economic statecraft. Andrew Tillett (Foreign Affairs & Defence correspondent) is the single most important beat reporter for pipeline-relevant coverage.
- **Domain coverage:** Diplomatic alignment, Economic & technological statecraft, Domestic constraints
- **Reasoning:** Primary venue for breaking trade policy, sanctions, AUKUS procurement, and economic statecraft news. Elite readership ensures policy signals surface here first. Hard paywall limits extraction (~86% gated), but Brave indexes headlines for ranking, and the pipeline needs AFR surfacing at the top even for headline-only signal. The domain `afr.com` (not `afr.com.au`) is NOT on the blocked domains list, though paywall is the practical extraction constraint.
- **Extraction note:** Hard paywall. Diffbot extraction likely partial. Factiva access with 72-hour embargo. RSS feeds carry headlines and leads.

**SBS News** | `sbs.com.au` | Type: `public_broadcaster` | Status: `EXISTING`
- **Structural role:** Public multicultural broadcaster with unique diaspora-community perspective on foreign policy. Mandarin and Arabic bulletins are early indicators of domestic constraint dynamics unavailable elsewhere.
- **Domain coverage:** Diplomatic alignment, Domestic constraints (diaspora/migration)
- **Reasoning:** Promoted from its apparent mid-list position to Tier 1 for a specific structural reason: with ABC blocked and Guardian blocked, SBS is the only remaining extractable free-access general news broadcaster. Its multicultural mandate gives it a unique structural role no other source fills — how diaspora communities interpret foreign policy shifts (e.g., China-Australia relations through a Chinese-Australian lens). Fully free and easily extractable.
- **Extraction note:** Fully free. English content fully accessible. Language-specific bulletins via SBS On Demand.

---

### Tier 2 — `$boost=2`

**United States Studies Centre (USSC)** | `ussc.edu.au` | Type: `think_tank` | Status: `EXISTING`
- **Structural role:** Indispensable for tracking granular US-Australia alliance dynamics — AUKUS implementation, AUSMIN outcomes, force posture, and tariff/trade friction with Washington.
- **Domain coverage:** Diplomatic alignment (US alliance), Security & defense autonomy (AUKUS), Economic & technological statecraft
- **Reasoning:** Think tanks earn boost through depth not speed. USSC publishes research reports and policy briefs with direct relevance to alliance management. Tier 2 rather than Tier 1 because its domain coverage is narrower (US-alliance focused) and it publishes less frequently than Lowy or ASPI. But within its niche, nothing else on the list competes.
- **Extraction note:** Fully free. All publications available online.

**East Asia Forum** | `eastasiaforum.org` | Type: `think_tank` / `academic` | Status: `EXISTING`
- **Structural role:** Peer-reviewed short-form analysis on Asia-Pacific economics, trade, and regional institutions. Essential for tracking Australia's position within RCEP, APEC, ASEAN engagement, and supply-chain diversification.
- **Domain coverage:** Economic & technological statecraft, Institutional engagement, Diplomatic alignment
- **Reasoning:** Tier 2 for analytical depth on trade and regional governance — a domain where ASPI (security-focused) and Lowy (broader foreign policy) are thinner. Directed by Peter Drysdale, a foundational figure in Australian trade policy scholarship. Not Tier 1 because it doesn't break news and its Australia-specific coverage is diluted by broader Asia-Pacific scope.
- **Extraction note:** Fully free. Also publishes East Asia Forum Quarterly (via ANU Press).

**Australian Institute of International Affairs (AIIA) — Australian Outlook** | `internationalaffairs.org.au` | Type: `think_tank` | Status: `EXISTING`
- **Structural role:** Weekly "This Week in Australian Foreign Affairs" digest provides structured, no-commentary summary of the week's foreign affairs events — ideal for pipeline validation and gap-checking. Contributor base includes retired diplomats and early-career DFAT officers.
- **Domain coverage:** Diplomatic alignment, Institutional engagement, Security & defense autonomy
- **Reasoning:** The weekly digest alone justifies Tier 2 — it functions as a structured audit of what the pipeline should have captured. Creative Commons licensing. Tier 2 rather than Tier 1 because it doesn't break news and its analysis is less frequent and less influential than Lowy or ASPI.
- **Extraction note:** Fully free. Creative Commons 3.0 BY-NC-ND.

**Defence Connect** | `defenceconnect.com.au` | Type: `security_defense` / `trade_press` | Status: `EXISTING`
- **Structural role:** Highest-volume Australian outlet dedicated to defence procurement and industrial base news. Tracks contracts, capability milestones, and industry partnerships signaling defence-autonomy posture (GWEO, AUKUS Pillar II).
- **Domain coverage:** Security & defense autonomy, Economic & technological statecraft (procurement)
- **Reasoning:** Fills the defence-industry trade press niche. With The Australian blocked, Defence Connect becomes the primary extractable source for defence procurement breaking news (as distinct from ASPI's analytical coverage). Tier 2 for structural importance to the security/defence autonomy domain.
- **Extraction note:** Free registration required for some content. Newsletter available.

**Department of Foreign Affairs and Trade (DFAT)** | `dfat.gov.au` | Type: `government_official` | Status: `EXISTING` — **LAYER 2 MIGRATION**
- **Structural role:** Joint statements, ministerial media releases, treaty texts, sanctions listings, and travel advisories are the raw signal layer for diplomatic alignment tracking.
- **Domain coverage:** Diplomatic alignment, Institutional engagement, Economic & technological statecraft
- **Reasoning:** Primary fetch via Layer 2 direct polling. Goggle boost at Tier 2 as belt-and-suspenders fallback. Government sources = Layer 2 migration at Tier 2 per audit principles.
- **Extraction note:** Fully free. Media releases page and minister's page are key entry points.

**Department of Defence** | `defence.gov.au` | Type: `government_official` | Status: `EXISTING` — **LAYER 2 MIGRATION**
- **Structural role:** National Defence Strategy, Defence Strategic Review, Integrated Investment Program, and exercise/operation announcements are foundational documents.
- **Domain coverage:** Security & defense autonomy
- **Reasoning:** Primary fetch via Layer 2 direct polling. Goggle boost at Tier 2 as belt-and-suspenders fallback. Includes ADF operational deployments, bilateral exercise announcements, and force posture updates.
- **Extraction note:** Fully free. Key publications section and media releases.

**Parliament of Australia / OpenAustralia** | `aph.gov.au` | Type: `legislative_official` | Status: `EXISTING` — **LAYER 2 MIGRATION**
- **Structural role:** Senate Estimates hearings compel DFAT, Defence, and Trade officials to answer on the record. This is where classified policy positions become public. OpenAustralia provides a searchable mirror with keyword alerts.
- **Domain coverage:** All five domains — direct government positioning
- **Reasoning:** Primary fetch via Layer 2 direct polling (aph.gov.au for Hansard, openaustralia.org.au for structured search). Goggle boost at Tier 2 as fallback. Hansard data is Creative Commons licensed.
- **Extraction note:** Fully free. OpenAustralia API available. Keyword alerts configurable.

**The Conversation — Australia** | `theconversation.com` | Type: `academic` | Status: `EXISTING`
- **Structural role:** High-volume, freely licensed academic expert commentary across all five domains. Rapid turnaround on policy events. Sentiment layer for academic/expert framing of strategic posture debates.
- **Domain coverage:** All five domains — academic expert commentary
- **Reasoning:** Tier 2 for volume and breadth. CC BY-ND licensing and RSS feeds make it ideal for automated ingestion. Not Tier 1 because it's commentary on events, not original reporting or first-mover analysis — it follows rather than leads. But with ABC and Guardian blocked, The Conversation becomes a more important free-access general-coverage source.
- **Extraction note:** Fully free. Creative Commons licensed. RSS feeds.

---

### Tier 3 — `$boost=1`

**Australian Defence Magazine (ADM)** | `australiandefence.com.au` | Type: `security_defense` / `trade_press` | Status: `EXISTING`
- **Structural role:** Complements Defence Connect with deeper technical and acquisition reporting. Over 30 years of institutional knowledge. ADM Today e-newsletter provides structured intelligence on capability programs.
- **Domain coverage:** Security & defense autonomy (acquisition, sustainment, capability)
- **Reasoning:** Tier 3 rather than Tier 2 because it overlaps significantly with Defence Connect (both are defence trade press). Redundancy reduces boost. ADM provides deeper technical depth but lower publication frequency. The boost ensures its periodic analysis surfaces when it appears.
- **Extraction note:** Mixed access model. Newsletter (ADM Today) via email subscription. Some content gated.

**Australian Foreign Affairs (AFA)** | `australianforeignaffairs.com` | Type: `journal` / `long_form` | Status: `EXISTING`
- **Structural role:** Long-form strategic journal published three times per year. Contributors include serving ministers, retired officials, and leading academics. Detects slow-moving shifts in elite consensus.
- **Domain coverage:** All five domains — strategic-level analysis
- **Reasoning:** Tier 3 because publication cadence (three issues per year) is too slow for daily monitoring. But when it publishes, contributors and content are high-signal for elite consensus shifts. The boost ensures its periodic output surfaces when relevant.
- **Extraction note:** Paywalled. Some articles released free online.

**ISEAS Fulcrum** | `fulcrum.sg` | Type: `think_tank` / `regional_lens` | Status: `NEW`
- **Structural role:** Fills the structural gap identified in the source map: Southeast Asian perspectives on Australia's posture. Published by ISEAS-Yusof Ishak Institute (Singapore), the region's premier Southeast Asia research institute.
- **Domain coverage:** Diplomatic alignment, Institutional engagement (ASEAN perspective)
- **Reasoning:** The source map explicitly recommends supplementing with Fulcrum for ASEAN interlocutor perspectives. All existing sources are Australia-based — the pipeline captures how Australia talks about ASEAN engagement but not how ASEAN perceives it. Tier 3 because it's a supplementary regional lens, not an Australian domestic source.
- **Extraction note:** Fully free. Published by ISEAS-Yusof Ishak Institute, Singapore.

**The Diplomat** | `thediplomat.com` | Type: `regional_specialist` | Status: `NEW`
- **Structural role:** English-language Asia-Pacific current affairs magazine with strong Australia/Indo-Pacific coverage. Provides the international analytical frame that domestic outlets lack.
- **Domain coverage:** Diplomatic alignment, Security & defense autonomy, Institutional engagement
- **Reasoning:** Tier 3 as a supplementary regional lens. Not Australia-specific (covers all of Asia-Pacific), but when it publishes Australia analysis, the international-comparative framing is unique. Free and extractable.
- **Extraction note:** Fully free. RSS available.

**DevPolicy Blog (ANU)** | `devpolicy.org` | Type: `think_tank` / `academic` | Status: `NEW`
- **Structural role:** Fills the Pacific Islands engagement gap identified in the source map. The Development Policy Centre at ANU is Australia's leading research institute on Pacific aid, development, and engagement.
- **Domain coverage:** Institutional engagement (Pacific Islands), Diplomatic alignment (Pacific Step-up)
- **Reasoning:** The source map identifies Pacific Islands engagement as a structural gap — no listed outlet maintains dedicated Pacific coverage. DevPolicy Blog systematically tracks Australian aid, Pacific labour mobility, and development engagement. Tier 3 for narrow scope, but structurally essential for a known gap.
- **Extraction note:** Fully free. Blog format with regular publication.

---

### Neutral — no Goggle rule

**The Australian** | `theaustralian.com.au` | Type: `paper_of_record` | Status: `EXISTING → DEMOTED TO NEUTRAL`
- **Why neutral:** Would be Tier 1 on editorial merit — houses dedicated defence and national security editors, Greg Sheridan is Australia's most influential foreign affairs columnist. However, **blocked by Anthropic's crawler** (`theaustralian.com.au` in blocked domains list) AND behind a hard paywall. Double extraction barrier makes boosting counterproductive — the pipeline cannot read what it finds. Under Goggle model, it can still appear organically and provide headline-level signal. If extraction route changes, re-evaluate immediately to Tier 1.

**ABC News** | `abc.net.au` | Type: `public_broadcaster` | Status: `EXISTING → DEMOTED TO NEUTRAL`
- **Why neutral:** Would be Tier 1 on structural merit — Australia's most trusted news brand, free, high-volume, structured content. However, **blocked by Anthropic's crawler** (`abc.net.au` in blocked domains list). This is the single most damaging blocked domain for the Australia pipeline. Under Goggle model, it can still appear organically and provide headline signal. Leave at Neutral rather than Discard — when extraction pathways evolve, ABC should be immediately restored to Tier 1.

**The Guardian Australia** | `theguardian.com/australia-news` | Type: `digital_daily` | Status: `EXISTING → DEMOTED TO NEUTRAL`
- **Why neutral:** Free-access counterweight to the Murdoch/Nine duopoly with strong asylum/migration and climate diplomacy coverage. However, **blocked by Anthropic's crawler** (`theguardian.com` in blocked domains list). Extraction will fail. Under Goggle model, organic ranking allows headline-level discovery. If extraction route opens, re-evaluate to Tier 2.

**Sydney Morning Herald** | `smh.com.au` | Type: `paper_of_record` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Curation exclusion was correct — coverage largely duplicated by AFR (same Nine Entertainment group) with fewer specialist correspondents. Also **blocked by Anthropic's crawler**. Under Goggle model, no reason to actively discard — it may surface organically for specific queries.

**Sky News Australia** | `skynews.com.au` | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Curation exclusion was correct under the hard-filter model — commentary programming with low signal-to-noise ratio, duplicated by The Australian. Under Goggle model, exclusions default to Neutral not Discard. Also **blocked by Anthropic's crawler**. If Sky News breaks a national security story (it occasionally does via Sharri Markson), Brave may surface it at organic ranking.

**Wire services (Reuters, AP)** | `reuters.com`, `apnews.com` | Type: `wire` | Status: `CONFIRMED NEUTRAL`
- **Why neutral:** Wire coverage of Australia is too thin and decontextualized for posture analysis — domestic outlets carry the same facts with more context. Not boosted, not discarded. Reuters is additionally blocked by Anthropic's crawler. AP News is not blocked and may surface organically.

---

### Discard — `$discard`

**Michael West Media** | `michaelwest.com.au` | Status: `NEW DISCARD`
- **Discard reasoning:** Independent outlet focused on corporate accountability and domestic politics. Foreign policy and defence coverage is sporadic and secondary. Would actively displace higher-signal sources from pipeline results without contributing posture-relevant analysis.

**Crikey** | `crikey.com.au` | Status: `NEW DISCARD`
- **Discard reasoning:** Same logic as Michael West Media — investigative capability exists but foreign policy and defence coverage is secondary to its core focus on media criticism and domestic political commentary. Paywalled. Would waste result slots.

**The Monthly / Quarterly Essay** | `themonthly.com.au` | Status: `NEW DISCARD`
- **Discard reasoning:** Publication cadence (monthly/quarterly) too slow for posture-change detection, and its strategic-level insights are better captured by Australian Foreign Affairs (same Schwartz Media publisher, explicitly foreign-policy focused). Actively discarding prevents Brave from surfacing Monthly essays in place of more timely AFA content.

---

## STRUCTURAL COVERAGE CHECK

| Structural Role | Source(s) | Tier | Notes |
|---|---|---|---|
| Government leak channel | N/A — no single outlet | — | Australia lacks a government-aligned signaling outlet equivalent to Mexico's La Jornada. Government messaging is distributed across press conferences, DFAT releases, and friendly columnists (Greg Sheridan in The Australian). Layer 2 direct polling of dfat.gov.au and defence.gov.au is the primary capture mechanism |
| Opposition voice | The Conversation (academic critique), AFR (business critique) | T2, T1 | Opposition framing is distributed across outlets rather than concentrated. The Greens' anti-AUKUS positioning surfaces primarily in parliamentary coverage (aph.gov.au) |
| Defence/security first-mover | ASPI Strategist, Defence Connect, ADM | T1, T2, T3 | Australia has unusually strong dedicated defence press. ASPI for analytical depth, Defence Connect for procurement speed, ADM for technical detail |
| Policy-elite discourse | Lowy Interpreter, AFR, USSC | T1, T1, T2 | Lowy for foreign policy debate; AFR for what decision-makers read daily; USSC for alliance management |
| Domestic-language depth | N/A | — | Australia is English-primary. No non-English domestic boost applies. SBS Mandarin/Arabic bulletins are the exception — captured through SBS at Tier 1 |
| Official government source | dfat.gov.au, defence.gov.au, aph.gov.au | T2 | **LAYER 2 MIGRATION** — primary fetch via direct polling. Goggle boost as fallback. Includes pm.gov.au (add to Layer 2 polling) |
| Analytical/think tank depth | Lowy, ASPI, USSC, East Asia Forum, AIIA | T1, T1, T2, T2, T2 | Five think tank platforms is high but each has a distinct niche. Australia's think tank ecosystem is unusually deep for a middle power |
| Wire service (regional) | Reuters, AP News | Neutral | Not boosted — wire copy available organically. Reuters blocked by Anthropic crawler |
| Pacific Islands lens | DevPolicy Blog | T3 | **NEW** — fills the structural gap identified in the source map. No other source systematically tracks Pacific engagement |
| Southeast Asian perspective | ISEAS Fulcrum | T3 | **NEW** — fills the second structural gap. Provides ASEAN interlocutor perspective on Australia's regional posture |

**Gaps identified:**
1. **Blocked domain impact** is the dominant structural concern. Three of the five recommended media sources (ABC, The Australian, Guardian) are blocked by Anthropic's crawler. This means the pipeline's media-source extraction capability for Australia is severely constrained. The pipeline will lean heavily on think tank platforms (Lowy, ASPI, USSC, East Asia Forum) and SBS for daily signal. This is workable but fragile — if think tank publication slows (holiday periods, funding disruptions), the pipeline loses its primary signal sources.
2. **Pacific Islands coverage** remains thin even with DevPolicy Blog added. Episodic event-driven coverage from major outlets will supplement, but no source provides daily Pacific monitoring.
3. **Chinese-language Australian media** (e.g., WeChat public accounts, Chinese-language newspapers in Sydney/Melbourne) are structurally important for diaspora constraint dynamics but not practically monitorable in this pipeline. SBS Mandarin bulletins are the accessible proxy.
4. **Defence procurement detail** is well-covered by Defence Connect and ADM, but **intelligence community oversight** (ASIO, ASIS, ASD) is underrepresented. ASIO annual threat assessments and PJCIS reports are accessible via aph.gov.au (Layer 2) but no dedicated source tracks intelligence policy daily.

---

## REDUNDANCY RESOLUTION

**Think tank cluster: Lowy Interpreter + ASPI Strategist + USSC + East Asia Forum + AIIA**
Five think tank platforms is high, but each has a distinct structural niche. Lowy (Tier 1, broadest foreign policy scope, daily cadence, benchmark polling data), ASPI (Tier 1, defence/security/tech specialist, daily cadence), USSC (Tier 2, US-alliance specialist, narrower scope), East Asia Forum (Tier 2, trade/regional institutions, academic rigour), AIIA (Tier 2, weekly digest validation function). Redundancy is minimal because domain coverage barely overlaps — Lowy and ASPI together cover the full foreign-policy/security spectrum, while USSC, East Asia Forum, and AIIA each fill specific sub-domains.

**Defence trade press cluster: Defence Connect + ADM**
Both cover defence procurement and industrial base. Defence Connect leads (Tier 2) for higher volume and speed. ADM drops to Tier 3 for deeper technical reporting at lower frequency. Differentiated by speed vs. depth — not redundant.

**Government official cluster: DFAT + Defence + Parliament**
All three are Layer 2 migration targets with Tier 2 Goggle fallback. No redundancy — each covers a different institutional domain (diplomacy, military, legislative oversight). All should be polled directly.

**Blocked media cluster: The Australian + ABC + Guardian + SMH**
Four blocked sources would otherwise span Tier 1 to Tier 2. All demoted to Neutral. No redundancy resolution needed — the pipeline cannot extract from any of them. The structural gap they leave is filled by elevated think tank and SBS coverage.

---

## QUERY CONFIGURATION

```
country: AU
search_lang: en
freshness: pw
```

**Multi-language notes:** Australia's media ecosystem operates overwhelmingly in English. No secondary language query cycle is needed. SBS Mandarin and Arabic bulletins provide non-English domestic signal but are accessed through the SBS English-language domain (sbs.com.au), so the pipeline captures them via the standard English query path.

**Localized query vocabulary validation:**

The curation prompt's vocabulary is solid. Notes:

- **Domain 1 (Diplomatic):** All terms valid. `"Penny Wong"` remains the primary diplomatic signal generator. Add `"Albanese foreign policy"` as a leader-specific pattern. `"Pacific Step-up"` is valid but may be declining as Labor has rebranded this as `"Pacific engagement"` — consider adding both. Add `"AUKUS"` here as well (not just Domain 2) since AUKUS has major diplomatic alignment implications beyond the defence domain.
- **Domain 2 (Security):** Strong list. Add `"Richard Marles"` (Deputy PM / Defence Minister — his statements are the primary defence posture signal). `"northern bases"` is valid and high-signal. Add `"GWEO"` (guided weapons and explosive ordnance) and `"nuclear submarines"` as specific AUKUS Pillar I terms. `"Defence Strategic Review"` may be declining as NDS supersedes it — keep both but weight NDS higher.
- **Domain 3 (Economic):** Good coverage. Add `"FIRB"` (Foreign Investment Review Board) — rejections are high-signal posture events. `"critical minerals"` is correct and high-priority. Add `"rare earths"` and `"lithium"` as specific commodity terms. `"anti-dumping"` is valid for China trade disputes. Add `"tariff"` and `"sanctions"` as general economic statecraft terms.
- **Domain 4 (Institutional):** Valid. `"Quad"` and `"PIF"` (Pacific Islands Forum) are essential. Add `"ASEAN summit"` and `"APEC"` explicitly. `"UN Human Rights Council"` is valid but low-frequency — keep for completeness. Add `"MIKTA"` (Mexico-Indonesia-Korea-Turkey-Australia) if still active.
- **Domain 5 (Domestic):** Strong. `"Senate Estimates"` is high-signal. `"Lowy Institute Poll"` is correct for annual benchmarking. Add `"bipartisanship"` as a term — breaks in bipartisan consensus on foreign/defence policy are high-signal events. Add `"Greens AUKUS"` for the main parliamentary opposition to defence posture. Add `"teals"` for independent MPs who may break consensus.

**Stale/problematic terms:** None are stale. `"Pacific Step-up"` may be declining in usage under Labor — monitor and potentially replace with `"Pacific engagement"`.

**Suggested topic query patterns:**

1. `AUKUS submarine Australia Marles` — AUKUS implementation and defence posture
2. `Penny Wong DFAT Indo-Pacific` — Diplomatic alignment and regional strategy
3. `FIRB critical minerals China Australia` — Economic statecraft and investment screening
4. `Senate Estimates defence foreign affairs` — Parliamentary oversight and official positioning
5. `Quad PIF Pacific Australia engagement` — Institutional engagement and regional architecture

---

## GOGGLE FILE

```goggle
! name: MPM Australia
! description: MPM pipeline source prioritization for Australia — boosts high-signal sources, discards noise
! public: false
! author: MPM Pipeline

! --- Tier 1: Essential (boost=3) ---
$boost=3,site=lowyinstitute.org
$boost=3,site=aspistrategist.org.au
$boost=3,site=afr.com
$boost=3,site=sbs.com.au

! --- Tier 2: Important (boost=2) ---
$boost=2,site=ussc.edu.au
$boost=2,site=eastasiaforum.org
$boost=2,site=internationalaffairs.org.au
$boost=2,site=defenceconnect.com.au
$boost=2,site=dfat.gov.au
$boost=2,site=defence.gov.au
$boost=2,site=aph.gov.au
$boost=2,site=theconversation.com

! --- Tier 3: Supplementary (boost=1) ---
$boost=1,site=australiandefence.com.au
$boost=1,site=australianforeignaffairs.com
$boost=1,site=fulcrum.sg
$boost=1,site=thediplomat.com
$boost=1,site=devpolicy.org

! --- Discard: Noise ---
$discard,site=michaelwest.com.au
$discard,site=crikey.com.au
$discard,site=themonthly.com.au
```

---

## INTERPRETIVE CONTEXT FOR DOSSIER

### Tier 1 Sources

> Articles from **The Interpreter (Lowy Institute)** about any foreign policy domain should be interpreted as Australia's most authoritative independent analytical voice — its realist-internationalist orientation and contributor base of former DFAT officials and regional experts mean it reflects the mainstream of Australia's foreign policy establishment. When Lowy analysis diverges from government messaging, this signals genuine policy contestation within the establishment.

> Articles from **The Strategist (ASPI)** about defence and security affairs should be interpreted as hawkish-leaning analysis from a partially Defence-funded institution — ASPI's editorial line consistently favours stronger defence posture, deeper alliance engagement, and more assertive China policy. Its analysis is technically rigorous and deeply sourced, but its institutional incentives align with defence expansion. When ASPI criticises government defence policy, it is almost always arguing for more spending or faster capability acquisition, not less.

> Articles from **Australian Financial Review** about trade, economic statecraft, or AUKUS procurement should be interpreted as reflecting the perspective of Australia's business and policy elite — its economically liberal, pro-alliance editorial line means it frames economic policy through an investment-climate and alliance-management lens. AFR is where policy signals surface first because of its elite readership, but its editorial framing favours market-oriented and alliance-deepening outcomes.

> Articles from **SBS News** about diaspora community reactions to foreign policy should be interpreted as a unique signal layer unavailable elsewhere — SBS's multicultural mandate means it captures how Chinese-Australian, Indian-Australian, and other diaspora communities interpret bilateral relationship shifts. This is essential for understanding domestic constraints on foreign policy but should not be treated as representative of mainstream Australian public opinion.

### Tier 2 Sources

> Articles from **United States Studies Centre** about the US-Australia alliance should be interpreted as analytically rigorous but structurally alliance-supportive — USSC's institutional purpose is to study and strengthen the bilateral relationship, which means its analysis rarely questions the fundamental value of the alliance. Essential for granular AUKUS and AUSMIN tracking, but its framing assumes alliance continuation as a baseline.

> Articles from **East Asia Forum** about trade and regional institutions should be interpreted as academic analysis with a liberal-institutionalist orientation — its ANU Crawford School base and Peter Drysdale's intellectual legacy mean it favours multilateral trade governance, RCEP deepening, and institutional engagement over bilateral or minilateral alternatives. When East Asia Forum is critical of government trade policy, it typically argues for more multilateral engagement, not less.

> Articles from **Australian Outlook (AIIA)** about foreign affairs events should be interpreted with awareness that its contributor base includes both retired diplomats (who may defend past policy decisions) and early-career DFAT officers (who may be constrained in their public commentary). The weekly digest is factual and non-editorial — use it as a structured event log, not an analytical source.

> Articles from **Defence Connect** about defence procurement and industry should be interpreted as pro-defence-industry reporting — its business model depends on the defence industrial base, which means it frames procurement decisions positively and capability gaps urgently. Useful for factual tracking of contracts and milestones but its editorial framing consistently favours defence spending increases.

> Articles from **dfat.gov.au**, **defence.gov.au**, and **aph.gov.au** should be interpreted as official government communications and parliamentary record — not journalism but primary source material. Press releases, joint statements, and Hansard transcripts represent the government's chosen public position or the formal legislative record. These are foundational for tracking what the government says it is doing, which may differ from what it is actually doing.

> Articles from **The Conversation (Australia)** about any domain should be interpreted as academic expert commentary with a progressive-leaning contributor pool — the platform's requirement that all contributors be academics means it reflects scholarly consensus rather than journalistic investigation. Useful as a sentiment layer for how Australia's expert class frames strategic posture debates, but not a source of original reporting.

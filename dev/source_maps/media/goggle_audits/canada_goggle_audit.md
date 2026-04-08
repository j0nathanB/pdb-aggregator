# AUDIT SUMMARY: CANADA

**Sources assessed:** 18 recommended + 5 excluded + 4 newly identified = 27 total
**Tier 1 (boost=3):** 5 sources
**Tier 2 (boost=2):** 7 sources
**Tier 3 (boost=1):** 5 sources
**Neutral (no rule):** 6 sources
**Discard:** 4 sources
**Overall assessment:** The curation prompt produced a well-balanced whitelist with strong think-tank coverage — unusual depth for a Five Eyes country where foreign policy media is structurally thin. Key changes: (1) promoted French-language sources (Radio-Canada, Le Devoir) to reflect bilingual political discourse and non-English boost premium; (2) resolved redundancy in the broadsheet cluster by differentiating Globe and Mail (Tier 1 paper of record) from National Post (demoted to Neutral — blocked by Anthropic crawler and editorially redundant with Globe); (3) promoted government official sources for Layer 2 migration; (4) flagged `nationalpost.com`, `financialpost.com`, and `thestar.com` as blocked by Anthropic's crawler; (5) added iPolitics (opposition/leak channel), Canadian Global Affairs Institute (defence think tank), and wire services for structural completeness.

---

## BOOST ASSIGNMENTS

### Tier 1 — `$boost=3`

**CBC News** | `cbc.ca` | Type: `public_broadcaster` | Status: `EXISTING`
- **Structural role:** Canada's largest newsroom and most-reached news brand. Functions as the default source for detecting any shift in government posture. Dedicated Parliament Hill bureau, defence reporter (Murray Brewster), and foreign correspondents.
- **Domain coverage:** Diplomatic alignment, Security & defence, Economic statecraft, Domestic constraints, Institutional engagement
- **Reasoning:** CBC is indispensable — the single source most likely to surface policy-relevant stories first, with broader topical coverage and deeper staffing than any competitor. Free and fully extractable, which maximizes pipeline utility. English-language, but its structural role as public broadcaster gives it unmatched access to official sources. The pipeline needs CBC surfacing first for any Canada query.
- **Extraction note:** Free; no paywall. Full text extraction reliable.

**The Globe and Mail** | `theglobeandmail.com` | Type: `paper_of_record` | Status: `EXISTING`
- **Structural role:** Canada's newspaper of record for elite political discourse. Campbell Clark on foreign policy; Robert Fife and Steven Chase on national security investigations. Op-ed page is the primary venue for Canadian foreign-policy debate among former officials and academics.
- **Domain coverage:** All five domains
- **Reasoning:** Where CBC provides breadth and speed, the Globe provides depth and elite framing. Its op-ed page is where former ambassadors, DND officials, and academics signal policy positions — essential for detecting shifts in elite consensus. Centre-right, pro-business, internationalist orientation means it frames trade and defence issues through a hawkish-pragmatic lens. Metered paywall means most content is extractable via Brave indexing.
- **Extraction note:** Metered paywall; subscription for full access. Brave indexes paywalled headlines.

**Radio-Canada (ICI Radio-Canada)** | `ici.radio-canada.ca` | Type: `public_broadcaster` | Status: `EXISTING — PROMOTED`
- **Structural role:** Essential French-language mirror of CBC; captures Quebec-specific political dynamics and francophone framing of foreign policy. Higher trust levels than English-language equivalents.
- **Domain coverage:** Diplomatic alignment, Domestic constraints, Institutional engagement
- **Reasoning:** Non-English domestic sources earn boost premium in bilingual countries. Radio-Canada is not merely a translation of CBC — its editorial selection reflects Quebec's distinct political culture, where La Francophonie, sovereignty, and federal-provincial dynamics shape foreign policy preferences differently than in English Canada. Higher trust ratings than any English-language source. Free and fully extractable. Promoted from implicit Tier 2 (where the whitelist placed it) to Tier 1 because the pipeline must capture francophone political discourse to avoid anglophone-only bias.
- **Extraction note:** Free; no paywall.

**The Hill Times** | `hilltimes.com` | Type: `parliamentary_specialist` | Status: `EXISTING — PROMOTED`
- **Structural role:** Canada's only remaining publication specifically covering the Ottawa policy apparatus. Read by Cabinet ministers, MPs, senators, PMO, Privy Council, and DND. Absorbed Embassy magazine (Canada's former dedicated diplomatic affairs paper) in 2016.
- **Domain coverage:** All five domains
- **Reasoning:** Structural role outweighs circulation per boost principles. The Hill Times is where parliamentary committee activities on defence and foreign affairs are reported, where backbench and Senate foreign policy views surface, and where the bureaucratic machinery of Global Affairs Canada and DND is scrutinized. No other outlet fills this niche. In a media ecosystem where the curation prompt itself notes the foreign policy coverage is "thin," the Hill Times is one of the few sources with a dedicated mandate. Paywall limits extraction, but Brave indexes headlines.
- **Extraction note:** Hard paywall; institutional subscriptions common. Extraction may be partial.

**La Presse** | `lapresse.ca` | Type: `digital_newspaper` | Status: `EXISTING — PROMOTED`
- **Structural role:** Highest-reach French-language digital news brand. Free access nonprofit model means wide readership. Strong political columnists and investigative team.
- **Domain coverage:** Diplomatic alignment, Domestic constraints, Economic statecraft
- **Reasoning:** Non-English boost premium applies. La Presse's nonprofit model and free access make it the most widely read French-language news source in Canada — its framing shapes how francophone Canadians understand federal policy. Essential for detecting Quebec-specific constraints on federal external action (e.g., Quebec's distinct positions on immigration, environmental treaties, La Francophonie engagement). Free and fully extractable — unlike most Tier 1 sources, no paywall limits pipeline access.
- **Extraction note:** Free; nonprofit model.

---

### Tier 2 — `$boost=2`

**Le Devoir** | `ledevoir.com` | Type: `independent_daily` | Status: `EXISTING`
- **Structural role:** Independently owned since 1910; disproportionate influence on Quebec's political class relative to circulation. Provides the Quebec-nationalist/autonomist perspective on Canada's international positioning.
- **Domain coverage:** Diplomatic alignment, Institutional engagement, Domestic constraints
- **Reasoning:** Non-English boost premium applies, but Le Devoir lands at Tier 2 rather than Tier 1 because its circulation is small and its influence, while outsized in Quebec intellectual circles, is narrower than Radio-Canada or La Presse in shaping mass francophone opinion. Its centre-left, Quebec-nationalist orientation provides a distinct perspective unavailable from any English-language source — particularly on how sovereignty/autonomism shapes Quebec's preferred foreign policy positioning. Metered paywall; partial extraction likely.

**CTV News** | `ctvnews.ca` | Type: `private_broadcaster` | Status: `EXISTING`
- **Structural role:** Bell Media's flagship news brand; second-highest TV news reach in Canada. Ottawa bureau covers Parliament Hill. Important for detecting how government messaging lands with mass audiences.
- **Domain coverage:** Diplomatic alignment, Domestic constraints
- **Reasoning:** Third major English-language news brand after CBC and Globe. CTV's mass audience reach means its framing reflects mainstream centrist Canadian opinion. Tier 2 rather than Tier 1 because it breaks fewer stories than CBC and its foreign policy coverage is thinner — CTV follows the agenda more than it sets it. But its reach means the pipeline should capture its framing. Free and extractable.

**Global News** | `globalnews.ca` | Type: `private_broadcaster` | Status: `EXISTING`
- **Structural role:** Corus Entertainment network; strong on national security and intelligence reporting (Mercedes Stephenson on defence). Third major broadcast perspective alongside CBC and CTV.
- **Domain coverage:** Security & defence, Domestic constraints
- **Reasoning:** Global News earns Tier 2 specifically for its defence/security beat — Mercedes Stephenson is one of the few dedicated defence reporters in Canadian media, and Global News broke several of the foreign interference stories in 2023-2025. Narrower domain coverage than CTV (mostly security + domestic constraints) but deeper in its niche. Free and extractable.

**BNN Bloomberg** | `bnnbloomberg.ca` | Type: `business_financial` | Status: `EXISTING`
- **Structural role:** Primary Canadian outlet for trade policy, sanctions, tariff impacts, supply-chain statecraft, and central bank positioning. Bloomberg partnership adds international data layer.
- **Domain coverage:** Economic & technological statecraft
- **Reasoning:** Sole dedicated business/financial outlet on the list. In the current Canada-U.S. tariff environment, BNN Bloomberg is where CUSMA/USMCA dynamics, Bank of Canada decisions, critical minerals policy, and investment screening stories surface first. Single-domain (economic statecraft) but irreplaceable within it. Free (some Bloomberg content gated); mostly extractable. Tier 2 rather than Tier 1 because single-domain coverage limits structural weight.

**Canada.ca (Global Affairs / DND)** | `canada.ca` | Type: `government_official` | Status: `EXISTING` — **LAYER 2 MIGRATION**
- **Structural role:** Official government portal. Houses Global Affairs Canada, DND, and PMO press releases, policy documents, sanctions lists, trade agreements, and defence policy updates.
- **Domain coverage:** All five domains (official source)
- **Reasoning:** Primary fetch via Layer 2 direct polling. Goggle boost at Tier 2 as belt-and-suspenders fallback. Government press releases and policy documents occasionally surface in Brave News Search. Includes subdomains: `international.gc.ca`, `forces.gc.ca`. Not journalism — official government communications.
- **Note:** `pm.gc.ca` (Prime Minister's Office) is listed separately in the pipeline config but resolves under the `canada.ca` umbrella for Goggle purposes. Both `pm.gc.ca` and `canada.ca` are boosted.

**pm.gc.ca (Prime Minister's Office)** | `pm.gc.ca` | Type: `government_official` | Status: `NEW (from config)` — **LAYER 2 MIGRATION**
- **Structural role:** Official PMO communications. Statements, press conferences, and policy announcements from the Prime Minister's Office.
- **Domain coverage:** All five domains (official source)
- **Reasoning:** Listed in pipeline config as Tier 1 government source. Boosted at Tier 2 in Goggle as belt-and-suspenders alongside Layer 2 direct polling. Distinct from `canada.ca` in that PMO statements signal executive intent specifically, whereas `canada.ca` aggregates all departmental communications.

**Canadian Global Affairs Institute (CGAI)** | `cgai.ca` | Type: `think_tank` | Status: `NEW`
- **Structural role:** Canada's principal defence and security think tank. Regular commentary from retired military officers, former diplomats, and security practitioners. Fills the structural gap noted in the coverage assessment for dedicated defence/security analysis.
- **Domain coverage:** Security & defence, Diplomatic alignment
- **Reasoning:** The curation prompt identified a gap: "the absence of a dedicated Canadian outlet for intelligence and national-security reporting." CGAI partially fills this — it publishes regular policy briefs on NORAD modernization, Arctic security, NATO interoperability, and CAF capabilities. Its retired-military contributor base provides insider perspectives unavailable from mainstream media. Think tanks earn boost through depth not speed. Free and extractable.

---

### Tier 3 — `$boost=1`

**OpenCanada (CIC)** | `opencanada.org` | Type: `think_tank_magazine` | Status: `EXISTING`
- **Structural role:** Published by the Canadian International Council. Features analysis by academics, former diplomats, and practitioners. Closest Canadian equivalent to Foreign Affairs for Canada-specific strategic positioning.
- **Domain coverage:** Diplomatic alignment, Institutional engagement, Security & defence
- **Reasoning:** Think tanks earn boost through depth, not speed. OpenCanada publishes the structural analysis the pipeline needs to interpret daily events — Canada's NATO posture, Five Eyes dynamics, multilateral positioning. Tier 3 rather than Tier 2 because publication frequency is low and it doesn't break news. But when it publishes, the analysis provides unique interpretive depth.

**CIGI (Centre for International Governance Innovation)** | `cigionline.org` | Type: `think_tank` | Status: `EXISTING`
- **Structural role:** Leading Canadian think tank on global governance, digital trade, AI regulation, and data sovereignty. Strong on tech-statecraft and institutional reform.
- **Domain coverage:** Economic & technological statecraft, Institutional engagement, Diplomatic alignment
- **Reasoning:** CIGI's niche — technology governance, digital trade, AI regulation — is increasingly relevant to Canada's strategic posture but is a specialized domain. Tier 3 because its output is periodic and narrowly focused compared to generalist news sources, but the boost ensures its analysis surfaces when relevant. Free and extractable.

**Macdonald-Laurier Institute (MLI)** | `macdonaldlaurier.ca` | Type: `think_tank` | Status: `EXISTING`
- **Structural role:** Most-cited think tank in Canada's Parliament. Regular defence and foreign policy output; experts frequently testify at parliamentary committees.
- **Domain coverage:** Security & defence, Diplomatic alignment, Economic statecraft
- **Reasoning:** MLI provides the conservative-realist perspective on Canadian strategic posture — hawkish on defence spending, critical of China engagement, Atlanticist. This perspective is structurally essential for understanding the right-of-centre policy consensus that shapes Conservative Party positions and cross-partisan defence hawks. Tier 3 rather than Tier 2 because its output overlaps with National Post commentary (where MLI experts frequently publish) and its analytical depth doesn't match CGAI on defence-specific topics.

**Policy Options (IRPP)** | `policyoptions.irpp.org` | Type: `think_tank_magazine` | Status: `EXISTING`
- **Structural role:** Published by the Institute for Research on Public Policy. Bilingual publication bridging academic research and policy debate.
- **Domain coverage:** Domestic constraints, Institutional engagement, Economic statecraft
- **Reasoning:** Bilingual output is a differentiator — Policy Options publishes in both English and French, bridging the two linguistic communities. Strong on trade policy, federalism constraints, and institutional questions. Tier 3 because its academic orientation means lower publication frequency and less breaking-news relevance, but the bilingual depth and federalism focus are unique.

**iPolitics** | `ipolitics.ca` | Type: `political_specialist` | Status: `NEW (was excluded)`
- **Structural role:** Ottawa-focused political news site with parliamentary coverage. Originally excluded as duplicating Hill Times ground, but fills the opposition-voice / leak-channel role that no other source explicitly occupies.
- **Domain coverage:** Domestic constraints, Diplomatic alignment
- **Reasoning:** The curation prompt excluded iPolitics as "largely duplicates Hill Times ground with thinner reporting capacity." Under the Goggle model, this is insufficient reason for exclusion — curation exclusions default to Neutral or Tier 3, not Discard. iPolitics fills a structural gap: Canada's whitelist lacks an explicit opposition-voice or government-leak channel (unlike Mexico's La Jornada/Latinus pairing). iPolitics' Ottawa insider coverage occasionally surfaces caucus dissent and policy leaks that don't appear in mainstream outlets. Tier 3 as supplementary Ottawa insider signal.

---

### Neutral — no Goggle rule

**National Post / Financial Post** | `nationalpost.com`, `financialpost.com` | Type: `national_newspaper` | Status: `EXISTING → DEMOTED TO NEUTRAL`
- **Why neutral:** Both domains are **blocked by Anthropic's crawler** (`nationalpost.com` and `financialpost.com` appear in blocked domains list). Even if Brave surfaces National Post results, the pipeline cannot extract full text. Editorially, its centre-right, hawkish positioning overlaps substantially with the Globe and Mail (Tier 1) and MLI commentary (Tier 3). Under the Goggle model, it can still appear organically — no need to boost, but no need to discard either. The U.S. hedge fund ownership (Chatham Asset Management) is a secondary concern but worth noting. If Globe and Mail becomes unavailable, National Post should be re-evaluated.

**Toronto Star** | `thestar.com` | Type: `major_newspaper` | Status: `EXISTING → DEMOTED TO NEUTRAL`
- **Why neutral:** **Blocked by Anthropic's crawler** (`thestar.com` appears in blocked domains list). Cannot be extracted even if Brave surfaces it. Its centre-left, social-liberal orientation provided the progressive counterpoint to the Globe's centre-right framing, but this structural role is partially filled by CBC (centrist public broadcaster) and La Presse (centrist-to-centre-left francophone). Under the Goggle model, leave at organic ranking — headlines may still provide signal even without full extraction.

**Canadian Defence Review** | `canadiandefencereview.com` | Type: `specialist_defence` | Status: `EXISTING → DEMOTED TO NEUTRAL`
- **Why neutral:** Trade publication with pro-defence-industry stance. Covers procurement and capabilities, but publication frequency is low and its trade-publication orientation means it reflects industry lobbying as much as policy analysis. CGAI (newly added at Tier 2) and Global News' defence beat provide sufficient defence coverage. Under the Goggle model, organic ranking is appropriate — if CDR publishes a significant procurement story, Brave may surface it without boost.

**The Canadian Press** | `thecanadianpress.com` | Type: `wire_service` | Status: `EXISTING → CONFIRMED NEUTRAL`
- **Why neutral:** Wire copy is available organically — CP stories appear across dozens of partner outlets under various publisher domains. Boosting the CP domain specifically would be redundant since CP-bylined stories are already surfaced through boosted outlets (CBC, CTV, Global News all carry CP wire). The pipeline already captures CP signal indirectly.

**The Conversation Canada** | `theconversation.com/ca` | Type: `excluded → neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Curation exclusion noted "occasionally publishes academic commentary but functions as an aggregator of expert opinion." Under the Goggle model, no reason to actively discard. Academic commentary on foreign policy occasionally surfaces here before appearing in policy journals. Organic ranking is appropriate.

**The Tyee** | `thetyee.ca` | Type: `excluded → neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Independent digital outlet with strong investigative capacity, particularly on British Columbia politics and environmental policy. Curation exclusion cited "minimal foreign policy or defence reporting," which is accurate, but under the Goggle model, curation exclusions default to Neutral. The Tyee occasionally covers Pacific trade and Asia-Pacific dynamics from a BC perspective — organic ranking allows this to surface when relevant.

---

### Discard — `$discard`

**Rebel News** | `rebelnews.com` | Status: `CONFIRMED DISCARD`
- **Discard reasoning:** Right-wing advocacy outlet with low factual reliability ratings. Not read by the policy-making class. Advocacy-first model would actively displace higher-signal sources from top results. Would inject partisan noise without adding analytical or reporting value.

**Daily Hive** | `dailyhive.com` | Status: `CONFIRMED DISCARD`
- **Discard reasoning:** Digital-native lifestyle/entertainment aggregator. Minimal original political or foreign policy reporting. Headlines are optimized for social engagement, not policy relevance. Would waste result slots that should go to substantive sources.

**Narcity** | `narcity.com` | Status: `CONFIRMED DISCARD`
- **Discard reasoning:** Lifestyle/entertainment aggregator targeting younger demographics. No original political or foreign policy reporting. Same rationale as Daily Hive — social-engagement-optimized headlines would displace substantive sources.

**Toronto Sun / Ottawa Sun (Postmedia tabloids)** | `torontosun.com`, `ottawasun.com` | Status: `CONFIRMED DISCARD`
- **Discard reasoning:** Tabloid format with populist commentary rather than original reporting on strategic posture. National Post (Neutral) already captures Postmedia's substantive policy coverage. Sun chain editorials and columnists would inject low-signal opinion content that displaces higher-quality analysis.

---

## STRUCTURAL COVERAGE CHECK

| Structural Role | Source(s) | Tier | Notes |
|---|---|---|---|
| Government leak channel | iPolitics, Hill Times | T3, T1 | Canada lacks an explicit government-aligned signaling outlet equivalent to Mexico's La Jornada. Leaks surface through Hill Times (parliamentary insider) and iPolitics (Ottawa specialist). CBC's Parliament Hill bureau also captures ministerial signaling |
| Opposition voice | Globe and Mail, Le Devoir | T1, T2 | Globe's op-ed page hosts Conservative and hawkish criticism of government policy. Le Devoir provides Quebec-autonomist opposition to federal foreign policy. No dedicated adversarial outlet equivalent to Mexico's Latinus — opposition voices are distributed across mainstream media |
| Defence/security first-mover | CBC (Murray Brewster), Global News (Mercedes Stephenson) | T1, T2 | No dedicated defence press. These two reporters are the closest thing Canada has to dedicated defence journalism. CGAI provides analytical depth. Canadian Defence Review (Neutral) covers procurement |
| Policy-elite discourse | Globe and Mail, Hill Times, OpenCanada | T1, T1, T3 | Globe op-ed page is the primary elite debate venue. Hill Times for parliamentary-insider discourse. OpenCanada for academic/practitioner analysis |
| Domestic-language depth | Radio-Canada, La Presse, Le Devoir, Policy Options | T1, T1, T2, T3 | French-language sources are critical — Canada's political discourse is genuinely bilingual. Quebec's distinct foreign policy preferences (La Francophonie, sovereignty, immigration) require French-language capture |
| Official government source | canada.ca, pm.gc.ca | T2, T2 | **LAYER 2 MIGRATION** — primary fetch via direct polling. Goggle boost as fallback. Includes subdomains: international.gc.ca, forces.gc.ca |
| Analytical/think tank depth | CGAI, OpenCanada, CIGI, MLI, Policy Options | T2, T3, T3, T3, T3 | Five think tanks is strong coverage: CGAI (defence/security), OpenCanada (foreign policy), CIGI (tech governance), MLI (conservative-realist), Policy Options (bilingual/federalism) |
| Wire services | Reuters, AP News, France24 | Neutral | Not boosted in Goggle — wire copy available organically. **Reuters is blocked by Anthropic's crawler** but Brave can still surface it for discovery. France24 provides francophone international wire perspective |

**Gaps identified:**
1. **Intelligence/national security dedicated outlet** remains the most significant structural gap — the curation prompt itself identified this. No Canadian equivalent to RUSI, Bellingcat, or The Intercept exists. Intelligence stories surface sporadically in Globe and Mail and Global News but are not systematically covered. CSIS public threat assessments are captured via Layer 2 polling of canada.ca.
2. **Arctic sovereignty and Northern affairs** receive thin coverage outside CBC North and occasional Globe features. No dedicated Arctic policy outlet is available. The NORAD modernization and Northwest Passage disputes noted in pipeline blind spots are partially mitigated by CGAI analysis and DND releases via Layer 2.
3. **Indigenous foreign policy dimensions** — First Nations' role in Arctic sovereignty claims, resource extraction diplomacy, and international indigenous rights forums (UN Permanent Forum) are not systematically covered by any source on this list.
4. **Asia-Pacific coverage** is thin — Canada's Indo-Pacific Strategy (2022) and growing tensions with China/India over foreign interference lack a dedicated analytical outlet. CIGI partially covers this but its focus is technology governance, not geopolitics.

---

## REDUNDANCY RESOLUTION

**Broadsheet cluster: Globe and Mail + National Post + Toronto Star**
Three major English-language newspapers with overlapping national coverage. Resolved by extraction reality and editorial differentiation: Globe and Mail (Tier 1, paper of record, elite discourse venue, extractable), National Post (Neutral — blocked by Anthropic crawler, editorially redundant with Globe's centre-right positioning), Toronto Star (Neutral — blocked by Anthropic crawler, progressive counterpoint partially filled by CBC and La Presse). Under the Goggle model, both National Post and Toronto Star can still surface organically for specific queries.

**Broadcast cluster: CBC + CTV + Global News**
Three major English-language broadcast/digital news operations. Resolved by differentiating structural roles: CBC (Tier 1, largest newsroom, broadest coverage, defence beat), CTV (Tier 2, mass audience reach, mainstream framing), Global News (Tier 2, defence/security niche with Mercedes Stephenson). All free and extractable. No redundancy concern — each provides distinct editorial selection and beat coverage.

**French-language cluster: Radio-Canada + La Presse + Le Devoir**
Three major French-language outlets. No redundancy issue — each occupies a distinct structural niche: Radio-Canada (Tier 1, public broadcaster, broadest francophone reach), La Presse (Tier 1, highest-traffic digital, nonprofit, federalist), Le Devoir (Tier 2, intellectual, Quebec-nationalist). The bilingual nature of Canadian political discourse requires all three to capture the full spectrum of francophone opinion.

**Think tank cluster: CGAI + OpenCanada + CIGI + MLI + Policy Options**
Five think tanks is above average but each has a distinct analytical niche. CGAI (Tier 2, defence/security — fills a gap), OpenCanada (Tier 3, foreign policy generalist), CIGI (Tier 3, tech governance), MLI (Tier 3, conservative-realist), Policy Options (Tier 3, bilingual/federalism). Resolved by tiering: CGAI earns Tier 2 for filling the defence gap; the other four earn Tier 3 for periodic depth. No overlap justifies further demotion.

**Parliamentary specialist cluster: Hill Times + iPolitics**
Both cover Ottawa insider politics. Hill Times (Tier 1) is the indispensable source — absorbed Embassy magazine, read by the policy-making class. iPolitics (Tier 3) is supplementary — thinner reporting but occasionally surfaces caucus dissent and leak signals that Hill Times misses. Tier differentiation resolves the redundancy.

---

## QUERY CONFIGURATION

```
country: CA
search_lang: en, fr
freshness: pw
```

**Multi-language notes:** Canada's political discourse is genuinely bilingual. Queries must run in both English and French to capture the full signal landscape. French-language queries are not supplementary — they capture Quebec-specific dynamics, La Francophonie engagement, and francophone framing of federal policy that English sources miss. The pipeline's existing `languages.primary: en` with `languages.additional: [fr]` configuration should produce parallel query cycles in both languages.

**Localized query vocabulary validation:**

The curation prompt's vocabulary is strong and comprehensive. Notes:

- **Domain 1 (Diplomatic):** All terms valid. Add `"Carney politique étrangère"` and `"Joly diplomatie"` as leader-specific patterns. `"puissance moyenne"` (middle power) is correct and high-signal — it's the dominant self-concept in Canadian foreign policy discourse. Add `"Indo-Pacifique"` / `"Indo-Pacific strategy"` — increasingly relevant since the 2022 strategy launch. Add `"AUKUS"` — Canada's exclusion from AUKUS is a live diplomatic issue.
- **Domain 2 (Security):** Strong list. Add `"CSIS ingérence"` / `"CSIS interference"` — the dominant frame for Canada-China/India security tensions since 2023. `"Hogue Commission"` / `"Commission Hogue"` is essential for foreign interference coverage. `"NORAD modernisation"` correctly included. Add `"sous-marins"` / `"submarines"` — the submarine procurement decision is a defining defence posture question. Add `"Arctique défense"` / `"Arctic defence"` as a paired query.
- **Domain 3 (Economic):** Excellent. `"ACEUM"` / `"CUSMA"` correctly included. Add `"tarifs Trump Canada"` / `"Trump tariffs Canada"` — the dominant economic frame in 2025-2026. `"minéraux critiques"` (critical minerals) is correctly flagged as a key strategic asset. Add `"chaîne d'approvisionnement semiconducteurs"` / `"semiconductor supply chain"` — relevant to tech sovereignty discussions. Add `"Banque du Canada taux"` / `"Bank of Canada rate"` — central bank positioning stories.
- **Domain 4 (Institutional):** Valid. Add `"Francophonie sommet"` — Canada's engagement in La Francophonie is structurally underweighted in English-language coverage but important for Quebec domestic constraints. `"G7"` and `"ONU"` are correctly included. Add `"OTAN contribution"` / `"NATO contribution"` — defence spending relative to 2% GDP target is a persistent institutional engagement story.
- **Domain 5 (Domestic):** Strong. Add `"Poilievre"` as a high-signal opposition leader term. `"gouvernement minoritaire"` (minority government) is correctly included and highly relevant given current parliamentary dynamics. Add `"ingérence étrangère enquête"` / `"foreign interference inquiry"` — the Hogue Commission is the dominant domestic constraint story. Add `"caucus libéral dissidence"` / `"Liberal caucus dissent"` for internal party dynamics.

**Stale/problematic terms:** None are stale. All five domain vocabularies reflect current 2025-2026 Canadian political discourse accurately.

**Suggested topic query patterns:**

1. `Carney Trump tarifs CUSMA défense` — PM response to U.S. trade/defence pressure
2. `NORAD modernisation budget défense Canada` — Continental defence investment
3. `Hogue ingérence étrangère Chine Inde CSIS` — Foreign interference inquiry
4. `minéraux critiques chaîne approvisionnement Canada` — Critical minerals statecraft
5. `Joly OTAN Ukraine aide militaire Canada` — NATO/Ukraine defence posture
6. `Poilievre politique étrangère opposition conservateur` — Opposition foreign policy positioning
7. `Arctique souveraineté passage Nord-Ouest` — Arctic sovereignty disputes
8. `sous-marins approvisionnement marine canadienne` — Submarine procurement decision

---

## GOGGLE FILE

```goggle
! name: MPM Canada
! description: MPM pipeline source prioritization for Canada — boosts high-signal sources, discards noise
! public: false
! author: MPM Pipeline

! --- Tier 1: Essential (boost=3) ---
$boost=3,site=cbc.ca
$boost=3,site=theglobeandmail.com
$boost=3,site=ici.radio-canada.ca
$boost=3,site=hilltimes.com
$boost=3,site=lapresse.ca

! --- Tier 2: Important (boost=2) ---
$boost=2,site=ledevoir.com
$boost=2,site=ctvnews.ca
$boost=2,site=globalnews.ca
$boost=2,site=bnnbloomberg.ca
$boost=2,site=canada.ca
$boost=2,site=pm.gc.ca
$boost=2,site=cgai.ca

! --- Tier 3: Supplementary (boost=1) ---
$boost=1,site=opencanada.org
$boost=1,site=cigionline.org
$boost=1,site=macdonaldlaurier.ca
$boost=1,site=policyoptions.irpp.org
$boost=1,site=ipolitics.ca

! --- Discard: Noise ---
$discard,site=rebelnews.com
$discard,site=dailyhive.com
$discard,site=narcity.com
$discard,site=torontosun.com
$discard,site=ottawasun.com
```

---

## INTERPRETIVE CONTEXT FOR DOSSIER

### Tier 1 Sources

> Articles from **CBC News** about any domain should be interpreted as Canada's most authoritative general news coverage — its editorial independence as a public broadcaster and its unmatched bureau infrastructure (Parliament Hill, Washington, London, foreign correspondents) make it the default baseline for factual reporting. Murray Brewster's defence reporting is particularly authoritative. CBC's centrist positioning means it reflects the mainstream policy consensus rather than challenging it — absence of a story from CBC is itself a signal that an issue hasn't reached mainstream political salience.

> Articles from **The Globe and Mail** about foreign policy and defence should be interpreted as reflecting Canada's establishment consensus because its centre-right, pro-business, internationalist orientation and its status as the paper of record for policy elites mean its editorial framing shapes how the political class understands Canada's strategic options. Robert Fife and Steven Chase's national security investigations are among the most reliable in the country. Op-eds from former officials published here signal elite opinion shifts — treat these as primary source material for detecting policy-community positioning, not as journalistic reporting.

> Articles from **Radio-Canada** about federal policy should be interpreted as reflecting francophone political culture, which frames sovereignty, immigration, and institutional questions differently than anglophone media — Radio-Canada's coverage of the same federal announcement may emphasize different implications than CBC, and this divergence is analytically meaningful. Higher trust ratings than any English-language equivalent mean its framing has outsized influence on Quebec public opinion, which constrains federal policy through the Bloc Québécois and provincial government.

> Articles from **The Hill Times** about parliamentary and bureaucratic dynamics should be interpreted as insider reporting from the Ottawa policy apparatus — its readership among Cabinet ministers, PMO staff, and senior bureaucrats means stories published here reflect what the political class considers important. Its absorption of Embassy magazine means it carries institutional memory on diplomatic affairs. Thin staffing limits its coverage breadth, but within its niche (parliamentary committees, departmental politics, bureaucratic dynamics), nothing else competes.

> Articles from **La Presse** about domestic and economic policy should be interpreted as reflecting mainstream francophone Quebec opinion with a federalist, centrist-to-centre-left orientation — its nonprofit model and free access mean it reaches the broadest francophone audience, making its editorial framing the closest proxy for how ordinary francophone Canadians understand federal policy choices. Its investigative team has broken significant stories on government contracting and institutional accountability.

### Tier 2 Sources

> Articles from **Le Devoir** about Canada's international positioning should be interpreted as filtered through a Quebec-nationalist/autonomist intellectual lens — Le Devoir's small circulation belies its outsized influence on Quebec's political and academic class. Its framing of federal foreign policy consistently evaluates whether Ottawa's actions respect Quebec's distinct interests and jurisdictional claims. This perspective is essential for understanding domestic constraints on federal external action that anglophone media underestimates.

> Articles from **CTV News** about government policy should be interpreted as mainstream centrist coverage that reflects how the median Canadian voter encounters political news — CTV's mass audience and moderate editorial line make it the best proxy for non-elite public opinion reception of government decisions, but its foreign policy coverage is thinner than CBC or Globe, so absence of a story from CTV suggests the issue hasn't penetrated mass public consciousness.

> Articles from **Global News** about defence and national security should be interpreted as credible specialist reporting — Mercedes Stephenson's defence beat and Global's track record on foreign interference stories (Chinese police stations, Indian diplomatic expulsions) make it the strongest broadcast source for security matters. Its Corus Entertainment ownership and mainstream orientation mean it tends toward hawkish framing on security issues.

> Articles from **BNN Bloomberg** about trade, tariffs, and economic policy should be interpreted as reflecting the perspective of Canada's business and financial community — its Bloomberg partnership means economic analysis is framed through an investor/market-impact lens. Negative coverage of protectionist measures or government economic intervention reflects business-community anxiety rather than objective policy failure.

> Articles from **canada.ca** and **pm.gc.ca** should be interpreted as official government communications — not journalism but primary source material. Press releases, policy documents, and ministerial statements represent the government's chosen public position, which may diverge from actual policy direction. The gap between what appears here and what appears in Hill Times or Globe investigations is analytically meaningful.

> Articles from **CGAI** about defence and security policy should be interpreted as reflecting the perspective of Canada's retired military and defence establishment — its contributor base of former generals, defence attachés, and security officials means analysis is informed by institutional knowledge but may reflect the biases of the defence community (pro-spending, pro-NATO, skeptical of diplomatic alternatives to military capacity).

### Tier 3 Sources

> Articles from **OpenCanada**, **CIGI**, **MLI**, and **Policy Options** should be interpreted as think-tank analysis providing structural depth rather than breaking news — each reflects the analytical orientation of its institutional home (OpenCanada: internationalist-liberal; CIGI: tech-governance multilateralist; MLI: conservative-realist hawkish; Policy Options: academic-centrist bilingual). These sources explain *why* events matter for Canada's strategic positioning rather than reporting *what* happened.

> Articles from **iPolitics** about Ottawa insider dynamics should be interpreted as supplementary parliamentary coverage — thinner than Hill Times but occasionally surfaces caucus dynamics, backbench dissent, and policy leaks that don't appear in mainstream outlets. Treat as a secondary signal for parliamentary politics rather than a primary source.

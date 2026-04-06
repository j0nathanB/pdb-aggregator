I need to verify several current facts about Pakistan's media landscape before completing this audit.
Now I have sufficient information to complete the audit. Let me compile the findings.

---

#### AUDIT SUMMARY: Pakistan

**Sources assessed:** 19 recommended + 6 excluded + 2 newly identified = 27 total
**Tier 1 (boost=3):** 4 sources
**Tier 2 (boost=2):** 8 sources
**Tier 3 (boost=1):** 8 sources
**Neutral (no rule):** 4 sources
**Discard:** 3 sources
**Overall assessment:** The curation prompt produced a high-quality whitelist that accurately reflects Pakistan's information architecture. The major updates required are: (1) incorporating the dramatically changed security environment post-May 2025 India-Pakistan conflict and the ongoing February-March 2026 Afghanistan-Pakistan war into query vocabulary; (2) adding the International Crisis Group as a missing analytical source critical for conflict monitoring; (3) promoting Daily Jang from implicit Tier 2 consideration to confirmed Tier 2 given the pipeline's need for Urdu-language domestic signals; and (4) flagging ISPR and APP as Layer 2 migration candidates. The curation prompt's structural analysis, editorial orientation descriptions, and interpretive context are exceptionally well-crafted and require only minor updates.

---

#### BOOST ASSIGNMENTS

##### Tier 1 — `$boost=3`

**Dawn** | `dawn.com` | Type: `paper_of_record` | Status: `EXISTING`
- **Structural role:** Pakistan's most editorially independent English-language daily; the single outlet most consistently willing to challenge establishment narratives on military accountability, Balochistan, and civil-military relations.
- **Domain coverage:** Diplomatic alignment; Domestic constraints; Economic & technological statecraft; Security & defense autonomy (limited by establishment red lines but still the best available)
- **Reasoning:** 
Dawn's financial distress — with federal and Punjab governments withholding advertisements for five consecutive months — is itself a regime behavior indicator.
 
The closure of Aurora magazine in August 2025 and DawnNews.tv Urdu digital platform on December 1, 2025
 confirms the whitelist's assessment of financial strangulation while the flagship `dawn.com` remains operational. Irreplaceable Tier 1.

**Geo News / Geo.tv** | `geo.tv` | Type: `paper_of_record` | Status: `EXISTING`
- **Structural role:** Pakistan's most-watched Urdu news channel; mass-audience signal vehicle whose divergence from ARY signals establishment control dynamics.
- **Domain coverage:** Domestic constraints; Diplomatic alignment; Security & defense autonomy
- **Reasoning:** 
The Jang Group terminated 80 employees in May from Jang Rawalpindi and The News, followed by 137 layoffs in June from Awaz,
 confirming the systemic financial pressure but the outlet remains operationally dominant. Geo-ARY divergence analysis remains the single most useful establishment-control indicator.

**The News International** | `thenews.com.pk` | Type: `paper_of_record` | Status: `EXISTING`
- **Structural role:** Jang Group's English-language flagship; widest-read English daily after Dawn; comprehensive event coverage, parliamentary reporting, and government policy announcements.
- **Domain coverage:** Economic & technological statecraft; Diplomatic alignment; Domestic constraints
- **Reasoning:** Confirmed Tier 1. Despite Jang Group financial pressures, The News remains the most comprehensive English-language event reporting outlet. Provides breadth where Dawn provides depth.

**ISPR (Inter-Services Public Relations)** | `ispr.gov.pk` | Type: `government_aligned` | Status: `EXISTING` | **LAYER 2 MIGRATION**
- **Structural role:** Official strategic communication arm of the Pakistan Armed Forces; first-mover on all defense and security information. 
Its executive authority, a director-general, is a chief military spokesperson. In 2024, ISPR underwent reorganization and expansion, with two two-star Major-general rank officers appointed to handle foreign/strategic communication and domestic media.

- **Domain coverage:** Security & defense autonomy; Diplomatic alignment
- **Reasoning:** 
ISPR's press releases on counter-terrorism operations
 now use distinctive "Indian Proxy, Fitna al Khwarij" framing for TTP, and the terminology "Fitna Al Hindustan" for BLA — these framings are themselves analytical signals about the establishment's strategic communication posture. The website is confirmed active and regularly updated. Primary fetch should migrate to Layer 2 direct polling of `ispr.gov.pk/press-release-archive`; Goggle boost retained as fallback. Still Tier 1 because no substitute exists for this function.

##### Tier 2 — `$boost=2`

**Express Tribune** | `tribune.com.pk` | Type: `business_financial` | Status: `EXISTING`
- **Structural role:** Pakistan's strongest general-audience business journalism; CPEC, IMF, trade policy specialist.
- **Domain coverage:** Economic & technological statecraft; Domestic constraints
- **Reasoning:** Confirmed Tier 2. Fills the business/financial niche distinctly from Dawn and The News. Former NYT partnership legacy editorial standards persist.

**Business Recorder** | `brecorder.com` | Type: `business_financial` | Status: `EXISTING`
- **Structural role:** Pakistan's dedicated financial press; highest-reliability source for economic data and SBP releases.
- **Domain coverage:** Economic & technological statecraft
- **Reasoning:** 
Business Recorder is an English-language financial daily newspaper in Pakistan, founded in 1965.
 
Current content confirms active publishing as of April 2026 with editorials on oil price impacts, LSM index, and fiscal analysis.
 Website appears free to access; no paywall confirmed. Tier 2 confirmed.

**ARY News** | `arynews.tv` | Type: `government_aligned` | Status: `EXISTING`
- **Structural role:** Semi-official channel for military-security narratives; establishment echo whose editorial choices reveal what the military wants the public to believe.
- **Domain coverage:** Security & defense autonomy; Domestic constraints
- **Reasoning:** Confirmed Tier 2. Post-May 2025 conflict, ARY's value as an establishment signaling vehicle has increased given the heightened security discourse.

**Daily Jang** | `jang.com.pk` | Type: `paper_of_record` | Status: `EXISTING`
- **Structural role:** Pakistan's largest-circulation Urdu daily; carries political factional signals in Urdu-language commentary that don't propagate to English outlets.
- **Domain coverage:** Domestic constraints; Diplomatic alignment
- **Reasoning:** Confirmed Tier 2. Under the non-English premium principle, Jang's Urdu-language domestic signals justify its tier. Despite Jang Group financial pressures, it remains the highest-circulation Urdu daily.

**The Diplomat** | `thediplomat.com` | Type: `political_specialist` | Status: `EXISTING`
- **Structural role:** External analytical outlet providing structural depth unconstrained by Pakistani establishment pressure.
- **Domain coverage:** Diplomatic alignment; Security & defense autonomy; Institutional engagement
- **Reasoning:** Confirmed Tier 2. Post-May 2025 conflict and February 2026 Afghanistan-Pakistan war, The Diplomat's analytical framing of Pakistan within regional geopolitical contexts is more valuable than ever.

**Associated Press of Pakistan (APP)** | `app.com.pk` | Type: `government_aligned` / `wire` | Status: `EXISTING` | **LAYER 2 MIGRATION**
- **Structural role:** State-run news agency; authoritative source for government policy announcements, bilateral agreement signings, official state visits.
- **Domain coverage:** Diplomatic alignment; Institutional engagement
- **Reasoning:** Confirmed Tier 2. Layer 2 migration candidate for direct polling. Goggle boost retained as belt-and-suspenders.

**Al Jazeera (Pakistan coverage)** | `aljazeera.com` | Type: `wire` / `regional` | Status: `EXISTING`
- **Structural role:** Fills the critical gap of covering stories Pakistani domestic media self-censors — PTI crackdowns, Balochistan operations, enforced disappearances. 
Al Jazeera's Kamal Hyder reported from Islamabad during the February 2026 Afghanistan-Pakistan conflict,
 and Al Jazeera provided some of the most detailed coverage of the cross-border hostilities.
- **Domain coverage:** Domestic constraints; Security & defense autonomy; Diplomatic alignment
- **Reasoning:** Confirmed Tier 2. Its Islamabad bureau coverage during both the May 2025 India-Pakistan conflict and the February 2026 Afghanistan-Pakistan war demonstrates it fills a critical crisis-reporting gap.

**International Crisis Group (Pakistan)** | `crisisgroup.org` | Type: `think_tank` / `investigative` | Status: `NEW`
- **Structural role:** Provides the most timely and authoritative analytical briefings on Pakistan's conflict dynamics, civil-military relations, and regional security crises.
- **Domain coverage:** Security & defense autonomy; Domestic constraints; Diplomatic alignment
- **Reasoning:** 
Crisis Group's Pakistan coverage tracks the October 2025 ceasefire collapse, BLA offensives, and army counter-insurgency operations in granular detail.
 Its CrisisWatch monthly monitoring and rapid-response briefings are essential for the pipeline's conflict tracking. More event-driven and timely than IPRI; deserves Tier 2 for analytical depth on conflict dynamics.

##### Tier 3 — `$boost=1`

**Pakistan Today** | `pakistantoday.com.pk` | Type: `political_specialist` | Status: `EXISTING`
- **Structural role:** Lahore-based English daily providing Punjab-centric political coverage. 
Pakistan Today's Profit section published the Ministry of Finance's economic outlook analysis including inflation projections and current account data,
 showing ongoing utility for economic coverage.
- **Domain coverage:** Domestic constraints; Economic & technological statecraft
- **Reasoning:** Confirmed Tier 3. Adds geographic diversity (Punjab perspective) but partially redundant with Dawn/The News.

**The Friday Times** | `thefridaytimes.com` | Type: `investigative` / `political_specialist` | Status: `EXISTING`
- **Structural role:** Liberal investigative/analytical publication; insider-critical perspective on civil-military dynamics. 
TFT is a Pakistani English-language online publication based in Lahore.
 
As recently as March 2026, TFT published substantive security analysis noting Pakistan was ranked as the most "terrorism-impacted" country globally in the GTI 2026.

- **Domain coverage:** Domestic constraints; Diplomatic alignment; Security & defense autonomy
- **Reasoning:** Confirmed Tier 3. Active and publishing substantive analytical content. Founder Najam Sethi's insider-critical lens remains distinctive.

**Naya Daur Media** | `nayadaur.tv` | Type: `opposition_aligned` / `investigative` | Status: `EXISTING`
- **Structural role:** Digital-native progressive platform covering human rights violations, enforced disappearances, and opposition suppression. 
Naya Daur Media is a bi-lingual progressive digital media platform.
 
Has historically faced website blocks in Pakistan for PTM-related content.

- **Domain coverage:** Domestic constraints
- **Reasoning:** Confirmed Tier 3. Essential for Domestic Constraints domain despite advocacy orientation. Access within Pakistan remains intermittent but content accessible internationally for the pipeline.

**Dawn News Urdu** | `dawnnews.tv` | Type: `paper_of_record` | Status: `EXISTING` — **CONFIDENCE: LOW**
- **Structural role:** Dawn Media Group's Urdu TV/digital platform. 
DawnNews.tv was formally closed on December 1, 2025, terminating 12 media workers.
 The TV channel may still broadcast, but the digital footprint has been severely diminished.
- **Domain coverage:** Domestic constraints; Diplomatic alignment
- **Reasoning:** Retained at Tier 3 as belt-and-suspenders; if any content surfaces via the domain, it carries Dawn-quality editorial standards. The closure itself is a structural indicator. **Uncertainty flag: domain may be redirected or defunct.**

**Reuters / AFP** | `reuters.com` / `france24.com` | Type: `wire` | Status: `EXISTING`
- **Structural role:** International wire services providing event-detection baseline when domestic media is throttled. During the May 2025 conflict, wire services were among the few with operational correspondents when domestic digital media was disrupted.
- **Domain coverage:** Diplomatic alignment; Security & defense autonomy; Economic & technological statecraft
- **Reasoning:** Confirmed Tier 3. Reuters paywall remains a concern for extraction but not for Brave News Search discovery.

**IPRI (Islamabad Policy Research Institute)** | `ipripak.org` | Type: `think_tank` | Status: `EXISTING`
- **Structural role:** Government-affiliated think tank revealing how Pakistan's security establishment conceptualizes strategic challenges.
- **Domain coverage:** Diplomatic alignment; Security & defense autonomy; Institutional engagement
- **Reasoning:** Confirmed Tier 3 (dropped from consideration for Tier 2 because the newly added International Crisis Group fills the analytical/think tank role more effectively for event-driven coverage). IPRI's value is in longer-term strategic thinking indicators.

**ProPakistani** | `propakistani.pk` | Type: `business_financial` / `political_specialist` | Status: `EXISTING`
- **Structural role:** Digital-native tech/telecom/digital economy specialist.
- **Domain coverage:** Economic & technological statecraft
- **Reasoning:** Confirmed Tier 3. Fills the technology statecraft niche uniquely.

**Samaa TV / Samaa English** | `samaaenglish.tv` | Type: `regional` | Status: `EXISTING`
- **Structural role:** Sindh/Karachi-focused coverage providing geographic diversity.
- **Domain coverage:** Domestic constraints; Economic & technological statecraft
- **Reasoning:** Confirmed Tier 3. Adds Sindh perspective on national events.

##### Neutral — no Goggle rule

**PTV News** | `ptv.com.pk` | Status: `LEFT AT ORGANIC`
- **Why neutral:** Entirely redundant with APP for policy announcements and adds no analytical value beyond ARY. 
PTV staff protested months of delayed wages,
 raising operational reliability concerns. May surface organically for official government ceremony coverage.

**Nawa-i-Waqt** | `nawaiwaqt.com.pk` | Status: `LEFT AT ORGANIC`
- **Why neutral:** Strong right-wing/establishment editorial line makes it redundant with ARY + Daily Jang. Under the Goggle model, it can surface organically for religious party positioning and conservative commentary signals without a boost.

**Dunya News** | `dunyanews.tv` | Status: `PROMOTED FROM DISCARD TO NEUTRAL`
- **Why neutral:** The curation prompt discarded Dunya for close PML-N alignment and low-quality English-language web content. Under the Goggle model, its PML-N proximity is actually a potential signal — when the ruling coalition wants to float trial balloons, PML-N-aligned outlets carry them. Removing it from discard allows serendipitous discovery of government leak channel content. Not harmful enough to discard; not valuable enough to boost.

**The Nation (Pakistan)** | `nation.com.pk` | Status: `PROMOTED FROM DISCARD TO NEUTRAL`
- **Why neutral:** Right-wing/pro-establishment orientation is redundant with ARY but not positively harmful. Under the Goggle model, it can surface organically for conservative establishment perspectives. Its conspiratorial framing is occasional, not systematic enough to warrant active discard.

##### Discard — `$discard`

**Bol News** | `bolnews.com` | Status: `CONFIRMED DISCARD`
- **Discard reasoning:** Documented pattern of inflammatory, unverified reporting; owner Shoaib Ahmed Shaikh faced fraud charges; would displace higher-quality results on political and security queries with sensationalist content.

**92 News** | `92newshd.tv` | Status: `CONFIRMED DISCARD`
- **Discard reasoning:** Pure aggregation outlet with no original reporting; republishes ISPR/government press releases without value-add; would consume result slots that ISPR.gov.pk fills more directly.

**Daily Pakistan** | `en.dailypakistan.com.pk` | Status: `CONFIRMED DISCARD`
- **Discard reasoning:** Click-driven aggregator with sensationalized headlines and SEO-optimized content that would displace analytical sources from top results.

**Republic TV (India)** | `republicworld.com` | Status: `CONFIRMED DISCARD`
- **Discard reasoning:** Extreme anti-Pakistan editorial bias with inflammatory framing and unverified claims; would severely degrade result quality on any Pakistan-related query.

---

#### STRUCTURAL COVERAGE CHECK

| Structural Role | Source(s) | Tier | Notes |
|---|---|---|---|
| Government leak channel / policy kite-flying | ARY News; The News International; Dunya News (organic) | Tier 2; Tier 1; Neutral | Dunya moved to neutral from discard to capture PML-N leak channel function organically |
| Opposition voice | Naya Daur Media; Al Jazeera (Pakistan) | Tier 3; Tier 2 | Coverage adequate; Naya Daur's intermittent access within Pakistan noted |
| Defence/security first-mover | ISPR | Tier 1 | **LAYER 2 MIGRATION** — primary fetch via direct polling; Goggle as fallback |
| Policy-elite discourse | Dawn; The News International; Business Recorder | Tier 1; Tier 1; Tier 2 | Comprehensive coverage of what decision-makers read |
| Domestic-language depth | Daily Jang; Geo News (Urdu) | Tier 2; Tier 1 | Urdu-language cycle for Domestic Constraints domain |
| Official government source | APP; ISPR | Tier 2; Tier 1 | Both flagged as **LAYER 2 MIGRATION** |
| Analytical/think tank depth | International Crisis Group; The Diplomat; IPRI | Tier 2; Tier 2; Tier 3 | ICG addition fills gap for event-driven conflict analysis |
| Wire service (local bureau) | Reuters/AFP; Al Jazeera | Tier 3; Tier 2 | Adequate; Al Jazeera's Islamabad bureau provides strongest local wire function |

**Gaps identified:**
1. **Afghanistan-Pakistan border coverage** — The February-March 2026 conflict has created a new permanent coverage gap. No boosted source has correspondents in the border tribal areas. Dawn, Al Jazeera, and ICG represent the best available but all acknowledge significant reporting gaps. **No actionable remedy within available outlets.**
2. **Military procurement and nuclear posture** — Post-May 2025 conflict, 
Pakistan now relies almost entirely on Chinese military hardware
 and 
US DNI warnings about potential Pakistani ICBM capability
 have elevated this gap's significance. The Bulletin of the Atomic Scientists and SIPRI provide periodic assessments but not event-driven coverage. Consider adding `sipri.org` at Tier 3 for arms transfer data.
3. **Parliamentary proceedings** — `na.gov.pk` and `senate.gov.pk` should be Layer 2 direct fetch targets for opposition speeches and budget debates not covered in media.

---

#### REDUNDANCY RESOLUTION

**Dawn / The News International cluster:** Both are English-language papers of record covering all five domains. Resolved by keeping both at Tier 1 because they serve distinct functions: Dawn provides investigative/analytical depth with editorial independence; The News provides comprehensive event coverage with wider ideological range in opinion columns. Dawn is structurally unique; The News represents the Jang Group's English voice. The divergence between them is itself an analytical signal.

**Geo News / ARY News / Samaa TV cluster:** All are Urdu-dominant TV news with English web portals covering domestic politics and security. Resolved: Geo (Tier 1) as the mass-audience leader with occasional editorial independence; ARY (Tier 2) as the establishment signaling vehicle; Samaa (Tier 3) for Sindh/Karachi geographic diversity. Geo-ARY divergence is the primary analytical signal.

**Express Tribune / Business Recorder / ProPakistani cluster:** All cover economic/financial domains. Resolved: Express Tribune (Tier 2) as strongest general-audience business journalism; Business Recorder (Tier 2) as specialist financial data source; ProPakistani (Tier 3) as digital economy niche. No redundancy — each fills a distinct sub-domain.

**The Diplomat / International Crisis Group / IPRI cluster:** All provide analytical depth. Resolved: ICG (Tier 2, new) for event-driven conflict analysis; The Diplomat (Tier 2) for regional geopolitical framing; IPRI (Tier 3) for establishment strategic thinking indicators. Minimal redundancy — ICG and The Diplomat are external/independent, IPRI is establishment-affiliated.

**Dawn / Al Jazeera on Domestic Constraints:** Both cover opposition suppression, Balochistan, human rights. Resolved by keeping both boosted: Dawn (Tier 1) as the domestic outlet pushing boundaries; Al Jazeera (Tier 2) as the external outlet covering what Dawn self-censors. Together they provide the most complete Domestic Constraints picture available.

---

#### QUERY CONFIGURATION

```
country: PK
search_lang: en
freshness: pw
```

**Multi-language notes:** Pakistan's media operates in both English and Urdu. English-language queries capture policy-elite discourse (Dawn, The News, Express Tribune, Business Recorder) and international coverage (Al Jazeera, Reuters, The Diplomat, ICG). Urdu-language queries (`search_lang: ur`) should be run as a supplementary cycle for the Domestic Constraints domain, targeting Jang and Geo for opposition/coalition dynamics, religious party positioning, and public sentiment. For the other four domains, English-language queries are sufficient.

**Localized query vocabulary validation:**

The curation prompt's vocabulary is strong but requires updates for the dramatically changed security environment:

*Diplomatic Alignment — updates needed:*
- `"Asim Munir" visit` → Update to `"Field Marshal" Asim Munir` — 
Asim Munir was promoted to Field Marshal on May 20, 2025
 and all ISPR references now use this title
- **ADD:** `"Afghanistan" Pakistan "open war"` — 
Pakistan's defense minister declared "an open war"
 with Afghanistan in February 2026; this is now the dominant bilateral diplomatic/security story
- **ADD:** `Pakistan Iran mediation` — 
Pakistan has emerged as a global crisis mediator amid the US war on Iran

- `"all-weather friendship"` — Still valid but increasingly supplemented by "iron brother" in official discourse

*Security & Defense Autonomy — updates needed:*
- **ADD:** `"Fitna al Khwarij" OR "Fitna al Hindustan"` — 
ISPR's current terminology for TTP and BLA respectively; "Indian Proxy" framing is now standard

- **ADD:** `"Operation Radd-ul-Fitna"` — 
Active counter-insurgency operation in Balochistan concluded in early 2026

- `"JF-17" OR "J-35" procurement` → Update to include `"J-10C" OR "HQ-9" OR "PL-15"` — 
Pakistan's May 2025 combat use of J-10C, PL-15, and HQ-9 systems
 has made these the current reference platforms
- `"full spectrum deterrence"` — Still valid; 
Pakistan continues to pursue this posture

- **ADD:** `"ICBM" Pakistan` — 
US DNI testimony that Pakistan may be developing ICBM capability
 is a new monitoring requirement
- **ADD:** `"Operation Sindoor" aftermath OR lessons` — Post-conflict analysis and reconstitution signals

*Economic & Technological Statecraft — updates needed:*
- `"IMF review" Pakistan` — Still valid but add year `2026` to freshness filter
- **ADD:** `"oil price" Pakistan impact` — 
Business Recorder editorials on oil price shockwave and foreign exchange buffer needs
 reflect the Iran conflict's economic impact on Pakistan
- **ADD:** `"Indus Waters" suspension impact` — 
India's decision to suspend the Indus Water Treaty will substantially damage Pakistan's agriculture


*Institutional Engagement — updates needed:*
- **ADD:** `Pakistan "peace talks" Afghanistan China` — 
Pakistan says a new round of peace talks with Afghanistan is underway in China

- `"BRICS" Pakistan membership` — Still valid
- **ADD:** `Pakistan "Nobel Peace Prize" Trump` — 
Pakistan announced it would nominate Donald Trump for the Nobel Peace Prize
 — this is an indicator of Pakistan-US alignment dynamics

*Domestic Constraints — updates needed:*
- `"PECA" Pakistan` — More critical than ever; 
the 2025 PECA amendment creates the Social Media Protection and Regulatory Authority (SMPRA) with sweeping powers to monitor, regulate, and remove content

- **ADD:** `"SMPRA" OR "Digital Rights Protection Authority"` — the new regulatory bodies under PECA 2025
- **ADD:** `Pakistan journalists "life imprisonment"` — 
In January 2026, an anti-terrorism court sentenced multiple journalists and social media personalities to life imprisonment

- **ADD:** `"KP" Afghanistan border PTI` — 
Khan's PTI controls KP province bordering Afghanistan,
 creating a civil-military-provincial governance dynamic

*Stale or problematic terms:*
- `"SMDA" OR "Saudi defence pact"` — Insufficient search volume; recommend broadening to `"Saudi" Pakistan defense cooperation`
- `"Nasr missile"` — Still valid but less current than Shaheen-III and Ababeel for tracking nuclear posture
- `"Section 144" Islamabad` — Too narrow; replace with `Pakistan protest "ban" OR "shutdown" OR "Section 144"`

**Suggested topic query patterns:**

1. `"Field Marshal" Asim Munir Afghanistan China` — Captures CDF diplomatic engagements on the Afghanistan-Pakistan crisis
2. `Pakistan IMF review 2026` — Captures quarterly program compliance against post-conflict economic pressure
3. `Pakistan Afghanistan ceasefire 2026` — Captures the dominant security story
4. `"PECA" Pakistan journalist arrest OR sentence` — Captures press freedom deterioration under new legal framework
5. `"Indus Waters Treaty" suspension Pakistan impact` — Captures the India-Pakistan water dispute's economic and diplomatic consequences

---

#### GOGGLE FILE

```goggle
! name: MPM Pakistan
! description: MPM pipeline source prioritization for Pakistan — boosts high-signal sources, discards noise
! public: false
! author: MPM Pipeline

! --- Tier 1: Essential (boost=3) ---
$boost=3,site=dawn.com
$boost=3,site=geo.tv
$boost=3,site=thenews.com.pk
$boost=3,site=ispr.gov.pk

! --- Tier 2: Important (boost=2) ---
$boost=2,site=tribune.com.pk
$boost=2,site=brecorder.com
$boost=2,site=arynews.tv
$boost=2,site=jang.com.pk
$boost=2,site=thediplomat.com
$boost=2,site=app.com.pk
$boost=2,site=aljazeera.com
$boost=2,site=crisisgroup.org

! --- Tier 3: Supplementary (boost=1) ---
$boost=1,site=pakistantoday.com.pk
$boost=1,site=thefridaytimes.com
$boost=1,site=nayadaur.tv
$boost=1,site=dawnnews.tv
$boost=1,site=reuters.com
$boost=1,site=france24.com
$boost=1,site=ipripak.org
$boost=1,site=propakistani.pk
$boost=1,site=samaaenglish.tv

! --- Discard: Noise ---
$discard,site=bolnews.com
$discard,site=92newshd.tv
$discard,site=en.dailypakistan.com.pk
$discard,site=republicworld.com
```

---

#### INTERPRETIVE CONTEXT FOR DOSSIER

**Tier 1 Sources:**

> Articles from **Dawn** about military operations, Balochistan, the Afghanistan-Pakistan conflict, or civil-military relations should be interpreted as the most editorially independent reporting available in Pakistan's domestic press; if Dawn reports a fact the government denies, default to Dawn's account pending contradictory evidence, because Dawn's editorial tradition prioritizes factual accuracy even at the cost of establishment displeasure — a cost now quantified by five consecutive months of federal and Punjab government advertising withdrawal.

> Articles from **Dawn** about economic policy, IMF compliance, or the post-conflict economic outlook should be interpreted as analytically reliable but editorially sympathetic to reform; Dawn's liberal-secular orientation frames IMF conditionality as necessary discipline rather than external imposition, potentially underweighting the domestic political costs and the military's economic interests (DHA, Fauji Foundation).

> Articles from **Geo News** about political crises, protests, or PTI should be interpreted as reflecting the Jang Group's current positioning relative to the establishment — when Geo's coverage aligns with ARY, the establishment narrative is unified; when Geo diverges from ARY, it signals either that the Jang Group is testing establishment tolerance or that the establishment itself is factionally divided.

> Articles from **Geo News** about the India-Pakistan or Afghanistan-Pakistan conflicts should be interpreted as constrained by the same establishment red lines as all Pakistani media; Geo will not contradict ISPR's narrative on active operations, making it unreliable for independent assessment of military claims during conflict.

> Articles from **The News International** about economic policy, parliamentary proceedings, or government decision-making should be interpreted as generally reliable event reporting with moderate establishment accommodation; opinion pieces by contributors like Mosharraf Zaidi carry significantly more independent analytical value than straight news copy, particularly on civil-military dynamics.

> Articles from **ISPR** about any topic should be interpreted as deliberate strategic communication from the Pakistan Armed Forces; the current "Fitna al Khwarij" and "Indian Proxy" framing for TTP/BLA is a deliberate narrative construction tying domestic insurgency to the India threat; threat assessments should be discounted by at least one severity level, own-casualty figures treated as likely understated, and adversary casualty figures (whether TTP, BLA, Afghan Taliban, or Indian) treated as likely overstated; the timing and topic selection of ISPR statements are themselves analytical signals about what the military wants audiences to focus on.

**Tier 2 Sources:**

> Articles from **Express Tribune** about CPEC, trade policy, IMF program compliance, or post-conflict economic restructuring should be interpreted as Pakistan's strongest general-audience business journalism; its coverage of military-economic interests is constrained by establishment pressure.

> Articles from **Business Recorder** about SBP data, fiscal policy, energy sector economics, or oil price impacts should be interpreted as the most technically accurate financial reporting in Pakistan; its audience (business community, economic policymakers, IMF mission) incentivizes data accuracy over political framing.

> Articles from **ARY News** about India, Afghanistan, Kashmir, security operations, or PTI should be interpreted as establishment-sympathetic signaling; when ARY leads with a particular framing before ISPR has published, it may indicate advance guidance from the military, making it a useful early indicator of establishment messaging direction.

> Articles from **Daily Jang** about coalition politics, religious party dynamics, or public sentiment on the Afghanistan-Pakistan conflict should be interpreted as reflecting both the Jang Group's editorial positioning and the discourse of Pakistan's Urdu-speaking political mainstream; editorial columns carry political signaling from establishment-connected commentators that does not always appear in English-language press.

> Articles from **The Diplomat** about Pakistan-China relations, nuclear doctrine, the May 2025 conflict aftermath, or constitutional developments should be interpreted as externally positioned analytical work unconstrained by Pakistani establishment pressure; should be cross-referenced with Dawn and The News for factual grounding.

> Articles from **APP** about bilateral agreements, official visits, ceasefire announcements, or government policy should be interpreted as verbatim government communication; the absence of a story from APP when other outlets are reporting it signals the government has not yet decided on its official position, which is itself an analytical signal.

> Articles from **Al Jazeera** about PTI suppression, Balochistan, enforced disappearances, the Afghanistan-Pakistan conflict, or human rights should be interpreted as the most reliable available reporting on topics Pakistani domestic media self-censors; Al Jazeera's Islamabad bureau correspondents have demonstrated operational continuity during both the May 2025 and February 2026 conflicts.

> Articles from **International Crisis Group** about Pakistan's conflict dynamics, civil-military relations, Afghanistan-Pakistan tensions, or BLA/TTP operations should be interpreted as the most analytically rigorous event-driven conflict analysis available from external observers; ICG's methodology combines local source networks with international analytical frameworks, producing assessments that neither Pakistani establishment sources nor Pakistani domestic media can match for balanced conflict reporting.
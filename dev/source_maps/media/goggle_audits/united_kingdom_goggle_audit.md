# AUDIT SUMMARY: UNITED KINGDOM

**Sources assessed:** 18 recommended + 5 excluded + 4 newly identified = 27 total
**Tier 1 (boost=3):** 4 sources
**Tier 2 (boost=2):** 8 sources
**Tier 3 (boost=1):** 5 sources
**Neutral (no rule):** 6 sources
**Discard:** 4 sources
**Overall assessment:** The curation prompt produced a strong whitelist with exceptional think-tank and defence-specialist depth — the RUSI/IISS/Chatham House triad is world-class and correctly identified. Key changes: (1) resolved redundancy within the three defence/security think tanks by differentiating tiers based on operational relevance; (2) promoted government official sources (gov.uk, parliament.uk) for Layer 2 migration; (3) flagged a critical extraction problem — 8 of 18 recommended sources are blocked by Anthropic's crawler, including BBC, FT, Guardian, Times, Telegraph, Economist, Politico Europe, and Reuters. This is the most severe crawler-blocking problem of any country audited so far; the UK's extractable source base is dramatically thinner than its discoverable source base. (4) Added missing structural sources: Private Eye (leak/scandal channel), openDemocracy (promoted from exclusion to Tier 3 for investigative function), AP News (unblocked wire fallback), and Bellingcat (OSINT investigations with UK nexus).

---

## BOOST ASSIGNMENTS

### Tier 1 — `$boost=3`

**RUSI (Royal United Services Institute)** | `rusi.org` | Type: `security_defense` | Status: `EXISTING`
- **Structural role:** The world's oldest defence and security think tank, directly embedded in the UK defence-policy establishment. Named Foreign Policy Think Tank of the Year. Cited in parliamentary debates and the 2025 Strategic Defence Review.
- **Domain coverage:** Security & defence autonomy, Diplomatic alignment, Economic & technological statecraft
- **Reasoning:** In the UK's media ecosystem, RUSI fills a role more important than in most countries: it is the primary source of original defence analysis that shapes policy debate. Think tanks earn boost through depth not speed, and RUSI has unmatched depth on UK defence procurement, nuclear deterrent policy, and NATO commitments. Critically, `rusi.org` is NOT blocked by Anthropic's crawler — making it one of the few high-value UK sources the pipeline can reliably extract. With BBC, FT, Guardian, Times, and Telegraph all blocked, extractable analytical sources must be prioritized. Most commentary is free.

**Chatham House** | `chathamhouse.org` | Type: `political_specialist` | Status: `EXISTING`
- **Structural role:** UK's flagship foreign-affairs think tank. Publishes *International Affairs* journal. "UK in the World" programme directly tracks the country's strategic posture.
- **Domain coverage:** Diplomatic alignment, Institutional engagement, Economic & technological statecraft
- **Reasoning:** Chatham House occupies the diplomatic-alignment lane that RUSI occupies for defence. Its post-Brexit trade analysis, Indo-Pacific tilt tracking, and multilateral engagement coverage are unmatched by any domestic media outlet. Like RUSI, `chathamhouse.org` is NOT blocked — making it an essential extractable source for the pipeline. Tier 1 because in a country where most broadsheets are blocked, the think tanks that produce original analysis AND can be extracted become primary rather than supplementary.

**UK Defence Journal** | `ukdefencejournal.org.uk` | Type: `security_defense` | Status: `EXISTING — PROMOTED FROM TIER 3`
- **Structural role:** Free-access defence news outlet that breaks procurement and capability stories. Submitted written evidence to parliamentary defence committees. Fills the accessible-defence-news gap left by Janes's paywall.
- **Domain coverage:** Security & defence autonomy
- **Reasoning:** Promoted to Tier 1 because of the extraction crisis. With BBC, Telegraph (strong defence desk), and The Times (establishment leak channel) all blocked, the pipeline needs an extractable first-mover on defence stories. UK Defence Journal is free, unblocked, and has demonstrated the ability to break stories (HMS Prince of Wales breakdown). Narrow domain scope but irreplaceable structural function as the only extractable daily-frequency defence source. In a normal extraction environment this would be Tier 2; the blocked-domain situation elevates it.

**IISS (International Institute for Strategic Studies)** | `iiss.org` | Type: `security_defense` | Status: `EXISTING — PROMOTED FROM TIER 2`
- **Structural role:** Publishes *The Military Balance* and *Survival* journal. Hosts Shangri-La Dialogue and Manama Dialogue — conferences that are themselves signals of UK strategic engagement.
- **Domain coverage:** Security & defence autonomy, Diplomatic alignment
- **Reasoning:** Alongside RUSI, forms the essential defence-analytical pair. IISS provides the global strategic context that RUSI's UK-focused work does not. Its conference hosting means it generates primary-source signals (who attends, what is said at Shangri-La). Not blocked by Anthropic's crawler. Commentary is free. Promoted to Tier 1 because the pipeline's ability to extract UK defence analysis depends almost entirely on the RUSI + IISS + UK Defence Journal triad.

---

### Tier 2 — `$boost=2`

**The Guardian** | `theguardian.com` | Type: `paper_of_record` | Status: `EXISTING`
- **Structural role:** Primary centre-left broadsheet. Strong investigative tradition (Snowden, WikiLeaks). Extensive foreign correspondent network. Free access model.
- **Domain coverage:** Diplomatic alignment, Domestic constraints, Institutional engagement
- **Reasoning:** Would be Tier 1 in a normal extraction environment — it's the UK's most accessible quality broadsheet (no paywall) and provides the essential centre-left policy lens. Demoted to Tier 2 because `theguardian.com` is **blocked by Anthropic's crawler**. Brave can still discover and rank Guardian articles, so the boost ensures they surface in results — the pipeline benefits from seeing Guardian headlines and snippets even without full extraction. The dossier LLM can reason from headlines.
- **Extraction note:** BLOCKED — `theguardian.com` in `blocked_domains.md`. Brave discovery works; extraction will fail.

**BBC News** | `bbc.co.uk` / `bbc.com` | Type: `paper_of_record` | Status: `EXISTING`
- **Structural role:** Most-used news source across the UK political spectrum. Statutory impartiality obligation. BBC World Service is a UK soft-power instrument.
- **Domain coverage:** Diplomatic alignment, Security & defence, Institutional engagement, Domestic constraints
- **Reasoning:** BBC is the single most important UK news source by reach, credibility, and breadth. In a normal extraction environment it would be Tier 1. Demoted to Tier 2 because both `bbc.co.uk` AND `bbc.com` are **blocked by Anthropic's crawler**. Like the Guardian, Brave discovery still works and headlines provide signal. Tier 2 ensures BBC articles still rank highly in Brave results even though extraction will fail.
- **Extraction note:** BLOCKED — both `bbc.co.uk` and `bbc.com` in `blocked_domains.md`. Brave discovery works; extraction will fail.

**GOV.UK (HM Government official)** | `gov.uk` | Type: `government_aligned` | Status: `EXISTING` — **LAYER 2 MIGRATION**
- **Structural role:** Sole authoritative source for FCDO statements, MOD announcements, sanctions listings, trade agreement texts, and ministerial speeches.
- **Domain coverage:** All five domains (primary source)
- **Reasoning:** Primary fetch via Layer 2 direct polling. Goggle boost at Tier 2 as belt-and-suspenders fallback. Government press releases occasionally surface in Brave News Search. Not blocked by Anthropic's crawler — one of the few official sources that can be reliably extracted. Includes key subdomains for foreign, defence, and trade policy.

**Hansard / Parliamentary Committees** | `parliament.uk` | Type: `legislative_official` | Status: `EXISTING` — **LAYER 2 MIGRATION**
- **Structural role:** Official record of all Commons and Lords debates, ministerial statements, and committee evidence sessions. Foreign Affairs Committee, Defence Committee, and Intelligence & Security Committee reports are first-order signals.
- **Domain coverage:** All five domains (primary source)
- **Reasoning:** Primary fetch via Layer 2 direct polling. Goggle boost at Tier 2 as belt-and-suspenders. Covers both `hansard.parliament.uk` and `committees.parliament.uk`. Not blocked — fully extractable. In a country where most media sources are blocked, parliamentary records become even more important as extractable primary sources.

**The New Statesman** | `newstatesman.com` | Type: `political_specialist` | Status: `EXISTING`
- **Structural role:** Counter-perspective to The Spectator. Influential among Labour policy class. Covers internal Labour debates on defence, NATO, nuclear deterrent, and foreign aid.
- **Domain coverage:** Domestic constraints, Diplomatic alignment, Institutional engagement
- **Reasoning:** Not blocked by Anthropic's crawler. With The Guardian blocked, the New Statesman becomes the primary extractable centre-left political voice. Essential for detecting domestic constraints on a Labour government's external posture — internal Labour debates on Trident renewal, NATO spending, and overseas development assistance surface here first. Metered paywall but partial extraction likely.

**The Spectator** | `spectator.co.uk` | Type: `opposition_aligned` | Status: `EXISTING`
- **Structural role:** Oldest continuously published English-language magazine. Read by Conservative political class. Provides early signals of right-wing policy opposition.
- **Domain coverage:** Domestic constraints, Diplomatic alignment
- **Reasoning:** Not blocked by Anthropic's crawler. With The Telegraph blocked, The Spectator becomes the primary extractable right-of-centre voice. Essential for detecting Conservative opposition to Labour's defence and foreign policy — backbench rebellion signals, Eurosceptic positioning on Windsor Framework, and defence-spending criticism surface here. Metered paywall — partial extraction likely.

**Declassified UK** | `declassifieduk.org` | Type: `investigative` | Status: `EXISTING`
- **Structural role:** Only UK outlet focused exclusively on investigating the UK's global military and intelligence footprint. Publishes FOI-based original reporting unavailable elsewhere.
- **Domain coverage:** Security & defence autonomy, Diplomatic alignment
- **Reasoning:** Not blocked. Free and fully extractable. Fills the adversarial-check function on official defence and foreign policy narratives. Left/anti-establishment orientation is a known bias the interpretive context can handle. No other source systematically tracks UK military bases, arms exports, and intelligence cooperation through FOI requests. Tier 2 because its unique structural role (adversarial defence watchdog) is irreplaceable, and its extractability makes it operationally valuable.

**Private Eye** | `private-eye.co.uk` | Type: `investigative` | Status: `NEW`
- **Structural role:** UK's premier satirical and investigative fortnightly. Breaks stories on government waste, corruption, and institutional dysfunction that mainstream outlets cannot or will not publish due to legal risk.
- **Domain coverage:** Domestic constraints, Institutional engagement
- **Reasoning:** Added to fill the government leak/scandal channel gap. Private Eye occupies a unique structural position in British media — its legal protections (Ian Hislop's willingness to litigate) and satirical format allow it to publish information that broadsheets hold back. Not blocked by Anthropic's crawler. Limited web presence (fortnightly publication) but when it publishes, stories are high-signal for domestic constraints on external action. Tier 2 for structural role despite low frequency.

---

### Tier 3 — `$boost=1`

**Janes (formerly Jane's)** | `janes.com` | Type: `security_defense` | Status: `EXISTING — DEMOTED FROM TIER 2`
- **Structural role:** Global gold-standard for defence equipment, order-of-battle, and procurement intelligence. 500,000+ analyst hours/year.
- **Domain coverage:** Security & defence autonomy, Economic & technological statecraft
- **Reasoning:** Demoted to Tier 3 because of extraction reality: Janes is a heavily paywalled subscription product. Only news headlines may surface in Brave. The pipeline benefits from seeing Janes headlines (they signal procurement changes and force-structure shifts), but full-text extraction is extremely unlikely. UK Defence Journal (Tier 1, free) provides an accessible alternative for many of the same stories. Tier 3 ensures Janes headlines surface when available without over-weighting an unextractable source.

**Politico Europe (London)** | `politico.eu` | Type: `political_specialist` | Status: `EXISTING — DEMOTED FROM TIER 2`
- **Structural role:** London Playbook newsletter is essential reading for Westminster insiders. Strong on UK-EU post-Brexit dynamics.
- **Domain coverage:** Diplomatic alignment, Institutional engagement, Domestic constraints
- **Reasoning:** **Blocked by Anthropic's crawler** (`politico.eu` in `blocked_domains.md`). Brave can still surface Politico results, and headlines contain useful signal on UK-EU regulatory alignment and Westminster insider dynamics. Demoted from Tier 2 to Tier 3 because blocked status limits extraction. The pipeline benefits from seeing Politico headlines ranked in Brave results, but not at the expense of extractable Tier 2 sources.
- **Extraction note:** BLOCKED — `politico.eu` in `blocked_domains.md`.

**openDemocracy** | `opendemocracy.net` | Type: `investigative` | Status: `PROMOTED FROM EXCLUSION`
- **Structural role:** Independent investigative journalism on democracy, human rights, and UK foreign policy. Publishes original investigations on dark money in UK politics, arms trade oversight, and democratic backsliding.
- **Domain coverage:** Domestic constraints, Diplomatic alignment
- **Reasoning:** The curation exclusion noted "coverage is episodic and skews toward commentary." Under the Goggle model, episodic sources with unique investigative function should be boosted at Tier 3, not excluded. openDemocracy's arms-trade investigations and dark-money reporting fill gaps that no other source covers. Not blocked by Anthropic's crawler — fully extractable. Tier 3 for supplementary depth when it publishes.

**Bellingcat** | `bellingcat.com` | Type: `investigative` / `security_defense` | Status: `NEW`
- **Structural role:** UK-based OSINT investigation outlet. Pioneered open-source intelligence methodology for tracking military activity, chemical weapons use, and covert operations.
- **Domain coverage:** Security & defence autonomy, Diplomatic alignment
- **Reasoning:** Added because Bellingcat fills the OSINT investigative niche — its Salisbury/Novichok investigation directly implicated Russian intelligence services operating on UK soil. UK-headquartered (Leicester) and frequently produces analysis relevant to UK defence and security posture. Not blocked. Tier 3 because publication is episodic and not UK-focused (covers global OSINT), but when it publishes UK-relevant material, the signal value is extremely high.

**AP News** | `apnews.com` | Type: `wire_service` | Status: `NEW`
- **Structural role:** Unblocked wire service providing fast factual reporting on UK government announcements and diplomatic moves.
- **Domain coverage:** All five domains (breaking news layer)
- **Reasoning:** Added because Reuters (`reuters.com`) — the UK's natural wire service — is **blocked by Anthropic's crawler**. AP News is not blocked and maintains a London bureau. Wire copy is normally left at Neutral, but the Reuters blocking creates a structural gap for fast, extractable breaking-news coverage. Tier 3 ensures AP surfaces for UK queries as a wire fallback. Not higher because AP's UK depth is less than Reuters'.

---

### Neutral — no Goggle rule

**Financial Times** | `ft.com` | Type: `business_financial` | Status: `EXISTING → DEMOTED TO NEUTRAL`
- **Why neutral:** Would be Tier 1 for economic statecraft coverage — FT is essential for UK trade negotiations, sanctions policy, and City of London regulatory shifts. **Blocked by Anthropic's crawler** (`ft.com` in `blocked_domains.md`). Hard paywall compounds the problem. Brave can still surface FT articles, and the pipeline benefits from seeing FT headlines organically. No boost needed — FT's SEO strength means it will appear in Brave results for economic queries without help. No need to discard. If the crawler block is ever lifted, immediately re-evaluate at Tier 1.

**The Times / The Sunday Times** | `thetimes.co.uk` | Type: `paper_of_record` | Status: `EXISTING → DEMOTED TO NEUTRAL`
- **Why neutral:** The newspaper of record for the UK establishment, frequently used by government for managed leaks. **Blocked by Anthropic's crawler** (`thetimes.co.uk` in `blocked_domains.md`). Hard paywall on top of crawler block makes extraction doubly unlikely. Like FT, its SEO strength means it surfaces organically in Brave. The pipeline can reason from headlines. No active boost needed; no reason to discard.

**The Telegraph** | `telegraph.co.uk` | Type: `paper_of_record` | Status: `EXISTING → DEMOTED TO NEUTRAL`
- **Why neutral:** Strong defence desk and distinct right-of-centre perspective. **Blocked by Anthropic's crawler** (`telegraph.co.uk` in `blocked_domains.md`). Metered paywall. The Spectator (Tier 2, extractable) partially fills the right-of-centre gap. Telegraph headlines will surface organically through Brave SEO strength. No boost needed; no reason to discard.

**The Economist** | `economist.com` | Type: `political_specialist` | Status: `EXISTING → DEMOTED TO NEUTRAL`
- **Why neutral:** Global agenda-setting publication for trade policy and multilateral engagement. **Blocked by Anthropic's crawler** (`economist.com` in `blocked_domains.md`). Hard paywall. Weekly publication frequency limits breaking-news utility. Its analytical function is partially covered by Chatham House (Tier 1) for institutional engagement and by FT headlines for economic statecraft. Organic Brave ranking is sufficient.

**Reuters** | `reuters.com` | Type: `wire_service` | Status: `EXISTING → DEMOTED TO NEUTRAL`
- **Why neutral:** London-headquartered wire service — fastest source for UK government announcements. **Blocked by Anthropic's crawler** (`reuters.com` in `blocked_domains.md`). Wire services are normally left neutral in the Goggle model anyway. Reuters' SEO dominance means it appears in Brave results organically. AP News (Tier 3, unblocked) provides the extractable wire fallback. No boost needed; no reason to discard.

**Sky News** | `news.sky.com` | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Curation exclusion was correct under the hard-filter model — broadcast-first, overlaps with BBC and wire coverage. Under the Goggle model, no reason to actively discard. Sky News has a competent digital operation and occasionally breaks stories. If it surfaces organically, the pipeline benefits. Not blocked by Anthropic's crawler, which makes it more extractable than the BBC — a useful fallback if BBC-originated stories prove inaccessible.

---

### Discard — `$discard`

**Daily Mail / Mail Online** | `dailymail.co.uk` | Status: `CONFIRMED DISCARD`
- **Discard reasoning:** Highest-traffic UK news website but editorial approach is tabloid-sensationalist. Foreign and defence coverage is shallow, editorialized for domestic outrage rather than policy analysis, and frequently misleading in headline framing. Would actively displace higher-signal sources from top results on Brave. Occasional scoops can be captured via wire syndication.

**The Sun** | `thesun.co.uk` | Status: `CONFIRMED DISCARD`
- **Discard reasoning:** Tabloid press. Political coverage exists but lacks depth or influence on the policy-making class. Headlines are optimized for engagement, not accuracy. Would inject noise into Brave results and displace analytical sources.

**The Mirror** | `mirror.co.uk` | Status: `CONFIRMED DISCARD`
- **Discard reasoning:** Tabloid press, entertainment-dominant. Labour-sympathetic but coverage is not policy-oriented. Same structural problem as The Sun — high SEO ranking for UK political queries but low signal-to-noise ratio. Would displace boosted sources.

**GB News** | `gbnews.com` | Status: `NEW DISCARD`
- **Discard reasoning:** Broadcast/digital outlet launched 2021 with explicit right-wing populist orientation. Functions primarily as opinion/commentary platform rather than reporting operation. Nigel Farage and other politicians have presented programmes — the outlet is a political actor, not an independent news source. Would inject partisan commentary framed as news into pipeline results.

---

## STRUCTURAL COVERAGE CHECK

| Structural Role | Source(s) | Tier | Notes |
|---|---|---|---|
| Government leak channel | The Times (Neutral/blocked), Private Eye (T2) | N, T2 | The Times is the traditional channel for Whitehall managed leaks but is blocked. Private Eye publishes leaked material other outlets won't touch. The Guardian (T2, blocked) also receives leaks but extraction fails |
| Opposition voice | The Spectator, New Statesman | T2, T2 | Spectator for Conservative opposition to Labour; New Statesman for intra-Labour dissent. Both extractable. Kemi Badenoch and Nigel Farage coverage surfaces through these |
| Defence/security first-mover | UK Defence Journal, RUSI, IISS | T1, T1, T1 | Three extractable sources forming a defence-analysis triad. UK Defence Journal for breaking news, RUSI for policy analysis, IISS for strategic context. Janes (T3) for procurement headlines |
| Policy-elite discourse | Chatham House, The Economist (Neutral/blocked), New Statesman | T1, N, T2 | Chatham House is the extractable policy-elite source. Economist headlines surface organically. New Statesman captures Labour policy-class debate |
| Domestic-language depth | N/A | — | UK media operates entirely in English. No domestic-language gap exists. All sources share the same language, so no non-English boost premium applies |
| Official government source | gov.uk, parliament.uk | T2, T2 | **LAYER 2 MIGRATION** — primary fetch via direct polling. Goggle boost as fallback. gov.uk covers FCDO, MOD, trade. parliament.uk covers Hansard, committees |
| Analytical/think tank depth | RUSI, Chatham House, IISS | T1, T1, T1 | World-class think-tank coverage — all three are extractable and free (commentary). This is the UK whitelist's greatest structural strength |
| Wire services | AP News (T3), Reuters (Neutral/blocked) | T3, N | Reuters is blocked but surfaces organically. AP News added as extractable wire fallback at Tier 3 |

**Gaps identified:**
1. **Government leak channel** is structurally weakened: The Times — the traditional vehicle for Whitehall managed leaks — is blocked. Private Eye partially fills this but publishes fortnightly. The pipeline may miss time-sensitive government signaling that would normally flow through The Times's front page. Mitigation: Layer 2 polling of gov.uk captures the official side of managed leaks; Private Eye and The Spectator catch the unofficial side with delay.
2. **Devolved-nation perspectives** remain a gap: Scottish Government foreign-policy positions (particularly on Trident basing and NATO posture in the context of independence dynamics), Welsh Government trade positions, and Northern Ireland power-sharing dynamics affecting the Windsor Framework receive minimal coverage in London-based sources. No dedicated Scottish, Welsh, or Northern Irish source is included. Mitigation: periodic manual checks as recommended in the curation prompt's coverage gap assessment.
3. **Economic statecraft depth** is compromised by the FT being blocked. No other UK source matches FT's coverage of sanctions policy, trade negotiations, City of London regulation, and industrial strategy. Chatham House provides analytical depth but not the daily reporting cadence. The pipeline will rely on FT headlines surfacing organically in Brave.
4. **Broadsheet breaking news** is structurally impaired: BBC, Guardian, Times, Telegraph, and FT are all blocked. The pipeline's ability to extract full-text from the UK's five most important news organizations is zero. This is mitigated by Brave discovery (headlines still surface), think-tank extraction (RUSI, Chatham House, IISS fill the analytical gap), and the unblocked second-tier press (New Statesman, Spectator, Declassified UK, UK Defence Journal).

---

## REDUNDANCY RESOLUTION

**Think-tank triad: RUSI + Chatham House + IISS**
Three think tanks at Tier 1 looks aggressive, but each occupies a distinct lane: RUSI (UK defence policy, procurement, nuclear deterrent), Chatham House (diplomatic alignment, multilateral engagement, post-Brexit trade), IISS (global strategic context, force balance, conference signals). No meaningful overlap — each produces original analysis that the others do not. All three are extractable and mostly free, which makes them operationally essential when broadsheets are blocked.

**Blocked broadsheet cluster: BBC + Guardian + FT + Times + Telegraph**
Five major sources all blocked. Resolved by differentiating between those that benefit from a Brave ranking boost (BBC, Guardian at Tier 2 — their headlines are still useful even without extraction) and those that can rely on organic SEO strength (FT, Times, Telegraph at Neutral — they will appear in results without boosting). The Guardian gets Tier 2 over the others because its free-access model means more full text appears in Brave snippets.

**Centre-left / centre-right pair: New Statesman + Spectator**
Both are political magazines at Tier 2. No redundancy — they represent opposite sides of the UK political spectrum. New Statesman captures Labour policy-class debate; Spectator captures Conservative opposition signaling. Both are extractable. The pipeline needs both to detect domestic constraints from left and right.

**Defence sources: RUSI + IISS + UK Defence Journal + Janes + Declassified UK**
Five sources is a lot for one domain, but the UK is a major military power and the pipeline's defence-coverage needs are high. Resolved by differentiating operational functions: RUSI (policy analysis), IISS (strategic context), UK Defence Journal (breaking news, free), Janes (procurement data, paywalled — Tier 3), Declassified UK (adversarial watchdog). Janes drops to Tier 3 because its paywall limits extraction and UK Defence Journal covers much of the same ground for free.

**Investigative outlets: Declassified UK + Private Eye + openDemocracy + Bellingcat**
Four investigative/watchdog sources, but each has a non-overlapping niche: Declassified UK (military/intelligence FOI investigations), Private Eye (government waste/corruption leaks), openDemocracy (dark money, arms trade, democratic process), Bellingcat (OSINT methodology, covert operations). Declassified UK and Private Eye at Tier 2 for frequency and structural importance; openDemocracy and Bellingcat at Tier 3 for episodic publication.

---

## QUERY CONFIGURATION

```
country: GB
search_lang: en
freshness: pw
```

**Multi-language notes:** The UK media ecosystem operates entirely in English. No secondary language query cycle is needed. The pipeline's `languages.primary: en` and `languages.metadata: en` configuration is correct. All sources are English-language.

**Localized query vocabulary validation:**

The curation prompt's vocabulary is comprehensive and well-targeted. Notes:

- **Domain 1 (Diplomatic Alignment):** All terms valid. `"FCDO"` is correct and high-signal. `"Global Britain"` is still in use but declining as the Starmer government distances itself from Johnson-era branding — consider adding `"progressive realism"` (Lammy's stated foreign policy doctrine). `"AUKUS"` remains highly relevant. Add `"Lammy foreign policy"` and `"Starmer NATO"` as leader-specific patterns. `"non-aligned"` is low-signal for the UK — it rarely describes UK positioning. Consider replacing with `"UK-EU reset"` (Starmer's stated goal for EU relations).
- **Domain 2 (Security & Defence):** Strong list. `"Strategic Defence Review"` and `"SDR"` are correct — the 2025 SDR is the defining defence document of the current government. Add `"Healey defence"` (Defence Secretary John Healey). `"defence spending 2.5% GDP"` is correct and high-signal. Add `"GCAP"` (Global Combat Air Programme — UK-Japan-Italy next-gen fighter, major procurement signal). Add `"Ukraine UK military aid"` — the dominant frame for UK defence engagement since 2022.
- **Domain 3 (Economic & Technological Statecraft):** Excellent. `"CPTPP"` is correct and high-signal for UK trade diversification. Add `"Reeves budget"` and `"industrial strategy"` (Starmer government's central economic framework). `"investment screening"` is correct — the National Security and Investment Act 2021 is actively used. Add `"AI regulation"` and `"AI Safety Institute"` — UK positioning as AI governance leader. Add `"semiconductor strategy"` for tech-statecraft tracking.
- **Domain 4 (Institutional Engagement):** Valid. `"Windsor Framework"` remains high-signal. Add `"UK-EU summit"` (Starmer pursuing closer EU ties). `"Commonwealth"` is correct but declining in policy relevance. Add `"COP"` (Climate summits — UK hosted COP26, remains active). `"OSCE"` is low-signal for UK specifically — consider `"Council of Europe"` as higher-signal for UK institutional engagement.
- **Domain 5 (Domestic Constraints):** Strong. `"backbench rebellion"` is high-signal. Add `"Labour left"` and `"Labour defence policy"` for intra-party constraint detection. `"Scottish independence"` remains relevant for Trident basing. Add `"Reform UK"` (Farage's party — emerging political constraint on both Labour and Conservative defence/immigration positioning). Add `"fiscal rules"` (Reeves's fiscal framework constraining defence spending increases).

**Stale/problematic terms:** `"Global Britain"` is not stale but is declining — the Starmer government is distancing from the phrase. Keep as a search term but do not rely on it as the primary diplomatic-alignment query. `"non-aligned"` is problematic for the UK specifically — the UK is emphatically aligned (NATO, Five Eyes, AUKUS). Replace with `"UK-EU reset"` or `"strategic autonomy"`.

**Suggested topic query patterns:**

1. `Starmer NATO defence spending 2.5%` — Defence spending commitments under Starmer
2. `AUKUS submarine programme UK` — AUKUS implementation and industrial base
3. `Lammy FCDO progressive realism` — Foreign Secretary's diplomatic doctrine
4. `Strategic Defence Review 2025 Healey` — SDR implementation
5. `Windsor Framework UK-EU trade reset` — Post-Brexit EU relationship evolution
6. `GCAP Tempest fighter programme` — Major trilateral defence procurement
7. `AI Safety Institute UK regulation` — Tech statecraft and AI governance
8. `Reform UK Farage defence immigration` — Domestic political constraints from the right

---

## GOGGLE FILE

```goggle
! name: MPM United Kingdom
! description: MPM pipeline source prioritization for United Kingdom — boosts extractable high-signal sources, accounts for severe crawler-blocking across major broadsheets
! public: false
! author: MPM Pipeline

! --- Tier 1: Essential (boost=3) ---
$boost=3,site=rusi.org
$boost=3,site=chathamhouse.org
$boost=3,site=ukdefencejournal.org.uk
$boost=3,site=iiss.org

! --- Tier 2: Important (boost=2) ---
$boost=2,site=theguardian.com
$boost=2,site=bbc.co.uk
$boost=2,site=bbc.com
$boost=2,site=gov.uk
$boost=2,site=parliament.uk
$boost=2,site=newstatesman.com
$boost=2,site=spectator.co.uk
$boost=2,site=declassifieduk.org
$boost=2,site=private-eye.co.uk

! --- Tier 3: Supplementary (boost=1) ---
$boost=1,site=janes.com
$boost=1,site=politico.eu
$boost=1,site=opendemocracy.net
$boost=1,site=bellingcat.com
$boost=1,site=apnews.com

! --- Discard: Noise ---
$discard,site=dailymail.co.uk
$discard,site=thesun.co.uk
$discard,site=mirror.co.uk
$discard,site=gbnews.com
```

---

## INTERPRETIVE CONTEXT FOR DOSSIER

### Tier 1 Sources

> Articles from **RUSI** about defence policy and procurement should be interpreted as the UK's most authoritative independent defence analysis — its proximity to the defence establishment (est. 1831, patron: the Monarch) means it reflects mainstream military-strategic thinking rather than adversarial criticism. When RUSI publishes concerns about a programme or capability gap, this signals genuine establishment anxiety, not opposition politics.

> Articles from **Chatham House** about diplomatic alignment and multilateral engagement should be interpreted as reflecting the UK foreign-policy mainstream — internationalist, rules-based-order-oriented, and implicitly pro-Western-alliance. Its "UK in the World" programme tracks strategic posture with academic rigor. Chatham House analysis provides the interpretive framework that daily news coverage lacks, but its internationalist orientation means it may underweight domestic political constraints on foreign policy.

> Articles from **UK Defence Journal** about military capabilities and procurement should be interpreted as credible but editorially pro-defence — the outlet exists to cover UK military capability and its editorial stance favours robust defence spending. It breaks stories faster than think tanks but with less analytical depth. When UK Defence Journal reports a capability problem (e.g., aircraft carrier readiness), the story is typically well-sourced; when it reports positively on a programme, calibrate for pro-defence bias.

> Articles from **IISS** about strategic developments and military balance should be interpreted as the global strategic-analytical lens — IISS positions UK developments within worldwide force-balance and alliance dynamics. Its annual *Military Balance* assessments are reference-standard. Conference hosting (Shangri-La, Manama) means IISS output sometimes reflects what conference participants want in the public domain — treat conference reports as diplomatic signals, not just analysis.

### Tier 2 Sources

> Articles from **The Guardian** about foreign and defence policy should be interpreted as filtered through a centre-left editorial lens — editorially independent (Scott Trust ownership) but consistently sceptical of military intervention, defence spending increases, and intelligence community overreach. Its investigative reporting (Snowden, WikiLeaks) is world-class, but its editorial framing of defence stories tends toward caution and restraint. **Note: blocked by Anthropic's crawler — pipeline may only capture headlines/snippets.**

> Articles from **BBC News** about any domain should be interpreted as reflecting the UK media consensus — its statutory impartiality obligation means BBC coverage represents the median of UK establishment opinion. When BBC framing shifts on a topic, this signals a broader shift in acceptable discourse. **Note: blocked by Anthropic's crawler — pipeline may only capture headlines/snippets.**

> Articles from **GOV.UK** should be interpreted as official government communications — not journalism but primary source material. FCDO statements, MOD announcements, and sanctions listings represent the government's chosen public position, which may differ from actual policy implementation or internal debate. Government tone and timing are themselves signals.

> Articles from **Hansard / Parliament.uk** should be interpreted as verbatim institutional record — ministerial statements represent official policy; committee reports represent cross-party parliamentary judgment (often more candid than government statements); backbench interventions during debates signal intra-party dissent before it becomes news.

> Articles from **The New Statesman** about Labour policy debates should be interpreted as reflecting the centre-left intellectual establishment — influential among Labour's policy class and soft-left faction. When New Statesman critiques Labour defence or foreign policy from the left, this signals genuine intra-party tension. Its editorial orientation means it frames defence spending increases as opportunity costs against domestic priorities.

> Articles from **The Spectator** about government foreign and defence policy should be interpreted as filtered through a conservative, Eurosceptic editorial lens — read by the Conservative political class and military community. When The Spectator criticises Labour defence policy, calibrate for opposition partisanship; when it praises a Labour defence move, this signals genuine cross-party consensus. Its Eurosceptic orientation means EU-related coverage systematically frames closer UK-EU ties negatively.

> Articles from **Declassified UK** about UK military and intelligence activity should be interpreted as adversarial investigative journalism from a left/anti-establishment perspective — it exists specifically to challenge official narratives on UK military operations, arms exports, and intelligence cooperation. FOI-based reporting is factually grounded, but editorial framing is consistently critical of UK military engagement. When Declassified UK reveals a previously unknown UK military activity, the factual core is typically reliable; the interpretive framing requires calibration.

> Articles from **Private Eye** about government conduct and institutional dysfunction should be interpreted as sourced from insiders willing to leak to a publication with strong legal protections — Private Eye's satirical format and willingness to litigate libel claims means it publishes material that risk-averse broadsheets hold back. Its fortnightly cadence means stories are not breaking news but confirmed patterns. When Private Eye reports on defence procurement waste or diplomatic dysfunction, the underlying sourcing is typically solid.

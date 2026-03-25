# AUDIT SUMMARY: LATVIA

**Sources assessed:** 17 recommended + 4 excluded + 4 newly identified = 25 total
**Tier 1 (boost=3):** 3 sources
**Tier 2 (boost=2):** 8 sources
**Tier 3 (boost=1):** 5 sources
**Neutral (no rule):** 6 sources
**Discard:** 3 sources
**Overall assessment:** The curation prompt produced a competent whitelist for a small media market, correctly identifying the LSM-Delfi-TVNET triad as the domestic core and Re:Baltica as the investigative anchor. Key changes: (1) flagged `delfi.lv` and `la.lv` as blocked by Anthropic's crawler — Delfi is the most-visited portal, so this is a material constraint; (2) promoted government official sources (saeima.lv, mod.gov.lv, mfa.gov.lv, president.lv, mk.gov.lv) for Layer 2 migration at Tier 2; (3) added missing structural roles — central bank (bank.lv), NATO eFP/allied presence sources, and LRT English (for Baltic comparative context); (4) applied non-English domestic language boost premium to Latvian-only sources; (5) resolved redundancy in the news-portal cluster (Delfi/TVNET/Diena) by differentiating tiers based on editorial distinctiveness. Latvia's small media market means fewer sources overall, but the linguistic segmentation (Latvian vs. Russian) and security-frontline positioning create unique structural demands.

---

## BOOST ASSIGNMENTS

### Tier 1 — `$boost=3`

**LSM (Latvian Public Media)** | `lsm.lv` | Type: `paper_of_record` | Status: `EXISTING`
- **Structural role:** Latvia's merged public broadcaster and the country's most trusted news platform. Functions as the national paper of record across all domains — parliament, defense, foreign policy, economic policy. English service at eng.lsm.lv provides pipeline-accessible coverage.
- **Domain coverage:** Diplomatic alignment, Security & defense autonomy, Economic & technological statecraft, Institutional engagement, Domestic constraints
- **Reasoning:** LSM is the single indispensable Latvian source. Since the 2025 merger of Latvian Television and Latvian Radio, it consolidates the entire public media apparatus. It covers all five analytical domains with original reporting, maintains editorial independence, and provides English-language output that the pipeline can extract reliably. Free access and no crawler blocks make it the highest-signal, most-extractable domestic source. The planned 2026 ban on its Russian-language content is itself a major signal event.
- **Extraction note:** Free. English service at eng.lsm.lv. No crawler blocks. Full extraction expected.

**Re:Baltica** | `rebaltica.lv` | Type: `investigative` | Status: `EXISTING`
- **Structural role:** Latvia's only dedicated investigative journalism center. GIJN member. Conducts cross-border investigations on corruption, money laundering, and disinformation — the exact topics where government sources are structurally silent.
- **Domain coverage:** Diplomatic alignment, Security & defense autonomy, Economic & technological statecraft, Institutional engagement, Domestic constraints
- **Reasoning:** In Latvia's small media market, Re:Baltica fills an outsized structural role. It is the sole source capable of sustained adversarial investigation into state corruption, Russian influence operations, and financial misconduct. Its English-language output and grant-funded independence from both government and oligarchic ownership make it uniquely reliable. No other Latvian outlet replicates this function. Free and extractable.
- **Extraction note:** Free. English-language content available. No crawler blocks.

**IR** | `ir.lv` | Type: `investigative` | Status: `EXISTING`
- **Structural role:** Latvia's leading independent weekly magazine. Founded in 2010 by former Diena journalists who left after an oligarchic ownership takeover — its origin story is itself a signal of Latvia's media-ownership dynamics. Strong investigative record on political and corporate misconduct.
- **Domain coverage:** Domestic constraints, Economic & technological statecraft, Security & defense autonomy
- **Reasoning:** IR fills the policy-elite discourse role that no other Latvian source occupies. Where LSM provides breadth and Re:Baltica provides cross-border investigation, IR provides the depth of domestic political and corporate accountability reporting that Latvian elites read. Its independent-liberal orientation and founding narrative give it credibility that the historically compromised broadsheets (Diena, NRA) lack. Paywalled, but Brave indexes headlines for discovery. Non-English domestic language boost premium applies — Latvian-language investigative journalism is structurally scarce and irreplaceable.
- **Extraction note:** Paywalled. Brave indexes headlines; Diffbot extraction may be partial. Pipeline value is in discovery and headline-level signal even when full text is unavailable.

---

### Tier 2 — `$boost=2`

**TVNET** | `tvnet.lv` | Type: `paper_of_record` | Status: `EXISTING`
- **Structural role:** Second-most-visited news portal. Complements the Delfi/LSM pair for speed and volume of political and security coverage. Ekspress Grupp / Eesti Media ownership.
- **Domain coverage:** Diplomatic alignment, Security & defense autonomy, Domestic constraints, Economic & technological statecraft, Institutional engagement
- **Reasoning:** With Delfi blocked by Anthropic's crawler, TVNET's practical importance rises — it becomes the primary extractable commercial news portal. Covers all five domains with original reporting. Free with ads. Not Tier 1 because it breaks fewer stories than LSM and has less editorial distinctiveness than IR, but its volume and speed earn a strong Tier 2.
- **Extraction note:** Free with ads. No crawler blocks. Full extraction expected.

**Delfi Latvia** | `delfi.lv` | Type: `paper_of_record` | Status: `EXISTING — BLOCKED`
- **Structural role:** Most-visited news portal in Latvia. Russian-language version (rus.delfi.lv) is critical for monitoring the Russophone audience after the 2026 public-media ban.
- **Domain coverage:** Diplomatic alignment, Security & defense autonomy, Domestic constraints, Economic & technological statecraft, Institutional engagement
- **Reasoning:** Delfi is structurally essential — highest traffic, dual-language coverage, broad domain reach. However, **`delfi.lv` is blocked by Anthropic's crawler** (`robots.txt` denial), which means extraction via pipeline tools will fail even when Brave surfaces it. This is a material constraint. Under the Goggle model, Brave can still discover and rank Delfi results, so a Tier 2 boost ensures its headlines surface for triage even without full-text extraction. TVNET at Tier 2 provides the extractable fallback. If Delfi unblocks Anthropic's crawler, this should be re-evaluated for Tier 1.
- **Extraction note:** **BLOCKED by Anthropic's crawler.** Brave can discover; full extraction will fail. Headline-level signal only.

**NRA (Neatkariga Rita Avize)** | `nra.lv` | Type: `opposition_aligned` | Status: `EXISTING`
- **Structural role:** Primary voice of nationalist-conservative and Eurosceptic sentiment. Historically linked to oligarch Aivars Lembergs. Represents the political current that constrains government flexibility on EU integration, migration, and minority policy.
- **Domain coverage:** Domestic constraints, Diplomatic alignment
- **Reasoning:** Opposition-aligned sources earn Tier 2 minimum per boost principles — the pipeline needs to see domestic contestation. NRA fills a unique niche: it is where Eurosceptic, national-sovereignty, and anti-establishment narratives surface in Latvia's press. Its Lembergs connection is a liability for trust but a feature for signal — what NRA amplifies reflects what the nationalist wing of Latvian politics wants amplified. Non-English domestic language boost premium applies. Partially paywalled but headlines are indexable.
- **Extraction note:** Partially paywalled. Latvian-language only. Non-English boost premium applied.

**Saeima (Parliament)** | `saeima.lv` | Type: `legislative_official` | Status: `EXISTING` — **LAYER 2 MIGRATION**
- **Structural role:** Latvia's parliament. Committee records, draft legislation, plenary transcripts. Essential for tracking defense-spending debates, foreign-policy votes, and coalition dynamics.
- **Domain coverage:** All five domains (official source)
- **Reasoning:** Primary fetch via Layer 2 direct polling. Goggle boost at Tier 2 as belt-and-suspenders fallback. Parliamentary records occasionally surface in Brave News Search. English-language content available.

**Ministry of Defence** | `mod.gov.lv` | Type: `government_aligned` | Status: `EXISTING` — **LAYER 2 MIGRATION**
- **Structural role:** Procurement announcements, NATO host-nation updates, defense-budget documents. Latvia allocating 4.9% GDP to defense in 2026 makes this a high-signal source.
- **Domain coverage:** Security & defense autonomy
- **Reasoning:** Primary fetch via Layer 2 direct polling. Goggle boost at Tier 2 as fallback. In a country with no specialist defense-procurement publication, mod.gov.lv press releases are the primary source for defense-spending and procurement signals.

**Ministry of Foreign Affairs** | `mfa.gov.lv` | Type: `government_aligned` | Status: `EXISTING` — **LAYER 2 MIGRATION**
- **Structural role:** Foreign-policy statements, EU/NATO positions, bilateral agreements. Latvia's diplomatic communications.
- **Domain coverage:** Diplomatic alignment, Institutional engagement
- **Reasoning:** Primary fetch via Layer 2 direct polling. Goggle boost at Tier 2 as fallback.

**Government Portal / Presidential Office** | `mk.gov.lv`, `president.lv` | Type: `government_aligned` | Status: `NEW (from lv.yaml)` — **LAYER 2 MIGRATION**
- **Structural role:** Central government portal (mk.gov.lv) and presidential office (president.lv). Official policy positions, cabinet decisions, presidential statements.
- **Domain coverage:** All five domains (official source)
- **Reasoning:** Both domains appear in lv.yaml as government Tier 1 sources. Primary fetch via Layer 2 direct polling. Goggle boost at Tier 2 as belt-and-suspenders fallback.

**LIIA (Latvian Institute of International Affairs)** | `liia.lv` | Type: `security_defense` / `think_tank` | Status: `EXISTING`
- **Structural role:** Latvia's foreign-policy research institute. Publishes yearbooks and policy analyses on Baltic security, EU strategic autonomy, and transatlantic relations.
- **Domain coverage:** Diplomatic alignment, Security & defense autonomy
- **Reasoning:** Think tanks earn boost through depth, not speed. LIIA provides the analytical framework the pipeline needs to interpret Latvia's security and diplomatic positioning — why the 4.9% GDP defense spend matters strategically, how Latvia views EU strategic autonomy vs. NATO primacy, what the Baltic-Nordic security convergence means. Tier 2 for analytical depth. English-language output makes it pipeline-accessible.
- **Extraction note:** Free. English-language content available. No crawler blocks.

---

### Tier 3 — `$boost=1`

**Latvijas Avize** | `la.lv` | Type: `paper_of_record` | Status: `EXISTING — BLOCKED`
- **Structural role:** Largest daily by circulation, especially outside Riga. Strong rural and national-identity readership base. National-conservative editorial orientation.
- **Domain coverage:** Domestic constraints, Security & defense autonomy
- **Reasoning:** Latvijas Avize provides the non-Riga, rural, national-identity perspective that the Riga-centric portals miss. However, **`la.lv` is blocked by Anthropic's crawler**, limiting extraction to headline-level signal from Brave. Combined with its partial paywall, this makes it a Tier 3 rather than Tier 2 source. Its national-conservative orientation overlaps somewhat with NRA, but its readership base (rural, older, outside Riga) is structurally distinct.
- **Extraction note:** **BLOCKED by Anthropic's crawler.** Partially paywalled. Latvian-language only. Headline-level signal only.

**Diena** | `diena.lv` | Type: `paper_of_record` | Status: `EXISTING`
- **Structural role:** Largest daily by tradition. Historically Latvia's most prominent broadsheet, but editorial independence compromised by oligarchic ownership (linked to Slesers/Skele port group).
- **Domain coverage:** Diplomatic alignment, Domestic constraints
- **Reasoning:** Diena's structural importance has declined — ownership concerns have eroded trust, and its agenda-setting role has been absorbed by LSM and Delfi/TVNET. Tier 3 because its ownership dynamics are themselves a signal (what Diena amplifies may reflect port-group business interests), but the pipeline cannot treat it as an independent source. Partially paywalled.
- **Extraction note:** Partially paywalled. Latvian-language only. No crawler blocks.

**Dienas Bizness (db.lv)** | `db.lv` | Type: `business_financial` | Status: `EXISTING`
- **Structural role:** Latvia's leading business publication. Covers trade, investment, sanctions, and EU economic regulation.
- **Domain coverage:** Economic & technological statecraft
- **Reasoning:** Single-domain (economic) but fills a structural gap — no other Latvian source provides dedicated business and financial coverage. Sanctions compliance, EU trade regulation, energy security, and investment policy are core pipeline topics that db.lv covers from a domestic business perspective. Tier 3 because of narrow domain scope and partial paywall. Non-English domestic language boost premium applies.
- **Extraction note:** Partially paywalled. Latvian-language only. No crawler blocks.

**Providus** | `providus.lv` | Type: `political_specialist` / `think_tank` | Status: `EXISTING`
- **Structural role:** Independent centrist-liberal think tank. Policy research on governance, EU integration, and democratic participation.
- **Domain coverage:** Institutional engagement, Domestic constraints
- **Reasoning:** Fills the domestic institutional-analysis niche alongside LIIA's international focus. Providus provides the structural analysis on governance reform, judicial independence, and democratic participation that daily outlets lack. Tier 3 rather than Tier 2 because its output volume is lower and its domain coverage narrower than LIIA's. English-language content available.
- **Extraction note:** Free. English-language content available. No crawler blocks.

**The Baltic Times** | `baltictimes.com` | Type: `regional` | Status: `EXISTING`
- **Structural role:** English-language pan-Baltic monthly. Provides cross-Baltic comparative context.
- **Domain coverage:** All five domains (summary level)
- **Reasoning:** Tier 3 for the same reason Mexico News Daily is Tier 3 in the Mexico audit — its editorial selection functions as a filter for what the English-speaking diplomatic and business community considers important across the Baltics. Not a primary source but a useful low-cost signal detector for cross-Baltic dynamics. Free and extractable.
- **Extraction note:** Free. English-language. No crawler blocks.

---

### Neutral — no Goggle rule

**BNS Latvia** | `bns.lv` | Type: `paper_of_record` (wire service) | Status: `EXISTING → NEUTRAL`
- **Why neutral:** Pan-Baltic wire service. Wire copy is available organically — Brave will surface BNS-sourced stories through the outlets that republish them (Delfi, TVNET, LSM). Boosting the wire service directly would double-count signal already captured through domestic outlets. Subscription access further limits direct extraction. Leave at organic ranking.

**VDD (State Security Service)** | `vdd.gov.lv` | Type: `security_defense` | Status: `EXISTING → NEUTRAL`
- **Why neutral:** Annual reports are high-value but infrequent (once per year). The pipeline cannot depend on regular output. VDD annual reports are better handled as Layer 2 direct polling targets on a scheduled basis rather than through Brave search boosting. When the annual report drops, LSM, Delfi, and Re:Baltica will all cover it extensively — the pipeline captures the signal through boosted outlets.

**Pietiek.com** | `pietiek.com` | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Anonymously authored political commentary blog. The curation prompt correctly excluded it for unverifiable sourcing, but under the Goggle model, no reason to actively discard. If Pietiek surfaces a story that gets picked up by boosted outlets, the pipeline benefits from seeing it in organic results. Its anonymous authorship is a liability but also means it occasionally surfaces information that attributed outlets cannot publish.

**Apollo.lv** | `apollo.lv` | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** News aggregator that duplicates Delfi/TVNET without original reporting. Under the Goggle model, organic ranking is appropriate — it won't displace boosted sources but may surface serendipitously for specific queries.

**Chas** | Type: excluded → `neutral` | Status: `CONFIRMED NEUTRAL (was exclusion)`
- **Why neutral:** Previously significant Russian-language daily, now marginal. Under the Goggle model, leave at organic ranking — if it surfaces, it provides a residual signal from the Russian-language information space that is otherwise becoming invisible post-2026 ban.

**rus.delfi.lv** | Type: `neutral` | Status: `NOTE — COVERED UNDER delfi.lv`
- **Why neutral:** The Russian-language version of Delfi is technically a subdomain covered by the `delfi.lv` Tier 2 boost. However, since `delfi.lv` is blocked by Anthropic's crawler, extraction of Russian-language content faces the same constraint. Noted here for completeness — this is the most important remaining Russian-language news source in Latvia and its signal loss due to the crawler block is a material gap.

---

### Discard — `$discard`

**Russian-language Telegram channels** | Status: `CONFIRMED DISCARD`
- **Discard reasoning:** Outside the scope of curated traditional-media whitelisting. Not indexable by Brave. Would inject unverifiable, unattributed content into the pipeline. The Russophone information gap is real but must be addressed through separate monitoring tools, not through the Goggle.

**Russian state media (RT, Sputnik, TASS Latvian services)** | Status: `NEW DISCARD`
- **Discard reasoning:** Russian state media operations targeting the Baltic states are propaganda instruments, not journalism. Banned in the EU since 2022. Would actively displace higher-signal sources and inject state-directed disinformation. Any signal from Russian state narratives that matters will be captured through VDD annual reports, Re:Baltica investigations, and LSM coverage of disinformation campaigns.

**Baltnews.lv / Sputnik Latvia** | Status: `NEW DISCARD`
- **Discard reasoning:** Kremlin-affiliated Latvian-language outlet. Blocked by Latvian authorities. Same reasoning as Russian state media above — pure noise that would displace genuine signal.

---

## STRUCTURAL COVERAGE CHECK

| Structural Role | Source(s) | Tier | Notes |
|---|---|---|---|
| Government leak channel / signaling | LSM, Diena | T1, T3 | LSM as public broadcaster receives government communications first; Diena's oligarchic ownership means it may amplify port-group interests |
| Opposition voice | NRA | T2 | Nationalist-conservative, Eurosceptic. Primary voice of domestic contestation against EU-integrationist consensus |
| Defence/security first-mover | LSM, mod.gov.lv, LIIA | T1, T2, T2 | No dedicated defence press. LSM breaks defence stories; mod.gov.lv provides official procurement/budget data; LIIA provides analytical depth |
| Policy-elite discourse | IR, LIIA, Providus | T1, T2, T3 | IR for domestic political/corporate investigation; LIIA for international security analysis; Providus for governance and EU integration |
| Domestic-language depth | IR, NRA, Latvijas Avize, Diena, db.lv | T1, T2, T3, T3, T3 | Non-English domestic language boost premium applied. Latvian-language sources are structurally scarce in a 1.8M population market — each carries disproportionate weight |
| Official government source | saeima.lv, mod.gov.lv, mfa.gov.lv, mk.gov.lv, president.lv | T2 | **LAYER 2 MIGRATION** — primary fetch via direct polling. Goggle boost as fallback |
| Analytical/think tank depth | LIIA, Providus, Re:Baltica | T2, T3, T1 | LIIA for Baltic security and transatlantic relations; Providus for domestic governance; Re:Baltica for cross-border investigative analysis |
| Wire service | Reuters, AP News, France24 | Neutral | Not boosted in Goggle. Reuters is blocked by Anthropic crawler. Wire copy surfaces organically and through domestic republication |
| Russophone audience monitor | Delfi (rus.delfi.lv) | T2 (blocked) | **STRUCTURAL VULNERABILITY.** Most important remaining Russian-language source blocked by crawler. Signal loss is material |

**Gaps identified:**
1. **Russian-language information space** is the most critical structural gap. The 2026 ban on LSM Russian-language content, the earlier closure of Russian state TV, and Anthropic's crawler blocking of delfi.lv (including rus.delfi.lv) means the pipeline has near-zero visibility into Russophone audience dynamics. Mitigated partially by VDD annual reports and Re:Baltica investigations, but real-time monitoring of Russian-speaking community sentiment is effectively blind.
2. **Defence-industrial reporting** is absent as a specialist function. Latvia's defense spending is surging (4.9% GDP in 2026) and includes major procurement programs (air defense, NATO brigade infrastructure), but no specialist defense-procurement publication exists. mod.gov.lv press releases and IR/Re:Baltica investigations partially fill this gap.
3. **Allied presence / NATO eFP coverage** from the Canadian-led multinational brigade perspective is not captured by any Latvian source. Canadian DND releases and NATO eFP communiques would need to be added as Layer 2 direct polling targets — they are outside the scope of a Latvia-specific Goggle.
4. **Central bank / monetary policy** — Bank of Latvia (bank.lv) is in lv.yaml as an actor but not in the source intelligence map. For a country navigating eurozone dynamics and sanctions-related financial compliance, this is a notable absence. Recommend adding bank.lv as a Layer 2 direct polling target.

---

## REDUNDANCY RESOLUTION

**News portal cluster: LSM + Delfi + TVNET**
All three are high-traffic portals covering all five domains. Resolved by differentiating structural roles: LSM (Tier 1, public broadcaster, most trusted, fully extractable), Delfi (Tier 2, highest traffic but crawler-blocked, Russian-language version uniquely valuable), TVNET (Tier 2, extractable commercial portal that serves as Delfi fallback). LSM leads because it combines editorial independence, full extractability, and the broadest domain coverage. Delfi and TVNET differentiate on extraction reliability rather than editorial function.

**Broadsheet cluster: Diena + Latvijas Avize + NRA**
Three traditional print dailies with different editorial orientations. Resolved by structural role: NRA (Tier 2, opposition-aligned, Eurosceptic voice the pipeline needs), Latvijas Avize (Tier 3, largest circulation but crawler-blocked, rural/national-identity niche), Diena (Tier 3, compromised by oligarchic ownership, declining agenda-setting power). NRA leads because opposition voices earn Tier 2 minimum per boost principles.

**Investigative cluster: Re:Baltica + IR**
Two investigative outlets but with distinct niches — Re:Baltica (cross-border, corruption, disinformation, English-language) and IR (domestic political/corporate, Latvian-language weekly). No redundancy. Both merit high tiers because Latvia's small market means each fills an irreplaceable structural role.

**Think tank cluster: LIIA + Providus**
Two think tanks with complementary foci — LIIA (international security, transatlantic relations) and Providus (domestic governance, EU integration). Resolved by scope: LIIA (Tier 2, broader domain coverage, more directly relevant to pipeline's security and diplomatic domains) and Providus (Tier 3, narrower domestic focus). No redundancy.

**Government source cluster: saeima.lv + mod.gov.lv + mfa.gov.lv + mk.gov.lv + president.lv**
Five government domains, all Layer 2 migration targets. No redundancy — each covers a distinct institutional function (parliament, defense, foreign affairs, cabinet, presidency). All boosted at Tier 2 as belt-and-suspenders fallback for Layer 2 direct polling.

---

## QUERY CONFIGURATION

```
country: LV
search_lang: lv
freshness: pw
```

**Multi-language notes:** Latvia's media ecosystem operates in Latvian with a significant Russian-language component that is shrinking due to policy. English-language output from LSM (eng.lsm.lv), Re:Baltica, LIIA, and Providus provides pipeline-accessible coverage. Queries should run primarily in Latvian; a secondary English query cycle captures the think tank and English-language investigative output. The lv.yaml `languages.metadata: en` configuration handles this correctly. Russian-language queries against rus.delfi.lv would be valuable but are constrained by the crawler block.

**Localized query vocabulary validation:**

The curation prompt's vocabulary is strong. Notes:

- **Domain 1 (Diplomatic):** All terms valid. Add `"Siliņa ārpolitika"` and `"Rinkēvičs"` as leader-specific patterns. `"Baltijas sadarbība"` is good — add `"Ziemeļvalstu-Baltijas sadarbība"` (Nordic-Baltic cooperation) to capture the increasingly important Nordic dimension. Add `"Trīs jūru iniciatīva"` (Three Seas Initiative) — relevant for Latvia's regional diplomatic positioning.
- **Domain 2 (Security):** Strong list. Add `"Sprūds aizsardzība"` (Defence Minister-specific). `"NATO atturēšana"` is good; add `"NATO kaujas grupa"` (NATO battlegroup) — the Canadian-led eFP battlegroup is the most visible allied presence. Add `"pretgaisa aizsardzība"` (air defense) — a major procurement priority. `"obligātais dienests"` (mandatory service) is timely given the 2027 reintroduction debates.
- **Domain 3 (Economic):** Solid. Add `"tranzīta koridors"` (transit corridor) — Latvia's rail/port transit infrastructure from Soviet era is a recurring economic-statecraft topic. Add `"Rīgas osta"` (Riga port) — historically linked to oligarchic interests and sanctions compliance. `"sankcijas"` should be paired with `"sankcijas Krievija"` (Russia sanctions) to improve signal-to-noise.
- **Domain 4 (Institutional):** Valid. Add `"ES prezidentūra"` (EU presidency) for forward-looking queries. `"Ziemeļvalstu sadarbība"` is correctly included. Add `"OSCE"` — Latvia has active OSCE engagement.
- **Domain 5 (Domestic):** Strong. Add `"Saeimas vēlēšanas"` (parliamentary elections). `"koalīcijas veidošana"` is essential for Latvia's fragmented party system. Add `"oligarhu ietekme"` (oligarch influence) — a perennial structural theme in Latvian domestic politics. Add `"diaspora"` — Latvia's large emigrant diaspora (estimated 250,000–370,000) is a significant domestic-constraint factor.

**Stale/problematic terms:** None are stale. The Russian-language terms for monitoring rus.delfi.lv are well-chosen but their utility is constrained by the crawler block on delfi.lv.

**Suggested topic query patterns:**

1. `Siliņa aizsardzības budžets NATO` — Defence spending / NATO commitments under Siliņa
2. `obligātais dienests Latvija 2027` — Mandatory military service reintroduction debate
3. `sankcijas Krievija tranzīts Rīgas osta` — Russia sanctions / transit infrastructure impact
4. `koalīcija Saeima balsojums` — Coalition dynamics / parliamentary votes
5. `NATO kaujas grupa Latvija Kanāda` — NATO eFP battlegroup / Canadian-led allied presence
6. `kiberdrošība hibrīddraudi VDD` — Cybersecurity / hybrid threats / security service assessments

---

## GOGGLE FILE

```goggle
! name: MPM Latvia
! description: MPM pipeline source prioritization for Latvia — boosts high-signal sources, discards noise
! public: false
! author: MPM Pipeline

! --- Tier 1: Essential (boost=3) ---
$boost=3,site=lsm.lv
$boost=3,site=rebaltica.lv
$boost=3,site=ir.lv

! --- Tier 2: Important (boost=2) ---
$boost=2,site=tvnet.lv
$boost=2,site=delfi.lv
$boost=2,site=nra.lv
$boost=2,site=saeima.lv
$boost=2,site=mod.gov.lv
$boost=2,site=mfa.gov.lv
$boost=2,site=mk.gov.lv
$boost=2,site=president.lv
$boost=2,site=liia.lv

! --- Tier 3: Supplementary (boost=1) ---
$boost=1,site=la.lv
$boost=1,site=diena.lv
$boost=1,site=db.lv
$boost=1,site=providus.lv
$boost=1,site=baltictimes.com

! --- Discard: Noise ---
$discard,site=baltnews.lv
$discard,site=rt.com
$discard,site=sputniknews.com
```

---

## INTERPRETIVE CONTEXT FOR DOSSIER

### Tier 1 Sources

> Articles from **LSM (lsm.lv)** about any domain should be interpreted as Latvia's most authoritative and trusted public-interest journalism — its merged public-broadcaster structure provides institutional depth across parliament, defense, and foreign policy. LSM's editorial independence is legally protected, and it is the outlet Latvian policymakers cite most frequently. Its planned 2026 discontinuation of Russian-language content is itself a signal of how Latvia's government frames the Russophone information space.

> Articles from **Re:Baltica** about corruption, disinformation, or Russian influence should be interpreted as Latvia's highest-quality investigative reporting — grant-funded independence from both government and oligarchic interests makes it the only Latvian outlet capable of sustained adversarial investigation without ownership constraints. Its cross-border methodology (working with Estonian, Lithuanian, and Nordic partners) provides regional depth unavailable from any single-country outlet.

> Articles from **IR (ir.lv)** about domestic political dynamics and corporate misconduct should be interpreted as Latvia's most independent analytical journalism — its founding narrative (journalists leaving Diena after oligarchic takeover) is itself a key to understanding Latvian media-ownership dynamics. IR's independent-liberal orientation means it frames stories through a rule-of-law and transparency lens, which is valuable for institutional analysis but may underweight nationalist or populist perspectives that NRA captures.

### Tier 2 Sources

> Articles from **TVNET** about political and security developments should be interpreted as Latvia's primary extractable commercial news portal — with Delfi blocked by the pipeline's crawler, TVNET becomes the de facto high-traffic commercial source. Its Ekspress Grupp / Eesti Media ownership provides editorial independence from Latvian oligarchic interests, though it introduces a mild Estonian-commercial editorial lens.

> Articles from **Delfi Latvia** about any domain should be interpreted with awareness that full-text extraction is blocked — headlines and snippets may surface through Brave discovery, but the pipeline cannot verify or contextualize claims from Delfi without cross-referencing against extractable sources. Its Russian-language edition (rus.delfi.lv) is structurally critical for Russophone monitoring but faces the same extraction constraint.

> Articles from **NRA (Neatkariga Rita Avize)** about EU policy, migration, or national identity should be interpreted as reflecting Latvia's nationalist-conservative political current — its historical links to oligarch Aivars Lembergs and its Eurosceptic editorial orientation mean it amplifies sovereignty-first narratives that constrain the governing coalition's European integration agenda. What NRA front-pages signals what the nationalist wing wants amplified; this is essential for understanding domestic constraints on foreign policy.

> Articles from **saeima.lv, mod.gov.lv, mfa.gov.lv, mk.gov.lv, president.lv** should be interpreted as official government communications — not journalism but primary source material. Press releases, committee records, and official statements represent the government's chosen public position. Latvia's government sources are particularly high-signal for defense procurement (4.9% GDP allocation) and NATO host-nation coordination, where media coverage often lags official announcements.

> Articles from **LIIA** about Baltic security and transatlantic relations should be interpreted as expert analytical output from Latvia's premier foreign-policy research institute — its yearbooks and policy briefs reflect the strategic thinking of Latvia's defense and diplomatic establishment. LIIA's analysis should be treated as depth, not speed — it explains why events matter strategically rather than reporting them first.

# Official Government Sources — Supplementary Curation Prompt

## Usage

Replace `{{COUNTRY}}` and `{{LANGUAGE}}` with the target country and its primary language of political discourse. Provide the country's existing Source Intelligence Map as input context.

Run in Claude Research mode (Opus), one country at a time. This prompt produces the **Layer 2 (government monitoring) configuration** that operates alongside the Layer 1 (Brave Search news discovery) pipeline. It does not replace or re-evaluate the media sources in the existing map.

The output — a YAML monitoring manifest and interpretive context — feeds directly into the pipeline's government source fetch agent. The media sources in the existing map are handled separately by the Brave Search Goggle system (Layer 1).

Expected runtime: one pass per country.

---

## Prompt

You are producing an **Official Government Sources Supplement** for **{{COUNTRY}}** (primary language of political discourse: **{{LANGUAGE}}**).

### Context

You have been provided with an existing Source Intelligence Map for {{COUNTRY}}. That map covers media outlets, think tanks, and analytical sources. Your task is to identify the **official government sources** — the institutional web presences where the state itself publishes decisions, positions, records, and announcements — that are missing from the map.

### Why Government Sources Are Different

Government sources serve two distinct functions in the pipeline:

1. **Ground truth anchors.** When the government publishes the text of a defense procurement contract, a treaty ratification, a sanctions designation, or a legislative act, that document is the primary source. Media coverage of the same event is secondary — it may add context, interpretation, or criticism, but the pipeline needs the actual announcement to establish what happened.

2. **Intent signals.** What a government *chooses* to publicize, and how it frames it, is analytically significant in its own right. A foreign ministry press release emphasizing "strategic partnership" versus "constructive dialogue" is a posture signal. The defense ministry announcing a procurement decision on a Friday afternoon versus at a press conference is a framing decision. The pipeline needs to see these signals directly, not filtered through media interpretation.

Both functions require that government sources be present in the pipeline's results. However, government sources also require explicit interpretive framing — the pipeline LLM must understand that these are official positions, not independent reporting.

### Pipeline Architecture: Two-Layer Fetch

The MPM pipeline uses a two-layer fetch architecture:

**Layer 1 — News discovery (Brave Search):** Topic-based queries with per-country Goggles applied. Discovers what media outlets are reporting. Runs weekly. This layer handles signal detection — what's being covered, framed, and contested.

**Layer 2 — Government monitoring (direct fetch):** Scheduled polling of known institutional URLs. Discovers what the government actually *did* — the announcement, the text, the procurement notice, the committee report. This layer handles ground truth anchoring.

**You are producing the configuration for Layer 2.** Government sources are fetched directly because:

1. **Search indexing is unreliable for government content.** Press releases, policy documents, and official statements often don't appear in Brave's News Search index. Government websites are structured as institutional portals, not news publishers. Depending on search to discover them means depending on media to cover them first — which defeats the purpose of having primary sources.

2. **You already know what to fetch.** Search is for discovering unknown content. Government sources publish at known URLs on semi-predictable schedules. Direct polling is more reliable, more efficient, and eliminates the search-ranking dependency.

3. **Government content requires different extraction.** Press releases embedded in CMS templates, PDF policy documents, and parliamentary record systems all need different extraction approaches than news articles. The pipeline's Diffbot-based extraction layer is optimized for news-format HTML. Government sources often need Playwright (browser automation) or specialized PDF extraction.

Both layers feed into the same downstream stages: classification against the five analytical domains, clustering, and synthesis into weekly briefs.

### Priority Levels

| Priority | Fetch behavior | Default assignment |
|---|---|---|
| **P1** | Fetch every cycle; alert on fetch failure | Foreign ministry, defense ministry, head of government office — these produce the most time-sensitive, pipeline-relevant content |
| **P2** | Fetch every cycle; process if new content found; silence is normal | Parliament, official gazette, finance ministry, central bank, trade ministry — important but often periodic, with long gaps between publications |

Priority determines the pipeline's error-handling behavior. A P1 source returning no new content for a full cycle may indicate a fetch failure and should trigger an alert. A P2 source returning no new content is expected — parliamentary committees don't publish every week.

### What to Identify

For each of the following institutional categories, identify the specific official web presence for {{COUNTRY}}. Not every country will have all categories — skip any that don't apply and note why.

**Category 1: Head of Government / Head of State Office**
The office that publishes the leader's schedule, statements, speeches, bilateral meeting readouts, and official positions. In presidential systems, this is typically the presidential administration's website. In parliamentary systems, it may be the prime minister's office or a cabinet office. In dual-executive systems (e.g., France), identify both.

**Category 2: Foreign Ministry**
The ministry responsible for diplomatic relations. Publishes: diplomatic statements, bilateral/multilateral meeting readouts, treaty notifications, sanctions designations, ambassador appointments, consular notices. This is typically the single most important government source for the Diplomatic Alignment domain.

**Category 3: Defense / Security Ministry**
The ministry responsible for armed forces and defense policy. Publishes: procurement announcements, exercise notifications, deployment orders, defense white papers, bilateral defense cooperation agreements, force structure changes. May be split between a civilian defense ministry and a military general staff — identify both if they have separate web presences with distinct content.

**Category 4: Parliament / Legislature**
The institution that publishes: debate records (Hansard equivalents), committee reports, voting records, legislation text, parliamentary questions. Identify:
- The main parliamentary record/debate transcript system
- The foreign affairs committee (or equivalent)
- The defense/security committee (or equivalent)
- The finance/budget committee if it publishes reports on defense or foreign affairs spending

If committee work is published on a unified parliamentary portal, list the portal once and note which committees produce the most pipeline-relevant output.

**Category 5: Official Gazette / Legal Publication**
The publication of record for legislation, executive orders, treaties, and regulatory changes. In some countries this is a standalone publication (e.g., France's Journal Officiel, Germany's Bundesgesetzblatt); in others it's integrated into the parliamentary or government portal. This source matters for the Institutional Engagement domain — treaty ratifications, sanctions implementations, and regulatory changes appear here first.

**Category 6: Finance Ministry / Treasury**
Publishes: budget documents, fiscal policy statements, economic forecasts, sanctions implementation guidance, FDI screening decisions. Relevant to Economic & Technological Statecraft domain.

**Category 7: Central Bank**
Publishes: monetary policy decisions, financial stability reports, reserve management data, sanctions compliance guidance. Relevant to Economic & Technological Statecraft domain. Include only if the central bank publishes substantive policy communications (most do).

**Category 8: Trade / Commerce / Industry Ministry**
The ministry responsible for trade negotiations, export controls, industrial strategy, technology regulation. May overlap with the foreign ministry for trade agreements or the economy ministry for industrial policy. Identify the specific institutional source where trade deal announcements, export control changes, and investment screening decisions are published.

**Category 9: Intelligence / National Security Council (if public-facing)**
Some countries have a national security council, national security advisor's office, or intelligence oversight body that publishes reports, threat assessments, or policy documents. If no public-facing presence exists, note this — the absence itself is informative for the pipeline's Coverage Gap Assessment.

**Category 10: Country-Specific Institutional Sources**
Identify any official sources specific to this country's governance structure that don't fit the categories above but are essential for the pipeline. Examples:
- EU member states: the country's permanent representation to the EU, or national transposition databases for EU directives
- NATO members: statements from the country's NATO delegation
- Federal states: subnational government sources where defense-relevant decisions are made (e.g., German Länder with military bases, Canadian provinces with resource/trade jurisdiction)
- Monarchies: royal court communications where these serve a policy-signaling function
- Countries with parallel military/security structures: separate institutional sources for each (e.g., Iran's IRGC vs. regular military; Turkey's MIT)

### Output Format

For each source, use the same field structure as the existing Source Intelligence Map:

---

#### OFFICIAL GOVERNMENT SOURCES: {{COUNTRY}}

##### [Category Name]

**[Source Name]**

| Field | Detail |
|---|---|
| **Domain** | `[primary domain]` |
| **Entry Point URL** | The specific URL to poll — not the institutional homepage, but the press release index, news feed, or publication archive where new content appears. If the source has multiple relevant entry points (e.g., a foreign ministry with separate pages for press releases, bilateral statements, and treaty texts), list each. Mark uncertain URLs with `[VERIFY URL]`. |
| **RSS/Atom Feed** | URL of the RSS or Atom feed if available, or `None identified` / `[VERIFY RSS]`. RSS is the preferred fetch mechanism — it's structured, timestamped, and lightweight. Many government sites have RSS feeds that aren't prominently linked. |
| **Language** | [publication language(s)] |
| **Type** | `legislative_official` or `government_aligned` — use `legislative_official` for parliamentary/legislative sources and official gazettes; use `government_aligned` for executive branch sources |
| **Priority** | `P1` (fetch every cycle) or `P2` (fetch every cycle, process if relevant) — see Priority guidance below |
| **Domain Coverage** | [Which of the 5 analytical domains this source covers] |
| **Publication Frequency** | How often new content typically appears: `daily`, `several times per week`, `weekly`, `event-driven` (publishes in bursts around summits, sessions, crises), `periodic` (quarterly reports, annual reviews). This informs how the pipeline should handle "no new content" — for a daily source, silence is signal; for a periodic source, silence is normal. |
| **Content Format** | `HTML articles` (standard web pages), `PDF documents`, `HTML + PDF mix`, `embedded CMS` (content rendered within a portal framework that may resist standard extraction), `structured data` (e.g., legislative databases with query interfaces). Flag extraction-challenging formats. |
| **Extraction Method** | Recommended approach: `RSS parser` (preferred if feed available), `Diffbot` (standard article extraction), `Playwright` (for JavaScript-rendered pages, CMS frameworks, or sites requiring interaction), `PDF extraction` (for document-heavy sources), `Custom scraper` (for legislative databases or structured-data sources that need tailored parsing). |
| **Editorial Orientation** | Official government/institutional source — not independent journalism. [Note any specific framing patterns relevant to interpretation.] |
| **Why This Source** | [What ground-truth or intent-signaling function this source serves that media sources cannot replace] |
| **Access Notes** | [Free/restricted, language, any anti-bot measures, authentication requirements. Flag known Cloudflare or CAPTCHA protections with `[BOT PROTECTION]`.] |

*(Repeat for each source in this category)*

---

*(Repeat for each applicable category)*

---

#### GOVERNMENT SOURCE SUMMARY

| Category | Source | Domain | Priority | Extraction | RSS | Key Domain(s) |
|---|---|---|---|---|---|---|
| Head of Government | | | | | | |
| Foreign Ministry | | | | | | |
| Defense Ministry | | | | | | |
| Parliament | | | | | | |
| Official Gazette | | | | | | |
| Finance Ministry | | | | | | |
| Central Bank | | | | | | |
| Trade Ministry | | | | | | |
| NSC / Intelligence | | | | | | |
| Country-Specific | | | | | | |

**Categories not applicable:** [List any categories that don't apply to this country, with brief explanation]

**Total entry points to poll:** [N — count individual URLs/feeds, not institutional categories. A single ministry with three relevant entry points counts as three.]

---

#### MONITORING CONFIGURATION

Produce a structured monitoring manifest for all identified government sources, ready to be loaded by the pipeline's Layer 2 fetch agent:

```yaml
# Government Source Monitor: {{COUNTRY}}
# Generated: [date]

country: {{COUNTRY}}
language: {{LANGUAGE}}

sources:
  - name: [Source Name]
    category: [head_of_government | foreign_ministry | defense_ministry | parliament | gazette | finance_ministry | central_bank | trade_ministry | nsc_intelligence | country_specific]
    domain: [domain]
    priority: [P1 | P2]
    entry_points:
      - url: [specific URL to poll]
        type: [rss | html_index | pdf_archive | api_endpoint]
        content_format: [html | pdf | mixed | structured_data]
        extraction: [rss_parser | diffbot | playwright | pdf_extraction | custom]
    publication_frequency: [daily | several_per_week | weekly | event_driven | periodic]
    analytical_domains:
      - [diplomatic_alignment | security_defense | economic_statecraft | institutional_engagement | domestic_constraints]
    notes: [any access, format, or extraction concerns]
    verify: [true if any URLs or access details need manual verification, false otherwise]

  - name: [Next Source]
    ...
```

For sources with RSS feeds, the entry point should be the feed URL. For sources requiring Playwright, note any specific interaction required (e.g., "click 'Press Releases' tab, then scrape list page"). For PDF-heavy sources, note whether PDFs are linked from an index page or require navigating a document management system.

---

#### INTERPRETIVE CONTEXT

For each government source, provide a source-weighting statement the pipeline LLM should use when interpreting content from this institution. Government sources require a two-part interpretive frame:

**Part 1 — Content type classification:**
> "Content from [source] is [ground truth / intent signal / both]. When this source publishes [type of content], the pipeline should treat it as [what it establishes as fact] and note [what the framing or timing reveals about government intent]."

**Part 2 — Cross-layer interpretation:**
> "Cross-reference [source] content with [specific media source(s) from the existing whitelist] for independent assessment of significance and domestic reception. [Source] will tell the pipeline *what the government did*; [media source] will tell the pipeline *what it means domestically*."

This section will be loaded into the pipeline's system prompt alongside the existing interpretive context for media sources. It should make explicit that Layer 2 content (government sources) and Layer 1 content (media sources) serve complementary functions — the LLM needs both to produce grounded analysis.

---

#### PIPELINE INTEGRATION NOTES

Address the following operational considerations for the Layer 2 government monitoring:

1. **RSS availability assessment:** How many of the identified sources have usable RSS/Atom feeds? RSS is the lowest-cost, most reliable fetch mechanism. Sources with RSS feeds can be polled with a simple HTTP client; sources without feeds require Playwright or custom scrapers. Estimate the split — e.g., "6 of 10 entry points have RSS; 3 require Playwright; 1 requires PDF extraction."

2. **Publication timing and pipeline alignment:** Do the key government sources publish on predictable schedules that the pipeline's weekly cycle should align with? Note specific timing considerations — e.g., "parliamentary committee reports publish on Thursdays; cabinet meeting readouts publish Tuesday evenings; central bank decisions publish on the first Wednesday of each month." If significant government activity consistently falls outside the pipeline's Monday-to-Sunday window, note the misalignment.

3. **Extraction complexity ranking:** Rank the identified sources from easiest to hardest to extract, and estimate implementation effort for each tier:
   - **Low effort:** RSS feeds, clean HTML article pages (standard Diffbot)
   - **Medium effort:** JavaScript-rendered pages requiring Playwright, CMS-embedded content, mixed HTML/PDF
   - **High effort:** PDF-heavy sources requiring OCR or structured PDF extraction, legislative databases with query interfaces, sources behind bot protection

4. **Redundancy with Layer 1 (Brave news discovery):** Note which government announcements are likely to also surface through Layer 1 because media outlets reliably cover them. For example, a major defense procurement announcement will appear in both the defense ministry press release (Layer 2) and the FT or Reuters coverage (Layer 1). The pipeline will encounter both — note where Layer 2 provides ground truth that Layer 1 doesn't carry (e.g., exact contract values, treaty text, legislative language) versus where Layer 2 merely duplicates what the media already reported.

5. **Centralized vs. fragmented government web architecture:** Note which pattern {{COUNTRY}} follows. Centralized portals (like GOV.UK) simplify monitoring — one domain, one RSS feed, structured content. Fragmented architectures (separate domains per ministry) multiply the number of entry points and extraction methods. If the country has a centralized portal, assess whether it actually surfaces the content from all relevant ministries or whether ministry-specific sites carry content the portal doesn't propagate.

6. **Language and translation requirements:** If government sources publish in {{LANGUAGE}} and the pipeline's synthesis stage operates in English, note which sources require translation and whether the content is structured enough for reliable automated translation. Dense legal or legislative text translates differently from press-release prose — flag sources where translation quality may degrade analytical utility.

7. **Fallback to Layer 1:** For any government source category where direct fetch is impractical (e.g., the source is behind heavy bot protection, publishes only PDFs with poor OCR quality, or requires authenticated access), note that the pipeline should rely on Layer 1 media coverage of the same institution instead. Identify which media sources on the existing whitelist most reliably cover that institution's outputs. These fallback sources should receive a Goggle boost premium in the audit to compensate for the missing Layer 2 coverage.

---

### Calibration Notes

- **Verify current URLs.** Government websites restructure frequently, especially after elections or ministry reorganizations. If you are uncertain whether a URL is current, mark with `[VERIFY URL]`. If you can identify the URL pattern but not the exact current path, provide the pattern and flag it.
- **RSS feeds are gold.** Spend extra research effort identifying RSS/Atom feeds — they're often available but not prominently linked. Check `/feed`, `/rss`, `/atom`, and look for `<link rel="alternate" type="application/rss+xml">` in page source. An RSS feed for a foreign ministry press page eliminates the need for Playwright-based scraping entirely.
- **Don't assume English availability.** Many government sources publish exclusively in {{LANGUAGE}}. If an English-language version exists, note it — but the primary entry point should be the {{LANGUAGE}} version, which will typically have more complete and timelier content.
- **Parliamentary sources are often the most structurally complex.** Parliaments publish through committee systems, debate records, bill trackers, and question-time archives — often on different sub-domains or platforms. Identify the most pipeline-relevant entry points rather than mapping the entire parliamentary web architecture. Prioritize: (a) foreign affairs committee outputs, (b) defense committee outputs, (c) plenary debate records on foreign/defense policy.
- **Central banks are underrated for this pipeline.** Central bank communications surface economic statecraft signals (sanctions compliance, reserve diversification, currency swap agreements) that rarely appear in media coverage until they're analytically stale. Most central banks have well-structured, RSS-enabled press pages.
- **"No public-facing source" is a valid answer.** For categories like intelligence/NSC, many countries have no public-facing institutional web presence. State this explicitly — the absence is informative for the coverage gap assessment.
- **Priority assignment guidance.** `P1` (fetch every cycle): foreign ministry, defense ministry, head of government office — these produce the highest-signal, most time-sensitive content for the pipeline's analytical domains. `P2` (fetch every cycle, process if relevant): parliament, official gazette, finance ministry, central bank, trade ministry — these produce important but often periodic content where most weekly fetches will return nothing new. The distinction informs the pipeline's error handling: a P1 source returning no new content may indicate a fetch failure; a P2 source returning no new content is normal.
- **Entry points, not homepages.** The pipeline needs specific URLs to poll — the press release index page, the news feed, the committee reports archive. A ministry homepage is not an entry point; the `/press-releases` or `/news` page is. Be as specific as possible about where new content surfaces.

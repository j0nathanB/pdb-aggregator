# Official Government Sources Supplement: Hungary

## Preliminary Research

Let me first verify the current state of Hungarian government web infrastructure, given the regime transition in progress.
Now I have comprehensive data on all the relevant government web sources. Let me compile the full Official Government Sources Supplement.

---

# OFFICIAL GOVERNMENT SOURCES SUPPLEMENT: HUNGARY

Generated: 17 April 2026

---

## CRITICAL TRANSITION NOTE

Hungary is in the midst of a regime transition. 
The opposition Tisza Party, led by former Fidesz member and MEP Péter Magyar, won the election in a landslide, defeating the incumbent Fidesz–KDNP government of Prime Minister Viktor Orbán
. 
President Tamás Sulyok has formally tasked prime minister-elect Péter Magyar with forming the country's next government
.

**The government web infrastructure is currently in flux.** Hungary uses a centralized government portal (`kormany.hu`) that hosts all ministry sub-pages. 
The website http://kormany.hu is the official information homepage of the Government of Hungary
. 
This is the Hungarian language website of Hungary's government. Choosing English as the language of the site redirects to abouthungary.hu.
 Historical pattern shows that previous government transitions archived the old government portal (as seen with `2010-2014.kormany.hu` and `2015-2019.kormany.hu`). **The pipeline should expect URL restructuring within weeks of the new government's formation.** All URLs below are current as of 17 April 2026 and should be verified once the Magyar government's web infrastructure is established. Most are marked `[VERIFY URL]` accordingly.

Hungary follows a **centralized government web architecture**: 
the Defence Ministry, for example, resides at `kormany.hu/honvedelmi-miniszterium/`
, and the Finance Ministry at `kormany.hu/penzugyminiszterium`. However, several institutions have separate domains — the Parliament (`parlament.hu`), the central bank (`mnb.hu`), the President's Office (`sandorpalota.hu`), and the defence forces portal (`honvedelem.hu`).

---

#### Category 1: Head of Government / Head of State Office

##### 1a. Prime Minister's Office / Government Portal (Kormány)

**Government of Hungary — Kormány.hu**

| Field | Detail |
|---|---|
| **Domain** | `kormany.hu` |
| **Entry Point URL** | **Hungarian news index:** `https://kormany.hu/hirek` `[VERIFY URL]` — this is where government press releases and policy announcements surface. **English-language portal:** `https://abouthungary.hu/` — the English-language government communications site, operated by the International Communications Office of the Cabinet Office of the Prime Minister. **Both URLs may change under the new government.** |
| **RSS/Atom Feed** | Historical government portals had RSS: `https://2015-2019.kormany.hu/en/rss` provided ministry-by-ministry feeds. Current site RSS: `[VERIFY RSS]` — check `https://kormany.hu/feed` and `https://abouthungary.hu/feed` once the new government site launches. |
| **Language** | Hungarian (primary, kormany.hu); English (abouthungary.hu) |
| **Type** | `government_aligned` |
| **Priority** | `P1` |
| **Domain Coverage** | Diplomatic Alignment, Security & Defense, Economic & Technological Statecraft, Institutional Engagement, Domestic Constraints |
| **Publication Frequency** | Daily — multiple press releases, "Kormányinfó" weekly press briefings, PM statements |
| **Content Format** | HTML articles. abouthungary.hu is clean HTML suitable for standard extraction. kormany.hu uses a CMS portal framework. |
| **Extraction Method** | `Playwright` for kormany.hu (CMS-embedded, Hungarian-language); `Diffbot` for abouthungary.hu (clean English HTML articles). If RSS feeds exist post-transition, prefer `RSS parser`. |
| **Editorial Orientation** | Official government messaging. abouthungary.hu was explicitly designed as a Fidesz-era narrative tool. Its future under the Magyar government is uncertain — it may be restructured, replaced, or maintained under new editorial direction. Until transition is complete, interpret all content as reflecting the outgoing government's framing. |
| **Why This Source** | Provides ground truth on government decisions, policy announcements, and PM statements. The "Kormányinfó" weekly briefings are the primary channel for government policy communication — media coverage is always secondary to the briefing itself. |
| **Access Notes** | Free access. No authentication. Kormany.hu may have CAPTCHA on some sub-pages. `[BOT PROTECTION]` — the Parliament-related pages showed CAPTCHA challenges. |

##### 1b. President of the Republic (Köztársasági Elnöki Hivatal)

**Sándor Palace — Office of the President**

| Field | Detail |
|---|---|
| **Domain** | `sandorpalota.hu` |
| **Entry Point URL** | `https://www.sandorpalota.hu/en/main-page` `[VERIFY URL]` — the English-language main page. Hungarian news/press section at `https://www.sandorpalota.hu/hu/hirek` `[VERIFY URL]` |
| **RSS/Atom Feed** | `None identified` `[VERIFY RSS]` |
| **Language** | Hungarian (primary), English (limited) |
| **Type** | `government_aligned` |
| **Priority** | `P2` |
| **Domain Coverage** | Institutional Engagement, Domestic Constraints |
| **Publication Frequency** | Event-driven — publishes around bill-signings, state visits, National Day ceremonies, and Constitutional Court referrals. Typically several times per month, with long gaps. |
| **Content Format** | HTML articles |
| **Extraction Method** | `Playwright` (site structure unclear; may be simple enough for Diffbot once verified) |
| **Editorial Orientation** | Official presidential communications. President Sulyok is a Fidesz appointee; his framing may diverge from the incoming government's position. This divergence is analytically significant — the pipeline should track it as an indicator of institutional friction. |
| **Why This Source** | The president's bill-signing decisions and any Constitutional Court referrals are primary-source events that media may not cover with full text. In the current transition, presidential cooperation or obstruction is a key watch indicator (dossier Section 15). |
| **Access Notes** | Free access. Limited English content. |

---

#### Category 2: Foreign Ministry

**Ministry of Foreign Affairs and Trade (Külgazdasági és Külügyminisztérium)**

| Field | Detail |
|---|---|
| **Domain** | `kormany.hu` (sub-section) |
| **Entry Point URL** | `https://kormany.hu/kulgazdasagi-es-kulugyminiszterium` `[VERIFY URL]` — the ministry sub-page on the government portal. The archive version was at `2015-2019.kormany.hu/en/ministry-of-foreign-affairs-and-trade`. The new government will likely restructure this. **Fallback:** The ministry's Facebook page and the PM office press releases cover major diplomatic announcements. |
| **RSS/Atom Feed** | Historical archive had RSS per ministry. Current feed: `[VERIFY RSS]` post-transition. |
| **Language** | Hungarian (primary). English output through abouthungary.hu and international press releases. |
| **Type** | `government_aligned` |
| **Priority** | `P1` |
| **Domain Coverage** | Diplomatic Alignment (primary), Security & Defense, Economic & Technological Statecraft |
| **Publication Frequency** | Daily — bilateral meeting readouts, treaty announcements, sanctions positions, EU Council positions, ambassador appointments. The Orbán-era foreign ministry under Szijjártó was extremely active on social media (Facebook). |
| **Content Format** | HTML articles embedded in kormany.hu CMS |
| **Extraction Method** | `Playwright` for kormany.hu CMS. If RSS becomes available post-transition, switch to `RSS parser`. |
| **Editorial Orientation** | Official government diplomatic positions. Under the outgoing Szijjártó tenure, the ministry functioned as a vehicle for the multi-vector foreign policy. Under the incoming government, expect a sharp rhetorical reorientation toward pro-EU, pro-NATO framing. |
| **Why This Source** | Foreign ministry statements establish ground truth on bilateral relationships, treaty commitments, EU Council positions, and sanctions compliance. Media coverage of Hungarian diplomacy is always filtered through the reporter's framing; the ministry's own statements reveal official posture. |
| **Access Notes** | Free access. May restructure post-transition. |

---

#### Category 3: Defence / Security Ministry

##### 3a. Ministry of Defence (Honvédelmi Minisztérium)

| Field | Detail |
|---|---|
| **Domain** | `kormany.hu` (sub-section) |
| **Entry Point URL** | `https://kormany.hu/honvedelmi-miniszterium/` `[VERIFY URL]` — currently shows minimal content. |
| **RSS/Atom Feed** | `None identified` `[VERIFY RSS]` |
| **Language** | Hungarian |
| **Type** | `government_aligned` |
| **Priority** | `P1` |
| **Domain Coverage** | Security & Defense (primary), Diplomatic Alignment |
| **Publication Frequency** | Several times per week — procurement announcements, exercise notifications, NATO cooperation statements, defense budget decisions |
| **Content Format** | HTML articles within kormany.hu CMS |
| **Extraction Method** | `Playwright` |
| **Editorial Orientation** | Official defense ministry positions. Procurement decisions, NATO commitment statements, and bilateral defense cooperation agreements published here are ground truth. |
| **Why This Source** | Defense procurement contracts, force structure changes, and NATO obligation statements are primary-source events. The Zrínyi 2026 program status updates are pipeline-critical (dossier Section 12). |
| **Access Notes** | Free access. Limited content currently visible; may expand post-transition. |

##### 3b. Hungarian Defence Forces Portal (Honvédelem.hu)

| Field | Detail |
|---|---|
| **Domain** | `honvedelem.hu` |
| **Entry Point URL** | `https://honvedelem.hu/` (Hungarian); `https://defence.hu/` (English) |
| **RSS/Atom Feed** | `[VERIFY RSS]` — check `https://honvedelem.hu/feed` |
| **Language** | Hungarian (honvedelem.hu); English (defence.hu) |
| **Type** | `government_aligned` |
| **Priority** | `P1` |
| **Domain Coverage** | Security & Defense (primary) |
| **Publication Frequency** | Several times per week — operational updates, exercise coverage, international military cooperation, equipment deliveries |
| **Content Format** | HTML articles with photos/videos |
| **Extraction Method** | `Diffbot` (clean article format on defence.hu); `Playwright` for honvedelem.hu if CMS-embedded |
| **Editorial Orientation** | Military public affairs — factual operational reporting. Less politically colored than the ministry proper. Defence.hu English content is concise and operationally focused. |
| **Why This Source** | Provides operational ground truth: which exercises Hungary participates in, equipment deliveries (Lynx IFV, Leopard 2, etc.), NATO Forward Land Forces battlegroup activities, and international deployment updates. This content rarely appears in mainstream media but is pipeline-critical for the Security & Defense domain. |
| **Access Notes** | Free access. honvedelem.hu uses cookies. No authentication required. |

---

#### Category 4: Parliament / Legislature

**National Assembly (Országgyűlés)**

| Field | Detail |
|---|---|
| **Domain** | `parlament.hu` |
| **Entry Point URL** | `https://www.parlament.hu/` (Hungarian main portal) — the legislative agenda and session calendar are available at sub-pages. **Committee outputs:** accessed through the portal's committee system. The foreign affairs and defense committees publish reports through the unified portal. **Plenary records:** debate transcripts (napló) are published on the site. `[VERIFY URL]` — the site showed CAPTCHA challenges during research, which complicates automated access. |
| **RSS/Atom Feed** | `None identified` — historical versions did not have RSS. `[VERIFY RSS]` |
| **Language** | Hungarian (primary). Very limited English content (visitor information only). |
| **Type** | `legislative_official` |
| **Priority** | `P2` |
| **Domain Coverage** | Institutional Engagement (primary), Domestic Constraints |
| **Publication Frequency** | Event-driven — publishes during parliamentary session weeks (typically Tuesday-Friday when in session). Legislative calendar drives publication timing. Long gaps during recesses. **The new parliament will convene after the 2026 election; initial session timing is a key watch indicator.** |
| **Content Format** | `Embedded CMS` — content is rendered within a complex portal framework. Debate transcripts are HTML. Legislation text is structured data within the portal or linked to njt.hu. |
| **Extraction Method** | `Playwright` required — the site uses CMS framework rendering and has CAPTCHA challenges `[BOT PROTECTION]`. Custom extraction logic needed for committee report pages and debate transcripts. **This is the highest-complexity extraction target in the Hungarian government source set.** |
| **Editorial Orientation** | Institutional/legislative source. Under Fidesz, the parliamentary portal's editorial framing was government-aligned. Post-transition, expect the new Speaker to restructure portal messaging. |
| **Why This Source** | Ground truth for legislation text, voting records, committee hearings on EPPO accession, defense spending authorization, media law reform, and constitutional amendments. The pipeline needs the actual legislative text, not media summaries, to assess institutional engagement indicators (dossier Section 19). |
| **Access Notes** | Free access but `[BOT PROTECTION]` — CAPTCHA challenges were observed on multiple pages. May require manual verification or CAPTCHA-solving integration. Hungarian language only for substantive content. |

---

#### Category 5: Official Gazette / Legal Publication

##### 5a. Magyar Közlöny (Official Gazette)

| Field | Detail |
|---|---|
| **Domain** | `magyarkozlony.hu` |
| **Entry Point URL** | `https://magyarkozlony.hu/` `[VERIFY URL]` |
| **RSS/Atom Feed** | `None identified` |
| **Language** | Hungarian only |
| **Type** | `legislative_official` |
| **Priority** | `P2` |
| **Domain Coverage** | Institutional Engagement (primary) |
| **Publication Frequency** | Periodic — publishes when new legislation, government decrees, or official appointments are enacted. Can be daily during active legislative periods, weekly otherwise. |
| **Content Format** | `PDF documents` — the gazette is published as PDF files. 
The electronic version of Magyar Közlöny is regarded as trustworthy, with time stamp and with the electronic signature of the editor.
 |
| **Extraction Method** | `PDF extraction` — gazette issues are PDF files that require structured PDF parsing. Content is legally authoritative Hungarian text. |
| **Editorial Orientation** | Pure legal/regulatory publication — no editorial framing. |
| **Why This Source** | This is the authoritative publication of record. 
For countries with civil law systems, the official gazette often serves as the sole source of the authoritative texts of laws until updated codes are published. In most countries, a law enters into force on the date of publication in the official gazette.
 Treaty ratifications, sanctions implementations, EPPO accession legislation, and constitutional amendments appear here first. |
| **Access Notes** | Free access. PDF-heavy. Hungarian language only. |

##### 5b. Nemzeti Jogszabálytár (National Legislation Database)

| Field | Detail |
|---|---|
| **Domain** | `njt.hu` |
| **Entry Point URL** | `https://njt.hu/` (Hungarian); `https://njt.hu/translations` (English translations of selected legislation) |
| **RSS/Atom Feed** | `None identified` |
| **Language** | Hungarian (primary); 
English translations of laws specified by the minister responsible for justice are also available from the National Legislation Database.
 |
| **Type** | `legislative_official` |
| **Priority** | `P2` |
| **Domain Coverage** | Institutional Engagement |
| **Publication Frequency** | Continuous — database is updated as legislation enters into force. The translations page (`/translations`) updates periodically when new English translations are produced. |
| **Content Format** | `Structured data` — searchable legislative database with query interface. HTML rendering of legislation text. |
| **Extraction Method** | `Custom scraper` for monitoring new translations at `/translations`; `Playwright` for querying specific legislation by number. 
The search functionality made available on the website of the National Legislation Database (http://njt.hu) is provided to the public free of charge.
 |
| **Editorial Orientation** | Pure legislative database — no editorial framing. |
| **Why This Source** | English translations of key legislation enable the pipeline to process Hungarian law without translation overhead. Critical for monitoring EPPO accession legislation, new media law, constitutional amendments, and anti-corruption legislation. |
| **Access Notes** | Free access. Database query interface. No bot protection observed. |

---

#### Category 6: Finance Ministry / Treasury

**Ministry for National Economy (Nemzetgazdasági Minisztérium)**

**Note:** 
As of 31 December 2024, the Ministry of Finance was merged into the Ministry for National Economy, with the latter being responsible for public finance and economic development.
 The new government may restructure this arrangement.

| Field | Detail |
|---|---|
| **Domain** | `kormany.hu` (sub-section) |
| **Entry Point URL** | `https://kormany.hu/nemzetgazdasagi-miniszterium` `[VERIFY URL]` — ministry sub-page on government portal. **Post-transition restructuring expected.** |
| **RSS/Atom Feed** | `[VERIFY RSS]` |
| **Language** | Hungarian |
| **Type** | `government_aligned` |
| **Priority** | `P2` |
| **Domain Coverage** | Economic & Technological Statecraft (primary), Domestic Constraints |
| **Publication Frequency** | Several times per week — budget reports, fiscal policy statements, EU fund disbursement updates, FDI announcements |
| **Content Format** | HTML articles within kormany.hu CMS; PDF budget documents |
| **Extraction Method** | `Playwright` for HTML; `PDF extraction` for budget documents |
| **Editorial Orientation** | Official fiscal/economic messaging. Under the outgoing government, fiscal reporting was politically framed. The incoming government will likely present inherited fiscal data more critically (exposing deficits, hidden liabilities). |
| **Why This Source** | Budget decisions, EU fund co-financing commitments, FDI screening decisions, and fiscal forecasts are ground truth. The pipeline needs actual budget numbers, not media approximations, to assess fiscal capacity constraints (dossier Section 6). |
| **Access Notes** | Free access. Ministry restructuring likely post-transition. |

---

#### Category 7: Central Bank

**Magyar Nemzeti Bank (MNB)**

| Field | Detail |
|---|---|
| **Domain** | `mnb.hu` |
| **Entry Point URL** | **Monetary Council press releases (English):** `https://mnb.hu/en/pressroom/press-releases-of-the-monetary-council` — the highest-priority entry point. **General press releases (English):** `https://mnb.hu/en/pressroom/press-releases` — broader institutional communications. **Inflation reports:** `https://mnb.hu/en/monetary-policy/inflation-reports` `[VERIFY URL]` **Financial stability reports:** `https://mnb.hu/en/publications/reports-on-financial-stability` `[VERIFY URL]` |
| **RSS/Atom Feed** | `[VERIFY RSS]` — check `https://mnb.hu/en/feed` or within page source for `<link rel="alternate">` |
| **Language** | Hungarian (primary); English (full parallel publication of all major policy communications) |
| **Type** | `government_aligned` |
| **Priority** | `P1` |
| **Domain Coverage** | Economic & Technological Statecraft (primary), Domestic Constraints |
| **Publication Frequency** | Monetary Council meets monthly; press releases follow each meeting. Inflation reports quarterly. Financial stability reports semi-annually. Ad hoc press releases several times per month. |
| **Content Format** | HTML articles (press releases); PDF documents (reports) |
| **Extraction Method** | `Diffbot` for English press release pages (clean HTML). `PDF extraction` for reports. |
| **Editorial Orientation** | Institutional central bank communications. The MNB under Governor Mihály Varga (Fidesz appointee, term to 2031) represents a structural constraint on the incoming government's economic policy. MNB communications that diverge from government policy positions are analytically significant signals of institutional friction. |
| **Why This Source** | Monetary policy decisions (base rate, interest corridor), inflation forecasts, financial stability assessments, and reserve management data surface here first. The MNB's English-language publications are among the most complete and analytically useful of all Hungarian government sources. The pipeline should treat MNB communications as both ground truth (interest rate decisions are facts) and intent signals (framing of economic outlook reveals institutional posture toward the new government). |
| **Access Notes** | Free access. Well-structured English content. No bot protection observed. **The best-structured and most extraction-friendly Hungarian government source.** |

---

#### Category 8: Trade / Commerce / Industry Ministry

Trade policy is handled by the Ministry of Foreign Affairs and Trade (Category 2) and the Ministry for National Economy (Category 6). No separate trade ministry exists. Export control decisions and FDI screening are published through the government portal (kormany.hu). The new government may create a separate trade/industry portfolio.

---

#### Category 9: Intelligence / National Security Council

**No public-facing source.** Hungary's intelligence services — the Constitution Protection Office (AH), the Information Office (IH), and the Military National Security Service (KNBSZ) — have no public-facing web presence that publishes reports, threat assessments, or policy documents. The Sovereignty Protection Office (SPO), which had a web presence, is expected to be abolished under the incoming government.

The absence of a public national security council or intelligence oversight body with published outputs is a coverage gap. The pipeline should rely on Layer 1 media sources (particularly Direkt36, which has a track record on security/intelligence reporting) for intelligence-related developments.

---

#### Category 10: Country-Specific Institutional Sources

##### 10a. Hungary's Permanent Representation to the EU

| Field | Detail |
|---|---|
| **Domain** | EU Council / Consilium system |
| **Entry Point URL** | `https://www.consilium.europa.eu/en/council-eu/configurations/` — Hungary's positions in EU Council formations (Foreign Affairs, General Affairs, ECOFIN) are published through the Council's own press releases. No separate Hungarian permanent representation website was identified for public-facing policy content. |
| **RSS/Atom Feed** | Council RSS available at `https://www.consilium.europa.eu/en/rss/` |
| **Language** | English |
| **Type** | `legislative_official` (EU institutional) |
| **Priority** | `P2` |
| **Domain Coverage** | Diplomatic Alignment, Institutional Engagement |
| **Publication Frequency** | Event-driven — around Council meetings |
| **Content Format** | HTML articles |
| **Extraction Method** | `RSS parser` (Council feeds are well-structured) |
| **Editorial Orientation** | EU institutional source — not Hungarian government messaging |
| **Why This Source** | Hungary's voting positions in EU Council decisions — especially on sanctions, rule-of-law conditionality, and defense cooperation — are ground truth for the Diplomatic Alignment domain. The shift from Orbán-era obstruction to Magyar-era cooperation will be directly observable through Council voting records. |
| **Access Notes** | Free access. |

##### 10b. Government Debt Management Agency (ÁKK)

| Field | Detail |
|---|---|
| **Domain** | `akk.hu` |
| **Entry Point URL** | `https://akk.hu/en/` `[VERIFY URL]` — English-language site publishes bond auction results, debt management strategy, and issuance calendar |
| **RSS/Atom Feed** | `[VERIFY RSS]` |
| **Language** | Hungarian, English |
| **Type** | `government_aligned` |
| **Priority** | `P2` |
| **Domain Coverage** | Economic & Technological Statecraft, Domestic Constraints |
| **Publication Frequency** | Event-driven — bond auction days; quarterly debt management reports |
| **Content Format** | HTML + PDF mix |
| **Extraction Method** | `Diffbot` for HTML; `PDF extraction` for reports |
| **Editorial Orientation** | Technical financial institution |
| **Why This Source** | Sovereign debt issuance terms, investor demand at auctions, and yield movements are early indicators of market confidence in the new government. Relevant to the BBB/negative-outlook credit rating constraint (dossier Section 6). |
| **Access Notes** | Free access. |

##### 10c. Hungarian Energy and Public Utility Regulatory Authority (MEKH)

| Field | Detail |
|---|---|
| **Domain** | `mekh.hu` |
| **Entry Point URL** | `https://www.mekh.hu/` `[VERIFY URL]` — publishes energy market data, including crude oil import sources, gas supply statistics, and electricity generation mix |
| **RSS/Atom Feed** | `[VERIFY RSS]` |
| **Language** | Hungarian (primary), some English |
| **Type** | `government_aligned` |
| **Priority** | `P2` |
| **Domain Coverage** | Economic & Technological Statecraft |
| **Publication Frequency** | Periodic — monthly/quarterly statistical releases |
| **Content Format** | HTML + PDF/Excel data files |
| **Extraction Method** | `Custom scraper` for statistical data; `PDF extraction` for reports |
| **Editorial Orientation** | Technical regulatory body |
| **Why This Source** | MEKH data is the primary domestic source for tracking Russian crude oil share (93% in 2025), gas import sources, and electricity generation mix — the key measurable indicators of energy diversification (dossier Watch Indicators 7, 9). |
| **Access Notes** | Free access. Data-heavy. |

---

#### GOVERNMENT SOURCE SUMMARY

| Category | Source | Domain | Priority | Extraction | RSS | Key Domain(s) |
|---|---|---|---|---|---|---|
| Head of Government | kormany.hu + abouthungary.hu | kormany.hu, abouthungary.hu | P1 | Playwright / Diffbot | [VERIFY] | All five domains |
| Head of State | Sándor Palace (sandorpalota.hu) | sandorpalota.hu | P2 | Playwright | None | Institutional, Domestic |
| Foreign Ministry | MFA via kormany.hu | kormany.hu | P1 | Playwright | [VERIFY] | Diplomatic, Security, Economic |
| Defence Ministry | MoD via kormany.hu | kormany.hu | P1 | Playwright | None | Security & Defense |
| Defence Forces | honvedelem.hu / defence.hu | honvedelem.hu | P1 | Diffbot (EN) | [VERIFY] | Security & Defense |
| Parliament | parlament.hu | parlament.hu | P2 | Playwright [BOT PROTECTION] | None | Institutional, Domestic |
| Official Gazette | magyarkozlony.hu | magyarkozlony.hu | P2 | PDF extraction | None | Institutional |
| Legislation DB | njt.hu | njt.hu | P2 | Custom scraper | None | Institutional |
| Finance/Economy | NGM via kormany.hu | kormany.hu | P2 | Playwright | [VERIFY] | Economic, Domestic |
| Central Bank | mnb.hu | mnb.hu | P1 | Diffbot / PDF | [VERIFY] | Economic, Domestic |
| EU Council | consilium.europa.eu | consilium.europa.eu | P2 | RSS parser | Yes | Diplomatic, Institutional |
| Debt Agency | akk.hu | akk.hu | P2 | Diffbot / PDF | [VERIFY] | Economic, Domestic |
| Energy Regulator | mekh.hu | mekh.hu | P2 | Custom scraper | [VERIFY] | Economic |
| NSC / Intelligence | *No public source* | — | — | — | — | — |

**Categories not applicable:**
- **Separate Trade Ministry:** Trade is handled by MFA (merged as "Foreign Affairs and Trade") and the Ministry for National Economy. No standalone trade ministry source.
- **Intelligence/NSC public output:** No public-facing intelligence assessment or national security council publication system exists. This is a coverage gap filled by Layer 1 media (Direkt36 primary fallback).

**Total entry points to poll:** 16 individual URLs (counting separate entry points per source)

---

#### MONITORING CONFIGURATION

```yaml
# Government Source Monitor: Hungary
# Generated: 17 April 2026
# NOTE: URLs marked [VERIFY] should be checked after Magyar government web infrastructure is established

country: Hungary
language: hu  # Primary language of government publications is Hungarian; English noted where available

sources:
  - name: Government Portal (kormany.hu)
    category: head_of_government
    domain: kormany.hu
    priority: P1
    entry_points:
      - url: https://kormany.hu/hirek
        type: html_index
        content_format: html
        extraction: playwright
      - url: https://abouthungary.hu/
        type: html_index
        content_format: html
        extraction: diffbot
    publication_frequency: daily
    analytical_domains:
      - diplomatic_alignment
      - security_defense
      - economic_statecraft
      - institutional_engagement
      - domestic_constraints
    notes: "URL restructuring expected post-transition. abouthungary.hu is English; kormany.hu is Hungarian. Monitor both. Check for RSS feeds post-transition."
    verify: true

  - name: President of the Republic (Sándor Palace)
    category: head_of_government
    domain: sandorpalota.hu
    priority: P2
    entry_points:
      - url: https://www.sandorpalota.hu/hu/hirek
        type: html_index
        content_format: html
        extraction: playwright
    publication_frequency: event_driven
    analytical_domains:
      - institutional_engagement
      - domestic_constraints
    notes: "President Sulyok is Fidesz appointee; divergence from new government is a key analytical signal. Limited English."
    verify: true

  - name: Ministry of Foreign Affairs and Trade
    category: foreign_ministry
    domain: kormany.hu
    priority: P1
    entry_points:
      - url: https://kormany.hu/kulgazdasagi-es-kulugyminiszterium
        type: html_index
        content_format: html
        extraction: playwright
    publication_frequency: daily
    analytical_domains:
      - diplomatic_alignment
      - security_defense
      - economic_statecraft
    notes: "Ministry sub-page within centralized kormany.hu portal. URL will restructure post-transition. Fallback: abouthungary.hu diplomatic coverage."
    verify: true

  - name: Ministry of Defence
    category: defense_ministry
    domain: kormany.hu
    priority: P1
    entry_points:
      - url: https://kormany.hu/honvedelmi-miniszterium/
        type: html_index
        content_format: html
        extraction: playwright
    publication_frequency: several_per_week
    analytical_domains:
      - security_defense
      - diplomatic_alignment
    notes: "Currently sparse content. May be restructured post-transition. Use honvedelem.hu as primary defense source."
    verify: true

  - name: Hungarian Defence Forces Portal
    category: defense_ministry
    domain: honvedelem.hu
    priority: P1
    entry_points:
      - url: https://honvedelem.hu/
        type: html_index
        content_format: html
        extraction: playwright
      - url: https://defence.hu/
        type: html_index
        content_format: html
        extraction: diffbot
    publication_frequency: several_per_week
    analytical_domains:
      - security_defense
    notes: "defence.hu is English-language portal with clean article format. honvedelem.hu is Hungarian. Both active and regularly updated."
    verify: false

  - name: National Assembly (Országgyűlés)
    category: parliament
    domain: parlament.hu
    priority: P2
    entry_points:
      - url: https://www.parlament.hu/
        type: html_index
        content_format: embedded_cms
        extraction: playwright
    publication_frequency: event_driven
    analytical_domains:
      - institutional_engagement
      - domestic_constraints
    notes: "BOT PROTECTION: CAPTCHA observed. May require manual verification or CAPTCHA-solving. Hungarian only for substantive content. Committee outputs (foreign affairs, defense, finance) are pipeline-relevant. New parliament will convene after government formation."
    verify: true

  - name: Magyar Közlöny (Official Gazette)
    category: gazette
    domain: magyarkozlony.hu
    priority: P2
    entry_points:
      - url: https://magyarkozlony.hu/
        type: pdf_archive
        content_format: pdf
        extraction: pdf_extraction
    publication_frequency: periodic
    analytical_domains:
      - institutional_engagement
    notes: "PDF-only publication. Hungarian language. Authoritative source for new legislation entering into force. Pipeline should monitor for EPPO accession act, media law, constitutional amendments."
    verify: true

  - name: Nemzeti Jogszabálytár (National Legislation Database)
    category: gazette
    domain: njt.hu
    priority: P2
    entry_points:
      - url: https://njt.hu/translations
        type: html_index
        content_format: html
        extraction: custom
      - url: https://njt.hu/
        type: html_index
        content_format: structured_data
        extraction: playwright
    publication_frequency: periodic
    analytical_domains:
      - institutional_engagement
    notes: "The /translations page provides English translations of key Hungarian legislation. Monitor for new translations of pipeline-relevant acts. Main database is query-based, Hungarian language."
    verify: false

  - name: Ministry for National Economy (merged Finance)
    category: finance_ministry
    domain: kormany.hu
    priority: P2
    entry_points:
      - url: https://kormany.hu/nemzetgazdasagi-miniszterium
        type: html_index
        content_format: html
        extraction: playwright
    publication_frequency: several_per_week
    analytical_domains:
      - economic_statecraft
      - domestic_constraints
    notes: "Ministry of Finance was merged into NGM as of Dec 2024. New government may restructure. Budget documents are often PDF."
    verify: true

  - name: Magyar Nemzeti Bank (MNB)
    category: central_bank
    domain: mnb.hu
    priority: P1
    entry_points:
      - url: https://mnb.hu/en/pressroom/press-releases-of-the-monetary-council
        type: html_index
        content_format: html
        extraction: diffbot
      - url: https://mnb.hu/en/pressroom/press-releases
        type: html_index
        content_format: html
        extraction: diffbot
    publication_frequency: several_per_week
    analytical_domains:
      - economic_statecraft
      - domestic_constraints
    notes: "Best-structured Hungarian government source. Full English parallel content. Monetary Council meets monthly on pre-announced dates. Governor Varga term to 2031 = structural constraint on new government."
    verify: false

  - name: EU Council (Hungary positions)
    category: country_specific
    domain: consilium.europa.eu
    priority: P2
    entry_points:
      - url: https://www.consilium.europa.eu/en/press/press-releases/
        type: rss
        content_format: html
        extraction: rss_parser
    publication_frequency: event_driven
    analytical_domains:
      - diplomatic_alignment
      - institutional_engagement
    notes: "Monitor for Hungarian voting positions on sanctions, rule-of-law conditionality, and defense cooperation. RSS available."
    verify: false

  - name: Government Debt Management Agency (ÁKK)
    category: country_specific
    domain: akk.hu
    priority: P2
    entry_points:
      - url: https://akk.hu/en/
        type: html_index
        content_format: mixed
        extraction: diffbot
    publication_frequency: event_driven
    analytical_domains:
      - economic_statecraft
      - domestic_constraints
    notes: "Bond auction results and debt management strategy. Market confidence indicator."
    verify: true

  - name: Energy Regulatory Authority (MEKH)
    category: country_specific
    domain: mekh.hu
    priority: P2
    entry_points:
      - url: https://www.mekh.hu/
        type: html_index
        content_format: mixed
        extraction: custom
    publication_frequency: periodic
    analytical_domains:
      - economic_statecraft
    notes: "Primary source for energy import composition data (Russian crude share, gas import sources). Key for Watch Indicators 7 and 9."
    verify: true
```

---

#### INTERPRETIVE CONTEXT

**Government Portal (kormany.hu / abouthungary.hu)**
Content from this source is **intent signal** (how the government frames its actions) and **ground truth** (the text of policy announcements). When this source publishes a press release on a bilateral meeting or policy decision, the pipeline should treat the factual claims (who met, what was signed) as ground truth and the framing (how the meeting is characterized, which aspects are emphasized) as an intent signal revealing the government's posture. Cross-reference with Telex.hu and 444.hu (from the existing whitelist) for independent assessment of significance and domestic reception. **During the transition period**, content from this source reflects the outgoing Fidesz government until the Magyar government's web infrastructure is established. The pipeline should flag content published before and after the transition date with appropriate government attribution.

**President of the Republic (sandorpalota.hu)**
Content from this source is **intent signal**. The president's formal powers are largely ceremonial, but bill-signing statements, Constitutional Court referrals, and public remarks signal the degree of institutional cooperation or friction with the incoming government. Cross-reference with Telex.hu and HVG for independent assessment. When the president signs a bill without comment, this is routine; when the president issues a statement explaining a signature or requests Constitutional Court review, this is signal.

**Foreign Ministry (via kormany.hu)**
Content from this source is **both ground truth and intent signal**. Bilateral meeting readouts establish who met and what was discussed (ground truth); the language used to characterize relationships ("strategic partnership" vs. "constructive dialogue") is intent signal. Cross-reference with Reuters, AP, and the relevant partner country's foreign ministry for the other side's characterization of the same meeting.

**Defence Ministry / Defence Forces Portal (honvedelem.hu / defence.hu)**
Content from these sources is **primarily ground truth**. Equipment delivery announcements, exercise participation, NATO battlegroup activities, and procurement contract signings are verifiable facts. The framing is typically operational rather than political. Cross-reference with Jane's Defence Weekly and IISS for independent assessment of procurement significance.

**National Assembly (parlament.hu)**
Content from this source is **ground truth**. Legislation text, voting records, and committee reports are the primary documents. The pipeline should treat legislation text from parlament.hu (or njt.hu) as the authoritative source; media summaries of legislation should always be checked against the actual text. Cross-reference with HVG for parliamentary analysis and with Telex.hu for political context.

**Magyar Közlöny / njt.hu**
Content from these sources is **pure ground truth**. Legislation published in the gazette enters into force on the date of publication. No framing or intent signal — these are legal instruments. The pipeline should treat gazette publication as the definitive confirmation that a legislative or regulatory change has occurred.

**Magyar Nemzeti Bank (mnb.hu)**
Content from this source is **both ground truth and intent signal**. Interest rate decisions are ground truth. The Monetary Council's post-meeting statements are intent signals — the language used to characterize inflation risks, growth outlook, and monetary policy stance reveals the central bank's institutional posture. Under Governor Mihály Varga (term to 2031), divergence between MNB and government economic messaging is analytically significant. Cross-reference with Portfolio.hu (Hungarian financial news) and HVG for market reaction and independent assessment.

**EU Council (consilium.europa.eu)**
Content from this source is **ground truth** for Hungary's positions in EU institutional forums. Voting records, Council conclusions, and press releases establish what Hungary supported, opposed, or abstained on. Cross-reference with Telex.hu and Euractiv for domestic and EU-level political context.

**MEKH (Energy Regulator)**
Content from this source is **ground truth** — statistical data on energy imports, generation mix, and regulatory decisions. No framing or intent signal. This is the primary domestic source for the physical metrics that track energy diversification (dossier Watch Indicators 7 and 9).

---

#### PIPELINE INTEGRATION NOTES

**1. RSS availability assessment:**
Of the 16 identified entry points, only **1** has a confirmed RSS feed (EU Council via consilium.europa.eu). The MNB likely has RSS (to be verified — their page structure suggests it). The government portal historically had RSS per ministry but current availability is unverified due to the transition. **Estimated split: 1–2 RSS feeds confirmed; 8–10 require Playwright; 3–4 require PDF extraction or custom scraping.** Hungary's government web infrastructure is not RSS-friendly.

**2. Publication timing and pipeline alignment:**
- **MNB Monetary Council:** Meets on pre-announced Tuesdays (typically last Tuesday of each month). Press releases follow immediately. The pipeline should ensure the Monday-to-Sunday cycle captures the Tuesday meeting.
- **Kormányinfó (Government Info) briefings:** Historically held on Thursdays. These are the primary weekly government communication events.
- **Parliament:** Session days are typically Tuesday through Friday when in session. Committee reports may publish any day during session weeks.
- **Magyar Közlöny:** Can publish any weekday. No predictable schedule.
- **The pipeline's weekly cycle is adequate** for all Hungarian government sources. No significant misalignment identified.

**3. Extraction complexity ranking:**

**Low effort (2 sources, ~4 entry points):**
- MNB English press releases — clean HTML articles, standard Diffbot extraction
- defence.hu English portal — clean article format
- EU Council press releases — RSS available

**Medium effort (5 sources, ~6 entry points):**
- abouthungary.hu — clean HTML but may restructure
- kormany.hu ministry pages — CMS-embedded, requires Playwright
- sandorpalota.hu — Playwright needed, structure unclear
- akk.hu — mixed HTML/PDF
- honvedelem.hu — Hungarian CMS, Playwright

**High effort (4 sources, ~6 entry points):**
- parlament.hu — `[BOT PROTECTION]` CAPTCHA challenges, complex CMS, Hungarian only
- magyarkozlony.hu — PDF-only, requires structured PDF extraction of legal text
- njt.hu — database query interface requiring custom scraper logic
- mekh.hu — statistical data extraction requiring custom parsing

**4. Redundancy with Layer 1 (Brave news discovery):**
- **High redundancy:** Major government announcements (PM speeches, foreign ministry bilateral meetings, defense procurement) will appear in both Layer 2 (government source) and Layer 1 (media coverage). Layer 2 provides exact text, contract values, and treaty language that Layer 1 summaries omit.
- **Low redundancy — Layer 2 unique value:** MNB Monetary Council statements (full technical text rarely reproduced by media); Magyar Közlöny legislative text (media summarizes, not quotes); MEKH energy statistics (rarely covered until trends are dramatic); ÁKK bond auction results (specialist financial data); parliamentary committee reports (rarely covered by generalist media); and defence.hu operational updates (routine military activities not covered by mainstream outlets).
- **The strongest case for Layer 2** is MNB, Magyar Közlöny/njt.hu, and MEKH — these sources provide quantitative ground truth that Layer 1 simply does not carry.

**5. Centralized vs. fragmented government web architecture:**
Hungary follows a **hybrid model**: the government portal (`kormany.hu`) centralizes ministry content under one domain, but several key institutions have independent domains:
- `parlament.hu` (Parliament — independent domain)
- `mnb.hu` (Central bank — independent domain)
- `sandorpalota.hu` (President — independent domain)
- `honvedelem.hu` / `defence.hu` (Defence forces — independent domain)
- `njt.hu` (Legislation database — independent domain)

The centralized kormany.hu portal is the **most vulnerable to transition disruption** — the incoming government will likely restructure it. Independent-domain sources (MNB, Parliament, defence.hu) will remain stable through the transition.

**6. Language and translation requirements:**
- **English available:** MNB (full parallel English), defence.hu (English portal), abouthungary.hu (English), njt.hu translations page, akk.hu (English)
- **Hungarian only:** kormany.hu (main site), parlament.hu (substantive content), Magyar Közlöny, sandorpalota.hu (mostly), honvedelem.hu, MEKH
- **Translation quality concern:** Dense Hungarian legal text (Magyar Közlöny, njt.hu) is the highest-risk category for automated translation degradation. The pipeline should prefer njt.hu's official English translations when available rather than machine-translating gazette text.

**7. Fallback to Layer 1:**
- **parlament.hu** — CAPTCHA protection makes direct fetch unreliable. **Fallback:** Telex.hu and HVG reliably cover parliamentary proceedings. Boost these in the Goggle configuration for parliamentary coverage.
- **Magyar Közlöny** — PDF extraction of Hungarian legal text is high-effort and low-frequency. **Fallback:** njt.hu translations page for English-available legislation; Telex.hu and 444.hu for media coverage of new legislation. The pipeline can defer gazette processing to when njt.hu publishes an English translation.
- **MEKH** — custom extraction needed. **Fallback:** IEA Oil Market Reports and Eurostat energy statistics provide equivalent data with a lag. Clean Energy Wire (Clew) covers Hungarian energy developments in English.
- **kormany.hu ministry sub-pages** — if the transition breaks URLs before new ones are established. **Fallback:** abouthungary.hu (if maintained) or MTI wire service coverage via Layer 1.
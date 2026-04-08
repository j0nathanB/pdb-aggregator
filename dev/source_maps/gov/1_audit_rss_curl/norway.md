# Norway Government Sources — URL Fetchability Test Results

**Test date:** 2026-03-19
**Source document:** `docs/source_intelligence_maps/norway_government_sources.md`
**Method:** WebFetch (primary), curl with Mozilla UA (fallback for failures)

---

## Summary

| Metric | Count |
|---|---|
| **Total unique URLs tested** | 73 |
| **Successful (HTTP 200 / valid feed)** | 69 |
| **Failed (HTTP 404 / unreachable)** | 4 |
| **Success rate** | 94.5% |
| **[VERIFY] items tested** | 5 |
| **[VERIFY] items confirmed working** | 1 |
| **[VERIFY] items confirmed broken** | 4 |

### Failed URLs

| URL | Status | Notes |
|---|---|---|
| `https://www.regjeringen.no/no/aktuelt/offisielt-fra-statsrad/` | 404 | Council of State page — confirmed 404 via both WebFetch and curl |
| `https://www.nato.int/cps/en/natohq/topics_52055.htm` | 404 | NATO Norway country page — confirmed 404 via both WebFetch and curl |
| `https://www.nato.int/cps/en/natohq/rss_channels.htm` | 404 | NATO RSS channels hub — confirmed 404 via both WebFetch and curl |
| `https://www.norges-bank.no/en/rss-feeds/usd/` | 404 | [VERIFY RSS] — exchange rate RSS feed not found; confirmed 404 via curl |
| `https://www.norges-bank.no/en/rss-feeds/eur/` | 404 | [VERIFY RSS] — exchange rate RSS feed not found; confirmed 404 via curl |

Note: The NATO news page at `https://www.nato.int/cps/en/natohq/news.htm` returns HTTP 200 via curl, so the NATO site is partially functional — the Norway-specific topic page and RSS channels page have been moved or removed.

---

## 1. Regjeringen.no Platform (SMK, UD, FD, FIN, NFD)

### RSS Feeds

| Feed | URL | Status | Details |
|---|---|---|---|
| Main RSS (NO) | `https://www.regjeringen.no/no/rss/Rss/2581966/` | OK | Valid RSS 2.0, 100 items, title "RSS Regjeringen.no" |
| Main RSS (EN) | `https://www.regjeringen.no/en/rss/Rss/2581966/` | OK | Valid RSS 2.0, 100 items, title "RSS Regjeringen.no" |
| RSS config page | `https://www.regjeringen.no/no/aktuelt/rss/id2581966/` | OK | Working config page with filters for content type, topic, department, time period; 71,345 results |

### Entry Point URLs

| Source | URL | Status | Details |
|---|---|---|---|
| SMK news | `https://www.regjeringen.no/no/dep/smk/navigasjonssider/snarvei-nyheter/id2008097/` | OK | "Nyheter og pressemeldinger" — 778 items (shows FD filtered content; shared URL with FD) |
| UD news | `https://www.regjeringen.no/no/dep/ud/navigasjonssider/snarvei-nyheter/id2076040/` | OK | "Nyheter og pressemeldinger" — 2,174 items |
| FD news | `https://www.regjeringen.no/no/dep/fd/navigasjonssider/snarvei-nyheter/id2008097/` | OK | "Nyheter og pressemeldinger" — 778 items |
| FIN (NO) | `https://www.regjeringen.no/no/dep/fin/id216/` | OK | "Finansdepartementet" — ministry homepage |
| FIN (EN) | `https://www.regjeringen.no/en/dep/fin/id216/` | OK | "Ministry of Finance" |
| NFD (NO) | `https://www.regjeringen.no/no/dep/nfd/id714/` | OK | Ministry homepage |
| NFD (EN) | `https://www.regjeringen.no/en/dep/nfd/id714/` | OK | "About the Ministry" |
| NFD news [VERIFY URL] | `https://www.regjeringen.no/no/dep/nfd/navigasjonssider/snarvei-nyheter/id2076040/` | OK | Redirected to general news listing (2,174 items). Shares same ID as UD news — likely not NFD-specific |

### Additional Entry Points

| Page | URL | Status | Details |
|---|---|---|---|
| Council of State | `https://www.regjeringen.no/no/aktuelt/offisielt-fra-statsrad/` | **404** | Confirmed broken via WebFetch and curl |
| PM speeches | `https://www.regjeringen.no/no/aktuelt/taler_artikler/id1334/` | OK | "Taler og innlegg" — 1,787 items |
| English news | `https://www.regjeringen.no/en/whatsnew/news-and-press-releases/id2006120/` | OK | "News and press releases" — 1,795 items |
| UD Storting dialogue | `https://www.regjeringen.no/no/dep/ud/navigasjonssider/dialog_stortinget/id2076043/` | OK | "Svar til Stortinget" |
| Travel advisories | `https://www.regjeringen.no/no/tema/utenrikssaker/reiseinformasjon/id2413163/` | OK | "UDs reiseinformasjon" |
| EN foreign affairs | `https://www.regjeringen.no/en/topics/foreign-affairs/id919/` | OK | "Foreign affairs" |
| FD laws/regs | `https://www.regjeringen.no/no/dep/fd/navigasjonssider/snarvei-lover-og-regler/id2076491/` | OK | "Lover og regler" — 53 documents |
| FD speeches | `https://www.regjeringen.no/no/dep/fd/navigasjonssider/snarvei-taler-og-artikler/id2009271/` | OK | "Taler og innlegg" — 73 items |
| EN defence | `https://www.regjeringen.no/en/topics/defence/id215/` | OK | "Defence" |
| Budget 2026 (NO) | `https://www.regjeringen.no/no/statsbudsjett/2026/id3118616/` | OK | "Statsbudsjettet 2026" |
| Budget docs | `https://www.regjeringen.no/no/statsbudsjett/2026/dokumenter-og-pressemeldinger/id3119385/` | OK | Budget documents and press releases |
| Finance speech | `https://www.regjeringen.no/no/aktuelt/finanstalen/id3124569/` | OK | "Finanstalen" — full text of Finance Minister's speech |
| Budget 2026 (EN) | `https://www.regjeringen.no/en/national-budget/2026/id3118616/` | OK | "The National Budget 2026" |
| High North (EN) | `https://www.regjeringen.no/en/topics/foreign-affairs/high-north/id1154/` | OK | "The High North" |
| SMK (EN) | `https://www.regjeringen.no/en/dep/smk/id875/` | OK | "Office of the Prime Minister" |
| UD (EN) | `https://www.regjeringen.no/en/dep/ud/id833/` | OK | "Ministry of Foreign Affairs" |
| FD (EN) | `https://www.regjeringen.no/en/dep/fd/id380/` | OK | "Ministry of Defence" |

---

## 2. Stortinget (Parliament)

### Entry Point

| Page | URL | Status | Details |
|---|---|---|---|
| Cases & publications | `https://www.stortinget.no/no/Saker-og-publikasjoner/` | OK | "Saker og publikasjoner" — main legislative hub |
| RSS hub | `https://www.stortinget.no/no/Stottemeny/RSS/` | OK | Comprehensive RSS directory with 60+ feeds |
| English section | `https://www.stortinget.no/en/In-English/` | OK | English homepage for Stortinget |

### RSS Feeds

| Feed | URL | Status | Items |
|---|---|---|---|
| News (Aktuelt) | `https://www.stortinget.no/no/Stottemeny/RSS/Aktuelt-saker/` | OK | 40 items |
| Representative proposals | `https://www.stortinget.no/no/Stottemeny/RSS/Representantforslag/` | OK | 196 items |
| Committee statements | `https://www.stortinget.no/no/Stottemeny/RSS/Innstillinger-til-Stortinget/` | OK | 176 items |
| Plenary minutes | `https://www.stortinget.no/no/Stottemeny/RSS/Referater-fra-Stortinget/` | OK | 50 items |
| Europe Committee | `https://www.stortinget.no/no/Stottemeny/RSS/Referater-fra-Europautvalget/` | OK | 3 items |
| Legislative decisions | `https://www.stortinget.no/no/Stottemeny/RSS/Lovbeslutninger/` | OK | 33 items |
| Parliamentary decisions | `https://www.stortinget.no/no/Stottemeny/RSS/Stortingsvedtak/` | OK | 20 items |
| Energy (topic) | `https://www.stortinget.no/no/Stottemeny/RSS/Rss-lister-for-hovedtema/Energi/` | OK | 50 items |

---

## 3. Lovdata (Official Gazette)

### Entry Point

| Page | URL | Status | Details |
|---|---|---|---|
| Lovtidend register | `https://lovdata.no/register/lovtidend` | OK | "Norsk Lovtidend" — 84,179 documents |

### RSS Feeds

| Feed | URL | Status | Items |
|---|---|---|---|
| Laws & regulations (combined) | `http://lovdata.no/feed?data=LT&type=RSS` | OK | 100 items, "Lovdata - Siste fra Norsk lovtidend" |
| Lovtidend Avd. I (national) | `http://lovdata.no/feed?data=LTI&type=RSS` | OK | 100 items |
| Lovtidend Avd. II (regional) | `http://lovdata.no/feed?data=LTII&type=RSS` | OK | 100 items |
| New court judgments | `http://lovdata.no/feed?data=newJudgements&type=RSS` | OK | 100 items, "Lovdata - Siste avgjorelser" |
| Lovdata news | `http://lovdata.no/feed?data=newArticles&type=RSS` | OK | 20 items |

---

## 4. Norges Bank (Central Bank)

### Entry Points

| Page | URL | Status | Details |
|---|---|---|---|
| News | `https://www.norges-bank.no/en/news-events/news/` | OK | 1,880 news items |
| Calendar | `https://www.norges-bank.no/en/news-events/calendar/` | OK | Event calendar with rate decisions |
| RSS hub | `https://www.norges-bank.no/en/rss-feeds/` | OK | Lists 40+ feeds (publications + exchange rates) |

### RSS Feeds

| Feed | URL | Status | Items |
|---|---|---|---|
| Press releases | `https://www.norges-bank.no/en/rss-feeds/Press-releases---Norges-Bank/` | OK | 5 items |
| Monetary Policy Report | `https://www.norges-bank.no/en/rss-feeds/Norges-Bank-Monetary-Policy-Report-with-financial-stability-assessment/` | OK | 5 items |
| Speeches | `https://www.norges-bank.no/en/rss-feeds/Speeches---Norges-Bank/` | OK | 5 items |
| Economic Commentaries | `https://www.norges-bank.no/en/rss-feeds/Economic-Commentaries---Norges-Bank/` | OK | Valid feed, 0 items (empty but structurally valid) |
| Financial Stability Report | `https://www.norges-bank.no/en/rss-feeds/Financial-Stability-report---Norges-Bank/` | OK | 5 items |
| Regional Network Reports | `https://www.norges-bank.no/en/rss-feeds/Regional-network-reports---Norges-Bank/` | OK | 5 items |
| Staff Memos | `https://www.norges-bank.no/en/rss-feeds/Staff-Memo---Norges-Bank/` | OK | 5 items |
| Working Papers | `https://www.norges-bank.no/en/rss-feeds/Working-papers---Norges-Bank/` | OK | 5 items |
| USD exchange rate [VERIFY RSS] | `https://www.norges-bank.no/en/rss-feeds/usd/` | **404** | Feed not found. Exchange rate feeds may use different URL pattern than documented |
| EUR exchange rate [VERIFY RSS] | `https://www.norges-bank.no/en/rss-feeds/eur/` | **404** | Feed not found. Same issue as USD feed |

**Note on exchange rate feeds:** The RSS hub page at `/en/rss-feeds/` confirms 30+ exchange rate feeds exist, but the URL pattern `/en/rss-feeds/usd/` and `/en/rss-feeds/eur/` returns 404. The actual URLs likely use a different naming convention (possibly the full currency name rather than the ISO code). This needs investigation via the RSS hub page.

---

## 5. Intelligence Agencies (PST, E-tjenesten, NSM)

### PST (Police Security Service)

| Page | URL | Status | Details |
|---|---|---|---|
| All articles | `https://www.pst.no/alle-artikler/` | OK | News hub with threat assessments, podcast |
| English homepage | `https://www.pst.no/en/forside-english/` | OK | English landing page |
| RSS | None documented | N/A | No RSS — HTML scraping required |

### E-tjenesten (Intelligence Service)

| Page | URL | Status | Details |
|---|---|---|---|
| News | `https://www.etterretningstjenesten.no/aktuelt/` | OK | "Aktuelt og presse" |
| Fokus report | `https://www.etterretningstjenesten.no/publikasjoner/focus` | OK | Annual threat assessment with PDF downloads |
| RSS | None documented | N/A | No RSS — periodic check required |

### NSM (National Security Authority)

| Page | URL | Status | Details |
|---|---|---|---|
| News | `https://nsm.no/aktuelt/` | OK | 248 articles, filterable archive |
| Reports | `https://nsm.no/regelverk-og-hjelp/rapporter/` | OK | 25 reports including Risiko 2024-2026 |
| Risiko 2026 | `https://nsm.no/regelverk-og-hjelp/rapporter/risiko-2026` | OK | Published 2026-02-06, PDF and podcast available |
| RSS | None documented | N/A | No RSS — HTML scraping required |

---

## 6. Country-Specific Institutions

### NBIM (Government Pension Fund Global)

| Page | URL | Status | Details |
|---|---|---|---|
| Press releases | `https://www.nbim.no/en/news-and-insights/the-press/press-releases/` | OK | Archive from 2005-present |
| Reports | `https://www.nbim.no/en/news-and-insights/reports/` | OK | Reports from 1998-2025 |
| Fund overview | `https://www.nbim.no/en/the-fund/` | OK | Live fund value (21,268B NOK as of 2025-12-31) |
| Responsible investment | `https://www.nbim.no/en/responsible-investment/` | OK | ESG and climate action hub |
| Publications | `https://www.nbim.no/en/news-and-insights/publications/` | OK | Discussion notes and analysis |
| RSS | None documented | N/A | No RSS — HTML scraping required |

### Council on Ethics

| Page | URL | Status | Details |
|---|---|---|---|
| English homepage | `https://etikkradet.no/en/` | OK | "Council on Ethics" — exclusion recommendations |

### Equinor

| Page | URL | Status | Details |
|---|---|---|---|
| Newsroom | `https://www.equinor.com/news` | OK | "All corporate news" with topic filters |
| Investors | `https://www.equinor.com/investors` | OK | IR hub with share price, dividends, calendar |
| RSS [VERIFY] | None found | N/A | No RSS feed identified — confirmed no RSS |

### Forsvaret (Armed Forces)

| Page | URL | Status | Details |
|---|---|---|---|
| News | `https://www.forsvaret.no/aktuelt` | OK | "Aktuelt" — military news hub |
| RSS [VERIFY] | None found | N/A | No RSS feed identified — confirmed no RSS |

### eInnsyn (FOIA Portal)

| Page | URL | Status | Details |
|---|---|---|---|
| Homepage | `https://einnsyn.no/` | OK | "eInnsyn - Innsyn i offentlig saksbehandling" |

---

## 7. NATO / Arctic Council

| Page | URL | Status | Details |
|---|---|---|---|
| Norway country page | `https://www.nato.int/cps/en/natohq/topics_52055.htm` | **404** | Page removed or URL changed |
| RSS channels | `https://www.nato.int/cps/en/natohq/rss_channels.htm` | **404** | Page removed or URL changed |
| NATO news (alt) | `https://www.nato.int/cps/en/natohq/news.htm` | OK (curl) | Returns 200 — NATO site works but specific pages have moved |
| Arctic Council | `https://arctic-council.org/` | OK | Active site, Denmark chairs 2025-2027 |

---

## 8. [VERIFY] Items Summary

| Item | URL | Result | Recommendation |
|---|---|---|---|
| Regjeringen.no RSS query params | RSS config page | **VALID** — config page works; dynamic filter generation confirmed | Use unfiltered feed + client-side filtering |
| NFD news entry URL | `regjeringen.no/no/dep/nfd/.../id2076040/` | **VALID** — but redirects to general news (same ID as UD). Not NFD-specific | Use `/no/dep/nfd/id714/` as entry point instead |
| Norges Bank USD RSS | `norges-bank.no/en/rss-feeds/usd/` | **BROKEN (404)** | Investigate actual exchange rate feed URL pattern from RSS hub |
| Norges Bank EUR RSS | `norges-bank.no/en/rss-feeds/eur/` | **BROKEN (404)** | Investigate actual exchange rate feed URL pattern from RSS hub |
| Equinor RSS | None found | **CONFIRMED: No RSS** | HTML scraping required |
| Forsvaret RSS | None found | **CONFIRMED: No RSS** | HTML scraping required |

---

## 9. Recommendations

1. **Fix Council of State URL:** The entry point `https://www.regjeringen.no/no/aktuelt/offisielt-fra-statsrad/` returns 404. Search regjeringen.no for the current "Offisielt fra statsrad" URL.

2. **Fix NATO URLs:** Both the Norway country page and RSS channels page return 404. NATO appears to have restructured its website. The news page at `/natohq/news.htm` still works. Investigate current NATO RSS feed availability and Norway-specific topic URL.

3. **Investigate Norges Bank exchange rate RSS URLs:** The RSS hub confirms 30+ exchange rate feeds exist but the documented `/usd/` and `/eur/` paths are 404. Scrape the RSS hub page to extract the actual feed URLs.

4. **NFD entry URL shares ID with UD:** The documented NFD news URL (`id2076040`) is identical to the UD news URL and redirects to the general news listing. Use the ministry homepage `/no/dep/nfd/id714/` as the entry point instead, or find the correct NFD-specific news shortcut URL.

5. **Norges Bank Economic Commentaries feed is empty:** The feed is structurally valid but contains 0 items. This may be a temporary condition or the feed may have been deprecated. Monitor periodically.

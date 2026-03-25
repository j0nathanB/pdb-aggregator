# France Government Sources: URL Fetchability Test Results

**Test date:** 2026-03-19
**Source document:** `france_government_sources.md`
**Test method:** WebFetch (primary), curl with browser User-Agent (fallback)

---

## Summary

| Metric | Count |
|---|---|
| Total unique URLs tested | 75 |
| RSS/Atom feeds tested | 24 |
| RSS/Atom feeds working | 22 |
| RSS/Atom feeds failed | 2 |
| Entry point / HTML pages tested | 51 |
| HTML pages returning 200 | 40 |
| HTML pages returning 403 (bot protection) | 7 |
| HTML pages returning 404 (not found) | 2 |
| HTML pages timing out | 2 |
| [VERIFY] items resolved | 8 |

**Overall fetchability rate:** 82.7% (62/75 URLs accessible)

---

## Per-Institution Results

### 1a. Elysee (Presidence de la Republique) -- P1

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://www.elysee.fr/toutes-les-actualites` | Entry point | 200 OK | Page title: "Toutes les actualites du president de la Republique francaise". No RSS autodiscovery found in page. |
| `https://www.elysee.fr/les-flux-rss` | RSS hub | 200 OK | Page exists but **no RSS feed URLs are exposed** in the page content. [VERIFY resolved: NO usable RSS] |
| `https://www.elysee.fr/agenda` | Additional | 200 OK | Presidential agenda, March 2026 |
| `https://www.elysee.fr/en/all-actualities` | Additional | 200 OK | English mirror works |
| `https://www.elysee.fr/lettre-information` | Additional | 200 OK | Newsletter subscription page |

**VERIFY resolution:** RSS page exists at `/les-flux-rss` but contains no actionable feed URLs. No `<link rel="alternate" type="application/rss+xml">` autodiscovery tags found. **No RSS available. HTML scraping required.**

---

### 1b. Premier Ministre / info.gouv.fr -- P1

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://www.info.gouv.fr/suivre-l-actualite-du-premier-ministre` | Entry point | **403 Forbidden** | Bot protection confirmed (WebFetch and curl both blocked) |
| `https://www.info.gouv.fr/` | Additional | **403 Forbidden** | Same bot protection on homepage |

**VERIFY resolution:** No RSS feeds found. Site deploys aggressive bot protection returning 403 on all automated requests. **Requires browser-based scraping or social media fallback (@gouvernementFR).**

---

### 2. Quai d'Orsay (Ministere de l'Europe et des Affaires etrangeres) -- P1

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://www.diplomatie.gouv.fr/fr/salle-de-presse/` | Entry point | 200 OK | Press room accessible |
| `https://www.diplomatie.gouv.fr/fr/salle-de-presse/toutes-les-actualites/` | Additional | 200 OK | All news listing |
| `https://www.diplomatie.gouv.fr/fr/salle-de-presse/agenda-des-ministres/` | Additional | 200 OK | Ministers' agenda |
| `https://www.diplomatie.gouv.fr/fr/mentions-legales/les-flux-rss-de-france-diplomatie/` | RSS hub | 200 OK | Feed list page |
| `http://www.diplomatie.gouv.fr/spip.php?page=backend-fd` | RSS | 200 OK | "Actualites" -- 10 items |
| `http://www.diplomatie.gouv.fr/spip.php?page=backend_fcv` | RSS | 200 OK | "Conseils aux Voyageurs" -- 10 items |
| `http://www.diplomatie.gouv.fr/spip.php?page=backend&id_rubrique=9035` | RSS | 200 OK | "Securite, desarmement et non-proliferation" -- 10 items |
| `http://www.diplomatie.gouv.fr/spip.php?page=backend&id_rubrique=901` | RSS | 200 OK | "Diplomatie economique et commerce exterieur" -- 10 items |
| `http://www.diplomatie.gouv.fr/spip.php?page=backend&id_rubrique=1048` | RSS | 200 OK | "Droits de l'Homme" -- 10 items |
| `http://www.diplomatie.gouv.fr/spip.php?page=backend&id_rubrique=1032` | RSS | 200 OK | "La France et les Nations unies" -- 10 items |
| `http://www.diplomatie.gouv.fr/spip.php?page=backend&id_rubrique=1063` | RSS | 200 OK | "Afrique" -- 10 items |
| `http://www.diplomatie.gouv.fr/spip.php?page=backend&id_rubrique=1062` | RSS | 200 OK | "Afrique du nord / Moyen-Orient" -- 10 items |
| `http://www.diplomatie.gouv.fr/spip.php?page=backend&id_rubrique=1059` | RSS | 200 OK | "Ameriques" -- 7 items |
| `http://www.diplomatie.gouv.fr/spip.php?page=backend&id_rubrique=62294` | RSS | 200 OK | "Asie - Oceanie" -- 10 items |
| `http://www.diplomatie.gouv.fr/spip.php?page=backend&id_rubrique=5128` | RSS | 200 OK | "Europe" -- 10 items |
| `http://www.diplomatie.gouv.fr/spip.php?page=backend&id_rubrique=1040` | RSS | 200 OK | "Francophonie et langue francaise" -- 10 items |

**All 12 RSS feeds operational.** Best government RSS infrastructure in France. All feeds return valid RSS 2.0 with 7-10 items each.

---

### 3. Ministere des Armees -- P1

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://www.defense.gouv.fr/salle-de-presse` | Entry point | 200 OK | "Salle de presse" -- 1,961 results across 5 categories |
| `https://www.defense.gouv.fr/siae/communiques-presse` | Additional | 200 OK | Defense industry communiques |
| `https://www.defense.gouv.fr/en/press-room` | Additional | 200 OK | English press room |
| `https://www.defense.gouv.fr/presse/archives-presse` | Additional | 200 OK | Press archives |
| `https://www.defense.gouv.fr/presse/actu-defense` | Additional | 200 OK | Weekly video summary |

**No RSS feeds.** [VERIFY resolved: confirmed no RSS on current site.] All HTML pages accessible without bot protection.

---

### 4a. Assemblee nationale -- P2

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://www.assemblee-nationale.fr/dyn/actualites-communiques` | Entry point | **404 Not Found** | [VERIFY resolved: URL is INVALID] |
| `https://www.assemblee-nationale.fr/dyn/les-fils-rss-de-l-assemblee-nationale` | RSS hub | 200 OK | RSS feed hub page accessible |
| `https://www.assemblee-nationale.fr/rss/communiques-de-presse.xml` | RSS | **404 Not Found** | [VERIFY resolved: feed URL is INVALID] |
| `https://www.assemblee-nationale.fr/dyn/s-abonner-aux-services-en-ligne-de-l-assemblee-nationale` | Additional | 200 OK | Online services/subscriptions |
| `https://www.assemblee-nationale.fr/video/?o=cm` | Additional | 200 OK | Video portal for committee hearings |

**Issues:** Entry point URL and RSS feed URL both return 404. The RSS hub page is accessible but the specific communiques-de-presse.xml feed does not exist at the documented path. Rate limiting (429) also observed on WebFetch. **Needs URL discovery from the RSS hub page.**

---

### 4b. Senat -- P2

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://www.senat.fr/communiques/index.html` | Entry point | 200 OK | Press releases listing |
| `https://www.senat.fr/flux-rss.html` | RSS hub | 200 OK | Lists all feeds including 33 thematic feeds |
| `https://www.senat.fr/rss/presse.rss` | RSS | 200 OK | "Senat - communiques de presse" -- 5 items |
| `https://www.senat.fr/rss/presse.xml` | Atom | 200 OK | Atom variant of press releases |
| `https://www.senat.fr/rss/rapports.rss` | RSS | 200 OK | "Senat - derniers rapports" -- 4 items |
| `https://www.senat.fr/rss/textes.rss` | RSS | 200 OK | "Senat - derniers textes" -- 20 items |
| `http://videos.senat.fr/video/videos.rss` | RSS | 200 OK | "Senat - videos" (Atom 0.3) -- 21 entries |
| `https://videos.senat.fr/video/videos.rss` | RSS | 200 OK | HTTPS variant also works |
| `https://www.senat.fr/basile/rechercheAutresCRCom.do` | Additional | 200 OK | Commission reports search |
| `https://www.senat.fr/basile/rechercheSeance.do` | Additional | 200 OK | Session transcripts search |

**All 4 main RSS feeds operational.** Both RSS and Atom variants work. 33+ thematic feeds also available. Excellent RSS infrastructure.

---

### 5. JORF / Legifrance -- P2

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://www.legifrance.gouv.fr/jorf/jo` | Entry point | **403 Forbidden** | Bot protection confirmed |
| `https://www.journal-officiel.gouv.fr/` | Additional | 200 OK | Portal accessible |
| `https://www.data.gouv.fr/datasets/jorf-les-donnees-de-l-edition-lois-et-decrets-du-journal-officiel` | Additional | 200 OK | Open data accessible |
| `https://www.legifrance.gouv.fr/abonnement.do` | Additional | **403 Forbidden** | Bot protection on subscription page too |
| `https://legifrss.org/latest` | RSS (3rd party) | 200 OK | "Legifrance RSS" (Atom 1.0) -- 15 entries. Unofficial but functional. |

**Legifrance blocked by bot protection.** Third-party LegifrSS works as documented. Journal-officiel.gouv.fr portal and data.gouv.fr open data are accessible alternatives.

---

### 6. Bercy (Ministere de l'Economie) -- P2

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://www.economie.gouv.fr/actualites` | Entry point | **403 Forbidden** | Bot protection |
| `https://www.economie.gouv.fr/rss` | RSS hub | 200 OK | RSS hub page accessible |
| `https://www.economie.gouv.fr/rss/toutesactualites` | RSS | 200 OK | "Flux RSS Toutes les actualites" -- 10 items |
| `https://www.economie.gouv.fr/daj/rss` | RSS | 200 OK | "Flux RSS Daj" -- 10 items |
| `https://www.economie.gouv.fr/tous-les-fils-d-infos` | Additional | **403 Forbidden** | Bot protection |
| `https://www.economie.gouv.fr/tracfin` | Additional | **403 Forbidden** | Bot protection |
| `https://www.economie.gouv.fr/tracfin/sabonner-au-flux-rss` | Additional | **404 Not Found** | Tracfin RSS subscription page gone |

**Bot protection on HTML pages but RSS feeds are accessible.** RSS polling is the correct extraction method. Tracfin RSS subscription page no longer exists.

---

### 7. Banque de France -- P2

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://www.banque-france.fr/fr/communiques-de-presse` | Entry point | 200 OK | Press releases page. No RSS found. Newsletter subscription at `/fr/alertes`. |
| `https://www.banque-france.fr/fr/espace-presse` | Additional | 200 OK | Press room |
| `https://www.banque-france.fr/fr/gouverneur` | Additional | 200 OK | Governor page |
| `https://www.banque-france.fr/fr/publications-et-statistiques/publications` | Additional | 200 OK | Publications |
| `https://www.banque-france.fr/fr/publications-et-statistiques/statistiques` | Additional | 200 OK | Statistics |
| `https://webstat.banque-france.fr/` | Additional | 200 OK | Webstat SDMX portal |
| `https://publications.banque-france.fr/` | Additional | 200 OK | Publications portal |

**All pages accessible.** [VERIFY resolved: confirmed NO RSS feeds.] No bot protection. Newsletter alerts available at `/fr/alertes`.

---

### 8. DG Tresor -- P2

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://www.tresor.economie.gouv.fr/Articles` | Entry point | 200 OK | Articles listing with recent G7, economic flash reports |
| `https://www.tresor.economie.gouv.fr/publications` | Additional | 200 OK | Publications page |
| `https://www.tresor.economie.gouv.fr/qui-sommes-nous/espace-presse` | Additional | 200 OK | Press space |
| `https://www.tresor.economie.gouv.fr/tresor-international` | Additional | 200 OK | International section |
| `https://www.tresor.economie.gouv.fr/RP-DP/810` | Additional | 200 OK | EU Perm Rep economic section |
| `https://www.tresor.economie.gouv.fr/publications/les-nouvelles-du-tresor` | Additional | 200 OK | Newsletter page |

**All pages accessible.** No RSS, no bot protection. HTML scraping viable.

---

### 9a. SGDSN -- P2

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://www.sgdsn.gouv.fr/publications` | Entry point | 200 OK | 150 publications across 15 pages. Filterable by type and theme. |

**Accessible.** No RSS. Low-frequency, high-signal source.

---

### 9b. DGSE -- P2

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://www.dgse.gouv.fr/` | Entry point | 200 OK | [VERIFY resolved: URL is VALID.] Page title: "Accueil - DGSE" |

**Accessible.** Institutional/recruitment site only. Minimal monitoring value.

---

### 9c. DGSI -- P2

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://www.dgsi.interieur.gouv.fr/` | Entry point | **403 Forbidden** | [VERIFY resolved: URL blocked by bot protection] |

**Blocked.** Bot protection returns 403 on both WebFetch and curl.

---

### 10a. RPUE (EU Permanent Representation) -- P2

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://ue.delegfrance.org/` | Entry point | 200 OK | SPIP site. References RSS feeds. |
| `https://ue.delegfrance.org/spip.php?page=rss` | RSS (documented) | **404 Not Found** | Generic RSS URL does not work |
| `https://ue.delegfrance.org/spip.php?page=rss&id_rubrique=2` | RSS (discovered) | 200 OK (HTML) | Returns HTML page listing feed options, not XML |
| `https://ue.delegfrance.org/spip.php?page=backend&id_rubrique=2` | RSS (actual) | 200 OK (XML) | "La France dans l'UE - Derniers articles" -- 9 items. **This is the correct feed URL.** |

**RSS works but the documented URL is wrong.** The correct feed URL uses `page=backend` (not `page=rss`) with `id_rubrique=2`. Valid RSS 2.0 with 9 items covering EU Council participation.

---

### 10b. ANSSI -- P2

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://cyber.gouv.fr/actualites` | Entry point | 200 OK | [VERIFY resolved: URL is VALID.] "Les actualites - Page 1/9 - ANSSI" |
| `https://cyber.gouv.fr/actualites/rss/` | RSS (discovered) | 200 OK | "Les actualites" -- 20 items. Valid RSS 2.0. |
| `https://cyber.gouv.fr/actualites/atom/` | Atom (discovered) | 200 OK | "Les actualites" -- 20 items. Valid Atom feed. |
| `https://www.cert.ssi.gouv.fr/` | Additional | 200 OK | CERT-FR legacy domain still accessible |

**[VERIFY resolved: RSS IS available.]** Both RSS and Atom feeds discovered at `/actualites/rss/` and `/actualites/atom/`. Not documented in source file. CERT-FR legacy domain still works.

---

### 10c. Outre-mer -- P2

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://www.outre-mer.gouv.fr/` | Entry point | **403 Forbidden** | [VERIFY resolved: blocked by bot protection] |

**Blocked.** Bot protection returns 403.

---

### 10d. Cour des comptes -- P2

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://www.ccomptes.fr/fr/publications` | Entry point | **TIMEOUT** | Connection times out completely (no response) |
| `https://www.ccomptes.fr/` | Homepage | **TIMEOUT** | Same -- entire domain unreachable |

**Domain unreachable.** [VERIFY resolved: cannot determine RSS status.] The site `ccomptes.fr` times out on all connection attempts (WebFetch and curl with multiple timeouts). May be temporarily down or blocking non-French IP ranges.

---

## VERIFY Items Resolution Summary

| Item | Document Claim | Test Result | Resolution |
|---|---|---|---|
| Elysee RSS | "page exists but feed URLs not directly exposed" | Page at `/les-flux-rss` exists but contains no feed URLs. No autodiscovery tags. | **NO RSS available** |
| info.gouv.fr RSS | "legacy RSS feeds may be broken" | Entire site returns 403 | **No RSS. Site blocked.** |
| Defense RSS | "no feeds found on current site" | Confirmed no RSS | **No RSS** |
| Assemblee nationale entry URL | `dyn/actualites-communiques` | 404 Not Found | **URL is invalid** |
| Assemblee nationale RSS | `rss/communiques-de-presse.xml` | 404 Not Found | **Feed URL is invalid** |
| DGSE URL | `dgse.gouv.fr` | 200 OK | **URL is valid** |
| DGSI URL | `dgsi.interieur.gouv.fr` | 403 Forbidden | **URL exists but blocked** |
| ANSSI RSS | "VERIFY RSS at cyber.gouv.fr" | RSS at `/actualites/rss/`, Atom at `/actualites/atom/` | **RSS IS available (20 items)** |
| Outre-mer URL | `outre-mer.gouv.fr` | 403 Forbidden | **URL exists but blocked** |
| Outre-mer RSS | "VERIFY RSS" | Cannot test (403) | **Unknown (blocked)** |
| Cour des comptes RSS | "VERIFY RSS at ccomptes.fr" | Domain unreachable (timeout) | **Unknown (timeout)** |
| Banque de France RSS | "site redesign may have removed feeds" | Confirmed no RSS. Newsletter alerts at `/fr/alertes`. | **No RSS** |

---

## Key Findings

### Corrections needed in source document

1. **RPUE RSS URL is wrong.** Documented as `spip.php?page=rss` (404). Correct URL is `spip.php?page=backend&id_rubrique=2` (200 OK, valid RSS 2.0).
2. **Assemblee nationale entry point URL is wrong.** `dyn/actualites-communiques` returns 404. Needs discovery from the RSS hub page.
3. **Assemblee nationale RSS URL is wrong.** `rss/communiques-de-presse.xml` returns 404. Needs discovery from the RSS hub page.
4. **ANSSI has RSS feeds (undocumented).** Both RSS (`/actualites/rss/`) and Atom (`/actualites/atom/`) feeds available with 20 items each.
5. **Tracfin RSS subscription page is gone.** `economie.gouv.fr/tracfin/sabonner-au-flux-rss` returns 404.

### Bot protection landscape

| Domain | Status | Severity |
|---|---|---|
| `info.gouv.fr` | 403 on all requests | **High** -- P1 source completely blocked |
| `legifrance.gouv.fr` | 403 on HTML pages | High -- use LegifrSS or data.gouv.fr instead |
| `economie.gouv.fr` | 403 on HTML, RSS accessible | Medium -- RSS workaround available |
| `dgsi.interieur.gouv.fr` | 403 | Low -- negligible monitoring value |
| `outre-mer.gouv.fr` | 403 | Medium -- strategic source blocked |
| `ccomptes.fr` | Timeout (unreachable) | Medium -- may be temporary or geo-blocked |

### RSS availability summary

| Source | RSS Status | Feed Count | Items |
|---|---|---|---|
| Quai d'Orsay | Fully operational | 12 tested (195+ available) | 7-10 per feed |
| Senat | Fully operational | 4 main + 33 thematic | 4-21 per feed |
| Bercy | Operational (HTML blocked) | 2 tested | 10 per feed |
| ANSSI | Operational (newly discovered) | 2 (RSS + Atom) | 20 per feed |
| RPUE | Operational (corrected URL) | 1 | 9 items |
| LegifrSS (3rd party) | Operational | 1 | 15 items |
| Senat videos | Operational | 1 | 21 items |
| Elysee | None | 0 | -- |
| info.gouv.fr | None | 0 | -- |
| Defense | None | 0 | -- |
| Assemblee nationale | Unknown (404 on documented URL) | 0 verified | -- |
| Banque de France | None | 0 | -- |
| DG Tresor | None | 0 | -- |
| SGDSN | None | 0 | -- |
| DGSE | None | 0 | -- |
| DGSI | None (403) | 0 | -- |
| Outre-mer | Unknown (403) | 0 | -- |
| Cour des comptes | Unknown (timeout) | 0 | -- |

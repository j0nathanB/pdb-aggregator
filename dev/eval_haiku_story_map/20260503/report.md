# Haiku 4.5 vs Sonnet 4.6 — story_map eval, 20260503

Mechanical replay. Identical system + user prompts; only `model` swapped. URL overlap = % of Sonnet's URLs (representative + article) present in any Haiku story. Story-pair matching is greedy by Jaccard URL overlap, 10% floor.

## Per-country summary

| Code | Stories (S→H) | Single-src (S→H) | Off-topic (S→H) | URL overlap | Avg src/story (S→H) | Matched / S orph / H orph | $ (S→H) | Δ$ | Lat (s) |
|------|---------------|------------------|-----------------|-------------|----------------------|---------------------------|---------|-----|--------|
| **mx** | 10→18 | 0→10 | 62→62 | 50% | 15.6→7.0 (max 47→17) | 8 / 2 / 10 | $0.85→$0.24 | **−$0.61** | 397.0 |
| **jp** | 10→9 | 13→10 | 212→127 | 82% | 6.4→6.1 (max 23→21) | 8 / 2 / 1 | $0.61→$0.14 | **−$0.47** | 104.6 |
| **br** | 7→12 | 0→36 | 117→124 | 58% | 21.0→14.4 (max 42→28) | 5 / 2 / 7 | $0.87→$0.29 | **−$0.58** | 406.1 |
| **fi** | 0→12 | 0→21 | 0→89 | 0% | 0.0→10.6 (max 0→18) | 0 / 0 / 12 | $0.76→$0.18 | **−$0.58** | 159.2 |
| **total** | | | | | | | **$3.09→$0.85** | **−$2.24** | |

## Per-country drilldown

### mx

Haiku replay: input=120,434 out=23,983 tokens, latency=397.0s **[no-tool fallback]**

**Matched stories** (best 6 by URL overlap):

- jaccard=0.75  S: _Trump mocks Sheinbaum at private dinner, imitates her voice over Gulf of Mexico _  ↔  H: _Trump ridicules Sheinbaum over Gulf of Mexico name change dispute_
- jaccard=0.53  S: _Morena holds national congress, names Ariadna Montiel as new party president ami_  ↔  H: _Morena appoints Adriana Montiel as new party president; Luisa María Alcalde depa_
- jaccard=0.52  S: _Pemex reports 46 billion peso loss in Q1 2026 while debt falls to 12-year low; a_  ↔  H: _Pemex reports losses of 45.9 billion pesos in first quarter 2026; debt declines _
- jaccard=0.50  S: _Mexico's Q1 2026 GDP contracts 0.8%, worse than expected; analysts cut full-year_  ↔  H: _Mexico's economy contracts 0.8% in first quarter 2026, slowdown amid uncertainty_
- jaccard=0.48  S: _Banxico reports 410 billion peso operating loss for 2025, leaves government with_  ↔  H: _Banxico may implement final rate cut in May despite inflation pressures_
- jaccard=0.28  S: _CJNG crackdown intensifies: SEMAR arrests 'El Jardinero' as cartel loses success_  ↔  H: _SEMAR captures 'El Jardinero,' key CJNG operative, after 19 months of intelligen_

**Sonnet stories with no Haiku match** (2):

- Morena's internal response to Sinaloa crisis: legislators defend Rocha's leave, others call for acco (sources=7)
- Sheinbaum signs 40-hour workweek constitutional agreement on Labor Day, meets with (sources=0)

**Haiku stories with no Sonnet match** (10):

- Sheinbaum rejects unauthorized US military intervention, defends Mexican sovereignty (sources=8)
- SRE receives US extradition requests for Rocha Moya and nine officials but disputes lack of evidence (sources=5)
- Banxico reports 410 billion peso loss in 2025; no government remanentes due to currency gains (sources=8)
- Sheinbaum signs constitutional agreement implementing 40-hour work week (sources=2)
- Sheinbaum inaugurates Nichupté Bridge, second-longest in Latin America (sources=3)
- ... +5 more


### jp

Haiku replay: input=73,764 out=13,263 tokens, latency=104.6s

**Matched stories** (best 6 by URL overlap):

- jaccard=1.00  S: _State ceremony marks 100th anniversary of start of Showa Era; Emperor Naruhito a_  ↔  H: _Japan holds ceremony marking 100th anniversary of Showa Era, with Emperor and PM_
- jaccard=0.83  S: _Takaichi completes Vietnam summit, arrives in Australia on five-day Indo-Pacific_  ↔  H: _PM Takaichi embarks on major Indo-Pacific regional tour, deepening ties with Vie_
- jaccard=0.80  S: _Japan intervenes in currency markets for first time in two years to prop up yen_  ↔  H: _Japan intervenes in foreign exchange markets for first time in two years, suppor_
- jaccard=0.78  S: _Takaichi signals renewed push for constitutional revision on Constitution Memori_  ↔  H: _PM Takaichi renews push to revise pacifist Constitution on Memorial Day, citing _
- jaccard=0.67  S: _Japan scraps lethal weapons export ban, inaugurates security document review pan_  ↔  H: _Japan relaxes weapons export restrictions, opening path for defense equipment sa_
- jaccard=0.67  S: _Bank of Japan holds rates at 0.75% with three dissents, Ueda keeps June hike opt_  ↔  H: _Bank of Japan holds interest rates unchanged amid inflation and Middle East conf_

**Sonnet stories with no Haiku match** (2):

- Takaichi resists calls for energy-saving measures as Middle East supply anxiety grows (sources=3)
- LDP proposes civil penalties for AI companies enabling copyright infringement and deepfakes (sources=2)

**Haiku stories with no Sonnet match** (1):

- PM Takaichi pledges government support for wage increases at May Day labor event (sources=1)


### br

Haiku replay: input=126,833 out=31,991 tokens, latency=406.1s **[no-tool fallback]**

**Matched stories** (best 6 by URL overlap):

- jaccard=0.58  S: _Presidential polls show Lula and Flávio Bolsonaro in technical tie ahead of Octo_  ↔  H: _Presidential election polls show technical tie between Lula and Flávio Bolsonaro_
- jaccard=0.58  S: _Bolsonaro undergoes shoulder surgery while serving home detention; medical updat_  ↔  H: _Former president Bolsonaro undergoes shoulder surgery; health recovery progresse_
- jaccard=0.31  S: _PT holds 8th national congress, approves electoral manifesto and 2026 campaign s_  ↔  H: _PT National Congress approves campaign manifesto, targets Flávio Bolsonaro with _
- jaccard=0.24  S: _Senate rejects Lula's STF nominee Messias in historic first, triggering politica_  ↔  H: _Congress deals twin defeats to Lula: Rejects Supreme Court nominee, overrides se_
- jaccard=0.13  S: _Petrobras posts record Q1 production, raises gas and aviation fuel prices, launc_  ↔  H: _Petrobras announces record Q1 2026 production; raises prices for gas and jet fue_

**Sonnet stories with no Haiku match** (2):

- Congress overrides Lula veto on Dosimetria bill, reducing sentences for Jan. 8 convicts including Bo (sources=32)
- PT airs 'BolsoMaster' video linking Flávio to bank scandal; PL files complaint with PGR (sources=10)

**Haiku stories with no Sonnet match** (7):

- Lula absent again on May Day; government launches campaign for work schedule reform (sources=16)
- Lula announces Desenrola 2.0 debt relief program with FGTS and deep discounts (sources=6)
- Flávio Bolsonaro shores up evangelical support with Malafaia alliance (sources=8)
- Supreme Court crisis deepens: Messias rejection exposes internal divisions and institutional legitim (sources=20)
- Central Bank cuts interest rates by 25 basis points; maintains cautious stance amid global tensions (sources=8)
- ... +2 more


### fi

Haiku replay: input=93,513 out=17,694 tokens, latency=159.2s

**Haiku stories with no Sonnet match** (12):

- Zelenskyi offers Finland drone technology cooperation and defense partnership (sources=12)
- Political discourse deterioration raises concerns as election nears; opposition launches interpellat (sources=18)
- Finance Minister Purra faces controversy over electoral promises regarding cuts to low-income benefi (sources=14)
- Government budget framework negotiation concludes with economic concerns and austerity measures (sources=9)
- President Stubb participates in international diplomatic events and reflects on Russia policy (sources=18)
- ... +7 more


## How to read this

- **URL overlap >70%**: Haiku is clustering the same events as Sonnet.
- **Stories delta within ±20%**: Haiku found ~the same shape of week.
- **Avg src/story comparable**: Haiku isn't under-attributing multi-source events.
- **High Haiku orphans**: Haiku splintered events Sonnet kept together (or hallucinated stories — eyeball them).
- **High Sonnet orphans**: Haiku missed events Sonnet caught (worst case).

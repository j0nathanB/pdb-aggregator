# Haiku 4.5 vs Sonnet 4.6 — story_map eval, 20260426

Mechanical replay. Identical system + user prompts; only `model` swapped. URL overlap = % of Sonnet's URLs (representative + article) present in any Haiku story. Story-pair matching is greedy by Jaccard URL overlap, 10% floor.

## Per-country summary

| Code | Stories (S→H) | Single-src (S→H) | Off-topic (S→H) | URL overlap | Avg src/story (S→H) | Matched / S orph / H orph | $ (S→H) | Δ$ | Lat (s) |
|------|---------------|------------------|-----------------|-------------|----------------------|---------------------------|---------|-----|--------|
| **mx** | 5→17 | 0→6 | 65→12 | 42% | 28.0→7.8 (max 63→25) | 4 / 1 / 13 | $0.85→$0.24 | **−$0.61** | 339.0 |
| **jp** | 28→24 | 14→8 | 162→178 | 59% | 4.4→3.9 (max 24→20) | 18 / 10 / 6 | $0.74→$0.21 | **−$0.54** | 307.0 |
| **br** | 8→14 | 0→33 | 152→110 | 65% | 16.5→9.4 (max 54→26) | 7 / 1 / 7 | $0.87→$0.26 | **−$0.60** | 193.1 |
| **fi** | 18→8 | 7→35 | 67→87 | 73% | 8.4→16.5 (max 37→28) | 7 / 11 / 1 | $0.77→$0.21 | **−$0.56** | 205.0 |
| **total** | | | | | | | **$3.22→$0.92** | **−$2.30** | |

## Per-country drilldown

### mx

Haiku replay: input=120,165 out=23,924 tokens, latency=339.0s **[no-tool fallback]**

**Matched stories** (best 6 by URL overlap):

- jaccard=0.67  S: _Sheinbaum inaugurates Felipe Ángeles train linking Mexico City to AIFA airport_  ↔  H: _President Sheinbaum inaugurates Felipe Ángeles suburban train connecting Mexico _
- jaccard=0.41  S: _Morena leadership overhaul: Luisa Alcalde exits party presidency, Ariadna Montie_  ↔  H: _Morena party undergoes leadership restructuring ahead of 2027 gubernatorial elec_
- jaccard=0.37  S: _SEMAR contralmirante Fernando Farías Laguna arrested in Argentina on fuel-smuggl_  ↔  H: _Contraalmirante Fernando Farías Laguna detained in Argentina for leading fuel sm_
- jaccard=0.15  S: _Deaths of two US agents in Chihuahua drug lab operation ignite sovereignty crisi_  ↔  H: _Sheinbaum confronts Chihuahua governor Maru Campos over unauthorized CIA agent o_

**Sonnet stories with no Haiku match** (1):

- Banxico monetary policy debate: inflation stalls above 4% target as analysts anticipate (sources=0)

**Haiku stories with no Sonnet match** (13):

- Government confirms CIA agents killed in Chihuahua crash were not authorized to operate (sources=4)
- Teotihuacán pyramids shooting kills Canadian tourist amid security concerns (sources=2)
- Sheinbaum condemns violence after assassination attempt on Trump at White House event (sources=2)
- Mexico and Canada strengthen bilateral coordination under T-MEC renegotiation (sources=4)
- SRE appoints Nobel Peace Prize laureate Rigoberta Menchú as high counselor for women and indigenous  (sources=5)
- ... +8 more


### jp

Haiku replay: input=90,153 out=23,525 tokens, latency=307.0s **[no-tool fallback]**

**Matched stories** (best 6 by URL overlap):

- jaccard=1.00  S: _Wildfires in northern Japan's Iwate Prefecture force thousands to evacuate over _  ↔  H: _Northern Japan Wildfires Force Mass Evacuations; Over 3,000 Residents Displaced_
- jaccard=1.00  S: _Magnitude 6.1–6.2 earthquake strikes Hokkaido with no casualties reported_  ↔  H: _Magnitude 6.1 Earthquake Strikes Hokkaido; No Damage or Casualties Reported_
- jaccard=1.00  S: _Takaichi set to visit Australia in early May as two countries deepen security an_  ↔  H: _Australian Foreign Minister Wong to Visit Japan for Energy Security Talks_
- jaccard=1.00  S: _Takaichi sleep and overwork remarks spark broad domestic and international media_  ↔  H: _Prime Minister Takaichi Complains of Sleep Deprivation and Meal Management Strug_
- jaccard=1.00  S: _Japan-Philippines-US military exercises expand with JSDF in direct operational r_  ↔  H: _Japan and US-Philippines Conduct Expanded Military Exercise Balikatan 2026_
- jaccard=1.00  S: _Three JSDF tank crew members killed in live-fire accident at Oita training area_  ↔  H: _JSDF Tank Incident Kills Three Ground Self-Defense Force Members_

**Sonnet stories with no Haiku match** (10):

- JS Izumo helicopter carrier photos reveal second-phase F-35B flight deck modifications (sources=1)
- LDP pushes constitutional reform including emergency clause allowing Diet term extension (sources=3)
- Macron-Takaichi joint statement on Taiwan Strait irritates Beijing (sources=2)
- Japan-Singapore mark 60 years of diplomatic relations (sources=1)
- Nikkei crosses 60,000 for first time on tech rally following US-Iran ceasefire extension (sources=1)
- ... +5 more

**Haiku stories with no Sonnet match** (6):

- Mexico to Supply Japan with One Million Barrels of Crude Oil (sources=1)
- Takaichi Pushes Constitutional Reform Agenda to Strengthen National Defense (sources=3)
- Japan Secures Alternative Crude Oil Supply Routes Amid Middle East Conflict (sources=2)
- JS Izumo Carrier Upgrade Progresses with New Rectangular Flight Deck (sources=1)
- Takaichi Faces Fresh Pressure Over Reported Rift with Key Security Ally (sources=1)
- ... +1 more


### br

Haiku replay: input=128,131 out=27,289 tokens, latency=193.1s

**Matched stories** (best 6 by URL overlap):

- jaccard=0.71  S: _Bolsonaro awaits STF authorization for shoulder surgery while STM weighs potenti_  ↔  H: _STF maintains Bolsonaro's home detention and approves military records collectio_
- jaccard=0.58  S: _Right-wing fracture widens as Nikolas Ferreira clashes with Bolsonaro family, Fl_  ↔  H: _Internal tensions escalate within PL as Nikolas Ferreira clashes with Bolsonaro _
- jaccard=0.54  S: _STF becomes central 2026 campaign target as Zema escalates satirical attacks and_  ↔  H: _Romeu Zema escalates criticism of STF with AI satire videos, proposes privatizat_
- jaccard=0.53  S: _Lula undergoes skin cancer removal and wrist procedure, discharged same day_  ↔  H: _President Lula undergoes skin cancer removal and wrist treatment at São Paulo ho_
- jaccard=0.50  S: _Multiple polls show Flávio Bolsonaro leading or tied with Lula in key states ahe_  ↔  H: _2026 presidential race: Flávio Bolsonaro gains in key states while Lula's approv_
- jaccard=0.39  S: _Brazil-US diplomatic crisis over Ramagem arrest escalates to agent expulsions, t_  ↔  H: _Brazil-US diplomatic crisis escalates over Alexandre Ramagem's detention in Flor_

**Sonnet stories with no Haiku match** (1):

- Senate CCJ to hold confirmation hearing for Lula's STF nominee Jorge Messias on April 29 (sources=4)

**Haiku stories with no Sonnet match** (7):

- Finance Ministry blocks prediction markets and regulates critical minerals without tax breaks (sources=3)
- Fernando Haddad discusses vice-presidential candidates for São Paulo race (sources=15)
- Petrobras decides not to exercise waiver rights on Braskem stake sale to international fund (sources=5)
- São Paulo gubernatorial race: Tarcísio criticizes Lula while poll gap with Haddad narrows (sources=8)
- Bank Master failure triggers pension fund restrictions and organized crime investigation (sources=2)
- ... +2 more


### fi

Haiku replay: input=94,616 out=23,021 tokens, latency=205.0s

**Matched stories** (best 6 by URL overlap):

- jaccard=0.56  S: _EU/NATO mutual defence debate intensifies at Cyprus summit following leaked Pent_  ↔  H: _EU and NATO debate mutual defense mechanisms amid US commitment uncertainty unde_
- jaccard=0.55  S: _Government completes final budget framework review amid austerity, S&P downgrade_  ↔  H: _Government finalizes 2027–2030 budget framework with defense spending increase a_
- jaccard=0.52  S: _Opposition demands PM Orpo resign over fiscal failure; Orpo refuses at Yle inter_  ↔  H: _Opposition demands PM Orpo resign following failed economic policy targets_
- jaccard=0.28  S: _Finnish Defence Forces calls up reserve volunteers for readiness exercises follo_  ↔  H: _Finland increases defense spending to 3.2% of GDP and enhances military readines_
- jaccard=0.21  S: _OP Pohjola sets automatic security limits on all personal bank accounts to count_  ↔  H: _Banks implement new security measures and warn of rising fraud threats in Finlan_
- jaccard=0.21  S: _Parties begin nominating 2027 parliamentary election candidates across districts_  ↔  H: _Opposition parties release election platforms and name 2027 parliamentary candid_

**Sonnet stories with no Haiku match** (11):

- US halts weapons deliveries to Baltic states; Finland says its defence capability unaffected (sources=4)
- Orpo attends EU Cyprus informal summit; backs Ukraine loan package and Russia sanctions, cautious on (sources=5)
- Stubb's 'shouting' communication style with Trump draws international 'Trump whisperer' label (sources=2)
- Stubb responds to White House shooting incident, reaffirms commitment to democratic values (sources=2)
- Stubb announces official state visit to Czech Republic for May, European security focus (sources=2)
- ... +6 more

**Haiku stories with no Sonnet match** (1):

- Finance Minister Purra faces criticism over policy statements and debates economic priorities (sources=12)


## How to read this

- **URL overlap >70%**: Haiku is clustering the same events as Sonnet.
- **Stories delta within ±20%**: Haiku found ~the same shape of week.
- **Avg src/story comparable**: Haiku isn't under-attributing multi-source events.
- **High Haiku orphans**: Haiku splintered events Sonnet kept together (or hallucinated stories — eyeball them).
- **High Sonnet orphans**: Haiku missed events Sonnet caught (worst case).

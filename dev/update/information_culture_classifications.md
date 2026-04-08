# Information Culture Classification

## Manifest Schema Addition

Add to each country's government monitoring manifest (`manifests/{code}_gov.yaml`):

```yaml
# Government Source Monitor: {{COUNTRY}}

country: {{COUNTRY}}
language: {{LANGUAGE}}
information_culture: transparent | managed | controlled
```

This field is consumed by the government source agent to calibrate how it classifies and annotates government publications.

---

## Definitions

**Transparent:** Government publications can generally be taken at face value for factual content. The state publishes through institutional habit and legal obligation, not primarily for strategic communication. Significant events are covered by default — omission is usually bureaucratic, not deliberate. Intent signals are found in language choice, timing, and emphasis, not in selective publication.

**Managed:** The government selectively publishes and frames strategically but does not routinely fabricate facts. What gets published is curated — the government decides what to announce, when, and how to frame it. Significant events may be downplayed, delayed, or omitted. Publication itself is a signal. Silence from normally active sources is more likely to be deliberate. Facts in publications are generally reliable, but context and completeness are not guaranteed.

**Controlled:** Everything published is instrumentalized. The line between information and propaganda is blurred. Factual content (budget figures, procurement records) may be incomplete or misleading. The act of publication is the primary signal — what the government wants the domestic and international audience to believe. Ground truth classification should be applied cautiously. (Not present in the current 28-country set but relevant for Phase 2 expansion.)

---

## Country Assignments

| Country | Code | Information Culture | Rationale |
|---------|------|-------------------|-----------|
| Canada | ca | transparent | Strong FOI laws, institutional publication norms, independent parliamentary record |
| Mexico | mx | managed | Government controls messaging through gob.mx portal; SEDENA/SEMAR particularly opaque; civilian institutions more transparent than security institutions |
| Brazil | br | managed | Government publications are strategic; institutional transparency varies significantly by ministry; Lula government uses framing actively |
| Chile | cl | transparent | Strong institutional norms, transparent parliamentary system, independent central bank communications |
| France | fr | transparent | Institutional publication culture, Journal Officiel as legal ground truth, Élysée communications are strategic but institutional sources (parliament, courts) are reliable |
| Germany | de | transparent | Strong institutional norms, Bundesgesetzblatt as legal ground truth, federal structure creates multiple independent publication channels |
| United Kingdom | gb | transparent | Hansard, FOI, institutional publication norms. Government communications are strategic but institutional sources (parliament, courts, BOE) are independently reliable |
| Italy | it | transparent | EU-standard institutional publication norms, Gazzetta Ufficiale as legal ground truth, parliamentary record reliable |
| Spain | es | transparent | Similar to Italy — institutional norms, BOE as legal ground truth, Cortes records reliable |
| Norway | no | transparent | Among the most transparent government communications globally |
| Sweden | se | transparent | Strong freedom of information tradition, institutional publication norms |
| Ukraine | ua | managed | Wartime information environment. Government publications are factually grounded but strategically framed for domestic morale and international audience. Military information is actively managed. Zelenskyy's office is a strategic communications operation. Parliamentary and judicial institutions are more transparent than executive |
| Poland | pl | transparent | EU-standard institutional norms, strong parliamentary record. Government communications under Tusk are more open than under PiS but still strategically framed |
| Finland | fi | transparent | Nordic transparency norms |
| Estonia | ee | transparent | Strong digital governance, institutional transparency norms |
| Lithuania | lt | transparent | EU-standard institutional norms, strong on defense transparency given threat environment |
| Latvia | lv | transparent | EU-standard institutional norms |
| Czech Republic | cz | transparent | EU-standard institutional norms, strong parliamentary record |
| Romania | ro | transparent | EU-standard institutional norms, though implementation can be uneven; Monitorul Oficial as legal ground truth |
| Turkey | tr | managed | Government actively manages information environment. Anadolu Agency functions as state messaging channel. Presidential communications office controls narrative. Institutional sources (TBMM, central bank, official gazette) are more reliable than executive communications. Defense sector is particularly opaque |
| Saudi Arabia | sa | managed | Government publications are strategic state communications. Official sources (SPA, royal court) function as policy announcement channels, not transparent institutional records. Ground truth exists in published budgets and contracts but is selectively disclosed. No independent parliamentary record |
| UAE | ae | managed | Similar to Saudi Arabia. WAM (state news agency) is the primary government communication channel. Institutional transparency is selective. Government publications are high-quality but curated |
| India | in | managed | Government communications are strategic, particularly from PMO and MEA. Parliamentary record (Lok Sabha/Rajya Sabha) is independently reliable. RBI communications are institutionally grounded. Defense sector publications are managed. PIB (Press Information Bureau) is the government's messaging channel — not independent |
| Taiwan | tw | transparent | Democratic institutional norms, strong parliamentary record, transparent defense and foreign affairs communications. Cross-strait sensitivity means some security-related communications are strategically managed but civilian institutions are transparent |
| Japan | jp | transparent | Strong institutional publication norms, reliable parliamentary record. Government communications are formal and carefully worded but factually reliable. MOF, BOJ, and MOFA publications are institutionally grounded |
| South Korea | kr | transparent | Democratic institutional norms, strong parliamentary record. Government communications can be politically charged (especially around North Korea) but institutional sources are reliable. Political instability may affect executive communications reliability |
| Australia | au | transparent | Strong FOI and institutional publication norms, Hansard, independent parliamentary record |
| Indonesia | id | managed | Government publications are strategic. Institutional transparency is improving but uneven. Parliamentary record is publicly available but less developed than in consolidated democracies. Defense and intelligence sectors are opaque. Presidential and foreign ministry communications are managed |

---

## Notes

- The assignment is at the **country level**, not the institution level. Within a `managed` country, some institutions may be more transparent than others (e.g., Mexico's Banxico is more transparent than SEDENA). The per-source interpretive context in the Source Intelligence Map captures these within-country variations. The information culture tag is the country-level default.
- **Transparent does not mean unbiased.** A transparent government publication still reflects government priorities and framing. The tag means the factual content is reliable and publication patterns are institutional rather than strategic.
- **Managed does not mean unreliable.** It means the pipeline should note *what* the government chose to publish and *when*, not just what the publication says. The act of publication is itself a data point.
- These assignments should be reviewed during the quarterly dossier refresh cycle and updated if political transitions change the information environment (e.g., a democratic backslide moving a country from transparent to managed).

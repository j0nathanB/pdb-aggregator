# Claude Code — Steps 1-5 Revision (CountryConfig + Project Structure)

## What Changed

The collection architecture was redesigned after the original steps 1-5 handoff. This affects only **Step 1 (project structure)** and **Step 2 (CountryConfig)**. Steps 3-5 (ledger schemas, ledger operations, initialization) are unchanged.

---

## Step 1 Revision: Additional Directories

Add these directories to the project structure:

```
middle-powers-monitor/
├── goggles/                # Per-country Brave Search Goggle files (.goggle)
├── government/             # Per-country government domain configs (.yaml)
├── extraction/
│   └── routing.yaml        # Global extraction routing table
├── context/                # Per-country source interpretive context (.md)
├── frameworks/             # Regional analytical framework documents
│   ├── americas.md
│   ├── western_europe.md
│   ├── frontline_eastern_europe.md
│   ├── middle_east_turkey_south_asia.md
│   └── asia_pacific.md
├── ... (everything else from original handoff unchanged)
```

These sit alongside the existing `config/`, `dossiers/`, `ledgers/`, `output/`, `prompts/`, `src/`, and `tests/` directories.

---

## Step 2 Revision: CountryConfig Schema

Replace the CountryConfig Pydantic model and Mexico YAML with the schema below. The old `sources` block (domestic/government/wire lists) is replaced by references to external collection configuration files.

### Pydantic Model

```python
from pydantic import BaseModel
from typing import Optional


class Actor(BaseModel):
    name: str
    role: str
    primary: bool = False
    search_terms: list[str]


class BraveParams(BaseModel):
    country: str          # ISO 3166-1 alpha-2, uppercase (e.g., "MX")
    search_lang: str      # ISO 639-1 (e.g., "es")
    freshness: str = "pw" # past week


class QueryVocabulary(BaseModel):
    diplomatic_alignment: list[str] = []
    security_defense: list[str] = []
    economic_tech: list[str] = []
    institutional: list[str] = []
    domestic_constraints: list[str] = []


class NewsDiscovery(BaseModel):
    goggle_file: str              # Path to .goggle file
    extraction_config: str = "extraction/routing.yaml"  # Global routing table
    brave_params: BraveParams
    query_vocabulary: QueryVocabulary


class GovernmentDiscovery(BaseModel):
    config_file: str              # Path to government domain config YAML


class BlindSpot(BaseModel):
    domain: str                   # Analytical domain that's dark
    reason: str                   # Why it's dark
    where_signal_lives: str       # Where the info actually exists


class Languages(BaseModel):
    primary: str                  # ISO 639-1 code
    additional: list[str] = []    # For multi-language countries
    metadata: str = "en"          # Always English for pipeline metadata


class SearchBudget(BaseModel):
    triage_queries_max: int = 3
    deep_dive_queries_max: int = 20


class CountryConfig(BaseModel):
    country: str                  # Full country name
    code: str                     # ISO 3166-1 alpha-2, lowercase
    tier: str                     # shield | next_test | pivot | periphery | crucible
    region: str                   # americas | western_europe | frontline_eastern_europe |
                                  # middle_east_turkey_south_asia | asia_pacific
    actors: list[Actor]
    languages: Languages
    news_discovery: NewsDiscovery
    government_discovery: GovernmentDiscovery
    interpretive_context_file: str  # Path to source interpretive context markdown
    blind_spots: list[BlindSpot] = []
    search: SearchBudget = SearchBudget()
```

### Mexico YAML (`config/countries/mx.yaml`)

```yaml
country: Mexico
code: mx
tier: periphery
region: americas

actors:
  - name: Claudia Sheinbaum
    role: President
    primary: true
    search_terms: ["Sheinbaum", "Claudia Sheinbaum"]
  - name: Juan Ramón de la Fuente
    role: Foreign Minister (SRE)
    primary: false
    search_terms: ["de la Fuente", "Juan Ramón de la Fuente"]
  - name: SEDENA
    role: National Defense Secretariat
    primary: false
    search_terms: ["SEDENA", "Secretaría de la Defensa Nacional"]
  - name: SEMAR
    role: Navy Secretariat
    primary: false
    search_terms: ["SEMAR", "Secretaría de Marina"]
  - name: SRE
    role: Foreign Affairs Secretariat
    primary: false
    search_terms: ["SRE", "Secretaría de Relaciones Exteriores"]
  - name: Banxico
    role: Central Bank
    primary: false
    search_terms: ["Banxico", "Banco de México"]
  - name: Morena
    role: Governing party
    primary: false
    search_terms: ["Morena"]

languages:
  primary: es
  additional: []
  metadata: en

news_discovery:
  goggle_file: goggles/mx.goggle
  extraction_config: extraction/routing.yaml
  brave_params:
    country: MX
    search_lang: es
    freshness: pw
  query_vocabulary:
    diplomatic_alignment:
      - "relaciones bilaterales"
      - "acuerdo diplomático"
      - "cancillería"
      - "cumbre bilateral"
      - "embajador"
    security_defense:
      - "SEDENA"
      - "adquisición militar"
      - "cooperación en seguridad"
      - "Guardia Nacional"
      - "despliegue militar"
    economic_tech:
      - "inversión extranjera"
      - "tratado comercial"
      - "Banxico"
      - "nearshoring"
      - "minerales críticos"
    institutional:
      - "OEA"
      - "Naciones Unidas"
      - "G20"
      - "ratificación tratado"
    domestic_constraints:
      - "reforma constitucional"
      - "coalición legislativa"
      - "Morena"
      - "oposición"
      - "Diputados"

government_discovery:
  config_file: government/mx.yaml

interpretive_context_file: context/mx_sources.md

blind_spots:
  - domain: Defense procurement
    reason: No dedicated defense press; SEDENA/SEMAR communicate through controlled bulletins only
    where_signal_lives: SEDENA/SEMAR official bulletins, leaked documents in Proceso or Animal Político
  - domain: Real-time security
    reason: Telegram/WhatsApp channels precede news coverage but are not ingestible
    where_signal_lives: Local journalists who monitor these channels; downstream reporting lag of 12-48 hours
  - domain: Legislative proceedings
    reason: Committee testimony not covered by media
    where_signal_lives: gob.mx portals, Senate/Chamber of Deputies websites

search:
  triage_queries_max: 3
  deep_dive_queries_max: 20
```

### Government Domain Config (`government/mx.yaml`)

```yaml
country: Mexico
code: mx
information_culture: managed

domains:
  - domain: gob.mx
    institutions: [Presidency, SEDENA, SEMAR, SRE, SE]
    priority: P1
  - domain: sre.gob.mx
    institutions: [Foreign Ministry]
    priority: P1
  - domain: banxico.org.mx
    institutions: [Central Bank]
    priority: P2
  - domain: senado.gob.mx
    institutions: [Senate]
    priority: P2
  - domain: diputados.gob.mx
    institutions: [Chamber of Deputies]
    priority: P2
  - domain: dof.gob.mx
    institutions: [Official Gazette]
    priority: P2

query_terms:
  - "comunicado"
  - "acuerdo bilateral"
  - "decreto"
  - "adquisición"
  - "presupuesto"
```

### Pydantic Model for Government Domain Config

```python
class GovernmentDomain(BaseModel):
    domain: str
    institutions: list[str]
    priority: str  # P1 | P2


class GovernmentDomainConfig(BaseModel):
    country: str
    code: str
    information_culture: str  # transparent | managed | controlled
    domains: list[GovernmentDomain]
    query_terms: list[str]
```

---

## What's Unchanged

- **Step 3 (Country Ledger Schema):** No changes. The ledger schema was designed around the five signal categories and is independent of the collection architecture.
- **Step 4 (Global Ledger Schema):** No changes.
- **Step 5 (Ledger Operations and Initialization):** No changes. The `bootstrap_country_ledger()` function still takes a config + claim_ids and produces an initialized ledger. The config format changed but the initialization logic doesn't depend on collection-specific fields.

---

## Tests to Add/Update

- Update CountryConfig schema validation tests for the new structure
- Add GovernmentDomainConfig schema validation tests
- Add test for loading a CountryConfig that correctly resolves file references (goggle_file, config_file, interpretive_context_file)
- Existing ledger tests are unaffected

"""
Country configuration and pipeline constants for the Middle Powers Monitor.

CountryConfig is loaded from YAML files in assets/country_configs/countries/{code}.yaml.
Government domain configs are loaded from assets/government/{code}.yaml.
"""

import os
from enum import Enum
from pathlib import Path
from typing import Optional

import yaml
from pydantic import BaseModel, Field, field_validator


# =============================================================================
# Constants
# =============================================================================

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Paths (relative to project root)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
ASSETS_DIR = PROJECT_ROOT / "assets"
CONFIGS_DIR = ASSETS_DIR / "country_configs" / "countries"
SETTINGS_PATH = ASSETS_DIR / "country_configs" / "settings.yaml"
GOVERNMENT_DIR = ASSETS_DIR / "government"
GOGGLES_DIR = ASSETS_DIR / "country_goggles"
CONTEXT_DIR = ASSETS_DIR / "context"
FRAMEWORKS_DIR = ASSETS_DIR / "frameworks"
EXTRACTION_ROUTING_PATH = ASSETS_DIR / "country_configs" / "extraction_routing.yaml"
PROMPTS_DIR = ASSETS_DIR / "prompts"

# Prompt cache — loaded once per process
_prompt_cache: dict[str, str] = {}


def load_prompt(name: str, **kwargs: str) -> str:
    """Load a prompt template from assets/prompts/{name}.md.

    Template variables like {{COUNTRY}} are substituted from kwargs.
    Results are cached (before substitution) for repeated loads.
    """
    if name not in _prompt_cache:
        path = PROMPTS_DIR / f"{name}.md"
        if not path.exists():
            raise FileNotFoundError(f"Prompt not found: {path}")
        _prompt_cache[name] = path.read_text()

    text = _prompt_cache[name]
    for key, value in kwargs.items():
        text = text.replace(f"{{{{{key}}}}}", value)
    return text


def load_settings() -> dict:
    """Load global settings from settings.yaml."""
    if SETTINGS_PATH.exists():
        with open(SETTINGS_PATH) as f:
            return yaml.safe_load(f) or {}
    return {}

_SETTINGS = load_settings()

MODEL = _SETTINGS.get("model", "claude-sonnet-4-20250514")
THINKING_BUDGET_TOKENS = _SETTINGS.get("thinking_budget_tokens", 16000)

LEDGERS_DIR = PROJECT_ROOT / "ledgers"
COUNTRY_LEDGERS_DIR = LEDGERS_DIR / "countries"
GLOBAL_LEDGER_PATH = LEDGERS_DIR / "global.json"
LEDGER_ARCHIVE_DIR = LEDGERS_DIR / "archive"
DOSSIERS_DIR = ASSETS_DIR / "country_dossiers"

# Ledger retention
WEEKLY_ENTRY_RETENTION = 8
STALENESS_THRESHOLD_WEEKS = 4

# Confidence and source tier bounds
CONFIDENCE_MIN = 1
CONFIDENCE_MAX = 5
SOURCE_TIER_MIN = 1
SOURCE_TIER_MAX = 4


# =============================================================================
# Enums
# =============================================================================

class Tier(str, Enum):
    SHIELD = "shield"
    NEXT_TEST = "next_test"
    PIVOT = "pivot"
    PERIPHERY = "periphery"
    CRUCIBLE = "crucible"


class Region(str, Enum):
    AMERICAS = "americas"
    WESTERN_EUROPE = "western_europe"
    FRONTLINE_EASTERN_EUROPE = "frontline_eastern_europe"
    MIDDLE_EAST_TURKEY_SOUTH_ASIA = "middle_east_turkey_south_asia"
    ASIA_PACIFIC = "asia_pacific"


class SignalCategory(str, Enum):
    ALIGNMENT_DIPLOMATIC = "alignment_diplomatic"
    SECURITY_DEFENSE = "security_defense"
    ECONOMIC_TECH = "economic_tech"
    INSTITUTIONAL = "institutional"
    DOMESTIC_REGIME = "domestic_regime"


class CategoryStatus(str, Enum):
    ACTIVE = "active"
    ROUTINE = "routine"
    QUIET = "quiet"
    ESCALATING = "escalating"


class Depth(str, Enum):
    DEEP_DIVE = "deep_dive"
    MAINTENANCE = "maintenance"


class ActivityRating(str, Enum):
    HIGH = "high"
    MODERATE = "moderate"
    LOW = "low"
    QUIET = "quiet"


class Movement(str, Enum):
    SIGNIFICANT = "significant"
    MINOR = "minor"
    NONE = "none"


class DynamicStatus(str, Enum):
    EMERGING = "emerging"
    DEVELOPING = "developing"
    ESTABLISHED = "established"
    MONITORING = "monitoring"
    WEAKENING = "weakening"
    RESOLVED = "resolved"


class LinkageType(str, Enum):
    PARALLEL_BEHAVIOR = "parallel_behavior"
    INTERACTION_EFFECT = "interaction_effect"
    INSTITUTIONAL = "institutional"
    ABSENCE = "absence"


class ClaimStatus(str, Enum):
    CONFIRMED = "confirmed"
    UNDER_PRESSURE = "under_pressure"
    WEAKENED = "weakened"
    FALSIFIED = "falsified"


# =============================================================================
# CountryConfig models
# =============================================================================

class Actor(BaseModel):
    name: str
    role: str
    primary: bool = False
    search_terms: list[str] = Field(default_factory=list)


class BraveParams(BaseModel):
    country: str  # ISO 3166-1 alpha-2, uppercase (e.g., "MX")
    search_lang: str  # ISO 639-1 (e.g., "es")
    freshness: str = "pw"  # past week


class QueryVocabulary(BaseModel):
    diplomatic_alignment: list[str] = Field(default_factory=list)
    security_defense: list[str] = Field(default_factory=list)
    economic_tech: list[str] = Field(default_factory=list)
    institutional: list[str] = Field(default_factory=list)
    domestic_constraints: list[str] = Field(default_factory=list)


class NewsDiscovery(BaseModel):
    goggle_file: str  # Path to .goggle file
    extraction_config: str = "extraction/routing.yaml"  # Global routing table
    brave_params: BraveParams
    query_vocabulary: QueryVocabulary = Field(default_factory=QueryVocabulary)


class GovernmentDiscovery(BaseModel):
    config_file: str  # Path to government domain config YAML


class Languages(BaseModel):
    primary: str  # ISO 639-1 code
    additional: list[str] = Field(default_factory=list)
    metadata: str = "en"  # Always English for pipeline metadata


class BlindSpot(BaseModel):
    domain: str  # Analytical domain that's dark
    reason: str
    where_signal_lives: str


class SearchBudget(BaseModel):
    triage_queries_max: int = 3
    deep_dive_queries_max: int = 20


class CountryConfig(BaseModel):
    country: str
    code: str = Field(pattern=r"^[a-z]{2}$")
    tier: Tier
    region: Region
    actors: list[Actor]
    languages: Languages = Field(default_factory=lambda: Languages(primary="en"))
    news_discovery: NewsDiscovery
    government_discovery: GovernmentDiscovery
    interpretive_context_file: str = ""  # Path to source interpretive context markdown
    blind_spots: list[BlindSpot] = Field(default_factory=list)
    search: SearchBudget = Field(default_factory=SearchBudget)

    @field_validator("actors")
    @classmethod
    def must_have_primary_actor(cls, v: list[Actor]) -> list[Actor]:
        if not any(a.primary for a in v):
            raise ValueError("At least one actor must be marked as primary")
        return v

    @property
    def primary_actors(self) -> list[Actor]:
        return [a for a in self.actors if a.primary]

    # Map country codes to common abbreviations used in dossier filenames
    _DOSSIER_ALIASES: dict[str, str] = {"ae": "uae", "gb": "united_kingdom"}

    @property
    def dossier_path(self) -> Path:
        patterns = [
            f"*_{self.code}_dossier_*.md",
            f"{self._dossier_name_stem}*.md",
            f"{self.code}_dossier_*.md",
        ]
        # Check aliases (e.g. ae → uae)
        alias = self._DOSSIER_ALIASES.get(self.code)
        if alias:
            patterns.append(f"{alias}_dossier_*.md")

        matches = []
        for pat in patterns:
            matches.extend(DOSSIERS_DIR.glob(pat))
        if matches:
            return sorted(matches, key=lambda p: p.stat().st_mtime, reverse=True)[0]
        raise FileNotFoundError(f"No dossier found for {self.code}")

    @property
    def _dossier_name_stem(self) -> str:
        return self.country.lower().replace(" ", "_")

    @property
    def ledger_path(self) -> Path:
        return COUNTRY_LEDGERS_DIR / f"{self.code}.json"

    @property
    def goggle_path(self) -> Path:
        return PROJECT_ROOT / self.news_discovery.goggle_file

    @property
    def government_config_path(self) -> Path:
        return PROJECT_ROOT / self.government_discovery.config_file

    @property
    def context_path(self) -> Path | None:
        if self.interpretive_context_file:
            return PROJECT_ROOT / self.interpretive_context_file
        return None


# =============================================================================
# Government domain config
# =============================================================================

class GovernmentDomain(BaseModel):
    domain: str
    institutions: list[str]
    priority: str = "P2"  # P1 | P2


class GovernmentDomainConfig(BaseModel):
    country: str
    code: str
    information_culture: str  # transparent | managed | controlled
    domains: list[GovernmentDomain]
    query_terms: list[str] = Field(default_factory=list)


def load_government_config(code: str) -> GovernmentDomainConfig:
    """Load a government domain config from its YAML file."""
    path = GOVERNMENT_DIR / f"{code}.yaml"
    if not path.exists():
        raise FileNotFoundError(f"No government config for country code '{code}': {path}")
    with open(path) as f:
        data = yaml.safe_load(f)
    return GovernmentDomainConfig(**data)


# =============================================================================
# Config loading
# =============================================================================

def load_country_config(code: str) -> CountryConfig:
    """Load a CountryConfig from its YAML file."""
    path = CONFIGS_DIR / f"{code}.yaml"
    if not path.exists():
        raise FileNotFoundError(f"No config file for country code '{code}': {path}")
    with open(path) as f:
        data = yaml.safe_load(f)
    return CountryConfig(**data)


def load_all_country_configs() -> dict[str, CountryConfig]:
    """Load all country configs, keyed by country code."""
    configs = {}
    for path in sorted(CONFIGS_DIR.glob("*.yaml")):
        code = path.stem
        configs[code] = load_country_config(code)
    return configs

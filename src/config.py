"""
Configuration and data models for the PDB Aggregator.

This module defines:
- Pydantic models for all data structures
- Paragon taxonomy (event types, leader roles, impact levels)
- Leader configurations with domestic sources
- Priority score calculation
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
import os


# =============================================================================
# CONSTANTS
# =============================================================================

RELEVANCE_THRESHOLD = 0.4
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
DEFAULT_MODEL = "claude-opus-4-6"
THINKING_BUDGET_TOKENS = 16000  # Extended thinking budget for all agents

# Model tiering: reserve Opus for high-value editorial prose, use Sonnet elsewhere
MODEL_EDITORIAL = DEFAULT_MODEL  # BTL, exec summary (few calls, quality matters)
MODEL_ANALYTICAL = "claude-sonnet-4-5-20250929"  # Dedup, story arcs, validation
MODEL_SYNTHESIS = MODEL_ANALYTICAL  # Event synthesis (bulk calls, structured extraction)
THINKING_EDITORIAL = THINKING_BUDGET_TOKENS  # 16000
THINKING_ANALYTICAL = 4000
THINKING_SYNTHESIS = 0  # Disabled — synthesis is structured extraction, not deep reasoning

# News fetching settings
MAX_ARTICLES_PER_LEADER = 5
MAX_ARTICLE_CONTENT_LENGTH = 0  # 0 = full text, positive = truncate
API_CALL_DELAY_SECONDS = 2.0

# Batch API settings
BATCH_POLL_INTERVAL_SECONDS = 30.0
BATCH_MAX_WAIT_SECONDS = 3600.0
BATCH_ENABLED = True
CACHE_TTL = "1h"

# Singleton detection thresholds
SINGLETON_THRESHOLD = 0.7

# Event clustering settings
MAX_SNIPPETS_PER_SOURCE = 20
MAX_EVENTS_FOR_BRIEF = 5
MAX_ARTICLES_PER_EVENT = 3
MIN_EVENT_SCORE_RATIO = 0.5  # Include events with score >= top * ratio

# Embedding model: unified multilingual for all leaders
# Using a single model ensures all vectors exist in the same latent space,
# enabling cross-lingual semantic comparison (e.g., German "Panzer" ↔ English "tanks").
# This replaces the previous split approach (bge-small-en + paraphrase-multilingual)
# which created incomparable vector spaces and blocked cross-leader semantic matching.
#
# E5-multilingual-small: 118M params, strong cross-lingual retrieval, same latent space
# for 100+ languages. Query prefix "query: " recommended for best performance.
EMBEDDING_MODEL = "intfloat/multilingual-e5-small"
MULTILINGUAL_EMBEDDING_MODEL = EMBEDDING_MODEL  # Unified - no separate model needed

# Cross-encoder for re-ranking candidate story matches
# Bi-encoder (cosine similarity) is fast but shallow - it embeds texts independently
# and can miss semantic inversions ("Leader denies charges" vs "Leader indicted").
# Cross-encoder reads both texts together, catching subtle differences.
# Used as validation gate after bi-encoder candidate selection.
CROSS_ENCODER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"
CROSS_ENCODER_THRESHOLD = 0.7  # Minimum score to confirm merge (0-1 scale)

# Arize AX Tracing
ARIZE_SPACE_ID = os.getenv("ARIZE_SPACE_ID")
ARIZE_API_KEY = os.getenv("ARIZE_API_KEY")
ARIZE_PROJECT_NAME = os.getenv("ARIZE_PROJECT_NAME", "pdb")


# =============================================================================
# PARAGON TAXONOMY
# =============================================================================

class EventType(str, Enum):
    """Classification of event types with associated weights."""
    POLICY_ANNOUNCEMENT = "policy_announcement"
    INTERNATIONAL_VISIT = "international_visit"
    MAJOR_SPEECH = "major_speech"
    CABINET_CHANGE = "cabinet_change"
    LEGAL_DEVELOPMENT = "legal_development"
    BILATERAL_AGREEMENT = "bilateral_agreement"
    CRISIS_RESPONSE = "crisis_response"
    ECONOMIC_ACTION = "economic_action"
    OTHER = "other"


EVENT_TYPE_WEIGHTS: dict[EventType, float] = {
    EventType.POLICY_ANNOUNCEMENT: 0.35,
    EventType.INTERNATIONAL_VISIT: 0.30,
    EventType.MAJOR_SPEECH: 0.30,
    EventType.CABINET_CHANGE: 0.25,
    EventType.LEGAL_DEVELOPMENT: 0.25,
    EventType.BILATERAL_AGREEMENT: 0.30,
    EventType.CRISIS_RESPONSE: 0.35,
    EventType.ECONOMIC_ACTION: 0.25,
    EventType.OTHER: 0.10,
}


class LeaderRole(str, Enum):
    """The leader's role in the reported event."""
    INITIATOR = "initiator"      # Driving the action
    PARTICIPANT = "participant"  # Involved but not driving
    SUBJECT = "subject"          # Being reported on passively


LEADER_ROLE_WEIGHTS: dict[LeaderRole, float] = {
    LeaderRole.INITIATOR: 0.40,
    LeaderRole.PARTICIPANT: 0.25,
    LeaderRole.SUBJECT: 0.10,
}

# Context-dependent role modifiers: being a SUBJECT in high-stakes events is newsworthy
# Example: "Leader investigated for corruption" (SUBJECT + LEGAL_DEVELOPMENT) should
# rank higher than "Leader cuts ribbon" (INITIATOR + OTHER)
#
# These event types elevate the SUBJECT role because being targeted/affected is the news
SUBJECT_ELEVATING_EVENTS: set["EventType"] = set()  # Populated after EventType is defined

# Modifier applied to SUBJECT role weight when event type is in SUBJECT_ELEVATING_EVENTS
# 3.0x brings SUBJECT (0.10 * 3.0 = 0.30) close to INITIATOR (0.40)
SUBJECT_ELEVATION_MODIFIER: float = 3.0


class ImpactLevel(str, Enum):
    """Geographic scope of impact."""
    INTERNATIONAL = "international"  # Multiple countries
    NATIONAL = "national"            # Country-wide
    REGIONAL = "regional"            # Sub-national region
    LOCAL = "local"                  # Limited local impact


IMPACT_LEVEL_WEIGHTS: dict[ImpactLevel, float] = {
    ImpactLevel.INTERNATIONAL: 0.25,
    ImpactLevel.NATIONAL: 0.20,
    ImpactLevel.REGIONAL: 0.10,
    ImpactLevel.LOCAL: 0.05,
}


# Maximum possible weight (for normalization)
MAX_WEIGHT = (
    max(EVENT_TYPE_WEIGHTS.values()) +
    max(LEADER_ROLE_WEIGHTS.values()) +
    max(IMPACT_LEVEL_WEIGHTS.values())
)  # 0.35 + 0.40 + 0.25 = 1.0


# High-weight event types for singleton detection
HIGH_WEIGHT_EVENT_TYPES: set[EventType] = {
    EventType.POLICY_ANNOUNCEMENT,
    EventType.CRISIS_RESPONSE,
    EventType.INTERNATIONAL_VISIT,
    EventType.MAJOR_SPEECH,
    EventType.BILATERAL_AGREEMENT,
}

# Now that EventType is defined, populate SUBJECT_ELEVATING_EVENTS
# These are event types where being the SUBJECT is newsworthy:
# - LEGAL_DEVELOPMENT: investigations, indictments, court rulings against leader
# - CRISIS_RESPONSE: leader being affected by crisis, not just responding
# - CABINET_CHANGE: leader being replaced/ousted (not doing the replacing)
SUBJECT_ELEVATING_EVENTS.update({
    EventType.LEGAL_DEVELOPMENT,
    EventType.CRISIS_RESPONSE,
    EventType.CABINET_CHANGE,
})


# =============================================================================
# SOURCE CONFIGURATION
# =============================================================================

@dataclass
class SourceConfig:
    """Configuration for a news source."""
    name: str
    url: str
    language: str = "en"
    source_type: str = "domestic"  # "wire", "domestic", "state_media"
    rss_url: Optional[str] = None
    requires_translation: bool = False
    
    def __post_init__(self):
        self.requires_translation = self.language != "en"


# Wire services (used for all leaders)
WIRE_SERVICES: list[SourceConfig] = [
    SourceConfig(
        name="Reuters",
        url="https://www.reuters.com",
        rss_url="https://www.reuters.com/rssFeed/worldNews",
        source_type="wire",
    ),
    SourceConfig(
        name="AP News",
        url="https://apnews.com",
        rss_url="https://apnews.com/feed",
        source_type="wire",
    ),
]


# =============================================================================
# LEADER CONFIGURATION
# =============================================================================

@dataclass
class LeaderConfig:
    """Configuration for a tracked world leader."""
    name: str
    title: str
    country: str
    region: str  # "europe", "americas", "asia_pacific", "baltics"
    domestic_sources: list[SourceConfig] = field(default_factory=list)
    search_terms: list[str] = field(default_factory=list)

    def __post_init__(self):
        # Auto-generate search terms if not provided
        if not self.search_terms:
            self.search_terms = [
                self.name,
                f"{self.title} {self.country}",
                f"{self.name} {self.country}",
            ]


def leader_needs_multilingual(leader: LeaderConfig) -> bool:
    """Check if any domestic source for this leader is non-English."""
    return any(s.language != "en" for s in leader.domestic_sources)


# Leader metadata not in CSV: title, region, primary language
LEADER_METADATA: dict[str, dict] = {
    # Americas
    "Mark Carney": {"title": "Prime Minister", "region": "americas", "language": "en"},
    "Claudia Sheinbaum": {"title": "President", "region": "americas", "language": "es"},
    "Lula da Silva": {"title": "President", "region": "americas", "language": "pt"},
    "Yamandú Orsi": {"title": "President", "region": "americas", "language": "es"},
    # Western Europe
    "Emmanuel Macron": {"title": "President", "region": "europe", "language": "fr"},
    "Keir Starmer": {"title": "Prime Minister", "region": "europe", "language": "en"},
    "Friedrich Merz": {"title": "Chancellor", "region": "europe", "language": "de"},
    "Giorgia Meloni": {"title": "Prime Minister", "region": "europe", "language": "it"},
    # Eastern Europe
    "Volodymyr Zelenskyy": {"title": "President", "region": "europe", "language": "uk"},
    "Alexander Stubb": {"title": "President", "region": "europe", "language": "fi"},
    "Donald Tusk": {"title": "Prime Minister", "region": "europe", "language": "pl"},
    # Baltics
    "Gitanas Nausėda": {"title": "President", "region": "baltics", "language": "lt"},
    "Evika Siliņa": {"title": "Prime Minister", "region": "baltics", "language": "lv"},
    "Kristen Michal": {"title": "Prime Minister", "region": "baltics", "language": "et"},
    "Maia Sandu": {"title": "President", "region": "baltics", "language": "ro"},
}

# Map country to primary language (for sources without explicit language)
COUNTRY_LANGUAGES: dict[str, str] = {
    "Canada": "en",
    "Mexico": "es",
    "Brazil": "pt",
    "Uruguay": "es",
    "France": "fr",
    "United Kingdom": "en",
    "Germany": "de",
    "Italy": "it",
    "Ukraine": "uk",
    "Finland": "fi",
    "Poland": "pl",
    "Lithuania": "lt",
    "Latvia": "lv",
    "Estonia": "et",
    "Moldova": "ro",
}

COUNTRY_EMOJI: dict[str, str] = {
    "Canada": "🇨🇦",
    "Mexico": "🇲🇽",
    "Brazil": "🇧🇷",
    "Uruguay": "🇺🇾",
    "France": "🇫🇷",
    "United Kingdom": "🇬🇧",
    "Germany": "🇩🇪",
    "Italy": "🇮🇹",
    "Ukraine": "🇺🇦",
    "Finland": "🇫🇮",
    "Poland": "🇵🇱",
    "Lithuania": "🇱🇹",
    "Latvia": "🇱🇻",
    "Estonia": "🇪🇪",
    "Moldova": "🇲🇩",
}


def _load_leaders_from_csv() -> list[LeaderConfig]:
    """Load leader configurations from leaders_sources.csv."""
    import csv
    from pathlib import Path

    csv_path = Path(__file__).parent.parent / "leaders_sources.csv"

    if not csv_path.exists():
        raise FileNotFoundError(f"Leaders CSV not found: {csv_path}")

    # Group sources by leader
    leader_sources: dict[str, list[dict]] = {}
    leader_countries: dict[str, str] = {}

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            leader_name = row["leader"]
            country = row["country"]

            if leader_name not in leader_sources:
                leader_sources[leader_name] = []
                leader_countries[leader_name] = country

            leader_sources[leader_name].append({
                "name": row["source_name"],
                "domain": row["domain"],
                "source_type": row["source_type"],
                "notes": row.get("notes", ""),
            })

    # Build LeaderConfig objects
    configs = []
    for leader_name, sources in leader_sources.items():
        if leader_name not in LEADER_METADATA:
            continue  # Skip leaders without metadata

        meta = LEADER_METADATA[leader_name]
        country = leader_countries[leader_name]
        language = COUNTRY_LANGUAGES.get(country, "en")

        # Build SourceConfig list
        domestic_sources = []
        for src in sources:
            # Skip quarantined sources (e.g., paywalled sites)
            if "quarantine" in src.get("notes", "").lower():
                continue

            # Determine source type
            src_type = src["source_type"]
            if src_type == "official":
                src_type = "official"
            else:
                src_type = "domestic"

            # Build URL from domain
            domain = src["domain"]
            if not domain.startswith("http"):
                url = f"https://{domain}"
            else:
                url = domain

            domestic_sources.append(SourceConfig(
                name=src["name"],
                url=url,
                language=language,
                source_type=src_type,
            ))

        configs.append(LeaderConfig(
            name=leader_name,
            title=meta["title"],
            country=country,
            region=meta["region"],
            domestic_sources=domestic_sources,
        ))

    return configs


def get_leader_configs() -> list[LeaderConfig]:
    """
    Return configurations for all tracked leaders.

    Loads from leaders_sources.csv with metadata from LEADER_METADATA.
    """
    return _load_leaders_from_csv()


def get_leaders_by_region() -> dict[str, list[LeaderConfig]]:
    """Group leaders by region for regional context generation."""
    leaders = get_leader_configs()
    by_region: dict[str, list[LeaderConfig]] = {}
    
    for leader in leaders:
        if leader.region not in by_region:
            by_region[leader.region] = []
        by_region[leader.region].append(leader)
    
    return by_region


# =============================================================================
# ARTICLE AND CLASSIFICATION MODELS
# =============================================================================

@dataclass
class ArticleClassification:
    """Classification of an article using Paragon taxonomy."""
    event_type: EventType
    leader_role: LeaderRole
    impact_level: ImpactLevel
    priority_score: float
    reasoning: str = ""
    
    @classmethod
    def calculate_priority(
        cls,
        event_type: EventType,
        leader_role: LeaderRole,
        impact_level: ImpactLevel,
    ) -> float:
        """
        Calculate normalized priority score from taxonomy values.

        Applies context-dependent modifiers:
        - SUBJECT role is elevated in high-stakes event types (LEGAL_DEVELOPMENT,
          CRISIS_RESPONSE, CABINET_CHANGE) because being investigated/targeted IS the news
        - Example: "Leader indicted for corruption" (SUBJECT + LEGAL_DEVELOPMENT)
          now ranks appropriately vs "Leader cuts ribbon" (INITIATOR + OTHER)
        """
        # Base role weight
        role_weight = LEADER_ROLE_WEIGHTS[leader_role]

        # Context-dependent elevation: SUBJECT in high-stakes events
        if leader_role == LeaderRole.SUBJECT and event_type in SUBJECT_ELEVATING_EVENTS:
            role_weight *= SUBJECT_ELEVATION_MODIFIER

        raw_score = (
            EVENT_TYPE_WEIGHTS[event_type] +
            role_weight +
            IMPACT_LEVEL_WEIGHTS[impact_level]
        )

        # Normalize (may exceed 1.0 with modifiers, which is fine for ranking)
        return round(raw_score / MAX_WEIGHT, 3)


@dataclass
class Article:
    """A news article about a tracked leader."""
    id: str
    title: str
    url: str
    source_name: str
    source_type: str  # "wire", "domestic", "state_media"
    published_at: Optional[datetime] = None
    fetched_at: datetime = field(default_factory=datetime.now)
    
    # Content
    content: str = ""
    summary: str = ""
    original_language: str = "en"
    translated_content: Optional[str] = None
    
    # Classification (populated by classifier agent)
    classification: Optional[ArticleClassification] = None
    
    # Extracted data
    underlying_event: Optional[str] = None  # Normalized event description
    entities_mentioned: list[str] = field(default_factory=list)
    
    @property
    def display_content(self) -> str:
        """Return translated content if available, otherwise original."""
        return self.translated_content or self.content


@dataclass
class UnderlyingEvent:
    """
    A normalized representation of a real-world event.
    
    Multiple articles may describe the same underlying event.
    Used for cross-cutting thread detection.
    """
    id: str
    description: str
    event_date: Optional[datetime] = None
    location: Optional[str] = None
    
    # Which leaders are involved
    leaders_involved: list[str] = field(default_factory=list)
    
    # Source articles
    article_ids: list[str] = field(default_factory=list)
    
    # Embedding for clustering (populated by thread detector)
    embedding: Optional[list[float]] = None


# =============================================================================
# STORY-CENTRIC OUTPUT MODELS
# =============================================================================

class StoryScope(str, Enum):
    """Whether a story is international or domestic in scope."""
    INTERNATIONAL = "international"
    DOMESTIC = "domestic"


@dataclass
class Story:
    """A single story in the briefing, used at both per-leader and aggregate levels."""
    id: str
    title: str
    narrative: str                    # AP-style news report with dateline
    scope: StoryScope
    source_count: int
    has_wire: bool
    score: float
    source_refs: dict[str, list[str]] = field(default_factory=dict)  # source_name -> [urls]
    entities: list[dict] = field(default_factory=list)  # high-salience entities from NLP
    cluster_id: str = ""              # originating EventCluster ID
    contributing_leaders: list[str] = field(default_factory=list)  # for aggregate shared stories
    classification: Optional[ArticleClassification] = None  # Paragon taxonomy for sorting overflow
    # Cluster centroid embedding for cross-leader semantic matching
    # Enables "Panzer" <-> "tanks" matching when entity URIs fail
    embedding: Optional[list[float]] = None


# =============================================================================
# DOSSIER AND BRIEF MODELS
# =============================================================================

@dataclass
class LeaderDossier:
    """
    Compiled intelligence on a single leader for the reporting period.

    Story-centric structure: Main Stories / International / Domestic / Between the Lines.
    """
    leader: LeaderConfig
    reporting_period: str  # e.g., "2026-01-13 to 2026-01-21"

    # Story-centric sections
    main_stories: list[Story] = field(default_factory=list)
    international_stories: list[Story] = field(default_factory=list)
    domestic_stories: list[Story] = field(default_factory=list)
    between_the_lines: list[str] = field(default_factory=list)

    # Source data
    articles: list[Article] = field(default_factory=list)
    underlying_events: list[UnderlyingEvent] = field(default_factory=list)

    # Metadata
    executive_summary: str = ""  # 2-3 sentence summary of leader's week
    source_quality_notes: str = ""
    generated_at: datetime = field(default_factory=datetime.now)


@dataclass
class WeeklyBrief:
    """
    The final compiled weekly intelligence brief.

    Story-centric structure at aggregate level.
    """
    date_range: str
    generated_at: datetime

    # Story-centric aggregate sections
    main_stories: list[Story] = field(default_factory=list)
    international_stories: list[Story] = field(default_factory=list)
    domestic_stories: list[Story] = field(default_factory=list)
    between_the_lines: list[str] = field(default_factory=list)

    # Executive summary (2-4 sentences distilling the week's key developments)
    executive_summary: str = ""

    # Per-leader dossiers
    leader_dossiers: list[LeaderDossier] = field(default_factory=list)

    # Methodology and quality
    methodology_notes: str = ""
    source_quality_notes: str = ""


# =============================================================================
# DEPRECATED MODELS (kept for backward-compat deserialization only)
# =============================================================================

@dataclass
class LeaderAction:
    """DEPRECATED: Use Story instead. Kept for backward-compat deserialization."""
    description: str
    event_type: EventType
    date: Optional[datetime] = None
    source_articles: list[str] = field(default_factory=list)
    significance: str = ""
    source_refs: dict[str, list[str]] = field(default_factory=dict)


@dataclass
class EventSummary:
    """DEPRECATED: Use Story instead. Kept for backward-compat deserialization."""
    title: str
    score: float
    source_count: int
    has_wire: bool
    snippet_count: int
    sources: list[str] = field(default_factory=list)
    is_opinion: bool = False


@dataclass
class CrossCuttingThread:
    """DEPRECATED: Use Story + AggregateBriefingBuilder instead. Kept for backward-compat."""
    id: str
    title: str
    description: str
    leader_postures: dict[str, str] = field(default_factory=dict)
    leader_count: int = 0
    event_ids: list[str] = field(default_factory=list)
    tension_points: list[str] = field(default_factory=list)
    convergence_points: list[str] = field(default_factory=list)
    trajectory: str = ""
    is_singleton: bool = False
    significance_score: float = 0.0
    event_type: str = ""


@dataclass
class GlobalPulse:
    """DEPRECATED: Kept for backward-compat deserialization."""
    top_stories: list[str] = field(default_factory=list)
    key_themes: list[str] = field(default_factory=list)
    date_range: str = ""


# =============================================================================
# REGIONAL GROUPINGS
# =============================================================================

REGION_DISPLAY_NAMES: dict[str, str] = {
    "europe": "Europe",
    "baltics": "Baltic States",
    "north_america": "North America",
    "south_america": "South America",
    "americas": "Americas",
    "asia_pacific": "Asia-Pacific",
}

# Country to sub-region mapping for finer grouping
COUNTRY_SUBREGION: dict[str, str] = {
    "Canada": "north_america",
    "Mexico": "north_america",
    "Brazil": "south_america",
    "Uruguay": "south_america",
    "France": "europe",
    "United Kingdom": "europe",
    "Germany": "europe",
    "Italy": "europe",
    "Ukraine": "europe",
    "Finland": "europe",
    "Poland": "europe",
    "Lithuania": "baltics",
    "Latvia": "baltics",
    "Estonia": "baltics",
    "Moldova": "europe",
}

REGION_ORDER: list[str] = ["north_america", "south_america", "europe", "baltics", "asia_pacific"]

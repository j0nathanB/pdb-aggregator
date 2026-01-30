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
DEFAULT_MODEL = "claude-sonnet-4-20250514"

# News fetching settings
MAX_ARTICLES_PER_LEADER = 5
MAX_ARTICLE_CONTENT_LENGTH = 0  # 0 = full text, positive = truncate
API_CALL_DELAY_SECONDS = 2.0

# Singleton detection thresholds
SINGLETON_THRESHOLD = 0.7

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
    SourceConfig(
        name="AFP",
        url="https://www.afp.com",
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
    region: str  # "europe", "americas", "asia_pacific"
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


def get_leader_configs() -> list[LeaderConfig]:
    """
    Return configurations for all tracked leaders.
    
    Leaders are selected based on geopolitical significance and
    availability of diverse source coverage.
    """
    return [
        # AMERICAS
        LeaderConfig(
            name="Mark Carney",
            title="Prime Minister",
            country="Canada",
            region="americas",
            domestic_sources=[
                SourceConfig(
                    name="Globe and Mail",
                    url="https://www.theglobeandmail.com",
                    language="en",
                ),
                SourceConfig(
                    name="CBC News",
                    url="https://www.cbc.ca/news",
                    language="en",
                    rss_url="https://www.cbc.ca/webfeed/rss/rss-topstories",
                ),
                SourceConfig(
                    name="National Post",
                    url="https://nationalpost.com",
                    language="en",
                ),
            ],
        ),
        LeaderConfig(
            name="Claudia Sheinbaum",
            title="President",
            country="Mexico",
            region="americas",
            domestic_sources=[
                SourceConfig(
                    name="El Universal",
                    url="https://www.eluniversal.com.mx",
                    language="es",
                ),
                SourceConfig(
                    name="Reforma",
                    url="https://www.reforma.com",
                    language="es",
                ),
                SourceConfig(
                    name="La Jornada",
                    url="https://www.jornada.com.mx",
                    language="es",
                ),
            ],
        ),
        
        # EUROPE
        LeaderConfig(
            name="Volodymyr Zelenskyy",
            title="President",
            country="Ukraine",
            region="europe",
            domestic_sources=[
                SourceConfig(
                    name="Ukrinform",
                    url="https://www.ukrinform.net",
                    language="en",  # English version available
                ),
                SourceConfig(
                    name="Kyiv Independent",
                    url="https://kyivindependent.com",
                    language="en",
                ),
            ],
        ),
        LeaderConfig(
            name="Emmanuel Macron",
            title="President",
            country="France",
            region="europe",
            domestic_sources=[
                SourceConfig(
                    name="Le Monde",
                    url="https://www.lemonde.fr",
                    language="fr",
                ),
                SourceConfig(
                    name="Le Figaro",
                    url="https://www.lefigaro.fr",
                    language="fr",
                ),
                SourceConfig(
                    name="Libération",
                    url="https://www.liberation.fr",
                    language="fr",
                ),
            ],
        ),
        LeaderConfig(
            name="Friedrich Merz",
            title="Chancellor",
            country="Germany",
            region="europe",
            domestic_sources=[
                SourceConfig(
                    name="Frankfurter Allgemeine",
                    url="https://www.faz.net",
                    language="de",
                ),
                SourceConfig(
                    name="Süddeutsche Zeitung",
                    url="https://www.sueddeutsche.de",
                    language="de",
                ),
                SourceConfig(
                    name="Der Spiegel",
                    url="https://www.spiegel.de",
                    language="de",
                ),
            ],
        ),
        LeaderConfig(
            name="Keir Starmer",
            title="Prime Minister",
            country="United Kingdom",
            region="europe",
            domestic_sources=[
                SourceConfig(
                    name="BBC News",
                    url="https://www.bbc.com/news",
                    language="en",
                    rss_url="https://feeds.bbci.co.uk/news/rss.xml",
                ),
                SourceConfig(
                    name="The Guardian",
                    url="https://www.theguardian.com",
                    language="en",
                    rss_url="https://www.theguardian.com/world/rss",
                ),
                SourceConfig(
                    name="The Telegraph",
                    url="https://www.telegraph.co.uk",
                    language="en",
                ),
            ],
        ),
        LeaderConfig(
            name="Karol Nawrocki",
            title="President",
            country="Poland",
            region="europe",
            domestic_sources=[
                SourceConfig(
                    name="Gazeta Wyborcza",
                    url="https://wyborcza.pl",
                    language="pl",
                ),
                SourceConfig(
                    name="Rzeczpospolita",
                    url="https://www.rp.pl",
                    language="pl",
                ),
            ],
        ),
        LeaderConfig(
            name="Alexander Stubb",
            title="President",
            country="Finland",
            region="europe",
            domestic_sources=[
                SourceConfig(
                    name="Helsingin Sanomat",
                    url="https://www.hs.fi",
                    language="fi",
                ),
                SourceConfig(
                    name="Yle News",
                    url="https://yle.fi/news",
                    language="en",  # English version
                ),
            ],
        ),
        LeaderConfig(
            name="Mark Rutte",
            title="NATO Secretary General",
            country="NATO",
            region="europe",
            domestic_sources=[
                SourceConfig(
                    name="NATO Press",
                    url="https://www.nato.int/cps/en/natohq/news.htm",
                    language="en",
                ),
            ],
        ),
        
        # ASIA-PACIFIC
        LeaderConfig(
            name="Xi Jinping",
            title="President",
            country="China",
            region="asia_pacific",
            domestic_sources=[
                SourceConfig(
                    name="Xinhua",
                    url="https://www.xinhuanet.com",
                    language="zh",
                    source_type="state_media",
                ),
                SourceConfig(
                    name="South China Morning Post",
                    url="https://www.scmp.com",
                    language="en",
                ),
                SourceConfig(
                    name="Caixin",
                    url="https://www.caixinglobal.com",
                    language="en",
                ),
            ],
        ),
    ]


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
        """Calculate normalized priority score from taxonomy values."""
        raw_score = (
            EVENT_TYPE_WEIGHTS[event_type] +
            LEADER_ROLE_WEIGHTS[leader_role] +
            IMPACT_LEVEL_WEIGHTS[impact_level]
        )
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
# DOSSIER AND BRIEF MODELS
# =============================================================================

@dataclass
class LeaderAction:
    """A significant action taken by a leader during the reporting period."""
    description: str
    event_type: EventType
    date: Optional[datetime] = None
    source_articles: list[str] = field(default_factory=list)  # Article IDs
    significance: str = ""  # Why this matters


@dataclass
class LeaderDossier:
    """
    Compiled intelligence on a single leader for the reporting period.
    """
    leader: LeaderConfig
    reporting_period: str  # e.g., "2026-01-13 to 2026-01-21"
    
    # Key actions (3-5 most significant)
    key_actions: list[LeaderAction] = field(default_factory=list)
    
    # Narrative analysis
    domestic_context: str = ""  # What's happening domestically
    international_posture: str = ""  # How they're engaging internationally
    assessment: str = ""  # Analyst assessment of trajectory
    
    # Source data
    articles: list[Article] = field(default_factory=list)
    underlying_events: list[UnderlyingEvent] = field(default_factory=list)
    
    # Metadata
    source_quality_notes: str = ""
    generated_at: datetime = field(default_factory=datetime.now)


@dataclass
class CrossCuttingThread:
    """
    A theme or event that connects multiple leaders.

    Detected via semantic clustering of underlying events.
    Also supports singleton threads for high-impact single-leader events.
    """
    id: str
    title: str  # e.g., "NATO Defense Spending Commitments"
    description: str

    # Which leaders are involved and how
    leader_postures: dict[str, str] = field(default_factory=dict)  # leader_name -> their position
    leader_count: int = 0

    # Underlying events in this cluster
    event_ids: list[str] = field(default_factory=list)

    # Analysis
    tension_points: list[str] = field(default_factory=list)
    convergence_points: list[str] = field(default_factory=list)
    trajectory: str = ""  # Where this is heading

    # Singleton support (single-leader high-impact events)
    is_singleton: bool = False
    significance_score: float = 0.0
    event_type: str = ""  # Event type for singletons


@dataclass
class GlobalPulse:
    """
    Top world stories providing context for the brief.
    
    Helps identify what events leaders might be responding to.
    """
    top_stories: list[str] = field(default_factory=list)
    key_themes: list[str] = field(default_factory=list)
    date_range: str = ""


@dataclass
class WeeklyBrief:
    """
    The final compiled weekly intelligence brief.
    """
    date_range: str
    generated_at: datetime

    # Context (optional in bottom-up architecture)
    global_pulse: Optional[GlobalPulse] = None

    # Core content
    executive_summary: str = ""
    cross_cutting_threads: list[CrossCuttingThread] = field(default_factory=list)
    leader_dossiers: list[LeaderDossier] = field(default_factory=list)

    # Regional analysis
    regional_context: dict[str, str] = field(default_factory=dict)  # region -> analysis

    # Methodology and quality
    methodology_notes: str = ""
    source_quality_notes: str = ""


# =============================================================================
# REGIONAL GROUPINGS
# =============================================================================

REGION_DISPLAY_NAMES: dict[str, str] = {
    "europe": "Europe",
    "americas": "Americas", 
    "asia_pacific": "Asia-Pacific",
}

REGION_ORDER: list[str] = ["europe", "americas", "asia_pacific"]

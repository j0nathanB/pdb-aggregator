"""
Structured content models for the newsletter pipeline.

These dataclasses are the interchange format between content_builder,
editor, copyeditor, and renderer. Markdown/MDX is never used as an
interchange format — it is produced exactly once by the renderer.
"""

from dataclasses import dataclass, field
from datetime import date
from typing import Optional

from ..config import Movement, Region, SignalCategory


# =============================================================================
# Leaf content types
# =============================================================================

@dataclass
class SourceRef:
    """Source attribution — rendered mechanically in Notes section."""
    name: str
    url: str
    tier: int = 2


@dataclass
class BriefingItemInput:
    """A single executive briefing item — input to the editor."""
    title: str
    regions_involved: list[str]
    what: str
    why_it_matters: str
    what_to_watch: str
    confidence: int
    confidence_note: str = ""


@dataclass
class DevelopmentContent:
    """A development within a signal category."""
    category: SignalCategory
    category_display: str
    movement: Movement
    text: str
    sources: list[SourceRef] = field(default_factory=list)


@dataclass
class StoryClusterContent:
    """A story cluster for the Other Stories accordion."""
    headline: str
    summary: str
    source_name: str = ""
    source_url: str = ""


@dataclass
class AbsenceContent:
    """A notable absence."""
    expected: str
    significance: str


@dataclass
class UnexpectedContent:
    """An unexpected development."""
    headline: str
    assessment: str


# =============================================================================
# Country content
# =============================================================================

@dataclass
class CountryContent:
    """Complete content for a single country section.

    The content builder populates structured fields. The editor reads them
    and produces narrative_body. The copyeditor polishes all prose. The
    template renders the final MDX.
    """

    # Identity
    code: str
    country: str

    # Activity level for sort ordering
    activity_rating: Optional[str] = None

    # Posture summary from ledger
    posture_summary: str = ""

    # --- Editor inputs ---

    # Developments — always populated (even for Movement.NONE)
    developments: list[DevelopmentContent] = field(default_factory=list)

    # Unexpected developments
    unexpected: list[UnexpectedContent] = field(default_factory=list)

    # Notable absences
    absences: list[AbsenceContent] = field(default_factory=list)

    # Raw analysis context for the editor (not rendered)
    raw_analysis: Optional[dict] = None

    # --- Editor output ---

    # Rewritten prose — None until editor runs
    narrative_body: Optional[str] = None

    # --- Passthrough ---

    # Other stories — copyeditor polishes, template renders in Accordion
    other_stories: list[StoryClusterContent] = field(default_factory=list)

    # Story map sidecar for Notes accordion (mechanical rendering)
    story_map_data: Optional[dict] = None


# =============================================================================
# Executive brief
# =============================================================================

@dataclass
class ExecutiveBriefContent:
    """Executive brief — items woven into a single essay by the editor."""

    items: list[BriefingItemInput] = field(default_factory=list)

    # Editor output — unified essay, plain prose. None until editor runs.
    edited_essay: Optional[str] = None
    headline: Optional[str] = None


# =============================================================================
# =============================================================================
# Page content types
# =============================================================================

@dataclass
class OverviewPageContent:
    """Structured content for the overview/landing page."""

    week_start: date
    week_end: date
    country_count: int

    executive_brief: ExecutiveBriefContent = field(default_factory=ExecutiveBriefContent)


@dataclass
class RegionPageContent:
    """Structured content for a region page."""

    region: Region
    display_name: str
    week_start: date
    week_end: date

    # Editor rewrites these
    regional_lead: str = ""
    headline: str = ""
    gap_paragraphs: list[str] = field(default_factory=list)
    card_summary: str = ""

    # Raw cross-cutting dynamics for editor context (not rendered directly)
    raw_dynamics: Optional[list[dict]] = None

    # Country sections ordered by activity level
    countries: list[CountryContent] = field(default_factory=list)


# =============================================================================
# At-a-glance page
# =============================================================================

@dataclass
class AtAGlanceCountry:
    """A single country entry on the at-a-glance page."""
    code: str
    name: str
    headline: str
    source_count: int


@dataclass
class AtAGlanceRegion:
    """A region group on the at-a-glance page."""
    region: Region
    display_name: str
    slug: str
    card_summary: str = ""
    countries: list[AtAGlanceCountry] = field(default_factory=list)


@dataclass
class AtAGlancePageContent:
    """Structured content for the at-a-glance page.

    Deterministic — built from story maps, no LLM calls.
    Shows top story headline per country, grouped by region.
    """

    week_start: date
    week_end: date
    regions: list[AtAGlanceRegion] = field(default_factory=list)

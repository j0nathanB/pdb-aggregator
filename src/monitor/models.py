"""
Pydantic models for country ledgers and global ledger.

These map directly to the schemas defined in the v4 architecture doc.
"""

from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, field_validator, model_validator

from .config import (
    CONFIDENCE_MAX,
    CONFIDENCE_MIN,
    SOURCE_TIER_MAX,
    SOURCE_TIER_MIN,
    ActivityRating,
    CategoryStatus,
    ClaimStatus,
    Depth,
    DynamicStatus,
    LinkageType,
    Movement,
    SignalCategory,
)


# =============================================================================
# Shared
# =============================================================================

def _confidence_field(default: int = 3) -> int:
    return Field(default=default, ge=CONFIDENCE_MIN, le=CONFIDENCE_MAX)


def _source_tier_field() -> int:
    return Field(ge=SOURCE_TIER_MIN, le=SOURCE_TIER_MAX)


class ActorRef(BaseModel):
    name: str
    role: str
    primary: bool = False


# =============================================================================
# Country Ledger
# =============================================================================

class PostureSummary(BaseModel):
    as_of: date
    text: str
    category_status: dict[SignalCategory, CategoryStatus]
    last_deep_dive: Optional[date] = None
    consecutive_maintenance_weeks: int = 0

    @field_validator("category_status")
    @classmethod
    def all_categories_present(cls, v: dict) -> dict:
        missing = set(SignalCategory) - set(v.keys())
        if missing:
            raise ValueError(f"Missing signal categories: {missing}")
        return v


class SignalCategoryAssessment(BaseModel):
    current_assessment: str
    confidence: int = _confidence_field()
    confidence_rationale: str = ""
    key_actors: list[str] = Field(default_factory=list)
    dossier_sections_referenced: list[str] = Field(default_factory=list)

    @field_validator("dossier_sections_referenced", mode="before")
    @classmethod
    def _coerce_sections_to_str(cls, v: list) -> list[str]:
        return [str(x) for x in v] if v else []
    last_updated: date


class SourceAttribution(BaseModel):
    name: str
    url: str = ""
    tier: int = _source_tier_field()


class Development(BaseModel):
    headline: str
    date: date
    sources: list[SourceAttribution] = Field(default_factory=list)
    summary: str = ""
    actors_involved: list[str] = Field(default_factory=list)
    signal_category_relevance: str = ""

    # Backward-compat: old ledgers have single source/source_url/source_tier
    @model_validator(mode="before")
    @classmethod
    def _migrate_single_source(cls, data: dict) -> dict:
        if isinstance(data, dict) and "source" in data and "sources" not in data:
            data["sources"] = [{
                "name": data.pop("source", "unknown"),
                "url": data.pop("source_url", ""),
                "tier": data.pop("source_tier", 2),
            }]
        elif isinstance(data, dict) and "source" in data and "sources" in data:
            # Both present — drop the old fields
            data.pop("source", None)
            data.pop("source_url", None)
            data.pop("source_tier", None)
        return data

    @property
    def source(self) -> str:
        """Primary source name (backward compat)."""
        return self.sources[0].name if self.sources else "unknown"

    @property
    def source_url(self) -> str:
        """Primary source URL (backward compat)."""
        return self.sources[0].url if self.sources else ""

    @property
    def source_tier(self) -> int:
        """Best (lowest) source tier."""
        return min((s.tier for s in self.sources), default=2)


class ConfidenceChange(BaseModel):
    model_config = {"populate_by_name": True}
    from_: int = Field(alias="from", ge=CONFIDENCE_MIN, le=CONFIDENCE_MAX, serialization_alias="from")
    to: int = Field(ge=CONFIDENCE_MIN, le=CONFIDENCE_MAX)
    reason: str = ""


class CategoryMovement(BaseModel):
    movement: Movement
    developments: list[Development] = Field(default_factory=list)
    prior_assessment: str = ""
    updated_assessment: str = ""
    confidence_change: Optional[ConfidenceChange] = None


class UnexpectedDevelopment(BaseModel):
    headline: str
    date: date
    sources: list[SourceAttribution] = Field(default_factory=list)
    signal_category: SignalCategory
    assessment: str = ""
    disposition: str = "logged"  # "logged" | "elevated_to_category"

    # Backward-compat: old ledgers and the LLM both emit a single `source` —
    # the LLM as a {name, url, tier} dict, old ledgers as a string with a
    # sibling `source_tier` int. Migrate either into the list shape.
    @model_validator(mode="before")
    @classmethod
    def _migrate_single_source(cls, data: dict) -> dict:
        if not isinstance(data, dict):
            return data
        if "source" in data and "sources" not in data:
            src = data.pop("source")
            if isinstance(src, dict):
                data["sources"] = [src]
            else:
                data["sources"] = [{
                    "name": str(src) if src else "unknown",
                    "url": data.pop("source_url", ""),
                    "tier": data.pop("source_tier", 2),
                }]
        if "sources" in data:
            data.pop("source", None)
            data.pop("source_url", None)
            data.pop("source_tier", None)
        return data

    @property
    def source(self) -> str:
        """Primary source name (backward compat)."""
        return self.sources[0].name if self.sources else "unknown"

    @property
    def source_url(self) -> str:
        """Primary source URL (backward compat)."""
        return self.sources[0].url if self.sources else ""

    @property
    def source_tier(self) -> int:
        """Best (lowest) source tier."""
        return min((s.tier for s in self.sources), default=2)


class AbsenceCheck(BaseModel):
    expected: str
    signal_category: SignalCategory
    occurred: bool
    significance: str = ""
    confidence: int = _confidence_field(default=2)


class DevilsAdvocate(BaseModel):
    challenges: list[str] = Field(default_factory=list)
    recommended_adjustments: list[str] = Field(default_factory=list)


class SelfCorrection(BaseModel):
    category: SignalCategory
    prior_week: date
    original_claim: str
    correction: str
    root_cause: str


class StructuralClaimCheck(BaseModel):
    claim_ref: str
    claim_text: str
    status: ClaimStatus
    evidence: str = ""
    confidence_in_claim: int = _confidence_field()


class StoryClusterSummary(BaseModel):
    """Lightweight story cluster record for newsletter rendering."""

    headline: str
    summary: str
    source_url: str = ""
    source_name: str = ""


class WeeklyEntry(BaseModel):
    week: date
    date_range: str
    depth: Depth
    activity_level: Optional[dict] = None  # {rating, rationale} — optional for maintenance
    category_movements: Optional[dict[SignalCategory, CategoryMovement]] = None
    unexpected_developments: list[UnexpectedDevelopment] = Field(default_factory=list)
    absence_check: list[AbsenceCheck] = Field(default_factory=list)
    devils_advocate: Optional[DevilsAdvocate] = None
    self_corrections: list[SelfCorrection] = Field(default_factory=list)
    structural_claim_checks: list[StructuralClaimCheck] = Field(default_factory=list)
    story_clusters: list[StoryClusterSummary] = Field(default_factory=list)

    @model_validator(mode="after")
    def deep_dive_requires_category_movements(self):
        if self.depth == Depth.DEEP_DIVE:
            if self.category_movements is None:
                raise ValueError("Deep-dive entries require category_movements")
            missing = set(SignalCategory) - set(self.category_movements.keys())
            if missing:
                raise ValueError(f"Deep-dive entries require all 5 categories; missing: {missing}")
        return self

    def validate_complete(self) -> list[str]:
        """Validate that a deep-dive entry is complete (has devils_advocate).

        Call this before writing to the ledger. Returns list of errors.
        """
        errors = []
        if self.depth == Depth.DEEP_DIVE and self.devils_advocate is None:
            errors.append("Deep-dive entries require devils_advocate before ledger write")
        return errors


class StructuralClaimStatus(BaseModel):
    claim_ref: str
    claim_text: str
    dossier_section: int
    status: ClaimStatus
    last_checked: date
    evidence_summary: str = ""
    weeks_under_pressure: int = 0
    recommendation: str = ""


class CorrectionLogEntry(BaseModel):
    correction_date: date
    original_week: date
    original_claim: str
    corrected_to: str
    category_affected: SignalCategory
    root_cause: str


class CountryLedger(BaseModel):
    country: str
    code: str = Field(pattern=r"^[a-z]{2}$")
    tier: str
    actors: list[ActorRef]
    last_updated: date
    created: date

    posture_summary: PostureSummary
    signal_categories: dict[SignalCategory, SignalCategoryAssessment]
    weekly_entries: list[WeeklyEntry] = Field(default_factory=list)
    structural_claim_status: list[StructuralClaimStatus] = Field(default_factory=list)
    corrections_log: list[CorrectionLogEntry] = Field(default_factory=list)
    consolidated_history: str = ""

    @field_validator("signal_categories")
    @classmethod
    def all_categories_present(cls, v: dict) -> dict:
        missing = set(SignalCategory) - set(v.keys())
        if missing:
            raise ValueError(f"Missing signal categories: {missing}")
        return v

    @property
    def needs_deep_dive(self) -> bool:
        return self.posture_summary.consecutive_maintenance_weeks >= 4

    @property
    def needs_consolidation(self) -> bool:
        return len(self.weekly_entries) > 8

    def latest_entry(self) -> Optional[WeeklyEntry]:
        return self.weekly_entries[-1] if self.weekly_entries else None


# =============================================================================
# Global Ledger
# =============================================================================

class SignalEnvironment(BaseModel):
    most_active_categories: list[SignalCategory] = Field(default_factory=list)
    quietest_categories: list[SignalCategory] = Field(default_factory=list)
    geographic_hotspots: list[str] = Field(default_factory=list)
    geographic_quiet_zones: list[str] = Field(default_factory=list)


class GlobalPostureSummary(BaseModel):
    as_of: date
    text: str
    signal_environment: SignalEnvironment = Field(default_factory=SignalEnvironment)


class TriageImplication(BaseModel):
    countries_to_flag: list[str] = Field(default_factory=list)
    reason: str = ""


class EvidenceStrength(BaseModel):
    confidence: int = _confidence_field()
    supporting_country_confidences: dict[str, int] = Field(default_factory=dict)
    weakest_link: str = ""
    linkage_type: LinkageType = LinkageType.PARALLEL_BEHAVIOR
    linkage_assessment: str = ""


class ActiveDynamic(BaseModel):
    dynamic_id: int
    title: str
    created_week: date
    last_updated: date
    status: DynamicStatus
    current_assessment: str
    countries_involved: list[str] = Field(default_factory=list)
    signal_categories_touched: list[SignalCategory] = Field(default_factory=list)
    evidence_strength: EvidenceStrength = Field(default_factory=EvidenceStrength)
    competing_interpretation: str = ""
    what_to_watch: str = ""
    triage_implications: TriageImplication = Field(default_factory=TriageImplication)
    weeks_active: int = 0
    consecutive_unchanged_weeks: int = 0


class WatchlistItem(BaseModel):
    item: str
    signal_category: SignalCategory
    countries: list[str] = Field(default_factory=list)
    why_it_matters: str = ""
    trigger: str = ""
    added_week: date


class ExecutiveBriefingItem(BaseModel):
    title: str
    regions_involved: list[str] = Field(default_factory=list)
    what: str
    why_it_matters: str
    what_to_watch: str = ""
    confidence: int = _confidence_field()
    confidence_note: str = ""


class RejectedItem(BaseModel):
    candidate: str
    reason_rejected: str


class GlobalSelfCorrection(BaseModel):
    dynamic_id: int
    prior_assessment: str
    correction: str
    root_cause: str


class GlobalWeeklyEntry(BaseModel):
    week: date
    executive_briefing_items: list[ExecutiveBriefingItem] = Field(default_factory=list)
    dynamics_created: list[int] = Field(default_factory=list)
    dynamics_updated: list[int] = Field(default_factory=list)
    dynamics_archived: list[int] = Field(default_factory=list)
    items_considered_rejected: list[RejectedItem] = Field(default_factory=list)
    self_corrections: list[GlobalSelfCorrection] = Field(default_factory=list)

    @field_validator("items_considered_rejected")
    @classmethod
    def rejection_log_not_empty(cls, v: list) -> list:
        if not v:
            raise ValueError("items_considered_rejected must not be empty")
        return v


class GlobalLedger(BaseModel):
    last_updated: date
    created: date

    global_posture_summary: GlobalPostureSummary
    active_dynamics: list[ActiveDynamic] = Field(default_factory=list)
    watchlist: list[WatchlistItem] = Field(default_factory=list)
    weekly_entries: list[GlobalWeeklyEntry] = Field(default_factory=list)
    archived_dynamics: list[ActiveDynamic] = Field(default_factory=list)
    consolidated_history: str = ""

    def next_dynamic_id(self) -> int:
        all_ids = [d.dynamic_id for d in self.active_dynamics + self.archived_dynamics]
        return max(all_ids, default=0) + 1

    @property
    def needs_consolidation(self) -> bool:
        return len(self.weekly_entries) > 8

    @property
    def triage_flagged_countries(self) -> set[str]:
        codes: set[str] = set()
        for d in self.active_dynamics:
            codes.update(d.triage_implications.countries_to_flag)
        return codes

    def latest_entry(self) -> Optional[GlobalWeeklyEntry]:
        return self.weekly_entries[-1] if self.weekly_entries else None

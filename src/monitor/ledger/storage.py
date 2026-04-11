"""
Ledger persistence: read/write country, global, and regional ledgers as JSON.
"""

import json
import logging
from dataclasses import asdict
from datetime import date
from pathlib import Path

from ..config import (
    COUNTRY_LEDGERS_DIR,
    GLOBAL_LEDGER_PATH,
    LEDGER_ARCHIVE_DIR,
    REGIONAL_REPORTS_DIR,
    STORY_MAPS_DIR,
    Region,
)
from ..models import CountryLedger, GlobalLedger

logger = logging.getLogger(__name__)


def _json_serializer(obj: object) -> str:
    if isinstance(obj, date):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def _write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    with open(tmp, "w") as f:
        json.dump(data, f, indent=2, default=_json_serializer)
        f.write("\n")
    tmp.rename(path)


def _read_json(path: Path) -> dict:
    with open(path) as f:
        return json.load(f)


# ---- Country Ledger ----

def save_country_ledger(ledger: CountryLedger) -> Path:
    path = COUNTRY_LEDGERS_DIR / f"{ledger.code}.json"
    _write_json(path, ledger.model_dump(mode="json", by_alias=True))
    logger.debug("Saved country ledger: %s (%d weekly entries)", ledger.code, len(ledger.weekly_entries))
    return path


def load_country_ledger(code: str) -> CountryLedger:
    path = COUNTRY_LEDGERS_DIR / f"{code}.json"
    if not path.exists():
        raise FileNotFoundError(f"No ledger for country code '{code}': {path}")
    ledger = CountryLedger.model_validate(_read_json(path))
    logger.debug("Loaded country ledger: %s (%d weekly entries)", code, len(ledger.weekly_entries))
    return ledger


def country_ledger_exists(code: str) -> bool:
    return (COUNTRY_LEDGERS_DIR / f"{code}.json").exists()


def list_country_ledgers() -> list[str]:
    return sorted(p.stem for p in COUNTRY_LEDGERS_DIR.glob("*.json"))


# ---- Global Ledger ----

def save_global_ledger(ledger: GlobalLedger) -> Path:
    _write_json(GLOBAL_LEDGER_PATH, ledger.model_dump(mode="json", by_alias=True))
    logger.debug(
        "Saved global ledger: %d active dynamics, %d weekly entries",
        len(ledger.active_dynamics), len(ledger.weekly_entries),
    )
    return GLOBAL_LEDGER_PATH


def load_global_ledger() -> GlobalLedger:
    if not GLOBAL_LEDGER_PATH.exists():
        raise FileNotFoundError(f"Global ledger not found: {GLOBAL_LEDGER_PATH}")
    ledger = GlobalLedger.model_validate(_read_json(GLOBAL_LEDGER_PATH))
    logger.debug(
        "Loaded global ledger: %d active dynamics, %d weekly entries",
        len(ledger.active_dynamics), len(ledger.weekly_entries),
    )
    return ledger


def global_ledger_exists() -> bool:
    return GLOBAL_LEDGER_PATH.exists()


def init_global_ledger() -> GlobalLedger:
    """Create an empty global ledger for cold start."""
    today = date.today()
    from ..models import GlobalPostureSummary, SignalEnvironment
    ledger = GlobalLedger(
        last_updated=today,
        created=today,
        global_posture_summary=GlobalPostureSummary(
            as_of=today,
            text="",
            signal_environment=SignalEnvironment(),
        ),
    )
    save_global_ledger(ledger)
    logger.info("Initialized new global ledger (cold start)")
    return ledger


# ---- Regional Reports ----

def save_regional_report(report: "RegionalReport") -> Path:
    from ..agents.regional import RegionalReport  # noqa: F811
    path = REGIONAL_REPORTS_DIR / f"{report.region.value}.json"
    _write_json(path, asdict(report))
    logger.debug("Saved regional report: %s", report.region.value)
    return path


def load_regional_report(region: Region) -> "RegionalReport":
    from ..agents.regional import (
        CrossCuttingDynamic,
        Gap,
        LowConfidenceItem,
        RegionalHighlight,
        RegionalReport,
        RejectedDynamic,
    )
    path = REGIONAL_REPORTS_DIR / f"{region.value}.json"
    if not path.exists():
        raise FileNotFoundError(f"No regional report for '{region.value}': {path}")
    raw = _read_json(path)
    return RegionalReport(
        region=Region(raw["region"]),
        week=date.fromisoformat(raw["week"]),
        regional_overview=raw.get("regional_overview", ""),
        regional_highlights=[RegionalHighlight(**h) for h in raw.get("regional_highlights", [])],
        cross_cutting_dynamics=[CrossCuttingDynamic(**d) for d in raw.get("cross_cutting_dynamics", [])],
        dynamics_considered_and_rejected=[RejectedDynamic(**d) for d in raw.get("dynamics_considered_and_rejected", [])],
        gaps=[Gap(**g) for g in raw.get("gaps", [])],
        low_confidence_items=[LowConfidenceItem(**i) for i in raw.get("low_confidence_items", [])],
    )


def load_all_regional_reports() -> dict[Region, "RegionalReport"]:
    reports = {}
    for path in REGIONAL_REPORTS_DIR.glob("*.json"):
        try:
            region = Region(path.stem)
            reports[region] = load_regional_report(region)
        except (ValueError, FileNotFoundError):
            logger.warning("Skipping invalid regional report: %s", path.name)
    return reports


# ---- Story Maps ----

def save_story_map(code: str, week: date, story_map: "StoryMapOutput") -> Path:
    """Persist a full StoryMapOutput as a sidecar JSON alongside the ledger."""
    from ..agents.story_map import StoryCluster, SingleSourceItem, UnassignedItem
    path = STORY_MAPS_DIR / f"{code}_{week.isoformat()}.json"
    data = {
        "country": story_map.country,
        "code": code,
        "week": week.isoformat(),
        "analysis_date": story_map.analysis_date,
        "search_results_total": story_map.search_results_total,
        "stories_identified": story_map.stories_identified,
        "off_topic_filtered": story_map.off_topic_filtered,
        "noise_summary": story_map.noise_summary,
        "stories": [
            {
                "story_id": s.story_id,
                "headline": s.headline,
                "summary": s.summary,
                "actors_involved": s.actors_involved,
                "signal_category_hint": s.signal_category_hint,
                "source_count": s.source_count,
                "sources": s.sources,
                "date_range": s.date_range,
                "articles": [
                    {"title": a.title, "source": a.source, "url": a.url, "date": a.date}
                    for a in s.articles
                ],
                "representative_urls": s.representative_urls,
            }
            for s in story_map.stories
        ],
        "single_source_items": [
            {
                "headline": item.headline,
                "source": item.source,
                "url": item.url,
                "signal_category_hint": item.signal_category_hint,
            }
            for item in story_map.single_source_items
        ],
    }
    _write_json(path, data)
    logger.info("Saved story map: %s %s (%d stories)", code, week, len(story_map.stories))
    return path


def load_story_map(code: str, week: date) -> dict:
    """Load a story map sidecar JSON. Returns raw dict."""
    path = STORY_MAPS_DIR / f"{code}_{week.isoformat()}.json"
    if not path.exists():
        raise FileNotFoundError(f"No story map for {code} week {week}: {path}")
    return _read_json(path)


def list_story_maps(code: str | None = None) -> list[Path]:
    """List story map files, optionally filtered by country code."""
    pattern = f"{code}_*.json" if code else "*.json"
    return sorted(STORY_MAPS_DIR.glob(pattern))


# ---- Archival ----

def archive_weekly_entries(ledger: CountryLedger, keep: int = 8) -> CountryLedger:
    """Move older weekly entries to archive file, keeping the most recent `keep`."""
    if len(ledger.weekly_entries) <= keep:
        return ledger

    to_archive = ledger.weekly_entries[:-keep]
    kept = ledger.weekly_entries[-keep:]

    if to_archive:
        first_week = to_archive[0].week.isoformat()
        last_week = to_archive[-1].week.isoformat()
        archive_path = LEDGER_ARCHIVE_DIR / f"{ledger.code}_weeks_{first_week}_{last_week}.json"
        archive_data = [e.model_dump(mode="json") for e in to_archive]
        _write_json(archive_path, archive_data)
        logger.info(
            "Archived %d weekly entries for %s (%s to %s)",
            len(to_archive), ledger.code, first_week, last_week,
        )

    ledger.weekly_entries = kept
    return ledger

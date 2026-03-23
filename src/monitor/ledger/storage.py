"""
Ledger persistence: read/write country and global ledgers as JSON.
"""

import json
import logging
from datetime import date
from pathlib import Path

from ..config import COUNTRY_LEDGERS_DIR, GLOBAL_LEDGER_PATH, LEDGER_ARCHIVE_DIR
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

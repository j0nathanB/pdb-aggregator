"""Tests for ledger storage: read/write/archive operations."""

import json
from datetime import date
from pathlib import Path

import pytest
from src.monitor.config import CategoryStatus, Depth, SignalCategory
from src.monitor.ledger.storage import (
    archive_weekly_entries,
    country_ledger_exists,
    global_ledger_exists,
    init_global_ledger,
    list_country_ledgers,
    load_country_ledger,
    load_global_ledger,
    save_country_ledger,
    save_global_ledger,
)
from src.monitor.models import (
    ActorRef,
    CountryLedger,
    GlobalLedger,
    GlobalPostureSummary,
    PostureSummary,
    SignalCategoryAssessment,
    SignalEnvironment,
    WeeklyEntry,
)


# ---- Fixtures ----

def _all_category_status():
    return {c: CategoryStatus.QUIET for c in SignalCategory}


def _all_category_assessments():
    return {
        c: SignalCategoryAssessment(
            current_assessment=f"Baseline for {c.value}",
            confidence=3,
            last_updated=date(2026, 3, 14),
        )
        for c in SignalCategory
    }


def _test_country_ledger() -> CountryLedger:
    return CountryLedger(
        country="Mexico",
        code="mx",
        tier="periphery",
        actors=[ActorRef(name="Sheinbaum", role="President", primary=True)],
        last_updated=date(2026, 3, 14),
        created=date(2026, 3, 1),
        posture_summary=PostureSummary(
            as_of=date(2026, 3, 14),
            text="Test posture.",
            category_status=_all_category_status(),
        ),
        signal_categories=_all_category_assessments(),
    )


@pytest.fixture(autouse=True)
def _use_tmp_dirs(tmp_path, monkeypatch):
    """Redirect all ledger paths to tmp_path for test isolation."""
    import src.monitor.config as cfg
    import src.monitor.ledger.storage as storage

    countries_dir = tmp_path / "ledgers" / "countries"
    countries_dir.mkdir(parents=True)
    global_path = tmp_path / "ledgers" / "global.json"
    archive_dir = tmp_path / "ledgers" / "archive"
    archive_dir.mkdir(parents=True)

    monkeypatch.setattr(storage, "COUNTRY_LEDGERS_DIR", countries_dir)
    monkeypatch.setattr(storage, "GLOBAL_LEDGER_PATH", global_path)
    monkeypatch.setattr(storage, "LEDGER_ARCHIVE_DIR", archive_dir)


# ---- Country Ledger ----

class TestCountryLedgerStorage:
    def test_roundtrip(self):
        ledger = _test_country_ledger()
        save_country_ledger(ledger)
        loaded = load_country_ledger("mx")
        assert loaded.country == "Mexico"
        assert loaded.code == "mx"
        assert len(loaded.signal_categories) == 5

    def test_exists(self):
        assert not country_ledger_exists("mx")
        save_country_ledger(_test_country_ledger())
        assert country_ledger_exists("mx")

    def test_list(self):
        save_country_ledger(_test_country_ledger())
        assert "mx" in list_country_ledgers()

    def test_load_missing_raises(self):
        with pytest.raises(FileNotFoundError):
            load_country_ledger("zz")

    def test_dates_roundtrip(self):
        ledger = _test_country_ledger()
        save_country_ledger(ledger)
        loaded = load_country_ledger("mx")
        assert loaded.last_updated == date(2026, 3, 14)
        assert loaded.posture_summary.as_of == date(2026, 3, 14)


class TestArchival:
    def test_no_archive_when_under_limit(self):
        ledger = _test_country_ledger()
        ledger.weekly_entries = [
            WeeklyEntry(week=date(2026, 1, i + 1), date_range=f"w{i}", depth=Depth.MAINTENANCE)
            for i in range(6)
        ]
        result = archive_weekly_entries(ledger, keep=8)
        assert len(result.weekly_entries) == 6

    def test_archive_trims_to_keep(self, tmp_path):
        ledger = _test_country_ledger()
        ledger.weekly_entries = [
            WeeklyEntry(week=date(2026, 1, i + 1), date_range=f"w{i}", depth=Depth.MAINTENANCE)
            for i in range(12)
        ]
        result = archive_weekly_entries(ledger, keep=8)
        assert len(result.weekly_entries) == 8
        # Most recent 8 kept
        assert result.weekly_entries[0].week == date(2026, 1, 5)
        assert result.weekly_entries[-1].week == date(2026, 1, 12)

    def test_archive_file_created(self, tmp_path):
        import src.monitor.ledger.storage as storage
        ledger = _test_country_ledger()
        ledger.weekly_entries = [
            WeeklyEntry(week=date(2026, 1, i + 1), date_range=f"w{i}", depth=Depth.MAINTENANCE)
            for i in range(10)
        ]
        archive_weekly_entries(ledger, keep=8)
        archives = list(storage.LEDGER_ARCHIVE_DIR.glob("mx_weeks_*.json"))
        assert len(archives) == 1


# ---- Global Ledger ----

class TestGlobalLedgerStorage:
    def test_init_and_load(self):
        assert not global_ledger_exists()
        ledger = init_global_ledger()
        assert global_ledger_exists()
        loaded = load_global_ledger()
        assert loaded.created == ledger.created

    def test_roundtrip(self):
        gl = GlobalLedger(
            last_updated=date(2026, 3, 14),
            created=date(2026, 3, 1),
            global_posture_summary=GlobalPostureSummary(
                as_of=date(2026, 3, 14),
                text="Test global posture.",
                signal_environment=SignalEnvironment(),
            ),
        )
        save_global_ledger(gl)
        loaded = load_global_ledger()
        assert loaded.global_posture_summary.text == "Test global posture."

    def test_load_missing_raises(self):
        with pytest.raises(FileNotFoundError):
            load_global_ledger()

"""Tests for source attribution validation."""

from datetime import date

from src.monitor.collection.extract import ExtractionResult
from src.monitor.config import Depth, SignalCategory
from src.monitor.models import (
    CategoryMovement,
    DevilsAdvocate,
    Development,
    Movement,
    SourceAttribution,
    WeeklyEntry,
)
from src.monitor.validation import (
    extract_proper_nouns,
    validate_source_attribution,
)


# =============================================================================
# extract_proper_nouns
# =============================================================================


class TestExtractProperNouns:
    def test_multi_word_names(self):
        text = "The talks were led by Rustem Umerov and Andrii Sybiha."
        entities = extract_proper_nouns(text)
        assert "rustem umerov" in entities
        assert "andrii sybiha" in entities

    def test_single_capitalized_mid_sentence(self):
        text = "The deployment near Kaliningrad raised concerns."
        entities = extract_proper_nouns(text)
        assert "kaliningrad" in entities

    def test_skips_sentence_starters(self):
        text = "Ukraine signed the deal. Poland welcomed the move."
        entities = extract_proper_nouns(text)
        # "Poland" starts second sentence — should be skipped
        assert "poland" not in entities

    def test_skips_stop_words(self):
        text = "The President met with the Foreign Minister."
        entities = extract_proper_nouns(text)
        assert "president" not in entities
        assert "foreign" not in entities

    def test_empty_text(self):
        assert extract_proper_nouns("") == set()
        assert extract_proper_nouns(None) == set()

    def test_multi_word_all_stop(self):
        text = "A meeting with Prime Minister yesterday."
        entities = extract_proper_nouns(text)
        assert "prime minister" not in entities

    def test_org_names(self):
        text = "Officials from Lockheed Martin confirmed the sale."
        entities = extract_proper_nouns(text)
        assert "lockheed martin" in entities

    def test_mixed_stop_and_real(self):
        text = "Officials from South Korea attended the summit."
        entities = extract_proper_nouns(text)
        assert "south korea" in entities


# =============================================================================
# validate_source_attribution
# =============================================================================


def _make_article(url: str, text: str, title: str = "") -> ExtractionResult:
    return ExtractionResult(
        url=url, method="curl", success=True, title=title, text=text,
    )


def _make_entry(developments: list[Development]) -> WeeklyEntry:
    movements = {c: CategoryMovement(movement=Movement.NONE) for c in SignalCategory}
    movements[SignalCategory.ALIGNMENT_DIPLOMATIC] = CategoryMovement(
        movement=Movement.SIGNIFICANT,
        developments=developments,
    )
    return WeeklyEntry(
        week=date(2026, 3, 14),
        date_range="2026-03-07 to 2026-03-14",
        depth=Depth.DEEP_DIVE,
        activity_level={"rating": "moderate", "rationale": "test"},
        category_movements=movements,
        devils_advocate=DevilsAdvocate(challenges=["test"]),
    )


class TestValidateSourceAttribution:
    def test_clean_when_entities_in_sources(self):
        articles = [
            _make_article(
                "https://reuters.com/1",
                "Defense Minister Rustem Umerov announced the new procurement deal.",
                title="Ukraine defense deal",
            ),
        ]
        dev = Development(
            headline="Ukraine defense procurement",
            date=date(2026, 3, 12),
            sources=[SourceAttribution(name="Reuters", url="https://reuters.com/1", tier=2)],
            summary="Rustem Umerov announced a new defense procurement deal.",
        )
        entry = _make_entry([dev])
        result = validate_source_attribution("ua", entry, articles)
        assert result.clean
        assert result.developments_checked == 1

    def test_flags_unattributed_entity(self):
        articles = [
            _make_article(
                "https://reuters.com/1",
                "The bilateral talks concluded on Tuesday.",
            ),
        ]
        dev = Development(
            headline="Trilateral defense talks",
            date=date(2026, 3, 12),
            sources=[SourceAttribution(name="Reuters", url="https://reuters.com/1", tier=2)],
            summary="Kyrylo Budanov led the trilateral defense discussions.",
        )
        entry = _make_entry([dev])
        result = validate_source_attribution("ua", entry, articles)
        assert not result.clean
        assert result.developments_flagged == 1
        assert "kyrylo budanov" in result.flags[0].unattributed_entities

    def test_entity_in_any_source_is_clean(self):
        articles = [
            _make_article("https://reuters.com/1", "The meeting was routine."),
            _make_article("https://bbc.com/1", "Andrii Sybiha discussed the framework."),
        ]
        dev = Development(
            headline="Framework talks",
            date=date(2026, 3, 12),
            sources=[
                SourceAttribution(name="Reuters", url="https://reuters.com/1", tier=2),
                SourceAttribution(name="BBC", url="https://bbc.com/1", tier=2),
            ],
            summary="Andrii Sybiha discussed the new framework.",
        )
        entry = _make_entry([dev])
        result = validate_source_attribution("ua", entry, articles)
        assert result.clean

    def test_skips_when_no_articles(self):
        dev = Development(
            headline="Something happened",
            date=date(2026, 3, 12),
            sources=[SourceAttribution(name="Reuters", url="https://reuters.com/1", tier=2)],
            summary="Important development occurred.",
        )
        entry = _make_entry([dev])
        result = validate_source_attribution("ua", entry, None)
        assert result.clean
        assert result.developments_checked == 0

    def test_skips_when_url_not_in_extraction_set(self):
        articles = [_make_article("https://other.com/1", "Unrelated article.")]
        dev = Development(
            headline="Important meeting",
            date=date(2026, 3, 12),
            sources=[SourceAttribution(name="Reuters", url="https://reuters.com/1", tier=2)],
            summary="Kyrylo Budanov attended the meeting.",
        )
        entry = _make_entry([dev])
        result = validate_source_attribution("ua", entry, articles)
        assert result.clean

    def test_severity_warning_for_multiple_unattributed(self):
        articles = [
            _make_article("https://reuters.com/1", "The talks concluded on schedule."),
        ]
        dev = Development(
            headline="Major diplomatic shift",
            date=date(2026, 3, 12),
            sources=[SourceAttribution(name="Reuters", url="https://reuters.com/1", tier=2)],
            summary="Kyrylo Budanov and Andrii Sybiha led discussions with NATO allies.",
        )
        entry = _make_entry([dev])
        result = validate_source_attribution("ua", entry, articles)
        assert not result.clean
        assert result.flags[0].severity == "warning"

    def test_no_category_movements(self):
        entry = WeeklyEntry(
            week=date(2026, 3, 14),
            date_range="2026-03-07 to 2026-03-14",
            depth=Depth.MAINTENANCE,
        )
        articles = [_make_article("https://reuters.com/1", "Some text.")]
        result = validate_source_attribution("ua", entry, articles)
        assert result.clean
        assert result.developments_checked == 0

    def test_development_without_source_urls_skipped(self):
        articles = [
            _make_article("https://reuters.com/1", "Some article text."),
        ]
        dev = Development(
            headline="Something",
            date=date(2026, 3, 12),
            sources=[SourceAttribution(name="Reuters", url="", tier=2)],
            summary="Kyrylo Budanov did a thing.",
        )
        entry = _make_entry([dev])
        result = validate_source_attribution("ua", entry, articles)
        # No URLs to check against, so no flags
        assert result.clean

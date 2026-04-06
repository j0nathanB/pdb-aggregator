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
    extract_entities,
    extract_figures,
    validate_source_attribution,
)


# =============================================================================
# extract_entities (spaCy NER)
# =============================================================================


class TestExtractEntities:
    def test_person_names(self):
        text = "The talks were led by Defense Minister Rustem Umerov and Andrii Sybiha."
        entities = extract_entities(text)
        assert "rustem umerov" in entities
        assert "andrii sybiha" in entities

    def test_gpe_mid_sentence(self):
        text = "The military deployment near Ankara raised concerns in Turkey."
        entities = extract_entities(text)
        assert "ankara" in entities

    def test_extracts_sentence_start_entities(self):
        """spaCy correctly extracts entities regardless of sentence position."""
        text = "Ukraine signed the deal. Poland welcomed the move."
        entities = extract_entities(text)
        assert "ukraine" in entities
        assert "poland" in entities

    def test_skips_generic_titles(self):
        text = "The President met with the Foreign Minister."
        entities = extract_entities(text)
        assert "president" not in entities
        assert "foreign minister" not in entities

    def test_empty_text(self):
        assert extract_entities("") == set()
        assert extract_entities(None) == set()

    def test_generic_title_not_entity(self):
        text = "A meeting with the Prime Minister yesterday."
        entities = extract_entities(text)
        assert "prime minister" not in entities

    def test_org_names(self):
        text = "Officials from Lockheed Martin confirmed the sale."
        entities = extract_entities(text)
        # Should detect the org (possibly as one or two tokens)
        assert any("lockheed" in e for e in entities)

    def test_country_names(self):
        text = "Officials from South Korea attended the summit."
        entities = extract_entities(text)
        assert "south korea" in entities

    def test_does_not_flag_political_vocabulary(self):
        """These were the top false positives with the old heuristic approach."""
        text = (
            "Finance officials met with the governor. "
            "The court ruled on the armed forces case."
        )
        entities = extract_entities(text)
        assert "finance" not in entities
        assert "governor" not in entities
        assert "court" not in entities
        assert "armed forces" not in entities

    def test_orgs_detected(self):
        text = "NATO and the SBU confirmed the intelligence sharing agreement."
        entities = extract_entities(text)
        assert "nato" in entities
        assert any("sbu" in e for e in entities)

    def test_facilities_detected(self):
        text = "The event was held at the Emirates Palace Hotel in Abu Dhabi."
        entities = extract_entities(text)
        assert any("emirates palace" in e for e in entities) or any("abu dhabi" in e for e in entities)


# =============================================================================
# extract_figures
# =============================================================================


class TestExtractFigures:
    def test_plain_integers(self):
        text = "Ukraine deployed 404 Shaheds and plans to reach 1,000 per day."
        figures = extract_figures(text)
        assert "404" in figures
        assert "1000" in figures

    def test_large_numbers_with_commas(self):
        text = "The goal is 50,000 deaths monthly, up from 35,000."
        figures = extract_figures(text)
        assert "50000" in figures
        assert "35000" in figures

    def test_decimals(self):
        text = "Inflation rose to 4.02% in March."
        figures = extract_figures(text)
        assert "4.02" in figures

    def test_currency_amounts(self):
        text = "The deal was worth $2.3 billion."
        figures = extract_figures(text)
        assert "2.3" in figures

    def test_skips_years(self):
        text = "In 2026, the country signed the deal from 1991."
        figures = extract_figures(text)
        assert "2026" not in figures
        assert "1991" not in figures

    def test_skips_trivial_numbers(self):
        text = "There were 3 meetings and 5 sessions."
        figures = extract_figures(text)
        assert "3" not in figures
        assert "5" not in figures

    def test_keeps_non_trivial_small_numbers(self):
        text = "Production dropped to 40 units from 87."
        figures = extract_figures(text)
        assert "40" in figures
        assert "87" in figures

    def test_area_measurements(self):
        text = "Ukrainian forces liberated 430 sq km near Pokrovsk."
        figures = extract_figures(text)
        assert "430" in figures

    def test_empty_text(self):
        assert extract_figures("") == set()
        assert extract_figures(None) == set()

    def test_mixed(self):
        text = "Fedorov announced 40,000 interceptor drones and 50,000 deaths monthly."
        figures = extract_figures(text)
        assert "40000" in figures
        assert "50000" in figures


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
        assert any("budanov" in e for e in result.flags[0].unattributed_entities)

    def test_entity_in_any_source_is_clean(self):
        articles = [
            _make_article("https://reuters.com/1", "The meeting was routine."),
            _make_article("https://bbc.com/1", "Foreign Minister Andrii Sybiha discussed the framework."),
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

    def test_flags_unattributed_figures(self):
        articles = [
            _make_article(
                "https://kyivpost.com/1",
                "Defense Minister outlined plans for drone-assault units.",
            ),
        ]
        dev = Development(
            headline="Ukraine drone warfare",
            date=date(2026, 3, 12),
            sources=[SourceAttribution(name="Kyiv Post", url="https://kyivpost.com/1", tier=2)],
            summary="Fedorov set a goal of 50,000 Russian deaths monthly, up from 35,000. "
                    "He announced 40,000 interceptor drones this month.",
        )
        entry = _make_entry([dev])
        result = validate_source_attribution("ua", entry, articles)
        assert not result.clean
        assert result.flags[0].unattributed_figures
        assert "50000" in result.flags[0].unattributed_figures
        assert "35000" in result.flags[0].unattributed_figures
        assert "40000" in result.flags[0].unattributed_figures

    def test_clean_when_figures_in_source(self):
        articles = [
            _make_article(
                "https://rbc.ua/1",
                "General Syrskyi reported Ukraine liberated 430 sq km near Pokrovsk.",
            ),
        ]
        dev = Development(
            headline="Counteroffensive advances",
            date=date(2026, 3, 12),
            sources=[SourceAttribution(name="RBC Ukraine", url="https://rbc.ua/1", tier=2)],
            summary="Ukraine retook 430 sq km near Pokrovsk.",
        )
        entry = _make_entry([dev])
        result = validate_source_attribution("ua", entry, articles)
        assert result.clean

    def test_severity_escalates_with_figures_and_entities(self):
        articles = [
            _make_article("https://reuters.com/1", "The meeting concluded."),
        ]
        dev = Development(
            headline="Defense developments",
            date=date(2026, 3, 12),
            sources=[SourceAttribution(name="Reuters", url="https://reuters.com/1", tier=2)],
            summary="Kyrylo Budanov announced Ukraine intercepted 404 drones daily.",
        )
        entry = _make_entry([dev])
        result = validate_source_attribution("ua", entry, articles)
        assert not result.clean
        # Entity (Budanov/Ukraine) + figure (404) = 2+ total → warning severity
        assert result.flags[0].severity == "warning"

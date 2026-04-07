"""Tests for sanitize_narrative_body — strips known editor LLM artifacts."""

from src.monitor.newsletter.structured_editor import sanitize_narrative_body
from src.monitor.sanitize import get_fallback_summary, reset_fallback_counts


# =============================================================================
# Empty / no-op cases
# =============================================================================


def test_empty_string_returns_empty():
    assert sanitize_narrative_body("") == ""


def test_none_returns_none():
    assert sanitize_narrative_body(None) is None


def test_clean_prose_unchanged():
    text = (
        "Pakistan picked fights with its biggest allies this week.\n\n"
        "Even as it clashes with traditional partners, it builds new ones."
    )
    assert sanitize_narrative_body(text) == text


# =============================================================================
# Accordion stripping
# =============================================================================


def test_strips_single_accordion_block():
    text = (
        "First paragraph of prose.\n\n"
        '<Accordion title="Other stories">\n'
        "- **Story one** — summary one\n"
        "- **Story two** — summary two\n"
        "</Accordion>"
    )
    result = sanitize_narrative_body(text)
    assert "First paragraph of prose." in result
    assert "<Accordion" not in result
    assert "</Accordion>" not in result
    assert "Story one" not in result


def test_strips_multiple_accordion_blocks():
    text = (
        "Prose paragraph.\n\n"
        '<Accordion title="Other stories">First</Accordion>\n\n'
        "Another paragraph.\n\n"
        '<Accordion title="Notes">Second</Accordion>'
    )
    result = sanitize_narrative_body(text)
    assert "Prose paragraph." in result
    assert "Another paragraph." in result
    assert "<Accordion" not in result
    assert "First" not in result
    assert "Second" not in result


def test_strips_accordion_case_insensitive():
    text = (
        "Prose.\n\n"
        '<accordion title="Other developments">stuff</accordion>'
    )
    result = sanitize_narrative_body(text)
    assert "<accordion" not in result.lower()


def test_strips_multiline_accordion():
    text = (
        "Lead paragraph.\n\n"
        '<Accordion title="Other stories">\n'
        "\n"
        "**Headline one**\n"
        "Summary line one.\n"
        "\n"
        "**Headline two**\n"
        "Summary line two.\n"
        "\n"
        "</Accordion>"
    )
    result = sanitize_narrative_body(text)
    assert result == "Lead paragraph."


# =============================================================================
# Leading heading stripping
# =============================================================================


def test_strips_leading_h3_heading():
    text = "### Pakistan\n\nPakistan picked fights with its biggest allies."
    result = sanitize_narrative_body(text)
    assert result.startswith("Pakistan picked fights")
    assert "### " not in result


def test_strips_leading_heading_with_whitespace():
    text = "\n\n### Ukraine\n\n\nUkraine clashed with allies."
    result = sanitize_narrative_body(text)
    assert result.startswith("Ukraine clashed")


def test_strips_mid_paragraph_heading():
    # Editor prompts prohibit headings; any `### ` line anywhere is an artifact
    text = "Opening paragraph.\n\n### Mid paragraph\n\nMore prose."
    result = sanitize_narrative_body(text)
    assert "### Mid paragraph" not in result
    assert "Opening paragraph." in result
    assert "More prose." in result


def test_strips_multiple_category_headings_poland_case():
    """Reproduces the Poland 2026-03-29 case: signal-category sub-headings."""
    text = (
        "Poland's institutional warfare has intensified.\n\n"
        "### Economic\n\n"
        "Fuel prices surged this week.\n\n"
        "### Institutional\n\n"
        "Constitutional restoration enters a new phase.\n\n"
        "### Diplomatic\n\n"
        "Tusk and Nawrocki split.\n\n"
        "### Security\n\n"
        "Defence modernisation continued.\n\n"
        "### Domestic\n\n"
        "PiS leadership reshuffled."
    )
    result = sanitize_narrative_body(text, label="test_pl")
    assert "### " not in result
    assert "Poland's institutional warfare" in result
    assert "Fuel prices" in result
    assert "Constitutional restoration" in result
    assert "Tusk and Nawrocki split" in result


def test_strips_h4_headings_too():
    text = "Opening.\n\n#### Subsection heading\n\nMore prose."
    result = sanitize_narrative_body(text)
    assert "#### Subsection heading" not in result


def test_strips_activity_level_with_value_inside_bold():
    """Variant where the value is inside the bold markers, not after."""
    text = "Lead paragraph.\n\n**Activity Level: High**\n\nBody paragraph."
    result = sanitize_narrative_body(text)
    assert "Activity Level" not in result
    assert "Lead paragraph" in result
    assert "Body paragraph" in result


# =============================================================================
# Activity Level marker stripping
# =============================================================================


def test_strips_activity_level_marker():
    text = (
        "Lead paragraph.\n\n"
        "**Activity Level:** High\n\n"
        "Body paragraph."
    )
    result = sanitize_narrative_body(text)
    assert "Activity Level" not in result
    assert "Lead paragraph" in result
    assert "Body paragraph" in result


def test_strips_activity_level_without_colon():
    text = (
        "Lead.\n\n"
        "**Activity Level** High\n\n"
        "Body."
    )
    result = sanitize_narrative_body(text)
    assert "Activity Level" not in result


def test_does_not_strip_natural_language_activity():
    # The literal markdown bold marker is required
    text = "The activity level was high in Ukraine this week."
    result = sanitize_narrative_body(text)
    assert "activity level" in result


# =============================================================================
# Combined / real-world cases
# =============================================================================


def test_strips_all_three_artifacts_ukraine_case():
    """Reproduces the Ukraine 2026-03-15 case: heading + marker + accordion."""
    text = (
        "### Ukraine\n\n"
        "Ukraine picked fights with its biggest allies this week.\n\n"
        "**Activity Level:** High\n\n"
        "Ukraine is clashing with its biggest allies. Zelensky condemned "
        "the US Treasury's 30-day waiver on Russian oil sanctions.\n\n"
        "<Accordion title=\"Other stories\">\n"
        "**Story one**  \n"
        "Summary one.\n\n"
        "**Story two**  \n"
        "Summary two.\n"
        "</Accordion>"
    )
    result = sanitize_narrative_body(text, label="test_ukraine")
    assert result.startswith("Ukraine picked fights")
    assert "### Ukraine" not in result
    assert "Activity Level" not in result
    assert "<Accordion" not in result
    assert "Story one" not in result
    assert "Zelensky condemned" in result


def test_logs_and_records_fallback_when_stripping():
    reset_fallback_counts()
    text = "### Pakistan\n\nPakistan picked fights."
    sanitize_narrative_body(text, label="test_pk")
    summary = get_fallback_summary()
    assert summary.get("narrative_sanitized", 0) == 1


def test_does_not_record_fallback_when_clean():
    reset_fallback_counts()
    text = "Pakistan picked fights with its biggest allies this week."
    sanitize_narrative_body(text, label="test_pk")
    summary = get_fallback_summary()
    assert summary.get("narrative_sanitized", 0) == 0

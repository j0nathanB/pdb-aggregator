"""Tests for copyeditor agent: prompt building and newsletter splitting."""

from src.monitor.agents.copyeditor import (
    EditableSection,
    build_copyeditor_prompt,
    _is_boilerplate,
    _split_newsletter_sections,
)


# ---- Prompt Building ----

class TestBuildCopyeditorPrompt:
    def test_includes_section(self):
        prompt = build_copyeditor_prompt("### Mexico\n\nSome analysis.", "country")
        assert "### Mexico" in prompt
        assert "Some analysis." in prompt

    def test_includes_type_hint_country(self):
        prompt = build_copyeditor_prompt("test", "country")
        assert "country section" in prompt

    def test_includes_type_hint_executive(self):
        prompt = build_copyeditor_prompt("test", "executive")
        assert "executive brief" in prompt

    def test_includes_type_hint_regional(self):
        prompt = build_copyeditor_prompt("test", "regional")
        assert "regional analysis" in prompt


# ---- Boilerplate Detection ----

class TestIsBoilerplate:
    def test_empty_is_boilerplate(self):
        assert _is_boilerplate("")
        assert _is_boilerplate("   ")

    def test_short_is_boilerplate(self):
        assert _is_boilerplate("Too short.")

    def test_no_dynamics_is_boilerplate(self):
        assert _is_boilerplate(
            "No significant cross-country dynamics emerged in The Americas this week."
        )

    def test_no_system_dynamics_is_boilerplate(self):
        assert _is_boilerplate(
            "*No system-level dynamics met the threshold for executive-level analysis.*"
        )

    def test_real_content_is_not_boilerplate(self):
        assert not _is_boilerplate(
            "Mexico faces increased coalition management challenges as Sheinbaum's "
            "first major legislative defeat on electoral reform demonstrates that "
            "formal supermajorities don't guarantee coalition discipline."
        )


# ---- Newsletter Splitting ----

SAMPLE_NEWSLETTER = (
    "# The Middle Powers Monitor\n"
    "## Week of March 10 to March 16, 2026\n\n"
    "*Covering 28 countries.*\n\n"
    "### Americas pushback crystallizes\n\n"
    "Several Latin American states pushed back against US tariff proposals.\n\n"
    "*High confidence. Based on multiple diplomatic sources.*\n\n"
    "---\n\n"
    "## The Americas\n\n"
    "Brazil and Mexico coordinated responses to new US trade measures, "
    "signalling a shift toward collective bargaining. Chile joined the bloc "
    "after its copper exports were targeted, broadening the coalition beyond "
    "the traditional Mercosur alignment.\n\n"
    "### Mexico\n\n"
    "Mexico faces challenges. Sheinbaum's reform failed.\n\n"
    "**Key developments:**\n\n"
    "- **Domestic:** Reform rejected. *([La Jornada](https://jornada.com), 2026-03-11)*\n\n"
    "### Brazil\n\n"
    "Brazil navigates trade tensions with pragmatic engagement.\n\n"
    "---\n\n"
    "## Watchlist\n\n"
    "- **Pipeline restoration** (ALL): Ongoing.\n\n"
    "---\n\n"
    "*Footer text.*"
)

BOILERPLATE_NEWSLETTER = (
    "# The Middle Powers Monitor\n"
    "## Week of March 10 to March 16, 2026\n\n"
    "*No system-level dynamics met the threshold for executive-level analysis.*\n\n"
    "---\n\n"
    "## The Americas\n\n"
    "No significant cross-country dynamics emerged in The Americas this week. "
    "Country-level developments are covered below.\n\n"
    "### Mexico\n\n"
    "Mexico faces challenges.\n\n"
    "---\n\n"
    "*Footer.*"
)


class TestSplitNewsletterSections:
    def test_finds_country_sections(self):
        segments = _split_newsletter_sections(SAMPLE_NEWSLETTER)
        countries = [s for _, s in segments if s and s.section_type == "country"]
        names = [s.label for s in countries]
        assert "Mexico" in names
        assert "Brazil" in names

    def test_finds_executive_brief(self):
        segments = _split_newsletter_sections(SAMPLE_NEWSLETTER)
        executive = [s for _, s in segments if s and s.section_type == "executive"]
        assert len(executive) == 1
        assert "Americas pushback" in executive[0].label

    def test_finds_regional_analysis(self):
        segments = _split_newsletter_sections(SAMPLE_NEWSLETTER)
        regional = [s for _, s in segments if s and s.section_type == "regional"]
        assert len(regional) == 1
        assert regional[0].label == "The Americas"
        assert "collective bargaining" in regional[0].text

    def test_skips_boilerplate_regional(self):
        segments = _split_newsletter_sections(BOILERPLATE_NEWSLETTER)
        regional = [s for _, s in segments if s and s.section_type == "regional"]
        assert len(regional) == 0

    def test_skips_watchlist(self):
        segments = _split_newsletter_sections(SAMPLE_NEWSLETTER)
        all_sections = [s for _, s in segments if s is not None]
        labels = [s.label for s in all_sections]
        assert not any("Watchlist" in l for l in labels)

    def test_reassembly_preserves_content(self):
        segments = _split_newsletter_sections(SAMPLE_NEWSLETTER)
        reassembled = "".join(text for text, _ in segments)
        assert reassembled == SAMPLE_NEWSLETTER

    def test_reassembly_preserves_boilerplate(self):
        segments = _split_newsletter_sections(BOILERPLATE_NEWSLETTER)
        reassembled = "".join(text for text, _ in segments)
        assert reassembled == BOILERPLATE_NEWSLETTER

    def test_country_section_includes_developments(self):
        segments = _split_newsletter_sections(SAMPLE_NEWSLETTER)
        mexico = next(s for _, s in segments if s and s.label == "Mexico")
        assert "Key developments" in mexico.text
        assert "La Jornada" in mexico.text

    def test_no_editable_sections_in_empty_newsletter(self):
        segments = _split_newsletter_sections("# Just a header\n\nSome text.")
        editable = [s for _, s in segments if s is not None]
        assert len(editable) == 0

"""Tests for story map agent: prompt building, response parsing, output properties."""

import json
from datetime import date

import pytest
from src.monitor.config import load_country_config
from src.monitor.agents.story_map import (
    StoryCluster,
    StoryMapOutput,
    SingleSourceItem,
    UnassignedItem,
    build_story_map_prompt,
    parse_story_map_response,
)
from src.monitor.agents.expansion import ExpansionResult
from src.monitor.collection.brave import BraveNewsResult


# ---- Helpers ----

def _mexico_config():
    return load_country_config("mx")


def _make_brave_result(title, url, domain="test.com", desc="snippet", age="1d"):
    return BraveNewsResult(
        title=title, url=url, description=desc,
        source_domain=domain, age=age,
    )


def _sample_expansion():
    return ExpansionResult(
        code="mx", country="Mexico",
        triage_wire=[
            _make_brave_result("Sheinbaum rejects US proposal", "https://reuters.com/1", "reuters.com"),
            _make_brave_result("Mexico trade talks stall", "https://apnews.com/2", "apnews.com"),
        ],
        triage_domestic=[
            _make_brave_result("Reforma: SEDENA expands ops", "https://reforma.com/1", "reforma.com"),
            _make_brave_result("Sheinbaum rechaza propuesta", "https://eluniversal.com.mx/1", "eluniversal.com.mx"),
        ],
        actor_results=[
            _make_brave_result("Banxico holds rate", "https://elfinanciero.com/1", "elfinanciero.com"),
            _make_brave_result("SEDENA contract award", "https://proceso.com.mx/1", "proceso.com.mx"),
        ],
        vocab_results=[
            _make_brave_result("Nearshoring boom continues", "https://expansion.mx/1", "expansion.mx"),
        ],
    )


VALID_RESPONSE = json.dumps({
    "country": "MX",
    "analysis_date": "2026-03-14",
    "search_results_total": 237,
    "stories_identified": 3,
    "off_topic_filtered": 12,
    "stories": [
        {
            "story_id": 1,
            "headline": "Sheinbaum rejects US military cooperation proposal",
            "summary": "President rejected joint military ops proposal.",
            "actors_involved": ["Sheinbaum", "SRE"],
            "signal_category_hint": "alignment_diplomatic",
            "source_count": 5,
            "sources": ["reuters.com", "eluniversal.com.mx", "reforma.com", "apnews.com", "proceso.com.mx"],
            "date_range": "2026-03-10 to 2026-03-12",
            "representative_urls": ["https://reuters.com/1", "https://eluniversal.com.mx/1"],
        },
        {
            "story_id": 2,
            "headline": "Banxico holds interest rate amid inflation concerns",
            "summary": "Central bank held rate steady at 9.5%.",
            "actors_involved": ["Banxico"],
            "signal_category_hint": "economic_tech",
            "source_count": 3,
            "sources": ["elfinanciero.com", "reforma.com", "expansion.mx"],
            "date_range": "2026-03-11",
            "representative_urls": ["https://elfinanciero.com/1"],
        },
        {
            "story_id": 3,
            "headline": "SEDENA expands border operations in northern states",
            "summary": "Military expanded presence in Sonora and Chihuahua.",
            "actors_involved": ["SEDENA"],
            "signal_category_hint": "security_defense",
            "source_count": 2,
            "sources": ["reforma.com", "proceso.com.mx"],
            "date_range": "2026-03-13",
            "representative_urls": ["https://reforma.com/1", "https://proceso.com.mx/1"],
        },
    ],
    "single_source_items": [
        {
            "headline": "SEDENA helicopter maintenance contract awarded",
            "source": "animalpolitico.com",
            "url": "https://animalpolitico.com/1",
            "signal_category_hint": "security_defense",
        },
    ],
    "noise_summary": "12 off-topic: 5 sports, 4 entertainment, 3 lifestyle.",
    "unassigned": [
        {
            "url": "https://example.com/orphan",
            "description": "An article that didn't fit any cluster",
            "extra_snippets": ["Additional context"],
        },
    ],
})


# ---- Prompt Building ----

class TestBuildStoryMapPrompt:
    def test_includes_country(self):
        config = _mexico_config()
        expansion = _sample_expansion()
        prompt, _ = build_story_map_prompt(config, expansion, date(2026, 3, 14))
        assert "Mexico" in prompt
        assert "MX" in prompt

    def test_includes_actors(self):
        config = _mexico_config()
        expansion = _sample_expansion()
        prompt, _ = build_story_map_prompt(config, expansion, date(2026, 3, 14))
        assert "Sheinbaum" in prompt
        assert "SEDENA" in prompt
        assert "Banxico" in prompt

    def test_includes_search_results(self):
        config = _mexico_config()
        expansion = _sample_expansion()
        prompt, _ = build_story_map_prompt(config, expansion, date(2026, 3, 14))
        assert "reuters.com" in prompt
        assert "Sheinbaum rejects US proposal" in prompt
        assert "Nearshoring boom" in prompt

    def test_labels_result_sources(self):
        config = _mexico_config()
        expansion = _sample_expansion()
        prompt, _ = build_story_map_prompt(config, expansion, date(2026, 3, 14))
        assert "[wire]" in prompt
        assert "[domestic]" in prompt
        assert "[actor]" in prompt
        assert "[vocab]" in prompt

    def test_includes_urls(self):
        config = _mexico_config()
        expansion = _sample_expansion()
        prompt, _ = build_story_map_prompt(config, expansion, date(2026, 3, 14))
        assert "https://reuters.com/1" in prompt

    def test_deduplicates_results(self):
        """Same URL from different sources should appear only once."""
        expansion = ExpansionResult(
            code="mx", country="Mexico",
            triage_wire=[_make_brave_result("Title A", "https://same.com/1", "same.com")],
            actor_results=[_make_brave_result("Title B", "https://same.com/1", "same.com")],
        )
        config = _mexico_config()
        prompt, _ = build_story_map_prompt(config, expansion, date(2026, 3, 14))
        assert prompt.count("https://same.com/1") == 1

    def test_dedup_record_tracks_overlap(self):
        """Dedup record should report duplicates removed at format stage."""
        expansion = ExpansionResult(
            code="mx", country="Mexico",
            triage_wire=[_make_brave_result("Title A", "https://same.com/1", "same.com")],
            actor_results=[
                _make_brave_result("Title B", "https://same.com/1", "same.com"),
                _make_brave_result("Title C", "https://other.com/2", "other.com"),
            ],
        )
        config = _mexico_config()
        _, dedup = build_story_map_prompt(config, expansion, date(2026, 3, 14))
        assert dedup["raw_input"] == 3
        assert dedup["unique_in_prompt"] == 2
        assert dedup["deduped_at_format"] == 1
        assert dedup["per_source"]["wire"]["included"] == 1
        assert dedup["per_source"]["actor"]["deduped_at_format"] == 1

    def test_includes_date(self):
        config = _mexico_config()
        expansion = _sample_expansion()
        prompt, _ = build_story_map_prompt(config, expansion, date(2026, 3, 14))
        assert "2026-03-14" in prompt


# ---- Response Parsing ----

class TestParseStoryMapResponse:
    def test_parses_valid_response(self):
        output = parse_story_map_response(VALID_RESPONSE)
        assert output.stories_identified == 3
        assert len(output.stories) == 3

    def test_parses_story_fields(self):
        output = parse_story_map_response(VALID_RESPONSE)
        s1 = output.stories[0]
        assert s1.story_id == 1
        assert "Sheinbaum" in s1.headline
        assert s1.source_count == 5
        assert "reuters.com" in s1.sources
        assert s1.signal_category_hint == "alignment_diplomatic"
        assert len(s1.representative_urls) == 2

    def test_parses_single_source_items(self):
        output = parse_story_map_response(VALID_RESPONSE)
        assert len(output.single_source_items) == 1
        assert output.single_source_items[0].source == "animalpolitico.com"

    def test_parses_unassigned(self):
        output = parse_story_map_response(VALID_RESPONSE)
        assert len(output.unassigned) == 1
        assert output.unassigned[0].url == "https://example.com/orphan"
        assert "didn't fit" in output.unassigned[0].description
        assert output.unassigned[0].extra_snippets == ["Additional context"]

    def test_parses_noise_summary(self):
        output = parse_story_map_response(VALID_RESPONSE)
        assert "12 off-topic" in output.noise_summary

    def test_strips_markdown_fencing(self):
        fenced = f"```json\n{VALID_RESPONSE}\n```"
        output = parse_story_map_response(fenced)
        assert len(output.stories) == 3

    def test_invalid_json_raises(self):
        with pytest.raises(json.JSONDecodeError):
            parse_story_map_response("not json at all")

    def test_empty_stories_ok(self):
        data = json.dumps({
            "country": "MX",
            "analysis_date": "2026-03-14",
            "search_results_total": 5,
            "stories_identified": 0,
            "off_topic_filtered": 5,
            "stories": [],
            "single_source_items": [],
            "noise_summary": "All off-topic.",
        })
        output = parse_story_map_response(data)
        assert output.stories_identified == 0
        assert output.stories == []

    def test_missing_optional_fields(self):
        """Minimal response with just stories should parse."""
        data = json.dumps({
            "stories": [{
                "story_id": 1,
                "headline": "Test",
                "summary": "Test story.",
                "source_count": 2,
                "sources": ["a.com", "b.com"],
                "representative_urls": ["https://a.com/1"],
            }],
        })
        output = parse_story_map_response(data)
        assert len(output.stories) == 1
        assert output.stories[0].signal_category_hint == "unclear"


# ---- StoryMapOutput Properties ----

class TestStoryMapOutput:
    def test_all_representative_urls(self):
        output = StoryMapOutput(
            country="Mexico", code="mx",
            analysis_date="2026-03-14",
            search_results_total=100,
            stories_identified=2,
            off_topic_filtered=10,
            stories=[
                StoryCluster(story_id=1, headline="A", summary="A",
                             representative_urls=["https://a.com/1", "https://b.com/1"]),
                StoryCluster(story_id=2, headline="B", summary="B",
                             representative_urls=["https://c.com/1", "https://a.com/1"]),  # dup
            ],
            single_source_items=[
                SingleSourceItem(headline="C", source="d.com", url="https://d.com/1"),
            ],
        )
        urls = output.all_representative_urls
        assert len(urls) == 4  # a, b, c, d — deduped
        assert urls[0] == "https://a.com/1"  # order preserved

    def test_extraction_url_count(self):
        output = StoryMapOutput(
            country="Mexico", code="mx",
            analysis_date="2026-03-14",
            search_results_total=50,
            stories_identified=1,
            off_topic_filtered=0,
            stories=[
                StoryCluster(story_id=1, headline="A", summary="A",
                             representative_urls=["https://a.com/1"]),
            ],
        )
        assert output.extraction_url_count == 1

    def test_empty_output(self):
        output = StoryMapOutput(
            country="Mexico", code="mx",
            analysis_date="2026-03-14",
            search_results_total=0,
            stories_identified=0,
            off_topic_filtered=0,
        )
        assert output.all_representative_urls == []
        assert output.extraction_url_count == 0

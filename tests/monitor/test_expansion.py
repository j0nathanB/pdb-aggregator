"""Tests for deep-dive search expansion: query building and result merging."""

import json
from datetime import date

import pytest
from src.monitor.config import load_country_config
from src.monitor.agents.expansion import (
    ExpansionResult,
    _build_actor_queries,
    _build_vocab_queries,
    expand_country,
)
from src.monitor.agents.triage import ScanResult
from src.monitor.collection.brave import BraveNewsClient, BraveNewsResult


# ---- Helpers ----

def _mexico_config():
    return load_country_config("mx")


def _make_brave_result(title: str, url: str, domain: str = "test.com") -> BraveNewsResult:
    return BraveNewsResult(
        title=title, url=url, description="", source_domain=domain,
    )


# ---- Actor Query Building ----

class TestBuildActorQueries:
    def test_excludes_primary_when_triage_available(self):
        config = _mexico_config()
        queries = _build_actor_queries(config, has_triage=True)
        primary_terms = []
        for a in config.actors:
            if a.primary:
                primary_terms.extend(a.search_terms)
        for q in queries:
            for term in primary_terms:
                assert term not in q, f"Primary actor term {term!r} found in expansion query {q!r}"

    def test_includes_primary_when_no_triage(self):
        config = _mexico_config()
        queries_with = _build_actor_queries(config, has_triage=True)
        queries_without = _build_actor_queries(config, has_triage=False)
        assert len(queries_without) == len(queries_with) + 1
        # Primary actor's first search term should be in queries
        primary = next(a for a in config.actors if a.primary)
        assert primary.search_terms[0] in queries_without

    def test_includes_non_primary_actors(self):
        config = _mexico_config()
        queries = _build_actor_queries(config, has_triage=True)
        non_primary_with_terms = [
            a for a in config.actors if not a.primary and a.search_terms
        ]
        assert len(queries) == len(non_primary_with_terms)

    def test_uses_first_search_term(self):
        config = _mexico_config()
        queries = _build_actor_queries(config)
        assert "SEDENA" in queries

    def test_empty_if_only_primary_with_triage(self):
        """If all actors are primary and triage ran, no expansion queries."""
        config = _mexico_config()
        for a in config.actors:
            a.primary = True
        queries = _build_actor_queries(config, has_triage=True)
        assert queries == []


# ---- Vocab Query Building ----

class TestBuildVocabQueries:
    def test_one_query_per_category(self):
        config = _mexico_config()
        queries = _build_vocab_queries(config)
        # Mexico has all 5 vocab categories populated
        assert len(queries) == 5

    def test_queries_use_quoted_terms(self):
        config = _mexico_config()
        queries = _build_vocab_queries(config)
        # Each query should have quoted terms joined with OR
        for q in queries:
            assert '"' in q
            assert "OR" in q or q.count('"') == 2  # single-term categories have no OR

    def test_empty_vocab_skipped(self):
        config = _mexico_config()
        config.news_discovery.query_vocabulary.institutional = []
        queries = _build_vocab_queries(config)
        assert len(queries) == 4  # one fewer


# ---- ExpansionResult ----

class TestExpansionResult:
    def test_deduplicates_by_url(self):
        result = ExpansionResult(
            code="mx", country="Mexico",
            triage_wire=[_make_brave_result("Wire A", "https://reuters.com/a", "reuters.com")],
            triage_domestic=[_make_brave_result("Domestic A", "https://reforma.com/a", "reforma.com")],
            actor_results=[
                _make_brave_result("Wire A dup", "https://reuters.com/a", "reuters.com"),  # duplicate URL
                _make_brave_result("Actor B", "https://proceso.com/b", "proceso.com"),
            ],
        )
        all_r = result.all_results
        urls = [r.url for r in all_r]
        assert len(urls) == len(set(urls))
        assert len(all_r) == 3  # reuters/a, reforma/a, proceso/b

    def test_total_count(self):
        result = ExpansionResult(
            code="mx", country="Mexico",
            triage_wire=[_make_brave_result("A", "https://a.com/1")],
            actor_results=[_make_brave_result("B", "https://b.com/1")],
        )
        assert result.total_count == 2

    def test_source_counts(self):
        result = ExpansionResult(
            code="mx", country="Mexico",
            triage_wire=[_make_brave_result("A", "https://a.com/1")],
            triage_domestic=[
                _make_brave_result("B", "https://b.com/1"),
                _make_brave_result("C", "https://c.com/1"),
            ],
            actor_results=[_make_brave_result("D", "https://d.com/1")],
            vocab_results=[],
        )
        counts = result.source_counts
        assert counts["triage_wire"] == 1
        assert counts["triage_domestic"] == 2
        assert counts["actor"] == 1
        assert counts["vocab"] == 0

    def test_empty_result(self):
        result = ExpansionResult(code="mx", country="Mexico")
        assert result.all_results == []
        assert result.total_count == 0

    def test_dedup_record(self):
        result = ExpansionResult(
            code="mx", country="Mexico",
            triage_wire=[_make_brave_result("Wire A", "https://reuters.com/a", "reuters.com")],
            triage_domestic=[_make_brave_result("Domestic A", "https://reforma.com/a", "reforma.com")],
            actor_results=[
                _make_brave_result("Wire A dup", "https://reuters.com/a", "reuters.com"),
                _make_brave_result("Actor B", "https://proceso.com/b", "proceso.com"),
            ],
        )
        rec = result.dedup_record
        assert rec["raw_total"] == 4
        assert rec["unique_urls"] == 3
        assert rec["duplicates_removed"] == 1
        assert rec["urls_found_by_multiple_sources"] == 1
        assert "https://reuters.com/a" in rec["duplicate_urls"]
        dup = rec["duplicate_urls"]["https://reuters.com/a"]
        assert dup["count"] == 2
        assert "triage_wire" in dup["found_in"]
        assert "actor" in dup["found_in"]

    def test_dedup_record_no_duplicates(self):
        result = ExpansionResult(
            code="mx", country="Mexico",
            triage_wire=[_make_brave_result("A", "https://a.com/1")],
            actor_results=[_make_brave_result("B", "https://b.com/1")],
        )
        rec = result.dedup_record
        assert rec["duplicates_removed"] == 0
        assert rec["urls_found_by_multiple_sources"] == 0
        assert rec["duplicate_urls"] == {}


# ---- Expansion with mocked Brave ----

class TestExpandCountry:
    @pytest.mark.asyncio
    async def test_forwards_triage_results(self):
        """Triage wire/domestic results are included in expansion output."""
        from unittest.mock import AsyncMock, MagicMock
        from src.monitor.collection.brave import BraveSearchResponse

        config = _mexico_config()
        mock_client = AsyncMock(spec=BraveNewsClient)

        # Mock country_configs for goggle lookup
        mock_cc = MagicMock()
        mock_cc.goggle_url.return_value = None
        mock_client.country_configs = {"mx": mock_cc}

        # Mock search_news to return empty results
        mock_client.search_news = AsyncMock(
            return_value=BraveSearchResponse(query="test", results=[], total_count=0)
        )

        triage_scan = ScanResult(
            code="mx", country="Mexico",
            wire_results=[_make_brave_result("Wire", "https://reuters.com/1", "reuters.com")],
            domestic_results=[_make_brave_result("Dom", "https://reforma.com/1", "reforma.com")],
        )

        result = await expand_country(config, mock_client, triage_scan, date(2026, 3, 14))

        assert len(result.triage_wire) == 1
        assert len(result.triage_domestic) == 1
        assert result.triage_wire[0].url == "https://reuters.com/1"

    @pytest.mark.asyncio
    async def test_runs_actor_and_vocab_queries(self):
        """Expansion runs the expected number of Brave queries."""
        from unittest.mock import AsyncMock, MagicMock
        from src.monitor.collection.brave import BraveSearchResponse

        config = _mexico_config()
        mock_client = AsyncMock(spec=BraveNewsClient)

        mock_cc = MagicMock()
        mock_cc.goggle_url.return_value = "https://example.com/mx.goggle"
        mock_client.country_configs = {"mx": mock_cc}

        mock_client.search_news = AsyncMock(
            return_value=BraveSearchResponse(
                query="test",
                results=[_make_brave_result("Result", "https://test.com/1")],
                total_count=1,
            )
        )

        result = await expand_country(config, mock_client, end_date=date(2026, 3, 14))

        # No triage_scan → primary actor gets a query too (all actors + vocab)
        actors_with_terms = [a for a in config.actors if a.search_terms]
        vocab_categories = 5  # Mexico has all 5
        expected_queries = len(actors_with_terms) + vocab_categories
        assert mock_client.search_news.call_count == expected_queries
        assert len(result.queries_run) == expected_queries

    @pytest.mark.asyncio
    async def test_handles_query_failure(self):
        """A failed query doesn't crash expansion — other queries still run."""
        from unittest.mock import AsyncMock, MagicMock
        from src.monitor.collection.brave import BraveSearchResponse

        config = _mexico_config()
        mock_client = AsyncMock(spec=BraveNewsClient)

        mock_cc = MagicMock()
        mock_cc.goggle_url.return_value = None
        mock_client.country_configs = {"mx": mock_cc}

        call_count = 0
        async def _mock_search(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise Exception("API timeout")
            return BraveSearchResponse(query="test", results=[], total_count=0)

        mock_client.search_news = _mock_search

        result = await expand_country(config, mock_client, end_date=date(2026, 3, 14))

        # Should still complete without error
        assert result.code == "mx"
        # One query failed but the rest ran
        assert call_count > 1

    @pytest.mark.asyncio
    async def test_no_queries_if_no_actors_or_vocab(self):
        """Country with all-primary actors + triage + no vocab produces no queries."""
        from unittest.mock import AsyncMock, MagicMock

        config = _mexico_config()
        # Make all actors primary
        for a in config.actors:
            a.primary = True
        # Clear vocab
        config.news_discovery.query_vocabulary.diplomatic_alignment = []
        config.news_discovery.query_vocabulary.security_defense = []
        config.news_discovery.query_vocabulary.economic_tech = []
        config.news_discovery.query_vocabulary.institutional = []
        config.news_discovery.query_vocabulary.domestic_constraints = []

        mock_client = AsyncMock(spec=BraveNewsClient)
        mock_cc = MagicMock()
        mock_cc.goggle_url.return_value = None
        mock_client.country_configs = {"mx": mock_cc}

        # Provide triage scan so primary actors are skipped
        triage_scan = ScanResult(code="mx", country="Mexico")
        result = await expand_country(
            config, mock_client, triage_scan=triage_scan, end_date=date(2026, 3, 14),
        )

        assert result.queries_run == []
        mock_client.search_news.assert_not_called()

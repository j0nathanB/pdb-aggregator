"""Tests for CountryConfig and GovernmentDomainConfig loading and validation."""

import pytest
from src.monitor.config import (
    Actor,
    BraveParams,
    CountryConfig,
    GovernmentDiscovery,
    GovernmentDomain,
    GovernmentDomainConfig,
    Languages,
    NewsDiscovery,
    QueryVocabulary,
    Region,
    SearchBudget,
    Tier,
    load_country_config,
    load_government_config,
)


class TestCountryConfig:
    def test_load_mexico(self):
        cfg = load_country_config("mx")
        assert cfg.country == "Mexico"
        assert cfg.code == "mx"
        assert cfg.tier == Tier.PERIPHERY
        assert cfg.region == Region.AMERICAS

    def test_actors(self):
        cfg = load_country_config("mx")
        assert len(cfg.actors) >= 7
        assert cfg.primary_actors[0].name == "Claudia Sheinbaum"

    def test_languages(self):
        cfg = load_country_config("mx")
        assert cfg.languages.primary == "es"
        assert cfg.languages.metadata == "en"

    def test_news_discovery(self):
        cfg = load_country_config("mx")
        assert cfg.news_discovery.goggle_file == "assets/country_goggles/mx.goggle"
        assert cfg.news_discovery.brave_params.country == "MX"
        assert cfg.news_discovery.brave_params.search_lang == "es"

    def test_query_vocabulary(self):
        cfg = load_country_config("mx")
        vocab = cfg.news_discovery.query_vocabulary
        assert len(vocab.diplomatic_alignment) >= 3
        assert len(vocab.security_defense) >= 3
        assert "SEDENA" in vocab.security_defense

    def test_government_discovery(self):
        cfg = load_country_config("mx")
        assert cfg.government_discovery.config_file == "assets/government/mx.yaml"

    def test_search_budget(self):
        cfg = load_country_config("mx")
        assert cfg.search.triage_queries_max == 3
        assert cfg.search.deep_dive_queries_max == 20

    def test_blind_spots(self):
        cfg = load_country_config("mx")
        assert len(cfg.blind_spots) == 3

    def test_dossier_path_exists(self):
        cfg = load_country_config("mx")
        path = cfg.dossier_path
        assert path.exists()
        assert "mexico" in path.name.lower()

    def test_invalid_code_rejected(self):
        with pytest.raises(ValueError):
            CountryConfig(
                country="Test",
                code="toolong",
                tier=Tier.SHIELD,
                region=Region.AMERICAS,
                actors=[Actor(name="X", role="Y", primary=True)],
                news_discovery=NewsDiscovery(
                    goggle_file="goggles/tt.goggle",
                    brave_params=BraveParams(country="TT", search_lang="en"),
                ),
                government_discovery=GovernmentDiscovery(config_file="government/tt.yaml"),
            )

    def test_no_primary_actor_rejected(self):
        with pytest.raises(ValueError, match="primary"):
            CountryConfig(
                country="Test",
                code="tt",
                tier=Tier.SHIELD,
                region=Region.AMERICAS,
                actors=[Actor(name="X", role="Y", primary=False)],
                news_discovery=NewsDiscovery(
                    goggle_file="goggles/tt.goggle",
                    brave_params=BraveParams(country="TT", search_lang="en"),
                ),
                government_discovery=GovernmentDiscovery(config_file="government/tt.yaml"),
            )

    def test_missing_config_file(self):
        with pytest.raises(FileNotFoundError):
            load_country_config("zz")

    def test_interpretive_context_file(self):
        cfg = load_country_config("mx")
        assert cfg.interpretive_context_file == "assets/context/mx_sources.md"


class TestGovernmentDomainConfig:
    def test_load_mexico(self):
        cfg = load_government_config("mx")
        assert cfg.country == "Mexico"
        assert cfg.code == "mx"
        assert cfg.information_culture == "managed"

    def test_domains(self):
        cfg = load_government_config("mx")
        assert len(cfg.domains) == 6
        p1_domains = [d for d in cfg.domains if d.priority == "P1"]
        assert len(p1_domains) == 2

    def test_query_terms(self):
        cfg = load_government_config("mx")
        assert "comunicado" in cfg.query_terms

    def test_domain_institutions(self):
        cfg = load_government_config("mx")
        gob = next(d for d in cfg.domains if d.domain == "gob.mx")
        assert "Presidency" in gob.institutions
        assert "SEDENA" in gob.institutions

    def test_missing_config(self):
        with pytest.raises(FileNotFoundError):
            load_government_config("zz")

    def test_construct_directly(self):
        cfg = GovernmentDomainConfig(
            country="Test",
            code="tt",
            information_culture="transparent",
            domains=[
                GovernmentDomain(domain="gov.tt", institutions=["PM Office"], priority="P1"),
            ],
            query_terms=["press release"],
        )
        assert cfg.information_culture == "transparent"
        assert len(cfg.domains) == 1

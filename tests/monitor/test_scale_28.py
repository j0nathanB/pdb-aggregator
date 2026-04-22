"""Scale tests: verify all 28 countries load, parse, and wire correctly.

Validates Steps 21-23: every country has a loadable config, government config,
goggle file, dossier, and Brave source config. Domain assembly and ledger
initialization (mechanical step) work for all 28. A mocked pipeline run
processes all countries without errors.
"""

from datetime import date
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

from src.monitor.collection.brave import load_brave_sources, GOGGLES_DIR
from src.monitor.config import (
    CountryConfig,
    Depth,
    Region,
    Tier,
    load_all_country_configs,
    load_country_config,
    load_government_config,
)
from src.monitor.ledger.initialize import mechanical_extract
from src.monitor.orchestrator import assemble_country_domains

# All 30 country codes (HU and PK added after the original 28-country set)
ALL_CODES = sorted([
    "ae", "au", "br", "ca", "cl", "cz", "de", "ee", "es", "fi",
    "fr", "gb", "hu", "id", "in", "it", "jp", "kr", "lt", "lv",
    "mx", "no", "pk", "pl", "ro", "sa", "se", "tr", "tw", "ua",
])


# =============================================================================
# Config loading
# =============================================================================


class TestAllCountryConfigs:
    """Every country config loads and passes validation."""

    def test_load_all_returns_30(self):
        configs = load_all_country_configs()
        assert len(configs) == 30
        assert sorted(configs.keys()) == ALL_CODES

    @pytest.mark.parametrize("code", ALL_CODES)
    def test_config_loads(self, code):
        cfg = load_country_config(code)
        assert cfg.code == code
        assert len(cfg.country) > 0

    @pytest.mark.parametrize("code", ALL_CODES)
    def test_has_primary_actor(self, code):
        cfg = load_country_config(code)
        assert len(cfg.primary_actors) >= 1

    @pytest.mark.parametrize("code", ALL_CODES)
    def test_has_valid_tier(self, code):
        cfg = load_country_config(code)
        assert cfg.tier in list(Tier)

    @pytest.mark.parametrize("code", ALL_CODES)
    def test_has_valid_region(self, code):
        cfg = load_country_config(code)
        assert cfg.region in list(Region)

    @pytest.mark.parametrize("code", ALL_CODES)
    def test_has_languages(self, code):
        cfg = load_country_config(code)
        assert len(cfg.languages.primary) >= 2


# =============================================================================
# Government configs
# =============================================================================


class TestAllGovernmentConfigs:
    """Every country has a loadable government domain config."""

    @pytest.mark.parametrize("code", ALL_CODES)
    def test_gov_config_loads(self, code):
        cfg = load_government_config(code)
        assert cfg.code == code
        assert len(cfg.domains) >= 1

    @pytest.mark.parametrize("code", ALL_CODES)
    def test_query_terms_is_list(self, code):
        cfg = load_government_config(code)
        assert isinstance(cfg.query_terms, list)

    @pytest.mark.parametrize("code", ALL_CODES)
    def test_has_information_culture(self, code):
        cfg = load_government_config(code)
        assert cfg.information_culture in ("transparent", "managed", "controlled")

    @pytest.mark.parametrize("code", ALL_CODES)
    def test_has_p1_domains(self, code):
        cfg = load_government_config(code)
        p1 = [d for d in cfg.domains if d.priority == "P1"]
        assert len(p1) >= 1, f"{code} has no P1 government domains"


# =============================================================================
# Goggles
# =============================================================================


class TestAllGoggles:
    """Every country has a goggle file."""

    @pytest.mark.parametrize("code", ALL_CODES)
    def test_goggle_file_exists(self, code):
        path = GOGGLES_DIR / f"{code}.goggle"
        assert path.exists(), f"Missing goggle: {path}"

    @pytest.mark.parametrize("code", ALL_CODES)
    def test_goggle_has_boost_rules(self, code):
        path = GOGGLES_DIR / f"{code}.goggle"
        content = path.read_text()
        assert "$boost=" in content, f"{code}.goggle has no boost rules"

    @pytest.mark.parametrize("code", ALL_CODES)
    def test_goggle_has_header(self, code):
        path = GOGGLES_DIR / f"{code}.goggle"
        content = path.read_text()
        assert "! name:" in content


# =============================================================================
# Brave sources
# =============================================================================


class TestAllBraveSources:
    """Brave source config covers every country."""

    def test_loads_all_countries(self):
        # Legit failure as of 2026-04-21: HU and PK were added to
        # country configs but not to the Brave source config.
        configs = load_brave_sources()
        assert sorted(configs.keys()) == ALL_CODES

    @pytest.mark.parametrize("code", ALL_CODES)
    def test_has_sources(self, code):
        configs = load_brave_sources()
        assert code in configs
        assert len(configs[code].sources) >= 5, (
            f"{code} has only {len(configs[code].sources)} Brave sources"
        )


# =============================================================================
# Dossiers
# =============================================================================

class TestAllDossiers:
    """Every country has a parseable dossier."""

    @pytest.mark.parametrize("code", ALL_CODES)
    def test_dossier_exists(self, code):
        cfg = load_country_config(code)
        path = cfg.dossier_path
        assert path.exists(), f"Missing dossier for {code}: {path}"

    @pytest.mark.parametrize("code", ALL_CODES)
    def test_dossier_has_content(self, code):
        cfg = load_country_config(code)
        content = cfg.dossier_path.read_text()
        assert len(content) > 1000, f"{code} dossier too short ({len(content)} chars)"


# =============================================================================
# Mechanical ledger initialization
# =============================================================================


class TestAllMechanicalExtract:
    """mechanical_extract succeeds for all countries with dossiers."""

    @pytest.mark.parametrize("code", ALL_CODES)
    def test_mechanical_extract(self, code):
        cfg = load_country_config(code)
        skeleton = mechanical_extract(cfg)
        assert skeleton["country"] == cfg.country
        assert skeleton["code"] == code
        assert skeleton["tier"] == cfg.tier.value
        assert len(skeleton["actors"]) >= 1


# =============================================================================
# Domain assembly
# =============================================================================


class TestAllDomainAssembly:
    """Domain assembly works for all 28 countries."""

    @pytest.mark.parametrize("code", ALL_CODES)
    def test_domain_assembly(self, code):
        cfg = load_country_config(code)
        gov_cfg = load_government_config(code)
        result = assemble_country_domains(cfg, gov_config=gov_cfg)

        assert "allowed_domains" in result
        assert "gov_domains" in result
        assert "wire_domains" in result
        assert len(result["gov_domains"]) >= 1
        assert len(result["wire_domains"]) >= 1
        # Gov domains should be in allowed_domains
        for gd in result["gov_domains"]:
            assert gd in result["allowed_domains"]

    @pytest.mark.parametrize("code", ALL_CODES)
    def test_no_duplicate_allowed_domains(self, code):
        cfg = load_country_config(code)
        gov_cfg = load_government_config(code)
        result = assemble_country_domains(cfg, gov_config=gov_cfg)
        assert len(result["allowed_domains"]) == len(set(result["allowed_domains"]))


# =============================================================================
# Full pipeline (mocked LLM calls)
# =============================================================================


class TestPipelineAll28:
    """Run desk pipeline for all 28 countries with mocked agents."""

    @pytest.fixture
    def tmp_ledger_dirs(self, tmp_path):
        """Redirect ledger storage to temp directory."""
        import src.monitor.config as config_mod
        import src.monitor.ledger.storage as storage_mod

        countries_dir = tmp_path / "countries"
        archive_dir = tmp_path / "archive"
        global_path = tmp_path / "global.json"
        countries_dir.mkdir()
        archive_dir.mkdir()

        orig = {
            "config_countries": config_mod.COUNTRY_LEDGERS_DIR,
            "config_global": config_mod.GLOBAL_LEDGER_PATH,
            "config_archive": config_mod.LEDGER_ARCHIVE_DIR,
            "storage_countries": storage_mod.COUNTRY_LEDGERS_DIR,
            "storage_global": storage_mod.GLOBAL_LEDGER_PATH,
            "storage_archive": storage_mod.LEDGER_ARCHIVE_DIR,
        }

        config_mod.COUNTRY_LEDGERS_DIR = countries_dir
        config_mod.GLOBAL_LEDGER_PATH = global_path
        config_mod.LEDGER_ARCHIVE_DIR = archive_dir
        storage_mod.COUNTRY_LEDGERS_DIR = countries_dir
        storage_mod.GLOBAL_LEDGER_PATH = global_path
        storage_mod.LEDGER_ARCHIVE_DIR = archive_dir

        yield tmp_path

        config_mod.COUNTRY_LEDGERS_DIR = orig["config_countries"]
        config_mod.GLOBAL_LEDGER_PATH = orig["config_global"]
        config_mod.LEDGER_ARCHIVE_DIR = orig["config_archive"]
        storage_mod.COUNTRY_LEDGERS_DIR = orig["storage_countries"]
        storage_mod.GLOBAL_LEDGER_PATH = orig["storage_global"]
        storage_mod.LEDGER_ARCHIVE_DIR = orig["storage_archive"]

    @pytest.mark.asyncio
    async def test_pipeline_all_countries(self, tmp_ledger_dirs):
        """Pipeline processes all 30 countries without errors when agents are mocked."""
        from src.monitor.agents.country import CountryAgentOutput
        from src.monitor.agents.expansion import ExpansionResult
        from src.monitor.agents.story_map import StoryMapOutput
        from src.monitor.agents.triage import TriageDecision, TriageOutput
        from src.monitor.models import (
            CategoryMovement,
            CountryLedger,
            DevilsAdvocate,
            PostureSummary,
            SignalCategoryAssessment,
            WeeklyEntry,
        )
        from src.monitor.config import (
            CategoryStatus,
            Movement,
            SignalCategory,
        )
        from src.monitor.orchestrator import run_desk_pipeline

        end_date = date(2026, 3, 21)
        configs = load_all_country_configs()

        # Build triage decisions: all deep dive
        triage_decisions = [
            TriageDecision(
                country=cfg.country,
                code=code,
                depth=Depth.DEEP_DIVE,
                rationale="Scale test.",
                triggered_by=["first_cycle"],
            )
            for code, cfg in configs.items()
        ]

        # Build a generic country agent output factory
        def _make_output(code, country):
            return CountryAgentOutput(
                weekly_entry=WeeklyEntry(
                    week=end_date,
                    date_range="2026-03-14 to 2026-03-21",
                    depth=Depth.DEEP_DIVE,
                    category_movements={
                        c: CategoryMovement(movement=Movement.NONE)
                        for c in SignalCategory
                    },
                    devils_advocate=DevilsAdvocate(
                        challenges=["Test challenge"],
                        recommended_adjustments=["Test adjustment"],
                    ),
                ),
                signal_categories={
                    c: SignalCategoryAssessment(
                        current_assessment=f"Baseline for {c.value}",
                        confidence=3,
                        last_updated=end_date,
                    )
                    for c in SignalCategory
                },
                posture_summary=PostureSummary(
                    as_of=end_date,
                    text=f"Initial posture for {country}.",
                    category_status={
                        c: CategoryStatus.QUIET for c in SignalCategory
                    },
                    last_deep_dive=end_date,
                    consecutive_maintenance_weeks=0,
                ),
            )

        # Mock country agent to return per-country output
        async def mock_country_agent(config, ledger, *args, **kwargs):
            return _make_output(config.code, config.country)

        # Mock expansion: one empty ExpansionResult per country (no Brave calls).
        # run_desk_pipeline calls expand_all_countries, so patch at that layer.
        async def mock_expand_all(configs_list, brave_client, scan_map, end_date_arg, concurrency):
            return {
                cfg.code: ExpansionResult(code=cfg.code, country=cfg.country)
                for cfg in configs_list
            }

        # Mock story_map: one empty StoryMapOutput per country (no Anthropic calls).
        async def mock_story_map(config, expansion, analysis_date, model=None):
            return StoryMapOutput(
                country=config.country,
                code=config.code,
                analysis_date=analysis_date.isoformat(),
                search_results_total=0,
                stories_identified=0,
                off_topic_filtered=0,
            )

        with (
            patch("src.monitor.orchestrator.collect_layer2") as mock_l2,
            patch("src.monitor.orchestrator.run_triage") as mock_triage,
            patch(
                "src.monitor.orchestrator.expand_all_countries",
                side_effect=mock_expand_all,
            ),
            patch(
                "src.monitor.orchestrator.run_story_map_agent",
                side_effect=mock_story_map,
            ),
            patch(
                "src.monitor.orchestrator.run_country_agent",
                side_effect=mock_country_agent,
            ),
            patch("src.monitor.orchestrator.run_devils_advocate") as mock_da,
            patch("src.monitor.orchestrator.initialize_country_ledger") as mock_init,
        ):
            # Layer 2: empty results (skip for scale test)
            mock_l2.return_value = {}

            # Triage: all deep dive
            mock_triage.return_value = TriageOutput(
                triage_date=end_date,
                decisions=triage_decisions,
            )

            # Devil's advocate: pass-through
            mock_da.return_value = DevilsAdvocate(
                challenges=["Scale test challenge"],
                recommended_adjustments=["Scale test adjustment"],
            )

            # Initialize: build skeleton ledgers
            async def mock_init_ledger(config):
                skeleton = mechanical_extract(config)
                # Add required fields for CountryLedger
                skeleton["last_updated"] = end_date
                skeleton["created"] = end_date
                skeleton["posture_summary"] = PostureSummary(
                    as_of=end_date,
                    text=f"Initial posture for {config.country}.",
                    category_status={
                        c: CategoryStatus.QUIET for c in SignalCategory
                    },
                    last_deep_dive=end_date,
                    consecutive_maintenance_weeks=0,
                )
                skeleton["signal_categories"] = {
                    c: SignalCategoryAssessment(
                        current_assessment=f"Baseline for {c.value}",
                        confidence=3,
                        last_updated=end_date,
                    )
                    for c in SignalCategory
                }
                return CountryLedger(**skeleton)

            mock_init.side_effect = mock_init_ledger

            result = await run_desk_pipeline(
                end_date=end_date,
                skip_layer2=True,
            )

        assert len(result.country_results) == 30, (
            f"Expected 30 results, got {len(result.country_results)}. "
            f"Errors: {result.errors}"
        )
        assert len(result.errors) == 0, f"Pipeline errors: {result.errors}"

        # All should be successful deep dives
        assert len(result.deep_dive_results) == 30
        assert len(result.failed_results) == 0

        # Verify each country code appears exactly once
        result_codes = sorted(cr.code for cr in result.country_results)
        assert result_codes == ALL_CODES

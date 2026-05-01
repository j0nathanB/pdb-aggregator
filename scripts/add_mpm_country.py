#!/usr/bin/env python3
"""
add_mpm_country — onboard a new country to the Middle Powers Monitor pipeline.

Usage:
    python scripts/add_mpm_country.py pakistan pk middle_east_turkey_south_asia
    python scripts/add_mpm_country.py pakistan pk middle_east_turkey_south_asia --phase 1
    python scripts/add_mpm_country.py pakistan pk middle_east_turkey_south_asia --resume

Phases (run sequentially by default; use --phase N to run a single phase):
    1. Dossier generation (3-pass LLM chain via Anthropic API + web_search)
    2. Source discovery and verification (Brave News + SearchAPI/Google)
    3. Extraction routing (deferred — uses defaults; run experiment manually if needed)
    4. Config file generation (goggle, country YAML, government YAML)
    5. Code integration (regional.py edits, validation runs)
    6. Final onboarding report

State is tracked in dev/onboarding/{code}/state.json so the script can resume after a failure.

See docs/adding_a_country.md for the full spec.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import re
import sys
from dataclasses import asdict, dataclass, field
from datetime import date
from pathlib import Path
from typing import Any

import anthropic
import yaml
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
load_dotenv(PROJECT_ROOT / ".env")

from src.monitor.collection.brave import BraveNewsClient  # noqa: E402
from src.monitor.collection.searchapi import SearchAPIClient  # noqa: E402

# =============================================================================
# Logging
# =============================================================================

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger("add_mpm_country")
logging.getLogger("httpx").setLevel(logging.WARNING)

# =============================================================================
# Constants
# =============================================================================

MODEL = "claude-opus-4-6"  # research-grade model for dossier generation
MAX_TOKENS = 16000

PROMPTS_DIR = PROJECT_ROOT / "dev" / "check_dossiers" / "prompts" / "updated_prompts"
SOURCE_PROMPTS_DIR = PROJECT_ROOT / "dev" / "source_maps"

DOSSIER_DIR = PROJECT_ROOT / "assets" / "country_dossiers"
PASS1_DIR = DOSSIER_DIR / "_pass1"
PASS2_DIR = DOSSIER_DIR / "_pass2"
PASS3_DIR = DOSSIER_DIR / "_pass3"

COUNTRY_CONFIG_DIR = PROJECT_ROOT / "assets" / "country_configs" / "countries"
GOVERNMENT_CONFIG_DIR = PROJECT_ROOT / "assets" / "government"
GOGGLE_DIR = PROJECT_ROOT / "assets" / "country_goggles"
SOURCE_MAPS_DIR = PROJECT_ROOT / "dev" / "source_maps" / "media" / "source_maps"
GOV_DRAFTS_DIR = PROJECT_ROOT / "dev" / "source_maps" / "gov" / "_drafts"
EXTRACTION_ROUTING_PATH = PROJECT_ROOT / "assets" / "country_configs" / "extraction_routing.yaml"
BRAVE_SOURCES_PATH = PROJECT_ROOT / "assets" / "country_configs" / "brave_sources.yaml"
REGIONAL_PY_PATH = PROJECT_ROOT / "src" / "monitor" / "agents" / "regional.py"

WORKSPACE_ROOT = PROJECT_ROOT / "dev" / "onboarding"
REPORTS_DIR = PROJECT_ROOT / "dev" / "check_dossiers" / "onboarding_reports"

VALID_REGIONS = {
    "americas",
    "western_europe",
    "central_eastern_europe",
    "nordic_baltic",
    "near_east_south_asia",
    "asia_pacific",
}

# =============================================================================
# Data structures
# =============================================================================


@dataclass
class CountryArgs:
    name: str          # display name, e.g. "Pakistan"
    code: str          # 2-letter ISO code, e.g. "pk"
    region: str        # region enum value, e.g. "middle_east_turkey_south_asia"
    language: str = "en"   # primary language for source curation prompt
    today: str = field(default_factory=lambda: date.today().isoformat())

    @property
    def slug(self) -> str:
        return self.name.lower().replace(" ", "_")

    @property
    def workspace(self) -> Path:
        return WORKSPACE_ROOT / self.code


@dataclass
class PhaseResult:
    phase: int
    name: str
    status: str  # "ok", "failed", "skipped"
    outputs: dict[str, str] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)


@dataclass
class OnboardingState:
    country: CountryArgs
    phase_results: dict[int, PhaseResult] = field(default_factory=dict)

    def save(self) -> None:
        self.country.workspace.mkdir(parents=True, exist_ok=True)
        path = self.country.workspace / "state.json"
        data = {
            "country": asdict(self.country),
            "phase_results": {
                str(k): asdict(v) for k, v in self.phase_results.items()
            },
        }
        path.write_text(json.dumps(data, indent=2))

    @classmethod
    def load_or_init(cls, args: CountryArgs) -> OnboardingState:
        path = args.workspace / "state.json"
        if not path.exists():
            return cls(country=args)
        data = json.loads(path.read_text())
        results = {
            int(k): PhaseResult(**v) for k, v in data.get("phase_results", {}).items()
        }
        return cls(country=args, phase_results=results)

    def mark(self, result: PhaseResult) -> None:
        self.phase_results[result.phase] = result
        self.save()


# =============================================================================
# LLM helper (Anthropic + web_search tool)
# =============================================================================


async def call_llm_with_search(
    *,
    prompt: str,
    label: str,
    max_tokens: int = MAX_TOKENS,
) -> str:
    """Run an Anthropic API call with the web_search tool enabled.

    Returns concatenated text content from the response.
    """
    client = anthropic.AsyncAnthropic()
    logger.info("LLM call [%s]: starting (max_tokens=%d)", label, max_tokens)

    # Use streaming for long-running research calls
    async with client.messages.stream(
        model=MODEL,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
        tools=[{
            "type": "web_search_20250305",
            "name": "web_search",
        }],
    ) as stream:
        response = await stream.get_final_message()

    text_parts: list[str] = []
    search_count = 0
    for block in response.content:
        if block.type == "text":
            text_parts.append(block.text)
        elif block.type == "web_search_tool_result":
            search_count += 1

    text = "\n".join(text_parts).strip()
    logger.info(
        "LLM call [%s]: done — input=%d, output=%d tokens, searches=%d, output=%d chars",
        label,
        response.usage.input_tokens,
        response.usage.output_tokens,
        search_count,
        len(text),
    )
    return text


def substitute_placeholders(prompt_text: str, country: CountryArgs) -> str:
    """Replace {{COUNTRY}}, [COUNTRY], {{LANGUAGE}} placeholders."""
    return (
        prompt_text
        .replace("{{COUNTRY}}", country.name)
        .replace("[COUNTRY]", country.name)
        .replace("{{LANGUAGE}}", country.language)
    )


def load_prompt(path: Path) -> str:
    return path.read_text()


# =============================================================================
# Phase 1: Dossier generation
# =============================================================================


async def phase_1_dossier(state: OnboardingState) -> PhaseResult:
    country = state.country
    result = PhaseResult(phase=1, name="dossier_generation", status="ok")
    PASS1_DIR.mkdir(parents=True, exist_ok=True)
    PASS2_DIR.mkdir(parents=True, exist_ok=True)
    PASS3_DIR.mkdir(parents=True, exist_ok=True)

    pass1_path = PASS1_DIR / f"{country.slug}_pass1_{country.today}.md"
    pass2_path = PASS2_DIR / f"{country.slug}_pass2_{country.today}.md"
    pass3_path = PASS3_DIR / f"{country.slug}_pass3_{country.today}.md"
    merged_path = DOSSIER_DIR / f"{country.slug}_dossier_{country.today}.md"

    # --- Pass 1 ---
    if pass1_path.exists():
        logger.info("Phase 1: pass 1 already exists at %s, skipping", pass1_path)
        pass1_text = pass1_path.read_text()
    else:
        prompt_text = load_prompt(PROMPTS_DIR / "pass_1 updated.md")
        prompt_text = substitute_placeholders(prompt_text, country)
        try:
            pass1_text = await call_llm_with_search(
                prompt=prompt_text,
                label=f"dossier-pass1-{country.code}",
            )
            pass1_path.write_text(pass1_text)
            logger.info("Phase 1: pass 1 saved → %s", pass1_path)
        except Exception as e:
            result.status = "failed"
            result.errors.append(f"pass 1: {e}")
            return result

    # --- Pass 2 (with pass 1 as context) ---
    if pass2_path.exists():
        logger.info("Phase 1: pass 2 already exists at %s, skipping", pass2_path)
        pass2_text = pass2_path.read_text()
    else:
        prompt_text = load_prompt(PROMPTS_DIR / "pass_2 updated.md")
        prompt_text = substitute_placeholders(prompt_text, country)
        full_prompt = (
            f"--- PASS 1 OUTPUT (context) ---\n\n{pass1_text}\n\n"
            f"--- PASS 2 PROMPT ---\n\n{prompt_text}"
        )
        try:
            pass2_text = await call_llm_with_search(
                prompt=full_prompt,
                label=f"dossier-pass2-{country.code}",
            )
            pass2_path.write_text(pass2_text)
            logger.info("Phase 1: pass 2 saved → %s", pass2_path)
        except Exception as e:
            result.status = "failed"
            result.errors.append(f"pass 2: {e}")
            return result

    # --- Pass 3 (with pass 1+2 as context) ---
    if pass3_path.exists():
        logger.info("Phase 1: pass 3 already exists at %s, skipping", pass3_path)
        pass3_text = pass3_path.read_text()
    else:
        prompt_text = load_prompt(PROMPTS_DIR / "pass_3 updated.md")
        prompt_text = substitute_placeholders(prompt_text, country)
        full_prompt = (
            f"--- PASS 1 OUTPUT (context) ---\n\n{pass1_text}\n\n"
            f"--- PASS 2 OUTPUT (context) ---\n\n{pass2_text}\n\n"
            f"--- PASS 3 PROMPT ---\n\n{prompt_text}"
        )
        try:
            pass3_text = await call_llm_with_search(
                prompt=full_prompt,
                label=f"dossier-pass3-{country.code}",
            )
            pass3_path.write_text(pass3_text)
            logger.info("Phase 1: pass 3 saved → %s", pass3_path)
        except Exception as e:
            result.status = "failed"
            result.errors.append(f"pass 3: {e}")
            return result

    # --- Merge ---
    merged = (
        f"# {country.name}: Middle Powers Monitor analytical dossier\n\n"
        f"{pass1_text}\n\n---\n\n{pass2_text}\n\n---\n\n{pass3_text}\n"
    )
    merged_path.write_text(merged)
    logger.info("Phase 1: merged dossier saved → %s", merged_path)

    result.outputs = {
        "pass1": str(pass1_path),
        "pass2": str(pass2_path),
        "pass3": str(pass3_path),
        "merged_dossier": str(merged_path),
    }
    return result


# =============================================================================
# Phase 2: Source discovery and verification
# =============================================================================


def extract_domains_from_markdown(text: str) -> list[str]:
    r"""Extract candidate domains from a curation/audit/gov markdown file.

    Handles three patterns:
    - `| **Domain** | example.com |` (curation/audit table)
    - `| **Domain** | \`example.com\` |` (gov table — backtick-wrapped)
    - `site=example.com` (goggle code block)
    """
    domains: set[str] = set()
    # Match `| **Domain** | [`]example.com[`] |` (optional backticks)
    pattern1 = re.compile(
        r"\|\s*\**Domain\**\s*\|\s*`?([a-z0-9][\w\-]*(?:\.[a-z]{2,})+)`?\s*\|",
        re.IGNORECASE,
    )
    for m in pattern1.finditer(text):
        domains.add(m.group(1).lower())
    # Match site=domain.com (goggle-style) and similar lines
    pattern2 = re.compile(r"\bsite=([a-z0-9][\w\-]*(?:\.[a-z]{2,})+)\b", re.IGNORECASE)
    for m in pattern2.finditer(text):
        domains.add(m.group(1).lower())
    return sorted(domains)


async def verify_brave_indexing(domains: list[str], country_code: str) -> dict[str, int]:
    """For each domain, run a Brave query and return result counts.

    Domains with 0 results are not indexed (or not searchable in news).
    """
    counts: dict[str, int] = {}
    async with BraveNewsClient() as client:
        for domain in domains:
            try:
                resp = await client.search_news(
                    query=f"site:{domain}",
                    count=10,
                    freshness="pm",  # past month
                )
                counts[domain] = len(resp.results)
                logger.info("Brave verify: %s → %d results", domain, counts[domain])
            except Exception as e:
                logger.warning("Brave verify: %s failed: %s", domain, e)
                counts[domain] = -1  # error
        logger.info("Brave verify: %d API calls for %s", client.api_call_count, country_code)
    return counts


async def verify_searchapi_indexing(domains: list[str]) -> dict[str, int]:
    """For each government domain, run a SearchAPI Google query and return result counts."""
    counts: dict[str, int] = {}
    async with SearchAPIClient() as client:
        for domain in domains:
            try:
                resp = await client.search(query=f"site:{domain}", num=10)
                counts[domain] = len(resp.results)
                logger.info("SearchAPI verify: %s → %d results", domain, counts[domain])
            except Exception as e:
                logger.warning("SearchAPI verify: %s failed: %s", domain, e)
                counts[domain] = -1
    return counts


async def phase_2_sources(state: OnboardingState) -> PhaseResult:
    country = state.country
    result = PhaseResult(phase=2, name="source_discovery", status="ok")

    SOURCE_MAPS_DIR.mkdir(parents=True, exist_ok=True)
    GOV_DRAFTS_DIR.mkdir(parents=True, exist_ok=True)
    drafts_dir = SOURCE_MAPS_DIR / "_drafts"
    drafts_dir.mkdir(parents=True, exist_ok=True)

    # Load merged dossier as context
    merged_dossier_path = DOSSIER_DIR / f"{country.slug}_dossier_{country.today}.md"
    if not merged_dossier_path.exists():
        result.status = "failed"
        result.errors.append(f"merged dossier not found at {merged_dossier_path} — run Phase 1 first")
        return result
    dossier_text = merged_dossier_path.read_text()

    curation_path = drafts_dir / f"{country.slug}_curation.md"
    audit_path = drafts_dir / f"{country.slug}_audit.md"
    gov_path = GOV_DRAFTS_DIR / f"{country.slug}_gov.md"
    final_source_map_path = SOURCE_MAPS_DIR / f"{country.slug}.md"

    # --- Source curation ---
    if curation_path.exists():
        logger.info("Phase 2: curation already exists, skipping LLM call")
        curation_text = curation_path.read_text()
    else:
        prompt_text = load_prompt(SOURCE_PROMPTS_DIR / "source_curation_prompt_v2.md")
        prompt_text = substitute_placeholders(prompt_text, country)
        full_prompt = (
            f"--- COUNTRY DOSSIER (context) ---\n\n{dossier_text}\n\n"
            f"--- CURATION PROMPT ---\n\n{prompt_text}"
        )
        try:
            curation_text = await call_llm_with_search(
                prompt=full_prompt,
                label=f"source-curation-{country.code}",
            )
            curation_path.write_text(curation_text)
            logger.info("Phase 2: curation saved → %s", curation_path)
        except Exception as e:
            result.status = "failed"
            result.errors.append(f"curation: {e}")
            return result

    # --- Source audit ---
    if audit_path.exists():
        logger.info("Phase 2: audit already exists, skipping LLM call")
        audit_text = audit_path.read_text()
    else:
        prompt_text = load_prompt(SOURCE_PROMPTS_DIR / "source_whitelist_audit_prompt_v2.md")
        prompt_text = substitute_placeholders(prompt_text, country)
        full_prompt = (
            f"--- CURATED SOURCES ---\n\n{curation_text}\n\n"
            f"--- AUDIT PROMPT ---\n\n{prompt_text}"
        )
        try:
            audit_text = await call_llm_with_search(
                prompt=full_prompt,
                label=f"source-audit-{country.code}",
            )
            audit_path.write_text(audit_text)
            logger.info("Phase 2: audit saved → %s", audit_path)
        except Exception as e:
            result.status = "failed"
            result.errors.append(f"audit: {e}")
            return result

    # --- Government source discovery ---
    if gov_path.exists():
        logger.info("Phase 2: gov sources already exist, skipping LLM call")
        gov_text = gov_path.read_text()
    else:
        prompt_text = load_prompt(SOURCE_PROMPTS_DIR / "government_sources_prompt.md")
        prompt_text = substitute_placeholders(prompt_text, country)
        full_prompt = (
            f"--- COUNTRY DOSSIER (context) ---\n\n{dossier_text}\n\n"
            f"--- GOVERNMENT SOURCES PROMPT ---\n\n{prompt_text}"
        )
        try:
            gov_text = await call_llm_with_search(
                prompt=full_prompt,
                label=f"gov-sources-{country.code}",
            )
            gov_path.write_text(gov_text)
            logger.info("Phase 2: gov sources saved → %s", gov_path)
        except Exception as e:
            result.status = "failed"
            result.errors.append(f"gov sources: {e}")
            return result

    # --- Verify against Brave ---
    media_domains = extract_domains_from_markdown(audit_text)
    logger.info("Phase 2: extracted %d media domains for Brave verification", len(media_domains))
    brave_counts = await verify_brave_indexing(media_domains, country.code)
    verified_media = [d for d, c in brave_counts.items() if c > 0]
    dropped_media = [d for d, c in brave_counts.items() if c == 0]
    logger.info("Phase 2: %d/%d media domains verified", len(verified_media), len(media_domains))

    # --- Verify against SearchAPI (government) ---
    gov_domains = extract_domains_from_markdown(gov_text)
    logger.info("Phase 2: extracted %d gov domains for SearchAPI verification", len(gov_domains))
    sapi_counts = await verify_searchapi_indexing(gov_domains)
    verified_gov = [d for d, c in sapi_counts.items() if c > 0]
    dropped_gov = [d for d, c in sapi_counts.items() if c == 0]
    logger.info("Phase 2: %d/%d gov domains verified", len(verified_gov), len(gov_domains))

    # --- Final source map ---
    final = (
        f"# Source Intelligence Map: {country.name.upper()}\n\n"
        f"---\n\n## MEDIA LANDSCAPE SUMMARY\n\n"
        f"_See `_drafts/{country.slug}_curation.md` and `_drafts/{country.slug}_audit.md` for full curation and audit notes._\n\n"
        f"---\n\n## VERIFIED MEDIA SOURCES ({len(verified_media)} of {len(media_domains)})\n\n"
        + "\n".join(f"- {d} (Brave indexed: {brave_counts[d]} results)" for d in verified_media)
        + f"\n\n## DROPPED MEDIA SOURCES ({len(dropped_media)})\n\n"
        + "\n".join(f"- {d} (no Brave results)" for d in dropped_media)
        + f"\n\n---\n\n## VERIFIED GOVERNMENT SOURCES ({len(verified_gov)} of {len(gov_domains)})\n\n"
        + "\n".join(f"- {d} (SearchAPI indexed: {sapi_counts[d]} results)" for d in verified_gov)
        + f"\n\n## DROPPED GOVERNMENT SOURCES ({len(dropped_gov)})\n\n"
        + "\n".join(f"- {d} (no SearchAPI results)" for d in dropped_gov)
        + "\n\n---\n\n_Full curation, audit, and government source files are in `_drafts/` and `gov/_drafts/`._\n"
    )
    final_source_map_path.write_text(final)
    logger.info("Phase 2: final source map saved → %s", final_source_map_path)

    # Save verification details to workspace for downstream phases
    verification_path = country.workspace / "verification.json"
    verification_path.write_text(json.dumps({
        "verified_media": verified_media,
        "dropped_media": dropped_media,
        "verified_gov": verified_gov,
        "dropped_gov": dropped_gov,
        "brave_counts": brave_counts,
        "searchapi_counts": sapi_counts,
    }, indent=2))

    result.outputs = {
        "curation": str(curation_path),
        "audit": str(audit_path),
        "gov": str(gov_path),
        "source_map": str(final_source_map_path),
        "verification": str(verification_path),
    }
    return result


# =============================================================================
# Phase 3: Extraction routing (deferred — uses defaults)
# =============================================================================


async def phase_3_extraction(state: OnboardingState) -> PhaseResult:
    """Build extraction routing entries with default fallback chain.

    The full 4-method extraction experiment (curl/diffbot/playwright/browserbase)
    is deferred. New domains use the default routing (curl → diffbot → playwright
    → browserbase), which the pipeline already applies via fallback when no
    specific entry exists. Per-domain optimization can be added later by running
    dev/source_maps/media/RETRIEVAL_EXPERIMENT_GUIDE.md manually.
    """
    country = state.country
    result = PhaseResult(phase=3, name="extraction_routing", status="ok")

    verification_path = country.workspace / "verification.json"
    if not verification_path.exists():
        result.status = "failed"
        result.errors.append("verification.json not found — run Phase 2 first")
        return result

    verification = json.loads(verification_path.read_text())
    verified = verification["verified_media"] + verification["verified_gov"]

    note_path = country.workspace / "extraction_routing_note.md"
    note = (
        f"# Extraction routing for {country.name} ({country.code})\n\n"
        f"Phase 3 deferred — all {len(verified)} verified domains will use the\n"
        f"pipeline's default extraction fallback chain (curl → diffbot → playwright\n"
        f"→ browserbase). No per-domain entries written to `extraction_routing.yaml`.\n\n"
        f"To optimize specific domains later, run the experiment in\n"
        f"`dev/source_maps/media/RETRIEVAL_EXPERIMENT_GUIDE.md` and append entries\n"
        f"to `assets/country_configs/extraction_routing.yaml`.\n\n"
        f"## Verified domains ({len(verified)})\n\n"
        + "\n".join(f"- {d}" for d in verified) + "\n"
    )
    note_path.write_text(note)
    logger.info("Phase 3: extraction routing note saved → %s", note_path)

    result.outputs = {"extraction_routing_note": str(note_path)}
    return result


# =============================================================================
# Phase 4: Config file generation
# =============================================================================


# International watchdog/think tank sources added to all goggles as tier 3.
# These cover universal blind spots (human rights, defence research, policy analysis).
# Verified indexed in Brave News.
DEFAULT_TIER3_SOURCES = [
    "hrw.org",
    "amnesty.org",
    "fas.org",
    "carnegieendowment.org",
]


def parse_audit_tiers(
    audit_text: str,
    verified_media: set[str],
) -> dict[str, list[str]]:
    """Parse the audit prompt's goggle code block for explicit tier assignments.

    The audit prompt outputs lines like:
        $boost=3,site=dawn.com
        $boost=2,site=tribune.com.pk
        $boost=1,site=pakistantoday.com.pk
        $discard,site=bolnews.com

    The audit uses the legacy 3/2/1 scale; we map to our 10/5/3 scale.
    Only domains that survived verification (in verified_media) are kept.
    """
    tier1: list[str] = []
    tier2: list[str] = []
    tier3: list[str] = []
    discard: list[str] = []

    # Match each goggle rule. Use line-anchored regex to avoid matching prose.
    rule_re = re.compile(
        r"^\s*\$(?:boost=(\d+)|(discard)),site=([a-z0-9][\w\-]*(?:\.[a-z]{2,})+)\s*$",
        re.MULTILINE | re.IGNORECASE,
    )
    seen: set[str] = set()
    for m in rule_re.finditer(audit_text):
        boost_val = m.group(1)
        is_discard = m.group(2)
        domain = m.group(3).lower()
        if domain in seen:
            continue
        seen.add(domain)
        if is_discard:
            discard.append(domain)
        elif boost_val == "3":
            if domain in verified_media:
                tier1.append(domain)
        elif boost_val == "2":
            if domain in verified_media:
                tier2.append(domain)
        elif boost_val == "1":
            if domain in verified_media:
                tier3.append(domain)

    return {"tier1": tier1, "tier2": tier2, "tier3": tier3, "discard": discard}


def classify_goggle_tiers(
    audit_text: str,
    verified_media: list[str],
    verified_gov: list[str],
) -> dict[str, list[str]]:
    """Build goggle tiers from the audit prompt's explicit assignments.

    Falls back to a simple heuristic if the audit didn't produce a goggle block.
    Government domains are always added to tier 2.
    """
    verified_set = set(verified_media)
    parsed = parse_audit_tiers(audit_text, verified_set)

    if not (parsed["tier1"] or parsed["tier2"] or parsed["tier3"]):
        # Fallback: alphabetical heuristic
        logger.warning("Audit did not produce explicit goggle tiers; falling back to heuristic")
        return {
            "tier1": verified_media[:6],
            "tier2": verified_media[6:16] + verified_gov,
            "tier3": list(DEFAULT_TIER3_SOURCES),
            "discard": [],
        }

    # Append verified government domains to tier 2 (deduplicated)
    tier2 = parsed["tier2"] + [d for d in verified_gov if d not in parsed["tier2"]]
    # Append default international sources to tier 3 (deduplicated)
    tier3 = parsed["tier3"] + [d for d in DEFAULT_TIER3_SOURCES if d not in parsed["tier3"]]
    return {
        "tier1": parsed["tier1"],
        "tier2": tier2,
        "tier3": tier3,
        "discard": parsed["discard"],
    }


def write_goggle_file(country: CountryArgs, tiers: dict[str, list[str]]) -> Path:
    path = GOGGLE_DIR / f"{country.code}.goggle"
    lines = [
        f"! name: MPM {country.name}",
        f"! description: MPM pipeline source prioritization for {country.name}",
        "! public: false",
        "! author: MPM Pipeline",
        "",
        "! --- Tier 1: Essential (boost=10) ---",
    ]
    for d in tiers["tier1"]:
        lines.append(f"$boost=10,site={d}")
    lines.append("")
    lines.append("! --- Tier 2: Important (boost=5) ---")
    for d in tiers["tier2"]:
        lines.append(f"$boost=5,site={d}")
    lines.append("")
    lines.append("! --- Tier 3: Supplementary (boost=3) ---")
    for d in tiers["tier3"]:
        lines.append(f"$boost=3,site={d}")
    if tiers.get("discard"):
        lines.append("")
        lines.append("! --- Discard: Noise ---")
        for d in tiers["discard"]:
            lines.append(f"$discard,site={d}")
    path.write_text("\n".join(lines) + "\n")
    return path


def write_country_config(country: CountryArgs, verified_media: list[str]) -> Path:
    """Write a minimal country config YAML scaffold.

    Most fields require human review — actors, blind spots, and query vocabulary
    must be filled in from the dossier.
    """
    path = COUNTRY_CONFIG_DIR / f"{country.code}.yaml"
    config = {
        "country": country.name,
        "code": country.code,
        "tier": "pivot",  # human review
        "region": country.region,
        "actors": [
            {
                "name": "TODO: Primary leader",
                "role": "TODO: e.g. Prime Minister",
                "primary": True,
                "search_terms": ["TODO"],
            }
        ],
        "languages": {
            "primary": country.language,
            "additional": [],
            "metadata": "en",
        },
        "blind_spots": [
            {
                "domain": "TODO: from dossier section 0",
                "reason": "TODO",
                "where_signal_lives": "TODO",
            }
        ],
        "news_discovery": {
            "goggle_file": f"assets/country_goggles/{country.code}.goggle",
            "extraction_config": "assets/country_configs/extraction_routing.yaml",
            "brave_params": {
                "country": country.code.upper(),
                "search_lang": country.language,
                "freshness": "pw",
            },
            "query_vocabulary": {
                "diplomatic_alignment": ["TODO"],
                "security_defense": ["TODO"],
                "economic_tech": ["TODO"],
                "institutional": ["TODO"],
                "domestic_constraints": ["TODO"],
            },
        },
        "government_discovery": {
            "config_file": f"assets/government/{country.code}.yaml",
        },
        "interpretive_context_file": f"assets/context/{country.code}_sources.md",
        "search": {
            "triage_queries_max": 2,
            "deep_dive_queries_max": 20,
        },
    }
    with open(path, "w") as f:
        yaml.dump(config, f, sort_keys=False, allow_unicode=True)
    return path


def write_government_config(country: CountryArgs, verified_gov: list[str]) -> Path:
    path = GOVERNMENT_CONFIG_DIR / f"{country.code}.yaml"
    config = {
        "country": country.name,
        "code": country.code,
        "information_culture": "TODO: open|managed|opaque",
        "domains": [
            {
                "domain": d,
                "institutions": ["TODO: identify institution"],
                "priority": "P2",
            }
            for d in verified_gov
        ],
        "query_terms": [],
    }
    with open(path, "w") as f:
        yaml.dump(config, f, sort_keys=False, allow_unicode=True)
    return path


async def phase_4_config(state: OnboardingState) -> PhaseResult:
    country = state.country
    result = PhaseResult(phase=4, name="config_generation", status="ok")

    verification_path = country.workspace / "verification.json"
    if not verification_path.exists():
        result.status = "failed"
        result.errors.append("verification.json not found — run Phase 2 first")
        return result

    verification = json.loads(verification_path.read_text())
    verified_media = verification["verified_media"]
    verified_gov = verification["verified_gov"]

    # Load the audit text to get explicit tier assignments
    audit_path = SOURCE_MAPS_DIR / "_drafts" / f"{country.slug}_audit.md"
    audit_text = audit_path.read_text() if audit_path.exists() else ""

    tiers = classify_goggle_tiers(audit_text, verified_media, verified_gov)
    goggle_path = write_goggle_file(country, tiers)
    logger.info("Phase 4: goggle saved → %s", goggle_path)

    country_path = write_country_config(country, verified_media)
    logger.info("Phase 4: country config saved → %s (TODO fields require human review)", country_path)

    gov_path = write_government_config(country, verified_gov)
    logger.info("Phase 4: government config saved → %s", gov_path)

    result.outputs = {
        "goggle": str(goggle_path),
        "country_config": str(country_path),
        "government_config": str(gov_path),
    }
    return result


# =============================================================================
# Phase 5: Code integration
# =============================================================================


def add_country_to_regional_py(code: str, region: str) -> bool:
    """Insert the country code into REGION_COUNTRIES[Region.{REGION}] in regional.py.

    Returns True if the file was modified.
    """
    text = REGIONAL_PY_PATH.read_text()
    region_enum_attr = region.upper()

    # Find the line: Region.{REGION_ENUM_ATTR}: ["aa", "bb", ...]
    pattern = re.compile(
        rf"(Region\.{region_enum_attr}:\s*\[)([^\]]*)(\])"
    )
    m = pattern.search(text)
    if not m:
        logger.error("Could not find Region.%s entry in regional.py", region_enum_attr)
        return False

    existing_codes = [c.strip().strip('"').strip("'") for c in m.group(2).split(",") if c.strip()]
    if code in existing_codes:
        logger.info("Country %s already in REGION_COUNTRIES[%s]", code, region_enum_attr)
        return False

    new_codes = existing_codes + [code]
    formatted = ", ".join(f'"{c}"' for c in new_codes)
    new_text = text[:m.start()] + f"Region.{region_enum_attr}: [{formatted}]" + text[m.end():]
    REGIONAL_PY_PATH.write_text(new_text)
    logger.info("Added %s to REGION_COUNTRIES[%s] in regional.py", code, region_enum_attr)
    return True


async def phase_5_integration(state: OnboardingState) -> PhaseResult:
    country = state.country
    result = PhaseResult(phase=5, name="integration", status="ok")

    # Update regional.py
    try:
        modified = add_country_to_regional_py(country.code, country.region)
        result.outputs["regional_py_modified"] = "yes" if modified else "no (already present)"
    except Exception as e:
        result.status = "failed"
        result.errors.append(f"regional.py edit: {e}")
        return result

    # Validation triage scan
    logger.info("Phase 5: running validation triage scan for %s", country.code)
    proc = await asyncio.create_subprocess_exec(
        sys.executable, "-m", "src.monitor.cli", "run",
        "--country", country.code, "--triage-only", "--date", country.today,
        cwd=str(PROJECT_ROOT),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
    )
    stdout, _ = await proc.communicate()
    triage_log_path = country.workspace / "triage_validation.log"
    triage_log_path.write_text(stdout.decode("utf-8", errors="replace"))
    logger.info("Phase 5: triage validation log → %s (exit=%d)", triage_log_path, proc.returncode)

    if proc.returncode != 0:
        result.status = "failed"
        result.errors.append(f"triage validation failed (exit={proc.returncode})")
        return result

    result.outputs["triage_validation_log"] = str(triage_log_path)
    return result


# =============================================================================
# Phase 6: Final report
# =============================================================================


async def phase_6_report(state: OnboardingState) -> PhaseResult:
    country = state.country
    result = PhaseResult(phase=6, name="final_report", status="ok")

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS_DIR / f"{country.slug}_{country.today}.md"

    lines = [
        f"# {country.name} ({country.code}) onboarding report",
        f"_Generated {country.today}_",
        "",
        f"**Region:** {country.region}",
        f"**Workspace:** `{country.workspace}`",
        "",
        "## Phase outputs",
        "",
    ]
    for phase_id in sorted(state.phase_results.keys()):
        pr = state.phase_results[phase_id]
        status_marker = {"ok": "✅", "failed": "❌", "skipped": "⏭"}.get(pr.status, "?")
        lines.append(f"### {status_marker} Phase {phase_id}: {pr.name} ({pr.status})")
        lines.append("")
        if pr.outputs:
            for key, val in pr.outputs.items():
                lines.append(f"- **{key}**: `{val}`")
        if pr.errors:
            lines.append("")
            lines.append("**Errors:**")
            for err in pr.errors:
                lines.append(f"- {err}")
        lines.append("")

    lines.extend([
        "## Required human review",
        "",
        f"- [ ] Edit `assets/country_configs/countries/{country.code}.yaml` — fill in TODO fields (actors, blind spots, query vocabulary) from dossier",
        f"- [ ] Edit `assets/government/{country.code}.yaml` — set information_culture and identify institutions per domain",
        f"- [ ] Review `assets/country_dossiers/{country.slug}_dossier_{country.today}.md` for accuracy",
        f"- [ ] Review `assets/country_goggles/{country.code}.goggle` and adjust tier classification",
        f"- [ ] Add Guardian tag in `src/monitor/collection/guardian.py` if applicable",
        f"- [ ] Run full single-country pipeline: `python -m src.monitor.cli run --country {country.code}`",
        "",
    ])

    report_path.write_text("\n".join(lines))
    logger.info("Phase 6: report saved → %s", report_path)
    result.outputs = {"report": str(report_path)}
    return result


# =============================================================================
# CLI
# =============================================================================


PHASES = {
    1: phase_1_dossier,
    2: phase_2_sources,
    3: phase_3_extraction,
    4: phase_4_config,
    5: phase_5_integration,
    6: phase_6_report,
}


async def run(args: argparse.Namespace) -> None:
    country = CountryArgs(
        name=args.name,
        code=args.code,
        region=args.region,
        language=args.language,
    )
    state = OnboardingState.load_or_init(country)
    state.country.workspace.mkdir(parents=True, exist_ok=True)

    if args.phase:
        phases_to_run = [args.phase]
    else:
        phases_to_run = list(PHASES.keys())

    for phase_id in phases_to_run:
        if not args.resume and phase_id in state.phase_results and state.phase_results[phase_id].status == "ok":
            logger.info("Phase %d already complete, skipping (use --resume to re-run only failed phases)", phase_id)
            continue
        if args.resume and phase_id in state.phase_results and state.phase_results[phase_id].status == "ok":
            logger.info("Phase %d already complete, skipping (--resume mode)", phase_id)
            continue

        logger.info("=" * 70)
        logger.info("Phase %d: starting", phase_id)
        logger.info("=" * 70)
        phase_func = PHASES[phase_id]
        result = await phase_func(state)
        state.mark(result)

        if result.status == "failed":
            logger.error("Phase %d failed: %s", phase_id, "; ".join(result.errors))
            logger.error("Fix the issue and re-run with --resume")
            sys.exit(1)

        logger.info("Phase %d complete (%s)", phase_id, result.status)

    logger.info("=" * 70)
    logger.info("All requested phases complete for %s (%s)", country.name, country.code)
    logger.info("=" * 70)


def main() -> None:
    parser = argparse.ArgumentParser(description="Onboard a new country to the MPM pipeline")
    parser.add_argument("name", help="Country name (e.g. Pakistan)")
    parser.add_argument("code", help="2-letter ISO code (e.g. pk)")
    parser.add_argument("region", choices=sorted(VALID_REGIONS), help="Target region enum value")
    parser.add_argument("--language", default="en", help="Primary language for source curation (default: en)")
    parser.add_argument("--phase", type=int, choices=list(PHASES.keys()), help="Run only this phase")
    parser.add_argument("--resume", action="store_true", help="Resume — re-run failed phases, skip completed ones")
    args = parser.parse_args()

    asyncio.run(run(args))


if __name__ == "__main__":
    main()

"""
Ledger initialization: cold-start a country ledger from its dossier + config.

Step 1 (mechanical): Extract structural fields and claims from config + dossier.
Step 2 (LLM call): Generate initial posture summary and signal category assessments.
"""

import logging
import os
import re
from datetime import date
from pathlib import Path

from ..rate_limit import anthropic_limiter
from ..config import (
    ANTHROPIC_API_KEY,
    MODEL,
    THINKING_BUDGET_TOKENS,
    CategoryStatus,
    ClaimStatus,
    CountryConfig,
    SignalCategory,
    load_prompt,
)
from ..models import (
    ActorRef,
    CountryLedger,
    PostureSummary,
    SignalCategoryAssessment,
    StructuralClaimStatus,
)
from ..sanitize import _record_fallback, extract_json

logger = logging.getLogger(__name__)

USE_TOOL_SCHEMA = os.getenv("MPM_USE_TOOL_SCHEMA", "0") == "1"


def _init_tool_schema() -> dict:
    """Build the ledger-init tool schema dynamically — one per SignalCategory."""
    category_props = {
        cat.value: {
            "type": "object",
            "required": ["current_assessment"],
            "properties": {
                "current_assessment": {"type": "string"},
                "confidence_rationale": {"type": "string"},
            },
        }
        for cat in SignalCategory
    }
    return {
        "name": "record_ledger_initialization",
        "description": (
            "Record the initial posture summary and per-category baseline "
            "assessments for a country ledger. Call exactly once."
        ),
        "input_schema": {
            "type": "object",
            "required": ["posture_text", "categories"],
            "properties": {
                "posture_text": {"type": "string"},
                "categories": {
                    "type": "object",
                    "required": list(category_props.keys()),
                    "properties": category_props,
                },
            },
        },
    }


LEDGER_INIT_TOOL_NAME = "record_ledger_initialization"
LEDGER_INIT_TOOL = _init_tool_schema()


# =============================================================================
# Step 1: Mechanical extraction (no API call)
# =============================================================================

def extract_structural_claims(dossier_text: str) -> list[dict]:
    """
    Extract [STRUC-XX] claims from a country dossier.

    Returns list of dicts with claim_ref, claim_text, dossier_section, status.
    Reuses the claim block parsing pattern from src/context/claims.py.
    """
    claims = []
    global_counter = 1

    # Find STRUCTURAL CLAIMS blocks
    block_pattern = re.compile(
        r"\*{0,2}(?:STRUCTURAL CLAIMS):?\*{0,2}\s*\n(.*?)(?=\n---|\n####|\n##[^#]|\Z)",
        re.DOTALL,
    )

    # Find section headers to determine which dossier section each block belongs to
    section_pattern = re.compile(
        r"^#{2,4}\s+(?:(\d+)\.\s+)?(.+?)$", re.MULTILINE
    )
    section_headers = list(section_pattern.finditer(dossier_text))

    for block_match in block_pattern.finditer(dossier_text):
        block_text = block_match.group(1).strip()
        block_start = block_match.start()

        # Find which numbered section this block is in
        section_num = 0
        for header in section_headers:
            if header.start() < block_start:
                if header.group(1):
                    section_num = int(header.group(1))
            else:
                break

        # Parse numbered items: "1. Claim text **[HIGH CONFIDENCE]**"
        item_pattern = re.compile(r"^\s*(\d+)\.\s+(.+?)$", re.MULTILINE)
        items = list(item_pattern.finditer(block_text))

        for i, item_match in enumerate(items):
            start = item_match.start(2)
            end = items[i + 1].start() if i + 1 < len(items) else len(block_text)
            full_text = block_text[start:end].strip()
            full_text = re.sub(r"\n\s*", " ", full_text)

            # Strip confidence markers
            clean_text = re.sub(
                r"\s*\*?\*?\[?(HIGH CONFIDENCE|MODERATE CONFIDENCE|ASSESSED)\]?\*?\*?\s*",
                "", full_text,
            ).strip().rstrip(" —-.")
            if clean_text and not clean_text.endswith("."):
                clean_text += "."

            claim_ref = f"STRUC-{global_counter:02d}"

            claims.append({
                "claim_ref": claim_ref,
                "claim_text": clean_text,
                "dossier_section": section_num,
                "status": ClaimStatus.CONFIRMED,
                "last_checked": date.today(),
                "evidence_summary": "Baseline — not yet tested against weekly evidence.",
                "weeks_under_pressure": 0,
                "recommendation": "",
            })
            global_counter += 1

    return claims


def mechanical_extract(config: CountryConfig) -> dict:
    """
    Step 1: Build the ledger skeleton from config + dossier.

    Returns a dict ready to be passed to CountryLedger (after LLM fills
    posture_summary and signal_categories).
    """
    dossier_path = config.dossier_path
    dossier_text = dossier_path.read_text()
    claims = extract_structural_claims(dossier_text)
    today = date.today()

    return {
        "country": config.country,
        "code": config.code,
        "tier": config.tier.value,
        "actors": [
            ActorRef(name=a.name, role=a.role, primary=a.primary)
            for a in config.actors
        ],
        "last_updated": today,
        "created": today,
        "weekly_entries": [],
        "structural_claim_status": [
            StructuralClaimStatus(**c) for c in claims
        ],
        "corrections_log": [],
        "consolidated_history": "",
    }


# =============================================================================
# Step 2: LLM initialization call
# =============================================================================

INIT_SYSTEM_PROMPT = load_prompt("ledger/initialize")


def _build_init_prompt(config: CountryConfig, dossier_text: str) -> str:
    actor_lines = []
    for a in config.actors:
        marker = " (primary)" if a.primary else ""
        actor_lines.append(f"- {a.name}: {a.role}{marker}")
    actors_block = "\n".join(actor_lines)

    return f"""\
Initialize the monitoring ledger for {config.country} ({config.code.upper()}).

Tier: {config.tier.value}
Region: {config.region.value}

Key actors:
{actors_block}

--- BEGIN COUNTRY DOSSIER ---

{dossier_text}

--- END COUNTRY DOSSIER ---

Produce the JSON object as specified in your instructions."""


def parse_init_data(data: dict) -> dict:
    """Build posture_summary + signal_categories from an already-parsed dict."""
    today = date.today()

    posture_summary = PostureSummary(
        as_of=today,
        text=data["posture_text"],
        category_status={c: CategoryStatus.QUIET for c in SignalCategory},
        last_deep_dive=None,
        consecutive_maintenance_weeks=0,
    )

    signal_categories = {}
    for cat in SignalCategory:
        cat_data = data["categories"][cat.value]
        signal_categories[cat] = SignalCategoryAssessment(
            current_assessment=cat_data["current_assessment"],
            confidence=3,  # baseline
            confidence_rationale=cat_data.get("confidence_rationale", "Baseline from dossier."),
            key_actors=[],
            dossier_sections_referenced=[],
            last_updated=today,
        )

    return {
        "posture_summary": posture_summary,
        "signal_categories": signal_categories,
    }


def parse_init_response(response_text: str) -> dict:
    """Parse the LLM's JSON response into posture_summary + signal_categories."""
    data = extract_json(response_text, context="init_response")
    return parse_init_data(data)


async def llm_initialize(config: CountryConfig) -> dict:
    """
    Step 2: Call the LLM to produce initial posture summary and assessments.

    Returns dict with posture_summary and signal_categories.
    """
    import anthropic

    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY not set")

    dossier_text = config.dossier_path.read_text()
    prompt = _build_init_prompt(config, dossier_text)

    client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)
    create_kwargs: dict = dict(
        model=MODEL,
        max_tokens=THINKING_BUDGET_TOKENS + 4096,
        temperature=1,  # required for extended thinking
        thinking={
            "type": "enabled",
            "budget_tokens": THINKING_BUDGET_TOKENS,
        },
        system=[{"type": "text", "text": INIT_SYSTEM_PROMPT}],
        messages=[{"role": "user", "content": prompt}],
    )
    if USE_TOOL_SCHEMA:
        create_kwargs["tools"] = [LEDGER_INIT_TOOL]

    async with anthropic_limiter():
        response = await client.messages.create(**create_kwargs)

    # Extract text blocks, skip thinking blocks
    text_parts = [
        block.text for block in response.content
        if block.type == "text"
    ]
    response_text = "\n".join(text_parts)

    tool_input: dict | None = None
    if USE_TOOL_SCHEMA:
        for block in response.content:
            if (getattr(block, "type", None) == "tool_use"
                    and getattr(block, "name", None) == LEDGER_INIT_TOOL_NAME):
                tool_input = getattr(block, "input", None)
                break

    logger.info(
        f"Initialization call for {config.code}: "
        f"input_tokens={response.usage.input_tokens}, "
        f"output_tokens={response.usage.output_tokens}"
        f"{' [tool_use]' if tool_input else ''}"
    )

    from ..trace import save_raw_response, update_trace_parsed, extract_thinking, extract_usage

    if tool_input is not None:
        import json as _json
        save_raw_response(
            "initialization", config.code, date.today(),
            system_prompt=INIT_SYSTEM_PROMPT,
            user_message=prompt,
            response_text=_json.dumps(tool_input, indent=2, ensure_ascii=False),
            thinking_text=extract_thinking(response),
            usage=extract_usage(response),
        )
        parsed = parse_init_data(tool_input)
    else:
        if USE_TOOL_SCHEMA:
            logger.warning(
                "Initialize %s: tool_use enabled but no valid block; falling back",
                config.code,
            )
            _record_fallback("initialize_tool_use_fallback")
        save_raw_response(
            "initialization", config.code, date.today(),
            system_prompt=INIT_SYSTEM_PROMPT,
            user_message=prompt,
            response_text=response_text,
            thinking_text=extract_thinking(response),
            usage=extract_usage(response),
        )
        parsed = parse_init_response(response_text)
    update_trace_parsed("initialization", config.code, date.today(), parsed_output=parsed)

    return parsed


async def initialize_country_ledger(config: CountryConfig) -> CountryLedger:
    """
    Full initialization: mechanical extraction + LLM call.

    Returns a validated CountryLedger ready to save.
    """
    logger.info(f"Initializing ledger for {config.country} ({config.code})")

    # Step 1: mechanical
    skeleton = mechanical_extract(config)

    # Step 2: LLM
    llm_output = await llm_initialize(config)

    # Merge
    skeleton["posture_summary"] = llm_output["posture_summary"]
    skeleton["signal_categories"] = llm_output["signal_categories"]

    ledger = CountryLedger(**skeleton)
    logger.info(
        f"Ledger initialized for {config.code}: "
        f"{len(skeleton['structural_claim_status'])} structural claims extracted"
    )
    return ledger

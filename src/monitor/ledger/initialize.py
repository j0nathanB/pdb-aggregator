"""
Ledger initialization: cold-start a country ledger from its dossier + config.

Step 1 (mechanical): Extract structural fields and claims from config + dossier.
Step 2 (LLM call): Generate initial posture summary and signal category assessments.
"""

import logging
import re
from datetime import date
from pathlib import Path

from ..config import (
    ANTHROPIC_API_KEY,
    MODEL,
    THINKING_BUDGET_TOKENS,
    CategoryStatus,
    ClaimStatus,
    CountryConfig,
    SignalCategory,
)
from ..models import (
    ActorRef,
    CountryLedger,
    PostureSummary,
    SignalCategoryAssessment,
    StructuralClaimStatus,
)
from ..sanitize import extract_json

logger = logging.getLogger(__name__)


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

INIT_SYSTEM_PROMPT = """\
You are an analytical intelligence officer initializing a country monitoring ledger.

You will read a structural country dossier and produce:
1. A posture summary (3-5 sentences) describing the country's current structural position
2. A baseline assessment for each of five signal categories

This is a STRUCTURAL BASELINE derived from the dossier, not a news analysis. \
Describe the country's standing position as documented in the dossier. \
All confidence scores should be 3 (baseline — not yet tested against weekly evidence).

Respond with a JSON object matching this schema exactly:

{
  "posture_text": "3-5 sentence structural baseline...",
  "categories": {
    "alignment_diplomatic": {
      "current_assessment": "Running analytical picture for this category...",
      "confidence_rationale": "Baseline from dossier, not yet tested."
    },
    "security_defense": { ... },
    "economic_tech": { ... },
    "institutional": { ... },
    "domestic_regime": { ... }
  }
}

Rules:
- Each assessment should be 2-4 sentences drawn from the dossier's structural analysis.
- Do NOT speculate about current events. Describe the structural baseline.
- Do NOT include news, predictions, or recommendations.
- Respond with valid JSON only. No markdown fencing, no commentary."""


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


def parse_init_response(response_text: str) -> dict:
    """Parse the LLM's JSON response into posture_summary + signal_categories."""
    data = extract_json(response_text, context="init_response")

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
    response = await client.messages.create(
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

    # Extract text blocks, skip thinking blocks
    text_parts = [
        block.text for block in response.content
        if block.type == "text"
    ]
    response_text = "\n".join(text_parts)

    logger.info(
        f"Initialization call for {config.code}: "
        f"input_tokens={response.usage.input_tokens}, "
        f"output_tokens={response.usage.output_tokens}"
    )

    parsed = parse_init_response(response_text)

    from ..trace import save_trace, extract_thinking, extract_usage
    save_trace(
        "initialization", config.code, date.today(),
        system_prompt=INIT_SYSTEM_PROMPT,
        user_message=prompt,
        response_text=response_text,
        parsed_output=parsed,
        thinking_text=extract_thinking(response),
        usage=extract_usage(response),
    )

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

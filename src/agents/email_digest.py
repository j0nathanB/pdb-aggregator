"""
Email Digest Agent - condenses a WeeklyBrief into a tight email digest.

Produces a short lede summarizing top stories, then per-region paragraphs
that combine leaders within each region (not per-leader).
"""

import logging
from dataclasses import dataclass, field

from ..config import (
    WeeklyBrief,
    COUNTRY_SUBREGION,
    REGION_DISPLAY_NAMES,
    REGION_ORDER,
)
from .base import complete, extract_json_from_response, with_retry

logger = logging.getLogger(__name__)


@dataclass
class RegionDigest:
    """A condensed paragraph covering one region's key developments."""
    name: str
    summary: str


@dataclass
class EmailDigest:
    """The condensed email digest output."""
    lede: str  # 3-5 sentence "This week" summary
    regions: list[RegionDigest] = field(default_factory=list)


SYSTEM_PROMPT = """\
You are a senior editor at a geopolitical intelligence firm. Your job is to \
condense a weekly intelligence brief into a tight email digest for busy \
executives. Write in crisp, authoritative prose. No filler, no hedging.

Rules:
- The "lede" is 3-5 sentences starting with "This week" that covers the most \
important developments across all regions.
- Each region gets ONE paragraph that weaves together the key stories for ALL \
leaders in that region. Do not use sub-headings or bullet points within a \
region paragraph.
- Name leaders by surname only (e.g., "Macron", "Starmer") after first mention.
- Keep the total digest under 600 words.
- Output valid JSON only, no markdown fencing."""


def _build_prompt(brief: WeeklyBrief) -> str:
    """Build the user prompt from brief data."""
    parts = []

    # Executive summary
    if brief.executive_summary:
        parts.append(f"EXECUTIVE SUMMARY:\n{brief.executive_summary}")

    # Main stories
    if brief.main_stories:
        parts.append("\nTOP STORIES:")
        for story in brief.main_stories:
            leaders = ""
            if story.contributing_leaders:
                leaders = f" [{', '.join(story.contributing_leaders)}]"
            parts.append(f"- {story.title}{leaders}: {story.narrative[:300]}")

    # Per-region leader summaries
    region_dossiers: dict[str, list] = {}
    for dossier in brief.leader_dossiers:
        country = dossier.leader.country
        region = COUNTRY_SUBREGION.get(country, dossier.leader.region)
        if region not in region_dossiers:
            region_dossiers[region] = []
        region_dossiers[region].append(dossier)

    parts.append("\nPER-REGION LEADER DETAILS:")
    for region in REGION_ORDER:
        if region not in region_dossiers:
            continue
        region_name = REGION_DISPLAY_NAMES.get(
            region, region.replace("_", " ").title()
        )
        parts.append(f"\n## {region_name}")
        for dossier in region_dossiers[region]:
            parts.append(
                f"\n{dossier.leader.name} ({dossier.leader.title}, "
                f"{dossier.leader.country}):"
            )
            if dossier.executive_summary:
                parts.append(f"  Summary: {dossier.executive_summary}")
            for story in (dossier.main_stories + dossier.international_stories)[
                :3
            ]:
                parts.append(f"  - {story.title}")

    # Remaining regions not in REGION_ORDER
    for region in sorted(region_dossiers.keys()):
        if region in REGION_ORDER:
            continue
        region_name = REGION_DISPLAY_NAMES.get(
            region, region.replace("_", " ").title()
        )
        parts.append(f"\n## {region_name}")
        for dossier in region_dossiers[region]:
            parts.append(
                f"\n{dossier.leader.name} ({dossier.leader.title}, "
                f"{dossier.leader.country}):"
            )
            if dossier.executive_summary:
                parts.append(f"  Summary: {dossier.executive_summary}")
            for story in (dossier.main_stories + dossier.international_stories)[
                :3
            ]:
                parts.append(f"  - {story.title}")

    # Collect region names for the expected output
    ordered_regions = []
    for region in REGION_ORDER:
        if region in region_dossiers:
            ordered_regions.append(
                REGION_DISPLAY_NAMES.get(
                    region, region.replace("_", " ").title()
                )
            )
    for region in sorted(region_dossiers.keys()):
        if region not in REGION_ORDER and region in region_dossiers:
            ordered_regions.append(
                REGION_DISPLAY_NAMES.get(
                    region, region.replace("_", " ").title()
                )
            )

    parts.append(f"""
Condense the above into an email digest. Return JSON:
{{
  "lede": "This week ...",
  "regions": [
    {', '.join(f'{{"name": "{r}", "summary": "..."}}' for r in ordered_regions)}
  ]
}}""")

    return "\n".join(parts)


class EmailDigestAgent:
    """Condenses a WeeklyBrief into a short email digest."""

    @with_retry(max_attempts=3)
    async def generate_digest(self, brief: WeeklyBrief) -> EmailDigest:
        """
        Generate a condensed email digest from a weekly brief.

        Args:
            brief: The full WeeklyBrief to condense

        Returns:
            EmailDigest with lede and per-region summaries
        """
        prompt = _build_prompt(brief)

        response = await complete(
            prompt=prompt,
            system=SYSTEM_PROMPT,
            temperature=0.3,
            max_tokens=2000,
        )

        data = extract_json_from_response(response)
        if not data:
            raise ValueError(
                f"Failed to extract JSON from email digest response: "
                f"{response[:200]}"
            )

        regions = []
        for r in data.get("regions", []):
            regions.append(
                RegionDigest(
                    name=r.get("name", ""),
                    summary=r.get("summary", ""),
                )
            )

        digest = EmailDigest(
            lede=data.get("lede", ""),
            regions=regions,
        )

        logger.info(
            f"Email digest generated: {len(digest.lede)} char lede, "
            f"{len(digest.regions)} regions"
        )

        return digest

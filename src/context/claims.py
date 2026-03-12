"""
Claims extraction from country dossiers and leader profiles.

Parses [STRUC-XX] and [PROF-XX] claims from markdown documents and
produces a condensed Claims Index for system prompt injection.
"""

import re
from dataclasses import dataclass


@dataclass
class Claim:
    """A single extracted claim from a baseline document."""
    ref: str  # e.g., "[STRUC-01]" or "[PROF-03]"
    text: str  # Full claim text
    confidence: str  # HIGH CONFIDENCE / MODERATE CONFIDENCE / ASSESSED
    section: str  # Source section title


def extract_claims(
    document_text: str,
    namespace: str,
) -> list[Claim]:
    """
    Extract numbered claims from a country dossier or leader profile.

    Dossiers use STRUCTURAL CLAIMS blocks with bare numbers (1, 2, 3...).
    Profiles use PROFILE CLAIMS blocks with bare numbers.

    This function reads both formats and produces namespaced references:
    - namespace="STRUC" -> [STRUC-01], [STRUC-02], ...
    - namespace="PROF" -> [PROF-01], [PROF-02], ...

    Args:
        document_text: Full markdown text of the document
        namespace: "STRUC" for country dossiers, "PROF" for leader profiles

    Returns:
        List of Claims with namespaced references, in document order.
    """
    claims = []
    global_counter = 1

    # Find all STRUCTURAL CLAIMS or PROFILE CLAIMS blocks
    block_pattern = re.compile(
        r"\*{0,2}(?:STRUCTURAL CLAIMS|PROFILE CLAIMS):?\*{0,2}\s*\n(.*?)(?=\n---|\n####|\n##[^#]|\Z)",
        re.DOTALL,
    )

    # Find the section each block belongs to
    section_pattern = re.compile(r"^#{2,4}\s+(?:\d+\.\s+)?(.+?)$", re.MULTILINE)
    section_headers = list(section_pattern.finditer(document_text))

    for block_match in block_pattern.finditer(document_text):
        block_text = block_match.group(1).strip()
        block_start = block_match.start()

        # Find which section this block is in
        section_name = ""
        for header in section_headers:
            if header.start() < block_start:
                section_name = header.group(1).strip()
            else:
                break

        # Parse numbered items
        # Match patterns like:
        #   1. Claim text **[HIGH CONFIDENCE]**
        #   2. Claim text [MODERATE CONFIDENCE]
        item_pattern = re.compile(
            r"^\s*(\d+)\.\s+(.+?)$",
            re.MULTILINE,
        )

        items = list(item_pattern.finditer(block_text))
        for i, item_match in enumerate(items):
            # Get full text until next numbered item or end of block
            start = item_match.start(2)
            if i + 1 < len(items):
                end = items[i + 1].start()
            else:
                end = len(block_text)

            full_text = block_text[start:end].strip()
            # Join multi-line text
            full_text = re.sub(r"\n\s*", " ", full_text)

            # Extract confidence marker
            confidence = "ASSESSED"
            conf_match = re.search(
                r"\*?\*?\[?(HIGH CONFIDENCE|MODERATE CONFIDENCE|ASSESSED)\]?\*?\*?",
                full_text,
            )
            if conf_match:
                confidence = conf_match.group(1)

            # Clean the text — remove confidence markers and surrounding formatting
            clean_text = re.sub(
                r"\s*\*?\*?\[?(HIGH CONFIDENCE|MODERATE CONFIDENCE|ASSESSED)\]?\*?\*?\s*",
                "",
                full_text,
            ).strip()
            # Remove trailing punctuation artifacts
            clean_text = clean_text.rstrip(" —-.")
            if clean_text and not clean_text.endswith("."):
                clean_text += "."

            ref = f"[{namespace}-{global_counter:02d}]"

            claims.append(Claim(
                ref=ref,
                text=clean_text,
                confidence=confidence,
                section=section_name,
            ))
            global_counter += 1

    return claims


def format_claims_index(
    structural_claims: list[Claim],
    profile_claims: list[Claim],
    country: str,
    leader_name: str,
) -> str:
    """
    Format claims into the Claims Index block for system prompt injection.

    Placed near the task instructions in the user prompt per v3 spec.

    Output format:
        ## CLAIMS INDEX (for reference)

        ### Country Structural Claims (France)
        [STRUC-01]: One-sentence summary
        [STRUC-02]: One-sentence summary
        ...

        ### Leader Profile Claims (Emmanuel Macron)
        [PROF-01]: One-sentence summary
        ...
    """
    lines = ["## CLAIMS INDEX (for reference)", ""]

    lines.append(f"### Country Structural Claims ({country})")
    if structural_claims:
        for claim in structural_claims:
            # Use first sentence as summary
            summary = _first_sentence(claim.text)
            lines.append(f"{claim.ref}: {summary}")
    else:
        lines.append("[No structural claims available]")
    lines.append("")

    lines.append(f"### Leader Profile Claims ({leader_name})")
    if profile_claims:
        for claim in profile_claims:
            summary = _first_sentence(claim.text)
            lines.append(f"{claim.ref}: {summary}")
    else:
        lines.append("[No profile claims available]")

    return "\n".join(lines)


def get_valid_claim_refs(
    structural_claims: list[Claim],
    profile_claims: list[Claim],
) -> set[str]:
    """Return the set of valid claim reference strings for validation."""
    return {c.ref for c in structural_claims} | {c.ref for c in profile_claims}


def _first_sentence(text: str) -> str:
    """Extract the first sentence from claim text, truncating if needed."""
    # Common abbreviations to avoid splitting on
    protected = text
    abbrevs = [r"U\.S\.", r"U\.K\.", r"U\.N\.", r"E\.U\.", r"e\.g\.", r"i\.e\."]
    for abbrev in abbrevs:
        protected = re.sub(abbrev, abbrev.replace(r"\.", "\x00"), protected)

    # Find first sentence boundary
    match = re.search(r"\.\s+[A-Z]", protected)
    if match:
        return text[: match.start() + 1]

    # No clear sentence boundary — return full text, truncated
    if len(text) > 200:
        return text[:197] + "..."
    return text

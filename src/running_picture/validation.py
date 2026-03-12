"""
Running Picture entry validation against the v3 schema.

Checks field presence, thread accounting, claim reference format,
and quality heuristics.
"""

import re
from dataclasses import dataclass, field
from typing import Optional

from .schema import parse_frontmatter


@dataclass
class ValidationResult:
    """Result of validating a running picture entry."""
    valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def correction_prompt(self) -> str:
        """Generate a correction prompt for auto-retry on validation failure."""
        if self.valid:
            return ""
        parts = ["Your output failed validation. Fix these issues:\n"]
        for e in self.errors:
            parts.append(f"- ERROR: {e}")
        for w in self.warnings:
            parts.append(f"- WARNING: {w}")
        parts.append("\nRegenerate the complete entry with all issues fixed.")
        return "\n".join(parts)


# Required sections in a valid v3 entry
REQUIRED_SECTIONS = [
    "Activity Level",
    "Key Actions",
    "Commitments & Positions",
    "Relationships",
    "Domestic Political Position",
    "Developing Threads",
    "Missing Thread Audit",
    "Structural Claim Check",
    "Analytical Notes",
]

# Required frontmatter fields
REQUIRED_FRONTMATTER = ["leader", "country", "week_of", "generated_at"]

# Valid claim reference pattern
CLAIM_REF_PATTERN = re.compile(r"\[(?:STRUC|PROF)-\d+\]")

# Invalid bare-number claim pattern (should be namespaced)
BARE_CLAIM_PATTERN = re.compile(r"(?<!\[)(?:structural claim|profile claim)\s+#?\d+", re.IGNORECASE)


def validate_entry(
    entry_text: str,
    prior_thread_count: Optional[int] = None,
    valid_claims: Optional[set[str]] = None,
) -> ValidationResult:
    """
    Validate a running picture entry against the v3 schema.

    Args:
        entry_text: Raw markdown text of the entry
        prior_thread_count: Expected number of threads from prior entry
            (for Missing Thread Audit count check). None skips this check.
        valid_claims: Set of valid claim references (e.g., {"[STRUC-01]", "[PROF-03]"}).
            None skips claim existence validation.

    Returns:
        ValidationResult with errors and warnings.
    """
    errors = []
    warnings = []

    # --- Frontmatter ---
    fm = parse_frontmatter(entry_text)
    if fm is None:
        errors.append("Missing frontmatter (--- delimited YAML block)")
    else:
        for field_name in REQUIRED_FRONTMATTER:
            if field_name not in fm:
                errors.append(f"Missing frontmatter field: {field_name}")

        if "week_of" in fm and not re.match(r"\d{4}-\d{2}-\d{2}", fm["week_of"]):
            errors.append(f"Invalid week_of format: {fm['week_of']} (expected YYYY-MM-DD)")

    # --- Required sections ---
    for section in REQUIRED_SECTIONS:
        if f"### {section}" not in entry_text:
            errors.append(f"Missing required section: ### {section}")

    # --- Key Actions: source attribution ---
    _check_key_actions(entry_text, errors, warnings)

    # --- Commitments: Audience and Binding Force ---
    _check_commitments(entry_text, errors, warnings)

    # --- Developing Threads: ACTIVE/DORMANT subsections ---
    _check_threads(entry_text, errors, warnings)

    # --- Missing Thread Audit: count check ---
    if prior_thread_count is not None:
        _check_thread_audit(entry_text, prior_thread_count, errors, warnings)

    # --- Claim references: namespace format ---
    _check_claims(entry_text, valid_claims, errors, warnings)

    # --- Structural Claim Check: quantity heuristic ---
    _check_claim_check_section(entry_text, warnings)

    return ValidationResult(
        valid=len(errors) == 0,
        errors=errors,
        warnings=warnings,
    )


def _extract_section(text: str, section_name: str) -> str:
    """Extract content of a ### section."""
    pattern = re.compile(
        rf"### {re.escape(section_name)}\n(.*?)(?=\n### |\Z)", re.DOTALL
    )
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def _check_key_actions(text: str, errors: list, warnings: list):
    """Check Key Actions have Source attributions."""
    content = _extract_section(text, "Key Actions")
    if not content:
        return

    numbered = re.findall(r"^\d+\.", content, re.MULTILINE)
    sources = re.findall(r"Source:", content)

    if numbered and len(sources) < len(numbered):
        errors.append(
            f"Key Actions: {len(numbered)} items but only "
            f"{len(sources)} Source attributions (each requires Source field)"
        )


def _check_commitments(text: str, errors: list, warnings: list):
    """Check Commitments have Audience and Binding Force fields."""
    content = _extract_section(text, "Commitments & Positions")
    if not content or content.startswith("[No") or content.startswith("No new"):
        return

    items = re.findall(r"^- \[", content, re.MULTILINE)
    if not items:
        return

    audience_count = len(re.findall(r"Audience:", content))
    binding_count = len(re.findall(r"Binding force:", content, re.IGNORECASE))
    status_count = len(re.findall(r"Status:", content))

    if status_count < len(items):
        errors.append(
            f"Commitments: {len(items)} items but only {status_count} Status fields"
        )
    if audience_count < len(items):
        warnings.append(
            f"Commitments: {len(items)} items but only {audience_count} Audience fields"
        )
    if binding_count < len(items):
        warnings.append(
            f"Commitments: {len(items)} items but only {binding_count} Binding force fields"
        )


def _check_threads(text: str, errors: list, warnings: list):
    """Check Developing Threads has ACTIVE/DORMANT structure and required fields."""
    content = _extract_section(text, "Developing Threads")
    if not content:
        return

    # Check for ACTIVE/DORMANT subsections
    has_active = "ACTIVE THREADS:" in content
    has_dormant = "DORMANT THREADS:" in content

    if not has_active and not has_dormant:
        # Might be a quiet week with "[No active threads.]"
        if not content.startswith("[No") and not content.startswith("No "):
            warnings.append(
                "Developing Threads should have ACTIVE THREADS: and/or "
                "DORMANT THREADS: subsections"
            )

    # Check active threads have required fields
    active_section = ""
    if has_active:
        active_start = content.index("ACTIVE THREADS:")
        dormant_start = content.index("DORMANT THREADS:") if has_dormant else len(content)
        active_section = content[active_start:dormant_start]

    thread_items = re.findall(r"^- \[", active_section, re.MULTILINE) if active_section else []
    if thread_items:
        watch_count = len(re.findall(r"Watch for:", active_section))
        originated_count = len(re.findall(r"Originated:", active_section))
        last_updated_count = len(re.findall(r"Last updated:", active_section))

        if watch_count < len(thread_items):
            warnings.append(
                f"Active Threads: {len(thread_items)} items but only "
                f"{watch_count} 'Watch for' fields"
            )
        if originated_count < len(thread_items):
            warnings.append(
                f"Active Threads: {len(thread_items)} items but only "
                f"{originated_count} 'Originated' fields"
            )
        if last_updated_count < len(thread_items):
            warnings.append(
                f"Active Threads: {len(thread_items)} items but only "
                f"{last_updated_count} 'Last updated' fields"
            )


def _check_thread_audit(text: str, prior_count: int, errors: list, warnings: list):
    """Check Missing Thread Audit accounts for all prior threads."""
    content = _extract_section(text, "Missing Thread Audit")
    if not content:
        if prior_count > 0:
            errors.append(
                f"Missing Thread Audit is empty but prior entry had "
                f"{prior_count} threads to account for"
            )
        return

    audit_items = re.findall(r"^- \[", content, re.MULTILINE)
    if len(audit_items) < prior_count:
        warnings.append(
            f"Missing Thread Audit has {len(audit_items)} items but "
            f"prior entry had {prior_count} threads"
        )


def _check_claims(
    text: str,
    valid_claims: Optional[set[str]],
    errors: list,
    warnings: list,
):
    """Check claim references use proper namespacing and exist in baseline docs."""
    # Check for bare (un-namespaced) claim references
    bare_matches = BARE_CLAIM_PATTERN.findall(text)
    if bare_matches:
        errors.append(
            f"Un-namespaced claim references found: {bare_matches[:3]}. "
            f"Use [STRUC-XX] or [PROF-XX] format."
        )

    if valid_claims is None:
        return

    # Find all claim references in the text
    refs = set(CLAIM_REF_PATTERN.findall(text))
    invalid = refs - valid_claims
    if invalid:
        warnings.append(
            f"Claim references not found in baseline documents: "
            f"{sorted(invalid)}"
        )


def _check_claim_check_section(text: str, warnings: list):
    """Heuristic check on Structural Claim Check section."""
    content = _extract_section(text, "Structural Claim Check")
    if not content:
        return

    # Skip if explicitly "none"
    if content.lower().startswith("no structural") or content.lower().startswith("none"):
        return

    items = re.findall(r"^- \[", content, re.MULTILINE)
    if len(items) > 5:
        warnings.append(
            f"Structural Claim Check has {len(items)} items "
            f"(expected 1-3; >5 suggests over-flagging)"
        )

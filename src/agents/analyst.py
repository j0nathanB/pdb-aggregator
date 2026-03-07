"""
Phase 1 Analyst Agent — per-leader analysis producing running picture entries
and analytical assessments.

Call A: Structured running picture entry (data logging)
Call B: Analytical assessment (interpretive analysis, uses Call A output)

This module replaces the DossierBuilderAgent for the v2 pipeline.
"""

import logging
from datetime import datetime
from typing import Optional

from ..config import LeaderConfig, MODEL_SYNTHESIS, THINKING_BUDGET_TOKENS
from ..running_picture import (
    RunningPictureEntry,
    append_entry,
    load_running_picture_text,
    validate_entry,
)
from .base import complete, with_retry
from .event_clustering import ProcessedEvent

logger = logging.getLogger(__name__)


# =============================================================================
# SYSTEM PROMPTS
# =============================================================================

CALL_A_SYSTEM = """You are a structured data logger for an intelligence analysis pipeline.
Your job is to convert this week's events into a structured Running Analytical
Picture entry that will be appended to a cumulative per-leader context file.
This file is read by an LLM analyst in future weeks, so optimize for machine
consumption: be precise, consistent, and structured.

You work within a layered context framework:

1. STRUCTURAL CONTEXT (Country Dossier): Persistent country features —
   geography, institutions, economy, history. Contains numbered STRUCTURAL
   CLAIMS (falsifiable assertions about persistent features).

2. LEADER CONTEXT (Leader Profile): How this individual exercises power —
   decision-making patterns, relationships, positioning. Contains numbered
   PROFILE CLAIMS (observable behavioral patterns).

3. RUNNING CONTEXT (Running Analytical Picture): Cumulative record of this
   leader's actions, commitments, and developing situations over recent weeks.

4. THIS WEEK'S EVENTS: Classified news events from the current reporting period.

Your task:
- Log this week's events into the Running Analytical Picture schema
- Carry forward unresolved Developing Threads from previous entries
- Track Commitments & Positions cumulatively (note shifts from prior positions)
- Flag Structural Claims or Profile Claims that were challenged, reinforced,
  or made newly relevant by this week's events
- Keep Key Actions concrete and verifiable — not interpretive
- Include source attribution for every Key Action

You produce ONLY the Running Picture entry in the exact schema format.
Do not add commentary, analysis, or explanation outside the schema."""


CALL_A_USER_TEMPLATE = """## STRUCTURAL CONTEXT: {country}

{country_dossier}

---

## LEADER CONTEXT: {leader_name}

{leader_profile}

---

## RUNNING CONTEXT: {leader_name} — Recent Weeks

{running_picture}

---

## THIS WEEK'S EVENTS: {leader_name}
Reporting period: {date_start} to {date_end}

{events_text}

---

## INSTRUCTIONS

Produce a Running Analytical Picture entry for {leader_name} ({title}, {country})
for the week of {week_of}.

Use this EXACT schema:

```
---
leader: {leader_name}
country: {country}
week_of: {week_of}
generated_at: {generated_at}
event_count: [number of classified events this week]
source_count: [number of articles processed]
---

### Activity Level
[ONE OF: High / Moderate / Low / Quiet]
[One sentence characterizing the week]

### Key Actions
[Numbered list of significant actions. Each entry must be concrete and
verifiable — not a media narrative or analyst interpretation.]

1. [DATE] [ACTION]: [Brief description]
   Source: [primary source attribution]
   Significance: [One sentence — reference structural/profile claims by number]

### Commitments & Positions
[New commitments, positions taken, or existing positions shifted.]

- [COMMITMENT/POSITION]: [What was said/pledged, to whom, in what context]
  Status: [NEW / REINFORCED / SHIFTED FROM [previous] / WALKED BACK]

### Relationships
[Significant interactions with other tracked leaders or external actors.]

- [INTERACTION]: [With whom, format, topic, observable outcome]
  Assessment: [Relationship trajectory]

### Domestic Political Position
[Only include if something changed this week. Do not repeat baseline.]

- [DEVELOPMENT]: [What changed and why it matters for foreign policy capacity]

### Developing Threads
[Unresolved situations to monitor. Carry forward from previous entries.]

- [THREAD]: [Current status]
  Watch for: [Specific observable event indicating development]
  Originated: [Week this thread first appeared]

### Structural Claim Check
[Flag structural/profile claims CHALLENGED, REINFORCED, or NEWLY RELEVANT.]

- [CLAIM TYPE + NUMBER]: [CHALLENGED / REINFORCED / NEWLY RELEVANT]
  Evidence: [What happened]
  Recommendation: [If challenged — does source document need refresh?]

### Analytical Notes
[1-3 sentences of between-the-lines observation grounded in the accumulated
context. Reference the running picture trajectory, not just this week.]
```

IMPORTANT:
- Carry forward ALL unresolved Developing Threads from the running context above.
  If a thread is not mentioned in this week's events, keep it with unchanged status.
- Only remove threads that are resolved, superseded, or stale (8+ weeks).
- Reference structural claims as [STRUC-XX] and profile claims as [PROF-XX].
- If this is the first entry (no running context), skip thread carry-forward
  and note this is the inaugural entry in Analytical Notes."""


# =============================================================================
# AGENT
# =============================================================================


class AnalystAgent:
    """Phase 1 analyst agent for per-leader weekly analysis."""

    @with_retry(max_attempts=2)
    async def run_call_a(
        self,
        leader: LeaderConfig,
        events: list[ProcessedEvent],
        date_start: str,
        date_end: str,
        country_dossier: str = "",
        leader_profile: str = "",
        running_picture_text: str = "",
        base_dir=None,
    ) -> tuple[str, RunningPictureEntry]:
        """
        Phase 1 Call A: Produce a structured Running Picture entry.

        Args:
            leader: Leader configuration
            events: Classified events from the event clustering pipeline
            date_start: Reporting period start (YYYY-MM-DD)
            date_end: Reporting period end (YYYY-MM-DD)
            country_dossier: Static country dossier content (markdown)
            leader_profile: Static leader profile content (markdown)
            running_picture_text: Pre-loaded running context (or loaded automatically)
            base_dir: Override running pictures directory

        Returns:
            Tuple of (raw entry text, parsed RunningPictureEntry)
        """
        # Load running context if not provided
        if not running_picture_text:
            running_picture_text = load_running_picture_text(
                leader.name, max_entries=10, base_dir=base_dir
            )

        if not running_picture_text:
            running_picture_text = "[No prior entries — this is the inaugural analysis.]"

        # Format events for the prompt
        events_text = _format_events(events)

        # Compute week_of (Monday of the reporting week)
        week_of = _monday_of_week(date_start)
        generated_at = datetime.now().isoformat(timespec="seconds")

        prompt = CALL_A_USER_TEMPLATE.format(
            country=leader.country,
            country_dossier=country_dossier or "[Country dossier not yet available]",
            leader_name=leader.name,
            leader_profile=leader_profile or "[Leader profile not yet available]",
            running_picture=running_picture_text,
            date_start=date_start,
            date_end=date_end,
            events_text=events_text,
            title=leader.title,
            week_of=week_of,
            generated_at=generated_at,
        )

        logger.info(f"Running Phase 1 Call A for {leader.name}")

        response = await complete(
            prompt=prompt,
            system=CALL_A_SYSTEM,
            model=MODEL_SYNTHESIS,
            max_tokens=8000,
            thinking_budget=THINKING_BUDGET_TOKENS,
        )

        # Extract the entry from the response
        entry_text = _extract_entry(response, leader.name, leader.country, week_of, generated_at)

        # Validate
        validation = validate_entry(entry_text)
        if not validation.valid:
            logger.warning(
                f"Call A entry for {leader.name} has validation errors: "
                f"{validation.errors}"
            )
        if validation.warnings:
            logger.info(
                f"Call A entry for {leader.name} warnings: {validation.warnings}"
            )

        # Parse into structured entry
        from ..running_picture import _parse_entry

        try:
            parsed = _parse_entry(entry_text)
        except ValueError as e:
            logger.error(f"Failed to parse Call A entry for {leader.name}: {e}")
            # Create a minimal entry so the pipeline can continue
            parsed = RunningPictureEntry(
                leader=leader.name,
                country=leader.country,
                week_of=week_of,
                generated_at=generated_at,
                event_count=len(events),
                source_count=sum(len(e.articles) for e in events),
                raw_text=entry_text,
            )

        return entry_text, parsed

    async def run_call_a_and_save(
        self,
        leader: LeaderConfig,
        events: list[ProcessedEvent],
        date_start: str,
        date_end: str,
        country_dossier: str = "",
        leader_profile: str = "",
        base_dir=None,
    ) -> tuple[str, RunningPictureEntry]:
        """
        Run Call A and append the entry to the leader's running picture file.

        Convenience method that combines run_call_a + append_entry.
        """
        entry_text, parsed = await self.run_call_a(
            leader=leader,
            events=events,
            date_start=date_start,
            date_end=date_end,
            country_dossier=country_dossier,
            leader_profile=leader_profile,
            base_dir=base_dir,
        )

        append_entry(leader.name, entry_text, base_dir=base_dir)

        return entry_text, parsed


# =============================================================================
# HELPERS
# =============================================================================


def _format_events(events: list[ProcessedEvent]) -> str:
    """Format ProcessedEvents into text for the LLM prompt."""
    if not events:
        return "[No classified events this week.]"

    lines = []
    for i, event in enumerate(events, 1):
        lines.append(f"### Event {i}: {event.title}")
        lines.append(f"Score: {event.score:.2f} | Sources: {event.source_count} | Wire: {'Yes' if event.has_wire else 'No'}")
        lines.append("")

        if event.summary:
            lines.append(event.summary)
            lines.append("")

        if event.articles:
            lines.append("**Sources:**")
            for article in event.articles:
                source = article.get("source_name", "Unknown")
                title = article.get("title", "Untitled")
                url = article.get("url", "")
                date = article.get("date", "")
                date_str = f" ({date})" if date else ""
                lines.append(f"- [{source}] {title}{date_str}")
                if url:
                    lines.append(f"  {url}")
            lines.append("")

        if event.entities:
            entity_names = [e.get("name", "") for e in event.entities if e.get("name")]
            if entity_names:
                lines.append(f"**Entities:** {', '.join(entity_names[:10])}")
                lines.append("")

    return "\n".join(lines)


def _monday_of_week(date_str: str) -> str:
    """Return the Monday of the week containing the given date."""
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    monday = dt - __import__("datetime").timedelta(days=dt.weekday())
    return monday.strftime("%Y-%m-%d")


def _extract_entry(
    response: str,
    leader_name: str,
    country: str,
    week_of: str,
    generated_at: str,
) -> str:
    """
    Extract the running picture entry from the LLM response.

    The response should contain the entry in the schema format.
    If the LLM wraps it in a code block, strip the fences.
    If the frontmatter is missing, prepend it.
    """
    import re

    text = response.strip()

    # Strip markdown code block fences if present
    text = re.sub(r"^```(?:markdown|md)?\s*\n", "", text)
    text = re.sub(r"\n```\s*$", "", text)
    text = text.strip()

    # Ensure frontmatter is present
    if not text.startswith("---"):
        # Prepend frontmatter
        frontmatter = (
            f"---\n"
            f"leader: {leader_name}\n"
            f"country: {country}\n"
            f"week_of: {week_of}\n"
            f"generated_at: {generated_at}\n"
            f"event_count: 0\n"
            f"source_count: 0\n"
            f"---"
        )
        text = frontmatter + "\n\n" + text

    return text

"""
Transcript preprocessor for government stenographic records.

Detects "Versión estenográfica" transcripts (and similar patterns from other
countries) in search snippets, fetches full text via Diffbot, and uses Claude
to split multi-topic press conferences into individual topic snippets or
rewrite single-topic event speeches with informative headlines.

Pipeline position:
    search_all_sources()
      -> preprocess_transcripts()   <- THIS MODULE
      -> filter_relevant()
      -> embed -> cluster -> score -> ...
"""

import asyncio
import json
import logging
import re
from typing import Optional

from ..agents.base import complete, extract_json_from_response
from ..fetcher.core import extract_article_diffbot, DIFFBOT_DELAY_SECONDS

logger = logging.getLogger(__name__)

# =============================================================================
# TRANSCRIPT DETECTION
# =============================================================================

# Regex patterns for detecting official transcript titles.
# Each entry is (compiled_regex, country_hint) for future extensibility.
TRANSCRIPT_TITLE_PATTERNS: list[tuple[re.Pattern, str]] = [
    (re.compile(r"Versión estenográfica", re.IGNORECASE), "MX"),
]

# Sub-pattern within title that marks a press conference (multi-topic)
PRESS_CONFERENCE_PATTERNS: list[re.Pattern] = [
    re.compile(r"Conferencia de prensa", re.IGNORECASE),
    re.compile(r"[Mm]añanera"),
]

# Patterns for third-party "mañanera recap" articles (live-blogs, summaries).
# These are redundant once we extract topics from the actual transcript.
MANRANERA_RECAP_PATTERNS: list[re.Pattern] = [
    re.compile(r"[Mm]añanera\b.*minuto a minuto", re.IGNORECASE),
    re.compile(r"[Ll]a [Mm]añanera de\b", re.IGNORECASE),
]


def is_transcript(snippet: dict) -> bool:
    """Return True if the snippet title matches a known transcript pattern."""
    title = snippet.get("title", "")
    return any(pat.search(title) for pat, _ in TRANSCRIPT_TITLE_PATTERNS)


def is_press_conference(snippet: dict) -> bool:
    """Return True if the transcript is a multi-topic press conference."""
    title = snippet.get("title", "")
    return any(pat.search(title) for pat in PRESS_CONFERENCE_PATTERNS)


def is_mananera_recap(snippet: dict) -> bool:
    """Return True if the snippet is a third-party mañanera recap/live-blog."""
    title = snippet.get("title", "")
    return any(pat.search(title) for pat in MANRANERA_RECAP_PATTERNS)


# =============================================================================
# FETCHING
# =============================================================================

async def fetch_transcript_text(url: str) -> Optional[str]:
    """Fetch full transcript text via Diffbot Article API.

    Returns the article body text, or None on any failure.
    """
    try:
        extracted = await extract_article_diffbot(url)
        if extracted:
            text = extracted.get("text", "")
            if len(text) > 500:  # sanity: transcripts are long
                return text
            logger.warning(f"Transcript text too short ({len(text)} chars): {url}")
        return None
    except Exception as e:
        logger.error(f"Failed to fetch transcript {url}: {e}")
        return None


# =============================================================================
# CLAUDE EXTRACTION PROMPTS (SPANISH)
# =============================================================================

PRESS_CONFERENCE_SYSTEM = (
    "Eres un analista político que extrae los temas individuales tratados "
    "en conferencias de prensa gubernamentales. Tu trabajo es identificar "
    "cada tema distinto y escribir un titular periodístico + resumen para cada uno."
)

PRESS_CONFERENCE_PROMPT = """\
A continuación se presenta la transcripción de una conferencia de prensa \
(«mañanera») de la presidenta de México, con fecha {date}.

Identifica cada tema distinto tratado en la conferencia. Para cada tema, escribe:
- **headline**: Un titular periodístico informativo en español (máx. 15 palabras). \
No uses "Versión estenográfica" ni frases genéricas.
- **summary**: Un resumen de 2-3 oraciones que explique qué se dijo o anunció \
sobre este tema.

Devuelve SOLAMENTE un JSON válido con la siguiente estructura (sin texto adicional):
```json
{{
  "topics": [
    {{"headline": "...", "summary": "..."}},
    ...
  ]
}}
```

Reglas:
- Identifica entre 2 y 10 temas.
- Cada tema debe ser distinto (no repitas el mismo asunto con distintas palabras).
- Si un periodista hace una pregunta sobre un tema ya cubierto, agrégalo al \
resumen existente en vez de crear un tema nuevo.
- Los titulares deben ser específicos y periodísticos, como si fueran de un \
periódico.

TRANSCRIPCIÓN:
{text}
"""

EVENT_SPEECH_SYSTEM = (
    "Eres un analista político que resume discursos y eventos gubernamentales. "
    "Tu trabajo es escribir un titular periodístico claro y un resumen conciso."
)

EVENT_SPEECH_PROMPT = """\
A continuación se presenta la transcripción de un evento oficial del gobierno \
de México. El título original del evento es:

«{event_title}»

Escribe:
- **headline**: Un titular periodístico informativo en español (máx. 15 palabras). \
No uses "Versión estenográfica" ni el título genérico del evento.
- **summary**: Un resumen de 2-3 oraciones que explique qué se anunció o discutió.

Devuelve SOLAMENTE un JSON válido (sin texto adicional):
```json
{{
  "headline": "...",
  "summary": "..."
}}
```

TRANSCRIPCIÓN:
{text}
"""


# =============================================================================
# EXTRACTION FUNCTIONS
# =============================================================================

def _extract_json_array_or_object(text: str) -> Optional[dict]:
    """Try to parse JSON from Claude's response, handling code fences."""
    # Try the shared utility first
    result = extract_json_from_response(text)
    if result is not None:
        return result

    # Fallback: look for a JSON array pattern (for cases where Claude
    # returns the topics array directly instead of wrapping it)
    try:
        match = re.search(r"\[.*\]", text, re.DOTALL)
        if match:
            arr = json.loads(match.group(0))
            if isinstance(arr, list):
                return {"topics": arr}
    except (json.JSONDecodeError, ValueError):
        pass

    return None


async def extract_press_conference_topics(
    text: str, date: str
) -> list[dict]:
    """Use Claude to extract individual topics from a press conference transcript.

    Args:
        text: Full transcript text.
        date: Human-readable date string for the conference.

    Returns:
        List of dicts with 'headline' and 'summary' keys.
        Empty list on failure.
    """
    # Truncate very long transcripts to stay within context window
    max_chars = 180_000  # ~45k tokens in Spanish
    if len(text) > max_chars:
        text = text[:max_chars] + "\n\n[TRANSCRIPCIÓN TRUNCADA]"

    prompt = PRESS_CONFERENCE_PROMPT.format(date=date, text=text)

    try:
        response = await complete(
            prompt=prompt,
            system=PRESS_CONFERENCE_SYSTEM,
            max_tokens=4096,
            temperature=0.2,
        )
        parsed = _extract_json_array_or_object(response)
        if parsed and "topics" in parsed:
            topics = parsed["topics"]
            # Validate each topic has required fields
            valid = [
                t for t in topics
                if isinstance(t, dict)
                and t.get("headline")
                and t.get("summary")
            ]
            if valid:
                return valid
            logger.warning(f"No valid topics in Claude response for conference {date}")
        else:
            logger.warning(f"Could not parse topics JSON for conference {date}")
        return []
    except Exception as e:
        logger.error(f"Claude extraction failed for press conference {date}: {e}")
        return []


async def extract_event_speech_topic(
    text: str, event_title: str
) -> Optional[dict]:
    """Use Claude to write a headline + summary for a single-topic event speech.

    Args:
        text: Full transcript text.
        event_title: Original title of the event.

    Returns:
        Dict with 'headline' and 'summary', or None on failure.
    """
    max_chars = 180_000
    if len(text) > max_chars:
        text = text[:max_chars] + "\n\n[TRANSCRIPCIÓN TRUNCADA]"

    prompt = EVENT_SPEECH_PROMPT.format(event_title=event_title, text=text)

    try:
        response = await complete(
            prompt=prompt,
            system=EVENT_SPEECH_SYSTEM,
            max_tokens=1024,
            temperature=0.2,
        )
        parsed = extract_json_from_response(response)
        if parsed and parsed.get("headline") and parsed.get("summary"):
            return parsed
        logger.warning(f"Could not parse event speech JSON for: {event_title}")
        return None
    except Exception as e:
        logger.error(f"Claude extraction failed for event speech '{event_title}': {e}")
        return None


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

async def preprocess_transcripts(
    snippets: list[dict],
    leader_name: str,
) -> list[dict]:
    """Preprocess transcript snippets by expanding them into topic-level snippets.

    Non-transcript snippets pass through unchanged.
    On any failure for a given transcript, the original snippet is kept.

    Args:
        snippets: List of snippet dicts from search_all_sources().
        leader_name: Name of the leader (for logging).

    Returns:
        New list of snippet dicts (same format as input).
    """
    result = []
    transcript_count = 0
    expanded_count = 0

    for snippet in snippets:
        if not is_transcript(snippet):
            result.append(snippet)
            continue

        transcript_count += 1
        url = snippet.get("url", "")
        title = snippet.get("title", "")
        logger.info(f"[transcript] Processing: {title[:80]}")

        # Fetch full text
        if transcript_count > 1:
            await asyncio.sleep(DIFFBOT_DELAY_SECONDS)
        text = await fetch_transcript_text(url)

        if not text:
            logger.warning(f"[transcript] Could not fetch text, keeping original: {title[:60]}")
            result.append(snippet)
            continue

        # Determine type and extract topics
        if is_press_conference(snippet):
            date = snippet.get("date", "fecha desconocida")
            topics = await extract_press_conference_topics(text, date)

            if not topics:
                logger.warning(f"[transcript] No topics extracted from conference, keeping original: {title[:60]}")
                result.append(snippet)
                continue

            for topic in topics:
                result.append({
                    "title": topic["headline"],
                    "snippet": topic["summary"],
                    "url": url,
                    "source_name": snippet.get("source_name", ""),
                    "source_type": snippet.get("source_type", ""),
                    "date": snippet.get("date", ""),
                    "_transcript_expanded": True,
                    "_original_title": title,
                })
            expanded_count += len(topics)
            logger.info(f"[transcript] Conference -> {len(topics)} topics")

        else:
            # Single-topic event speech
            topic = await extract_event_speech_topic(text, title)

            if not topic:
                logger.warning(f"[transcript] No topic extracted from event, keeping original: {title[:60]}")
                result.append(snippet)
                continue

            result.append({
                "title": topic["headline"],
                "snippet": topic["summary"],
                "url": url,
                "source_name": snippet.get("source_name", ""),
                "source_type": snippet.get("source_type", ""),
                "date": snippet.get("date", ""),
                "_transcript_expanded": True,
                "_original_title": title,
            })
            expanded_count += 1
            logger.info(f"[transcript] Event speech -> 1 topic")

    # Second pass: drop mañanera recap articles if we successfully expanded
    # at least one press conference transcript (recaps are now redundant).
    expanded_conferences = any(
        s.get("_transcript_expanded") and is_press_conference({"title": s.get("_original_title", "")})
        for s in result
    )
    if expanded_conferences:
        before_filter = len(result)
        filtered = []
        recap_dropped = 0
        for s in result:
            if not s.get("_transcript_expanded") and is_mananera_recap(s):
                recap_dropped += 1
                logger.info(f"[transcript] Dropping redundant recap: {s.get('title', '')[:60]}")
            else:
                filtered.append(s)
        result = filtered
        if recap_dropped:
            logger.info(f"[transcript] Dropped {recap_dropped} mañanera recaps")

    logger.info(
        f"[transcript] Done for {leader_name}: "
        f"{transcript_count} transcripts processed, "
        f"{expanded_count} topic snippets created, "
        f"{len(result)} total snippets"
    )
    return result

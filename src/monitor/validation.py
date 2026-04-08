"""
Source attribution validation.

Checks that named entities in country agent development summaries
actually appear in the cited source articles. Flags unattributed
entities for review.

Runs between the country agent output and the ledger write.
Uses spaCy NER for entity extraction (en_core_web_md).
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field

import spacy

from .collection.extract import ExtractionResult
from .config import SignalCategory
from .models import WeeklyEntry

logger = logging.getLogger(__name__)

# spaCy model — loaded once on first call, reused across all countries
_nlp: spacy.Language | None = None

# Entity labels to extract from NER output
_NER_ENTITY_LABELS = frozenset({"PERSON", "ORG", "GPE", "LOC", "FAC"})

# Minimum character length to consider as a potential entity
_MIN_ENTITY_LEN = 2


def _get_nlp() -> spacy.Language:
    """Lazy-load spaCy model with only the NER component enabled."""
    global _nlp
    if _nlp is None:
        _nlp = spacy.load(
            "en_core_web_md",
            disable=["tok2vec", "tagger", "parser", "attribute_ruler", "lemmatizer"],
        )
    return _nlp


@dataclass
class AttributionFlag:
    """A development where summary entities or figures don't appear in cited sources."""

    category: str
    headline: str
    unattributed_entities: list[str]
    cited_source_urls: list[str]
    severity: str = "warning"  # "warning" or "info"
    unattributed_figures: list[str] = field(default_factory=list)


@dataclass
class ValidationResult:
    """Result of source attribution validation for a country."""

    code: str
    flags: list[AttributionFlag] = field(default_factory=list)
    developments_checked: int = 0
    developments_flagged: int = 0

    @property
    def clean(self) -> bool:
        return len(self.flags) == 0


def extract_entities(text: str) -> set[str]:
    """Extract named entities from text using spaCy NER.

    Returns lowercased entity strings for case-insensitive matching.
    Keeps PERSON, ORG, GPE, LOC, and FAC entities.
    """
    if not text:
        return set()
    nlp = _get_nlp()
    doc = nlp(text)
    return {
        ent.text.lower()
        for ent in doc.ents
        if ent.label_ in _NER_ENTITY_LABELS
        and len(ent.text.strip()) >= _MIN_ENTITY_LEN
    }


# Patterns that look like numbers but aren't meaningful figures
_TRIVIAL_NUMBERS = frozenset({"0", "1", "2", "3", "4", "5", "10", "100"})


def extract_figures(text: str) -> set[str]:
    """Extract numeric figures from text for attribution checking.

    Captures quantities, percentages, monetary amounts, and other
    specific numbers that represent factual claims. Returns normalised
    string forms for matching.

    Returns a set of canonical number strings (e.g. "404", "50000",
    "4.02", "2.3").
    """
    if not text:
        return set()

    figures: set[str] = set()

    # Match numbers with optional comma separators and decimals
    # Covers: 404, 1,000, 50,000, 4.02, $2.3, 2.3%
    raw_numbers = re.findall(
        r"(?<![.\w])"           # not preceded by word char or dot
        r"[$€£¥]?"             # optional currency symbol
        r"(\d[\d,]*\.?\d*)"    # the number itself (capture group)
        r"(?:\s?%|(?:bn|mn|m|k|tr))?"  # optional suffix
        r"(?![.\w])",          # not followed by word char or dot
        text,
    )

    for raw in raw_numbers:
        # Strip commas to normalise: "50,000" → "50000"
        normalised = raw.replace(",", "")
        # Strip trailing dot if any: "50." → "50"
        normalised = normalised.rstrip(".")
        if not normalised:
            continue
        # Skip trivially common numbers (years handled separately below)
        if normalised in _TRIVIAL_NUMBERS:
            continue
        # Skip 4-digit numbers in the 1900–2099 range (likely years)
        if re.fullmatch(r"(19|20)\d{2}", normalised):
            continue
        figures.add(normalised)

    return figures


def _build_source_indexes(
    articles: list[ExtractionResult],
) -> tuple[dict[str, set[str]], dict[str, set[str]]]:
    """Build URL → entity set and URL → figure set mappings from extracted articles."""
    nlp = _get_nlp()
    entity_index: dict[str, set[str]] = {}
    figure_index: dict[str, set[str]] = {}

    # Prepare texts for batch NER
    url_text_pairs: list[tuple[str, str]] = []
    for article in articles:
        if article.success and article.text:
            combined = f"{article.title or ''} {article.text}"
            url_text_pairs.append((article.url, combined))
            figure_index[article.url] = extract_figures(combined)

    # Batch NER processing
    texts = [t for _, t in url_text_pairs]
    for (url, _), doc in zip(url_text_pairs, nlp.pipe(texts, batch_size=8)):
        entity_index[url] = {
            ent.text.lower()
            for ent in doc.ents
            if ent.label_ in _NER_ENTITY_LABELS
            and len(ent.text.strip()) >= _MIN_ENTITY_LEN
        }

    return entity_index, figure_index


def validate_source_attribution(
    code: str,
    weekly_entry: WeeklyEntry,
    extracted_articles: list[ExtractionResult] | None,
) -> ValidationResult:
    """Check that entities in development summaries appear in cited sources.

    For each development with sources, extracts named entities from the summary
    using spaCy NER and checks whether they appear in at least one of the cited
    articles. Entities that appear in the summary but none of the cited sources
    are flagged.

    Args:
        code: Country code.
        weekly_entry: The country agent's weekly entry output.
        extracted_articles: Articles extracted for this country (may be None).

    Returns:
        ValidationResult with any attribution flags.
    """
    result = ValidationResult(code=code)

    if not weekly_entry.category_movements or not extracted_articles:
        return result

    source_entities, source_figures = _build_source_indexes(extracted_articles)

    for cat, movement in weekly_entry.category_movements.items():
        for dev in movement.developments:
            result.developments_checked += 1

            # Get entity pool from all cited sources
            cited_urls = [s.url for s in dev.sources if s.url]
            if not cited_urls:
                continue

            cited_entities: set[str] = set()
            cited_figures: set[str] = set()
            matched_urls = 0
            for url in cited_urls:
                if url in source_entities:
                    cited_entities.update(source_entities[url])
                    cited_figures.update(source_figures.get(url, set()))
                    matched_urls += 1

            # If none of the cited URLs were in our extraction set, skip
            # (the source may have been from fallback/search mode)
            if matched_urls == 0:
                continue

            # Extract entities from the development summary + headline
            summary_text = f"{dev.headline} {dev.summary}"
            summary_entities = extract_entities(summary_text)

            # Flag entities in summary not found in any cited source.
            # Allow partial matches: "umerov" matches "rustem umerov".
            unattributed = set()
            for entity in summary_entities:
                if entity in cited_entities:
                    continue
                # Check if entity is a component of a multi-word cited entity
                if any(entity in ce for ce in cited_entities):
                    continue
                # Check if any cited entity is a component of this entity
                if any(ce in entity for ce in cited_entities):
                    continue
                unattributed.add(entity)

            # Flag figures in summary not found in any cited source
            summary_figures = extract_figures(summary_text)
            unattributed_figs = summary_figures - cited_figures

            if unattributed or unattributed_figs:
                cat_name = cat.value if isinstance(cat, SignalCategory) else str(cat)
                total_unattributed = len(unattributed) + len(unattributed_figs)
                flag = AttributionFlag(
                    category=cat_name,
                    headline=dev.headline,
                    unattributed_entities=sorted(unattributed),
                    cited_source_urls=cited_urls,
                    severity="warning" if total_unattributed >= 2 else "info",
                    unattributed_figures=sorted(unattributed_figs),
                )
                result.flags.append(flag)
                result.developments_flagged += 1
                parts = []
                if unattributed:
                    parts.append(f"{len(unattributed)} entities: {', '.join(sorted(unattributed))}")
                if unattributed_figs:
                    parts.append(f"{len(unattributed_figs)} figures: {', '.join(sorted(unattributed_figs))}")
                logger.info(
                    "Attribution flag [%s] %s: %s",
                    code, dev.headline, "; ".join(parts),
                )

    if result.clean:
        logger.debug("Attribution check clean for %s (%d developments)", code, result.developments_checked)
    else:
        logger.warning(
            "Attribution check for %s: %d/%d developments flagged",
            code, result.developments_flagged, result.developments_checked,
        )

    return result

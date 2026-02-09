"""
URL-based opinion filtering using domain-specific patterns.

Loads patterns from opinion_filters.csv and checks URLs against them.
"""

import csv
import logging
import re
from pathlib import Path
from urllib.parse import urlparse
from functools import lru_cache

logger = logging.getLogger(__name__)

# Path to opinion filters CSV (relative to project root)
OPINION_FILTERS_PATH = Path(__file__).parent.parent.parent / "opinion_filters.csv"


@lru_cache(maxsize=1)
def _load_filters() -> list[dict]:
    """Load opinion filters from CSV (cached)."""
    filters = []

    if not OPINION_FILTERS_PATH.exists():
        logger.warning(f"Opinion filters not found: {OPINION_FILTERS_PATH}")
        return filters

    with open(OPINION_FILTERS_PATH, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("domain"):  # Skip empty rows
                filters.append(row)

    logger.info(f"Loaded {len(filters)} opinion filters from {OPINION_FILTERS_PATH.name}")
    return filters


def is_opinion_url(url: str) -> tuple[bool, str]:
    """
    Check if a URL matches any opinion filter pattern.

    Args:
        url: Full URL to check

    Returns:
        Tuple of (is_opinion, matched_pattern)
        - is_opinion: True if URL matches an opinion pattern
        - matched_pattern: Description of the matched pattern (for logging)
    """
    if not url:
        return False, ""

    filters = _load_filters()
    parsed = urlparse(url)
    domain = parsed.netloc.replace("www.", "")
    path = parsed.path

    for filt in filters:
        filter_domain = filt.get("domain", "")
        opinion_type = filt.get("opinion_type", "")
        pattern = filt.get("opinion_pattern", "")

        # Check if this filter applies to this domain
        if filter_domain not in domain:
            continue

        if opinion_type == "subdomain":
            # Check if the subdomain matches (e.g., arvamus.postimees.ee)
            if pattern in parsed.netloc:
                return True, f"subdomain:{pattern}"

        elif opinion_type == "path":
            # Check if the path contains the pattern (e.g., /opinion/)
            if pattern in path:
                return True, f"path:{pattern}"

        elif opinion_type == "regex":
            # Check if the path matches the regex (e.g., /op\d+$)
            if re.search(pattern, path):
                return True, f"regex:{pattern}"

    return False, ""


def filter_opinion_snippets(
    snippets: list[dict],
) -> tuple[list[dict], list[dict]]:
    """
    Separate opinion pieces from news based on URL patterns.

    Args:
        snippets: List of snippet dicts with 'url' key

    Returns:
        Tuple of (news_snippets, opinion_snippets)
    """
    news = []
    opinions = []

    for snippet in snippets:
        url = snippet.get("url", "")
        is_opinion, pattern = is_opinion_url(url)

        if is_opinion:
            snippet["opinion_pattern"] = pattern  # Tag for debugging
            opinions.append(snippet)
        else:
            news.append(snippet)

    if opinions:
        logger.info(f"Opinion filter: {len(news)} news, {len(opinions)} opinion pieces filtered")

    return news, opinions

"""
Brave News Search API client for Layer 1 news discovery.

Handles per-country search param selection (EN vs local), rate limiting,
and source configuration loading from brave_sources.yaml.

API reference: https://api-dashboard.search.brave.com/api-reference/news/news_search/get
"""

from __future__ import annotations

import asyncio
import csv
import logging
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

import httpx
import yaml
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Load .env from project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(PROJECT_ROOT / ".env")

BRAVE_NEWS_URL = "https://api.search.brave.com/res/v1/news/search"
BRAVE_SOURCES_PATH = PROJECT_ROOT / "assets" / "country_configs" / "brave_sources.yaml"
GOGGLES_DIR = PROJECT_ROOT / "assets" / "country_goggles"

# Goggle files must be served via URL for the Brave API.
# Default: GitHub raw content URL for this repo.
GOGGLES_BASE_URL = os.environ.get(
    "MPM_GOGGLES_BASE_URL",
    "https://raw.githubusercontent.com/j0nathanB/pdb-aggregator/main/assets/country_goggles",
)


# =============================================================================
# Data classes
# =============================================================================


@dataclass
class BraveNewsResult:
    """A single news result from Brave Search."""

    title: str
    url: str
    description: str
    age: str | None = None
    page_age: str | None = None
    source_domain: str | None = None
    extra_snippets: list[str] = field(default_factory=list)

    @classmethod
    def from_api(cls, item: dict) -> BraveNewsResult:
        meta = item.get("meta_url", {})
        return cls(
            title=item.get("title", ""),
            url=item.get("url", ""),
            description=item.get("description", ""),
            age=item.get("age"),
            page_age=item.get("page_age"),
            source_domain=meta.get("netloc") or meta.get("hostname"),
            extra_snippets=item.get("extra_snippets", []),
        )


@dataclass
class BraveSearchResponse:
    """Response from a Brave News Search query."""

    query: str
    results: list[BraveNewsResult]
    total_count: int


@dataclass
class IndexedSource:
    """A news source confirmed indexed by Brave."""

    name: str
    domain: str
    rss_full_text: bool = False


@dataclass
class CountrySearchConfig:
    """Per-country Brave search configuration."""

    code: str
    use_local_params: bool
    local_params: dict[str, str] | None
    sources: list[IndexedSource]
    discard_domains: frozenset[str] = field(default_factory=frozenset)
    allowed_domains: frozenset[str] = field(default_factory=frozenset)

    @property
    def search_params(self) -> dict[str, str]:
        """Return the search params to use for this country."""
        if self.use_local_params and self.local_params:
            return dict(self.local_params)
        return {}

    def goggle_path(self) -> Path | None:
        """Return path to this country's goggle file, if it exists."""
        path = GOGGLES_DIR / f"{self.code}.goggle"
        return path if path.exists() else None

    def goggle_url(self) -> str | None:
        """Return the URL to this country's goggle file, if it exists locally."""
        if self.goggle_path() is None:
            return None
        return f"{GOGGLES_BASE_URL}/{self.code}.goggle"


# =============================================================================
# Discard enforcement (hard filter for $discard directives from goggle files)
# =============================================================================
#
# Brave's $discard directive in a goggle deranks matching results but does not
# reliably exclude them — politically-loaded sources still surface on highly-
# relevant queries. We enforce discards in the pipeline post-fetch so exclusion
# is deterministic. Source of truth is the goggle file itself.

_DISCARD_LINE_RE = re.compile(r"^\$discard,\s*site=([\w\.\-]+)\s*$")
_BOOST_LINE_RE = re.compile(r"^\$boost=\d+,\s*site=([\w\.\-]+)\s*$")

GLOBAL_DISCARDS_PATH = GOGGLES_DIR / "_global_discards.txt"
GLOBAL_ALLOWLIST_PATH = GOGGLES_DIR / "_global_allowlist.txt"

# Feature flag: inverted-allowlist mode. When set, only results whose domain
# is in the per-country effective allowlist (goggle $boost union + global
# allowlist) pass through. Off by default — current behavior is allow-all-
# except-blocklist. See dev notes from 2026-04-20 for rationale.
USE_DOMAIN_ALLOWLIST = os.getenv("MPM_DOMAIN_ALLOWLIST", "0") == "1"


def _parse_goggle_discards(goggle_path: Path) -> frozenset[str]:
    """Extract domains marked with $discard from a goggle file."""
    if not goggle_path.exists():
        return frozenset()
    discards: set[str] = set()
    for line in goggle_path.read_text().splitlines():
        m = _DISCARD_LINE_RE.match(line.strip())
        if m:
            discards.add(m.group(1).lower())
    return frozenset(discards)


def _parse_global_discards(path: Path) -> frozenset[str]:
    """Load the cross-country discard list (plain text, one domain per line).

    Format: `#` starts a comment. Blank lines and comments ignored.
    Applied to every country via union with per-country goggle $discards.
    """
    return _parse_plain_domain_list(path, allow_goggle_syntax="discard")


def _parse_global_allowlist(path: Path) -> frozenset[str]:
    """Load the cross-country trusted-sources allowlist (same format as discards)."""
    return _parse_plain_domain_list(path, allow_goggle_syntax="boost")


def _parse_plain_domain_list(path: Path, allow_goggle_syntax: str = "") -> frozenset[str]:
    """Parse a plain-text file of one-domain-per-line.

    Shared helper for discard and allowlist files. `#` starts a comment.
    If `allow_goggle_syntax="discard"` or `"boost"`, goggle lines like
    `$discard,site=X` or `$boost=N,site=X` are accepted too.
    """
    if not path.exists():
        return frozenset()
    domains: set[str] = set()
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if allow_goggle_syntax == "discard":
            m = _DISCARD_LINE_RE.match(line)
            if m:
                domains.add(m.group(1).lower())
                continue
        elif allow_goggle_syntax == "boost":
            m = _BOOST_LINE_RE.match(line)
            if m:
                domains.add(m.group(1).lower())
                continue
        # Bare domain — basic sanity check, must contain a dot, no spaces
        if "." in line and " " not in line:
            domains.add(line.lower())
    return frozenset(domains)


def _parse_goggle_boosts(goggle_path: Path) -> frozenset[str]:
    """Extract domains marked with $boost=... from a goggle file."""
    if not goggle_path.exists():
        return frozenset()
    boosts: set[str] = set()
    for line in goggle_path.read_text().splitlines():
        m = _BOOST_LINE_RE.match(line.strip())
        if m:
            boosts.add(m.group(1).lower())
    return frozenset(boosts)


def _is_allowlisted(source_domain: str | None, allowlist: frozenset[str]) -> bool:
    """Check if a result's source domain is in the allowlist.

    Same matching semantics as _is_discarded: exact + subdomain, www. stripped.
    """
    if not source_domain or not allowlist:
        return False
    d = source_domain.lower()
    if d.startswith("www."):
        d = d[4:]
    if d in allowlist:
        return True
    return any(d.endswith("." + ad) for ad in allowlist)


def _is_discarded(source_domain: str | None, discards: frozenset[str]) -> bool:
    """Check if a result's source domain matches the discard list.

    Matches exact (cnews.fr == cnews.fr) and subdomain (x.cnews.fr blocked by
    cnews.fr). Strips www. prefix. Safe on None.
    """
    if not source_domain or not discards:
        return False
    d = source_domain.lower()
    if d.startswith("www."):
        d = d[4:]
    if d in discards:
        return True
    return any(d.endswith("." + dd) for dd in discards)


# =============================================================================
# Off-topic URL filter (path/subdomain/regex rules loaded from CSV)
# =============================================================================
#
# Drops sports/entertainment/lifestyle URLs at the search-result boundary
# before they reach story_map. story_map was already dropping ~70-90% of
# these as noise — filtering upstream saves tokens without changing what
# the LLM sees for the URLs that remain. Schema mirrors opinion_filters.csv.

OFF_TOPIC_FILTERS_PATH = PROJECT_ROOT / "off_topic_filters.csv"


def _load_off_topic_filters(path: Path = OFF_TOPIC_FILTERS_PATH) -> list[dict]:
    """Load off-topic filter rules from CSV.

    Lines starting with `#` are skipped (allows header comments).
    Returns list of {domain, type, pattern} dicts. Regex patterns are
    precompiled under `_compiled`.
    """
    if not path.exists():
        logger.warning("off_topic_filters.csv not found at %s", path)
        return []
    rules: list[dict] = []
    with open(path, newline="", encoding="utf-8") as f:
        non_comment = (line for line in f if not line.lstrip().startswith("#"))
        for row in csv.DictReader(non_comment):
            rule = {
                "domain": row["domain"].strip().lower(),
                "type": row["filter_type"].strip(),
                "pattern": row["filter_pattern"].strip(),
            }
            if rule["type"] == "regex":
                rule["_compiled"] = re.compile(rule["pattern"])
            rules.append(rule)
    return rules


_OFF_TOPIC_RULES: list[dict] = _load_off_topic_filters()


def _is_off_topic_url(url: str, rules: list[dict] | None = None) -> bool:
    """Check if a URL matches an off-topic filter rule.

    Matching rules mirror opinion_filters in extract.py:
      - path: URL path starts with pattern
      - subdomain: hostname exactly matches pattern
      - regex: precompiled pattern searches the full URL
    """
    rules = rules if rules is not None else _OFF_TOPIC_RULES
    if not rules:
        return False
    parsed = urlparse(url)
    hostname = parsed.netloc.lower()
    if hostname.startswith("www."):
        hostname = hostname[4:]
    path = parsed.path.lower()
    for rule in rules:
        if rule["domain"] not in hostname:
            continue
        if rule["type"] == "path" and path.startswith(rule["pattern"].lower()):
            return True
        if rule["type"] == "subdomain" and hostname == rule["pattern"].lower():
            return True
        if rule["type"] == "regex" and rule["_compiled"].search(url):
            return True
    return False


# =============================================================================
# Source config loader
# =============================================================================


def load_brave_sources() -> dict[str, CountrySearchConfig]:
    """Load per-country Brave source config from brave_sources.yaml."""
    if not BRAVE_SOURCES_PATH.exists():
        raise FileNotFoundError(
            f"Brave sources config not found: {BRAVE_SOURCES_PATH}\n"
            "Generate it with: python dev/source_maps/media/generate_brave_config.py"
        )

    with open(BRAVE_SOURCES_PATH) as f:
        data = yaml.safe_load(f)

    global_discards = _parse_global_discards(GLOBAL_DISCARDS_PATH)
    if global_discards:
        logger.info(
            "Loaded %d cross-country discard domains from %s",
            len(global_discards), GLOBAL_DISCARDS_PATH.name,
        )
    global_allowlist = _parse_global_allowlist(GLOBAL_ALLOWLIST_PATH)
    if global_allowlist:
        logger.info(
            "Loaded %d cross-country allowlist domains from %s",
            len(global_allowlist), GLOBAL_ALLOWLIST_PATH.name,
        )

    configs = {}
    for code, entry in data.get("countries", {}).items():
        sources = [
            IndexedSource(
                name=s["name"],
                domain=s["domain"],
                rss_full_text=s.get("rss_full_text", False),
            )
            for s in entry.get("sources", [])
        ]
        goggle_path = GOGGLES_DIR / f"{code}.goggle"
        country_discards = _parse_goggle_discards(goggle_path)
        country_boosts = _parse_goggle_boosts(goggle_path)
        configs[code] = CountrySearchConfig(
            code=code,
            use_local_params=entry.get("use_local_params", False),
            local_params=entry.get("local_params"),
            sources=sources,
            discard_domains=country_discards | global_discards,
            allowed_domains=country_boosts | global_allowlist,
        )

    return configs


# =============================================================================
# Brave News API client
# =============================================================================


class BraveNewsClient:
    """Async client for the Brave News Search API.

    Handles rate limiting, per-country param selection, and response parsing.

    Usage:
        async with BraveNewsClient() as client:
            response = await client.search_news("Sheinbaum SEDENA", country_code="mx")
    """

    def __init__(
        self,
        api_key: str | None = None,
        rate_limit_delay: float = 1.1,
    ):
        self.api_key = api_key or os.getenv("BRAVE_API_KEY")
        if not self.api_key:
            raise ValueError("BRAVE_API_KEY not found in environment or constructor")
        self._rate_limit_delay = rate_limit_delay
        self._last_request_time = 0.0
        self._lock = asyncio.Lock()
        self._client = httpx.AsyncClient(
            headers={
                "Accept": "application/json",
                "Accept-Encoding": "gzip",
                "X-Subscription-Token": self.api_key,
            },
            timeout=30.0,
        )
        self._country_configs: dict[str, CountrySearchConfig] | None = None

    @property
    def country_configs(self) -> dict[str, CountrySearchConfig]:
        if self._country_configs is None:
            self._country_configs = load_brave_sources()
        return self._country_configs

    async def close(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> BraveNewsClient:
        return self

    async def __aexit__(self, *args) -> None:
        await self.close()

    async def _rate_limit(self) -> None:
        """Enforce minimum delay between API requests."""
        async with self._lock:
            loop = asyncio.get_event_loop()
            now = loop.time()
            elapsed = now - self._last_request_time
            if elapsed < self._rate_limit_delay:
                await asyncio.sleep(self._rate_limit_delay - elapsed)
            self._last_request_time = loop.time()

    async def search_news(
        self,
        query: str,
        *,
        country_code: str | None = None,
        count: int = 50,
        offset: int = 0,
        freshness: str = "pw",
        extra_snippets: bool = True,
        goggles: str | None = None,
        search_lang: str | None = None,
        ui_lang: str | None = None,
        country: str | None = None,
    ) -> BraveSearchResponse:
        """Search the Brave News API.

        Args:
            query: Search query (max 400 chars, 50 words).
            country_code: ISO 2-letter code. If provided, applies that country's
                configured search params (EN or local) automatically.
            count: Results per request (1-50, default 50).
            offset: Pagination offset (0-9, default 0).
            freshness: Age filter. "pw" (past week), "pd" (past day),
                "pm" (past month), or "YYYY-MM-DDtoYYYY-MM-DD" for date range.
            extra_snippets: Request up to 5 additional excerpts per result.
            goggles: URL to a Goggle file for custom ranking.
            search_lang: Override search language (normally set via country_code).
            ui_lang: Override UI language (normally set via country_code).
            country: Override country param (normally set via country_code).

        Returns:
            BraveSearchResponse with parsed results.
        """
        await self._rate_limit()

        params: dict[str, str | int | bool] = {
            "q": query,
            "count": count,
            "offset": offset,
            "freshness": freshness,
            "extra_snippets": extra_snippets,
        }

        # Apply per-country params if country_code provided
        if country_code:
            cc = self.country_configs.get(country_code)
            if cc:
                params.update(cc.search_params)

        # Explicit overrides take precedence
        if search_lang is not None:
            params["search_lang"] = search_lang
        if ui_lang is not None:
            params["ui_lang"] = ui_lang
        if country is not None:
            params["country"] = country
        if goggles is not None:
            params["goggles"] = goggles

        logger.debug("Brave News API request: q=%r params=%s", query, params)

        response = await self._client.get(BRAVE_NEWS_URL, params=params)
        response.raise_for_status()
        data = response.json()

        results = [
            BraveNewsResult.from_api(item) for item in data.get("results", [])
        ]

        # Enforce $discard from the country's goggle. Brave's built-in
        # discard is soft (deranks but still surfaces on relevant queries);
        # this makes exclusion deterministic.
        if country_code:
            cc = self.country_configs.get(country_code)
            if cc and cc.discard_domains:
                pre = len(results)
                results = [
                    r for r in results
                    if not _is_discarded(r.source_domain, cc.discard_domains)
                ]
                dropped = pre - len(results)
                if dropped:
                    logger.info(
                        "Brave [%s]: dropped %d/%d results matching goggle $discard",
                        country_code, dropped, pre,
                    )

        # Off-topic URL-path filter (sports/entertainment/lifestyle).
        # Applied globally since rules match on (domain, path) rather than
        # country — a /sport/ path on bbc.com is off-topic everywhere.
        if _OFF_TOPIC_RULES:
            pre = len(results)
            results = [r for r in results if not _is_off_topic_url(r.url)]
            dropped = pre - len(results)
            if dropped:
                logger.info(
                    "Brave [%s]: dropped %d/%d off-topic URLs",
                    country_code or "-", dropped, pre,
                )

        # Inverted-allowlist filter (opt-in via MPM_DOMAIN_ALLOWLIST=1).
        # Drops any result whose domain isn't in the country's effective
        # allowlist (goggle $boost ∪ global allowlist). Eliminates keyword-
        # collision noise that neither $discard nor path filters can catch.
        if USE_DOMAIN_ALLOWLIST and country_code:
            cc = self.country_configs.get(country_code)
            if cc and cc.allowed_domains:
                pre = len(results)
                results = [
                    r for r in results
                    if _is_allowlisted(r.source_domain, cc.allowed_domains)
                ]
                dropped = pre - len(results)
                if dropped:
                    logger.info(
                        "Brave [%s]: dropped %d/%d off-allowlist URLs",
                        country_code, dropped, pre,
                    )

        logger.debug("Brave News: q=%r → %d results", query, len(results))

        return BraveSearchResponse(
            query=query,
            results=results,
            total_count=len(results),
        )

    async def search_country_sources(
        self,
        country_code: str,
        query_terms: list[str],
        *,
        freshness: str = "pw",
        goggles: str | None = None,
    ) -> list[BraveSearchResponse]:
        """Run multiple queries for a country using its configured params.

        Combines each query term with the country's search params and goggle.
        Used during deep-dive collection (Step 2 in the pipeline).

        Args:
            country_code: ISO 2-letter code.
            query_terms: List of search queries (actor names, vocab terms, etc.).
            freshness: Age filter.
            goggles: URL to goggle file. If None, checks for local goggle.

        Returns:
            List of BraveSearchResponse, one per query term.
        """
        cc = self.country_configs.get(country_code)
        if not cc:
            logger.warning("No Brave config for country %s", country_code)
            return []

        # Use country goggle if available and no explicit goggle provided
        if goggles is None:
            goggles = cc.goggle_url()
            if goggles:
                logger.debug("Using goggle for %s: %s", country_code, goggles)

        logger.info("Brave: searching %s with %d query terms", country_code, len(query_terms))
        responses = []
        for term in query_terms:
            resp = await self.search_news(
                term,
                country_code=country_code,
                freshness=freshness,
                goggles=goggles,
            )
            responses.append(resp)

        total = sum(r.total_count for r in responses)
        logger.info("Brave: %s → %d queries, %d total results", country_code, len(responses), total)
        return responses

    def get_indexed_sources(self, country_code: str) -> list[IndexedSource]:
        """Return the list of Brave-indexed sources for a country."""
        cc = self.country_configs.get(country_code)
        return cc.sources if cc else []

    def get_country_config(self, country_code: str) -> CountrySearchConfig | None:
        """Return the search config for a country."""
        return self.country_configs.get(country_code)

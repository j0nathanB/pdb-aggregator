"""
Shared fixtures and loaders for PDB replay regression tests.

Two fixture types:
1. processed_events — post-dedup ProcessedEvent lists, input for dossier builder
2. clusters — post-HDBSCAN EventCluster lists, input for dedup and story arcs
"""

import json
from pathlib import Path
from typing import Optional

import numpy as np
import pytest

from src.config import LeaderConfig, LEADER_METADATA
# Import base before clustering to break circular import chain
# (clustering.__init__ -> transcript_processor -> agents.base -> agents.__init__ -> event_clustering -> clustering)
from src.agents.base import complete  # noqa: F401
from src.agents.event_clustering import ProcessedEvent
from src.clustering.clusterer import EventCluster
from src.clustering.embedder import EmbeddedSnippet

FIXTURES_DIR = Path(__file__).parent / "fixtures" / "processed_events"
CLUSTERS_DIR = Path(__file__).parent / "fixtures" / "clusters"


def load_processed_events(leader_slug: str) -> tuple[list[ProcessedEvent], list[ProcessedEvent]]:
    """
    Load processed events from fixture file.

    Args:
        leader_slug: Lowercase underscore-separated leader name (e.g., "mark_carney")

    Returns:
        Tuple of (top_events, rest_events) as ProcessedEvent lists
    """
    fixture_path = FIXTURES_DIR / f"{leader_slug}.json"
    if not fixture_path.exists():
        raise FileNotFoundError(f"Fixture not found: {fixture_path}")

    with open(fixture_path) as f:
        data = json.load(f)

    def dict_to_processed_event(d: dict) -> ProcessedEvent:
        return ProcessedEvent(
            id=d["id"],
            title=d["title"],
            articles=d.get("articles", []),
            entities=d.get("entities", []),
            summary=d.get("summary", ""),
            score=d.get("score", 0.0),
            rank=d.get("rank", 0),
            source_count=d.get("source_count", 0),
            has_wire=d.get("has_wire", False),
            embedding=d.get("embedding"),
        )

    top_events = [dict_to_processed_event(e) for e in data.get("top_events", [])]
    rest_events = [dict_to_processed_event(e) for e in data.get("rest_events", [])]

    return top_events, rest_events


def get_leader_config(leader_name: str) -> Optional[LeaderConfig]:
    """
    Get LeaderConfig for a leader by name.

    Looks up metadata from LEADER_METADATA and constructs a LeaderConfig.
    """
    if leader_name not in LEADER_METADATA:
        return None

    meta = LEADER_METADATA[leader_name]

    # Map leader name to country
    name_to_country = {
        "Mark Carney": "Canada",
        "Claudia Sheinbaum": "Mexico",
        "Volodymyr Zelenskyy": "Ukraine",
        "Lula da Silva": "Brazil",
        "Emmanuel Macron": "France",
        "Keir Starmer": "United Kingdom",
        "Friedrich Merz": "Germany",
        "Giorgia Meloni": "Italy",
        "Alexander Stubb": "Finland",
        "Donald Tusk": "Poland",
        "Gitanas Nausėda": "Lithuania",
        "Evika Siliņa": "Latvia",
        "Kristen Michal": "Estonia",
        "Maia Sandu": "Moldova",
        "Yamandú Orsi": "Uruguay",
    }

    return LeaderConfig(
        name=leader_name,
        title=meta["title"],
        country=name_to_country.get(leader_name, "Unknown"),
        region=meta["region"],
    )


def load_clusters(leader_slug: str) -> tuple[list[EventCluster], str]:
    """
    Load pre-HDBSCAN clusters from fixture file.

    Reconstructs full EventCluster objects with embeddings from the fixture,
    ready to pass to deduplicate_clusters() or detect_story_arcs().

    Args:
        leader_slug: Lowercase underscore-separated leader name

    Returns:
        Tuple of (clusters, leader_name)
    """
    fixture_path = CLUSTERS_DIR / f"{leader_slug}.json"
    if not fixture_path.exists():
        raise FileNotFoundError(f"Cluster fixture not found: {fixture_path}")

    with open(fixture_path) as f:
        data = json.load(f)

    leader_name = data["leader"]
    clusters = []

    for c in data["clusters"]:
        snippets = []
        for s in c["snippets"]:
            snippets.append(EmbeddedSnippet(
                title=s["title"],
                snippet=s["title"],  # Debug output doesn't save snippet text; title is close enough
                url=s["url"],
                source_name=s["source_name"],
                source_type=s["source_type"],
                date="",
                embedding=np.array(s["embedding"]),
            ))

        centroid = np.array(c["centroid"])
        cluster = EventCluster(
            id=c["id"],
            snippets=snippets,
            centroid=centroid,
        )
        clusters.append(cluster)

    return clusters, leader_name


# --- Pytest fixtures ---

@pytest.fixture
def carney_events():
    """Mark Carney processed events (English)."""
    return load_processed_events("mark_carney")


@pytest.fixture
def sheinbaum_events():
    """Claudia Sheinbaum processed events (Spanish)."""
    return load_processed_events("claudia_sheinbaum")


@pytest.fixture
def zelenskyy_events():
    """Volodymyr Zelenskyy processed events (Ukrainian)."""
    return load_processed_events("volodymyr_zelenskyy")


@pytest.fixture
def carney_config():
    """LeaderConfig for Mark Carney."""
    return get_leader_config("Mark Carney")


@pytest.fixture
def sheinbaum_config():
    """LeaderConfig for Claudia Sheinbaum."""
    return get_leader_config("Claudia Sheinbaum")


@pytest.fixture
def zelenskyy_config():
    """LeaderConfig for Volodymyr Zelenskyy."""
    return get_leader_config("Volodymyr Zelenskyy")


@pytest.fixture
def carney_clusters():
    """Mark Carney post-HDBSCAN clusters with embeddings."""
    return load_clusters("mark_carney")


@pytest.fixture
def sheinbaum_clusters():
    """Claudia Sheinbaum post-HDBSCAN clusters with embeddings."""
    return load_clusters("claudia_sheinbaum")


@pytest.fixture
def zelenskyy_clusters():
    """Volodymyr Zelenskyy post-HDBSCAN clusters with embeddings."""
    return load_clusters("volodymyr_zelenskyy")

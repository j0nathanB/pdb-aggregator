#!/usr/bin/env python3
"""
Extract test fixtures from debug output.

Reads debug JSON files and creates stripped-down fixtures for replay regression testing.

Two fixture types:
1. processed_events (from 06_processed_*.json) — input for dossier builder
2. clusters (from 02_clusters_*.json) — input for dedup and story arc detection

Usage:
    python scripts/extract_fixtures.py briefs/20260210/debug/
"""

import json
import sys
import numpy as np
from pathlib import Path


# Leaders to extract fixtures for (covers language diversity)
FIXTURE_LEADERS = {
    "mark_carney",           # English
    "claudia_sheinbaum",     # Spanish
    "volodymyr_zelenskyy",   # Ukrainian
}

FIXTURES_BASE = Path(__file__).parent.parent / "tests" / "fixtures"
PROCESSED_DIR = FIXTURES_BASE / "processed_events"
CLUSTERS_DIR = FIXTURES_BASE / "clusters"


def strip_embeddings(obj):
    """Recursively remove embedding fields to reduce fixture size."""
    if isinstance(obj, dict):
        return {
            k: strip_embeddings(v)
            for k, v in obj.items()
            if k != "embedding"
        }
    elif isinstance(obj, list):
        return [strip_embeddings(item) for item in obj]
    return obj


def extract_processed_events(debug_dir: Path):
    """Extract processed event fixtures (06_processed_*.json)."""
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    processed_files = sorted(debug_dir.glob("06_processed_*.json"))
    if not processed_files:
        print(f"No 06_processed_*.json files found in {debug_dir}")
        return 0

    print(f"Found {len(processed_files)} processed event files")

    extracted = 0
    for filepath in processed_files:
        slug = filepath.stem.replace("06_processed_", "")

        if slug not in FIXTURE_LEADERS:
            continue

        with open(filepath) as f:
            data = json.load(f)

        stripped = strip_embeddings(data)

        output_path = PROCESSED_DIR / f"{slug}.json"
        with open(output_path, "w") as f:
            json.dump(stripped, f, indent=2, ensure_ascii=False)

        top_count = len(stripped.get("top_events", []))
        rest_count = len(stripped.get("rest_events", []))
        size_kb = output_path.stat().st_size / 1024

        print(f"  {slug}: {top_count} top + {rest_count} rest events ({size_kb:.0f} KB)")
        extracted += 1

    return extracted


def extract_clusters(debug_dir: Path):
    """
    Extract cluster fixtures (02_clusters_*.json) with embeddings.

    The debug output only saves titles/urls/sources per snippet, not embeddings.
    We re-embed snippet titles using E5 to produce real embeddings for the fixture.
    This makes dedup and story arc tests use realistic cluster geometry.
    """
    CLUSTERS_DIR.mkdir(parents=True, exist_ok=True)

    cluster_files = sorted(debug_dir.glob("02_clusters_*.json"))
    if not cluster_files:
        print(f"No 02_clusters_*.json files found in {debug_dir}")
        return 0

    # Load embedding model once
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("intfloat/multilingual-e5-small")
    print(f"Loaded embedding model for cluster fixture generation")

    extracted = 0
    for filepath in cluster_files:
        slug = filepath.stem.replace("02_clusters_", "")

        if slug not in FIXTURE_LEADERS:
            continue

        with open(filepath) as f:
            data = json.load(f)

        # Embed all snippet titles and compute centroids
        for cluster in data["clusters"]:
            titles = [s["title"] for s in cluster["snippets"]]
            # E5 models use "passage: " prefix for documents
            prefixed = [f"passage: {t}" for t in titles]
            embeddings = model.encode(prefixed, normalize_embeddings=True)

            for snippet, emb in zip(cluster["snippets"], embeddings):
                snippet["embedding"] = emb.tolist()

            centroid = np.mean(embeddings, axis=0)
            centroid = centroid / np.linalg.norm(centroid)
            cluster["centroid"] = centroid.tolist()

        output_path = CLUSTERS_DIR / f"{slug}.json"
        with open(output_path, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        cluster_count = len(data["clusters"])
        size_kb = output_path.stat().st_size / 1024

        print(f"  {slug}: {cluster_count} clusters ({size_kb:.0f} KB)")
        extracted += 1

    return extracted


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/extract_fixtures.py <debug_dir>")
        print("Example: python scripts/extract_fixtures.py briefs/20260210/debug/")
        sys.exit(1)

    debug_dir = Path(sys.argv[1])
    if not debug_dir.is_dir():
        print(f"Not a directory: {debug_dir}")
        sys.exit(1)

    print("=== Processed Events ===")
    pe_count = extract_processed_events(debug_dir)
    print(f"Extracted {pe_count} processed event fixtures to {PROCESSED_DIR}\n")

    print("=== Clusters ===")
    cl_count = extract_clusters(debug_dir)
    print(f"Extracted {cl_count} cluster fixtures to {CLUSTERS_DIR}\n")

    print(f"Total: {pe_count + cl_count} fixtures")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Inspect search results for leaders across all sources defined in sources.csv.

CSV format:
    country,leader,source_name,domain

Outputs raw search API results to debug/search/ folder with format:
    YYYYMMDD_HHMMSS_source_name.json

Usage:
    python inspect_search.py
    python inspect_search.py --csv path/to/sources.csv
"""

import asyncio
import csv
import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from fetcher.core import search_news_searchapi, SEARCHAPI_KEY

DEFAULT_CSV = Path(__file__).parent / "sources.csv"


def load_sources(csv_path: Path) -> dict[str, list[dict]]:
    """
    Load sources from CSV, grouped by leader.

    Returns:
        Dict of leader_name -> list of source dicts
    """
    leaders: dict[str, list[dict]] = {}

    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            leader = row["leader"].strip()
            if leader not in leaders:
                leaders[leader] = []
            leaders[leader].append({
                "country": row["country"].strip(),
                "source_name": row["source_name"].strip(),
                "domain": row["domain"].strip(),
            })

    return leaders


async def search_source_all_pages(
    leader_name: str,
    source_name: str,
    domain: str,
    time_period: str = "last_week",
    max_results: int = 15,
) -> dict:
    """
    Search a single source, paginating to collect up to max_results.

    Fetches 10 per page, paginating as needed to reach max_results.
    """
    all_results = []
    page = 1
    pages_fetched = []
    num_per_page = 10

    while len(all_results) < max_results:
        results = await search_news_searchapi(
            query=leader_name,
            num_results=num_per_page,
            site=domain,
            page=page,
            time_period=time_period,
        )

        if not results:
            pages_fetched.append({
                "page": page,
                "results_count": 0,
            })
            break

        remaining = max_results - len(all_results)
        results_to_take = results[:remaining]

        pages_fetched.append({
            "page": page,
            "results_count": len(results_to_take),
        })

        all_results.extend(results_to_take)
        print(f"    Page {page}: took {len(results_to_take)} of {len(results)} results")

        if len(all_results) >= max_results or len(results) < num_per_page:
            break

        page += 1

    return {
        "leader": leader_name,
        "source_name": source_name,
        "domain": domain,
        "query": f"site:{domain} {leader_name}",
        "time_period": time_period,
        "searched_at": datetime.now().isoformat(),
        "pagination": {
            "pages_fetched": len(pages_fetched),
            "per_page": pages_fetched,
        },
        "result_count": len(all_results),
        "results": all_results,
    }


async def main():
    if not SEARCHAPI_KEY:
        print("ERROR: SEARCHAPI_KEY environment variable not set")
        sys.exit(1)

    # Parse args
    csv_path = DEFAULT_CSV
    for i, arg in enumerate(sys.argv[1:], 1):
        if arg == "--csv" and i < len(sys.argv) - 1:
            csv_path = Path(sys.argv[i + 1])

    if not csv_path.exists():
        print(f"ERROR: CSV file not found: {csv_path}")
        sys.exit(1)

    # Load sources from CSV
    leaders = load_sources(csv_path)
    time_period = "last_week"

    # Create output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path("debug") / "search" / timestamp
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"CSV: {csv_path}")
    print(f"Time period: {time_period}")
    print(f"Output directory: {output_dir}")
    print("-" * 60)

    for leader_name, sources in leaders.items():
        country = sources[0]["country"]
        print(f"\n{leader_name} ({country})")
        print(f"  Sources: {len(sources)}")
        for src in sources:
            print(f"    - {src['source_name']} ({src['domain']})")

    print("-" * 60)

    # Search all leaders and sources
    all_results = []

    for leader_name, sources in leaders.items():
        print(f"\n{'=' * 40}")
        print(f"  {leader_name}")
        print(f"{'=' * 40}")

        for source in sources:
            print(f"\n  Searching {source['source_name']}...")

            try:
                result = await search_source_all_pages(
                    leader_name=leader_name,
                    source_name=source["source_name"],
                    domain=source["domain"],
                    time_period=time_period,
                    max_results=15,
                )

                safe_leader = leader_name.lower().replace(" ", "_")
                safe_source = source["source_name"].lower().replace(" ", "_").replace("&", "and")
                filename = f"{timestamp}_{safe_leader}_{safe_source}.json"
                filepath = output_dir / filename

                with open(filepath, "w") as f:
                    json.dump(result, f, indent=2)

                pages = result["pagination"]["pages_fetched"]
                print(f"  Total: {result['result_count']} results across {pages} pages -> {filename}")
                all_results.append(result)

            except Exception as e:
                print(f"  ERROR: {e}")
                import traceback
                traceback.print_exc()
                all_results.append({
                    "leader": leader_name,
                    "source_name": source["source_name"],
                    "error": str(e),
                    "searched_at": datetime.now().isoformat(),
                })

    # Save summary
    summary = {
        "time_period": time_period,
        "csv": str(csv_path),
        "searched_at": datetime.now().isoformat(),
        "leaders_searched": list(leaders.keys()),
        "total_sources": sum(len(s) for s in leaders.values()),
        "total_results": sum(r.get("result_count", 0) for r in all_results),
        "per_source_summary": [
            {
                "leader": r.get("leader"),
                "source": r.get("source_name"),
                "count": r.get("result_count", 0),
                "pages": r.get("pagination", {}).get("pages_fetched", 0),
                "error": r.get("error"),
            }
            for r in all_results
        ],
    }

    summary_path = output_dir / f"{timestamp}_summary.json"
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Leaders searched: {len(leaders)}")
    print(f"Total sources: {summary['total_sources']}")
    print(f"Total results: {summary['total_results']}")
    print("\nPer-source breakdown:")
    for s in summary["per_source_summary"]:
        pages = s.get("pages", "?")
        print(f"  - {s['leader']} / {s['source']}: {s['count']} results ({pages} pages)")
    print(f"\nOutput: {output_dir}")


if __name__ == "__main__":
    asyncio.run(main())

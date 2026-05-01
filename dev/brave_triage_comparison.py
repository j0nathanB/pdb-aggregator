"""
Compare Brave News API (with goggles) vs triage agent's Claude web_search
for Mexico, week of March 16-22 2026.
"""
import asyncio
import json
import sys
sys.path.insert(0, ".")

from src.monitor.collection.brave import BraveNewsClient


# Triage-equivalent queries: actor names + key topics from the triage scan prompt
QUERIES = [
    "Sheinbaum",
    "García Harfuch seguridad",
    "USMCA T-MEC negociaciones",
    "Morena reforma electoral",
    "PEMEX energía",
    "SEDENA SEMAR despliegue",
    "de la Fuente cancillería",
    "Banxico inversión",
]


async def main():
    async with BraveNewsClient() as client:
        for q in QUERIES:
            resp = await client.search_news(
                q,
                country_code="mx",
                freshness="2026-03-15to2026-03-22",
                count=20,
            )
            print(f"\n{'='*80}")
            print(f"QUERY: {q!r} → {resp.total_count} results")
            print(f"{'='*80}")
            for i, r in enumerate(resp.results, 1):
                age = f" ({r.age})" if r.age else ""
                src = r.source_domain or "?"
                print(f"  {i:2d}. [{src}] {r.title}{age}")
                print(f"      {r.url}")
                if r.description:
                    print(f"      {r.description[:120]}")
        print(f"\nBrave API calls: {client.api_call_count}")


if __name__ == "__main__":
    asyncio.run(main())

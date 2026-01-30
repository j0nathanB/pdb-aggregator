#!/usr/bin/env python3
"""Debug the SearchAPI response format."""

import asyncio
import json
import os
import httpx

SEARCHAPI_KEY = os.environ.get("SEARCHAPI_KEY")

async def test_search():
    params = {
        "engine": "google_news",
        "q": "Mark Carney",
        "api_key": SEARCHAPI_KEY,
        "num": 5,
    }

    print(f"API Key: {SEARCHAPI_KEY[:8]}..." if SEARCHAPI_KEY else "No API key!")
    print(f"Params: {json.dumps({k:v for k,v in params.items() if k != 'api_key'}, indent=2)}")
    print("-" * 60)

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            "https://www.searchapi.io/api/v1/search",
            params=params,
        )
        print(f"Status: {response.status_code}")
        print(f"Response type: {type(response.json())}")
        print("-" * 60)

        data = response.json()
        print(json.dumps(data, indent=2)[:3000])

        # Check structure
        print("\n" + "=" * 60)
        print("STRUCTURE:")
        if isinstance(data, dict):
            for key in data.keys():
                val = data[key]
                print(f"  {key}: {type(val).__name__}", end="")
                if isinstance(val, list):
                    print(f" (len={len(val)})", end="")
                    if val:
                        print(f" - first item type: {type(val[0]).__name__}")
                    else:
                        print()
                else:
                    print()

if __name__ == "__main__":
    asyncio.run(test_search())

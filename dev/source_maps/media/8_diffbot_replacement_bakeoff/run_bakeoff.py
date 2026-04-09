"""Bake-off: curl vs diffbot vs playwright vs browserbase.

Purpose
-------
Determine whether Browserbase can replace Diffbot as the primary
anti-bot fallback. Tests the 42 domains where Diffbot was actually
invoked in recent production runs.

Usage
-----
    .venv/bin/python dev/source_maps/media/8_diffbot_replacement_bakeoff/run_bakeoff.py

Reads from:  ./input_urls.json (produced by the URL-builder script)
Writes to:   ./results.json    (one record per URL × method)

Each method runs independently per URL; they do not gate each other.
Diffbot calls go through the same DiffbotExtractor used in production,
which enforces the 5/min rate limit via its token bucket.
"""
from __future__ import annotations

import asyncio
import json
import logging
import sys
import time
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))

from src.monitor.collection.extract import (  # noqa: E402
    BrowserbaseExtractor,
    CurlTrafilaturaExtractor,
    DiffbotExtractor,
    ExtractionResult,
    PlaywrightExtractor,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
# Silence httpx INFO logs (secrets-in-URLs).
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger("bakeoff")

HERE = Path(__file__).parent
INPUT = HERE / "input_urls.json"
OUTPUT = HERE / "results.json"
PROGRESS = HERE / "progress.json"

# Per-method concurrency caps so slower methods don't drown the box.
CONCURRENCY = {
    "curl": 10,
    "diffbot": 1,  # DiffbotExtractor's own bucket gates real throughput
    "playwright": 3,
    "browserbase": 5,  # browserbase supports 25 concurrent sessions on our plan
}


def serialize_result(r: ExtractionResult) -> dict:
    """Trim the full ExtractionResult to just the bake-off fields we care about."""
    text = r.text or ""
    return {
        "success": r.success,
        "method": r.method,
        "latency_ms": r.latency_ms,
        "text_length": len(text),
        "text_ok": bool(text and len(text.strip()) >= 200),
        "title": (r.title or "")[:200],
        "error": (r.error or "")[:300],
        "snippet": text[:200],
    }


async def run_method(
    name: str,
    extractor,
    urls: list[str],
    sem: asyncio.Semaphore,
) -> dict:
    """Run one extraction method across all URLs, return {url: result_dict}."""
    results: dict[str, dict] = {}

    async def _one(url: str) -> tuple[str, dict]:
        async with sem:
            start = time.monotonic()
            try:
                r = await extractor.extract(url)
                r_dict = serialize_result(r)
            except Exception as e:
                r_dict = {
                    "success": False,
                    "method": name,
                    "latency_ms": int((time.monotonic() - start) * 1000),
                    "text_length": 0,
                    "text_ok": False,
                    "title": "",
                    "error": f"harness exception: {e}",
                    "snippet": "",
                }
            return url, r_dict

    tasks = [asyncio.create_task(_one(u)) for u in urls]
    done = 0
    for task in asyncio.as_completed(tasks):
        url, r = await task
        results[url] = r
        done += 1
        status = "OK" if r["text_ok"] else ("NOCONTENT" if r["success"] else "FAIL")
        logger.info(
            "[%s] %d/%d %s %s (%sms)",
            name, done, len(urls), status, url[:80], r["latency_ms"],
        )

    return results


async def main() -> int:
    if not INPUT.exists():
        logger.error("No input file at %s — run the URL-builder first", INPUT)
        return 1

    test_set: dict = json.loads(INPUT.read_text())
    all_urls: list[str] = []
    domain_for: dict[str, str] = {}
    for domain, spec in test_set.items():
        for url in spec.get("urls", []):
            all_urls.append(url)
            domain_for[url] = domain

    logger.info("Loaded %d URLs across %d domains", len(all_urls), len(test_set))

    # Initialize extractors. DiffbotExtractor reuses the production class
    # including its 5/min token bucket.
    curl_ext = CurlTrafilaturaExtractor()
    diffbot_ext = DiffbotExtractor(max_wait_seconds=120.0)  # be generous in the test
    pw_ext = PlaywrightExtractor()
    bb_ext = BrowserbaseExtractor()

    sems = {name: asyncio.Semaphore(CONCURRENCY[name]) for name in CONCURRENCY}

    # Run all four methods concurrently at the top level. Each method's
    # own semaphore + the diffbot bucket pace them internally.
    logger.info("Kicking off all four methods in parallel...")
    t0 = time.monotonic()

    curl_task = asyncio.create_task(run_method("curl", curl_ext, all_urls, sems["curl"]))
    diffbot_task = asyncio.create_task(run_method("diffbot", diffbot_ext, all_urls, sems["diffbot"]))
    pw_task = asyncio.create_task(run_method("playwright", pw_ext, all_urls, sems["playwright"]))
    bb_task = asyncio.create_task(run_method("browserbase", bb_ext, all_urls, sems["browserbase"]))

    curl_results = await curl_task
    logger.info("curl finished in %.1fs", time.monotonic() - t0)
    pw_results = await pw_task
    logger.info("playwright finished in %.1fs", time.monotonic() - t0)
    bb_results = await bb_task
    logger.info("browserbase finished in %.1fs", time.monotonic() - t0)
    diffbot_results = await diffbot_task
    logger.info("diffbot finished in %.1fs", time.monotonic() - t0)

    await curl_ext.close() if hasattr(curl_ext, "close") else None
    await diffbot_ext.close()
    # playwright/browserbase do not need an explicit close — their resources
    # are per-call.

    # Aggregate per URL
    records = []
    for url in all_urls:
        records.append({
            "domain": domain_for[url],
            "url": url,
            "curl": curl_results.get(url, {"success": False, "error": "not run"}),
            "diffbot": diffbot_results.get(url, {"success": False, "error": "not run"}),
            "playwright": pw_results.get(url, {"success": False, "error": "not run"}),
            "browserbase": bb_results.get(url, {"success": False, "error": "not run"}),
        })

    OUTPUT.write_text(json.dumps(
        {
            "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "total_urls": len(all_urls),
            "total_domains": len(test_set),
            "wall_time_seconds": round(time.monotonic() - t0, 1),
            "results": records,
        },
        indent=2,
        ensure_ascii=False,
    ))
    logger.info("Wrote %s", OUTPUT)
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))

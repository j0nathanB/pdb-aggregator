"""
A/B comparison report for optimization changes.

Run manually for human review:
    pytest tests/test_optimization_comparison.py -v --timeout=600 -s

Generates a structured report to tests/reports/ for side-by-side comparison
before/after optimization changes.
"""

import json
import asyncio
from datetime import datetime
from pathlib import Path

import pytest

from src.agents.dossier_builder import DossierBuilderAgent
from tests.conftest import load_processed_events, get_leader_config


REPORTS_DIR = Path(__file__).parent / "reports"


@pytest.fixture
def builder():
    return DossierBuilderAgent()


@pytest.mark.timeout(600)
class TestOptimizationComparison:
    """Generate comparison report for manual review."""

    @pytest.mark.asyncio
    async def test_generate_carney_report(self, builder):
        """Run dossier builder on Carney fixture and save structured report."""
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)

        top_events, rest_events = load_processed_events("mark_carney")
        leader = get_leader_config("Mark Carney")

        dossier = await builder.build_from_events(
            leader=leader,
            top_events=top_events,
            remaining_events=rest_events,
        )

        # Build structured report
        report = {
            "leader": leader.name,
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "total_stories": (
                    len(dossier.main_stories)
                    + len(dossier.international_stories)
                    + len(dossier.domestic_stories)
                ),
                "main_stories": len(dossier.main_stories),
                "international_stories": len(dossier.international_stories),
                "domestic_stories": len(dossier.domestic_stories),
                "btl_bullets": len(dossier.between_the_lines),
                "has_exec_summary": bool(dossier.executive_summary),
            },
            "executive_summary": dossier.executive_summary,
            "main_stories": [
                {
                    "title": s.title,
                    "narrative_length": len(s.narrative),
                    "scope": s.scope.value if hasattr(s.scope, "value") else s.scope,
                    "source_count": s.source_count,
                    "score": s.score,
                    "classification": {
                        "event_type": s.classification.event_type.value if s.classification else None,
                        "leader_role": s.classification.leader_role.value if s.classification else None,
                        "impact_level": s.classification.impact_level.value if s.classification else None,
                        "priority_score": s.classification.priority_score if s.classification else None,
                    } if s.classification else None,
                    "narrative_preview": s.narrative[:200],
                }
                for s in dossier.main_stories
            ],
            "overflow_stories": [
                {
                    "title": s.title,
                    "scope": s.scope.value if hasattr(s.scope, "value") else s.scope,
                    "source_count": s.source_count,
                    "classification": {
                        "event_type": s.classification.event_type.value if s.classification else None,
                        "leader_role": s.classification.leader_role.value if s.classification else None,
                        "impact_level": s.classification.impact_level.value if s.classification else None,
                        "priority_score": s.classification.priority_score if s.classification else None,
                    } if s.classification else None,
                }
                for s in dossier.international_stories + dossier.domestic_stories
            ],
            "between_the_lines": dossier.between_the_lines,
        }

        # Save report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = REPORTS_DIR / f"carney_{timestamp}.json"
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        print(f"\nReport saved to: {report_path}")
        print(f"Total stories: {report['summary']['total_stories']}")
        print(f"Main stories: {report['summary']['main_stories']}")
        print(f"BTL bullets: {report['summary']['btl_bullets']}")
        print(f"Executive summary: {report['executive_summary'][:200]}...")

        for i, story in enumerate(report["main_stories"]):
            print(f"\n  Main {i+1}: {story['title']}")
            cls = story.get("classification")
            if cls:
                print(f"    Type: {cls['event_type']}, Role: {cls['leader_role']}, "
                      f"Impact: {cls['impact_level']}, Priority: {cls['priority_score']}")

        # Basic assertions to make this a valid test
        assert report["summary"]["total_stories"] > 0
        assert report["summary"]["has_exec_summary"]

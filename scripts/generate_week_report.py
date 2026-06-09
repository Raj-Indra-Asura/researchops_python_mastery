#!/usr/bin/env python3
"""Generate a weekly progress report.

Usage:
    python scripts/generate_week_report.py --week 3

Outputs a markdown summary of completed / pending items for the week.
"""

from __future__ import annotations

import argparse
from pathlib import Path


def generate_report(week: int) -> None:
    root = Path(__file__).parent.parent

    # Map week number to curriculum path
    month = (week - 1) // 4 + 1
    month_dirs = {
        1: "month-01-python-core",
        2: "month-02-data-storage-concurrency",
        3: "month-03-ml-engineering",
        4: "month-04-ai-engineering-api-workers",
        5: "month-05-production-portfolio",
    }

    week_names = {
        1: "week-01-foundations",
        2: "week-02-files-errors-logging",
        3: "week-03-oop-domain-modeling",
        4: "week-04-cli-packaging",
        5: "week-05-sqlite-storage",
        6: "week-06-pdf-parsing-pipeline",
        7: "week-07-keyword-search-data-quality",
        8: "week-08-multiprocessing-ingestion",
        9: "week-09-protocols-clean-architecture",
        10: "week-10-testing-quality-gates",
        11: "week-11-classical-ml-topic-classification",
        12: "week-12-experiment-tracking",
        13: "week-13-embeddings-semantic-search",
        14: "week-14-fastapi-layer",
        15: "week-15-async-io-network-fetching",
        16: "week-16-local-worker-job-system",
        17: "week-17-rag-assistant",
        18: "week-18-docker-environment-config",
        19: "week-19-documentation-portfolio-polish",
        20: "week-20-final-hardening-v1-release",
    }

    week_dir = root / "curriculum" / month_dirs[month] / week_names[week]

    print(f"\n# Week {week} Report\n")

    files = ["README.md", "notes.md", "exercises.md", "break_it.md", "validation.md", "reflection.md"]
    for fname in files:
        path = week_dir / fname
        status = "✅" if path.exists() and path.stat().st_size > 100 else "❌"
        print(f"{status} {fname}")

    reflection = week_dir / "reflection.md"
    if reflection.exists():
        content = reflection.read_text()
        if "confidence score" in content.lower():
            print("\n⚠️  Remember to fill in your reflection.md before moving to the next week!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a weekly report")
    parser.add_argument("--week", type=int, required=True, help="Week number (1-20)")
    args = parser.parse_args()
    generate_report(args.week)

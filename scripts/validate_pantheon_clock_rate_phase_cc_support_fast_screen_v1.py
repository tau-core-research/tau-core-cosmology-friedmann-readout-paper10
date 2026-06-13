#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GRID = ROOT / "data/derived/pantheon_clock_rate_phase_cc_support_fast_screen_v1_grid.csv"
FAMILY = ROOT / "data/derived/pantheon_clock_rate_phase_cc_support_fast_screen_v1_family_summary.csv"
SUMMARY = ROOT / "data/derived/pantheon_clock_rate_phase_cc_support_fast_screen_v1_summary.csv"
CLAIM_BOUNDARY = "clock_rate_phase_cc_support_fast_screen_source_frozen_not_replay_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    grid = read_rows(GRID)
    family = read_rows(FAMILY)
    summary_rows = read_rows(SUMMARY)
    require(len(summary_rows) == 1, "summary must contain one row")
    summary = summary_rows[0]
    require(len(grid) == 3476, f"unexpected grid row count: {len(grid)}")
    require(len(family) == 3, f"unexpected family count: {len(family)}")
    require(summary["status"] == "PREAUTH_FAST_SCREEN_COMPLETE_NOT_REPLAY_NOT_VALIDATION", "bad status")
    require(summary["n_rows"] == "1370", "expected 1370 CC-support rows")
    require(summary["endpoint_replay_allowed"] == "false", "fast screen must not allow replay")
    require(summary["endpoint_validation_claimed"] == "false", "fast screen must not claim validation")
    require(summary["physical_validation_claimed"] == "false", "fast screen must not claim physical validation")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "bad claim boundary")
    for row in grid + family:
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "bad row claim boundary")
    print(
        "PAPER10_CLOCK_RATE_PHASE_CC_SUPPORT_FAST_SCREEN_VALIDATED "
        f"verdict={summary['verdict']} best_family={summary['best_candidate_family']}"
    )


if __name__ == "__main__":
    main()

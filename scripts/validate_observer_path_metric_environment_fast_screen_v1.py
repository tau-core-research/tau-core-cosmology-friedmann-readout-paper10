#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GRID = ROOT / "data/derived/observer_path_metric_environment_fast_screen_v1_grid.csv"
FAMILY_SUMMARY = ROOT / "data/derived/observer_path_metric_environment_fast_screen_v1_family_summary.csv"
SUMMARY = ROOT / "data/derived/observer_path_metric_environment_fast_screen_v1_summary.csv"
DOC = ROOT / "docs/observer_path_metric_environment_fast_screen_v1.md"
CLAIM_BOUNDARY = "observer_path_metric_environment_fast_screen_not_endpoint_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    grid = read_rows(GRID)
    families = read_rows(FAMILY_SUMMARY)
    summary_rows = read_rows(SUMMARY)
    if len(summary_rows) != 1:
        raise SystemExit("summary must contain one row")
    summary = summary_rows[0]
    if len(families) != 7:
        raise SystemExit("expected seven metric-environment candidate families")
    if int(summary["grid_rows"]) != len(grid):
        raise SystemExit("grid row count mismatch")
    for rows in [grid, families, summary_rows]:
        for row in rows:
            if row["claim_boundary"] != CLAIM_BOUNDARY:
                raise SystemExit("claim boundary mismatch")
            if row["endpoint_replay_allowed"] != "false":
                raise SystemExit("screen must not authorize endpoint replay")
            if row["endpoint_validation_claimed"] != "false":
                raise SystemExit("screen must not claim validation")
            if row["physical_lensing_path_weight_claimed"] != "false":
                raise SystemExit("screen must not claim physical lensing")
    if summary["n_rows"] != "12":
        raise SystemExit("screen must use the frozen 12-row scope")
    if summary["best_candidate_family"] not in {row["family_id"] for row in families}:
        raise SystemExit("best family missing from family summary")
    text = DOC.read_text()
    for marker in ["not endpoint replay", "Delta chi2 versus baseline", CLAIM_BOUNDARY]:
        if marker not in text:
            raise SystemExit(f"doc missing marker: {marker}")
    print(
        "OBSERVER_PATH_METRIC_ENVIRONMENT_FAST_SCREEN_V1_VALIDATED "
        f"best={summary['best_candidate_family']} verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/paper10_desi_shape_route_robustness_stress_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_shape_route_robustness_stress_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_shape_route_robustness_stress_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    rows = read_rows(OUT)
    summary = read_one(SUMMARY)
    require(summary["status"] == "DESI_SHAPE_ROUTE_ROBUSTNESS_STRESS_BUILT_PERMISSION_REPLAY_NOT_VALIDATION", "bad status")
    require(summary["endpoint_replay_allowed"] == "true", "robustness stress follows authorized replay")
    require(summary["endpoint_validation_claimed"] == "false", "must not claim endpoint validation")
    require(summary["physical_validation_claimed"] == "false", "must not claim physical validation")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    require(len([row for row in rows if row["test_family"] == "leave_one"]) == 4, "leave-one count mismatch")
    require(len([row for row in rows if row["test_family"] == "leave_two"]) == 6, "leave-two count mismatch")
    require(summary["candidate_score_rank_among_replay_branches"] == "1", "candidate should remain top-ranked by score")
    require(
        summary["verdict"]
        in {
            "positive_but_narrow_margin_and_row_sensitive_not_validation",
            "positive_and_internally_robust_not_validation",
            "mixed_robustness_not_validation",
        },
        "bad verdict",
    )
    for row in rows:
        require(row["endpoint_validation_claimed"] == "false", "row must not claim validation")
        require(row["physical_validation_claimed"] == "false", "row must not claim physical validation")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
        float(row["shape_rms"])
        float(row["shape_quadratic_score"])
        float(row["score_fraction_of_full_candidate"])
    print(
        "PAPER10_DESI_SHAPE_ROUTE_ROBUSTNESS_STRESS_VALIDATED "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()

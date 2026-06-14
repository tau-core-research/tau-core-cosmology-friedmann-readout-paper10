#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_numeric_t_joint_source_route_overlap_metric_v1.csv"
SUMMARY = ROOT / "data/derived/joint_numeric_t_joint_source_route_overlap_metric_v1_summary.csv"
DOC = ROOT / "docs/joint_numeric_t_joint_source_route_overlap_metric_v1.md"
CLAIM_BOUNDARY = "joint_numeric_t_joint_source_route_overlap_metric_not_scoring_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    rows = read_rows(OUT)
    summary_rows = read_rows(SUMMARY)
    require(len(rows) == 2, "expected two route rows")
    require(len(summary_rows) == 1, "summary must contain one row")
    summary = summary_rows[0]
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "wrong claim boundary")
    require(summary["uses_endpoint_scores_or_residuals"] == "false", "must not use endpoint scores/residuals")
    require(summary["numeric_t_joint_rescoring_allowed"] == "false", "rescoring must remain forbidden")
    require(summary["penalty_admissible_now"] == "false", "penalty must remain inadmissible")
    require(float(summary["jaccard_distance"]) > 0.75, "route distance should indicate largely distinct routes")
    for row in rows:
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
        require(row["uses_endpoint_scores_or_residuals"] == "false", "row must be residual-blind")
        require(row["numeric_t_joint_rescoring_allowed"] == "false", "row rescoring must remain false")
    text = DOC.read_text()
    for marker in [CLAIM_BOUNDARY, "not authorize a penalty", "endpoint residuals"]:
        require(marker in text, f"doc missing marker: {marker}")
    print(
        "JOINT_NUMERIC_T_JOINT_SOURCE_ROUTE_OVERLAP_METRIC_V1_VALIDATED "
        f"distance={summary['jaccard_distance']}"
    )


if __name__ == "__main__":
    main()

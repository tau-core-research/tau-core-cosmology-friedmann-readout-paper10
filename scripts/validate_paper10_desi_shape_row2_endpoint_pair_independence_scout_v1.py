#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROWS = ROOT / "data/derived/paper10_desi_shape_row2_endpoint_pair_independence_scout_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_shape_row2_endpoint_pair_independence_scout_v1_summary.csv"
DOC = ROOT / "docs/paper10_desi_shape_row2_endpoint_pair_independence_scout_v1.md"
CLAIM_BOUNDARY = "paper10_desi_shape_row2_endpoint_pair_independence_scout_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    rows = read_rows(ROWS)
    summary_rows = read_rows(SUMMARY)
    require(len(summary_rows) == 1, "row2 endpoint-pair scout summary must contain one row")
    summary = summary_rows[0]
    require(
        summary["status"] == "DESI_SHAPE_ROW2_ENDPOINT_PAIR_INDEPENDENCE_SCOUT_BUILT_NOT_REPLAY_NOT_VALIDATION",
        "bad summary status",
    )
    require(summary["left_strict_independent_count"] == "0", "left endpoint should not have strict independent support")
    require(summary["right_strict_independent_count"] == "1", "right endpoint should have one strict independent support")
    require(summary["right_best_independent_candidate"] == "Moresco (2015)", "expected Moresco 2015 right endpoint context")
    require(summary["endpoint_pair_independence_satisfied"] == "false", "endpoint-pair independence must remain unsatisfied")
    require(summary["row2_promotion_ready"] == "false", "row2 must not be promotion-ready")
    require(summary["shape_route_promotion_allowed"] == "false", "shape route promotion must remain disabled")
    require(summary["endpoint_replay_allowed"] == "false", "summary replay flag mismatch")
    require(summary["endpoint_validation_claimed"] == "false", "summary validation flag mismatch")
    require(summary["physical_validation_claimed"] == "false", "summary physical validation flag mismatch")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    require(
        summary["verdict"] == "row2_endpoint_pair_independence_not_satisfied_in_frozen_CC_table",
        "bad verdict",
    )
    right_moresco = [
        row for row in rows
        if row["endpoint_label"] == "right"
        and row["candidate_reference"] == "Moresco (2015)"
        and row["support_class"] == "strict_independent_endpoint_support"
    ]
    require(len(right_moresco) == 1, "expected one right-endpoint Moresco 2015 strict support row")
    left_strict = [
        row for row in rows
        if row["endpoint_label"] == "left" and row["support_class"] == "strict_independent_endpoint_support"
    ]
    require(not left_strict, "left endpoint strict independent support should be absent")
    require({row["endpoint_replay_allowed"] for row in rows} == {"false"}, "rows must not authorize replay")
    require({row["endpoint_validation_claimed"] for row in rows} == {"false"}, "rows must not claim validation")
    require({row["physical_validation_claimed"] for row in rows} == {"false"}, "rows must not claim physical validation")
    require({row["claim_boundary"] for row in rows} == {CLAIM_BOUNDARY}, "row claim boundary mismatch")
    require(DOC.exists() and DOC.stat().st_size > 0, "missing scout documentation")
    print("paper10_desi_shape_row2_endpoint_pair_independence_scout_v1: OK")


if __name__ == "__main__":
    main()

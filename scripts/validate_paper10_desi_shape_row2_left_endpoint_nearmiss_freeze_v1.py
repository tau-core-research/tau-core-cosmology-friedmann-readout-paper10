#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROWS = ROOT / "data/derived/paper10_desi_shape_row2_left_endpoint_nearmiss_freeze_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_shape_row2_left_endpoint_nearmiss_freeze_v1_summary.csv"
DOC = ROOT / "docs/paper10_desi_shape_row2_left_endpoint_nearmiss_freeze_v1.md"
CLAIM_BOUNDARY = "paper10_desi_shape_row2_left_endpoint_nearmiss_freeze_not_validation"


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
    require(len(summary_rows) == 1, "row2 left near-miss summary must contain one row")
    summary = summary_rows[0]
    require(
        summary["status"] == "DESI_SHAPE_ROW2_LEFT_ENDPOINT_NEARMISS_CONTEXT_FROZEN_NOT_REPLAY_NOT_VALIDATION",
        "bad summary status",
    )
    require(summary["relaxed_independent_left_candidate_count"] == "2", "expected two relaxed left near-misses")
    require(summary["strict_independent_left_support_count"] == "0", "strict left support must remain absent")
    require(summary["closest_relaxed_independent_candidate"] == "Stern et al. (2010)", "expected Stern 2010 as closest near-miss")
    require(summary["closest_relaxed_independent_delta_z"] == "0.054", "unexpected closest near-miss delta-z")
    require(summary["left_endpoint_release_allowed"] == "false", "left endpoint release must remain disabled")
    require(summary["endpoint_pair_independence_satisfied"] == "false", "endpoint-pair independence must remain false")
    require(summary["row2_promotion_ready"] == "false", "row2 must not be promotion-ready")
    require(summary["shape_route_promotion_allowed"] == "false", "shape route promotion must remain disabled")
    require(summary["endpoint_replay_allowed"] == "false", "summary replay flag mismatch")
    require(summary["endpoint_validation_claimed"] == "false", "summary validation flag mismatch")
    require(summary["physical_validation_claimed"] == "false", "summary physical validation flag mismatch")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    require(
        summary["verdict"] == "row2_left_endpoint_has_relaxed_independent_nearmisses_but_no_strict_support",
        "bad verdict",
    )
    require(len(rows) == 2, "expected two frozen near-miss rows")
    refs = {row["candidate_reference"] for row in rows}
    require(refs == {"Stern et al. (2010)", "Moresco et al. (2012)"}, "unexpected near-miss references")
    require({row["endpoint_label"] for row in rows} == {"left"}, "all rows must be left endpoint")
    require({row["within_strict_endpoint_window"] for row in rows} == {"false"}, "near-misses must remain outside strict window")
    require({row["within_relaxed_endpoint_window"] for row in rows} == {"true"}, "near-misses must be inside relaxed window")
    require({row["left_endpoint_release_allowed"] for row in rows} == {"false"}, "rows must not release left endpoint")
    require({row["endpoint_replay_allowed"] for row in rows} == {"false"}, "rows must not authorize replay")
    require({row["endpoint_validation_claimed"] for row in rows} == {"false"}, "rows must not claim validation")
    require({row["physical_validation_claimed"] for row in rows} == {"false"}, "rows must not claim physical validation")
    require({row["claim_boundary"] for row in rows} == {CLAIM_BOUNDARY}, "row claim boundary mismatch")
    require(DOC.exists() and DOC.stat().st_size > 0, "missing near-miss documentation")
    print("paper10_desi_shape_row2_left_endpoint_nearmiss_freeze_v1: OK")


if __name__ == "__main__":
    main()

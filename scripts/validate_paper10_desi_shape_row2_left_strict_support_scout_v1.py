#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROWS = ROOT / "data/derived/paper10_desi_shape_row2_left_strict_support_scout_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_shape_row2_left_strict_support_scout_v1_summary.csv"
DOC = ROOT / "docs/paper10_desi_shape_row2_left_strict_support_scout_v1.md"
CLAIM_BOUNDARY = "paper10_desi_shape_row2_left_strict_support_scout_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def require_false(row: dict[str, str], fields: list[str], label: str) -> None:
    for field in fields:
        if row.get(field) != "false":
            raise SystemExit(f"{label} {field} must be false")


def main() -> None:
    rows = read_rows(ROWS)
    summary_rows = read_rows(SUMMARY)
    if len(summary_rows) != 1:
        raise SystemExit("strict-support scout summary must contain one row")
    summary = summary_rows[0]
    false_fields = [
        "left_endpoint_release_allowed",
        "row2_promotion_ready",
        "shape_route_promotion_allowed",
        "endpoint_replay_allowed",
        "endpoint_validation_claimed",
        "physical_validation_claimed",
    ]
    require_false(summary, false_fields, "summary")
    if summary["status"] != "DESI_SHAPE_ROW2_LEFT_STRICT_SUPPORT_SCOUT_BUILT_NOT_REPLAY_NOT_VALIDATION":
        raise SystemExit("bad strict-support scout status")
    if summary["strict_independent_support_count"] != "0":
        raise SystemExit("strict independent support must remain absent")
    if summary["strict_any_support_count"] != "1":
        raise SystemExit("expected only the current same-family strict point in the frozen CC table")
    if summary["nearest_candidate_reference"] != "Simon et al. (2005)":
        raise SystemExit("expected Simon 2005 as nearest frozen same-family candidate")
    if summary["nearest_candidate_abs_delta_z"] != "0.034":
        raise SystemExit("unexpected nearest candidate delta-z")
    if summary["nearest_independent_candidate_reference"] != "Stern et al. (2010)":
        raise SystemExit("expected Stern 2010 as nearest independent frozen candidate")
    if summary["nearest_independent_candidate_abs_delta_z"] != "0.054":
        raise SystemExit("unexpected nearest independent candidate delta-z")
    if summary["verdict"] != "row2_left_strict_support_absent_in_frozen_cc_table":
        raise SystemExit("bad strict-support scout verdict")
    if summary["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("summary claim boundary mismatch")
    if not rows:
        raise SystemExit("strict-support scout rows must not be empty")
    for row in rows:
        require_false(row, false_fields, f"row {row['candidate_reference']}")
        if row["claim_boundary"] != CLAIM_BOUNDARY:
            raise SystemExit("row claim boundary mismatch")
    strict_independent = [
        row
        for row in rows
        if row["within_strict_endpoint_window"] == "true"
        and row["independent_of_current_left_family"] == "true"
    ]
    if strict_independent:
        raise SystemExit("strict independent rows must be absent")
    if not DOC.exists() or DOC.stat().st_size == 0:
        raise SystemExit("missing strict-support scout documentation")
    print("PAPER10_DESI_SHAPE_ROW2_LEFT_STRICT_SUPPORT_SCOUT_VALIDATED")


if __name__ == "__main__":
    main()

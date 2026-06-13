#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROWS = ROOT / "data/derived/paper10_desi_shape_row2_source_native_shape_support_scout_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_shape_row2_source_native_shape_support_scout_v1_summary.csv"
DOC = ROOT / "docs/paper10_desi_shape_row2_source_native_shape_support_scout_v1.md"
CLAIM_BOUNDARY = "paper10_desi_shape_row2_source_native_shape_support_scout_not_validation"


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
        raise SystemExit("source-native shape support summary must contain one row")
    summary = summary_rows[0]
    false_fields = [
        "uses_endpoint_scores",
        "uses_endpoint_residuals",
        "row2_promotion_ready",
        "shape_route_promotion_allowed",
        "endpoint_replay_allowed",
        "endpoint_validation_claimed",
        "physical_validation_claimed",
    ]
    require_false(summary, false_fields + ["left_endpoint_release_allowed"], "summary")
    if summary["status"] != "DESI_SHAPE_ROW2_SOURCE_NATIVE_SHAPE_SUPPORT_SCOUT_BUILT_NOT_REPLAY_NOT_VALIDATION":
        raise SystemExit("bad source-native scout status")
    if summary["source_native_row_count"] != "4":
        raise SystemExit("expected four source-native Row2 BAO rows")
    if summary["row2_covariance_positive_definite"] != "true":
        raise SystemExit("Row2 covariance subblock must be positive definite")
    if "delta_log_anisotropy_DM_over_DH=" not in summary["shape_vector_components"]:
        raise SystemExit("missing anisotropy shape-vector component")
    if summary["verdict"] != "row2_source_native_desi_bao_shape_support_present_but_not_promotion_ready":
        raise SystemExit("bad source-native scout verdict")
    if summary["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("summary claim boundary mismatch")
    if len(rows) != 4:
        raise SystemExit("expected four source-native support rows")
    if {row["quantity"] for row in rows} != {"DM_over_rs", "DH_over_rs"}:
        raise SystemExit("source-native rows must include DM and DH")
    if {row["z_eff"] for row in rows} != {"0.93400000", "1.32100000"}:
        raise SystemExit("source-native rows must be row2 endpoints")
    for row in rows:
        require_false(row, false_fields, f"row {row['source_row_index']}")
        if row["source_native_shape_component"] != "true":
            raise SystemExit("row must be source-native shape component")
        if row["claim_boundary"] != CLAIM_BOUNDARY:
            raise SystemExit("row claim boundary mismatch")
    if not DOC.exists() or DOC.stat().st_size == 0:
        raise SystemExit("missing source-native shape support documentation")
    print("PAPER10_DESI_SHAPE_ROW2_SOURCE_NATIVE_SHAPE_SUPPORT_SCOUT_VALIDATED")


if __name__ == "__main__":
    main()

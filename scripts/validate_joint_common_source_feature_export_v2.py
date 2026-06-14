#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_common_source_feature_export_v2.csv"
SUMMARY = ROOT / "data/derived/joint_common_source_feature_export_v2_summary.csv"
DOC = ROOT / "docs/joint_common_source_feature_export_v2.md"
CLAIM_BOUNDARY = "joint_common_source_feature_export_v2_not_scoring_not_validation"


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
    require(len(summary_rows) == 1, "summary must contain one row")
    summary = summary_rows[0]
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "wrong claim boundary")
    require(summary["observer_path_row_features_exported"] == "true", "observer features should be exported")
    require(summary["observer_path_r6_leakage_review_complete"] == "false", "R6 must remain open")
    require(summary["source_feature_export_complete_for_penalty"] == "false", "export must not authorize penalty")
    require(summary["numeric_t_joint_rescoring_allowed"] == "false", "rescoring must remain forbidden")
    require(summary["verdict"] == "COMMON_EXPORT_V2_OBSERVER_FEATURES_ADDED_KIDS_AND_R6_STILL_BLOCK", "unexpected verdict")
    observer_rows = [row for row in rows if row["channel_id"] == "observer_path_basis_low_z"]
    require(observer_rows, "observer rows missing")
    require(any(row["row_type"] == "candidate" and row["feature_status"] == "available_caveated_r5_r6_open" for row in observer_rows), "observer candidate features missing")
    require(any(row["row_type"] == "matched_control" and row["feature_status"] == "available_caveated_r5_r6_open" for row in observer_rows), "observer control features missing")
    require(any(row["channel_id"] == "desi_shape_time_readout" and row["feature_status"] == "available" for row in rows), "DESI features missing")
    require(any(row["channel_id"] == "kids_lensing_cosebis_low_mode" and row["feature_status"] == "missing" for row in rows), "KiDS missing marker missing")
    for row in rows:
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
        require(row["uses_endpoint_scores_or_residuals"] == "false", "feature export must be residual-blind")
        require(row["candidate_control_symmetric_schema"] == "true", "row schema symmetry missing")
        require(row["numeric_t_joint_rescoring_allowed"] == "false", "row rescoring must be false")
    text = DOC.read_text()
    for marker in [CLAIM_BOUNDARY, "observer features added", "R6 leakage"]:
        require(marker in text, f"doc missing marker: {marker}")
    print(
        "JOINT_COMMON_SOURCE_FEATURE_EXPORT_V2_VALIDATED "
        f"rows={summary['total_feature_rows']}"
    )


if __name__ == "__main__":
    main()

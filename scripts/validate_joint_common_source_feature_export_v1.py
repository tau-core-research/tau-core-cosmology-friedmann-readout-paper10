#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_common_source_feature_export_v1.csv"
SUMMARY = ROOT / "data/derived/joint_common_source_feature_export_v1_summary.csv"
DOC = ROOT / "docs/joint_common_source_feature_export_v1.md"
CLAIM_BOUNDARY = "joint_common_source_feature_export_not_scoring_not_validation"


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
    require(summary["candidate_control_symmetric_schema"] == "true", "schema must be symmetric")
    require(summary["source_feature_export_complete_for_penalty"] == "false", "export must not be penalty-complete yet")
    require(summary["numeric_t_joint_rescoring_allowed"] == "false", "rescoring must remain forbidden")
    require(summary["verdict"] == "COMMON_SCHEMA_BUILT_FEATURE_EXPORT_INCOMPLETE_NO_RESCORING", "unexpected verdict")
    channels = {row["channel_id"] for row in rows}
    require("desi_shape_time_readout" in channels, "DESI channel missing")
    require("observer_path_basis_low_z" in channels, "observer-path channel missing")
    require("kids_lensing_cosebis_low_mode" in channels, "KiDS missing marker missing")
    require(any(row["feature_status"] == "available" for row in rows if row["channel_id"] == "desi_shape_time_readout"), "DESI available features missing")
    require(any(row["feature_status"] == "missing" for row in rows if row["channel_id"] == "observer_path_basis_low_z"), "observer missing feature marker missing")
    require(any(row["feature_status"] == "missing" for row in rows if row["channel_id"] == "kids_lensing_cosebis_low_mode"), "KiDS missing feature marker missing")
    for row in rows:
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
        require(row["uses_endpoint_scores_or_residuals"] == "false", "feature export must be residual-blind")
        require(row["candidate_control_symmetric_schema"] == "true", "row schema symmetry missing")
        require(row["numeric_t_joint_rescoring_allowed"] == "false", "row rescoring must be false")
    text = DOC.read_text()
    for marker in [CLAIM_BOUNDARY, "common schema built", "incomplete feature export"]:
        require(marker in text, f"doc missing marker: {marker}")
    print(
        "JOINT_COMMON_SOURCE_FEATURE_EXPORT_V1_VALIDATED "
        f"rows={summary['total_feature_rows']}"
    )


if __name__ == "__main__":
    main()

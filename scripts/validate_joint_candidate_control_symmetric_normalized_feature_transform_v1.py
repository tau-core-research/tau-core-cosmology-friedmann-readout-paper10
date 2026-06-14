#!/usr/bin/env python3
from __future__ import annotations

import csv
import gzip
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_candidate_control_symmetric_normalized_feature_transform_v1.csv.gz"
SUMMARY = ROOT / "data/derived/joint_candidate_control_symmetric_normalized_feature_transform_v1_summary.csv"
DOC = ROOT / "docs/joint_candidate_control_symmetric_normalized_feature_transform_v1.md"
CLAIM_BOUNDARY = "joint_candidate_control_symmetric_normalized_feature_transform_not_scoring_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", newline="") as f:
        return list(csv.DictReader(f))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    rows = read_rows(OUT)
    summary_rows = read_rows(SUMMARY)
    require(len(summary_rows) == 1, "summary must contain one row")
    summary = summary_rows[0]
    require(len(rows) == int(summary["normalized_feature_rows"]), "row count mismatch")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    require(summary["candidate_control_symmetric_transform_built"] == "true", "transform should be built")
    require(summary["penalty_formula_defined"] == "false", "penalty formula must remain undefined")
    require(summary["penalty_computed"] == "false", "penalty must not be computed")
    require(summary["numeric_t_joint_rescoring_allowed"] == "false", "rescoring must remain forbidden")
    require(summary["endpoint_replay_allowed"] == "false", "endpoint replay must remain forbidden")
    require(summary["verdict"] == "NORMALIZED_FEATURE_TRANSFORM_BUILT_NOT_SCORING", "unexpected verdict")

    channels = set()
    row_types = set()
    max_abs_normalized = 0.0
    for row in rows:
        channels.add(row["channel_id"])
        row_types.add(row["row_type"])
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
        for key in [
            "uses_endpoint_scores_or_residuals",
            "penalty_formula_defined",
            "penalty_computed",
            "numeric_t_joint_rescoring_allowed",
            "endpoint_validation_claimed",
        ]:
            require(row[key] == "false", f"row must keep {key}=false")
        scale = float(row["normalization_scale"])
        normalized = float(row["normalized_feature_value"])
        require(scale > 0, "normalization scale must be positive")
        max_abs_normalized = max(max_abs_normalized, abs(normalized))
    require(channels == {"desi_shape_time_readout", "kids_lensing_cosebis_low_mode", "observer_path_basis_low_z"}, "unexpected channels")
    require("candidate" in row_types and "matched_control" in row_types, "candidate and matched controls required")
    require(max_abs_normalized <= 1.000000000001, f"normalized values exceed source-local unit bound: {max_abs_normalized}")

    text = DOC.read_text()
    for marker in [CLAIM_BOUNDARY, "same transform", "does not define or compute a penalty"]:
        require(marker in text, f"doc missing marker: {marker}")
    print(
        "JOINT_CANDIDATE_CONTROL_SYMMETRIC_NORMALIZED_FEATURE_TRANSFORM_V1_VALIDATED "
        f"rows={summary['normalized_feature_rows']}"
    )


if __name__ == "__main__":
    main()

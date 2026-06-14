#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_channel_local_source_normalization_rule_v1.csv"
SUMMARY = ROOT / "data/derived/joint_channel_local_source_normalization_rule_v1_summary.csv"
DOC = ROOT / "docs/joint_channel_local_source_normalization_rule_v1.md"
CLAIM_BOUNDARY = "joint_channel_local_source_normalization_rule_not_scoring_not_validation"
EXPECTED_CHANNELS = {
    "desi_shape_time_readout",
    "kids_lensing_cosebis_low_mode",
    "observer_path_basis_low_z",
}


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
    require(len(rows) == len(EXPECTED_CHANNELS), "expected one normalization row per active channel")
    require(set(row["channel_id"] for row in rows) == EXPECTED_CHANNELS, "unexpected channel set")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    require(summary["source_only_normalization_frozen"] == "true", "normalization should be frozen")
    require(summary["normalization_applied_to_scoring"] == "false", "normalization must not be applied to scoring")
    require(summary["candidate_control_symmetric_transform_built"] == "false", "transform must remain unbuilt")
    require(summary["penalty_formula_defined"] == "false", "penalty formula must remain undefined")
    require(summary["penalty_computed"] == "false", "penalty must not be computed")
    require(summary["numeric_t_joint_rescoring_allowed"] == "false", "rescoring must remain forbidden")
    require(summary["endpoint_replay_allowed"] == "false", "endpoint replay must remain forbidden")
    require(summary["verdict"] == "CHANNEL_LOCAL_SOURCE_NORMALIZATION_FROZEN_NOT_SCORING", "unexpected verdict")

    for row in rows:
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
        require(row["normalization_rule"] == "divide_by_max_abs_source_feature_with_unit_fallback", "unexpected rule")
        require(row["normalization_status"] == "FROZEN_NOT_APPLIED_TO_SCORING", "unexpected status")
        require(float(row["normalization_scale"]) > 0, "normalization scale must be positive")
        require(int(row["source_feature_count"]) > 0, "each channel needs source features")
        for key in [
            "uses_endpoint_scores_or_residuals",
            "penalty_formula_defined",
            "penalty_computed",
            "numeric_t_joint_rescoring_allowed",
            "endpoint_validation_claimed",
        ]:
            require(row[key] == "false", f"row must keep {key}=false")
        require(row["candidate_control_symmetric_transform_required_next"] == "true", "next transform flag missing")

    text = DOC.read_text()
    for marker in [CLAIM_BOUNDARY, "source-only normalization", "does not permit `T_joint`"]:
        require(marker in text, f"doc missing marker: {marker}")
    print(
        "JOINT_CHANNEL_LOCAL_SOURCE_NORMALIZATION_RULE_V1_VALIDATED "
        f"channels={summary['channel_count']}"
    )


if __name__ == "__main__":
    main()

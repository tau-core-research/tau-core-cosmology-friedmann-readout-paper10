#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_symbolic_row_level_penalty_formula_shell_v1.csv"
SUMMARY = ROOT / "data/derived/joint_symbolic_row_level_penalty_formula_shell_v1_summary.csv"
DOC = ROOT / "docs/joint_symbolic_row_level_penalty_formula_shell_v1.md"
CLAIM_BOUNDARY = "joint_symbolic_row_level_penalty_formula_shell_not_scoring_not_validation"


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
    require(len(rows) == 3, "expected exactly three formula rows")
    require(len(summary_rows) == 1, "summary must contain one row")
    summary = summary_rows[0]

    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    require(summary["formula_family"] == "source_only_normalized_quadratic_feature_energy", "unexpected formula family")
    require("z_{i,a,r,f}^2" in summary["channel_penalty_formula"], "formula should use normalized feature square")
    require(summary["lambda_status"] == "symbolic_only_not_numeric_not_fit", "lambda must remain symbolic")
    require(summary["candidate_control_same_formula_required"] == "true", "same formula required")
    require(summary["candidate_control_same_transform_required"] == "true", "same transform required")
    require(summary["candidate_control_same_block_weight_required"] == "true", "same block weight required")
    require(summary["candidate_control_same_covariance_required"] == "true", "same covariance required")
    require(summary["uses_endpoint_scores_or_residuals"] == "false", "must not use endpoint scores/residuals")
    require(summary["penalty_formula_defined"] == "true", "symbolic formula should be defined")
    require(summary["penalty_computed"] == "false", "penalty must not be computed")
    require(summary["numeric_penalty_values_written"] == "false", "numeric penalty values must not be written")
    require(summary["numeric_t_joint_rescoring_allowed"] == "false", "rescoring must remain forbidden")
    require(summary["endpoint_replay_allowed"] == "false", "endpoint replay must remain forbidden")
    require(summary["endpoint_validation_claimed"] == "false", "endpoint validation must remain false")
    require(
        summary["verdict"] == "SYMBOLIC_ROW_LEVEL_PENALTY_FORMULA_FROZEN_NOT_COMPUTED_NOT_SCORING",
        "unexpected verdict",
    )

    channels = set()
    for row in rows:
        channels.add(row["channel_id"])
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
        require(row["lambda_status"] == "symbolic_only_not_numeric_not_fit", "row lambda must remain symbolic")
        require(row["candidate_control_same_formula_required"] == "true", "row formula symmetry required")
        require(row["candidate_control_same_transform_required"] == "true", "row transform symmetry required")
        require(row["candidate_control_same_block_weight_required"] == "true", "row block-weight symmetry required")
        require(row["candidate_control_same_covariance_required"] == "true", "row covariance symmetry required")
        require(row["uses_endpoint_scores_or_residuals"] == "false", "row must not use endpoint scores/residuals")
        require(row["penalty_formula_defined"] == "true", "row formula should be defined")
        require(row["penalty_computed"] == "false", "row penalty must not be computed")
        require(row["numeric_penalty_values_written"] == "false", "row numeric penalty must not be written")
        require(row["numeric_t_joint_rescoring_allowed"] == "false", "row rescoring must remain forbidden")
        require(row["endpoint_validation_claimed"] == "false", "row endpoint validation must remain false")

    require(
        channels == {
            "desi_shape_time_readout",
            "kids_lensing_cosebis_low_mode",
            "observer_path_basis_low_z",
        },
        f"unexpected channels: {sorted(channels)}",
    )

    text = DOC.read_text()
    for marker in [
        CLAIM_BOUNDARY,
        "formula defined symbolically",
        "No numeric value is",
        "candidate/control symmetric",
    ]:
        require(marker in text, f"doc missing marker: {marker}")

    print(
        "JOINT_SYMBOLIC_ROW_LEVEL_PENALTY_FORMULA_SHELL_V1_VALIDATED "
        f"channels={len(channels)}"
    )


if __name__ == "__main__":
    main()

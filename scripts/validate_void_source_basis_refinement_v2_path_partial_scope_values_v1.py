#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALUES = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_path_partial_scope_values.csv"
SUMMARY = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_path_partial_scope_values_summary.csv"

ARTIFACT_ID = "VOID_SOURCE_BASIS_REFINEMENT_V2_PATH_PARTIAL_SCOPE_VALUES_V1"
CLAIM_BOUNDARY = "v2_path_partial_scope_values_source_only_not_endpoint"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    rows = read_rows(VALUES)
    summary = read_one(SUMMARY)
    require(rows, "partial path values are empty")
    require(summary["artifact_id"] == ARTIFACT_ID, "summary artifact mismatch")
    require(summary["status"] == "V2_PATH_PARTIAL_SCOPE_VALUES_FROZEN_NOT_ENDPOINT_READY", "bad status")
    require(summary["n_rows"] == str(len(rows)), "row count mismatch")
    require(summary["strict_path_scope_candidate_count"] == "5", "strict count mismatch")
    require(summary["caveated_path_scope_candidate_count"] == "7", "caveated count mismatch")
    require(summary["total_path_scope_candidate_count"] == "12", "candidate count mismatch")
    require(summary["full_lowz_scope_path_ready"] == "false", "full low-z W_path must remain unavailable")
    require(summary["partial_path_values_computed"] == "true", "partial values should be computed")
    require(summary["full_lowz_path_values_computed"] == "false", "full low-z values must not be computed")
    require(summary["nonzero_partial_path_value_count"] == "12", "only partial-scope candidates should be nonzero")
    require(summary["rule_status"] == "SOURCE_ONLY_TILE_PROXIMITY_CONTROL_NOT_PHYSICAL_LENSING_WEIGHT", "bad rule status")
    require(summary["endpoint_replay_allowed"] == "false", "summary must not allow endpoint replay")
    require(summary["endpoint_validation_claimed"] == "false", "summary must not claim validation")
    require(summary["contains_endpoint_scores"] == "false", "summary must not contain endpoint scores")
    require(summary["contains_distance_residuals"] == "false", "summary must not contain distance residuals")
    require(summary["contains_lensing_residuals"] == "false", "summary must not contain lensing residuals")
    require(summary["contains_fit_statistics"] == "false", "summary must not contain fit statistics")
    require(summary["verdict"] == "partial_scope_W_path_values_available_only_as_source_side_control", "unexpected verdict")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    nonzero = 0
    for row in rows:
        require(row["artifact_id"] == ARTIFACT_ID, "row artifact mismatch")
        value = float(row["W_path_source_value"])
        if row["path_scope_eligibility"] == "NOT_PATH_SCOPE_ELIGIBLE":
            require(row["W_path_value_status"] == "PATH_OFF_OUTSIDE_PARTIAL_SCOPE", "path-off status mismatch")
            require(value == 0.0, "non-eligible rows must have zero path value")
        else:
            require(
                row["W_path_value_status"] == "SOURCE_ONLY_TILE_PROXIMITY_PARTIAL_SCOPE_VALUE",
                "candidate status mismatch",
            )
            require(value > 0.0, "candidate rows must have positive source-only value")
            nonzero += 1
        require(row["full_lowz_W_path_channel"] == "false", "row must not claim full low-z W_path channel")
        require(row["endpoint_replay_allowed"] == "false", "row must not allow endpoint replay")
        require(row["endpoint_validation_claimed"] == "false", "row must not claim validation")
        require(row["contains_endpoint_scores"] == "false", "row must not contain endpoint scores")
        require(row["contains_distance_residuals"] == "false", "row must not contain distance residuals")
        require(row["contains_lensing_residuals"] == "false", "row must not contain lensing residuals")
        require(row["contains_fit_statistics"] == "false", "row must not contain fit statistics")
        require(row["uses_kids_data_vector_values"] == "false", "row must not use KiDS data vector values")
        require(row["uses_posterior_chains"] == "false", "row must not use posterior chains")
        require(row["uses_posthoc_sky_direction_selection"] == "false", "row must not use post-hoc sky selection")
        require(row["uses_posthoc_path_projection_labels"] == "false", "row must not use post-hoc path labels")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
    require(nonzero == 12, "candidate nonzero count mismatch")
    print(
        "PAPER10_V2_PATH_PARTIAL_SCOPE_VALUES_VALIDATED "
        f"candidate_rows={nonzero} full_lowz=false endpoint=false"
    )


if __name__ == "__main__":
    main()

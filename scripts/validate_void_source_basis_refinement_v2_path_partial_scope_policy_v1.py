#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_path_partial_scope_policy.csv"
SUMMARY = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_path_partial_scope_policy_summary.csv"

ARTIFACT_ID = "VOID_SOURCE_BASIS_REFINEMENT_V2_PATH_PARTIAL_SCOPE_POLICY_V1"
CLAIM_BOUNDARY = "v2_path_partial_scope_policy_not_values_not_scoring"
ALLOWED_ELIGIBILITY = {
    "STRICT_PATH_SCOPE_CANDIDATE",
    "CAVEATED_PATH_SCOPE_CANDIDATE",
    "NOT_PATH_SCOPE_ELIGIBLE",
}


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
    rows = read_rows(POLICY)
    summary = read_one(SUMMARY)
    require(rows, "partial scope policy is empty")
    require(summary["artifact_id"] == ARTIFACT_ID, "summary artifact mismatch")
    require(summary["status"] == "V2_PATH_PARTIAL_SCOPE_POLICY_FROZEN_VALUES_NOT_COMPUTED", "bad status")
    require(summary["n_rows"] == str(len(rows)), "row count mismatch")
    strict_count = sum(row["path_scope_eligibility"] == "STRICT_PATH_SCOPE_CANDIDATE" for row in rows)
    caveated_count = sum(row["path_scope_eligibility"] == "CAVEATED_PATH_SCOPE_CANDIDATE" for row in rows)
    require(summary["strict_path_scope_candidate_count"] == str(strict_count), "strict count mismatch")
    require(summary["caveated_path_scope_candidate_count"] == str(caveated_count), "caveated count mismatch")
    require(summary["total_path_scope_candidate_count"] == str(strict_count + caveated_count), "total count mismatch")
    require(strict_count > 0, "expected at least one strict path-scope candidate")
    require(caveated_count > 0, "expected at least one caveated path-scope candidate")
    require(summary["full_lowz_scope_path_ready"] == "false", "full low-z path scope must remain unavailable")
    require(summary["path_values_computed"] == "false", "partial scope policy must not compute W_path values")
    require(summary["endpoint_replay_allowed"] == "false", "summary must not allow endpoint replay")
    require(summary["endpoint_validation_claimed"] == "false", "summary must not claim validation")
    require(summary["contains_endpoint_scores"] == "false", "summary must not contain endpoint scores")
    require(summary["contains_distance_residuals"] == "false", "summary must not contain distance residuals")
    require(summary["contains_lensing_residuals"] == "false", "summary must not contain lensing residuals")
    require(summary["contains_fit_statistics"] == "false", "summary must not contain fit statistics")
    require(summary["verdict"] == "W_path_is_partial_scope_candidate_only_not_full_lowz_channel", "unexpected verdict")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    for row in rows:
        require(row["artifact_id"] == ARTIFACT_ID, "row artifact mismatch")
        require(row["path_scope_eligibility"] in ALLOWED_ELIGIBILITY, "bad eligibility label")
        require(row["W_path_value_status"] == "NOT_COMPUTED_PARTIAL_SCOPE_POLICY_ONLY", "row must not compute W_path")
        require(row["W_path_source_value"] == "NA", "row W_path value must remain NA")
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
    print(
        "PAPER10_V2_PATH_PARTIAL_SCOPE_POLICY_VALIDATED "
        f"strict={strict_count} caveated={caveated_count} path_values_computed=false"
    )


if __name__ == "__main__":
    main()

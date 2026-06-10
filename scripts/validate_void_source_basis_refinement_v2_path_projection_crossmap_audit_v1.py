#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_path_projection_crossmap_audit.csv"
SUMMARY = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_path_projection_crossmap_audit_summary.csv"

ARTIFACT_ID = "VOID_SOURCE_BASIS_REFINEMENT_V2_PATH_PROJECTION_CROSSMAP_AUDIT_V1"
CLAIM_BOUNDARY = "v2_path_projection_crossmap_audit_not_values_not_scoring"


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
    rows = read_rows(AUDIT)
    summary = read_one(SUMMARY)
    require(rows, "crossmap audit is empty")
    require(summary["artifact_id"] == ARTIFACT_ID, "summary artifact mismatch")
    require(summary["status"] == "V2_PATH_PROJECTION_CROSSMAP_AUDIT_BUILT_VALUES_NOT_COMPUTED", "bad status")
    require(summary["n_rows"] == str(len(rows)), "row count mismatch")
    require(summary["lowz_ra_dec_available"] == "true", "low-z RA/DEC should be available")
    require(summary["kids_tile_coordinate_inventory_available"] == "true", "KiDS tile inventory should be available")
    require(summary["path_values_computed"] == "false", "crossmap audit must not compute W_path values")
    require(summary["endpoint_replay_allowed"] == "false", "summary must not allow endpoint replay")
    require(summary["endpoint_validation_claimed"] == "false", "summary must not claim validation")
    require(summary["contains_endpoint_scores"] == "false", "summary must not contain endpoint scores")
    require(summary["contains_distance_residuals"] == "false", "summary must not contain distance residuals")
    require(summary["contains_lensing_residuals"] == "false", "summary must not contain lensing residuals")
    require(summary["contains_fit_statistics"] == "false", "summary must not contain fit statistics")
    require(summary["verdict"] == "lowz_coordinates_available_but_path_values_not_computed", "unexpected verdict")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    n_1deg = int(summary["rows_nearest_tile_within_1_deg"])
    n_2deg = int(summary["rows_nearest_tile_within_2_deg"])
    require((n_1deg > 0 or n_2deg > 0) == (summary["crossmap_candidate_available"] == "true"), "candidate flag mismatch")
    require(summary["crossmap_complete_for_lowz_scope"] == "false", "crossmap should not be complete for low-z scope")
    for row in rows:
        require(row["artifact_id"] == ARTIFACT_ID, "row artifact mismatch")
        require(row["kids_tile_inventory_available"] == "true", "row should see KiDS tile inventory")
        require(row["W_path_value_status"] == "NOT_COMPUTED_CROSSMAP_AUDIT_ONLY", "row must not compute W_path")
        require(row["W_path_source_value"] == "NA", "row W_path source value must remain NA")
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
        "PAPER10_V2_PATH_PROJECTION_CROSSMAP_AUDIT_VALIDATED "
        f"rows={len(rows)} path_values_computed=false"
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_path_projection_route_ledger.csv"
SUMMARY = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_path_projection_route_ledger_summary.csv"

COMPONENT_ID = "V2_OBSERVER_PATH_PROJECTION"
CLAIM_BOUNDARY = "v2_path_projection_route_ledger_not_scoring_not_validation"


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
    rows = read_rows(LEDGER)
    summary = read_one(SUMMARY)
    require(rows, "path route ledger is empty")
    require(summary["component_id"] == COMPONENT_ID, "summary component mismatch")
    require(summary["status"] == "V2_PATH_PROJECTION_ROUTE_LEDGER_FROZEN_VALUES_BLOCKED", "bad summary status")
    require(summary["n_rows"] == str(len(rows)), "row count mismatch")
    require(summary["kids_lensing_route_available"] == "true", "KiDS route should be available")
    require(summary["pantheon_lowz_ra_dec_available"] == "false", "low-z Pantheon RA/DEC should remain unavailable")
    require(summary["lowz_to_kids_path_crossmap_available"] == "false", "low-z to KiDS crossmap should remain unavailable")
    require(summary["path_values_computed"] == "false", "path values must not be computed")
    require(summary["endpoint_replay_allowed"] == "false", "summary must not allow endpoint replay")
    require(summary["endpoint_validation_claimed"] == "false", "summary must not claim endpoint validation")
    require(summary["contains_endpoint_scores"] == "false", "summary must not contain endpoint scores")
    require(summary["contains_distance_residuals"] == "false", "summary must not contain distance residuals")
    require(summary["contains_lensing_residuals"] == "false", "summary must not contain lensing residuals")
    require(summary["contains_fit_statistics"] == "false", "summary must not contain fit statistics")
    require(summary["uses_kids_data_vector_values"] == "false", "summary must not use KiDS data vector values")
    require(summary["uses_posterior_chains"] == "false", "summary must not use posterior chains")
    require(summary["verdict"] == "path_route_available_but_lowz_coordinate_crossmap_missing", "unexpected verdict")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")

    for row in rows:
        require(row["component_id"] == COMPONENT_ID, "row component mismatch")
        require(row["channel_id"] == "W_PATH_PROJECTION", "row channel mismatch")
        require(row["kids_lensing_route_available"] == "true", "row route availability mismatch")
        require(row["pantheon_lowz_ra_dec_available"] == "false", "row must not claim RA/DEC")
        require(row["lowz_to_kids_path_crossmap_available"] == "false", "row must not claim crossmap")
        require(row["W_path_value_status"] == "BLOCKED_SOURCE_COORDINATE_JOIN_REQUIRED", "path value status mismatch")
        require(row["W_path_source_value"] == "NA", "path source value must remain NA")
        require(row["path_off_control"] == "0", "path off control must be zero")
        require(row["endpoint_replay_allowed"] == "false", "rows must not allow endpoint replay")
        require(row["endpoint_validation_claimed"] == "false", "rows must not claim endpoint validation")
        require(row["contains_endpoint_scores"] == "false", "rows must not contain endpoint scores")
        require(row["contains_distance_residuals"] == "false", "rows must not contain distance residuals")
        require(row["contains_lensing_residuals"] == "false", "rows must not contain lensing residuals")
        require(row["contains_fit_statistics"] == "false", "rows must not contain fit statistics")
        require(row["uses_kids_data_vector_values"] == "false", "rows must not use KiDS data vector values")
        require(row["uses_posterior_chains"] == "false", "rows must not use posterior chains")
        require(row["uses_posthoc_sky_direction_selection"] == "false", "rows must not use posthoc sky selection")
        require(row["uses_posthoc_path_projection_labels"] == "false", "rows must not use posthoc path labels")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
    print(
        "PAPER10_V2_PATH_PROJECTION_ROUTE_LEDGER_VALIDATED "
        f"rows={len(rows)} path_values_computed=false"
    )


if __name__ == "__main__":
    main()

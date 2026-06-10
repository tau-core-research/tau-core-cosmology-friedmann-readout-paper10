#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALUES = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_cmb_safety_values.csv"
SUMMARY = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_cmb_safety_values_summary.csv"

COMPONENT_ID = "V2_CMB_SAFETY"
CLAIM_BOUNDARY = "v2_cmb_safety_source_values_frozen_not_scoring_not_validation"


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
    require(rows, "CMB safety values table is empty")
    require(summary["component_id"] == COMPONENT_ID, "summary component mismatch")
    require(summary["status"] == "V2_CMB_SAFETY_VALUES_FROZEN_NOT_ENDPOINT_READY", "bad summary status")
    require(summary["n_rows"] == str(len(rows)), "summary row count mismatch")
    require(summary["cmb_lowz_support_passed"] == "true", "CMB low-z support must pass")
    require(summary["rows_below_safety_floor"] == str(len(rows)), "all low-z rows should be below safety floor")
    require(summary["endpoint_replay_allowed"] == "false", "summary must not allow endpoint replay")
    require(summary["endpoint_validation_claimed"] == "false", "summary must not claim endpoint validation")
    require(summary["contains_endpoint_scores"] == "false", "summary must not contain endpoint scores")
    require(summary["contains_distance_residuals"] == "false", "summary must not contain distance residuals")
    require(summary["contains_fit_statistics"] == "false", "summary must not contain fit statistics")
    require(summary["contains_cmb_map_data"] == "false", "summary must not contain CMB map data")
    require(summary["contains_cmb_likelihood"] == "false", "summary must not contain CMB likelihood")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    z_floor = float(summary["z_safety_floor"])
    z_recombination = float(summary["z_recombination_proxy"])
    require(z_floor > 0.0, "safety floor must be positive")
    require(z_recombination > z_floor, "recombination proxy must exceed safety floor")

    for row in rows:
        require(row["component_id"] == COMPONENT_ID, "row component mismatch")
        require(row["channel_id"] == "W_PATH_PROJECTION;W_TIME_READOUT", "row channel mismatch")
        require(float(row["zHD"]) < z_floor, "row is not below CMB safety floor")
        require(row["low_z_below_safety_floor"] == "true", "low-z safety flag mismatch")
        require(row["cmb_lowz_support_passed"] == "true", "CMB support flag mismatch")
        require(row["cmb_map_data_used"] == "false", "row must not use CMB map data")
        require(row["cmb_likelihood_used"] == "false", "row must not use CMB likelihood")
        require(row["cmb_safety_off_control"] == "0", "off control must be zero")
        require(row["cmb_wrong_prior_control"] == "1", "wrong-prior control must be marker one")
        require(row["endpoint_replay_allowed"] == "false", "rows must not allow endpoint replay")
        require(row["endpoint_validation_claimed"] == "false", "rows must not claim endpoint validation")
        require(row["contains_endpoint_scores"] == "false", "rows must not contain endpoint scores")
        require(row["contains_distance_residuals"] == "false", "rows must not contain distance residuals")
        require(row["contains_fit_statistics"] == "false", "rows must not contain fit statistics")
        require(row["contains_cmb_map_data"] == "false", "rows must not contain CMB map data")
        require(row["contains_cmb_likelihood"] == "false", "rows must not contain CMB likelihood")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")

    require(
        summary["verdict"] == "cmb_safety_values_frozen_not_endpoint_ready",
        "unexpected CMB safety verdict",
    )
    print(
        "PAPER10_V2_CMB_SAFETY_VALUES_VALIDATED "
        f"rows={len(rows)} endpoint_replay_allowed=false"
    )


if __name__ == "__main__":
    main()

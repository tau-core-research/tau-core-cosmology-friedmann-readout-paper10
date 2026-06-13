#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "data/source_manifest/paper10_desi_shape_route_replay_run_template_v1.csv"
SHAPE_SUMMARY = ROOT / "data/derived/paper10_desi_time_readout_shape_observable_gate_v1_summary.csv"
PROJECTION_SUMMARY = ROOT / "data/derived/paper10_desi_time_readout_shape_projection_induction_v1_summary.csv"
CONTROL_SUMMARY = ROOT / "data/derived/paper10_desi_shape_bound_control_vectors_v1_summary.csv"
CC_WINDOW_SUMMARY = ROOT / "data/derived/paper10_desi_cc_window_stress_binding_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_shape_route_replay_template_not_validation"
EXPECTED_CONTROLS = {
    "redshift_order_shuffle",
    "leave_row_or_pair",
    "cc_window_stress",
    "wrong_time_basis",
    "rd_prior_stress",
}
EXPECTED_FORBIDDEN = {
    "endpoint_scores_before_authorization",
    "fit_statistics_before_authorization",
    "posthoc_shape_selection",
    "posthoc_row_selection",
    "posthoc_control_selection",
    "posthoc_cc_window_selection",
    "posthoc_high_z_policy_change",
    "posthoc_cc_extrapolation",
    "posthoc_hz_smoothing",
    "posthoc_beta_retuning",
    "Pantheon_distance_residuals",
    "late_time_fit_parameter_selection",
    "physical_validation_claims",
}


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    row = read_one(TEMPLATE)
    shape = read_one(SHAPE_SUMMARY)
    projection = read_one(PROJECTION_SUMMARY)
    controls = read_one(CONTROL_SUMMARY)
    cc_window = read_one(CC_WINDOW_SUMMARY)
    require(row["status"] == "DESI_SHAPE_ROUTE_REPLAY_PREPARED_AUTH_REQUIRED_NOT_VALIDATION", "bad status")
    require(row["active_route_family"] == "DESI_CC_MATCHED_RADIAL_BAO_TIME_SHAPE", "bad route family")
    require(row["endpoint_scope"] == "first_CC_matched_DESI_5row_shape_scope", "bad endpoint scope")
    require(row["shape_rows_allowed"] == "0;1;2;3", "bad shape-row scope")
    require(row["curvature_rows_available"] == "0;1;2", "bad curvature-row scope")
    require(row["radial_rows_allowed"] == "0;1;2;3;4", "bad radial-row scope")
    require(row["radial_rows_excluded"] == "5", "high-z holdout must remain excluded")
    require(set(row["control_families"].split(";")) == EXPECTED_CONTROLS, "control family set mismatch")
    require(set(row["forbidden_inputs"].split(";")) == EXPECTED_FORBIDDEN, "forbidden input set mismatch")
    require(row["endpoint_replay_allowed"] == "false", "template must not authorize replay")
    require(row["endpoint_validation_claimed"] == "false", "template must not claim validation")
    require(row["physical_validation_claimed"] == "false", "template must not claim physical validation")
    require(row["claim_boundary"] == CLAIM_BOUNDARY, "claim boundary mismatch")
    require(shape["shape_observable_candidate_available"] == "true", "shape candidate must be available")
    require(shape["first_difference_rows"] == "4", "first-difference row count mismatch")
    require(shape["second_difference_rows"] == "3", "curvature row count mismatch")
    require(shape["high_z_row_included"] == "false", "shape route must exclude high-z row")
    require(projection["primary_candidate"] == "CLOCK_SLOPE_SHAPE", "primary candidate mismatch")
    require(projection["projection_induction_complete"] == "false", "projection induction should remain incomplete")
    require(controls["shape_bound_control_count"] == "5", "controls must be shape-bound")
    require(controls["unbound_control_families"] == "none", "unbound control family remains")
    require(controls["ordering_control_suite_ready_for_replay"] == "false", "template should not mark controls replay-ready")
    require(cc_window["cc_window_stress_release_policy"] == "SOURCE_REOPEN_ONLY_NO_REPLAY", "CC-window policy changed")
    print("PAPER10_DESI_SHAPE_ROUTE_REPLAY_RUN_TEMPLATE_VALIDATED status=auth_required_not_replay")


if __name__ == "__main__":
    main()

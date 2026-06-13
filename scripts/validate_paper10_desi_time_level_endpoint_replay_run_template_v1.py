#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "data/source_manifest/paper10_desi_time_level_endpoint_replay_run_template_v1.csv"
READINESS = ROOT / "data/derived/paper10_time_level_route_external_rd_readiness_gate_v1_summary.csv"
CONTROL_SEEDS = ROOT / "data/derived/paper10_desi_time_level_control_seed_manifest_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_time_level_endpoint_replay_template_not_validation"
EXPECTED_CONTROLS = {
    "rd_off_control",
    "external_prior_width_stress",
    "wrong_prior_control",
    "BAO_pair_drop_control",
    "CC_match_window_stress",
    "level_slope_swap_control",
    "redshift_order_shuffle_control",
}
EXPECTED_FORBIDDEN = {
    "endpoint_scores_before_authorization",
    "fit_statistics_before_authorization",
    "posthoc_row_selection",
    "posthoc_control_selection",
    "posthoc_seed_selection",
    "posthoc_high_z_policy_change",
    "posthoc_cc_extrapolation",
    "posthoc_hz_smoothing",
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
    readiness = read_one(READINESS)
    seeds = read_one(CONTROL_SEEDS)
    require(row["status"] == "DESI_TIME_LEVEL_ENDPOINT_REPLAY_PREPARED_AUTH_REQUIRED_NOT_VALIDATION", "bad status")
    require(row["active_route_family"] == "DESI_CC_MATCHED_RADIAL_BAO_TIME_LEVEL", "bad route family")
    require(row["endpoint_scope"] == "first_CC_matched_DESI_5row_scope", "bad endpoint scope")
    require(row["radial_rows_allowed"] == "0;1;2;3;4", "bad allowed radial rows")
    require(row["radial_rows_excluded"] == "5", "bad excluded radial rows")
    require(set(row["control_branches"].split(";")) == EXPECTED_CONTROLS, "control family set mismatch")
    require(set(row["forbidden_inputs"].split(";")) == EXPECTED_FORBIDDEN, "forbidden input set mismatch")
    require(row["endpoint_replay_allowed"] == "false", "template must not authorize replay")
    require(row["endpoint_validation_claimed"] == "false", "template must not claim validation")
    require(row["physical_validation_claimed"] == "false", "template must not claim physical validation")
    require(row["claim_boundary"] == CLAIM_BOUNDARY, "claim boundary mismatch")
    require(
        readiness["verdict"] == "desi_time_cc_matched_scope_and_controls_frozen_but_endpoint_authorization_missing",
        "readiness gate must still require endpoint authorization",
    )
    require(readiness["desi_dr2_first_cc_matched_endpoint_rows"] == "5", "readiness row count mismatch")
    require(seeds["control_family_count"] == "7", "control seed count mismatch")
    require(seeds["deterministic_seed_min"] == "41001", "control seed min mismatch")
    require(seeds["deterministic_seed_max"] == "41007", "control seed max mismatch")
    print(
        "PAPER10_DESI_TIME_LEVEL_ENDPOINT_REPLAY_RUN_TEMPLATE_VALIDATED "
        "status=auth_required_not_replay"
    )


if __name__ == "__main__":
    main()

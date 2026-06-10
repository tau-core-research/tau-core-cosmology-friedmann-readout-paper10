#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "data" / "source_manifest" / "low_z_pantheon_void_replay_protocol_v1.csv"
SCOPE = ROOT / "data" / "derived" / "low_z_pantheon_void_scope_candidate_v1_summary.csv"
PACKAGE = ROOT / "data" / "derived" / "low_z_pantheon_void_scope_replay_authorization_review_package_v1_summary.csv"

FORBIDDEN_SCORE_ARTIFACTS = [
    ROOT / "data" / "derived" / "low_z_pantheon_void_replay_v1_results.csv",
    ROOT / "data" / "derived" / "low_z_pantheon_void_replay_v1_residuals.csv",
    ROOT / "data" / "derived" / "low_z_pantheon_void_replay_v1_grid.csv",
    ROOT / "data" / "derived" / "low_z_pantheon_void_replay_v1_summary.csv",
]


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    protocol = read_one(PROTOCOL)
    scope = read_one(SCOPE)
    package = read_one(PACKAGE)

    require(protocol["status"] == "LOW_Z_VOID_REPLAY_PROTOCOL_FROZEN_NOT_RUN", "protocol status mismatch")
    require(protocol["scoring_allowed"] == "false", "protocol must keep scoring_allowed=false")
    require(protocol["physical_validation_claimed"] == "false", "protocol must not claim physical validation")
    require(protocol["parent_scope_candidate"] == scope["scope_id"], "parent scope mismatch")
    require(protocol["parent_authorization_package"] == package["package_id"], "authorization package mismatch")
    require(scope["scope_status"] == "SCOPE_CANDIDATE_FROZEN_NOT_ENDPOINT", "scope must be frozen candidate")
    require(scope["candidate_endpoint_run_allowed_now"] == "false", "scope must not pre-authorize endpoint")
    require(package["endpoint_run_allowed"] == "false", "authorization package must not pre-authorize replay")

    require(protocol["observable_blocks"] == "Pantheon_distance_low_z_void_supported_subset", "unexpected block")
    require(protocol["included_channel_families"] == "W_VOID_MATURITY", "only void channel should be active")
    for channel in ["W_WEB_ANISOTROPY", "W_PATH_PROJECTION", "W_TIME_READOUT"]:
        require(channel in protocol["disabled_channel_families"], f"disabled channel missing: {channel}")
    for marker in ["AIC_lowz", "chi2_lowz_distance", "k_shared"]:
        require(marker in protocol["information_criterion_shell"], f"criterion missing: {marker}")
    for marker in [
        "baseline_only",
        "void_only",
        "wrong_void_sign",
        "wrong_void_threshold",
        "deterministic_shuffled_void_within_low_z_mask",
        "zero_void_amplitude",
    ]:
        require(marker in protocol["null_controls"], f"control missing: {marker}")
    for marker in [
        "low-z AIC improves",
        "survives wrong/shuffled controls",
        "no endpoint leakage fields",
    ]:
        require(marker in protocol["pass_condition_shell"], f"pass condition missing: {marker}")
    for marker in [
        "distance_residual_driven_activation",
        "fit_improvement_driven_row_selection",
        "posthoc_row_selection",
        "posthoc_void_thresholds",
        "posthoc_amplitude_tuning",
        "posthoc_covariance_reweighting",
        "endpoint_score_claims",
        "physical_validation_claims",
    ]:
        require(marker in protocol["forbidden_inputs"], f"forbidden marker missing: {marker}")
    existing_forbidden = [str(path.relative_to(ROOT)) for path in FORBIDDEN_SCORE_ARTIFACTS if path.exists()]
    require(not existing_forbidden, "low-z protocol cannot coexist with score artifacts: " + ",".join(existing_forbidden))

    print(
        "PAPER10_LOW_Z_PANTHEON_VOID_REPLAY_PROTOCOL_V1_VALIDATED "
        "scoring_allowed=false"
    )


if __name__ == "__main__":
    main()

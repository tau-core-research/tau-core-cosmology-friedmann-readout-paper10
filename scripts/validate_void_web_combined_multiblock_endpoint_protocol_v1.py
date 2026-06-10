#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "data" / "source_manifest" / "void_web_combined_multiblock_endpoint_protocol_v1.csv"
READINESS = ROOT / "data" / "derived" / "void_web_endpoint_readiness_after_flrw_audit_v1_summary.csv"

FORBIDDEN_SCORE_ARTIFACTS = [
    ROOT / "data" / "derived" / "void_web_combined_multiblock_endpoint_v1_results.csv",
    ROOT / "data" / "derived" / "void_web_combined_multiblock_endpoint_v1_residuals.csv",
    ROOT / "data" / "derived" / "void_web_combined_multiblock_endpoint_v1_grid.csv",
    ROOT / "data" / "derived" / "void_web_combined_multiblock_endpoint_v1_summary.csv",
]


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def main() -> None:
    protocol = read_one(PROTOCOL)
    readiness = read_one(READINESS)

    if protocol["status"] != "COMBINED_MULTIBLOCK_ENDPOINT_PROTOCOL_FROZEN_NOT_RUN":
        raise SystemExit("combined protocol must remain frozen-not-run")
    if protocol["scoring_allowed"] != "false":
        raise SystemExit("combined protocol must keep scoring_allowed=false")
    if protocol["physical_validation_claimed"] != "false":
        raise SystemExit("combined protocol must not claim physical validation")
    if protocol["parent_readiness_policy"] != readiness["policy_id"]:
        raise SystemExit("combined protocol parent readiness mismatch")
    if readiness["endpoint_ready_count"] != "0":
        raise SystemExit("parent readiness ledger should not declare endpoint-ready components")
    if readiness["endpoint_scoring_allowed"] != "false":
        raise SystemExit("parent readiness ledger must keep endpoint scoring disabled")
    if "combined_multiblock_endpoint_protocol" not in readiness["next_required_gate"]:
        raise SystemExit("parent readiness ledger must call for the combined multiblock protocol")

    for marker in [
        "Pantheon_distance_full_cov",
        "SDSS_growth_summary",
        "SDSS_multitracer_BAO_RSD_full_cov",
        "CMB_lowz_safety_support",
    ]:
        if marker not in protocol["observable_blocks"]:
            raise SystemExit(f"observable block missing: {marker}")
    for channel in ["W_VOID_MATURITY", "W_WEB_ANISOTROPY"]:
        if channel not in protocol["included_channel_families"]:
            raise SystemExit(f"included channel missing: {channel}")
    for channel in ["W_PATH_PROJECTION", "W_TIME_READOUT"]:
        if channel not in protocol["disabled_channel_families"]:
            raise SystemExit(f"disabled channel missing: {channel}")
    for marker in [
        "AIC_total",
        "chi2_distance",
        "chi2_growth",
        "chi2_multitracer",
        "k_shared",
    ]:
        if marker not in protocol["unified_information_criterion"]:
            raise SystemExit(f"unified information criterion missing: {marker}")
    for marker in [
        "baseline_only",
        "source_native_void_web",
        "wrong_web_sign",
        "wrong_void_threshold",
        "deterministic_shuffled_void_web",
        "block_drop_distance",
        "block_drop_growth",
        "block_drop_multitracer",
        "CMB_safety_off_control",
    ]:
        if marker not in protocol["joint_null_controls"]:
            raise SystemExit(f"joint null/control missing: {marker}")
    for marker in [
        "unified AIC improves",
        "survives joint shuffled/wrong controls",
        "stable under block-drop controls",
        "preserves CMB-safety support",
        "no endpoint leakage fields",
    ]:
        if marker not in protocol["pass_condition_shell"]:
            raise SystemExit(f"pass-condition shell missing: {marker}")
    for marker in [
        "distance_residual_driven_activation",
        "growth_residual_driven_activation",
        "fit_improvement_driven_channel_selection",
        "posthoc_void_thresholds",
        "posthoc_environment_labels",
        "posthoc_block_weights",
        "posthoc_covariance_reweighting",
        "endpoint_score_claims",
    ]:
        if marker not in protocol["forbidden_inputs"]:
            raise SystemExit(f"forbidden input marker missing: {marker}")
    existing_forbidden = [
        str(path.relative_to(ROOT))
        for path in FORBIDDEN_SCORE_ARTIFACTS
        if path.exists()
    ]
    if existing_forbidden:
        raise SystemExit(
            "combined protocol freeze cannot coexist with score artifacts: "
            + ",".join(existing_forbidden)
        )

    print(
        "PAPER10_VOID_WEB_COMBINED_MULTIBLOCK_ENDPOINT_PROTOCOL_V1_VALIDATED "
        "scoring_allowed=false"
    )


if __name__ == "__main__":
    main()

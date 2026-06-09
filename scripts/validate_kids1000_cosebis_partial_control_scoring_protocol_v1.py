#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "data" / "source_manifest" / "kids1000_cosebis_partial_control_scoring_protocol_v1.csv"
F_OVERLAP_DECISION = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_resolution_decision_v1_summary.csv"
JOIN_CONTRACT = ROOT / "data" / "derived" / "kids1000_cosebis_mapping_template_join_contract_v1_summary.csv"

FORBIDDEN_PARTIAL_SCORE_ARTIFACTS = [
    ROOT / "data" / "derived" / "kids1000_cosebis_partial_control_scoring_v1_results.csv",
    ROOT / "data" / "derived" / "kids1000_cosebis_partial_control_scoring_v1_residuals.csv",
    ROOT / "data" / "derived" / "kids1000_cosebis_partial_control_scoring_v1_grid.csv",
    ROOT / "data" / "derived" / "kids1000_cosebis_partial_control_scoring_v1_null_controls.csv",
    ROOT / "data" / "derived" / "kids1000_cosebis_partial_control_scoring_v1_summary.csv",
]


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def main() -> None:
    protocol = read_one(PROTOCOL)
    f_overlap = read_one(F_OVERLAP_DECISION)
    join_contract = read_one(JOIN_CONTRACT)

    if protocol["status"] != "PARTIAL_CONTROL_SCORING_PROTOCOL_FROZEN_NOT_RUN":
        raise SystemExit("partial-control scoring protocol must remain frozen-not-run")
    if protocol["partial_control_scoring_allowed"] != "false":
        raise SystemExit("partial-control scoring protocol must keep scoring disabled")
    if protocol["endpoint_scoring_allowed"] != "false":
        raise SystemExit("partial-control protocol must not enable endpoint scoring")
    if protocol["parent_f_overlap_decision_policy"] != f_overlap["policy_id"]:
        raise SystemExit("partial-control protocol parent F_overlap decision mismatch")
    if protocol["parent_join_contract_policy"] != join_contract["policy_id"]:
        raise SystemExit("partial-control protocol parent join contract mismatch")
    if f_overlap["f_overlap_endpoint_ready"] != "true":
        raise SystemExit("partial-control protocol now expects endpoint-route F_overlap source support")
    if f_overlap["endpoint_scoring_allowed"] != "false":
        raise SystemExit("partial-control protocol must not inherit endpoint scoring permission")
    if f_overlap["f_overlap_control_ready"] != "true":
        raise SystemExit("partial-control protocol requires caveated F_overlap control readiness")
    if f_overlap["accepted_control_scope"] != protocol["control_scope"]:
        raise SystemExit("partial-control scope mismatch")
    if join_contract["join_values_computed"] != "false":
        raise SystemExit("join contract must not contain join values")
    if join_contract["mapping_vector_computed"] != "false":
        raise SystemExit("join contract must not contain a mapping vector")
    if join_contract["theory_values_computed"] != "false":
        raise SystemExit("join contract must not contain theory values")
    if "diagnostic_chi2_shell_only" not in protocol["primary_score_shell"]:
        raise SystemExit("partial-control protocol must declare only a diagnostic chi-square shell")
    for marker in [
        "partial_control_baseline",
        "partial_control_candidate",
        "wrong_channel_controls",
        "fixed_seed_sign_flip_controls",
        "control_rank_only",
    ]:
        if marker not in protocol["allowed_comparison_outputs"]:
            raise SystemExit(f"missing comparison output marker: {marker}")
    for marker in [
        "F_overlap endpoint route rejected",
        "F_overlap partial control accepted",
        "partial mapping vector source-frozen",
        "null controls declared",
        "no endpoint leakage flags",
    ]:
        if marker not in protocol["minimum_preconditions"]:
            raise SystemExit(f"missing minimum precondition marker: {marker}")
    for marker in [
        "kids_data_vector_values_for_source_selection",
        "posterior_chains",
        "fit_improvement_flags",
        "lensing_residuals",
        "posthoc_channel_activation",
        "posthoc_mode_cuts",
        "posthoc_tomographic_selection",
        "posthoc_sky_direction_selection",
        "posthoc_web_environment_labels",
        "posthoc_path_projection_labels",
        "posthoc_weight_selection",
        "posthoc_mask_subset_selection",
    ]:
        if marker not in protocol["forbidden_inputs"]:
            raise SystemExit(f"forbidden input marker missing: {marker}")
    existing_forbidden = [
        str(path.relative_to(ROOT)) for path in FORBIDDEN_PARTIAL_SCORE_ARTIFACTS if path.exists()
    ]
    if existing_forbidden:
        raise SystemExit(
            "partial-control scoring protocol freeze cannot coexist with score artifacts: "
            + ",".join(existing_forbidden)
        )
    print("PAPER10_KIDS1000_COSEBIS_PARTIAL_CONTROL_SCORING_PROTOCOL_V1_VALIDATED scoring_allowed=false")


if __name__ == "__main__":
    main()

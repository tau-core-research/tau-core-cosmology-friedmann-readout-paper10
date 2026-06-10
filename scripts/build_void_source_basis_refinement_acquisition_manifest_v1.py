#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "void_source_basis_refinement_acquisition_manifest_policy_v1.csv"
GATE = ROOT / "data" / "derived" / "void_source_basis_refinement_gate_v1.csv"
OUT = ROOT / "data" / "derived" / "void_source_basis_refinement_acquisition_manifest_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "void_source_basis_refinement_acquisition_manifest_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    policy = read_one(POLICY)
    gate = read_one(GATE)

    if policy["status"] != "VOID_SOURCE_BASIS_REFINEMENT_ACQUISITION_MANIFEST_FROZEN_NOT_ATTACHED":
        raise SystemExit("unexpected acquisition-manifest policy status")
    if policy["current_endpoint_replay_allowed"] != "false":
        raise SystemExit("acquisition manifest must not authorize endpoint replay")
    if gate["source_unique_ready"] != "false":
        raise SystemExit("refinement acquisition expects current basis to remain not source-unique-ready")
    if gate["next_allowed_artifact"] != "void_source_basis_refinement_acquisition_manifest_v1":
        raise SystemExit("parent gate does not allow this artifact")
    if gate["endpoint_scoring_allowed"] != "false" or gate["physical_validation_claimed"] != "false":
        raise SystemExit("parent gate must not allow scoring or validation")

    rows = [
        {
            "policy_id": policy["policy_id"],
            "route_id": "R1_void_catalogue_object_properties",
            "required_evidence": "attach_source_native_void_catalogue_with_object_level_radius_depth_center_redshift_and_boundary_fields",
            "accepted_source_types": "published_void_catalogue_table;official_survey_void_catalogue_release;machine_readable_catalogue_with_documented_selection_function",
            "candidate_source_hint": "void catalogue must expose radius/depth/center/boundary information rather than only redshift support",
            "required_features": "void_depth;void_radius;void_center;void_boundary_or_membership;catalogue_selection_function",
            "current_status": "TO_ATTACH",
            "closure_role": "needed_to_replace_redshift_like_W_void_with_object_level_void_morphology",
            "forbidden_inputs_used": "false",
            "endpoint_replay_allowed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "route_id": "R2_supernova_host_to_void_geometry",
            "required_evidence": "attach_residual_blind_join_between_low_z_pantheon_hosts_and_void_catalogue_geometry",
            "accepted_source_types": "host_coordinate_catalogue;crossmatch_table;published_host_assignment;scripted_sky_redshift_join_with_frozen_radius_rule",
            "candidate_source_hint": "derive host-to-void position, wall distance, and membership before any replay score",
            "required_features": "host_to_void_position;wall_distance;void_membership_or_nearest_void_id;line_of_sight_relative_position",
            "current_status": "TO_ATTACH",
            "closure_role": "needed_to_separate_void_environment_from_redshift_ordering",
            "forbidden_inputs_used": "false",
            "endpoint_replay_allowed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "route_id": "R3_line_of_sight_environment",
            "required_evidence": "attach_source_side_line_of_sight_density_or_environment_proxy_independent_of_distance_residuals",
            "accepted_source_types": "galaxy_density_field;group_cluster_catalogue;line_of_sight_environment_table;survey_mask_selection_function",
            "candidate_source_hint": "line-of-sight environment must be computed from source catalogues, not from Pantheon residuals",
            "required_features": "line_of_sight_environment;foreground_background_density;survey_mask_or_selection_function",
            "current_status": "TO_ATTACH",
            "closure_role": "needed_to_distinguish_void_maturity_from_path_environment",
            "forbidden_inputs_used": "false",
            "endpoint_replay_allowed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "route_id": "R4_redshift_degeneracy_independence_preflight",
            "required_evidence": "compute_source_side_independence_report_before_scoring",
            "accepted_source_types": "preflight_csv;scripted_correlation_report;reviewed_no_residual_leakage_report",
            "candidate_source_hint": "must show refined basis is not mostly a redshift or source-row-index proxy",
            "required_features": "low_correlation_with_redshift;low_correlation_with_source_row_index;basis_variation_not_dominated_by_z",
            "current_status": "WAITING_FOR_R1_TO_R3",
            "closure_role": "needed_before_any_replay_permission_request",
            "forbidden_inputs_used": "false",
            "endpoint_replay_allowed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "route_id": "R5_control_resistance_preflight",
            "required_evidence": "predeclare_control_suite_for_refined_basis_without_running_endpoint_scores",
            "accepted_source_types": "control_manifest;deterministic_shuffle_seed_manifest;wrong_sign_and_threshold_manifest",
            "candidate_source_hint": "controls must be fixed before replay authorization",
            "required_features": "shuffled_control_resistance;wrong_sign_control_resistance;threshold_control_resistance;zero_void_control",
            "current_status": "WAITING_FOR_R1_TO_R4",
            "closure_role": "needed_to_prevent_repeating_low_z_shuffled_control_failure",
            "forbidden_inputs_used": "false",
            "endpoint_replay_allowed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "route_id": "R6_independent_leakage_review",
            "required_evidence": "complete_external_or_independent_review_of_attached_void_basis_artifacts",
            "accepted_source_types": "review_response_csv;independent_reviewer_attestation;script_validated_no_endpoint_leakage_report",
            "candidate_source_hint": "review must confirm no distance residuals or fit statistics entered basis construction",
            "required_features": "forbidden_inputs_used_false;endpoint_score_claims_false;physical_validation_claims_false",
            "current_status": "WAITING_FOR_R1_TO_R5",
            "closure_role": "needed_before_any_new_replay_authorization_package",
            "forbidden_inputs_used": "false",
            "endpoint_replay_allowed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": policy["claim_boundary"],
        },
    ]

    summary = [
        {
            "policy_id": policy["policy_id"],
            "parent_gate_id": gate["gate_id"],
            "status": "VOID_SOURCE_BASIS_REFINEMENT_ACQUISITION_MANIFEST_BUILT_NOT_ATTACHED",
            "required_routes": str(len(rows)),
            "attached_routes": "0",
            "source_unique_ready": "false",
            "redshift_independence_preflight_complete": "false",
            "control_resistance_preflight_complete": "false",
            "leakage_review_complete": "false",
            "computes_new_scores": "false",
            "uses_distance_residuals": "false",
            "uses_fit_statistics": "false",
            "endpoint_replay_allowed": "false",
            "physical_validation_claimed": "false",
            "verdict": "void_source_basis_refinement_acquisition_manifest_frozen_sources_not_attached",
            "recommended_next_action": "attach_R1_to_R3_source_artifacts_then_run_R4_to_R6_preflight_and_review_before_any_replay_request",
            "claim_boundary": policy["claim_boundary"],
        }
    ]
    write_csv(OUT, rows)
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_VOID_SOURCE_BASIS_REFINEMENT_ACQUISITION_MANIFEST_V1_BUILT "
        f"routes={summary[0]['required_routes']} verdict={summary[0]['verdict']}"
    )


if __name__ == "__main__":
    main()

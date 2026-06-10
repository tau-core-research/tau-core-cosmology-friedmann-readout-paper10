#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_external_photoz_calibration_acquisition_plan_policy_v1.csv"
EVIDENCE_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_photoz_tomographic_calibration_evidence_v1_summary.csv"
HOLDOUT_GATE = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_holdout_calibration_gate_v1_summary.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_external_photoz_calibration_acquisition_plan_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_external_photoz_calibration_acquisition_plan_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    policy = read_one(POLICY)
    evidence = read_one(EVIDENCE_SUMMARY)
    holdout = read_one(HOLDOUT_GATE)

    if policy["status"] != "EXTERNAL_PHOTOZ_CALIBRATION_ACQUISITION_PLAN_FROZEN_NOT_ATTACHED":
        raise SystemExit("unexpected acquisition-plan policy status")
    if policy["current_endpoint_replay_allowed"] != "false":
        raise SystemExit("acquisition plan must not authorize endpoint replay")
    if evidence["h1_independent_evidence_complete"] != "false":
        raise SystemExit("acquisition plan expects H1 to remain open")
    if evidence["endpoint_replay_allowed"] != "false" or holdout["endpoint_replay_allowed"] != "false":
        raise SystemExit("parents must keep endpoint replay forbidden")

    rows = [
        {
            "policy_id": policy["policy_id"],
            "route_id": "R1_photoz_calibration_reference_manifest",
            "required_evidence": "attach_source_frozen_photoz_calibration_reference_or_product_manifest",
            "accepted_source_types": "official_kids_photoz_calibration_paper;official_kids_dr4_or_kids1000_calibration_product;collaboration_release_note",
            "candidate_source_hint": "KiDS-1000/DR4 photo-z calibration references visible in cached KiDS weak-lensing product page",
            "current_status": "TO_ATTACH",
            "h1_closure_role": "needed_to_close_independent_photoz_calibration_evidence",
            "forbidden_inputs_used": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "route_id": "R2_som_gold_or_nz_validation_manifest",
            "required_evidence": "attach_independent_som_gold_or_redshift_distribution_validation_manifest",
            "accepted_source_types": "official_som_gold_catalogue_documentation;source_native_nz_validation_table;published_photoz_validation_summary",
            "candidate_source_hint": "SOM-gold catalogue route and source-native NZ_SOURCE inventory already detected but not independently closed",
            "current_status": "TO_ATTACH",
            "h1_closure_role": "needed_to_show_tomographic_source_bins_are_calibration_supported",
            "forbidden_inputs_used": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "route_id": "R3_tomographic_bin_quality_manifest",
            "required_evidence": "attach_source_side_tomographic_bin_quality_or_delta_z_prior_manifest",
            "accepted_source_types": "published_bin_quality_flags;official_delta_z_priors;survey_validation_table",
            "candidate_source_hint": "five source bins are present; calibration quality and independent bin-level closure are not yet attached",
            "current_status": "TO_ATTACH",
            "h1_closure_role": "needed_before_promoting_tomographic_control_to_source_systematic_candidate",
            "forbidden_inputs_used": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "route_id": "R4_leakage_review_for_attached_calibration",
            "required_evidence": "complete_leakage_review_for_any_attached_calibration_manifest",
            "accepted_source_types": "review_response_csv;independent_reviewer_attestation;script_validated_no_endpoint_leakage_report",
            "candidate_source_hint": "must be created only after R1-R3 artifacts are attached",
            "current_status": "WAITING_FOR_R1_TO_R3",
            "h1_closure_role": "needed_to_verify_attached_calibration_did_not_use_endpoint_residuals_or_scores",
            "forbidden_inputs_used": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": policy["claim_boundary"],
        },
    ]

    summary = [
        {
            "policy_id": policy["policy_id"],
            "status": "EXTERNAL_PHOTOZ_CALIBRATION_ACQUISITION_PLAN_BUILT_NOT_ATTACHED",
            "required_routes": str(len(rows)),
            "attached_routes": "0",
            "leakage_review_complete": "false",
            "h1_independent_evidence_complete": "false",
            "h2_holdout_partition_frozen": evidence["h2_holdout_partition_frozen"],
            "computes_new_scores": "false",
            "uses_kids_data_vector_values_for_scoring": "false",
            "uses_kids_data_vector_values_for_source_selection": "false",
            "uses_residuals": "false",
            "uses_fit_statistics": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "verdict": "external_photoz_calibration_acquisition_plan_frozen_h1_still_open",
            "recommended_next_action": "attach_R1_to_R3_source_frozen_calibration_artifacts_then_complete_R4_leakage_review",
            "claim_boundary": policy["claim_boundary"],
        }
    ]
    write_csv(OUT, rows)
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_EXTERNAL_PHOTOZ_CALIBRATION_ACQUISITION_PLAN_V1_BUILT "
        f"verdict={summary[0]['verdict']}"
    )


if __name__ == "__main__":
    main()

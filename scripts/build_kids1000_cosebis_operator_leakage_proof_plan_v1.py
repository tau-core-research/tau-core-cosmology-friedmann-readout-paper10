#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_operator_leakage_proof_plan_policy_v1.csv"
REQ = ROOT / "data" / "derived" / "kids1000_cosebis_operator_leakage_theorem_requirements_v1_summary.csv"
MASK = ROOT / "data" / "derived" / "kids1000_cosebis_mask_mode_leakage_audit_v1_summary.csv"
PURE = ROOT / "data" / "derived" / "kids1000_cosebis_pure_mask_response_gate_v1_summary.csv"
NULL = ROOT / "data" / "derived" / "kids1000_cosebis_operator_null_safety_gate_v1_summary.csv"
SPEC = ROOT / "data" / "derived" / "kids1000_cosebis_mode_response_operator_spec_v1_summary.csv"
SPECTRUM = ROOT / "data" / "derived" / "kids1000_cosebis_mode_response_spectrum_attempt_v1_summary.csv"

OUT = ROOT / "data" / "derived" / "kids1000_cosebis_operator_leakage_proof_plan_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_operator_leakage_proof_plan_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    policy = read_one(POLICY)
    req = read_one(REQ)
    mask = read_one(MASK)
    pure = read_one(PURE)
    null = read_one(NULL)
    spec = read_one(SPEC)
    spectrum = read_one(SPECTRUM)

    require(policy["status"] == "OPERATOR_LEAKAGE_PROOF_PLAN_POLICY_FROZEN", "unexpected policy status")
    require(policy["computes_new_scores"] == "false", "proof plan must not compute scores")
    require(policy["endpoint_validation_claimed"] == "false", "proof plan must not claim validation")
    require(req["operator_leakage_theorem_proven"] == "false", "leakage theorem should remain open")
    require(mask["uniform_collapse_all_null"] == "true", "uniform tile null limit should be available")
    require(mask["leakage_risk_recorded"] == "true", "nonuniform leakage risk should be recorded")
    require(pure["pure_mask_basis_constructed"] == "true", "pure-mask basis should be constructed")
    require(pure["pure_mask_quotient_triviality_proven"] == "false", "pure-mask quotient triviality should remain open")
    require(null["operator_null_safety_proven"] == "false", "operator null safety should remain open")
    require(spec["mode_response_operator_derived"] == "false", "mode-response operator should remain open")
    require(spectrum["mode_response_operator_derived"] == "false", "spectrum must not imply operator derivation")

    rows = [
        {
            "policy_id": policy["policy_id"],
            "step_id": "P1_uniform_null_limit_anchor",
            "step_status": "ANCHOR_AVAILABLE",
            "source_artifacts": "kids1000_cosebis_mask_mode_leakage_audit_v1",
            "current_evidence": (
                f"uniform_collapse_all_null={mask['uniform_collapse_all_null']};"
                f"max_uniform_collapse_norm={mask['max_uniform_collapse_norm']}"
            ),
            "proof_obligation": "future_operator_must_reduce_to_uniform_tile_null_limit_for_centered_pure_mask_basis",
            "exit_condition": "uniform_limit_included_as_boundary_condition_in_operator_leakage_theorem",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "step_id": "P2_nonuniform_leakage_projection",
            "step_status": "PRIMARY_OPEN_PROOF_STEP",
            "source_artifacts": "kids1000_cosebis_mask_mode_leakage_audit_v1",
            "current_evidence": (
                f"leakage_risk_recorded={mask['leakage_risk_recorded']};"
                f"max_low_mode_rms_envelope_norm={mask['max_low_mode_rms_envelope_norm']}"
            ),
            "proof_obligation": "construct_or_reject_operator_projection_that_sends_nonuniform_mask_only_directions_to_null_or_control_subspace",
            "exit_condition": "nonuniform_mask_response_cannot_masquerade_as_positive_low_mode_tau_path_signal",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "step_id": "P3_pure_mask_quotient_or_control",
            "step_status": "PRIMARY_OPEN_PROOF_STEP",
            "source_artifacts": "kids1000_cosebis_pure_mask_response_gate_v1;kids1000_cosebis_operator_null_safety_gate_v1",
            "current_evidence": (
                f"pure_mask_basis_constructed={pure['pure_mask_basis_constructed']};"
                f"pure_mask_quotient_triviality_proven={pure['pure_mask_quotient_triviality_proven']};"
                f"operator_null_safety_proven={null['operator_null_safety_proven']}"
            ),
            "proof_obligation": "prove_pure_mask_basis_is_quotient_trivial_or_route_it_to_predeclared_null_control_family",
            "exit_condition": "pure_mask_directions_do_not_enter_positive_physical_tau_response_class",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "step_id": "P4_single_operator_coupling",
            "step_status": "COUPLING_OPEN_PROOF_STEP",
            "source_artifacts": "kids1000_cosebis_mode_response_operator_spec_v1;kids1000_cosebis_mode_response_spectrum_attempt_v1",
            "current_evidence": (
                f"conditional_primary_spectrum={spectrum['conditional_primary_spectrum']};"
                f"mode_response_operator_derived={spec['mode_response_operator_derived']}"
            ),
            "proof_obligation": "derive_or_reject_one_source_native_operator_that_generates_both_mode_response_and_null_descent",
            "exit_condition": "mode_spectrum_and_null_safety_are_not_separate_ad_hoc_artifacts",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "step_id": "P5_no_endpoint_feedback_guard",
            "step_status": "GUARD_SATISFIED",
            "source_artifacts": "kids1000_cosebis_operator_leakage_theorem_requirements_v1",
            "current_evidence": (
                f"uses_kids_data_vector_values={req['uses_kids_data_vector_values']};"
                f"contains_fit_statistics={req['contains_fit_statistics']};"
                f"endpoint_scoring_allowed={req['endpoint_scoring_allowed']}"
            ),
            "proof_obligation": "keep_B2_proof_plan_source_side_only_until_theorem_exists",
            "exit_condition": "no_endpoint_feedback_enters_operator_leakage_theorem_inputs",
            "claim_boundary": policy["claim_boundary"],
        },
    ]

    open_steps = [row for row in rows if "OPEN" in row["step_status"]]
    summary = [
        {
            "policy_id": policy["policy_id"],
            "status": "OPERATOR_LEAKAGE_PROOF_PLAN_BUILT_NOT_PROOF",
            "selected_statistic": policy["selected_statistic"],
            "proof_plan_rows": str(len(rows)),
            "anchor_available_count": "1",
            "guard_satisfied_count": "1",
            "open_proof_step_count": str(len(open_steps)),
            "next_primary_exit_condition": "nonuniform_mask_response_cannot_masquerade_as_positive_low_mode_tau_path_signal",
            "operator_leakage_theorem_proven": "false",
            "physical_promotion_ready": "false",
            "validation_ready": "false",
            "computes_new_scores": "false",
            "uses_kids_data_vector_values_for_source_selection": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "verdict": "B2_operator_leakage_exit_conditions_frozen_but_theorem_open",
            "claim_boundary": policy["claim_boundary"],
        }
    ]
    write_csv(OUT, rows)
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_OPERATOR_LEAKAGE_PROOF_PLAN_V1_BUILT "
        f"open_steps={summary[0]['open_proof_step_count']} verdict={summary[0]['verdict']}"
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_operator_leakage_domain_decomposition_policy_v1.csv"
PROJECTION_POLICY = (
    ROOT / "data" / "source_manifest" / "kids1000_cosebis_operator_leakage_projection_criterion_policy_v1.csv"
)
MAPPING = ROOT / "data" / "derived" / "kids1000_cosebis_source_frozen_mapping_vector_v1_summary.csv"
THEORY = ROOT / "data" / "derived" / "kids1000_cosebis_source_frozen_theory_vector_v1_summary.csv"
PURE = ROOT / "data" / "derived" / "kids1000_cosebis_pure_mask_response_gate_v1_summary.csv"
NULL_READY = ROOT / "data" / "derived" / "kids1000_cosebis_null_control_readiness_v1_summary.csv"

OUT = ROOT / "data" / "derived" / "kids1000_cosebis_operator_leakage_domain_decomposition_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_operator_leakage_domain_decomposition_v1_summary.csv"


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
    projection_policy = read_one(PROJECTION_POLICY)
    mapping = read_one(MAPPING)
    theory = read_one(THEORY)
    pure = read_one(PURE)
    null_ready = read_one(NULL_READY)

    require(policy["status"] == "OPERATOR_LEAKAGE_DOMAIN_DECOMPOSITION_POLICY_FROZEN", "unexpected policy")
    require(policy["computes_new_scores"] == "false", "domain decomposition must not compute scores")
    require(policy["endpoint_validation_claimed"] == "false", "domain decomposition must not claim validation")
    require(policy["physical_validation_claimed"] == "false", "domain decomposition must not claim physics")
    require(
        projection_policy["status"] == "OPERATOR_LEAKAGE_PROJECTION_CRITERION_POLICY_FROZEN",
        "projection criterion policy must be frozen first",
    )
    require(mapping["contains_mapping_vector"] == "true", "candidate component needs source-frozen mapping")
    require(mapping["endpoint_scoring_allowed"] == "false", "mapping vector is not endpoint scoring")
    require(theory["contains_theory_vector"] == "true", "candidate component needs source-frozen theory shell")
    require(theory["contains_predictions"] == "false", "theory shell must not contain predictions")
    require(theory["endpoint_scoring_allowed"] == "false", "theory vector is not endpoint scoring")
    require(pure["pure_mask_basis_constructed"] == "true", "mask component needs pure-mask basis")
    require(pure["pure_mask_quotient_triviality_proven"] == "false", "mask quotient proof must remain open")
    require(null_ready["control_family_count"] == "4", "expected four null-control families")
    require(null_ready["contains_control_scores"] == "false", "null controls must not contain scores")

    rows = [
        {
            "policy_id": policy["policy_id"],
            "component_id": "V_phys_candidate",
            "component_status": "DECLARED_CANDIDATE_NOT_PHYSICAL_PROOF",
            "source_artifacts": (
                "data/derived/kids1000_cosebis_source_frozen_mapping_vector_v1_summary.csv;"
                "data/derived/kids1000_cosebis_source_frozen_theory_vector_v1_summary.csv"
            ),
            "formal_role": "source_frozen_low_mode_candidate_response_subspace",
            "row_count": theory["theory_rows"],
            "allowed_interpretation": "candidate_response_for_operator_leakage_testing_only",
            "forbidden_interpretation": "validated_physical_signal_or_positive_tau_detection",
            "proof_status": "declared_not_orthogonalized_not_leakage_proven",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "component_id": "V_mask",
            "component_status": "DECLARED_MASK_ONLY_BASIS_NOT_NULL_PROVEN",
            "source_artifacts": (
                "data/derived/kids1000_cosebis_pure_mask_response_tile_basis_v1.csv;"
                "data/derived/kids1000_cosebis_pure_mask_response_domain_basis_v1.csv"
            ),
            "formal_role": "pure_mask_and_depth_path_basis_directions",
            "row_count": pure["domain_rows"],
            "allowed_interpretation": "mask_only_leakage_test_domain",
            "forbidden_interpretation": "physical_low_mode_tau_response",
            "proof_status": "basis_exists_but_quotient_triviality_and_operator_coupling_not_proven",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "component_id": "V_control_or_null",
            "component_status": "DECLARED_CONTROL_OR_NULL_NOT_SIGNAL",
            "source_artifacts": "data/derived/kids1000_cosebis_null_control_readiness_v1_summary.csv",
            "formal_role": "predeclared_control_or_quotient_null_response_family",
            "row_count": null_ready["control_draw_count"],
            "allowed_interpretation": "routing_target_for_mask_response_or_null_descent_tests",
            "forbidden_interpretation": "positive_response_family",
            "proof_status": "controls_exist_but_operator_routing_not_proven",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "component_id": "no_endpoint_feedback_guard",
            "component_status": "SATISFIED_AS_LEDGER_GUARD",
            "source_artifacts": "policy_and_summary_flags_only",
            "formal_role": "forbid_endpoint_values_from_component_declaration",
            "row_count": "0",
            "allowed_interpretation": "leakage_prevention_guard",
            "forbidden_interpretation": "evidence_for_physical_promotion",
            "proof_status": "guard_satisfied_but_not_a_leakage_theorem",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "component_id": "decomposition_status",
            "component_status": "DECLARED_BOOKKEEPING_NOT_PROJECTION_PROOF",
            "source_artifacts": "this_ledger",
            "formal_role": "V_source = V_phys_candidate plus V_mask plus V_control_or_null",
            "row_count": "3",
            "allowed_interpretation": "domain_decomposition_available_for_future_projection_theorem",
            "forbidden_interpretation": "pairwise_orthogonality_or_null_projection_proven",
            "proof_status": "domain_components_declared_only",
            "claim_boundary": policy["claim_boundary"],
        },
    ]

    summary = [
        {
            "policy_id": policy["policy_id"],
            "status": "OPERATOR_LEAKAGE_DOMAIN_DECOMPOSITION_DECLARED_NOT_PROJECTION_PROOF",
            "selected_statistic": policy["selected_statistic"],
            "component_rows": str(len(rows)),
            "domain_decomposition_declared": "true",
            "candidate_physical_component_declared": "true",
            "mask_component_declared": "true",
            "control_or_null_component_declared": "true",
            "no_endpoint_feedback_guard_satisfied": "true",
            "components_pairwise_orthogonality_proven": "false",
            "mask_component_quotient_triviality_proven": "false",
            "operator_projection_condition_proven": "false",
            "control_routing_condition_proven": "false",
            "single_operator_consistency_proven": "false",
            "operator_leakage_theorem_proven": "false",
            "p2_nonuniform_leakage_closed": "false",
            "physical_promotion_ready": "false",
            "validation_ready": "false",
            "computes_new_scores": "false",
            "uses_kids_data_vector_values_for_source_selection": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "verdict": "domain_decomposition_declared_but_projection_and_leakage_theorem_remain_open",
            "claim_boundary": policy["claim_boundary"],
        }
    ]

    write_csv(OUT, rows)
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_OPERATOR_LEAKAGE_DOMAIN_DECOMPOSITION_V1_BUILT "
        f"declared={summary[0]['domain_decomposition_declared']} "
        f"p2_closed={summary[0]['p2_nonuniform_leakage_closed']} verdict={summary[0]['verdict']}"
    )


if __name__ == "__main__":
    main()

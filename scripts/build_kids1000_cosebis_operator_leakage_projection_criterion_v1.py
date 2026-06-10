#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_operator_leakage_projection_criterion_policy_v1.csv"
PLAN = ROOT / "data" / "derived" / "kids1000_cosebis_operator_leakage_proof_plan_v1_summary.csv"
REQ = ROOT / "data" / "derived" / "kids1000_cosebis_operator_leakage_theorem_requirements_v1_summary.csv"
PURE = ROOT / "data" / "derived" / "kids1000_cosebis_pure_mask_response_gate_v1_summary.csv"
NULL = ROOT / "data" / "derived" / "kids1000_cosebis_operator_null_safety_gate_v1_summary.csv"
DOMAIN = ROOT / "data" / "derived" / "kids1000_cosebis_operator_leakage_domain_decomposition_v1_summary.csv"

OUT = ROOT / "data" / "derived" / "kids1000_cosebis_operator_leakage_projection_criterion_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_operator_leakage_projection_criterion_v1_summary.csv"


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
    plan = read_one(PLAN)
    req = read_one(REQ)
    pure = read_one(PURE)
    null = read_one(NULL)
    domain = read_one(DOMAIN)

    require(policy["status"] == "OPERATOR_LEAKAGE_PROJECTION_CRITERION_POLICY_FROZEN", "unexpected policy")
    require(policy["computes_new_scores"] == "false", "criterion must not compute scores")
    require(policy["endpoint_validation_claimed"] == "false", "criterion must not claim validation")
    require(plan["operator_leakage_theorem_proven"] == "false", "leakage theorem must remain open")
    require(plan["open_proof_step_count"] == "3", "expected three open B2 proof steps")
    require(req["operator_leakage_theorem_proven"] == "false", "requirements must not imply theorem")
    require(pure["pure_mask_basis_constructed"] == "true", "pure-mask basis must exist")
    require(pure["pure_mask_quotient_triviality_proven"] == "false", "pure-mask quotient triviality remains open")
    require(null["operator_null_safety_proven"] == "false", "operator null safety remains open")
    require(
        domain["status"] == "OPERATOR_LEAKAGE_DOMAIN_DECOMPOSITION_DECLARED_NOT_PROJECTION_PROOF",
        "domain decomposition must be declared first",
    )
    require(domain["domain_decomposition_declared"] == "true", "domain decomposition must be declared")
    require(domain["operator_projection_condition_proven"] == "false", "projection condition must remain open")

    rows = [
        {
            "policy_id": policy["policy_id"],
            "criterion_id": "C1_domain_decomposition",
            "criterion_status": "DECLARED_NOT_PROJECTION_PROOF",
            "formal_statement": "V_source = V_phys_candidate plus V_mask plus V_control_or_null",
            "purpose": "separate candidate path/readout response from mask-only directions before any physical promotion",
            "current_status": (
                f"domain_decomposition_declared={domain['domain_decomposition_declared']};"
                f"components_pairwise_orthogonality_proven={domain['components_pairwise_orthogonality_proven']};"
                f"operator_projection_condition_proven={domain['operator_projection_condition_proven']}"
            ),
            "exit_condition": "source_native_operator_domain_decomposition_declared_without_endpoint_feedback",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "criterion_id": "C2_null_projection_condition",
            "criterion_status": "SUFFICIENT_CONDITION_FROZEN_NOT_PROVEN",
            "formal_statement": "Pi_phys O m = 0 for every m in V_mask, modulo quotient-null directions",
            "purpose": "prevent nonuniform mask-only perturbations from entering the positive low-mode Tau response class",
            "current_status": (
                f"operator_null_safety_proven={null['operator_null_safety_proven']};"
                f"mask_null_operator_proven={null['mask_null_operator_proven']}"
            ),
            "exit_condition": "prove_null_projection_condition_or_reject_the_candidate_operator_class",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "criterion_id": "C3_control_routing_alternative",
            "criterion_status": "ALTERNATIVE_SUFFICIENT_CONDITION_FROZEN_NOT_PROVEN",
            "formal_statement": "O(V_mask) subset V_control and V_control is scored only as predeclared null-control response",
            "purpose": "allow mask response to exist only as a separately controlled null family, not as positive Tau signal",
            "current_status": (
                f"null_control_family_count={null['null_control_family_count']};"
                f"null_control_draw_count={null['null_control_draw_count']}"
            ),
            "exit_condition": "prove_mask_response_is_routed_to_predeclared_control_family_before_positive_interpretation",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "criterion_id": "C4_single_operator_consistency",
            "criterion_status": "CONSISTENCY_CONDITION_FROZEN_NOT_PROVEN",
            "formal_statement": "the same O must generate the mode response and satisfy C2 or C3",
            "purpose": "avoid using one artifact for the low-mode spectrum and another unrelated artifact for null descent",
            "current_status": (
                f"next_primary_exit_condition={plan['next_primary_exit_condition']};"
                f"operator_leakage_theorem_proven={plan['operator_leakage_theorem_proven']}"
            ),
            "exit_condition": "derive_one_operator_or_keep_B2_open",
            "claim_boundary": policy["claim_boundary"],
        },
        {
            "policy_id": policy["policy_id"],
            "criterion_id": "C5_theorem_status",
            "criterion_status": "OPEN_NOT_PROVEN",
            "formal_statement": "C1 plus C2 or C3 plus C4 would be sufficient to close P2 nonuniform leakage",
            "purpose": "record that the criterion is sufficient as a theorem target, not already established",
            "current_status": "criterion_frozen; theorem_absent; validation_forbidden",
            "exit_condition": "future_theorem_proves_conditions_or_B2_remains_open",
            "claim_boundary": policy["claim_boundary"],
        },
    ]

    summary = [
        {
            "policy_id": policy["policy_id"],
            "status": "OPERATOR_LEAKAGE_PROJECTION_CRITERION_BUILT_NOT_PROVEN",
            "selected_statistic": policy["selected_statistic"],
            "criterion_rows": str(len(rows)),
            "sufficient_projection_criterion_frozen": "true",
            "domain_decomposition_declared": "true",
            "null_projection_condition_proven": "false",
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
            "verdict": "nonuniform_leakage_projection_criterion_frozen_but_not_proven",
            "claim_boundary": policy["claim_boundary"],
        }
    ]
    write_csv(OUT, rows)
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_OPERATOR_LEAKAGE_PROJECTION_CRITERION_V1_BUILT "
        f"p2_closed={summary[0]['p2_nonuniform_leakage_closed']} verdict={summary[0]['verdict']}"
    )


if __name__ == "__main__":
    main()

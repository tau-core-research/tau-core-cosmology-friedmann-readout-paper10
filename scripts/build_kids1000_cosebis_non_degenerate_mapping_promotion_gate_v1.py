#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_non_degenerate_mapping_promotion_gate_policy_v1.csv"
F_OVERLAP = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_resolution_decision_v1_summary.csv"
PREFLIGHT = ROOT / "data" / "derived" / "kids1000_cosebis_path_mapping_source_preflight_v1_summary.csv"
DEGENERACY = ROOT / "data" / "derived" / "kids1000_cosebis_partial_control_degeneracy_audit_v1_summary.csv"
THEORY = ROOT / "data" / "derived" / "kids1000_cosebis_theory_vector_readiness_v1_summary.csv"
NULL_READINESS = ROOT / "data" / "derived" / "kids1000_cosebis_null_control_readiness_v1_summary.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_non_degenerate_mapping_promotion_gate_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_non_degenerate_mapping_promotion_gate_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def gate_row(
    policy: dict[str, str],
    gate_id: str,
    description: str,
    current_state: str,
    required_state: str,
    passed: bool,
    evidence_artifact: str,
    blocker_class: str,
    next_action: str,
) -> dict[str, str]:
    return {
        "policy_id": policy["policy_id"],
        "gate_id": gate_id,
        "gate_description": description,
        "current_state": current_state,
        "required_state": required_state,
        "gate_passed": str(passed).lower(),
        "blocking_status": "not_blocking" if passed else blocker_class,
        "evidence_artifact": evidence_artifact,
        "next_action": next_action,
        "uses_kids_data_vector_values": "false",
        "uses_posterior_chains": "false",
        "uses_posthoc_selection": "false",
        "contains_theory_vector": "true" if gate_id == "PROMOTE_04_THEORY_VECTOR_COMPUTED" and passed else "false",
        "contains_predictions": "false",
        "contains_residuals": "false",
        "contains_fit_statistics": "false",
        "endpoint_scoring_allowed": "false",
        "scoring_executed": "false",
        "claim_boundary": policy["claim_boundary"],
    }


def main() -> None:
    policy = read_one(POLICY)
    f_overlap = read_one(F_OVERLAP)
    preflight = read_one(PREFLIGHT)
    degeneracy = read_one(DEGENERACY)
    theory = read_one(THEORY)
    null_readiness = read_one(NULL_READINESS)
    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("promotion gate policy must keep endpoint scoring disabled")
    if degeneracy["policy_id"] != policy["parent_partial_control_degeneracy_audit"]:
        raise SystemExit("parent degeneracy audit mismatch")

    positive_rank = int(degeneracy["positive_effective_rank_tol_1e_minus_8"])
    rows = [
        gate_row(
            policy,
            "PROMOTE_01_F_OVERLAP_ENDPOINT_ROUTE",
            "Accept an endpoint-grade F_overlap route from official geometry or full route masks.",
            f"endpoint_ready_{f_overlap['f_overlap_endpoint_ready']}_control_ready_{f_overlap['f_overlap_control_ready']}",
            "endpoint_ready_true",
            f_overlap["f_overlap_endpoint_ready"] == "true",
            "data/derived/kids1000_cosebis_f_overlap_resolution_decision_v1_summary.csv",
            "blocking_source_overlap",
            f_overlap["first_required_next_action"],
        ),
        gate_row(
            policy,
            "PROMOTE_02_SOURCE_PREFLIGHT_MAPPING_READY",
            "Require all source-side mapping inputs to be ready before theory-vector construction.",
            f"available_{preflight['available_component_count']}_partial_{preflight['partial_available_component_count']}_missing_{preflight['missing_component_count']}_mapping_ready_{preflight['mapping_ready']}",
            "mapping_ready_true_missing_0_declared_unexecuted_0_declared_uncomputed_0",
            preflight["mapping_ready"] == "true"
            and preflight["missing_component_count"] == "0"
            and preflight["declared_not_executed_component_count"] == "0"
            and preflight["declared_not_computed_component_count"] == "0",
            "data/derived/kids1000_cosebis_path_mapping_source_preflight_v1_summary.csv",
            "blocking_source_preflight",
            "freeze_F_overlap_D_path_E_web_C_norm_and_null_control_execution_inputs",
        ),
        gate_row(
            policy,
            "PROMOTE_03_NON_DEGENERATE_BRANCH_GEOMETRY",
            "Reject endpoint promotion if the candidate branch family is effectively rank one.",
            f"positive_rank_{positive_rank}_degenerate_{degeneracy['branch_degeneracy_detected']}",
            "effective_rank_at_least_2_and_branch_degeneracy_detected_false",
            positive_rank >= 2 and degeneracy["branch_degeneracy_detected"] == "false",
            "data/derived/kids1000_cosebis_partial_control_degeneracy_audit_v1_summary.csv",
            "blocking_rank_one_partial_control",
            degeneracy["recommended_next_action"],
        ),
        gate_row(
            policy,
            "PROMOTE_04_THEORY_VECTOR_COMPUTED",
            "Require a frozen 300-row theory vector before endpoint scoring.",
            theory["theory_vector_status"],
            "computed_from_source_frozen_mapping",
            theory["theory_vector_status"] == "computed_from_source_frozen_mapping",
            "data/derived/kids1000_cosebis_theory_vector_readiness_v1_summary.csv",
            "blocking_theory_vector",
            "theory_vector_available_execute_null_controls_and_resolve_degeneracy_before_scoring",
        ),
        gate_row(
            policy,
            "PROMOTE_05_NULL_CONTROLS_EXECUTED_AFTER_MAPPING",
            "Run predeclared null controls only after the non-degenerate mapping vector exists.",
            f"controls_executed_{null_readiness['current_controls_executed']}",
            "null_controls_executed_true_after_mapping",
            null_readiness["current_controls_executed"] == "true",
            "data/derived/kids1000_cosebis_null_control_readiness_v1_summary.csv",
            "blocking_null_controls",
            "execute_predeclared_null_controls_after_mapping_vector_exists",
        ),
        gate_row(
            policy,
            "PROMOTE_06_LEAKAGE_GUARDS",
            "Keep endpoint data residuals posterior chains and post-hoc labels forbidden before scoring.",
            "forbidden_inputs_declared",
            "forbidden_inputs_declared",
            all(
                marker in policy["forbidden_inputs"]
                for marker in [
                    "kids_data_vector_values",
                    "posterior_chains",
                    "lensing_residuals",
                    "posthoc_weight_selection",
                    "posthoc_mask_subset_selection",
                ]
            ),
            "data/source_manifest/kids1000_cosebis_non_degenerate_mapping_promotion_gate_policy_v1.csv",
            "blocking_leakage_guard",
            "keep_forbidden_inputs_false_in_all_future_promotion_artifacts",
        ),
    ]

    passed = [row for row in rows if row["gate_passed"] == "true"]
    blockers = [row for row in rows if row["gate_passed"] == "false"]
    status = (
        "NON_DEGENERATE_MAPPING_PROMOTION_GATE_PASSED_NOT_SCORED"
        if not blockers
        else "NON_DEGENERATE_MAPPING_PROMOTION_GATE_BUILT_NOT_READY"
    )
    summary = {
        "policy_id": policy["policy_id"],
        "status": status,
        "gate_count": str(len(rows)),
        "passed_gate_count": str(len(passed)),
        "blocking_gate_count": str(len(blockers)),
        "first_blocking_gate": blockers[0]["gate_id"] if blockers else "none",
        "non_degenerate_mapping_promotion_allowed": str(not blockers).lower(),
        "endpoint_scoring_allowed": "false",
        "scoring_executed": "false",
        "contains_theory_vector": str(any(row["contains_theory_vector"] == "true" for row in rows)).lower(),
        "contains_predictions": "false",
        "contains_residuals": "false",
        "contains_fit_statistics": "false",
        "uses_kids_data_vector_values": "false",
        "uses_posterior_chains": "false",
        "uses_posthoc_selection": "false",
        "claim_boundary": policy["claim_boundary"],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_NON_DEGENERATE_MAPPING_PROMOTION_GATE_V1_BUILT "
        f"passed={summary['passed_gate_count']} blockers={summary['blocking_gate_count']} "
        "endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()

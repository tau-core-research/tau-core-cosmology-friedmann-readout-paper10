#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQ = ROOT / "data/derived/kids1000_cosebis_operator_leakage_theorem_requirements_v1_summary.csv"
PROJ = ROOT / "data/derived/kids1000_cosebis_operator_leakage_projection_criterion_v1_summary.csv"
DOMAIN = ROOT / "data/derived/kids1000_cosebis_operator_leakage_domain_decomposition_v1_summary.csv"
NULL = ROOT / "data/derived/kids1000_cosebis_operator_null_safety_gate_v1_summary.csv"
PLAN = ROOT / "data/derived/joint_kids_caveated_block_resolution_plan_v1_summary.csv"
OUT = ROOT / "data/derived/kids1000_cosebis_operator_leakage_closure_attempt_v1.csv"
SUMMARY = ROOT / "data/derived/kids1000_cosebis_operator_leakage_closure_attempt_v1_summary.csv"
DOC = ROOT / "docs/kids1000_cosebis_operator_leakage_closure_attempt_v1.md"
CLAIM_BOUNDARY = "kids1000_cosebis_operator_leakage_closure_attempt_not_validation"


def read_one(path: Path) -> dict[str, str]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path.relative_to(ROOT)}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def main() -> None:
    req = read_one(REQ)
    proj = read_one(PROJ)
    domain = read_one(DOMAIN)
    null = read_one(NULL)
    plan = read_one(PLAN)

    if plan["next_primary_proof_gate"] != "B2_operator_leakage_theorem_open":
        raise SystemExit("KiDS resolution plan is not currently focused on B2")
    if req["operator_leakage_theorem_proven"] != "false":
        raise SystemExit("closure attempt must not inherit a proven leakage theorem")
    if proj["operator_leakage_theorem_proven"] != "false":
        raise SystemExit("projection criterion must not mark leakage theorem proven")
    if domain["p2_nonuniform_leakage_closed"] != "false":
        raise SystemExit("domain decomposition must keep nonuniform leakage open")
    if null["operator_null_safety_proven"] != "false":
        raise SystemExit("null-safety gate must remain unproven")

    rows = [
        {
            "attempt_id": "KIDS1000_COSEBIS_OPERATOR_LEAKAGE_CLOSURE_ATTEMPT_V1",
            "closure_item": "C1_uniform_limit",
            "status": "AVAILABLE_AS_LIMIT_CHECK",
            "current_artifact": rel(REQ),
            "formal_requirement": "The admissible operator must reduce to the centered uniform-tile pure-mask null limit.",
            "current_evidence": f"uniform_tile_null_limit_available={req['uniform_tile_null_limit_available']}; satisfied_as_source_limit_count={req['satisfied_as_source_limit_count']}",
            "remaining_gap": "Extend the limit statement from the uniform source-side check to the full survey-native nonuniform operator.",
            "dimension_check": "The uniform collapse norm is dimensionless and cannot set a lensing amplitude.",
            "known_limit_check": "A centered pure-mask basis must map to zero in the uniform-mask limit.",
            "computes_new_scores": "false",
            "uses_kids_data_vector_values": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "attempt_id": "KIDS1000_COSEBIS_OPERATOR_LEAKAGE_CLOSURE_ATTEMPT_V1",
            "closure_item": "C2_domain_decomposition",
            "status": "DECLARED_NOT_PROVEN",
            "current_artifact": rel(DOMAIN),
            "formal_requirement": "Decompose the source domain into physical candidate, mask-only, and controlled/null subspaces.",
            "current_evidence": f"domain_decomposition_declared={domain['domain_decomposition_declared']}; components_pairwise_orthogonality_proven={domain['components_pairwise_orthogonality_proven']}",
            "remaining_gap": "Prove pairwise orthogonality or a replacement quotient decomposition strong enough for the operator proof.",
            "dimension_check": "The decomposition is a vector-space statement; it does not introduce physical units.",
            "known_limit_check": "Gauge/null and mask-only directions must not create endpoint-visible physical response by representation choice.",
            "computes_new_scores": "false",
            "uses_kids_data_vector_values": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "attempt_id": "KIDS1000_COSEBIS_OPERATOR_LEAKAGE_CLOSURE_ATTEMPT_V1",
            "closure_item": "C3_mask_quotient_triviality",
            "status": "OPEN_BLOCKER",
            "current_artifact": rel(DOMAIN),
            "formal_requirement": "For each admissible mask-only direction m, the quotient-visible projection of O_tau(m) must vanish or be routed to a frozen null-control family.",
            "current_evidence": f"mask_component_quotient_triviality_proven={domain['mask_component_quotient_triviality_proven']}; null_control_draw_count={null['null_control_draw_count']}",
            "remaining_gap": "Prove null projection for mask-only directions, or prove same-statistic routing into the already frozen null-control family.",
            "dimension_check": "Mask-only directions are dimensionless source objects; their response cannot be promoted to a physical amplitude without the operator theorem.",
            "known_limit_check": "A pure mask perturbation must not mimic a standard-lensing or Tau path signal.",
            "computes_new_scores": "false",
            "uses_kids_data_vector_values": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "attempt_id": "KIDS1000_COSEBIS_OPERATOR_LEAKAGE_CLOSURE_ATTEMPT_V1",
            "closure_item": "C4_projection_criterion",
            "status": "FROZEN_NOT_PROVEN",
            "current_artifact": rel(PROJ),
            "formal_requirement": "The physical projection, control routing, and single-operator consistency conditions must all hold under one operator.",
            "current_evidence": f"null_projection_condition_proven={proj['null_projection_condition_proven']}; control_routing_condition_proven={proj['control_routing_condition_proven']}; single_operator_consistency_proven={proj['single_operator_consistency_proven']}",
            "remaining_gap": "Show that the projection criterion is satisfied by a single source-native operator rather than separate diagnostic artifacts.",
            "dimension_check": "Projection conditions are quotient-level algebraic checks, not a new theory-vector normalization.",
            "known_limit_check": "The same operator must recover standard null limits and the candidate response domain.",
            "computes_new_scores": "false",
            "uses_kids_data_vector_values": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "attempt_id": "KIDS1000_COSEBIS_OPERATOR_LEAKAGE_CLOSURE_ATTEMPT_V1",
            "closure_item": "C5_gauge_quotient_descent",
            "status": "OPEN_BLOCKER",
            "current_artifact": rel(NULL),
            "formal_requirement": "Gauge and representation changes must descend to the same quotient-visible response class.",
            "current_evidence": f"gauge_quotient_descent_proven={null['gauge_quotient_descent_proven']}; operator_null_safety_proven={null['operator_null_safety_proven']}",
            "remaining_gap": "Prove that admissible representation changes cannot move mask leakage into the physical quotient class.",
            "dimension_check": "Gauge transformations must not alter physical units or create amplitude support.",
            "known_limit_check": "Quotient-trivial transformations must leave endpoint predictions unchanged.",
            "computes_new_scores": "false",
            "uses_kids_data_vector_values": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(OUT, rows)

    open_blockers = sum(row["status"] == "OPEN_BLOCKER" for row in rows)
    frozen_not_proven = sum(row["status"] in {"FROZEN_NOT_PROVEN", "DECLARED_NOT_PROVEN"} for row in rows)
    summary = {
        "attempt_id": "KIDS1000_COSEBIS_OPERATOR_LEAKAGE_CLOSURE_ATTEMPT_V1",
        "status": "OPERATOR_LEAKAGE_CLOSURE_ATTEMPT_NARROWS_PROOF_NOT_PROVEN",
        "parent_joint_blocker": plan["next_primary_proof_gate"],
        "closure_items": str(len(rows)),
        "available_limit_checks": "1",
        "declared_or_frozen_not_proven_items": str(frozen_not_proven),
        "open_blocker_count": str(open_blockers),
        "uniform_limit_available": req["uniform_tile_null_limit_available"],
        "domain_decomposition_declared": domain["domain_decomposition_declared"],
        "null_control_draw_count": null["null_control_draw_count"],
        "operator_leakage_theorem_proven": "false",
        "mask_quotient_triviality_proven": domain["mask_component_quotient_triviality_proven"],
        "null_projection_condition_proven": proj["null_projection_condition_proven"],
        "control_routing_condition_proven": proj["control_routing_condition_proven"],
        "single_operator_consistency_proven": proj["single_operator_consistency_proven"],
        "gauge_quotient_descent_proven": null["gauge_quotient_descent_proven"],
        "computes_new_scores": "false",
        "uses_kids_data_vector_values": "false",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "verdict": "OPERATOR_LEAKAGE_CLOSURE_ATTEMPT_NARROWS_PROOF_BUT_THEOREM_REMAINS_OPEN",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(SUMMARY, [summary])

    DOC.write_text(
        "\n".join(
            [
                "# KiDS/COSEBIs operator-leakage closure attempt v1",
                "",
                "**Doc class:** proof-blocker narrowing artifact",
                "**Status:** theorem not proven; no endpoint scoring; no validation claim",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`",
                "",
                "This note narrows the first KiDS/COSEBIs physical-promotion blocker:",
                "`B2_operator_leakage_theorem_open`.  It does not close the blocker.",
                "Its role is to state the exact source-side conditions under which",
                "nonuniform mask leakage cannot be promoted into a quotient-visible",
                "Tau path/readout signal.",
                "",
                "Minimal target theorem:",
                "",
                "```text",
                "For every admissible mask-only direction m in the source mask domain,",
                "either P_phys O_tau(m) = 0 in the quotient, or O_tau(m) is routed",
                "to the frozen null-control family under the same statistic and",
                "covariance discipline.  The same operator must reduce to the",
                "uniform-tile pure-mask null limit and descend through gauge/quotient",
                "representations.",
                "```",
                "",
                "Current status:",
                "",
                f"- uniform limit available: `{summary['uniform_limit_available']}`",
                f"- domain decomposition declared: `{summary['domain_decomposition_declared']}`",
                f"- null-control draws available: `{summary['null_control_draw_count']}`",
                f"- mask quotient triviality proven: `{summary['mask_quotient_triviality_proven']}`",
                f"- null projection condition proven: `{summary['null_projection_condition_proven']}`",
                f"- control routing condition proven: `{summary['control_routing_condition_proven']}`",
                f"- single-operator consistency proven: `{summary['single_operator_consistency_proven']}`",
                f"- gauge quotient descent proven: `{summary['gauge_quotient_descent_proven']}`",
                f"- verdict: `{summary['verdict']}`",
                "",
                "Interpretation: the KiDS low-tail block remains useful as a caveated",
                "diagnostic signal, but the operator-level theorem is still open.  The",
                "next proof work must close mask quotient triviality or same-statistic",
                "control routing, and then prove gauge/quotient descent for the same",
                "source-native operator.",
                "",
            ]
        )
    )
    print(
        "KIDS1000_COSEBIS_OPERATOR_LEAKAGE_CLOSURE_ATTEMPT_V1_BUILT "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()

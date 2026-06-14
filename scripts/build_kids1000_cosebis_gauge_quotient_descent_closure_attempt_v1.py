#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GAUGE = ROOT / "data/derived/kids1000_cosebis_gauge_quotient_descent_gate_v1_summary.csv"
LEAKAGE = ROOT / "data/derived/kids1000_cosebis_operator_leakage_closure_attempt_v1_summary.csv"
NULL = ROOT / "data/derived/kids1000_cosebis_operator_null_safety_gate_v1_summary.csv"
PLAN = ROOT / "data/derived/joint_kids_caveated_block_resolution_plan_v1_summary.csv"
OUT = ROOT / "data/derived/kids1000_cosebis_gauge_quotient_descent_closure_attempt_v1.csv"
SUMMARY = ROOT / "data/derived/kids1000_cosebis_gauge_quotient_descent_closure_attempt_v1_summary.csv"
DOC = ROOT / "docs/kids1000_cosebis_gauge_quotient_descent_closure_attempt_v1.md"
CLAIM_BOUNDARY = "kids1000_cosebis_gauge_quotient_descent_closure_attempt_not_validation"


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
    gauge = read_one(GAUGE)
    leakage = read_one(LEAKAGE)
    null = read_one(NULL)
    plan = read_one(PLAN)

    if plan["next_parallel_proof_gate"] != "B3_gauge_quotient_descent_open":
        raise SystemExit("KiDS resolution plan is not currently carrying B3 as parallel gate")
    if leakage["operator_leakage_theorem_proven"] != "false":
        raise SystemExit("gauge closure attempt must not inherit proven leakage theorem")
    if gauge["gauge_quotient_descent_proven"] != "false":
        raise SystemExit("gauge descent must remain unproven")
    if gauge["survey_native_operator_constructed"] != "false":
        raise SystemExit("survey-native operator must not be marked constructed")
    if null["gauge_quotient_descent_proven"] != "false":
        raise SystemExit("null-safety gate must keep gauge descent open")

    rows = [
        {
            "attempt_id": "KIDS1000_COSEBIS_GAUGE_QUOTIENT_DESCENT_CLOSURE_ATTEMPT_V1",
            "descent_item": "D1_equivalence_relation",
            "status": "DECLARED_NOT_PROVEN",
            "current_artifact": rel(GAUGE),
            "formal_requirement": "Declare source representatives equivalent when they differ only by tile relabeling, source-basis recentering, admissible normalization, or gauge/null directions.",
            "current_evidence": f"equivalence_classes_declared={gauge['equivalence_classes_declared']}",
            "remaining_gap": "Prove the future operator is well-defined on equivalence classes, not only on selected representatives.",
            "dimension_check": "Representative changes are dimensionless or unit-preserving and cannot set COSEBIs response units.",
            "known_limit_check": "The identity representative and uniform null representative must map to the same physical class.",
            "computes_new_scores": "false",
            "uses_kids_data_vector_values": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "attempt_id": "KIDS1000_COSEBIS_GAUGE_QUOTIENT_DESCENT_CLOSURE_ATTEMPT_V1",
            "descent_item": "D2_uniform_offset_limit",
            "status": "AVAILABLE_AS_LIMIT_CHECK",
            "current_artifact": rel(GAUGE),
            "formal_requirement": "The quotient map must preserve the centered uniform mask-offset null limit.",
            "current_evidence": f"uniform_mask_offset_limit_available={gauge['uniform_mask_offset_limit_available']}",
            "remaining_gap": "Lift the uniform limit from source-side evidence to the full survey-native operator domain.",
            "dimension_check": "The uniform offset test is dimensionless and cannot provide physical amplitude.",
            "known_limit_check": "Uniform centered offsets remain quotient-trivial.",
            "computes_new_scores": "false",
            "uses_kids_data_vector_values": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "attempt_id": "KIDS1000_COSEBIS_GAUGE_QUOTIENT_DESCENT_CLOSURE_ATTEMPT_V1",
            "descent_item": "D3_normalization_invariance",
            "status": "OPEN_BLOCKER",
            "current_artifact": rel(GAUGE),
            "formal_requirement": "Allowed source-normalization representatives must not create or remove quotient-visible path response.",
            "current_evidence": f"normalization_invariance_proven={gauge['normalization_invariance_proven']}",
            "remaining_gap": "Prove invariance under admissible normalization/rescaling, or route normalization-sensitive response to controls.",
            "dimension_check": "Normalization changes must preserve the operator codomain units.",
            "known_limit_check": "Null controls and zero path-source cases must remain null after normalization changes.",
            "computes_new_scores": "false",
            "uses_kids_data_vector_values": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "attempt_id": "KIDS1000_COSEBIS_GAUGE_QUOTIENT_DESCENT_CLOSURE_ATTEMPT_V1",
            "descent_item": "D4_tile_relabeling_invariance",
            "status": "OPEN_BLOCKER",
            "current_artifact": rel(GAUGE),
            "formal_requirement": "Tile relabeling or route-coordinate relabeling must not change the physical quotient response.",
            "current_evidence": f"tile_relabeling_invariance_proven={gauge['tile_relabeling_invariance_proven']}",
            "remaining_gap": "Prove operator commutation with admissible relabelings or replace route dependence with label-invariant aggregates.",
            "dimension_check": "Tile indices are labels rather than physical units.",
            "known_limit_check": "Permutation of identical route tiles must not change physical response.",
            "computes_new_scores": "false",
            "uses_kids_data_vector_values": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "attempt_id": "KIDS1000_COSEBIS_GAUGE_QUOTIENT_DESCENT_CLOSURE_ATTEMPT_V1",
            "descent_item": "D5_pure_mask_control_compatibility",
            "status": "OPEN_BLOCKER",
            "current_artifact": f"{rel(GAUGE)};{rel(LEAKAGE)}",
            "formal_requirement": "Gauge/representative changes of pure-mask modes must remain quotient-trivial or stay inside the same frozen null-control family.",
            "current_evidence": f"pure_mask_control_compatibility_proven={gauge['pure_mask_control_compatibility_proven']}; mask_quotient_triviality_proven={leakage['mask_quotient_triviality_proven']}",
            "remaining_gap": "Couple the gauge descent proof to the B2 leakage closure proof, not a separate representative choice.",
            "dimension_check": "Pure-mask representative changes cannot set endpoint amplitudes or physical units.",
            "known_limit_check": "Standard-lensing null limit cannot gain positive Tau path signal from pure-mask representatives.",
            "computes_new_scores": "false",
            "uses_kids_data_vector_values": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "attempt_id": "KIDS1000_COSEBIS_GAUGE_QUOTIENT_DESCENT_CLOSURE_ATTEMPT_V1",
            "descent_item": "D6_single_operator_dependency",
            "status": "OPEN_BLOCKER",
            "current_artifact": rel(GAUGE),
            "formal_requirement": "The same survey-native operator must satisfy leakage control, quotient descent, and response-unit normalization.",
            "current_evidence": f"survey_native_operator_constructed={gauge['survey_native_operator_constructed']}; operator_leakage_theorem_proven={gauge['operator_leakage_theorem_proven']}",
            "remaining_gap": "Construct or reject one operator before treating descent as proven.",
            "dimension_check": "The operator domain and codomain units must be explicit before descent can carry physical response.",
            "known_limit_check": "The operator must recover standard-lensing and pure-mask null limits when Tau residual channels are absent.",
            "computes_new_scores": "false",
            "uses_kids_data_vector_values": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(OUT, rows)

    open_blockers = sum(row["status"] == "OPEN_BLOCKER" for row in rows)
    summary = {
        "attempt_id": "KIDS1000_COSEBIS_GAUGE_QUOTIENT_DESCENT_CLOSURE_ATTEMPT_V1",
        "status": "GAUGE_QUOTIENT_DESCENT_CLOSURE_ATTEMPT_NARROWS_PROOF_NOT_PROVEN",
        "parent_joint_blocker": plan["next_parallel_proof_gate"],
        "descent_items": str(len(rows)),
        "available_limit_checks": "1",
        "open_blocker_count": str(open_blockers),
        "equivalence_classes_declared": gauge["equivalence_classes_declared"],
        "uniform_mask_offset_limit_available": gauge["uniform_mask_offset_limit_available"],
        "normalization_invariance_proven": gauge["normalization_invariance_proven"],
        "tile_relabeling_invariance_proven": gauge["tile_relabeling_invariance_proven"],
        "pure_mask_control_compatibility_proven": gauge["pure_mask_control_compatibility_proven"],
        "gauge_quotient_descent_proven": gauge["gauge_quotient_descent_proven"],
        "survey_native_operator_constructed": gauge["survey_native_operator_constructed"],
        "operator_leakage_theorem_proven": gauge["operator_leakage_theorem_proven"],
        "computes_new_scores": "false",
        "uses_kids_data_vector_values": "false",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "verdict": "GAUGE_QUOTIENT_DESCENT_CLOSURE_ATTEMPT_NARROWS_PROOF_BUT_THEOREM_REMAINS_OPEN",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(SUMMARY, [summary])

    DOC.write_text(
        "\n".join(
            [
                "# KiDS/COSEBIs gauge/quotient descent closure attempt v1",
                "",
                "**Doc class:** proof-blocker narrowing artifact",
                "**Status:** theorem not proven; no endpoint scoring; no validation claim",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`",
                "",
                "This note narrows the second KiDS/COSEBIs physical-promotion blocker:",
                "`B3_gauge_quotient_descent_open`. It does not close the blocker.",
                "",
                "Minimal target theorem:",
                "",
                "```text",
                "For any two admissible source representatives x and x' related by",
                "tile relabeling, source-basis recentering, admissible normalization,",
                "or gauge/null transformation, the future survey-native operator O_tau",
                "must satisfy [O_tau(x)] = [O_tau(x')] in the physical quotient.",
                "Pure-mask representatives must remain quotient-trivial or route to",
                "the same frozen null-control family.",
                "```",
                "",
                "Current status:",
                "",
                f"- equivalence classes declared: `{summary['equivalence_classes_declared']}`",
                f"- uniform mask-offset limit available: `{summary['uniform_mask_offset_limit_available']}`",
                f"- normalization invariance proven: `{summary['normalization_invariance_proven']}`",
                f"- tile relabeling invariance proven: `{summary['tile_relabeling_invariance_proven']}`",
                f"- pure-mask control compatibility proven: `{summary['pure_mask_control_compatibility_proven']}`",
                f"- survey-native operator constructed: `{summary['survey_native_operator_constructed']}`",
                f"- gauge quotient descent proven: `{summary['gauge_quotient_descent_proven']}`",
                f"- verdict: `{summary['verdict']}`",
                "",
                "Interpretation: the quotient-descent target is now explicit, but it",
                "still waits on a single operator that also closes leakage control and",
                "response-unit normalization. The KiDS block therefore remains caveated.",
                "",
            ]
        )
    )
    print(
        "KIDS1000_COSEBIS_GAUGE_QUOTIENT_DESCENT_CLOSURE_ATTEMPT_V1_BUILT "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKELETON = ROOT / "data/derived/kids1000_cosebis_survey_native_operator_construction_attempt_v1_summary.csv"
LEAKAGE = ROOT / "data/derived/kids1000_cosebis_operator_leakage_closure_attempt_v1_summary.csv"
GAUGE = ROOT / "data/derived/kids1000_cosebis_gauge_quotient_descent_closure_attempt_v1_summary.csv"
UNITS = ROOT / "data/derived/kids1000_cosebis_response_unit_normalization_closure_attempt_v1_summary.csv"
NULL = ROOT / "data/derived/kids1000_cosebis_standard_lensing_null_amplitude_closure_attempt_v1_summary.csv"
ORDER = ROOT / "data/derived/kids1000_cosebis_physical_promotion_dependency_order_v1_summary.csv"
PLAN = ROOT / "data/derived/joint_kids_caveated_block_resolution_plan_v1_summary.csv"
OUT = ROOT / "data/derived/kids1000_cosebis_survey_native_operator_theorem_closure_attempt_v1.csv"
SUMMARY = ROOT / "data/derived/kids1000_cosebis_survey_native_operator_theorem_closure_attempt_v1_summary.csv"
DOC = ROOT / "docs/kids1000_cosebis_survey_native_operator_theorem_closure_attempt_v1.md"
CLAIM_BOUNDARY = "kids1000_cosebis_survey_native_operator_theorem_closure_attempt_not_validation"


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
    skeleton = read_one(SKELETON)
    leakage = read_one(LEAKAGE)
    gauge = read_one(GAUGE)
    units = read_one(UNITS)
    null = read_one(NULL)
    order = read_one(ORDER)
    plan = read_one(PLAN)

    if skeleton["operator_skeleton_constructed"] != "true":
        raise SystemExit("survey-native skeleton must exist before theorem synthesis")
    for label, row, key in [
        ("skeleton", skeleton, "operator_theorem_proven"),
        ("leakage", leakage, "operator_leakage_theorem_proven"),
        ("gauge", gauge, "gauge_quotient_descent_proven"),
        ("units", units, "response_unit_normalization_derived"),
        ("null", null, "standard_lensing_null_amplitude_proven"),
        ("order", order, "physical_promotion_ready"),
        ("plan", plan, "can_promote_kids_block_to_clean_joint_support"),
    ]:
        if row[key] != "false":
            raise SystemExit(f"{label} unexpectedly closes {key}")

    rows = [
        {
            "attempt_id": "KIDS1000_COSEBIS_SURVEY_NATIVE_OPERATOR_THEOREM_CLOSURE_ATTEMPT_V1",
            "synthesis_item": "S1_factorized_skeleton_available",
            "status": "AVAILABLE_AS_SOURCE_SKELETON",
            "current_artifact": rel(SKELETON),
            "formal_requirement": "A retained COSEBIs-domain source-side operator skeleton must exist before a physical survey-native operator theorem can be attempted.",
            "current_evidence": f"operator_skeleton_constructed={skeleton['operator_skeleton_constructed']}; operator_rows={skeleton['operator_rows']}; mean_operator_kernel_value={skeleton['mean_operator_kernel_value']}",
            "remaining_gap": "The current object is a dimensionless source-side skeleton, not a physical survey-native operator theorem.",
            "dimension_check": "The kernel is dimensionless until a response-unit map is derived.",
            "known_limit_check": "Zero source mapping or zero response component remains a skeleton-level zero, not yet a physical no-Tau-source theorem.",
            "computes_new_scores": "false",
            "uses_kids_data_vector_values": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "attempt_id": "KIDS1000_COSEBIS_SURVEY_NATIVE_OPERATOR_THEOREM_CLOSURE_ATTEMPT_V1",
            "synthesis_item": "S2_leakage_closure_required",
            "status": "OPEN_BLOCKER",
            "current_artifact": rel(LEAKAGE),
            "formal_requirement": "Mask-only and null directions must either be quotient-trivial or routed into frozen null controls under the same operator.",
            "current_evidence": f"operator_leakage_theorem_proven={leakage['operator_leakage_theorem_proven']}; mask_quotient_triviality_proven={leakage['mask_quotient_triviality_proven']}; null_projection_condition_proven={leakage['null_projection_condition_proven']}",
            "remaining_gap": "Close the operator leakage theorem for the actual survey-native operator, not only for separate control artifacts.",
            "dimension_check": "Leakage control is not a unit derivation, but it determines whether the response class is physical.",
            "known_limit_check": "Uniform and pure-mask limits must not create positive Tau COSEBIs response.",
            "computes_new_scores": "false",
            "uses_kids_data_vector_values": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "attempt_id": "KIDS1000_COSEBIS_SURVEY_NATIVE_OPERATOR_THEOREM_CLOSURE_ATTEMPT_V1",
            "synthesis_item": "S3_gauge_quotient_descent_required",
            "status": "OPEN_BLOCKER",
            "current_artifact": rel(GAUGE),
            "formal_requirement": "Tile relabeling, source-basis recentering, admissible normalization changes, and gauge/null representatives must descend to the same quotient-visible response class.",
            "current_evidence": f"gauge_quotient_descent_proven={gauge['gauge_quotient_descent_proven']}; normalization_invariance_proven={gauge['normalization_invariance_proven']}; tile_relabeling_invariance_proven={gauge['tile_relabeling_invariance_proven']}",
            "remaining_gap": "Prove representative independence for the same operator that later receives physical units.",
            "dimension_check": "Representative changes must preserve both response class and later response units.",
            "known_limit_check": "Admissible source reparameterizations must not change physical COSEBIs response.",
            "computes_new_scores": "false",
            "uses_kids_data_vector_values": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "attempt_id": "KIDS1000_COSEBIS_SURVEY_NATIVE_OPERATOR_THEOREM_CLOSURE_ATTEMPT_V1",
            "synthesis_item": "S4_response_units_required",
            "status": "OPEN_BLOCKER",
            "current_artifact": rel(UNITS),
            "formal_requirement": "The operator must carry a source-side or theorem-side response-unit map from the dimensionless kernel into COSEBIs response units.",
            "current_evidence": f"response_unit_normalization_derived={units['response_unit_normalization_derived']}; physical_operator_units_derived={units['physical_operator_units_derived']}; covariance_metric_used_as_units_derivation={units['covariance_metric_used_as_units_derivation']}",
            "remaining_gap": "Derive the physical response-unit codomain independently of endpoint feedback and without treating covariance weighting as a unit map.",
            "dimension_check": "This is the explicit dimensional blocker: the current A_src K_i object is dimensionless.",
            "known_limit_check": "The same units must apply to candidate response and standard-lensing/no-Tau-source limits.",
            "computes_new_scores": "false",
            "uses_kids_data_vector_values": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "attempt_id": "KIDS1000_COSEBIS_SURVEY_NATIVE_OPERATOR_THEOREM_CLOSURE_ATTEMPT_V1",
            "synthesis_item": "S5_standard_null_required",
            "status": "OPEN_BLOCKER",
            "current_artifact": rel(NULL),
            "formal_requirement": "The no-Tau-source / standard-lensing limit must send the physical Tau contribution to zero or to the frozen null-control class.",
            "current_evidence": f"standard_lensing_null_amplitude_proven={null['standard_lensing_null_amplitude_proven']}; zero_tau_source_amplitude_statement_specified={null['zero_tau_source_amplitude_statement_specified']}; operator_null_safety_proven={null['operator_null_safety_proven']}",
            "remaining_gap": "Promote the specified zero-source statement into a theorem after leakage, gauge descent, null safety, and unit normalization are closed.",
            "dimension_check": "A physical zero-amplitude theorem is meaningful only after response units are fixed.",
            "known_limit_check": "Standard lensing must be recovered when Tau residual channels are absent.",
            "computes_new_scores": "false",
            "uses_kids_data_vector_values": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "attempt_id": "KIDS1000_COSEBIS_SURVEY_NATIVE_OPERATOR_THEOREM_CLOSURE_ATTEMPT_V1",
            "synthesis_item": "S6_single_operator_synthesis_required",
            "status": "OPEN_BLOCKER",
            "current_artifact": f"{rel(ORDER)};{rel(PLAN)}",
            "formal_requirement": "One and the same survey-native operator must satisfy leakage, quotient descent, response-unit, and standard-null conditions.",
            "current_evidence": f"operator_theorem_waits_for={order['operator_theorem_waits_for']}; physical_promotion_ready={order['physical_promotion_ready']}; can_promote_kids_block_to_clean_joint_support={plan['can_promote_kids_block_to_clean_joint_support']}",
            "remaining_gap": "The current evidence is a collection of narrowed blockers, not a single coherent physical operator theorem.",
            "dimension_check": "All four physical conditions must share one response-unit codomain.",
            "known_limit_check": "The same operator must recover the standard limit and retain the candidate response class.",
            "computes_new_scores": "false",
            "uses_kids_data_vector_values": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "attempt_id": "KIDS1000_COSEBIS_SURVEY_NATIVE_OPERATOR_THEOREM_CLOSURE_ATTEMPT_V1",
            "synthesis_item": "S7_no_endpoint_feedback",
            "status": "SATISFIED",
            "current_artifact": f"{rel(SKELETON)};{rel(LEAKAGE)};{rel(GAUGE)};{rel(UNITS)};{rel(NULL)}",
            "formal_requirement": "The theorem-synthesis attempt must not use KiDS data-vector values, endpoint scores, residuals, or posterior chains.",
            "current_evidence": "all imported closure summaries keep computes_new_scores=false, uses_kids_data_vector_values=false, endpoint_scoring_allowed=false, and endpoint_validation_claimed=false",
            "remaining_gap": "No leakage of endpoint data is detected here; the remaining gaps are physical proof gaps.",
            "dimension_check": "No observed COSEBIs response units or chi-square statistics enter this proof-blocker synthesis.",
            "known_limit_check": "The synthesis can be rebuilt without endpoint data.",
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
        "attempt_id": "KIDS1000_COSEBIS_SURVEY_NATIVE_OPERATOR_THEOREM_CLOSURE_ATTEMPT_V1",
        "status": "SURVEY_NATIVE_OPERATOR_THEOREM_CLOSURE_ATTEMPT_SYNTHESIZES_BLOCKERS_NOT_PROVEN",
        "parent_joint_blocker": "B1_survey_native_operator_theorem_open",
        "synthesis_items": str(len(rows)),
        "available_source_skeletons": "1",
        "open_blocker_count": str(open_blockers),
        "operator_skeleton_constructed": skeleton["operator_skeleton_constructed"],
        "survey_native_operator_constructed": skeleton["survey_native_operator_constructed"],
        "operator_theorem_proven": skeleton["operator_theorem_proven"],
        "operator_leakage_theorem_proven": leakage["operator_leakage_theorem_proven"],
        "gauge_quotient_descent_proven": gauge["gauge_quotient_descent_proven"],
        "response_unit_normalization_derived": units["response_unit_normalization_derived"],
        "standard_lensing_null_amplitude_proven": null["standard_lensing_null_amplitude_proven"],
        "physical_promotion_ready": order["physical_promotion_ready"],
        "can_promote_kids_block_to_clean_joint_support": plan["can_promote_kids_block_to_clean_joint_support"],
        "computes_new_scores": "false",
        "uses_kids_data_vector_values": "false",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "verdict": "SURVEY_NATIVE_OPERATOR_THEOREM_SYNTHESIS_HAS_SOURCE_SKELETON_BUT_PROOF_CHAIN_REMAINS_OPEN",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(SUMMARY, [summary])

    DOC.write_text(
        "\n".join(
            [
                "# KiDS/COSEBIs survey-native operator theorem closure attempt v1",
                "",
                "**Doc class:** proof-blocker synthesis artifact",
                "**Status:** survey-native physical operator theorem not proven; no endpoint scoring; no validation claim",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`",
                "",
                "This note synthesizes the KiDS/COSEBIs physical-promotion blocker",
                "`B1_survey_native_operator_theorem_open`. It does not close the",
                "blocker. It records that a factorized source-side skeleton exists,",
                "while the physical survey-native operator theorem remains open.",
                "",
                "Minimal target theorem:",
                "",
                "```text",
                "There exists one survey-native operator O_tau on the source-frozen",
                "KiDS/COSEBIs domain such that:",
                "  (i) it generates the retained COSEBIs response class,",
                "  (ii) mask-only directions are quotient-trivial or null-controlled,",
                "  (iii) admissible representatives descend to the same quotient class,",
                "  (iv) response units are derived independently of endpoint feedback",
                "       and independently of covariance weighting as a unit substitute,",
                "  (v) the no-Tau-source / standard-lensing limit gives zero Tau",
                "      contribution or the frozen null-control class.",
                "```",
                "",
                "Current status:",
                "",
                f"- operator skeleton constructed: `{summary['operator_skeleton_constructed']}`",
                f"- survey-native operator constructed: `{summary['survey_native_operator_constructed']}`",
                f"- operator theorem proven: `{summary['operator_theorem_proven']}`",
                f"- leakage theorem proven: `{summary['operator_leakage_theorem_proven']}`",
                f"- gauge quotient descent proven: `{summary['gauge_quotient_descent_proven']}`",
                f"- response-unit normalization derived: `{summary['response_unit_normalization_derived']}`",
                f"- standard-lensing null amplitude proven: `{summary['standard_lensing_null_amplitude_proven']}`",
                f"- physical promotion ready: `{summary['physical_promotion_ready']}`",
                f"- clean joint support promotion ready: `{summary['can_promote_kids_block_to_clean_joint_support']}`",
                f"- verdict: `{summary['verdict']}`",
                "",
                "Interpretation: B1 is stronger than the existence of a source-side",
                "operator skeleton. It requires one physical operator that survives",
                "leakage, quotient, unit, and standard-null tests simultaneously. Since",
                "B2--B5 remain open, the KiDS block remains caveated and cannot yet be",
                "promoted to clean joint support.",
                "",
            ]
        )
    )
    print(
        "KIDS1000_COSEBIS_SURVEY_NATIVE_OPERATOR_THEOREM_CLOSURE_ATTEMPT_V1_BUILT "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()

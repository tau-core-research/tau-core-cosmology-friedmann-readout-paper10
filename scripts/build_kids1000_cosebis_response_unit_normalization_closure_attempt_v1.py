#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQ = ROOT / "data/derived/kids1000_cosebis_response_unit_normalization_requirements_gate_v1_summary.csv"
UNITS = ROOT / "data/derived/kids1000_cosebis_physical_operator_units_gate_v1_summary.csv"
GAUGE = ROOT / "data/derived/kids1000_cosebis_gauge_quotient_descent_closure_attempt_v1_summary.csv"
LEAKAGE = ROOT / "data/derived/kids1000_cosebis_operator_leakage_closure_attempt_v1_summary.csv"
PLAN = ROOT / "data/derived/joint_kids_caveated_block_resolution_plan_v1_summary.csv"
OUT = ROOT / "data/derived/kids1000_cosebis_response_unit_normalization_closure_attempt_v1.csv"
SUMMARY = ROOT / "data/derived/kids1000_cosebis_response_unit_normalization_closure_attempt_v1_summary.csv"
DOC = ROOT / "docs/kids1000_cosebis_response_unit_normalization_closure_attempt_v1.md"
CLAIM_BOUNDARY = "kids1000_cosebis_response_unit_normalization_closure_attempt_not_validation"


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
    units = read_one(UNITS)
    gauge = read_one(GAUGE)
    leakage = read_one(LEAKAGE)
    plan = read_one(PLAN)

    if "B4_response_unit_normalization_open" not in Path(
        ROOT / "data/derived/joint_kids_caveated_block_resolution_plan_v1.csv"
    ).read_text():
        raise SystemExit("KiDS resolution plan does not carry B4")
    if req["response_unit_normalization_derived"] != "false":
        raise SystemExit("response-unit normalization must remain open")
    if units["physical_operator_units_derived"] != "false":
        raise SystemExit("physical operator units must remain open")
    if req["covariance_metric_used_as_units_derivation"] != "false":
        raise SystemExit("covariance metric must not be used as unit derivation")
    if gauge["gauge_quotient_descent_proven"] != "false":
        raise SystemExit("B4 closure must not inherit gauge descent")
    if leakage["operator_leakage_theorem_proven"] != "false":
        raise SystemExit("B4 closure must not inherit leakage theorem")
    if plan["can_promote_kids_block_to_clean_joint_support"] != "false":
        raise SystemExit("KiDS block must not be promoted")

    rows = [
        {
            "attempt_id": "KIDS1000_COSEBIS_RESPONSE_UNIT_NORMALIZATION_CLOSURE_ATTEMPT_V1",
            "unit_item": "U1_codomain_domain_match",
            "status": "AVAILABLE_AS_DOMAIN_LIMIT",
            "current_artifact": rel(REQ),
            "formal_requirement": "The response-unit map must act on the retained 300-row COSEBIs response codomain.",
            "current_evidence": f"cosebis_row_domain_available={req['cosebis_row_domain_available']}",
            "remaining_gap": "Domain matching is necessary but does not provide response units.",
            "dimension_check": "COSEBIs row matching defines codomain support, not the physical amplitude scale.",
            "known_limit_check": "A theory vector and data-vector domain must match before any null or Tau-response limit is meaningful.",
            "computes_new_scores": "false",
            "uses_kids_data_vector_values": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "attempt_id": "KIDS1000_COSEBIS_RESPONSE_UNIT_NORMALIZATION_CLOSURE_ATTEMPT_V1",
            "unit_item": "U2_dimensionless_kernel_identified",
            "status": "AVAILABLE_AS_SOURCE_LIMIT",
            "current_artifact": f"{rel(REQ)};{rel(UNITS)}",
            "formal_requirement": "The current source-side kernel and amplitude are dimensionless and therefore require a separate response-unit map.",
            "current_evidence": f"dimensionless_kernel_and_source_amplitude_available={req['dimensionless_kernel_and_source_amplitude_available']}; dimensionless_source_kernel_identified={units['dimensionless_source_kernel_identified']}",
            "remaining_gap": "Derive a physical map A_phys or operator units that converts the dimensionless source kernel into COSEBIs response units.",
            "dimension_check": "A_src K_i is dimensionless; the missing unit map must carry COSEBIs response units.",
            "known_limit_check": "Dimensionless normalization alone cannot create a physical Tau COSEBIs signal.",
            "computes_new_scores": "false",
            "uses_kids_data_vector_values": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "attempt_id": "KIDS1000_COSEBIS_RESPONSE_UNIT_NORMALIZATION_CLOSURE_ATTEMPT_V1",
            "unit_item": "U3_covariance_metric_separation",
            "status": "REQUIREMENT_FROZEN",
            "current_artifact": rel(REQ),
            "formal_requirement": "The covariance metric may score a future response vector but cannot define its physical units.",
            "current_evidence": f"covariance_metric_available={req['covariance_metric_available']}; covariance_metric_used_as_units_derivation={req['covariance_metric_used_as_units_derivation']}",
            "remaining_gap": "Keep likelihood/scoring metric separate from the source/theorem-side response-unit derivation.",
            "dimension_check": "Covariance readiness is a metric property, not a Tau source-unit derivation.",
            "known_limit_check": "A valid covariance does not imply a nonzero Tau response.",
            "computes_new_scores": "false",
            "uses_kids_data_vector_values": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "attempt_id": "KIDS1000_COSEBIS_RESPONSE_UNIT_NORMALIZATION_CLOSURE_ATTEMPT_V1",
            "unit_item": "U4_response_unit_map",
            "status": "OPEN_BLOCKER",
            "current_artifact": f"{rel(REQ)};{rel(UNITS)}",
            "formal_requirement": "A source-side or theorem-side physical derivation must supply the map from dimensionless source kernel to COSEBIs response units.",
            "current_evidence": f"response_unit_normalization_derived={req['response_unit_normalization_derived']}; physical_operator_units_derived={units['physical_operator_units_derived']}",
            "remaining_gap": "Derive or reject the physical unit map without endpoint residual, fit-statistic, or posterior feedback.",
            "dimension_check": "The map must convert dimensionless source factors into the same units as the retained COSEBIs response vector.",
            "known_limit_check": "The map must reduce to zero Tau response when the Tau source channel is absent.",
            "computes_new_scores": "false",
            "uses_kids_data_vector_values": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "attempt_id": "KIDS1000_COSEBIS_RESPONSE_UNIT_NORMALIZATION_CLOSURE_ATTEMPT_V1",
            "unit_item": "U5_null_limit_compatibility",
            "status": "OPEN_BLOCKER",
            "current_artifact": rel(REQ),
            "formal_requirement": "The response-unit map must be compatible with the standard-lensing/no-Tau-source null-amplitude theorem.",
            "current_evidence": f"standard_lensing_null_compatibility_proven={req['standard_lensing_null_compatibility_proven']}",
            "remaining_gap": "Prove the same units that scale the candidate also preserve the standard-lensing null limit.",
            "dimension_check": "Null-limit and unit-normalization statements must live in the same physical response space.",
            "known_limit_check": "Standard lensing must be recovered when Tau residual channels vanish.",
            "computes_new_scores": "false",
            "uses_kids_data_vector_values": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "attempt_id": "KIDS1000_COSEBIS_RESPONSE_UNIT_NORMALIZATION_CLOSURE_ATTEMPT_V1",
            "unit_item": "U6_dependency_on_B2_B3",
            "status": "OPEN_BLOCKER",
            "current_artifact": f"{rel(LEAKAGE)};{rel(GAUGE)}",
            "formal_requirement": "The response-unit theorem must attach units to the same operator class that satisfies leakage closure and gauge/quotient descent.",
            "current_evidence": f"operator_leakage_theorem_proven={leakage['operator_leakage_theorem_proven']}; gauge_quotient_descent_proven={gauge['gauge_quotient_descent_proven']}",
            "remaining_gap": "Do not attach physical units to an operator class that can still leak mask/gauge representatives into the physical quotient.",
            "dimension_check": "Physical units cannot rescue an operator whose quotient class is not well-defined.",
            "known_limit_check": "Leakage-safe and gauge-safe null limits must survive before unit promotion.",
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
        "attempt_id": "KIDS1000_COSEBIS_RESPONSE_UNIT_NORMALIZATION_CLOSURE_ATTEMPT_V1",
        "status": "RESPONSE_UNIT_NORMALIZATION_CLOSURE_ATTEMPT_NARROWS_PROOF_NOT_DERIVED",
        "parent_joint_blocker": "B4_response_unit_normalization_open",
        "unit_items": str(len(rows)),
        "available_domain_or_source_checks": "2",
        "open_blocker_count": str(open_blockers),
        "cosebis_row_domain_available": req["cosebis_row_domain_available"],
        "dimensionless_kernel_and_source_amplitude_available": req["dimensionless_kernel_and_source_amplitude_available"],
        "covariance_metric_available": req["covariance_metric_available"],
        "covariance_metric_used_as_units_derivation": req["covariance_metric_used_as_units_derivation"],
        "response_unit_normalization_derived": req["response_unit_normalization_derived"],
        "physical_operator_units_derived": units["physical_operator_units_derived"],
        "standard_lensing_null_compatibility_proven": req["standard_lensing_null_compatibility_proven"],
        "operator_leakage_theorem_proven": leakage["operator_leakage_theorem_proven"],
        "gauge_quotient_descent_proven": gauge["gauge_quotient_descent_proven"],
        "computes_new_scores": "false",
        "uses_kids_data_vector_values": "false",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "verdict": "RESPONSE_UNIT_NORMALIZATION_CLOSURE_ATTEMPT_NARROWS_PROOF_BUT_UNITS_REMAIN_OPEN",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(SUMMARY, [summary])

    DOC.write_text(
        "\n".join(
            [
                "# KiDS/COSEBIs response-unit normalization closure attempt v1",
                "",
                "**Doc class:** proof-blocker narrowing artifact",
                "**Status:** unit map not derived; no endpoint scoring; no validation claim",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`",
                "",
                "This note narrows the third KiDS/COSEBIs physical-promotion blocker:",
                "`B4_response_unit_normalization_open`. It does not derive the missing",
                "response-unit map.",
                "",
                "Minimal target theorem:",
                "",
                "```text",
                "A source-side or theorem-side map U_tau must convert the dimensionless",
                "source kernel A_src K_i into the retained COSEBIs response codomain,",
                "without using endpoint residuals, fit statistics, posterior feedback,",
                "or the covariance metric as a unit derivation. The same U_tau must",
                "preserve the standard-lensing/no-Tau-source null limit and must attach",
                "only to an operator class that has passed leakage and gauge/quotient",
                "descent.",
                "```",
                "",
                "Current status:",
                "",
                f"- COSEBIs row domain available: `{summary['cosebis_row_domain_available']}`",
                f"- dimensionless kernel/source amplitude available: `{summary['dimensionless_kernel_and_source_amplitude_available']}`",
                f"- covariance metric available: `{summary['covariance_metric_available']}`",
                f"- covariance metric used as units derivation: `{summary['covariance_metric_used_as_units_derivation']}`",
                f"- response-unit normalization derived: `{summary['response_unit_normalization_derived']}`",
                f"- physical operator units derived: `{summary['physical_operator_units_derived']}`",
                f"- standard-lensing null compatibility proven: `{summary['standard_lensing_null_compatibility_proven']}`",
                f"- leakage theorem proven: `{summary['operator_leakage_theorem_proven']}`",
                f"- gauge quotient descent proven: `{summary['gauge_quotient_descent_proven']}`",
                f"- verdict: `{summary['verdict']}`",
                "",
                "Interpretation: Paper 10 has a reproducible response domain and a",
                "dimensionless source-side kernel, but not yet a physical COSEBIs",
                "response-unit theorem. The KiDS block therefore remains caveated.",
                "",
            ]
        )
    )
    print(
        "KIDS1000_COSEBIS_RESPONSE_UNIT_NORMALIZATION_CLOSURE_ATTEMPT_V1_BUILT "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()

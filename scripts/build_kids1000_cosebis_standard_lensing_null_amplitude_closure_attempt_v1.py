#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NULL_REQ = ROOT / "data/derived/kids1000_cosebis_standard_lensing_null_amplitude_theorem_requirements_v1_summary.csv"
UNIT = ROOT / "data/derived/kids1000_cosebis_response_unit_normalization_closure_attempt_v1_summary.csv"
GAUGE = ROOT / "data/derived/kids1000_cosebis_gauge_quotient_descent_closure_attempt_v1_summary.csv"
LEAKAGE = ROOT / "data/derived/kids1000_cosebis_operator_leakage_closure_attempt_v1_summary.csv"
OP_NULL = ROOT / "data/derived/kids1000_cosebis_operator_null_safety_gate_v1_summary.csv"
PLAN = ROOT / "data/derived/joint_kids_caveated_block_resolution_plan_v1_summary.csv"
OUT = ROOT / "data/derived/kids1000_cosebis_standard_lensing_null_amplitude_closure_attempt_v1.csv"
SUMMARY = ROOT / "data/derived/kids1000_cosebis_standard_lensing_null_amplitude_closure_attempt_v1_summary.csv"
DOC = ROOT / "docs/kids1000_cosebis_standard_lensing_null_amplitude_closure_attempt_v1.md"
CLAIM_BOUNDARY = "kids1000_cosebis_standard_lensing_null_amplitude_closure_attempt_not_validation"


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
    null_req = read_one(NULL_REQ)
    unit = read_one(UNIT)
    gauge = read_one(GAUGE)
    leakage = read_one(LEAKAGE)
    op_null = read_one(OP_NULL)
    read_one(PLAN)

    if null_req["standard_lensing_null_amplitude_proven"] != "false":
        raise SystemExit("null-amplitude theorem must remain open")
    if unit["response_unit_normalization_derived"] != "false":
        raise SystemExit("null-amplitude closure must not inherit response units")
    if gauge["gauge_quotient_descent_proven"] != "false":
        raise SystemExit("null-amplitude closure must not inherit gauge descent")
    if leakage["operator_leakage_theorem_proven"] != "false":
        raise SystemExit("null-amplitude closure must not inherit leakage theorem")
    if op_null["operator_null_safety_proven"] != "false":
        raise SystemExit("null-amplitude closure must not inherit operator null safety")

    rows = [
        {
            "attempt_id": "KIDS1000_COSEBIS_STANDARD_LENSING_NULL_AMPLITUDE_CLOSURE_ATTEMPT_V1",
            "null_item": "N1_null_controls_available",
            "status": "AVAILABLE_AS_CONTROL_LIMIT",
            "current_artifact": rel(NULL_REQ),
            "formal_requirement": "Source-replayed null controls may bound control behavior but cannot be fitted into a positive physical Tau response.",
            "current_evidence": f"null_controls_available_as_control_limit={null_req['null_controls_available_as_control_limit']}",
            "remaining_gap": "Lift null-control availability into a theorem about the physical operator, rather than a replay artifact.",
            "dimension_check": "Control-limit artifacts are dimensionless theory-vector shells, not physical amplitudes.",
            "known_limit_check": "Null controls must remain controls when Tau source is absent.",
            "computes_new_scores": "false",
            "uses_kids_data_vector_values": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "attempt_id": "KIDS1000_COSEBIS_STANDARD_LENSING_NULL_AMPLITUDE_CLOSURE_ATTEMPT_V1",
            "null_item": "N2_zero_tau_source_statement",
            "status": "SPECIFIED_NOT_DERIVED",
            "current_artifact": rel(NULL_REQ),
            "formal_requirement": "When the Tau residual source is zero, the physical Tau contribution must vanish or remain inside the frozen null-control response class.",
            "current_evidence": f"zero_tau_source_amplitude_statement_specified={null_req['zero_tau_source_amplitude_statement_specified']}",
            "remaining_gap": "Prove the zero-source statement in the same physical response space as the future unit map.",
            "dimension_check": "A zero-amplitude statement is physical only after response units are derived.",
            "known_limit_check": "Standard lensing must be recovered when Tau residual channels are absent.",
            "computes_new_scores": "false",
            "uses_kids_data_vector_values": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "attempt_id": "KIDS1000_COSEBIS_STANDARD_LENSING_NULL_AMPLITUDE_CLOSURE_ATTEMPT_V1",
            "null_item": "N3_operator_null_safety",
            "status": "OPEN_BLOCKER",
            "current_artifact": rel(OP_NULL),
            "formal_requirement": "The same operator must kill or control pure null, mask, and wrong-channel directions before null amplitude can be physical.",
            "current_evidence": f"operator_null_safety_proven={op_null['operator_null_safety_proven']}; mask_null_operator_proven={op_null['mask_null_operator_proven']}; spectrum_null_coupling_proven={op_null['spectrum_null_coupling_proven']}",
            "remaining_gap": "Prove operator-level null safety rather than relying on deterministic control replays.",
            "dimension_check": "Null safety must be established before attaching physical response units.",
            "known_limit_check": "Mask/wrong-channel perturbations must not create positive Tau COSEBIs response.",
            "computes_new_scores": "false",
            "uses_kids_data_vector_values": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "attempt_id": "KIDS1000_COSEBIS_STANDARD_LENSING_NULL_AMPLITUDE_CLOSURE_ATTEMPT_V1",
            "null_item": "N4_response_unit_dependency",
            "status": "OPEN_BLOCKER",
            "current_artifact": rel(UNIT),
            "formal_requirement": "The standard-lensing null amplitude must be stated after, and in the same units as, the response-unit normalization theorem.",
            "current_evidence": f"response_unit_normalization_derived={unit['response_unit_normalization_derived']}; physical_operator_units_derived={unit['physical_operator_units_derived']}",
            "remaining_gap": "Do not claim a physical zero-amplitude theorem before the physical response-unit map exists.",
            "dimension_check": "Null amplitude and positive candidate amplitude must share the same response-unit codomain.",
            "known_limit_check": "No-Tau-source limit must remain zero under the same units used for the candidate.",
            "computes_new_scores": "false",
            "uses_kids_data_vector_values": "false",
            "endpoint_scoring_allowed": "false",
            "endpoint_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "attempt_id": "KIDS1000_COSEBIS_STANDARD_LENSING_NULL_AMPLITUDE_CLOSURE_ATTEMPT_V1",
            "null_item": "N5_leakage_and_gauge_dependency",
            "status": "OPEN_BLOCKER",
            "current_artifact": f"{rel(LEAKAGE)};{rel(GAUGE)}",
            "formal_requirement": "No mask leakage or gauge representative may enter the physical zero-Tau response class as a positive residual.",
            "current_evidence": f"operator_leakage_theorem_proven={leakage['operator_leakage_theorem_proven']}; gauge_quotient_descent_proven={gauge['gauge_quotient_descent_proven']}",
            "remaining_gap": "Close B2 and B3 before using standard-lensing null amplitude as a physical promotion theorem.",
            "dimension_check": "Leakage and gauge risks are not physical response units but can invalidate the response class.",
            "known_limit_check": "Uniform mask and quotient-trivial representatives must stay null in the standard-lensing limit.",
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
        "attempt_id": "KIDS1000_COSEBIS_STANDARD_LENSING_NULL_AMPLITUDE_CLOSURE_ATTEMPT_V1",
        "status": "STANDARD_LENSING_NULL_AMPLITUDE_CLOSURE_ATTEMPT_NARROWS_PROOF_NOT_PROVEN",
        "parent_joint_blocker": "B5_standard_lensing_null_amplitude_theorem_open",
        "null_items": str(len(rows)),
        "available_control_limits": "1",
        "specified_not_derived_items": "1",
        "open_blocker_count": str(open_blockers),
        "null_controls_available_as_control_limit": null_req["null_controls_available_as_control_limit"],
        "zero_tau_source_amplitude_statement_specified": null_req["zero_tau_source_amplitude_statement_specified"],
        "standard_lensing_null_amplitude_proven": null_req["standard_lensing_null_amplitude_proven"],
        "operator_null_safety_proven": op_null["operator_null_safety_proven"],
        "response_unit_normalization_derived": unit["response_unit_normalization_derived"],
        "operator_leakage_theorem_proven": leakage["operator_leakage_theorem_proven"],
        "gauge_quotient_descent_proven": gauge["gauge_quotient_descent_proven"],
        "computes_new_scores": "false",
        "uses_kids_data_vector_values": "false",
        "endpoint_scoring_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "cosmological_validation_claimed": "false",
        "verdict": "STANDARD_LENSING_NULL_AMPLITUDE_CLOSURE_ATTEMPT_NARROWS_PROOF_BUT_THEOREM_REMAINS_OPEN",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(SUMMARY, [summary])

    DOC.write_text(
        "\n".join(
            [
                "# KiDS/COSEBIs standard-lensing null-amplitude closure attempt v1",
                "",
                "**Doc class:** proof-blocker narrowing artifact",
                "**Status:** null-amplitude theorem not proven; no endpoint scoring; no validation claim",
                f"**Claim boundary:** `{CLAIM_BOUNDARY}`",
                "",
                "This note narrows the fourth KiDS/COSEBIs physical-promotion blocker:",
                "`B5_standard_lensing_null_amplitude_theorem_open`. It does not prove",
                "the standard-lensing/no-Tau-source null-amplitude theorem.",
                "",
                "Minimal target theorem:",
                "",
                "```text",
                "In the physical COSEBIs response space, after response units are",
                "derived and after leakage/gauge/null safety have been proven, setting",
                "the Tau residual source to zero must send the Tau contribution to zero",
                "or to the frozen null-control class. Thus the standard-lensing",
                "baseline is recovered and no positive Tau COSEBIs amplitude is created",
                "from null, mask, wrong-channel, or gauge representatives.",
                "```",
                "",
                "Current status:",
                "",
                f"- null controls available as control limit: `{summary['null_controls_available_as_control_limit']}`",
                f"- zero-Tau-source statement specified: `{summary['zero_tau_source_amplitude_statement_specified']}`",
                f"- standard-lensing null amplitude proven: `{summary['standard_lensing_null_amplitude_proven']}`",
                f"- operator null safety proven: `{summary['operator_null_safety_proven']}`",
                f"- response-unit normalization derived: `{summary['response_unit_normalization_derived']}`",
                f"- leakage theorem proven: `{summary['operator_leakage_theorem_proven']}`",
                f"- gauge quotient descent proven: `{summary['gauge_quotient_descent_proven']}`",
                f"- verdict: `{summary['verdict']}`",
                "",
                "Interpretation: null controls and a zero-source requirement exist, but",
                "the physical theorem remains blocked by unit normalization, operator",
                "null safety, leakage control, and gauge/quotient descent. The KiDS",
                "block therefore remains caveated.",
                "",
            ]
        )
    )
    print(
        "KIDS1000_COSEBIS_STANDARD_LENSING_NULL_AMPLITUDE_CLOSURE_ATTEMPT_V1_BUILT "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()

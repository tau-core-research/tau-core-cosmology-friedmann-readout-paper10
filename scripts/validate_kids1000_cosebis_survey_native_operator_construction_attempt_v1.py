#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_survey_native_operator_construction_attempt_policy_v1.csv"
OPERATOR = ROOT / "data" / "derived" / "kids1000_cosebis_survey_native_operator_construction_attempt_v1.csv"
LEDGER = ROOT / "data" / "derived" / "kids1000_cosebis_survey_native_operator_construction_attempt_v1_ledger.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_survey_native_operator_construction_attempt_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    policy = read_one(POLICY)
    summary = read_one(SUMMARY)
    operator_rows = read_rows(OPERATOR)
    ledger = read_rows(LEDGER)

    if policy["status"] != "SURVEY_NATIVE_OPERATOR_CONSTRUCTION_ATTEMPT_POLICY_FROZEN":
        raise SystemExit("unexpected operator construction attempt policy status")
    for key in [
        "uses_kids_data_vector_values",
        "uses_fit_statistics",
        "uses_random_noise",
        "endpoint_scoring_allowed",
    ]:
        if policy[key] != "false":
            raise SystemExit(f"policy {key} must be false")
    if summary["status"] != "SURVEY_NATIVE_OPERATOR_SKELETON_CONSTRUCTED_THEOREM_OPEN":
        raise SystemExit("unexpected operator construction summary status")
    if summary["verdict"] != "factorized_source_side_operator_skeleton_exists_but_operator_theorem_remains_open":
        raise SystemExit("unexpected operator construction verdict")
    if summary["operator_rows"] != "300" or len(operator_rows) != 300:
        raise SystemExit("expected 300 operator rows")
    if summary["ledger_rows"] != "6" or len(ledger) != 6:
        raise SystemExit("expected six ledger rows")
    if summary["satisfied_count"] != "1":
        raise SystemExit("expected one satisfied no-endpoint row")
    if summary["satisfied_caveated_count"] != "2":
        raise SystemExit("expected two caveated construction rows")
    if summary["open_blocker_count"] != "3":
        raise SystemExit("expected three open blockers")
    if summary["operator_skeleton_constructed"] != "true":
        raise SystemExit("operator skeleton must be constructed")
    for key in [
        "survey_native_operator_constructed",
        "operator_theorem_proven",
        "operator_leakage_theorem_proven",
        "mask_leakage_theorem_proven",
        "gauge_quotient_descent_proven",
        "physical_operator_units_derived",
        "mode_response_operator_derived",
    ]:
        if summary[key] != "false":
            raise SystemExit(f"summary {key} must remain false")
    if summary["contains_theory_vector"] != "true":
        raise SystemExit("operator skeleton should contain the source-side unit-amplitude theory kernel")
    for key in [
        "contains_predictions",
        "contains_residuals",
        "contains_fit_statistics",
        "uses_kids_data_vector_values",
        "uses_posterior_chains",
        "uses_random_noise",
        "endpoint_scoring_allowed",
        "endpoint_validation_claimed",
    ]:
        if summary[key] != "false":
            raise SystemExit(f"summary {key} must be false")

    by_gate = {row["gate_id"]: row for row in ledger}
    expected = {
        "O1_domain_codomain_available",
        "O2_factorized_operator_skeleton_constructed",
        "O3_mask_leakage_theorem_open",
        "O4_gauge_quotient_descent_open",
        "O5_no_endpoint_feedback",
        "O6_physical_operator_units_open",
    }
    if set(by_gate) != expected:
        raise SystemExit("unexpected operator construction ledger ids")
    if by_gate["O1_domain_codomain_available"]["status"] != "SATISFIED_CAVEATED":
        raise SystemExit("domain/codomain row must be caveated")
    if by_gate["O2_factorized_operator_skeleton_constructed"]["status"] != "SATISFIED_CAVEATED":
        raise SystemExit("operator skeleton row must be caveated")
    if by_gate["O5_no_endpoint_feedback"]["status"] != "SATISFIED":
        raise SystemExit("no-endpoint row must pass")
    for gate_id in [
        "O3_mask_leakage_theorem_open",
        "O4_gauge_quotient_descent_open",
        "O6_physical_operator_units_open",
    ]:
        if by_gate[gate_id]["status"] != "OPEN_BLOCKER":
            raise SystemExit(f"{gate_id} must remain an open blocker")
    for row in ledger:
        if row["claim_boundary"] != policy["claim_boundary"]:
            raise SystemExit("ledger claim boundary mismatch")
        if not row["dimension_check"]:
            raise SystemExit("missing dimension check")
        if not row["known_limit_check"]:
            raise SystemExit("missing known-limit check")
    for row in operator_rows:
        value = float(row["operator_kernel_value"])
        expected_value = float(row["source_mapping_component"]) * float(row["mode_response_component"])
        if abs(value - expected_value) > 1.0e-10:
            raise SystemExit("operator kernel value must equal mapping times mode response")
        if row["operator_skeleton_constructed"] != "true":
            raise SystemExit("operator skeleton flag must be true")
        for key in [
            "operator_theorem_proven",
            "mask_leakage_theorem_proven",
            "gauge_quotient_descent_proven",
            "contains_predictions",
            "contains_residuals",
            "contains_fit_statistics",
            "uses_kids_data_vector_values",
            "uses_posterior_chains",
            "uses_random_noise",
            "endpoint_scoring_allowed",
            "endpoint_validation_claimed",
        ]:
            if row[key] != "false":
                raise SystemExit(f"operator row {key} must be false")
    print(
        "PAPER10_KIDS1000_COSEBIS_SURVEY_NATIVE_OPERATOR_CONSTRUCTION_ATTEMPT_V1_VALIDATED "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()

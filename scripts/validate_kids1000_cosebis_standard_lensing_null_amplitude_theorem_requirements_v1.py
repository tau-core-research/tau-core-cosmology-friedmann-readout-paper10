#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_standard_lensing_null_amplitude_theorem_requirements_policy_v1.csv"
LEDGER = ROOT / "data" / "derived" / "kids1000_cosebis_standard_lensing_null_amplitude_theorem_requirements_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_standard_lensing_null_amplitude_theorem_requirements_v1_summary.csv"


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
    ledger = read_rows(LEDGER)

    if policy["status"] != "STANDARD_LENSING_NULL_AMPLITUDE_THEOREM_REQUIREMENTS_POLICY_FROZEN":
        raise SystemExit("unexpected null-amplitude theorem requirements policy status")
    for key in ["uses_kids_data_vector_values", "uses_fit_statistics", "uses_random_noise", "endpoint_scoring_allowed"]:
        if policy[key] != "false":
            raise SystemExit(f"policy {key} must be false")
    if summary["status"] != "STANDARD_LENSING_NULL_AMPLITUDE_THEOREM_REQUIREMENTS_FROZEN_NOT_PROVEN":
        raise SystemExit("unexpected null-amplitude theorem requirements status")
    if summary["verdict"] != "standard_lensing_null_amplitude_requirements_frozen_but_theorem_remains_open":
        raise SystemExit("unexpected null-amplitude theorem requirements verdict")
    if summary["requirement_rows"] != "6":
        raise SystemExit("unexpected null-amplitude requirement row count")
    if summary["satisfied_count"] != "1":
        raise SystemExit("expected one no-endpoint satisfied row")
    if summary["satisfied_as_control_limit_count"] != "1":
        raise SystemExit("expected one control-limit row")
    if summary["specified_not_derived_count"] != "1":
        raise SystemExit("expected one specified-not-derived row")
    if summary["open_blocker_count"] != "3":
        raise SystemExit("expected three open blockers")
    if summary["null_controls_available_as_control_limit"] != "true":
        raise SystemExit("null controls should be available as control limit")
    if summary["zero_tau_source_amplitude_statement_specified"] != "true":
        raise SystemExit("zero Tau source statement should be specified")
    for key in [
        "standard_lensing_null_amplitude_proven",
        "operator_null_safety_proven",
        "gauge_quotient_descent_proven",
        "operator_leakage_theorem_proven",
        "physical_amplitude_units_derived",
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

    expected = {
        "Z1_source_replayed_null_controls_available": "SATISFIED_AS_CONTROL_LIMIT",
        "Z2_zero_tau_source_amplitude_statement": "SPECIFIED_NOT_DERIVED",
        "Z3_operator_null_safety_required": "OPEN_BLOCKER",
        "Z4_gauge_quotient_descent_required": "OPEN_BLOCKER",
        "Z5_leakage_theorem_required": "OPEN_BLOCKER",
        "Z6_no_endpoint_feedback": "SATISFIED",
    }
    by_req = {row["requirement_id"]: row for row in ledger}
    for requirement_id, status in expected.items():
        if by_req[requirement_id]["status"] != status:
            raise SystemExit(f"{requirement_id} must have status {status}")
    for row in ledger:
        if row["claim_boundary"] != policy["claim_boundary"]:
            raise SystemExit("claim boundary mismatch")
        if not row["dimension_check"]:
            raise SystemExit("missing dimension check")
        if not row["known_limit_check"]:
            raise SystemExit("missing known-limit check")
    print(
        "PAPER10_KIDS1000_COSEBIS_STANDARD_LENSING_NULL_AMPLITUDE_THEOREM_REQUIREMENTS_V1_VALIDATED "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()

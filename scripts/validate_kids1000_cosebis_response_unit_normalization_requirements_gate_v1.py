#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_response_unit_normalization_requirements_gate_policy_v1.csv"
LEDGER = ROOT / "data" / "derived" / "kids1000_cosebis_response_unit_normalization_requirements_gate_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_response_unit_normalization_requirements_gate_v1_summary.csv"


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
    rows = read_rows(LEDGER)

    if policy["status"] != "RESPONSE_UNIT_NORMALIZATION_REQUIREMENTS_GATE_POLICY_FROZEN":
        raise SystemExit("unexpected response-unit normalization policy status")
    for key in ["uses_kids_data_vector_values", "uses_fit_statistics", "uses_random_noise", "endpoint_scoring_allowed"]:
        if policy[key] != "false":
            raise SystemExit(f"policy {key} must be false")
    if summary["status"] != "RESPONSE_UNIT_NORMALIZATION_REQUIREMENTS_FROZEN_NOT_DERIVED":
        raise SystemExit("unexpected response-unit normalization summary status")
    if summary["verdict"] != "cosebis_response_unit_requirements_frozen_but_normalization_remains_open":
        raise SystemExit("unexpected response-unit normalization verdict")
    if summary["gate_rows"] != "6":
        raise SystemExit("unexpected response-unit ledger row count")
    if summary["satisfied_count"] != "1":
        raise SystemExit("expected one no-endpoint satisfied row")
    if summary["satisfied_as_domain_limit_count"] != "1":
        raise SystemExit("expected one domain-limit row")
    if summary["satisfied_as_source_limit_count"] != "1":
        raise SystemExit("expected one source-limit row")
    if summary["requirement_frozen_count"] != "1":
        raise SystemExit("expected one frozen covariance requirement row")
    if summary["open_blocker_count"] != "2":
        raise SystemExit("expected two open blockers")
    for key in [
        "cosebis_row_domain_available",
        "dimensionless_kernel_and_source_amplitude_available",
        "covariance_metric_available",
    ]:
        if summary[key] != "true":
            raise SystemExit(f"summary {key} must be true")
    for key in [
        "covariance_metric_used_as_units_derivation",
        "response_unit_normalization_derived",
        "physical_amplitude_units_derived",
        "standard_lensing_null_compatibility_proven",
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
        "R1_cosebis_row_domain_available": "SATISFIED_AS_DOMAIN_LIMIT",
        "R2_dimensionless_kernel_and_source_amplitude_available": "SATISFIED_AS_SOURCE_LIMIT",
        "R3_covariance_metric_available_not_units": "REQUIREMENT_FROZEN",
        "R4_response_unit_map_not_derived": "OPEN_BLOCKER",
        "R5_standard_lensing_null_compatibility_required": "OPEN_BLOCKER",
        "R6_no_endpoint_feedback": "SATISFIED",
    }
    by_gate = {row["gate_id"]: row for row in rows}
    for gate_id, status in expected.items():
        if by_gate[gate_id]["status"] != status:
            raise SystemExit(f"{gate_id} must have status {status}")
    for row in rows:
        if row["claim_boundary"] != policy["claim_boundary"]:
            raise SystemExit("claim boundary mismatch")
        if not row["dimension_check"]:
            raise SystemExit("missing dimension check")
        if not row["known_limit_check"]:
            raise SystemExit("missing known-limit check")
    print(
        "PAPER10_KIDS1000_COSEBIS_RESPONSE_UNIT_NORMALIZATION_REQUIREMENTS_GATE_V1_VALIDATED "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()

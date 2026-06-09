#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_physical_amplitude_requirements_gate_policy_v1.csv"
LEDGER = ROOT / "data" / "derived" / "kids1000_cosebis_physical_amplitude_requirements_gate_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_physical_amplitude_requirements_gate_v1_summary.csv"


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

    if policy["status"] != "PHYSICAL_AMPLITUDE_REQUIREMENTS_GATE_POLICY_FROZEN":
        raise SystemExit("unexpected physical amplitude requirements policy status")
    for key in ["uses_kids_data_vector_values", "uses_fit_statistics", "uses_random_noise", "endpoint_scoring_allowed"]:
        if policy[key] != "false":
            raise SystemExit(f"policy {key} must be false")
    if summary["status"] != "PHYSICAL_AMPLITUDE_REQUIREMENTS_FROZEN_NOT_DERIVED":
        raise SystemExit("unexpected physical amplitude requirements status")
    if summary["verdict"] != "dimensionless_source_amplitude_available_but_physical_response_amplitude_remains_open":
        raise SystemExit("unexpected physical amplitude requirements verdict")
    if summary["gate_rows"] != "5":
        raise SystemExit("unexpected physical amplitude ledger row count")
    if summary["satisfied_count"] != "1":
        raise SystemExit("expected one satisfied no-endpoint row")
    if summary["satisfied_as_source_limit_count"] != "1":
        raise SystemExit("expected one source-limit row")
    if summary["requirement_frozen_count"] != "1":
        raise SystemExit("expected one frozen covariance requirement row")
    if summary["open_blocker_count"] != "2":
        raise SystemExit("expected two open blockers")
    if summary["dimensionless_source_amplitude_available"] != "true":
        raise SystemExit("dimensionless source amplitude should be available")
    if summary["dimensionless_amplitude_value"] != "1.000000000000e+00":
        raise SystemExit("dimensionless source amplitude must be one")
    for key in [
        "physical_amplitude_units_derived",
        "response_unit_normalization_derived",
        "standard_lensing_null_amplitude_proven",
        "covariance_metric_used_as_amplitude_derivation",
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
        "P1_dimensionless_source_amplitude_available": "SATISFIED_AS_SOURCE_LIMIT",
        "P2_response_unit_normalization_required": "OPEN_BLOCKER",
        "P3_standard_lensing_null_amplitude_required": "OPEN_BLOCKER",
        "P4_covariance_metric_not_amplitude_derivation": "REQUIREMENT_FROZEN",
        "P5_no_endpoint_feedback": "SATISFIED",
    }
    for gate_id, status in expected.items():
        if by_gate[gate_id]["status"] != status:
            raise SystemExit(f"{gate_id} must have status {status}")
    for row in ledger:
        if row["claim_boundary"] != policy["claim_boundary"]:
            raise SystemExit("claim boundary mismatch")
        if not row["dimension_check"]:
            raise SystemExit("missing dimension check")
        if not row["known_limit_check"]:
            raise SystemExit("missing known-limit check")
    print(
        "PAPER10_KIDS1000_COSEBIS_PHYSICAL_AMPLITUDE_REQUIREMENTS_GATE_V1_VALIDATED "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()

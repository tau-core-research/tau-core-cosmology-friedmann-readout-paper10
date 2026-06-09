#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_physical_operator_units_gate_policy_v1.csv"
LEDGER = ROOT / "data" / "derived" / "kids1000_cosebis_physical_operator_units_gate_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_physical_operator_units_gate_v1_summary.csv"


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

    if policy["status"] != "PHYSICAL_OPERATOR_UNITS_GATE_POLICY_FROZEN":
        raise SystemExit("unexpected physical operator units policy status")
    for key in [
        "uses_kids_data_vector_values",
        "uses_fit_statistics",
        "uses_random_noise",
        "endpoint_scoring_allowed",
    ]:
        if policy[key] != "false":
            raise SystemExit(f"policy {key} must be false")
    if summary["status"] != "PHYSICAL_OPERATOR_UNITS_REQUIREMENTS_FROZEN_NOT_DERIVED":
        raise SystemExit("unexpected units gate summary status")
    if summary["verdict"] != "dimensionless_operator_kernel_identified_but_physical_units_and_amplitude_remain_open":
        raise SystemExit("unexpected units gate verdict")
    if summary["gate_rows"] != "6" or len(rows) != 6:
        raise SystemExit("expected six units gate rows")
    if summary["satisfied_count"] != "1":
        raise SystemExit("expected one satisfied no-endpoint row")
    if summary["satisfied_as_source_limit_count"] != "1":
        raise SystemExit("expected one source-limit row")
    if summary["requirement_frozen_count"] != "2":
        raise SystemExit("expected two frozen requirements")
    if summary["open_blocker_count"] != "2":
        raise SystemExit("expected two open blockers")
    if summary["dimensionless_source_kernel_identified"] != "true":
        raise SystemExit("dimensionless source kernel should be identified")
    if summary["covariance_metric_available"] != "true":
        raise SystemExit("covariance metric should be available")
    for key in [
        "physical_operator_units_derived",
        "source_side_amplitude_map_derived",
        "standard_lensing_null_normalization_proven",
        "covariance_metric_used_as_units_derivation",
        "contains_theory_vector",
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
    by_gate = {row["gate_id"]: row for row in rows}
    expected = {
        "U1_dimensionless_source_kernel_identified",
        "U2_cosebis_response_units_need_derivation",
        "U3_amplitude_map_not_derived",
        "U4_standard_lensing_null_normalization_open",
        "U5_covariance_metric_not_units_derivation",
        "U6_no_endpoint_feedback",
    }
    if set(by_gate) != expected:
        raise SystemExit("unexpected units gate ids")
    if by_gate["U1_dimensionless_source_kernel_identified"]["status"] != "SATISFIED_AS_SOURCE_LIMIT":
        raise SystemExit("dimensionless kernel row should be a source-limit row")
    if by_gate["U2_cosebis_response_units_need_derivation"]["status"] != "REQUIREMENT_FROZEN":
        raise SystemExit("COSEBIs response units requirement must be frozen")
    if by_gate["U3_amplitude_map_not_derived"]["status"] != "OPEN_BLOCKER":
        raise SystemExit("amplitude map must remain open")
    if by_gate["U4_standard_lensing_null_normalization_open"]["status"] != "OPEN_BLOCKER":
        raise SystemExit("standard-lensing null normalization must remain open")
    if by_gate["U5_covariance_metric_not_units_derivation"]["status"] != "REQUIREMENT_FROZEN":
        raise SystemExit("covariance metric separation must be frozen")
    if by_gate["U6_no_endpoint_feedback"]["status"] != "SATISFIED":
        raise SystemExit("no-endpoint row should pass")
    for row in rows:
        if row["claim_boundary"] != policy["claim_boundary"]:
            raise SystemExit("claim boundary mismatch")
        if not row["dimension_check"]:
            raise SystemExit("missing dimension check")
        if not row["known_limit_check"]:
            raise SystemExit("missing known-limit check")
    print(
        "PAPER10_KIDS1000_COSEBIS_PHYSICAL_OPERATOR_UNITS_GATE_V1_VALIDATED "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()

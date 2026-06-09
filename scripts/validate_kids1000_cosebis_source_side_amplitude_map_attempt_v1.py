#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_source_side_amplitude_map_attempt_policy_v1.csv"
AMPLITUDE = ROOT / "data" / "derived" / "kids1000_cosebis_source_side_amplitude_map_attempt_v1.csv"
LEDGER = ROOT / "data" / "derived" / "kids1000_cosebis_source_side_amplitude_map_attempt_v1_ledger.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_source_side_amplitude_map_attempt_v1_summary.csv"


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
    amplitude = read_one(AMPLITUDE)
    ledger = read_rows(LEDGER)

    if policy["status"] != "SOURCE_SIDE_AMPLITUDE_MAP_ATTEMPT_POLICY_FROZEN":
        raise SystemExit("unexpected source-side amplitude map policy status")
    for key in ["uses_kids_data_vector_values", "uses_fit_statistics", "uses_random_noise", "endpoint_scoring_allowed"]:
        if policy[key] != "false":
            raise SystemExit(f"policy {key} must be false")
    if summary["status"] != "DIMENSIONLESS_SOURCE_SIDE_AMPLITUDE_MAP_CONSTRUCTED_PHYSICAL_AMPLITUDE_OPEN":
        raise SystemExit("unexpected amplitude map summary status")
    if summary["verdict"] != "dimensionless_source_amplitude_map_exists_but_physical_amplitude_remains_open":
        raise SystemExit("unexpected amplitude map verdict")
    if summary["amplitude_rows"] != "1" or summary["ledger_rows"] != "5":
        raise SystemExit("unexpected amplitude row counts")
    if summary["satisfied_count"] != "1":
        raise SystemExit("expected one satisfied no-endpoint row")
    if summary["satisfied_as_source_limit_count"] != "1":
        raise SystemExit("expected one source-limit row")
    if summary["satisfied_caveated_count"] != "1":
        raise SystemExit("expected one caveated amplitude row")
    if summary["open_blocker_count"] != "2":
        raise SystemExit("expected two open blockers")
    if summary["dimensionless_source_side_amplitude_map_constructed"] != "true":
        raise SystemExit("dimensionless amplitude map should be constructed")
    if summary["source_side_amplitude_map_derived"] != "true":
        raise SystemExit("source-side dimensionless amplitude map should be derived")
    if abs(float(summary["dimensionless_amplitude_value"]) - 1.0) > 1.0e-12:
        raise SystemExit("dimensionless amplitude must be one")
    for key in [
        "physical_amplitude_units_derived",
        "physical_operator_units_derived",
        "endpoint_calibrated_amplitude",
        "standard_lensing_null_amplitude_proven",
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
    if amplitude["amplitude_units"] != "dimensionless":
        raise SystemExit("amplitude units must remain dimensionless")
    if amplitude["physical_units_derived"] != "false":
        raise SystemExit("amplitude must not claim physical units")
    if amplitude["endpoint_calibrated"] != "false":
        raise SystemExit("amplitude must not be endpoint calibrated")
    if float(amplitude["amplitude_value"]) != 1.0:
        raise SystemExit("amplitude value must be exactly one in this protocol")
    by_gate = {row["gate_id"]: row for row in ledger}
    expected_statuses = {
        "A1_unit_mean_source_normalization_available": "SATISFIED_AS_SOURCE_LIMIT",
        "A2_dimensionless_amplitude_map_constructed": "SATISFIED_CAVEATED",
        "A3_no_endpoint_feedback": "SATISFIED",
        "A4_physical_amplitude_units_not_derived": "OPEN_BLOCKER",
        "A5_standard_lensing_null_amplitude_open": "OPEN_BLOCKER",
    }
    for gate_id, expected_status in expected_statuses.items():
        if by_gate[gate_id]["status"] != expected_status:
            raise SystemExit(f"{gate_id} must have status {expected_status}")
    for row in ledger:
        if row["claim_boundary"] != policy["claim_boundary"]:
            raise SystemExit("claim boundary mismatch")
        if not row["dimension_check"]:
            raise SystemExit("missing dimension check")
        if not row["known_limit_check"]:
            raise SystemExit("missing known-limit check")
    print(
        "PAPER10_KIDS1000_COSEBIS_SOURCE_SIDE_AMPLITUDE_MAP_ATTEMPT_V1_VALIDATED "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()

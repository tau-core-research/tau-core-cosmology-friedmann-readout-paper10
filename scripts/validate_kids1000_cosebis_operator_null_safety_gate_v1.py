#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_operator_null_safety_gate_policy_v1.csv"
LEDGER = ROOT / "data" / "derived" / "kids1000_cosebis_operator_null_safety_gate_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_operator_null_safety_gate_v1_summary.csv"


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
    rows = read_rows(LEDGER)
    summary = read_one(SUMMARY)

    if policy["status"] != "OPERATOR_NULL_SAFETY_GATE_POLICY_FROZEN":
        raise SystemExit("unexpected null-safety gate policy status")
    for key in [
        "uses_kids_data_vector_values",
        "uses_fit_statistics",
        "uses_random_noise",
        "endpoint_scoring_allowed",
    ]:
        if policy[key] != "false":
            raise SystemExit(f"policy {key} must be false")
    if summary["status"] != "OPERATOR_NULL_SAFETY_GATE_BLOCKED_NOT_DERIVED":
        raise SystemExit("unexpected null-safety gate summary status")
    if summary["verdict"] != "null_controls_exist_but_operator_level_null_safety_remains_blocked":
        raise SystemExit("unexpected null-safety gate verdict")
    if summary["operator_null_safety_proven"] != "false":
        raise SystemExit("operator null safety must not be marked proven")
    if summary["mask_null_operator_proven"] != "false":
        raise SystemExit("mask null operator must not be marked proven")
    if summary["gauge_quotient_descent_proven"] != "false":
        raise SystemExit("gauge quotient descent must not be marked proven")
    if summary["spectrum_null_coupling_proven"] != "false":
        raise SystemExit("spectrum-null coupling must not be marked proven")
    if summary["open_blocker_count"] != "3":
        raise SystemExit("expected three open operator null-safety blockers")
    if len(rows) != 8 or summary["gate_rows"] != "8":
        raise SystemExit("gate row count mismatch")

    expected_ids = {
        "N1_source_frozen_null_family_inventory",
        "N2_no_endpoint_feedback_in_null_replay",
        "N3_domain_and_codomain_support",
        "N4_uniform_web_null_control",
        "N5_mask_null_operator_response",
        "N6_gauge_quotient_descent",
        "N7_spectrum_null_coupling",
        "N8_standard_lensing_zero_tau_limit",
    }
    by_id = {row["gate_id"]: row for row in rows}
    if set(by_id) != expected_ids:
        raise SystemExit("unexpected null-safety gate ids")
    for gate_id in [
        "N5_mask_null_operator_response",
        "N6_gauge_quotient_descent",
        "N7_spectrum_null_coupling",
    ]:
        if by_id[gate_id]["status"] != "OPEN_BLOCKER":
            raise SystemExit(f"{gate_id} must remain an open blocker")
    if by_id["N2_no_endpoint_feedback_in_null_replay"]["status"] != "SATISFIED":
        raise SystemExit("no-feedback null replay gate should be satisfied")
    if by_id["N4_uniform_web_null_control"]["status"] != "SATISFIED_AS_NULL_CONTROL_ONLY":
        raise SystemExit("uniform web route should be null-control only")

    for row in rows:
        if row["claim_boundary"] != policy["claim_boundary"]:
            raise SystemExit("claim boundary mismatch")
        if not row["dimension_check"]:
            raise SystemExit("missing dimension check")
        if not row["limit_check"]:
            raise SystemExit("missing limit check")
        if "validation" in row["operator_null_implication"] and "not" not in row["operator_null_implication"]:
            raise SystemExit("operator null implication must not claim validation")
    for key in [
        "uses_kids_data_vector_values",
        "uses_fit_statistics",
        "uses_random_noise",
        "endpoint_scoring_allowed",
        "endpoint_validation_claimed",
        "mode_response_operator_derived",
    ]:
        if summary[key] != "false":
            raise SystemExit(f"summary {key} must be false")
    print(
        "PAPER10_KIDS1000_COSEBIS_OPERATOR_NULL_SAFETY_GATE_V1_VALIDATED "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()

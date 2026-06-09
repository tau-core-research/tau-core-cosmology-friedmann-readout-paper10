#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_survey_native_path_kernel_derivation_gate_policy_v1.csv"
LEDGER = ROOT / "data" / "derived" / "kids1000_cosebis_survey_native_path_kernel_derivation_gate_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_survey_native_path_kernel_derivation_gate_v1_summary.csv"


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
    if policy["status"] != "SURVEY_NATIVE_PATH_KERNEL_DERIVATION_GATE_FROZEN":
        raise SystemExit("unexpected survey-native path-kernel policy status")
    if policy["uses_kids_data_vector_values"] != "false":
        raise SystemExit("policy must not use KiDS data-vector values")
    if policy["uses_fit_statistics"] != "false":
        raise SystemExit("policy must not use fit statistics")
    if policy["uses_random_noise"] != "false":
        raise SystemExit("policy must not use random noise")
    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("policy must not allow endpoint scoring")
    if summary["status"] != "SURVEY_NATIVE_PATH_KERNEL_DERIVATION_GATE_PARTIAL":
        raise SystemExit("unexpected survey-native path-kernel summary status")
    if summary["survey_native_gate_verdict"] != "survey_native_path_route_available_but_mode_response_and_covariant_kernel_derivation_blocked":
        raise SystemExit("unexpected survey-native path-kernel verdict")
    if summary["route_support_conditions_passed"] != "true":
        raise SystemExit("route support conditions should pass or pass caveated")
    if summary["full_kernel_derivation_closed"] != "false":
        raise SystemExit("full kernel derivation must remain open")
    if summary["open_blocker_count"] != "3":
        raise SystemExit("expected three open blockers")
    if summary["fail_count"] != "0":
        raise SystemExit("survey-native path-kernel gate should not contain failed support rows")
    if len(rows) != 8 or summary["conditions"] != "8":
        raise SystemExit("condition row count mismatch")

    by_id = {row["condition_id"]: row for row in rows}
    expected_ids = {
        "K1_source_frozen_mapping_vector",
        "K2_full_route_path_observable",
        "K3_path_weight_factorization",
        "K4_source_frozen_theory_vector_shell",
        "K5_template_recovery_guardrail",
        "K6_survey_native_mode_response_operator",
        "K7_log_band_prior_from_kernel",
        "K8_covariant_lensing_path_limit",
    }
    if set(by_id) != expected_ids:
        raise SystemExit("unexpected survey-native condition ids")
    if by_id["K2_full_route_path_observable"]["status"] != "PASS_CAVEATED":
        raise SystemExit("full-route path observable should remain caveated")
    for blocker in [
        "K6_survey_native_mode_response_operator",
        "K7_log_band_prior_from_kernel",
        "K8_covariant_lensing_path_limit",
    ]:
        if by_id[blocker]["status"] != "OPEN_BLOCKER":
            raise SystemExit(f"{blocker} must remain an open blocker")
    for row in rows:
        if row["claim_boundary"] != policy["claim_boundary"]:
            raise SystemExit("claim boundary mismatch")
        if not row["dimension_check"]:
            raise SystemExit("missing dimension check")
        if not row["known_limit_check"]:
            raise SystemExit("missing known-limit check")
    for row in [summary]:
        if row["uses_kids_data_vector_values"] != "false":
            raise SystemExit("summary must not use KiDS data-vector values")
        if row["uses_fit_statistics"] != "false":
            raise SystemExit("summary must not use fit statistics")
        if row["endpoint_scoring_allowed"] != "false":
            raise SystemExit("summary must remain non-scoring")
        if row["endpoint_validation_claimed"] != "false":
            raise SystemExit("summary must not claim endpoint validation")
        if row["claim_boundary"] != policy["claim_boundary"]:
            raise SystemExit("summary claim boundary mismatch")
    print(
        "PAPER10_KIDS1000_COSEBIS_SURVEY_NATIVE_PATH_KERNEL_DERIVATION_GATE_V1_VALIDATED "
        f"verdict={summary['survey_native_gate_verdict']}"
    )


if __name__ == "__main__":
    main()

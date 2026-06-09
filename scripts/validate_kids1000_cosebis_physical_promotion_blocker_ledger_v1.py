#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_physical_promotion_blocker_ledger_policy_v1.csv"
LEDGER = ROOT / "data" / "derived" / "kids1000_cosebis_physical_promotion_blocker_ledger_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_physical_promotion_blocker_ledger_v1_summary.csv"


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

    if policy["status"] != "PHYSICAL_PROMOTION_BLOCKER_LEDGER_POLICY_FROZEN":
        raise SystemExit("unexpected physical promotion blocker policy status")
    for key in ["uses_kids_data_vector_values", "uses_fit_statistics", "uses_random_noise", "endpoint_scoring_allowed"]:
        if policy[key] != "false":
            raise SystemExit(f"policy {key} must be false")
    if summary["status"] != "PHYSICAL_PROMOTION_BLOCKER_LEDGER_BUILT_NOT_CLOSED":
        raise SystemExit("unexpected physical promotion blocker summary status")
    if summary["verdict"] != "diagnostic_endpoint_ready_but_physical_promotion_blocked_by_five_open_requirements":
        raise SystemExit("unexpected physical promotion blocker verdict")
    if summary["ledger_rows"] != "6":
        raise SystemExit("unexpected blocker ledger row count")
    if summary["diagnostic_ready_not_physical_count"] != "1":
        raise SystemExit("expected one diagnostic-ready row")
    if summary["open_blocker_count"] != "5":
        raise SystemExit("expected five open physical promotion blockers")
    if summary["diagnostic_endpoint_pipeline_ready"] != "true":
        raise SystemExit("diagnostic endpoint pipeline should be ready")
    for key in [
        "physical_promotion_ready",
        "survey_native_operator_theorem_proven",
        "operator_leakage_theorem_proven",
        "gauge_quotient_descent_proven",
        "response_unit_normalization_derived",
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
    expected = {
        "G0_diagnostic_endpoint_pipeline_ready_not_physical_promotion": "DIAGNOSTIC_READY_NOT_PHYSICAL",
        "B1_survey_native_operator_theorem_open": "OPEN_BLOCKER",
        "B2_operator_leakage_theorem_open": "OPEN_BLOCKER",
        "B3_gauge_quotient_descent_open": "OPEN_BLOCKER",
        "B4_response_unit_normalization_open": "OPEN_BLOCKER",
        "B5_standard_lensing_null_amplitude_theorem_open": "OPEN_BLOCKER",
    }
    by_blocker = {row["blocker_id"]: row for row in rows}
    for blocker_id, status in expected.items():
        if by_blocker[blocker_id]["status"] != status:
            raise SystemExit(f"{blocker_id} must have status {status}")
    for row in rows:
        if row["claim_boundary"] != policy["claim_boundary"]:
            raise SystemExit("claim boundary mismatch")
        if not row["dimension_check"]:
            raise SystemExit("missing dimension check")
        if not row["known_limit_check"]:
            raise SystemExit("missing known-limit check")
    print(
        "PAPER10_KIDS1000_COSEBIS_PHYSICAL_PROMOTION_BLOCKER_LEDGER_V1_VALIDATED "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()

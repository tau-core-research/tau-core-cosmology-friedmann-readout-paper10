#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_mask_mode_leakage_audit_policy_v1.csv"
GRID = ROOT / "data" / "derived" / "kids1000_cosebis_mask_mode_leakage_audit_v1_grid.csv"
LEDGER = ROOT / "data" / "derived" / "kids1000_cosebis_mask_mode_leakage_audit_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_mask_mode_leakage_audit_v1_summary.csv"


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
    grid = read_rows(GRID)

    if policy["status"] != "MASK_MODE_LEAKAGE_AUDIT_POLICY_FROZEN":
        raise SystemExit("unexpected mask-mode leakage audit policy status")
    for key in [
        "uses_kids_data_vector_values",
        "uses_fit_statistics",
        "uses_random_noise",
        "endpoint_scoring_allowed",
    ]:
        if policy[key] != "false":
            raise SystemExit(f"policy {key} must be false")
    if summary["status"] != "MASK_MODE_LEAKAGE_AUDIT_SOURCE_SIDE_COMPLETE_OPERATOR_BLOCKED":
        raise SystemExit("unexpected leakage audit status")
    if summary["verdict"] != "uniform_mask_collapse_is_null_but_nonuniform_operator_leakage_remains_open":
        raise SystemExit("unexpected leakage audit verdict")
    if summary["uniform_collapse_all_null"] != "true":
        raise SystemExit("uniform tile collapse should be null for centered mask basis")
    if summary["leakage_risk_recorded"] != "true":
        raise SystemExit("leakage risk must be recorded")
    if summary["operator_level_leakage_theorem_proven"] != "false":
        raise SystemExit("operator-level leakage theorem must not be marked proven")
    if summary["mode_response_operator_derived"] != "false":
        raise SystemExit("mode-response operator must not be marked derived")
    if summary["basis_count"] != "3":
        raise SystemExit("expected three mask basis directions")
    if summary["spectrum_family_count"] != "4":
        raise SystemExit("expected four spectrum families")
    if summary["grid_rows"] != "12" or len(grid) != 12:
        raise SystemExit("expected 12 leakage grid rows")
    if summary["open_blocker_count"] != "1":
        raise SystemExit("expected one leakage theorem blocker")
    if float(summary["max_uniform_collapse_norm"]) >= 1.0e-10:
        raise SystemExit("uniform collapse norm too large")
    if float(summary["max_low_mode_rms_envelope_norm"]) <= 0.0:
        raise SystemExit("low-mode leakage risk norm must be positive")

    by_gate = {row["gate_id"]: row for row in ledger}
    expected = {
        "L1_centered_mask_uniform_collapse",
        "L2_nonuniform_operator_leakage_risk",
        "L3_no_endpoint_or_data_vector_use",
        "L4_operator_level_leakage_theorem",
    }
    if set(by_gate) != expected:
        raise SystemExit("unexpected leakage ledger ids")
    if by_gate["L1_centered_mask_uniform_collapse"]["status"] != "PASS":
        raise SystemExit("uniform collapse should pass")
    if by_gate["L2_nonuniform_operator_leakage_risk"]["status"] != "RISK_RECORDED":
        raise SystemExit("nonuniform leakage risk must be recorded")
    if by_gate["L4_operator_level_leakage_theorem"]["status"] != "OPEN_BLOCKER":
        raise SystemExit("operator-level leakage theorem must remain open")
    for row in ledger:
        if row["claim_boundary"] != policy["claim_boundary"]:
            raise SystemExit("ledger claim boundary mismatch")
        if not row["dimension_check"]:
            raise SystemExit("missing dimension check")
        if not row["limit_check"]:
            raise SystemExit("missing limit check")
    for row in grid:
        if row["uniform_collapse_is_null"] != "true":
            raise SystemExit("all grid rows should have null uniform collapse")
        if row["leakage_risk_if_operator_uses_rms_or_abs_mask_load"] != "true":
            raise SystemExit("grid should preserve nonuniform operator leakage risk")
        for key in [
            "contains_theory_vector",
            "contains_predictions",
            "contains_residuals",
            "contains_fit_statistics",
            "uses_kids_data_vector_values",
            "uses_posterior_chains",
            "endpoint_scoring_allowed",
            "endpoint_validation_claimed",
        ]:
            if row[key] != "false":
                raise SystemExit(f"grid {key} must be false")
        if row["claim_boundary"] != policy["claim_boundary"]:
            raise SystemExit("grid claim boundary mismatch")
    for key in [
        "contains_theory_vector",
        "contains_predictions",
        "contains_residuals",
        "contains_fit_statistics",
        "uses_kids_data_vector_values",
        "uses_posterior_chains",
        "endpoint_scoring_allowed",
        "endpoint_validation_claimed",
    ]:
        if summary[key] != "false":
            raise SystemExit(f"summary {key} must be false")
    print(
        "PAPER10_KIDS1000_COSEBIS_MASK_MODE_LEAKAGE_AUDIT_V1_VALIDATED "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()

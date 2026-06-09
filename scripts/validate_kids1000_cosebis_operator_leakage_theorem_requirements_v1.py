#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_operator_leakage_theorem_requirements_policy_v1.csv"
LEDGER = ROOT / "data" / "derived" / "kids1000_cosebis_operator_leakage_theorem_requirements_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_operator_leakage_theorem_requirements_v1_summary.csv"


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

    if policy["status"] != "OPERATOR_LEAKAGE_THEOREM_REQUIREMENTS_POLICY_FROZEN":
        raise SystemExit("unexpected operator leakage theorem requirements policy status")
    for key in [
        "uses_kids_data_vector_values",
        "uses_fit_statistics",
        "uses_random_noise",
        "endpoint_scoring_allowed",
    ]:
        if policy[key] != "false":
            raise SystemExit(f"policy {key} must be false")
    if summary["status"] != "OPERATOR_LEAKAGE_THEOREM_REQUIREMENTS_FROZEN_NOT_PROVEN":
        raise SystemExit("unexpected requirements summary status")
    if summary["verdict"] != "requirements_frozen_for_operator_leakage_theorem_but_proof_remains_open":
        raise SystemExit("unexpected requirements verdict")
    if summary["requirement_rows"] != "7" or len(rows) != 7:
        raise SystemExit("expected seven requirements rows")
    if summary["satisfied_count"] != "1":
        raise SystemExit("expected one fully satisfied no-endpoint requirement")
    if summary["satisfied_as_source_limit_count"] != "1":
        raise SystemExit("expected one source-limit requirement")
    if summary["risk_recorded_count"] != "1":
        raise SystemExit("expected one recorded risk")
    if summary["requirement_frozen_count"] != "2":
        raise SystemExit("expected two frozen theorem requirements")
    if summary["open_blocker_count"] != "2":
        raise SystemExit("expected two open theorem blockers")
    for key in [
        "uniform_tile_null_limit_available",
        "nonuniform_leakage_risk_recorded",
        "pure_mask_rejection_requirement_frozen",
        "mode_spectrum_coupling_requirement_frozen",
    ]:
        if summary[key] != "true":
            raise SystemExit(f"summary {key} must be true")
    for key in [
        "operator_leakage_theorem_proven",
        "gauge_quotient_descent_proven",
        "mode_response_operator_derived",
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

    by_req = {row["requirement_id"]: row for row in rows}
    expected = {
        "T1_uniform_tile_null_limit",
        "T2_nonuniform_mask_leakage_risk",
        "T3_pure_mask_rejection_or_control_subspace",
        "T4_mode_spectrum_coupling_requirement",
        "T5_no_endpoint_feedback",
        "T6_operator_leakage_theorem_not_proven",
        "T7_gauge_quotient_descent_not_proven",
    }
    if set(by_req) != expected:
        raise SystemExit("unexpected requirement ids")
    if by_req["T1_uniform_tile_null_limit"]["status"] != "SATISFIED_AS_SOURCE_LIMIT":
        raise SystemExit("uniform tile limit should be a source-limit satisfaction")
    if by_req["T2_nonuniform_mask_leakage_risk"]["status"] != "RISK_RECORDED":
        raise SystemExit("nonuniform mask leakage risk must be recorded")
    if by_req["T3_pure_mask_rejection_or_control_subspace"]["status"] != "REQUIREMENT_FROZEN":
        raise SystemExit("pure-mask rejection requirement must be frozen")
    if by_req["T4_mode_spectrum_coupling_requirement"]["status"] != "REQUIREMENT_FROZEN":
        raise SystemExit("mode-spectrum coupling requirement must be frozen")
    if by_req["T5_no_endpoint_feedback"]["status"] != "SATISFIED":
        raise SystemExit("no-endpoint feedback requirement should pass")
    if by_req["T6_operator_leakage_theorem_not_proven"]["status"] != "OPEN_BLOCKER":
        raise SystemExit("operator leakage theorem must remain open")
    if by_req["T7_gauge_quotient_descent_not_proven"]["status"] != "OPEN_BLOCKER":
        raise SystemExit("gauge quotient descent must remain open")
    for row in rows:
        if row["claim_boundary"] != policy["claim_boundary"]:
            raise SystemExit("claim boundary mismatch")
        if not row["dimension_check"]:
            raise SystemExit("missing dimension check")
        if not row["known_limit_check"]:
            raise SystemExit("missing known-limit check")
        if row["requirement_id"] in {"T6_operator_leakage_theorem_not_proven", "T7_gauge_quotient_descent_not_proven"}:
            if row["status"] != "OPEN_BLOCKER":
                raise SystemExit("theorem blockers must not be closed")
    print(
        "PAPER10_KIDS1000_COSEBIS_OPERATOR_LEAKAGE_THEOREM_REQUIREMENTS_V1_VALIDATED "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()

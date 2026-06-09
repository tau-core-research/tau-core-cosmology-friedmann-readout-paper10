#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_gauge_quotient_descent_gate_policy_v1.csv"
LEDGER = ROOT / "data" / "derived" / "kids1000_cosebis_gauge_quotient_descent_gate_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_gauge_quotient_descent_gate_v1_summary.csv"


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

    if policy["status"] != "GAUGE_QUOTIENT_DESCENT_GATE_POLICY_FROZEN":
        raise SystemExit("unexpected gauge quotient descent policy status")
    for key in [
        "uses_kids_data_vector_values",
        "uses_fit_statistics",
        "uses_random_noise",
        "endpoint_scoring_allowed",
    ]:
        if policy[key] != "false":
            raise SystemExit(f"policy {key} must be false")
    if summary["status"] != "GAUGE_QUOTIENT_DESCENT_REQUIREMENTS_FROZEN_NOT_PROVEN":
        raise SystemExit("unexpected gauge quotient descent summary status")
    if summary["verdict"] != "gauge_quotient_descent_requirements_frozen_but_theorem_remains_open":
        raise SystemExit("unexpected gauge quotient descent verdict")
    if summary["gate_rows"] != "8" or len(rows) != 8:
        raise SystemExit("expected eight quotient descent rows")
    if summary["satisfied_count"] != "1":
        raise SystemExit("expected one satisfied no-endpoint row")
    if summary["satisfied_as_source_limit_count"] != "1":
        raise SystemExit("expected one source-limit row")
    if summary["requirement_frozen_count"] != "4":
        raise SystemExit("expected four frozen requirements")
    if summary["open_blocker_count"] != "2":
        raise SystemExit("expected two open blockers")
    for key in ["equivalence_classes_declared", "uniform_mask_offset_limit_available"]:
        if summary[key] != "true":
            raise SystemExit(f"summary {key} must be true")
    for key in [
        "normalization_invariance_proven",
        "tile_relabeling_invariance_proven",
        "pure_mask_control_compatibility_proven",
        "gauge_quotient_descent_proven",
        "survey_native_operator_constructed",
        "operator_leakage_theorem_proven",
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
        "Q1_equivalence_class_declared",
        "Q2_uniform_mask_offset_limit",
        "Q3_normalization_representative_independence",
        "Q4_tile_relabeling_and_route_coordinate_invariance",
        "Q5_mask_pure_mode_control_compatibility",
        "Q6_no_endpoint_feedback",
        "Q7_gauge_quotient_descent_theorem_not_proven",
        "Q8_survey_native_operator_not_constructed",
    }
    if set(by_gate) != expected:
        raise SystemExit("unexpected quotient descent gate ids")
    if by_gate["Q1_equivalence_class_declared"]["status"] != "REQUIREMENT_FROZEN":
        raise SystemExit("equivalence class declaration must remain a frozen requirement")
    if by_gate["Q2_uniform_mask_offset_limit"]["status"] != "SATISFIED_AS_SOURCE_LIMIT":
        raise SystemExit("uniform mask offset must be a source-limit row")
    if by_gate["Q3_normalization_representative_independence"]["status"] != "REQUIREMENT_FROZEN":
        raise SystemExit("normalization independence must be frozen")
    if by_gate["Q4_tile_relabeling_and_route_coordinate_invariance"]["status"] != "REQUIREMENT_FROZEN":
        raise SystemExit("tile relabeling invariance must be frozen")
    if by_gate["Q5_mask_pure_mode_control_compatibility"]["status"] != "REQUIREMENT_FROZEN":
        raise SystemExit("mask pure-mode compatibility must be frozen")
    if by_gate["Q6_no_endpoint_feedback"]["status"] != "SATISFIED":
        raise SystemExit("no-endpoint feedback row should pass")
    if by_gate["Q7_gauge_quotient_descent_theorem_not_proven"]["status"] != "OPEN_BLOCKER":
        raise SystemExit("gauge quotient descent theorem must remain open")
    if by_gate["Q8_survey_native_operator_not_constructed"]["status"] != "OPEN_BLOCKER":
        raise SystemExit("survey-native operator construction must remain open")
    for row in rows:
        if row["claim_boundary"] != policy["claim_boundary"]:
            raise SystemExit("claim boundary mismatch")
        if not row["dimension_check"]:
            raise SystemExit("missing dimension check")
        if not row["known_limit_check"]:
            raise SystemExit("missing known-limit check")
    print(
        "PAPER10_KIDS1000_COSEBIS_GAUGE_QUOTIENT_DESCENT_GATE_V1_VALIDATED "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()

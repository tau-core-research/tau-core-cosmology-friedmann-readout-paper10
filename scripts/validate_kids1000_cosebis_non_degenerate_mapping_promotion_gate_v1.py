#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_non_degenerate_mapping_promotion_gate_policy_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_non_degenerate_mapping_promotion_gate_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_non_degenerate_mapping_promotion_gate_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def main() -> None:
    policy = read_one(POLICY)
    summary = read_one(SUMMARY)
    with OUT.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if policy["status"] != "NON_DEGENERATE_MAPPING_PROMOTION_GATE_FROZEN_NOT_PASSED":
        raise SystemExit("unexpected promotion gate policy status")
    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("promotion gate policy must keep endpoint scoring disabled")
    if summary["status"] != "NON_DEGENERATE_MAPPING_PROMOTION_GATE_BUILT_NOT_READY":
        raise SystemExit("promotion gate should be built but not ready")
    if summary["gate_count"] != "6":
        raise SystemExit("promotion gate must contain six gates")
    if summary["passed_gate_count"] != "1":
        raise SystemExit("only the leakage guard should currently pass")
    if summary["blocking_gate_count"] != "5":
        raise SystemExit("five promotion gates should currently block")
    if summary["first_blocking_gate"] != "PROMOTE_01_F_OVERLAP_ENDPOINT_ROUTE":
        raise SystemExit("F_overlap endpoint route must remain first promotion blocker")
    if summary["non_degenerate_mapping_promotion_allowed"] != "false":
        raise SystemExit("non-degenerate mapping promotion must remain disabled")
    for key in [
        "endpoint_scoring_allowed",
        "scoring_executed",
        "contains_theory_vector",
        "contains_predictions",
        "contains_residuals",
        "contains_fit_statistics",
        "uses_kids_data_vector_values",
        "uses_posterior_chains",
        "uses_posthoc_selection",
    ]:
        if summary[key] != "false":
            raise SystemExit(f"summary must keep {key}=false")
        if any(row[key] != "false" for row in rows):
            raise SystemExit(f"rows must keep {key}=false")
    expected = {
        "PROMOTE_01_F_OVERLAP_ENDPOINT_ROUTE": ("false", "blocking_source_overlap"),
        "PROMOTE_02_SOURCE_PREFLIGHT_MAPPING_READY": ("false", "blocking_source_preflight"),
        "PROMOTE_03_NON_DEGENERATE_BRANCH_GEOMETRY": ("false", "blocking_rank_one_partial_control"),
        "PROMOTE_04_THEORY_VECTOR_COMPUTED": ("false", "blocking_theory_vector"),
        "PROMOTE_05_NULL_CONTROLS_EXECUTED_AFTER_MAPPING": ("false", "blocking_null_controls"),
        "PROMOTE_06_LEAKAGE_GUARDS": ("true", "not_blocking"),
    }
    by_gate = {row["gate_id"]: row for row in rows}
    if set(by_gate) != set(expected):
        raise SystemExit("unexpected promotion gate IDs")
    for gate_id, (passed, blocker) in expected.items():
        if by_gate[gate_id]["gate_passed"] != passed:
            raise SystemExit(f"unexpected pass state for {gate_id}")
        if by_gate[gate_id]["blocking_status"] != blocker:
            raise SystemExit(f"unexpected blocker state for {gate_id}")
    if "positive_rank_1" not in by_gate["PROMOTE_03_NON_DEGENERATE_BRANCH_GEOMETRY"]["current_state"]:
        raise SystemExit("rank-one degeneracy must remain recorded in promotion gate")
    for marker in [
        "kids_data_vector_values",
        "posterior_chains",
        "lensing_residuals",
        "posthoc_weight_selection",
        "posthoc_mask_subset_selection",
    ]:
        if marker not in policy["forbidden_inputs"]:
            raise SystemExit(f"missing forbidden input marker: {marker}")
    print(
        "PAPER10_KIDS1000_COSEBIS_NON_DEGENERATE_MAPPING_PROMOTION_GATE_V1_VALIDATED "
        f"blockers={summary['blocking_gate_count']} endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()

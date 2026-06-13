#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_shape_bound_control_vectors_policy_v1.csv"
OUT = ROOT / "data/derived/paper10_desi_shape_bound_control_vectors_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_shape_bound_control_vectors_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_shape_bound_control_vectors_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def one_row(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    policy = one_row(POLICY)
    rows = read_rows(OUT)
    summary = one_row(SUMMARY)
    require(policy["claim_boundary"] == CLAIM_BOUNDARY, "bad policy claim boundary")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "bad summary claim boundary")
    require(len(rows) == 5, "shape-bound controls must contain five families")
    for row in rows + [policy, summary]:
        require(row["endpoint_replay_allowed"] == "false", "must not authorize replay")
        require(row["endpoint_validation_claimed"] == "false", "must not claim endpoint validation")
        require(row["physical_validation_claimed"] == "false", "must not claim physical validation")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "bad row claim boundary")
    by_family = {row["control_family"]: row for row in rows}
    require(set(by_family) == {"redshift_order_shuffle", "leave_row_or_pair", "cc_window_stress", "wrong_time_basis", "rd_prior_stress"}, "unexpected control family set")
    require(by_family["redshift_order_shuffle"]["control_binding_status"] == "bound_source_vector", "redshift shuffle must be bound")
    require(by_family["cc_window_stress"]["control_binding_status"] == "bound_caveated_source_window_stress", "CC window stress must be caveated-bound")
    require(by_family["rd_prior_stress"]["control_binding_status"] == "bound_analytic_null_for_first_difference", "rd prior stress should bind as analytic null")
    require({row["uses_endpoint_scores"] for row in rows} == {"false"}, "must not use endpoint scores")
    require({row["uses_endpoint_residuals"] for row in rows} == {"false"}, "must not use endpoint residuals")
    require(summary["status"] == "DESI_SHAPE_BOUND_CONTROL_VECTORS_BUILT_NOT_REPLAY_NOT_VALIDATION", "bad summary status")
    require(summary["required_control_count"] == "5", "bad required control count")
    require(summary["shape_bound_control_count"] == "5", "expected all controls to be shape-bound")
    require(summary["unbound_control_families"] == "none", "no control family should remain unbound")
    require(summary["ordering_control_suite_shape_bound"] == "true", "ordering suite should be shape-bound")
    require(summary["ordering_control_suite_ready_for_replay"] == "false", "suite must not be replay-ready")
    require(summary["verdict"] == "shape_route_controls_bound_but_replay_not_authorized", "bad verdict")
    print("paper10_desi_shape_bound_control_vectors_v1: OK")


if __name__ == "__main__":
    main()

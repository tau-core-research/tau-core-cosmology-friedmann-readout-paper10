#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_ordering_control_suite_policy_v1.csv"
OUT = ROOT / "data/derived/paper10_desi_ordering_control_suite_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_ordering_control_suite_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_ordering_control_suite_not_validation"


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
    require(len(rows) == 5, "ordering suite must freeze five controls")
    for row in rows + [policy, summary]:
        require(row["endpoint_replay_allowed"] == "false", "must not authorize replay")
        require(row["endpoint_validation_claimed"] == "false", "must not claim endpoint validation")
        require(row["physical_validation_claimed"] == "false", "must not claim physical validation")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "bad row claim boundary")
    controls = {row["control_family"] for row in rows}
    require(
        controls == {"redshift_order_shuffle", "leave_row_or_pair", "cc_window_stress", "wrong_time_basis", "rd_prior_stress"},
        "unexpected control family set",
    )
    require({row["control_channel"] for row in rows} == {"K_null"}, "all controls must map to K_null")
    require(summary["status"] == "DESI_ORDERING_CONTROL_SUITE_DECLARED_NOT_REPLAY_NOT_VALIDATION", "bad status")
    require(summary["available_control_count"] == "1", "only redshift-order shuffle should be available now")
    require(summary["shape_bound_control_count"] == "0", "controls are not yet bound to the shape route")
    require(summary["ordering_control_suite_ready_for_replay"] == "false", "ordering suite must not be replay-ready")
    require(summary["quotient_survival_gate_status"] == "not_proven_ordering_null_unresolved", "quotient survival blocker must remain")
    require(summary["verdict"] == "k_null_ordering_controls_declared_but_not_shape_bound", "bad verdict")
    print("paper10_desi_ordering_control_suite_v1: OK")


if __name__ == "__main__":
    main()

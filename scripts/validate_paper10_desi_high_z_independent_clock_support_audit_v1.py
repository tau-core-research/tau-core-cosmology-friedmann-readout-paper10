#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_high_z_independent_clock_support_audit_policy_v1.csv"
OUT = ROOT / "data/derived/paper10_desi_high_z_independent_clock_support_audit_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_high_z_independent_clock_support_audit_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_high_z_independent_clock_support_audit_not_validation"


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


def main() -> None:
    policy = one_row(POLICY)
    rows = read_rows(OUT)
    summary = one_row(SUMMARY)
    if policy["claim_boundary"] != CLAIM_BOUNDARY or summary["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("bad high-z clock support audit claim boundary")
    if len(rows) != 3:
        raise SystemExit("high-z clock support audit must contain three route rows")
    if {row["claim_boundary"] for row in rows} != {CLAIM_BOUNDARY}:
        raise SystemExit("bad high-z clock support audit row claim boundary")
    for row in rows + [policy, summary]:
        if row["endpoint_replay_allowed"] != "false":
            raise SystemExit("high-z support audit must not authorize replay")
        if row["endpoint_validation_claimed"] != "false" or row["physical_validation_claimed"] != "false":
            raise SystemExit("high-z support audit must not claim validation")
    if summary["status"] != "DESI_HIGH_Z_INDEPENDENT_CLOCK_SUPPORT_AUDIT_BUILT_NOT_REPLAY_NOT_VALIDATION":
        raise SystemExit("bad high-z clock support audit status")
    if summary["target_radial_index"] != "5" or summary["target_z_eff"] != "2.33":
        raise SystemExit("high-z support audit target changed")
    if summary["target_within_frozen_cc_support"] != "false":
        raise SystemExit("target must remain outside frozen CC support")
    if summary["target_bracketed_without_extrapolation"] != "false":
        raise SystemExit("target must not be bracketed without extrapolation")
    if summary["endpoint_ready_support_count"] != "0":
        raise SystemExit("no endpoint-ready high-z support should be present")
    if summary["high_z_row_can_enter_replay"] != "false":
        raise SystemExit("high-z row must remain replay-blocked")
    if summary["verdict"] != "desi_high_z_clock_support_missing_row_remains_holdout_not_validation":
        raise SystemExit("bad high-z support audit verdict")
    frozen = {row["route_id"]: row for row in rows}["FROZEN_CC_TABLE"]
    if frozen["route_status"] != "AVAILABLE_BUT_DOES_NOT_COVER_TARGET_Z":
        raise SystemExit("frozen CC route status should show missing coverage")
    print("paper10_desi_high_z_independent_clock_support_audit_v1: OK")


if __name__ == "__main__":
    main()

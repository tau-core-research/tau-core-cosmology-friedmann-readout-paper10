#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_clock_support_blocker_verdict_policy_v1.csv"
ROWS = ROOT / "data/derived/paper10_desi_clock_support_blocker_verdict_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_clock_support_blocker_verdict_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_clock_support_blocker_verdict_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def one_row(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def require_false(row: dict[str, str], fields: list[str], label: str) -> None:
    for field in fields:
        if row.get(field) != "false":
            raise SystemExit(f"{label} {field} must be false")


def main() -> None:
    policy = one_row(POLICY)
    summary = one_row(SUMMARY)
    rows = read_rows(ROWS)
    require_false(policy, ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"], "policy")
    require_false(summary, ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"], "summary")
    if policy["claim_boundary"] != CLAIM_BOUNDARY or summary["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("bad claim boundary")
    if summary["status"] != "DESI_CLOCK_SUPPORT_ROUTE_BLOCKED_AFTER_SOURCE_SCAN_NOT_REPLAY_NOT_VALIDATION":
        raise SystemExit("bad summary status")
    if summary["active_blocker_count"] != "2" or len(rows) != 2:
        raise SystemExit("blocker verdict must contain two active blockers")
    if summary["candidate_scan_accepted_count"] != "0":
        raise SystemExit("candidate scan must not close a blocker")
    if summary["verdict"] != "desi_clock_support_route_remains_blocked_pending_independent_clock_sources":
        raise SystemExit("bad summary verdict")
    by_blocker = {row["blocker_id"]: row for row in rows}
    expected = {
        "ROW4_INDEPENDENT_CLOCK_REDUNDANCY_MISSING",
        "ROW5_HIGH_Z_CLOCK_SUPPORT_MISSING",
    }
    if set(by_blocker) != expected:
        raise SystemExit("unexpected blocker ids")
    for blocker_id, row in by_blocker.items():
        require_false(row, ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"], blocker_id)
        if row["blocker_status"] != "ACTIVE_BLOCKER":
            raise SystemExit(f"{blocker_id} must remain active")
        if row["claim_boundary"] != CLAIM_BOUNDARY:
            raise SystemExit(f"{blocker_id} has bad claim boundary")
        if "endpoint_replay" not in row["disallowed_next_action"]:
            raise SystemExit(f"{blocker_id} must disallow endpoint replay")
    if "BAO_RSD_as_clock_support" not in by_blocker["ROW4_INDEPENDENT_CLOCK_REDUNDANCY_MISSING"]["disallowed_next_action"]:
        raise SystemExit("row4 must disallow BAO/RSD as clock support")
    if "LyA_BAO_as_clock_support" not in by_blocker["ROW5_HIGH_Z_CLOCK_SUPPORT_MISSING"]["disallowed_next_action"]:
        raise SystemExit("row5 must disallow Ly-alpha BAO as clock support")


if __name__ == "__main__":
    main()

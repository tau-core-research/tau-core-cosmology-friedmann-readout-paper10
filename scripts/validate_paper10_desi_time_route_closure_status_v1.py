#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_time_route_closure_status_policy_v1.csv"
OUT = ROOT / "data/derived/paper10_desi_time_route_closure_status_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_time_route_closure_status_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_time_route_closure_status_not_validation"


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
    row = one_row(OUT)
    summary = one_row(SUMMARY)
    require_false(policy, ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"], "policy")
    require_false(row, ["row4_can_enter_replay", "desi_time_route_endpoint_ready", "endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"], "row")
    require_false(summary, ["row4_can_enter_replay", "desi_time_route_endpoint_ready", "endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"], "summary")
    if policy["claim_boundary"] != CLAIM_BOUNDARY or row["claim_boundary"] != CLAIM_BOUNDARY or summary["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("claim boundary mismatch")
    if summary["status"] != "DESI_TIME_ROUTE_CLOSURE_STATUS_BUILT_NOT_REPLAY_NOT_VALIDATION":
        raise SystemExit("bad summary status")
    if row["closure_status"] != summary["closure_status"]:
        raise SystemExit("summary closure status mismatch")
    if row["closure_status"] == "DESI_TIME_ROUTE_CLOSED_PENDING_SOURCE_BLOCKERS_NOT_REPLAY":
        if row["verdict"] != "desi_time_route_closed_pending_row4_or_row5_or_richer_clock_readout_support":
            raise SystemExit("bad blocked-route verdict")
    if row["row5_status"] == "ROW5_HIGH_Z_CLOCK_SUPPORT_MISSING" and row["row5_can_enter_replay"] != "false":
        raise SystemExit("row5 missing support cannot enter replay")
    print(f"PAPER10_DESI_TIME_ROUTE_CLOSURE_STATUS_VALIDATED closure_status={row['closure_status']}")


if __name__ == "__main__":
    main()

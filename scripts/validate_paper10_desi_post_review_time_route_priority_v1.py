#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_post_review_time_route_priority_policy_v1.csv"
OUT = ROOT / "data/derived/paper10_desi_post_review_time_route_priority_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_post_review_time_route_priority_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_post_review_time_route_priority_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def require_false(row: dict[str, str], fields: list[str], label: str) -> None:
    for field in fields:
        if row[field] != "false":
            raise SystemExit(f"{label} {field} must be false")


def main() -> None:
    policy = read_one(POLICY)
    rows = read_rows(OUT)
    summary = read_one(SUMMARY)
    require_false(policy, ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"], "policy")
    require_false(summary, ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"], "summary")
    if policy["claim_boundary"] != CLAIM_BOUNDARY or summary["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("claim boundary mismatch")
    if len(rows) != 5:
        raise SystemExit("priority ledger must contain exactly five route rows")
    by_rank = {row["rank"]: row for row in rows}
    if by_rank["1"]["route"] != "TIME_READOUT_SHAPE_OBSERVABLE":
        raise SystemExit("time-readout shape must be primary next gate")
    if by_rank["5"]["route"] != "HIGH_Z_INDEPENDENT_CLOCK_SUPPORT":
        raise SystemExit("high-z support must be future holdout reopen gate after row5 confirmation")
    for row in rows:
        require_false(row, ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"], row["route"])
        if row["claim_boundary"] != CLAIM_BOUNDARY:
            raise SystemExit(f"{row['route']} claim boundary mismatch")
    if summary["primary_next_gate"] != "TIME_READOUT_SHAPE_OBSERVABLE":
        raise SystemExit("bad primary next gate")
    if summary["row5_role"] != "HIGH_Z_HOLDOUT_FUTURE_REOPEN_ONLY":
        raise SystemExit("bad row5 role")
    if summary["verdict"] != "post_review_priority_is_shape_derivation_not_row5_replay":
        raise SystemExit("bad priority verdict")
    print("PAPER10_DESI_POST_REVIEW_TIME_ROUTE_PRIORITY_VALIDATED")


if __name__ == "__main__":
    main()

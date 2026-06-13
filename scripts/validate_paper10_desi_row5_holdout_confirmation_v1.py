#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_row5_holdout_confirmation_policy_v1.csv"
OUT = ROOT / "data/derived/paper10_desi_row5_holdout_confirmation_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_row5_holdout_confirmation_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_row5_holdout_confirmation_not_validation"


def read_one(path: Path) -> dict[str, str]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def require_false(row: dict[str, str], fields: list[str], label: str) -> None:
    for field in fields:
        if row.get(field) != "false":
            raise SystemExit(f"{label} {field} must be false")


def main() -> None:
    policy = read_one(POLICY)
    row = read_one(OUT)
    summary = read_one(SUMMARY)
    require_false(policy, ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"], "policy")
    require_false(row, ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"], "row")
    require_false(summary, ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"], "summary")
    if policy["claim_boundary"] != CLAIM_BOUNDARY or row["claim_boundary"] != CLAIM_BOUNDARY or summary["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("claim boundary mismatch")
    if row["status"] != "ROW5_HOLDOUT_CONFIRMED_NOT_REPLAY_NOT_VALIDATION":
        raise SystemExit("bad holdout status")
    if row["row5_gate_status"] != "ROW5_HIGH_Z_BLOCKER_REMAINS_NOT_REPLAY":
        raise SystemExit("row5 must remain blocked")
    if row["accepted_for_row5_count"] != "0":
        raise SystemExit("accepted row5 source count must be zero")
    if row["allowed_radial_rows"] != "0;1;2;3;4" or row["excluded_radial_rows"] != "5":
        raise SystemExit("bad allowed/excluded row grammar")
    if row["verdict"] != "row5_holdout_confirmed_no_gate_closing_source_not_replay":
        raise SystemExit("bad holdout verdict")
    print("PAPER10_DESI_ROW5_HOLDOUT_CONFIRMATION_VALIDATED")


if __name__ == "__main__":
    main()

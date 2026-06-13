#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_row4_window_decision_gate_policy_v1.csv"
OUT = ROOT / "data/derived/paper10_desi_row4_window_decision_gate_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_row4_window_decision_gate_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_row4_window_decision_gate_not_validation"
ALLOWED_GATE_STATUSES = {
    "ROW4_WINDOW_REVIEW_PENDING_NOT_REPLAY",
    "ROW4_WINDOW_BLOCKER_REMAINS_NOT_REPLAY",
    "ROW4_SOURCE_REOPEN_CAVEATED_NO_REPLAY",
    "ROW4_SOURCE_REOPEN_CAVEATED_REPLAY_REVIEW_REQUIRED_NOT_REPLAY",
}


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
    require_false(row, ["row4_can_enter_replay", "endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"], "row")
    require_false(summary, ["row4_can_enter_replay", "endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"], "summary")
    if policy["claim_boundary"] != CLAIM_BOUNDARY or row["claim_boundary"] != CLAIM_BOUNDARY or summary["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("claim boundary mismatch")
    if summary["status"] != "DESI_ROW4_WINDOW_DECISION_GATE_BUILT_NOT_REPLAY_NOT_VALIDATION":
        raise SystemExit("bad summary status")
    if row["gate_status"] not in ALLOWED_GATE_STATUSES:
        raise SystemExit("bad row gate status")
    if summary["gate_status"] != row["gate_status"]:
        raise SystemExit("summary and row gate status mismatch")
    if row["review_completed"] == "false":
        if row["gate_status"] != "ROW4_WINDOW_REVIEW_PENDING_NOT_REPLAY":
            raise SystemExit("incomplete review must map to pending gate")
        if row["strict_window_decision"] != "PENDING":
            raise SystemExit("pending review must not carry a strict-window decision")
    if row["source_reopen_caveated"] == "true":
        if not row["gate_status"].startswith("ROW4_SOURCE_REOPEN_CAVEATED"):
            raise SystemExit("source reopen flag must match source reopen gate")
    print(f"PAPER10_DESI_ROW4_WINDOW_DECISION_GATE_VALIDATED gate_status={row['gate_status']}")


if __name__ == "__main__":
    main()

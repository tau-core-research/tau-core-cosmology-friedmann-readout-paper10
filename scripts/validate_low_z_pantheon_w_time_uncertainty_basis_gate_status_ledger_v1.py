#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/low_z_pantheon_w_time_uncertainty_basis_gate_status_ledger_v1.csv"
SUMMARY = ROOT / "data/derived/low_z_pantheon_w_time_uncertainty_basis_gate_status_ledger_v1_summary.csv"
CLAIM_BOUNDARY = "w_time_uncertainty_basis_gate_status_ledger_not_scoring_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    rows = read_rows(OUT)
    summary = read_one(SUMMARY)
    require(len(rows) == 4, "expected four W_time gates")
    require({row["gate_id"] for row in rows} == {
        "G1_SOURCE_SIDE_W_TIME_BASIS",
        "G2_REVIEW_PACKAGE",
        "G3_COMPLETED_REVIEW_RESPONSE",
        "G4_REPLAY_RUN_TEMPLATE",
    }, "gate set mismatch")
    require(summary["gate_count"] == "4", "bad gate count")
    require(summary["endpoint_validation_claimed"] == "false", "ledger must not claim validation")
    require(summary["physical_validation_claimed"] == "false", "ledger must not claim physical validation")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    for row in rows:
        require(row["endpoint_validation_claimed"] == "false", "row must not claim validation")
        require(row["physical_validation_claimed"] == "false", "row must not claim physical validation")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
    g3 = next(row for row in rows if row["gate_id"] == "G3_COMPLETED_REVIEW_RESPONSE")
    if summary["completed_review_response_exists"] == "false":
        require(summary["status"] == "SCORING_BLOCKED_AWAITING_REVIEW_RESPONSE", "missing response should block scoring")
        require(summary["endpoint_replay_allowed"] == "false", "missing response must keep replay false")
        require(g3["status"] == "BLOCKED_RESPONSE_MISSING_OR_NOT_GO", "G3 should be blocked")
    print(
        "PAPER10_W_TIME_GATE_STATUS_LEDGER_VALIDATED "
        f"status={summary['status']}"
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_row_level_lambda_policy_blocker_status_v1.csv"
SUMMARY = ROOT / "data/derived/joint_row_level_lambda_policy_blocker_status_v1_summary.csv"
DOC = ROOT / "docs/joint_row_level_lambda_policy_blocker_status_v1.md"
CLAIM_BOUNDARY = "joint_row_level_lambda_policy_blocker_not_numeric_not_scoring_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    rows = read_rows(OUT)
    summary_rows = read_rows(SUMMARY)
    require(len(rows) == 4, "expected four blocker rows")
    require(len(summary_rows) == 1, "summary must contain one row")
    summary = summary_rows[0]
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    require(summary["lambda_row_numeric_value_authorized"] == "false", "lambda numeric value must remain false")
    require(summary["t_joint_rescoring_authorized"] == "false", "rescoring must remain false")
    require(summary["endpoint_validation_claimed"] == "false", "validation must remain false")
    require(summary["verdict"] in {
        "LAMBDA_POLICY_WAITING_FOR_REVIEW_RESPONSE",
        "LAMBDA_POLICY_ACCEPTED_NUMERIC_VALUE_STILL_BLOCKED",
    }, "unexpected verdict")
    gate_status = {row["gate_id"]: row["status"] for row in rows}
    require(gate_status["LP_GATE_4_T_JOINT_RESCORING"] == "BLOCKED", "rescoring must remain blocked")
    if summary["verdict"] == "LAMBDA_POLICY_ACCEPTED_NUMERIC_VALUE_STILL_BLOCKED":
        require(gate_status["LP_GATE_3_NUMERIC_LAMBDA_VALUE"] == "OPEN_REQUIRED", "numeric lambda gate must be open-required")
    for row in rows:
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
        require(row["lambda_row_numeric_value_authorized"] == "false", "row lambda must remain false")
        require(row["t_joint_rescoring_authorized"] == "false", "row rescoring must remain false")
        require(row["endpoint_validation_claimed"] == "false", "row validation must remain false")
    text = DOC.read_text()
    for marker in [CLAIM_BOUNDARY, "policy gate only", "no numeric `lambda_row`", "no `T_joint` rescoring"]:
        require(marker in text, f"doc missing marker: {marker}")
    print(f"JOINT_ROW_LEVEL_LAMBDA_POLICY_BLOCKER_STATUS_V1_VALIDATED verdict={summary['verdict']}")


if __name__ == "__main__":
    main()

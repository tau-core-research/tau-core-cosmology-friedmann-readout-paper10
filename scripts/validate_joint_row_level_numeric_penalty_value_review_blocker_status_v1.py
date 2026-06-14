#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_row_level_numeric_penalty_value_review_blocker_status_v1.csv"
SUMMARY = ROOT / "data/derived/joint_row_level_numeric_penalty_value_review_blocker_status_v1_summary.csv"
DOC = ROOT / "docs/joint_row_level_numeric_penalty_value_review_blocker_status_v1.md"
CLAIM_BOUNDARY = "joint_row_level_numeric_penalty_value_review_blocker_not_rescoring_not_validation"


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
    require(len(rows) == 2, "expected two blocker rows")
    require(len(summary_rows) == 1, "summary must contain one row")
    summary = summary_rows[0]
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    require(summary["numeric_penalty_values_accepted"] == "true", "numeric values should be accepted")
    require(summary["cross_channel_control_alignment_authorized"] == "false", "cross-channel alignment must remain false")
    require(summary["lambda_row_numeric_value_authorized"] == "false", "lambda_row must remain false")
    require(summary["t_joint_rescoring_authorized"] == "false", "rescoring must remain false")
    require(summary["endpoint_validation_claimed"] == "false", "validation must remain false")
    require(
        summary["verdict"] == "NUMERIC_PENALTY_VALUES_ACCEPTED_FOR_RECORD_ONLY_NEXT_USE_BLOCKED",
        "unexpected verdict",
    )
    for row in rows:
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
        require(row["lambda_row_numeric_value_authorized"] == "false", "row lambda_row must remain false")
        require(row["t_joint_rescoring_authorized"] == "false", "row rescoring must remain false")
        require(row["endpoint_validation_claimed"] == "false", "row validation must remain false")
    require(
        any(row["gate_id"] == "NPV_GATE_2_NEXT_USE_BLOCKED" and row["status"] == "BLOCKED" for row in rows),
        "next-use gate must remain blocked",
    )
    text = DOC.read_text()
    for marker in [CLAIM_BOUNDARY, "accepted numeric values for record only", "not `T_joint` rescoring"]:
        require(marker in text, f"doc missing marker: {marker}")
    print(
        "JOINT_ROW_LEVEL_NUMERIC_PENALTY_VALUE_REVIEW_BLOCKER_STATUS_V1_VALIDATED "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()

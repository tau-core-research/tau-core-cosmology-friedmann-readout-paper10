#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_row_level_numeric_penalty_blocker_status_v1.csv"
SUMMARY = ROOT / "data/derived/joint_row_level_numeric_penalty_blocker_status_v1_summary.csv"
DOC = ROOT / "docs/joint_row_level_numeric_penalty_blocker_status_v1.md"
CLAIM_BOUNDARY = "joint_row_level_numeric_penalty_blocker_status_not_scoring_not_validation"


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
    require(len(rows) == 3, "expected three blocker rows")
    require(len(summary_rows) == 1, "summary must contain one row")
    summary = summary_rows[0]

    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    require(summary["review_package_ready"] == "true", "review package should be ready")
    require(summary["lambda_row_numeric_value_allowed"] == "false", "lambda_row must remain forbidden")
    require(summary["t_joint_rescoring_allowed"] == "false", "T_joint rescoring must remain forbidden")
    require(summary["endpoint_replay_allowed"] == "false", "endpoint replay must remain forbidden")
    require(summary["endpoint_validation_claimed"] == "false", "endpoint validation must be false")
    require(summary["penalty_values_computed"] == "false", "penalty values must not be computed")

    if summary["review_response_imported"] == "false":
        require(
            summary["numeric_penalty_computation_allowed"] == "false",
            "numeric penalty must remain blocked without imported response",
        )
        require(
            summary["verdict"] == "NUMERIC_PENALTY_VALUES_BLOCKED_WAITING_FOR_REVIEW_RESPONSE",
            "unexpected blocked verdict",
        )
    else:
        require(
            summary["verdict"] == "NUMERIC_PENALTY_VALUES_READY_FOR_SEPARATE_PACKAGE_NOT_RESCORING",
            "unexpected ready verdict",
        )

    gate_ids = {row["gate_id"] for row in rows}
    require(
        gate_ids == {
            "RNP_GATE_1_REVIEW_RESPONSE_IMPORTED",
            "RNP_GATE_2_NUMERIC_VALUES_ONLY",
            "RNP_GATE_3_RESCORING",
        },
        f"unexpected gate ids: {sorted(gate_ids)}",
    )
    for row in rows:
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
        require(row["lambda_row_numeric_value_allowed"] == "false", "row lambda_row must remain forbidden")
        require(row["t_joint_rescoring_allowed"] == "false", "row rescoring must remain forbidden")
        require(row["endpoint_validation_claimed"] == "false", "row validation must remain false")
    require(
        {row["status"] for row in rows if row["gate_id"] == "RNP_GATE_3_RESCORING"} == {"BLOCKED"},
        "rescoring gate must always remain blocked in this artifact",
    )

    text = DOC.read_text()
    for marker in [CLAIM_BOUNDARY, "not scoring", "never authorizes", "verdict"]:
        require(marker in text, f"doc missing marker: {marker}")

    print(
        "JOINT_ROW_LEVEL_NUMERIC_PENALTY_BLOCKER_STATUS_V1_VALIDATED "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()

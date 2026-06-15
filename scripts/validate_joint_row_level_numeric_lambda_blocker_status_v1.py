#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_row_level_numeric_lambda_blocker_status_v1.csv"
SUMMARY = ROOT / "data/derived/joint_row_level_numeric_lambda_blocker_status_v1_summary.csv"
DOC = ROOT / "docs/joint_row_level_numeric_lambda_blocker_status_v1.md"
CLAIM_BOUNDARY = "joint_row_level_numeric_lambda_blocker_not_rescoring_not_validation"


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
    require(len(rows) == 4, "expected four gate rows")
    require(len(summary_rows) == 1, "summary must contain one row")
    summary = summary_rows[0]
    allowed_verdicts = {
        "NUMERIC_LAMBDA_WAITING_FOR_REVIEW_RESPONSE",
        "NUMERIC_LAMBDA_RECORDED_RESCORING_STILL_BLOCKED",
    }
    require(summary["verdict"] in allowed_verdicts, "unexpected verdict")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    require(summary["t_joint_rescoring_authorized"] == "false", "rescoring must remain false")
    require(summary["endpoint_scoring_allowed"] == "false", "endpoint scoring must remain false")
    require(summary["endpoint_validation_claimed"] == "false", "validation must remain false")
    gate_status = {row["gate_id"]: row["status"] for row in rows}
    if summary["verdict"] == "NUMERIC_LAMBDA_RECORDED_RESCORING_STILL_BLOCKED":
        require(summary["lambda_row_numeric_value_authorized"] == "true", "lambda must be authorized")
        require(summary["lambda_row_numeric_value"] == "1.0", "lambda value must be 1.0")
        require(gate_status["NL_GATE_2_NUMERIC_LAMBDA_RECORD"] == "SATISFIED", "numeric lambda gate must be satisfied")
        require(gate_status["NL_GATE_3_T_JOINT_RESCORING"] == "BLOCKED", "rescoring must remain blocked")
    for row in rows:
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
        require(row["t_joint_rescoring_authorized"] == "false", "row rescoring flag must be false")
        require(row["endpoint_scoring_allowed"] == "false", "row endpoint scoring flag must be false")
        require(row["endpoint_validation_claimed"] == "false", "row validation flag must be false")
    text = DOC.read_text()
    for marker in [CLAIM_BOUNDARY, "numeric lambda record only", "no `T_joint` rescoring", summary["verdict"]]:
        require(marker in text, f"doc missing marker: {marker}")
    print(f"JOINT_ROW_LEVEL_NUMERIC_LAMBDA_BLOCKER_STATUS_V1_VALIDATED verdict={summary['verdict']}")


if __name__ == "__main__":
    main()

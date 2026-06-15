#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_row_level_aligned_control_value_authorization_blocker_status_v1.csv"
SUMMARY = ROOT / "data/derived/joint_row_level_aligned_control_value_authorization_blocker_status_v1_summary.csv"
DOC = ROOT / "docs/joint_row_level_aligned_control_value_authorization_blocker_status_v1.md"
CLAIM_BOUNDARY = "joint_row_level_aligned_control_value_authorization_blocker_not_rescoring_not_validation"


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
        "ALIGNED_CONTROL_VALUE_AUTHORIZATION_WAITING_FOR_REVIEW_RESPONSE",
        "ALIGNED_CONTROL_VALUE_COMPUTATION_AUTHORIZED_VALUES_STILL_UNCOMPUTED",
        "ALIGNED_CONTROL_VALUES_COMPUTED_RESCORING_STILL_BLOCKED",
    }
    require(summary["verdict"] in allowed_verdicts, "unexpected verdict")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    require(summary["aligned_joint_control_values_authorized"] == "false", "aligned values must remain false")
    require(summary["lambda_row_numeric_value_authorized"] == "false", "lambda must remain false")
    require(summary["t_joint_rescoring_authorized"] == "false", "rescoring must remain false")
    require(summary["endpoint_scoring_allowed"] == "false", "endpoint scoring must remain false")
    require(summary["endpoint_validation_claimed"] == "false", "validation must remain false")
    gate_status = {row["gate_id"]: row["status"] for row in rows}
    if summary["verdict"] == "ALIGNED_CONTROL_VALUE_COMPUTATION_AUTHORIZED_VALUES_STILL_UNCOMPUTED":
        require(gate_status["ACV_GATE_3_ALIGNED_VALUES"] == "OPEN_REQUIRED", "aligned values gate must be open-required")
        require(gate_status["ACV_GATE_4_T_JOINT_RESCORING"] == "BLOCKED", "rescoring must remain blocked")
    if summary["verdict"] == "ALIGNED_CONTROL_VALUES_COMPUTED_RESCORING_STILL_BLOCKED":
        require(summary["aligned_control_values_computed"] == "true", "aligned values computed flag must be true")
        require(gate_status["ACV_GATE_3_ALIGNED_VALUES"] == "SATISFIED", "aligned values gate must be satisfied")
        require(gate_status["ACV_GATE_4_T_JOINT_RESCORING"] == "BLOCKED", "rescoring must remain blocked")
    for row in rows:
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
        require(row["aligned_control_values_computed"] in {"true", "false"}, "row aligned values computed flag malformed")
        require(row["aligned_joint_control_values_authorized"] == "false", "row aligned values authorization flag must be false")
        require(row["lambda_row_numeric_value_authorized"] == "false", "row lambda flag must be false")
        require(row["t_joint_rescoring_authorized"] == "false", "row rescoring flag must be false")
        require(row["endpoint_scoring_allowed"] == "false", "row endpoint scoring flag must be false")
        require(row["endpoint_validation_claimed"] == "false", "row validation flag must be false")
    text = DOC.read_text()
    for marker in [CLAIM_BOUNDARY, "no `T_joint` rescoring", summary["verdict"]]:
        require(marker in text, f"doc missing marker: {marker}")
    print(f"JOINT_ROW_LEVEL_ALIGNED_CONTROL_VALUE_AUTHORIZATION_BLOCKER_STATUS_V1_VALIDATED verdict={summary['verdict']}")


if __name__ == "__main__":
    main()

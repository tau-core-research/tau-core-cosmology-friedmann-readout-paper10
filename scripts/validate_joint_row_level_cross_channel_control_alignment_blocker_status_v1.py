#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_row_level_cross_channel_control_alignment_blocker_status_v1.csv"
SUMMARY = ROOT / "data/derived/joint_row_level_cross_channel_control_alignment_blocker_status_v1_summary.csv"
DOC = ROOT / "docs/joint_row_level_cross_channel_control_alignment_blocker_status_v1.md"
CLAIM_BOUNDARY = "joint_row_level_cross_channel_control_alignment_blocker_not_scoring_not_validation"


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
    require(summary["aligned_joint_control_values_authorized"] == "false", "aligned values must remain false")
    require(summary["lambda_row_numeric_value_authorized"] == "false", "lambda numeric value must remain false")
    require(summary["t_joint_rescoring_authorized"] == "false", "rescoring must remain false")
    require(summary["endpoint_validation_claimed"] == "false", "validation must remain false")
    require(summary["verdict"] in {
        "CROSS_CHANNEL_ALIGNMENT_DESIGN_WAITING_FOR_REVIEW_RESPONSE",
        "CROSS_CHANNEL_ALIGNMENT_DESIGN_ACCEPTED_VALUES_STILL_BLOCKED",
    }, "unexpected verdict")
    gate_status = {row["gate_id"]: row["status"] for row in rows}
    require(gate_status["CCA_GATE_4_T_JOINT_RESCORING"] == "BLOCKED", "rescoring must remain blocked")
    if summary["verdict"] == "CROSS_CHANNEL_ALIGNMENT_DESIGN_ACCEPTED_VALUES_STILL_BLOCKED":
        require(gate_status["CCA_GATE_3_ALIGNED_CONTROL_VALUES"] == "OPEN_REQUIRED", "aligned values gate must be open-required")
    for row in rows:
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
        require(row["aligned_joint_control_values_authorized"] == "false", "row aligned values must remain false")
        require(row["lambda_row_numeric_value_authorized"] == "false", "row lambda must remain false")
        require(row["t_joint_rescoring_authorized"] == "false", "row rescoring must remain false")
        require(row["endpoint_validation_claimed"] == "false", "row validation must remain false")
    text = DOC.read_text()
    for marker in [CLAIM_BOUNDARY, "design gate only", "no aligned control values", "no `T_joint` rescoring"]:
        require(marker in text, f"doc missing marker: {marker}")
    print(f"JOINT_ROW_LEVEL_CROSS_CHANNEL_CONTROL_ALIGNMENT_BLOCKER_STATUS_V1_VALIDATED verdict={summary['verdict']}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_row_level_penalty_use_authorization_blocker_status_v1.csv"
SUMMARY = ROOT / "data/derived/joint_row_level_penalty_use_authorization_blocker_status_v1_summary.csv"
DOC = ROOT / "docs/joint_row_level_penalty_use_authorization_blocker_status_v1.md"
CLAIM_BOUNDARY = "joint_row_level_penalty_use_authorization_blocker_not_scoring_not_validation"


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
    require(summary["values_as_precondition_accepted"] == "true", "values precondition should be true")
    require(summary["cross_channel_control_alignment_required"] == "true", "cross-channel controls should be required")
    require(summary["future_lambda_policy_package_allowed"] == "true", "future lambda policy should be allowed")
    require(summary["lambda_row_numeric_value_authorized"] == "false", "lambda numeric value must remain false")
    require(summary["t_joint_rescoring_authorized"] == "false", "rescoring must remain false")
    require(summary["endpoint_replay_allowed"] == "false", "endpoint replay must remain false")
    require(summary["endpoint_validation_claimed"] == "false", "validation must remain false")
    require(
        summary["verdict"] == "PENALTY_USE_ROUTE_PLANNING_ALLOWED_RESCORING_STILL_BLOCKED",
        "unexpected verdict",
    )
    gate_status = {row["gate_id"]: row["status"] for row in rows}
    require(gate_status["PUA_GATE_2_CROSS_CHANNEL_CONTROL_ALIGNMENT"] == "OPEN_REQUIRED", "cross-channel gate must be open-required")
    require(gate_status["PUA_GATE_3_RESIDUAL_BLIND_LAMBDA_POLICY"] == "OPEN_REQUIRED", "lambda policy gate must be open-required")
    require(gate_status["PUA_GATE_4_T_JOINT_RESCORING"] == "BLOCKED", "rescoring must remain blocked")
    for row in rows:
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
        require(row["lambda_row_numeric_value_authorized"] == "false", "row lambda must remain false")
        require(row["t_joint_rescoring_authorized"] == "false", "row rescoring must remain false")
        require(row["endpoint_validation_claimed"] == "false", "row validation must remain false")
    text = DOC.read_text()
    for marker in [CLAIM_BOUNDARY, "route planning only", "residual-blind cross-channel control alignment", "residual-blind `lambda_row` policy"]:
        require(marker in text, f"doc missing marker: {marker}")
    print(f"JOINT_ROW_LEVEL_PENALTY_USE_AUTHORIZATION_BLOCKER_STATUS_V1_VALIDATED verdict={summary['verdict']}")


if __name__ == "__main__":
    main()

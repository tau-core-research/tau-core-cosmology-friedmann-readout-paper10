#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_row_level_scoring_readiness_v1.csv"
SUMMARY = ROOT / "data/derived/joint_row_level_scoring_readiness_v1_summary.csv"
DOC = ROOT / "docs/joint_row_level_scoring_readiness_v1.md"
CLAIM_BOUNDARY = "joint_row_level_scoring_readiness_not_scoring_not_validation"


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
    require(len(rows) == 4, "expected four readiness gates")
    require(len(summary_rows) == 1, "summary must contain one row")
    summary = summary_rows[0]
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    require(summary["endpoint_scoring_allowed"] == "false", "endpoint scoring must remain false")
    require(summary["endpoint_validation_claimed"] == "false", "validation must remain false")
    require(summary["t_joint_rescoring_authorized"] == "false", "rescoring must remain false")
    require(summary["aligned_control_values_ready"] == "true", "aligned-control values should be ready in this state")
    require(summary["numeric_lambda_package_ready"] == "true", "numeric-lambda package should be ready")
    require(summary["numeric_lambda_ready"] == "false", "numeric lambda must not be ready before completed response")
    require(
        summary["verdict"] == "ROW_LEVEL_SCORING_NOT_READY_NUMERIC_LAMBDA_RESPONSE_MISSING",
        "unexpected readiness verdict",
    )
    statuses = {row["gate_id"]: row["status"] for row in rows}
    require(statuses["JRSR_GATE_1_ALIGNED_CONTROL_VALUES"] == "SATISFIED", "aligned-control gate should be satisfied")
    require(statuses["JRSR_GATE_2_NUMERIC_LAMBDA"] == "BLOCKED", "numeric-lambda gate should be blocked")
    require(statuses["JRSR_GATE_3_T_JOINT_RESCORING_AUTHORIZATION"] == "BLOCKED", "rescoring gate must be blocked")
    require(statuses["JRSR_GATE_4_ENDPOINT_SCORING"] == "BLOCKED", "endpoint scoring gate must be blocked")
    for row in rows:
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
        require(row["endpoint_scoring_allowed"] == "false", "row endpoint scoring flag must be false")
        require(row["endpoint_validation_claimed"] == "false", "row validation flag must be false")
    text = DOC.read_text()
    for marker in [
        CLAIM_BOUNDARY,
        "not scoring; not validation",
        "missing completed numeric-lambda review",
        "separate rescoring authorization",
    ]:
        require(marker in text, f"doc missing marker: {marker}")
    print(f"JOINT_ROW_LEVEL_SCORING_READINESS_V1_VALIDATED verdict={summary['verdict']}")


if __name__ == "__main__":
    main()

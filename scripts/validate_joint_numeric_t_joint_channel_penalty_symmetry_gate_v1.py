#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_numeric_t_joint_channel_penalty_symmetry_gate_v1.csv"
SUMMARY = ROOT / "data/derived/joint_numeric_t_joint_channel_penalty_symmetry_gate_v1_summary.csv"
DOC = ROOT / "docs/joint_numeric_t_joint_channel_penalty_symmetry_gate_v1.md"
CLAIM_BOUNDARY = "joint_numeric_t_joint_channel_penalty_symmetry_gate_not_scoring_not_validation"


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
    require(len(rows) == 4, "expected four symmetry checks")
    require(len(summary_rows) == 1, "summary must contain one row")
    summary = summary_rows[0]
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "wrong claim boundary")
    require(summary["candidate_control_symmetry_scaffold_available"] == "true", "symmetry scaffold expected")
    require(summary["nontrivial_row_level_penalty_available"] == "false", "nontrivial penalty must remain unavailable")
    require(summary["penalty_admissible_now"] == "false", "penalty must remain inadmissible")
    require(summary["numeric_t_joint_rescoring_allowed"] == "false", "rescoring must remain forbidden")
    statuses = {row["check_id"]: row["status"] for row in rows}
    require(statuses["CPS_C2_CANDIDATE_CONTROL_SYMMETRY"] == "SATISFIED_SCAFFOLD_ONLY", "C2 scaffold status mismatch")
    require(statuses["CPS_C3_NONTRIVIAL_ROW_LEVEL_RULE"] == "OPEN", "C3 must remain open")
    for row in rows:
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
        require(row["numeric_t_joint_rescoring_allowed"] == "false", "row rescoring must remain false")
    text = DOC.read_text()
    for marker in [CLAIM_BOUNDARY, "candidate/control symmetric", "not a nontrivial row-level penalty"]:
        require(marker in text, f"doc missing marker: {marker}")
    print(
        "JOINT_NUMERIC_T_JOINT_CHANNEL_PENALTY_SYMMETRY_GATE_V1_VALIDATED "
        f"open={summary['checks_open_or_caveated']}"
    )


if __name__ == "__main__":
    main()

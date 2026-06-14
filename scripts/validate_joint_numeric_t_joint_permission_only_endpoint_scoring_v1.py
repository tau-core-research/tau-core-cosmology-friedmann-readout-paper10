#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_numeric_t_joint_permission_only_endpoint_scoring_v1.csv"
SUMMARY = ROOT / "data/derived/joint_numeric_t_joint_permission_only_endpoint_scoring_v1_summary.csv"
DOC = ROOT / "docs/joint_numeric_t_joint_permission_only_endpoint_scoring_v1.md"
AUTH = ROOT / "data/derived/joint_numeric_t_joint_endpoint_scoring_authorization_response_v1_summary.csv"
CLAIM_BOUNDARY = "joint_numeric_t_joint_permission_only_endpoint_scoring_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def as_float(value: str) -> float:
    return float(value)


def main() -> None:
    auth = read_one(AUTH)
    rows = read_rows(OUT)
    summary = read_one(SUMMARY)
    require(auth["decision"] == "AUTHORIZE_PERMISSION_ONLY_ENDPOINT_SCORING_NOT_VALIDATION", "missing authorization")
    require(summary["status"] == "PERMISSION_ONLY_ENDPOINT_SCORING_COMPLETE_NOT_VALIDATION", "bad status")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    require(len(rows) == int(summary["numeric_control_count"]), "row count mismatch")
    require(summary["controls_beating_or_equal_candidate"] == "0", "candidate must exceed all controls in this run")
    require(summary["candidate_rank_among_controls_plus_candidate"] == "1", "candidate rank mismatch")
    for field in ["endpoint_validation_claimed", "cosmological_validation_claimed", "physical_validation_claimed"]:
        require(summary[field] == "false", f"summary {field} must be false")
    for row in rows:
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
        require(row["control_beats_or_equals_candidate"] == "false", f"{row['control_id']} beats candidate")
        require(as_float(row["candidate_minus_control"]) > 0, f"{row['control_id']} non-positive margin")
        for field in [
            "same_t_joint_formula",
            "same_q_i_weights",
            "same_sign_and_standardization_rule",
            "same_row_scope_boundary",
        ]:
            require(row[field] == "true", f"{row['control_id']} violates {field}")
        for field in ["endpoint_validation_claimed", "cosmological_validation_claimed", "physical_validation_claimed"]:
            require(row[field] == "false", f"{row['control_id']} {field} must be false")
    doc = DOC.read_text()
    for marker in [CLAIM_BOUNDARY, "not validation", summary["candidate_minus_best_control"], summary["best_control_id"]]:
        require(marker in doc, f"doc missing marker: {marker}")
    print(
        "JOINT_NUMERIC_T_JOINT_PERMISSION_ONLY_ENDPOINT_SCORING_V1_VALIDATED "
        f"controls_beating={summary['controls_beating_or_equal_candidate']}"
    )


if __name__ == "__main__":
    main()

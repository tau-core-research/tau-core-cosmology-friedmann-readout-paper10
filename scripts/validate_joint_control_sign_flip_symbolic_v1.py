#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_control_sign_flip_symbolic_v1.csv"
SUMMARY = ROOT / "data/derived/joint_control_sign_flip_symbolic_v1_summary.csv"
DOC = ROOT / "docs/joint_control_sign_flip_symbolic_v1.md"
CLAIM_BOUNDARY = "joint_control_sign_flip_symbolic_not_scoring_not_validation"
VERDICT = "SIGN_FLIP_CONTROLS_SYMBOLICALLY_COMPLETE_NOT_SCORING"


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


def main() -> None:
    rows = read_rows(OUT)
    summary = read_one(SUMMARY)
    require(summary["verdict"] == VERDICT, "unexpected verdict")
    require(summary["active_channel_count"] == "3", "expected three channels")
    require(summary["control_count"] == "7", "expected seven nontrivial sign flips")
    require(summary["complete_nontrivial_enumeration"] == "true", "sign-flip enumeration incomplete")
    require(summary["computes_numeric_statistic_now"] == "false", "must not compute numeric statistic")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    sign_vectors = {row["sign_vector"] for row in rows}
    require(len(sign_vectors) == 7, "duplicate sign vectors")
    require("1;1;1" not in sign_vectors, "identity sign vector must not be included")
    for row in rows:
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
        require(row["complete_nontrivial_enumeration"] == "true", "row enumeration flag mismatch")
        for field in [
            "computes_numeric_statistic_now",
            "endpoint_scoring_allowed",
            "endpoint_validation_claimed",
            "cosmological_validation_claimed",
            "physical_validation_claimed",
        ]:
            require(row[field] == "false", f"{field} must remain false")
    text = DOC.read_text()
    for marker in ["nontrivial sign-flip", "not scoring", "not validation", VERDICT, CLAIM_BOUNDARY]:
        require(marker in text, f"doc missing marker: {marker}")
    print(f"JOINT_CONTROL_SIGN_FLIP_SYMBOLIC_V1_VALIDATED controls={summary['control_count']}")


if __name__ == "__main__":
    main()

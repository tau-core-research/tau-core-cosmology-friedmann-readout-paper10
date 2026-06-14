#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FAMILY = ROOT / "data/derived/joint_numeric_t_joint_shuffle_margin_diagnostic_v1.csv"
CLOSEST = ROOT / "data/derived/joint_numeric_t_joint_shuffle_margin_closest_controls_v1.csv"
SUMMARY = ROOT / "data/derived/joint_numeric_t_joint_shuffle_margin_diagnostic_v1_summary.csv"
DOC = ROOT / "docs/joint_numeric_t_joint_shuffle_margin_diagnostic_v1.md"
CLAIM_BOUNDARY = "joint_numeric_t_joint_shuffle_margin_diagnostic_not_validation"


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
    family_rows = read_rows(FAMILY)
    closest_rows = read_rows(CLOSEST)
    summary = read_one(SUMMARY)
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    require(summary["controls_beating_or_equal_candidate"] == "0", "expected 0 controls beating/equal candidate")
    require(summary["closest_control_family"] == "shuffled_channel_labels", "closest control should be shuffled-channel")
    require(as_float(summary["closest_margin"]) > 0, "closest margin must be positive")
    require(as_float(summary["next_best_to_shuffle_min_margin_ratio"]) > 100, "shuffle margin should be at least two orders thinner than next family")
    require(len(closest_rows) == 10, "expected top 10 closest controls")
    require(closest_rows[0]["control_id"] == summary["closest_control_id"], "closest list mismatch")
    for row in family_rows + closest_rows + [summary]:
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "claim boundary mismatch")
        for field in ["endpoint_validation_claimed", "cosmological_validation_claimed", "physical_validation_claimed"]:
            require(row[field] == "false", f"{field} must be false")
    for row in family_rows:
        require(row["candidate_exceeds_all_controls_in_family"] == "true", f"{row['control_family']} has non-exceeding control")
    doc = DOC.read_text()
    for marker in [CLAIM_BOUNDARY, summary["closest_margin"], summary["closest_control_id"], "not validation"]:
        require(marker in doc, f"doc missing marker: {marker}")
    print(
        "JOINT_NUMERIC_T_JOINT_SHUFFLE_MARGIN_DIAGNOSTIC_V1_VALIDATED "
        f"closest_margin={summary['closest_margin']}"
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_numeric_t_joint_closest_shuffle_decomposition_v1.csv"
SUMMARY = ROOT / "data/derived/joint_numeric_t_joint_closest_shuffle_decomposition_v1_summary.csv"
DOC = ROOT / "docs/joint_numeric_t_joint_closest_shuffle_decomposition_v1.md"
CLAIM_BOUNDARY = "joint_numeric_t_joint_closest_shuffle_decomposition_not_validation"


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
    require(len(rows) == 3, "expected exactly three active-channel decomposition rows")
    require(len(summary_rows) == 1, "summary must contain one row")
    summary = summary_rows[0]
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "wrong summary claim boundary")
    require(summary["closest_control_id"] == "channel_shuffle_002", "unexpected closest shuffle control")
    require(summary["endpoint_validation_claimed"] == "false", "endpoint validation must remain false")
    require(summary["cosmological_validation_claimed"] == "false", "cosmological validation must remain false")
    require(summary["physical_validation_claimed"] == "false", "physical validation must remain false")
    margin = float(summary["candidate_minus_control"])
    reconstructed = sum(float(row["candidate_minus_control_contribution"]) for row in rows)
    require(math.isclose(margin, reconstructed, rel_tol=0.0, abs_tol=1e-10), "decomposition contributions do not sum to margin")
    require(float(summary["weighted_q_spread"]) < 0.05, "q_i spread unexpectedly large")
    require(float(summary["candidate_z_spread"]) < 2.5, "z_i spread unexpectedly large")
    text = DOC.read_text()
    for marker in [CLAIM_BOUNDARY, "not validation", "channel-assignment diagnostic"]:
        require(marker in text, f"doc missing marker: {marker}")
    print(
        "JOINT_NUMERIC_T_JOINT_CLOSEST_SHUFFLE_DECOMPOSITION_V1_VALIDATED "
        f"margin={summary['candidate_minus_control']}"
    )


if __name__ == "__main__":
    main()

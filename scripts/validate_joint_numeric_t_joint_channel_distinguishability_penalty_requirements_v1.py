#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_numeric_t_joint_channel_distinguishability_penalty_requirements_v1.csv"
SUMMARY = ROOT / "data/derived/joint_numeric_t_joint_channel_distinguishability_penalty_requirements_v1_summary.csv"
DOC = ROOT / "docs/joint_numeric_t_joint_channel_distinguishability_penalty_requirements_v1.md"
CLAIM_BOUNDARY = "joint_numeric_t_joint_channel_distinguishability_penalty_requirements_not_scoring_not_validation"


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
    require(len(rows) == 4, "expected four penalty requirements")
    require(len(summary_rows) == 1, "summary must contain one row")
    summary = summary_rows[0]
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "wrong claim boundary")
    require(summary["source_route_distinctness_satisfied"] == "true", "source route distinctness must be satisfied")
    require(summary["source_native_penalty_admissible_now"] == "false", "penalty must not be admissible yet")
    require(summary["numeric_t_joint_rescoring_allowed"] == "false", "rescoring must remain forbidden")
    require(summary["endpoint_validation_claimed"] == "false", "endpoint validation must remain false")
    require(summary["cosmological_validation_claimed"] == "false", "cosmological validation must remain false")
    require(summary["physical_validation_claimed"] == "false", "physical validation must remain false")
    statuses = {row["requirement_id"]: row["status"] for row in rows}
    require(statuses["CDP_R1_SOURCE_ROUTE_DISTINCTNESS"] == "SATISFIED", "R1 should be satisfied")
    require(statuses["CDP_R2_SOURCE_NATIVE_SEPARATION_METRIC"] == "OPEN", "R2 must remain open")
    require(statuses["CDP_R4_CANDIDATE_CONTROL_SYMMETRY"] == "REQUIRED_NOT_BUILT", "R4 must remain not built")
    for row in rows:
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
        require(row["endpoint_validation_claimed"] == "false", "row endpoint validation must remain false")
    text = DOC.read_text()
    for marker in [CLAIM_BOUNDARY, "penalty not admissible yet", "residual-blind"]:
        require(marker in text, f"doc missing marker: {marker}")
    print(
        "JOINT_NUMERIC_T_JOINT_CHANNEL_DISTINGUISHABILITY_PENALTY_REQUIREMENTS_V1_VALIDATED "
        f"open={summary['requirements_open_or_caveated']}"
    )


if __name__ == "__main__":
    main()

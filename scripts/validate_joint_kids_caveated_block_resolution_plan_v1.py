#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_kids_caveated_block_resolution_plan_v1.csv"
SUMMARY = ROOT / "data/derived/joint_kids_caveated_block_resolution_plan_v1_summary.csv"
DOC = ROOT / "docs/joint_kids_caveated_block_resolution_plan_v1.md"
CLAIM_BOUNDARY = "joint_kids_caveated_block_resolution_plan_not_validation"
EXPECTED_ORDER = [
    "B2_operator_leakage_theorem_open",
    "B3_gauge_quotient_descent_open",
    "B4_response_unit_normalization_open",
    "B5_standard_lensing_null_amplitude_theorem_open",
    "B1_survey_native_operator_theorem_open",
]


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path.relative_to(ROOT)}")
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
    require(len(rows) == 5, "expected five resolution rows")
    require([row["blocker_id"] for row in rows] == EXPECTED_ORDER, "unexpected resolution order")
    require(summary["open_resolution_steps"] == "5", "summary step count mismatch")
    require(summary["current_joint_block_status"] == "caveated", "KiDS block must remain caveated")
    require(summary["can_promote_kids_block_to_clean_joint_support"] == "false", "KiDS block must not be promoted")
    require(
        summary["b1_synthesis_verdict"]
        == "SURVEY_NATIVE_OPERATOR_THEOREM_SYNTHESIS_HAS_SOURCE_SKELETON_BUT_PROOF_CHAIN_REMAINS_OPEN",
        "B1 synthesis verdict mismatch",
    )
    require(summary["b1_operator_skeleton_constructed"] == "true", "B1 skeleton should be present")
    require(summary["b1_operator_theorem_proven"] == "false", "B1 theorem must remain open")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    require(
        rows[-1]["source_artifact"]
        == "data/derived/kids1000_cosebis_survey_native_operator_theorem_closure_attempt_v1_summary.csv",
        "B1 row must cite the theorem synthesis artifact",
    )
    for row in rows:
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
        require(row["latest_closure_verdict"], "row missing latest closure verdict")
        for field in [
            "computes_new_scores",
            "endpoint_scoring_allowed",
            "endpoint_validation_claimed",
            "cosmological_validation_claimed",
            "physical_validation_claimed",
        ]:
            require(row[field] == "false", f"{field} must remain false")
    for field in [
        "endpoint_scoring_allowed",
        "endpoint_validation_claimed",
        "cosmological_validation_claimed",
        "physical_validation_claimed",
    ]:
        require(summary[field] == "false", f"summary {field} must remain false")
    text = DOC.read_text()
    for marker in [
        "operator leakage theorem",
        "gauge quotient descent",
        "response unit normalization",
        "standard-lensing null-amplitude theorem",
        "survey-native operator theorem",
        CLAIM_BOUNDARY,
    ]:
        require(marker in text, f"doc missing marker: {marker}")
    print(
        "JOINT_KIDS_CAVEATED_BLOCK_RESOLUTION_PLAN_V1_VALIDATED "
        f"steps={summary['open_resolution_steps']}"
    )


if __name__ == "__main__":
    main()

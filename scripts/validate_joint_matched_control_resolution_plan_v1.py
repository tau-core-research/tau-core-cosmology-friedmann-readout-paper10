#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_matched_control_resolution_plan_v1.csv"
SUMMARY = ROOT / "data/derived/joint_matched_control_resolution_plan_v1_summary.csv"
DOC = ROOT / "docs/joint_matched_control_resolution_plan_v1.md"
CLAIM_BOUNDARY = "joint_matched_control_resolution_plan_not_scoring_not_validation"
EXPECTED_FAMILIES = [
    "shuffled_channel_labels",
    "wrong_channel_or_wrong_family_controls",
    "sign_flip_controls",
    "leave_one_probe_or_block_drop",
    "null_readout_controls",
    "scope_and_forbidden_input_controls",
    "single_statistic_binding",
    "covariance_binding",
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
    require([row["control_family"] for row in rows] == EXPECTED_FAMILIES, "unexpected control family order")
    require(summary["control_families_total"] == "8", "summary control count mismatch")
    require(summary["implementation_ready_now"] == "false", "implementation must remain blocked")
    require(summary["same_statistic_required_for_all_controls"] == "true", "same-statistic requirement missing")
    require(summary["same_covariance_required_for_all_controls"] == "true", "same-covariance requirement missing")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    for row in rows:
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
        require(row["exit_condition"].endswith("same_statistic_same_covariance"), "bad exit condition")
        for field in [
            "allowed_to_score_now",
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
    for marker in EXPECTED_FAMILIES + [CLAIM_BOUNDARY, "not scoring"]:
        marker_text = marker.replace("_", "-") if marker == "wrong_channel_or_wrong_family_controls" else marker
        if marker not in text and marker_text not in text:
            raise SystemExit(f"doc missing marker: {marker}")
    print(
        "JOINT_MATCHED_CONTROL_RESOLUTION_PLAN_V1_VALIDATED "
        f"controls={summary['control_families_total']}"
    )


if __name__ == "__main__":
    main()

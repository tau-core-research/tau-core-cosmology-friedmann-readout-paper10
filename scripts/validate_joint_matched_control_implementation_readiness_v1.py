#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_matched_control_implementation_readiness_v1.csv"
SUMMARY = ROOT / "data/derived/joint_matched_control_implementation_readiness_v1_summary.csv"
DOC = ROOT / "docs/joint_matched_control_implementation_readiness_v1.md"
CLAIM_BOUNDARY = "joint_matched_control_implementation_readiness_not_scoring_not_validation"
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
    require(len(rows) == 8, "expected eight control readiness rows")
    require([row["control_family"] for row in rows] == EXPECTED_FAMILIES, "unexpected control family order")
    require(summary["control_families_total"] == "8", "bad control-family count")
    require(summary["design_ready_protocol_blocked"] == "6", "expected six design-ready protocol-blocked controls")
    require(summary["upstream_blocked"] == "2", "expected two upstream-blocked controls")
    require(summary["single_statistic_defined"] == "false", "single statistic must remain undefined")
    require(summary["ready_for_single_statistic_protocol"] == "false", "single-statistic protocol must remain blocked")
    require(summary["cross_probe_covariance_defined"] == "false", "cross-probe covariance must remain undefined")
    require(summary["implementation_ready_for_scoring"] == "false", "implementation must not be scoring-ready")
    require(
        summary["verdict"] == "MATCHED_CONTROL_IMPLEMENTATION_READINESS_HAS_DESIGNS_BUT_PROTOCOL_BINDING_BLOCKED",
        "bad verdict",
    )
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    for field in [
        "endpoint_scoring_allowed",
        "endpoint_validation_claimed",
        "cosmological_validation_claimed",
        "physical_validation_claimed",
    ]:
        require(summary[field] == "false", f"summary {field} must remain false")

    for index, row in enumerate(rows):
        expected = "DESIGN_READY_PROTOCOL_BLOCKED" if index < 6 else "UPSTREAM_BLOCKED"
        require(row["readiness_status"] == expected, f"{row['control_family']} readiness mismatch")
        require(row["same_statistic_required"] == "true", f"{row['control_family']} missing same-statistic binding")
        require(row["same_covariance_required"] == "true", f"{row['control_family']} missing same-covariance binding")
        require(row["future_builder"].startswith("scripts/build_"), f"{row['control_family']} missing future builder")
        require(row["future_validator"].startswith("scripts/validate_"), f"{row['control_family']} missing future validator")
        require(row["future_artifact"].startswith("data/derived/"), f"{row['control_family']} missing future artifact")
        require(row["exit_condition"], f"{row['control_family']} missing exit condition")
        require(row["allowed_next_action"], f"{row['control_family']} missing allowed next action")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
        for field in [
            "allowed_to_score_now",
            "endpoint_scoring_allowed",
            "endpoint_validation_claimed",
            "cosmological_validation_claimed",
            "physical_validation_claimed",
        ]:
            require(row[field] == "false", f"{row['control_family']} {field} must remain false")

    text = DOC.read_text()
    for marker in [
        "six control families have source-side design scaffolds",
        "single joint",
        "covariance route",
        "does not run controls",
        CLAIM_BOUNDARY,
    ]:
        require(marker in text, f"doc missing marker: {marker}")
    print(
        "JOINT_MATCHED_CONTROL_IMPLEMENTATION_READINESS_V1_VALIDATED "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()

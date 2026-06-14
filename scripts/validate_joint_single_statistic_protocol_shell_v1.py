#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_single_statistic_protocol_shell_v1.csv"
SUMMARY = ROOT / "data/derived/joint_single_statistic_protocol_shell_v1_summary.csv"
DOC = ROOT / "docs/joint_single_statistic_protocol_shell_v1.md"
CLAIM_BOUNDARY = "joint_single_statistic_protocol_shell_not_scoring_not_validation"
EXPECTED_CHANNELS = [
    "kids_lensing_cosebis_low_mode",
    "observer_path_basis_low_z",
    "desi_shape_time_readout",
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
    require(len(rows) == 3, "expected three channel rows")
    require([row["channel_id"] for row in rows] == EXPECTED_CHANNELS, "unexpected active channel order")
    require(summary["active_channel_count"] == "3", "bad channel count")
    require(summary["symbolic_joint_statistic"] == "T_joint = sum_i q_i z_i", "bad symbolic statistic")
    require(summary["candidate_control_same_formula_required"] == "true", "same-formula requirement missing")
    require(summary["candidate_control_same_rows_required"] == "true", "same-row requirement missing")
    require(summary["candidate_control_same_covariance_required"] == "true", "same-covariance requirement missing")
    require(summary["single_joint_statistic_defined"] == "false", "single joint statistic must remain undefined")
    require(summary["protocol_executable"] == "false", "protocol shell must not be executable")
    require(summary["cross_probe_covariance_defined"] == "false", "cross-probe covariance must remain undefined")
    require(summary["matched_controls_ready_for_scoring"] == "false", "matched controls must not be scoring-ready")
    require(
        summary["verdict"] == "JOINT_SINGLE_STATISTIC_PROTOCOL_SHELL_FROZEN_SYMBOLIC_NOT_EXECUTABLE",
        "bad verdict",
    )
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    for field in [
        "contains_endpoint_residuals",
        "contains_new_endpoint_scores",
        "contains_fit_statistics",
        "endpoint_scoring_allowed",
        "endpoint_validation_claimed",
        "cosmological_validation_claimed",
        "physical_validation_claimed",
    ]:
        require(summary[field] == "false", f"summary {field} must remain false")
    for row in rows:
        require(row["symbolic_joint_statistic"] == "T_joint = sum_i q_i z_i", "row symbolic statistic mismatch")
        for field in [
            "same_formula_for_candidate_and_controls",
            "same_rows_for_candidate_and_controls",
            "same_covariance_for_candidate_and_controls",
        ]:
            require(row[field] == "true", f"{row['channel_id']} {field} must be true")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
        for field in [
            "uses_observed_endpoint_values",
            "computes_numeric_statistic_now",
            "protocol_executable",
            "endpoint_scoring_allowed",
            "endpoint_validation_claimed",
            "cosmological_validation_claimed",
            "physical_validation_claimed",
        ]:
            require(row[field] == "false", f"{row['channel_id']} {field} must remain false")
    text = DOC.read_text()
    for marker in [
        "Symbolic form",
        "T_joint = sum_i q_i z_i",
        "does not compute the statistic",
        "not executable",
        CLAIM_BOUNDARY,
    ]:
        require(marker in text, f"doc missing marker: {marker}")
    print(
        "JOINT_SINGLE_STATISTIC_PROTOCOL_SHELL_V1_VALIDATED "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()

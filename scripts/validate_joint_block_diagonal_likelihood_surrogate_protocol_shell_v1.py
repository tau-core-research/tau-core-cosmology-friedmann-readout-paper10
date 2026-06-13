#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_block_diagonal_likelihood_surrogate_protocol_shell_v1.csv"
SUMMARY = ROOT / "data/derived/joint_block_diagonal_likelihood_surrogate_protocol_shell_v1_summary.csv"
DOC = ROOT / "docs/joint_block_diagonal_likelihood_surrogate_protocol_shell_v1.md"
CLAIM_BOUNDARY = "joint_block_diagonal_likelihood_surrogate_protocol_shell_not_scoring_not_validation"


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


def main() -> None:
    rows = read_rows(OUT)
    summary = read_one(SUMMARY)
    expected_channels = [
        "kids_lensing_cosebis_low_mode",
        "observer_path_basis_low_z",
        "desi_shape_time_readout",
    ]
    if [row["channel_id"] for row in rows] != expected_channels:
        raise SystemExit("unexpected active channel order")
    if summary["active_channel_order"] != ";".join(expected_channels):
        raise SystemExit("summary active channel order mismatch")
    for row in rows:
        if row["claim_boundary"] != CLAIM_BOUNDARY:
            raise SystemExit(f"claim boundary mismatch for {row['channel_id']}")
        if row["block_statistic_form"] != "r_i^T C_i^{-1} r_i":
            raise SystemExit("unexpected block statistic form")
        if row["joint_surrogate_form"] != "sum_i r_i^T C_i^{-1} r_i":
            raise SystemExit("unexpected joint surrogate form")
        for flag in [
            "candidate_control_same_statistic_required",
            "candidate_control_same_covariance_required",
        ]:
            if row[flag] != "true":
                raise SystemExit(f"{flag} must be true for {row['channel_id']}")
        for flag in [
            "contains_endpoint_residuals",
            "contains_new_endpoint_scores",
            "contains_fit_statistics",
            "endpoint_scoring_allowed",
            "endpoint_validation_claimed",
            "cosmological_validation_claimed",
        ]:
            if row[flag] != "false":
                raise SystemExit(f"{flag} must remain false for {row['channel_id']}")
    if summary["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("summary claim boundary mismatch")
    if summary["single_joint_surrogate_form_declared"] != "true":
        raise SystemExit("single joint surrogate form must be declared")
    for flag in [
        "contains_endpoint_residuals",
        "contains_new_endpoint_scores",
        "contains_fit_statistics",
        "endpoint_scoring_allowed",
        "endpoint_validation_claimed",
        "cosmological_validation_claimed",
    ]:
        if summary[flag] != "false":
            raise SystemExit(f"summary {flag} must remain false")
    if summary["review_response_status"] == "not_completed":
        if summary["protocol_executable"] != "false":
            raise SystemExit("not-completed review must not make protocol executable")
        if summary["verdict"] != "JOINT_BLOCK_DIAGONAL_PROTOCOL_SHELL_DRAFT_WAITING_FOR_REVIEW_NOT_SCORING":
            raise SystemExit(f"unexpected waiting verdict: {summary['verdict']}")
    text = DOC.read_text()
    for marker in ["not scoring", "Q_{\\rm joint}^{\\rm BD}", "does not compute a score", summary["verdict"]]:
        if marker not in text:
            raise SystemExit(f"doc missing marker: {marker}")
    print(
        "JOINT_BLOCK_DIAGONAL_LIKELIHOOD_SURROGATE_PROTOCOL_SHELL_V1_VALIDATED "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()

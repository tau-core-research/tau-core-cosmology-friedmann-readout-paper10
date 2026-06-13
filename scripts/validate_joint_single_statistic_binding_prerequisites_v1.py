#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_single_statistic_binding_prerequisites_v1.csv"
SUMMARY = ROOT / "data/derived/joint_single_statistic_binding_prerequisites_v1_summary.csv"
DOC = ROOT / "docs/joint_single_statistic_binding_prerequisites_v1.md"
CLAIM_BOUNDARY = "joint_single_statistic_binding_prerequisites_not_scoring_not_validation"
EXPECTED_VERDICT = "JOINT_SINGLE_STATISTIC_BINDING_PREREQUISITES_FROZEN_PROTOCOL_BLOCKED"


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
    if len(rows) != 3:
        raise SystemExit("expected exactly three active binding rows")
    expected = ["kids_lensing_cosebis_low_mode", "observer_path_basis_low_z", "desi_shape_time_readout"]
    if [row["channel_id"] for row in rows] != expected:
        raise SystemExit("unexpected active channel order")
    for row in rows:
        if row["claim_boundary"] != CLAIM_BOUNDARY:
            raise SystemExit(f"claim boundary mismatch for {row['channel_id']}")
        for flag in ["candidate_control_same_statistic_required", "candidate_control_same_covariance_required"]:
            if row[flag] != "true":
                raise SystemExit(f"{flag} must be true for {row['channel_id']}")
        if row["ready_for_single_statistic_protocol"] != "false":
            raise SystemExit("binding rows must not be ready before covariance/statistic closure")
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
    if summary["verdict"] != EXPECTED_VERDICT:
        raise SystemExit(f"unexpected verdict: {summary['verdict']}")
    if summary["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("summary claim boundary mismatch")
    for flag in ["single_joint_statistic_defined", "covariance_or_independence_closed", "ready_for_single_statistic_protocol"]:
        if summary[flag] != "false":
            raise SystemExit(f"{flag} must remain false")
    for flag in ["endpoint_scoring_allowed", "endpoint_validation_claimed", "cosmological_validation_claimed"]:
        if summary[flag] != "false":
            raise SystemExit(f"{flag} must remain false")
    text = DOC.read_text()
    for marker in ["not scoring", "row-scope artifact", "single statistic defined", EXPECTED_VERDICT]:
        if marker not in text:
            raise SystemExit(f"doc missing marker: {marker}")
    print(
        "JOINT_SINGLE_STATISTIC_BINDING_PREREQUISITES_V1_VALIDATED "
        f"verdict={summary['verdict']} channels={summary['active_channel_count']}"
    )


if __name__ == "__main__":
    main()

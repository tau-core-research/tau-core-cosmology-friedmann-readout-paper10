#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_matched_control_suite_implementation_scaffold_v1.csv"
SUMMARY = ROOT / "data/derived/joint_matched_control_suite_implementation_scaffold_v1_summary.csv"
DOC = ROOT / "docs/joint_matched_control_suite_implementation_scaffold_v1.md"
CLAIM_BOUNDARY = "joint_matched_control_suite_implementation_scaffold_not_scoring_not_validation"
EXPECTED_VERDICT = "JOINT_MATCHED_CONTROL_SUITE_IMPLEMENTATION_SCAFFOLD_FROZEN_NOT_RUN"


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
    if len(rows) != 8:
        raise SystemExit("implementation scaffold must contain eight control families")
    for row in rows:
        if row["claim_boundary"] != CLAIM_BOUNDARY:
            raise SystemExit(f"claim boundary mismatch for {row['scaffold_id']}")
        if row["scaffold_status"] not in {"planned_not_implemented", "blocked_by_upstream_gate"}:
            raise SystemExit(f"unexpected scaffold status: {row['scaffold_status']}")
        for key in ["future_builder", "future_validator", "future_artifact", "required_freeze_input"]:
            if not row[key]:
                raise SystemExit(f"missing {key} for {row['scaffold_id']}")
        for flag in [
            "candidate_and_control_same_statistic_required",
            "candidate_and_control_same_covariance_required",
        ]:
            if row[flag] != "true":
                raise SystemExit(f"{flag} must be true for {row['scaffold_id']}")
        for flag in [
            "contains_endpoint_residuals",
            "contains_new_endpoint_scores",
            "contains_fit_statistics",
            "endpoint_scoring_allowed",
            "endpoint_validation_claimed",
            "cosmological_validation_claimed",
        ]:
            if row[flag] != "false":
                raise SystemExit(f"{flag} must remain false for {row['scaffold_id']}")

    if summary["verdict"] != EXPECTED_VERDICT:
        raise SystemExit(f"unexpected verdict: {summary['verdict']}")
    if summary["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("summary claim boundary mismatch")
    if summary["control_families"] != "8":
        raise SystemExit("expected eight control families")
    if summary["blocked_by_upstream_gate"] != "2":
        raise SystemExit("expected two upstream-blocked binding rows")
    if summary["implementation_ready"] != "false":
        raise SystemExit("implementation must not be marked ready")
    for flag in ["endpoint_scoring_allowed", "endpoint_validation_claimed", "cosmological_validation_claimed"]:
        if summary[flag] != "false":
            raise SystemExit(f"summary {flag} must remain false")
    text = DOC.read_text()
    for marker in ["not run", "future implementation checklist", "single-statistic binding", EXPECTED_VERDICT]:
        if marker not in text:
            raise SystemExit(f"doc missing marker: {marker}")
    print(
        "JOINT_MATCHED_CONTROL_SUITE_IMPLEMENTATION_SCAFFOLD_V1_VALIDATED "
        f"verdict={summary['verdict']} controls={summary['control_families']}"
    )


if __name__ == "__main__":
    main()

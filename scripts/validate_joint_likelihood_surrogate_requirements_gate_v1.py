#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_likelihood_surrogate_requirements_gate_v1.csv"
SUMMARY = ROOT / "data/derived/joint_likelihood_surrogate_requirements_gate_v1_summary.csv"
DOC = ROOT / "docs/joint_likelihood_surrogate_requirements_gate_v1.md"
CLAIM_BOUNDARY = "joint_likelihood_surrogate_requirements_gate_not_scoring_not_validation"
EXPECTED_VERDICT = "JOINT_LIKELIHOOD_SURROGATE_REQUIREMENTS_FROZEN_SCORING_BLOCKED"


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
        raise SystemExit("requirements gate must contain eight rows")
    if not DOC.exists():
        raise SystemExit("missing requirements gate documentation")
    statuses = {row["requirement_id"]: row["status"] for row in rows}
    for required in [
        "JLS_REQ_01_QI_SOURCE_REVIEW",
        "JLS_REQ_02_ACTIVE_CHANNEL_SET",
        "JLS_REQ_03_PREFLIGHT_SIGNAL",
        "JLS_REQ_07_FORBIDDEN_FIELDS",
        "JLS_REQ_08_CLAIM_BOUNDARY",
    ]:
        if statuses.get(required) != "pass":
            raise SystemExit(f"expected pass for {required}")
    for blocked in ["JLS_REQ_04_COVARIANCE_MODEL", "JLS_REQ_05_JOINT_STATISTIC", "JLS_REQ_06_CONTROL_SUITE"]:
        if statuses.get(blocked) != "blocked":
            raise SystemExit(f"expected blocked for {blocked}")
    for row in rows:
        if row["claim_boundary"] != CLAIM_BOUNDARY:
            raise SystemExit(f"claim boundary mismatch for {row['requirement_id']}")
        for flag in ["endpoint_scoring_allowed", "endpoint_validation_claimed", "cosmological_validation_claimed"]:
            if row[flag] != "false":
                raise SystemExit(f"{flag} must remain false for {row['requirement_id']}")
    if summary["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("summary claim boundary mismatch")
    if summary["verdict"] != EXPECTED_VERDICT:
        raise SystemExit(f"unexpected verdict: {summary['verdict']}")
    if summary["endpoint_scoring_allowed"] != "false":
        raise SystemExit("endpoint scoring must remain blocked")
    if summary["endpoint_validation_claimed"] != "false" or summary["cosmological_validation_claimed"] != "false":
        raise SystemExit("validation flags must remain false")
    if int(summary["hard_blockers_open"]) != 3:
        raise SystemExit("expected exactly three hard blockers: covariance, statistic, controls")
    text = DOC.read_text()
    for marker in ["not scoring", "covariance", "single joint", EXPECTED_VERDICT]:
        if marker not in text:
            raise SystemExit(f"doc missing marker: {marker}")
    print(
        "JOINT_LIKELIHOOD_SURROGATE_REQUIREMENTS_GATE_V1_VALIDATED "
        f"verdict={summary['verdict']} hard_blockers_open={summary['hard_blockers_open']}"
    )


if __name__ == "__main__":
    main()

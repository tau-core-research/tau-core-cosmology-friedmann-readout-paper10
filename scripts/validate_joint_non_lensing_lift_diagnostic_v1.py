#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_non_lensing_lift_diagnostic_v1.csv"
SUMMARY = ROOT / "data/derived/joint_non_lensing_lift_diagnostic_v1_summary.csv"
DOC = ROOT / "docs/joint_non_lensing_lift_diagnostic_v1.md"
CLAIM_BOUNDARY = "joint_non_lensing_lift_diagnostic_not_validation"


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
    if not DOC.exists():
        raise SystemExit("missing non-lensing lift diagnostic documentation")
    if int(summary["active_non_lensing_channels"]) != len(rows):
        raise SystemExit("non-lensing row count mismatch")
    for row in rows:
        if row["claim_boundary"] != CLAIM_BOUNDARY:
            raise SystemExit(f"bad claim boundary for {row['channel_id']}")
        for flag in ["endpoint_validation_claimed", "cosmological_validation_claimed"]:
            if row[flag] != "false":
                raise SystemExit(f"{flag} must remain false for {row['channel_id']}")
        if float(row["max_additional_lift_if_channel_reaches_score_1"]) < 0.0:
            raise SystemExit("negative max lift is invalid")
    for flag in ["endpoint_validation_claimed", "cosmological_validation_claimed"]:
        if summary[flag] != "false":
            raise SystemExit(f"summary {flag} must remain false")
    if summary["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("summary claim boundary mismatch")
    if float(summary["required_lift_to_zero"]) <= 0.0:
        raise SystemExit("this diagnostic should be active only when non-lensing block is not positive")
    if "VALIDATION" in summary["verdict"] and "NOT_VALIDATION" not in summary["verdict"]:
        raise SystemExit("verdict risks validation overclaim")
    print(
        "JOINT_NON_LENSING_LIFT_DIAGNOSTIC_V1_VALIDATED "
        f"required_lift={summary['required_lift_to_zero']} "
        f"priority={summary['highest_lift_priority_channel']}"
    )


if __name__ == "__main__":
    main()

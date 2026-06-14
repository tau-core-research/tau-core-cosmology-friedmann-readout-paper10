#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_permission_replay_promotion_readiness_gate_v1.csv"
SUMMARY = ROOT / "data/derived/joint_permission_replay_promotion_readiness_gate_v1_summary.csv"
DOC = ROOT / "docs/joint_permission_replay_promotion_readiness_gate_v1.md"
CLAIM_BOUNDARY = "joint_permission_replay_promotion_readiness_not_validation"


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
    require(len(rows) == int(summary["criteria_total"]), "criteria count mismatch")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    for row in rows:
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
        for field in [
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
    require(
        summary["verdict"]
        in {
            "JOINT_PERMISSION_REPLAY_PROMOTION_READY_FOR_SEPARATE_VALIDATION_PROTOCOL",
            "JOINT_PERMISSION_REPLAY_POSITIVE_BUT_PROMOTION_BLOCKED_NOT_VALIDATION",
        },
        "unexpected verdict",
    )
    require(
        summary["promotion_ready_for_validation_protocol"] == "false"
        or summary["hard_blockers_open"] == "0",
        "promotion-ready flag inconsistent with blockers",
    )
    text = DOC.read_text()
    for marker in [
        "not endpoint scoring",
        "not endpoint validation",
        "not cosmological validation",
        summary["verdict"],
        CLAIM_BOUNDARY,
    ]:
        require(marker in text, f"doc missing marker: {marker}")
    print(
        "JOINT_PERMISSION_REPLAY_PROMOTION_READINESS_GATE_V1_VALIDATED "
        f"verdict={summary['verdict']} blockers={summary['hard_blockers_open']}"
    )


if __name__ == "__main__":
    main()

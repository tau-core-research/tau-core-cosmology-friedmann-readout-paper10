#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_post_replay_validation_roadmap_v1.csv"
SUMMARY = ROOT / "data/derived/joint_post_replay_validation_roadmap_v1_summary.csv"
DOC = ROOT / "docs/joint_post_replay_validation_roadmap_v1.md"
CLAIM_BOUNDARY = "joint_post_replay_validation_roadmap_not_validation"
EXPECTED_BLOCKERS = [
    "kids_caveated_support_block",
    "covariance_or_surrogate_closure",
    "same_statistic_matched_controls",
    "separate_validation_protocol_authorization",
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
    require([row["blocker"] for row in rows] == EXPECTED_BLOCKERS, "unexpected blocker order")
    require(summary["validation_ready"] == "false", "roadmap must not be validation-ready")
    require(summary["executable_steps_now"] == "0", "roadmap must not expose executable steps")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    for row in rows:
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
        require(row["can_execute_now"] == "false", "roadmap row must not execute now")
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
    text = DOC.read_text()
    for marker in [
        "not endpoint scoring",
        "not endpoint validation",
        "not cosmological validation",
        "KiDS/COSEBIs",
        "same-statistic matched controls",
        CLAIM_BOUNDARY,
    ]:
        require(marker in text, f"doc missing marker: {marker}")
    print(
        "JOINT_POST_REPLAY_VALIDATION_ROADMAP_V1_VALIDATED "
        f"steps={summary['roadmap_steps']}"
    )


if __name__ == "__main__":
    main()

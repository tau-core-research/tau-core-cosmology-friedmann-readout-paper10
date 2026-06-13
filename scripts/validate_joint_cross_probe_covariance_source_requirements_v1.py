#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_cross_probe_covariance_source_requirements_v1.csv"
SUMMARY = ROOT / "data/derived/joint_cross_probe_covariance_source_requirements_v1_summary.csv"
DOC = ROOT / "docs/joint_cross_probe_covariance_source_requirements_v1.md"
CLAIM_BOUNDARY = "joint_cross_probe_covariance_source_requirements_not_scoring_not_validation"
EXPECTED_VERDICT = "JOINT_CROSS_PROBE_COVARIANCE_SOURCE_REQUIREMENTS_FROZEN_BLOCKED_NOT_SCORING"


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
    expected_ids = {
        "CPC_SRC_01_ACTIVE_BLOCK_SCOPE",
        "CPC_SRC_02_CROSS_COV_PRODUCT",
        "CPC_SRC_03_SHARED_SKY_AND_MASK_OVERLAP",
        "CPC_SRC_04_REDSHIFT_KERNEL_OVERLAP",
        "CPC_SRC_05_SHARED_COSMOLOGY_AND_NUISANCE",
        "CPC_SRC_06_BLOCK_DIAGONAL_LIMITS",
        "CPC_SRC_07_SAME_STATISTIC_AND_CONTROLS",
        "CPC_SRC_08_FORBIDDEN_FIELDS",
    }
    if {row["requirement_id"] for row in rows} != expected_ids:
        raise SystemExit("requirement ids mismatch")
    for row in rows:
        if row["claim_boundary"] != CLAIM_BOUNDARY:
            raise SystemExit(f"claim boundary mismatch for {row['requirement_id']}")
        if row["endpoint_scoring_allowed"] != "false":
            raise SystemExit(f"scoring must remain false for {row['requirement_id']}")
    if summary["verdict"] != EXPECTED_VERDICT:
        raise SystemExit(f"unexpected verdict: {summary['verdict']}")
    for field in [
        "covariance_product_route_ready",
        "independence_rationale_route_ready",
        "endpoint_scoring_allowed",
        "endpoint_validation_claimed",
        "cosmological_validation_claimed",
    ]:
        if summary[field] != "false":
            raise SystemExit(f"summary {field} must be false")
    if int(summary["open_or_partial_blockers"]) < 1:
        raise SystemExit("expected open blockers")
    if summary["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("summary claim boundary mismatch")
    text = DOC.read_text()
    for marker in [
        "not scoring",
        "source-frozen cross-probe covariance",
        "block-diagonal independence",
        EXPECTED_VERDICT,
    ]:
        if marker not in text:
            raise SystemExit(f"doc missing marker: {marker}")
    print(
        "JOINT_CROSS_PROBE_COVARIANCE_SOURCE_REQUIREMENTS_V1_VALIDATED "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()

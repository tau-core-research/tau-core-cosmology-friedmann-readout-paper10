#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_covariance_resolution_plan_v1.csv"
SUMMARY = ROOT / "data/derived/joint_covariance_resolution_plan_v1_summary.csv"
DOC = ROOT / "docs/joint_covariance_resolution_plan_v1.md"
CLAIM_BOUNDARY = "joint_covariance_resolution_plan_not_scoring_not_validation"
EXPECTED_ROUTES = [
    "source_native_cross_probe_covariance_product",
    "caveated_block_diagonal_surrogate",
    "same_statistic_control_binding",
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
    require([row["resolution_route"] for row in rows] == EXPECTED_ROUTES, "unexpected route order")
    require(summary["cross_probe_covariance_defined"] == "false", "cross-probe covariance should remain open")
    require(summary["independence_rationale_route_ready"] == "true", "caveated independence route should be ready")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    for row in rows:
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
        for field in [
            "allowed_to_score_now",
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
        "source-native or source-frozen cross-probe covariance",
        "caveated block-diagonal surrogate",
        "same-statistic matched-control",
        CLAIM_BOUNDARY,
    ]:
        require(marker in text, f"doc missing marker: {marker}")
    print(
        "JOINT_COVARIANCE_RESOLUTION_PLAN_V1_VALIDATED "
        f"routes={summary['resolution_routes_frozen']}"
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "derived" / "void_source_basis_refinement_r4_independence_preflight_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "void_source_basis_refinement_r4_independence_preflight_v1_summary.csv"
PARENT = ROOT / "data" / "derived" / "void_source_basis_refinement_r1_r3_source_attachment_v1_summary.csv"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    parent = read_one(PARENT)
    rows = read_rows(OUT)
    summary = read_one(SUMMARY)

    require(parent["endpoint_replay_allowed"] == "false", "parent R1-R3 attachment must not allow replay")
    require(summary["redshift_independence_preflight_complete"] == "true", "R4 should be complete")
    require(summary["control_resistance_preflight_complete"] == "false", "R5 must remain open")
    require(summary["leakage_review_complete"] == "false", "R6 must remain open")
    require(summary["source_unique_ready"] == "false", "R4 alone must not claim source uniqueness")
    for key in [
        "endpoint_replay_allowed",
        "computes_new_scores",
        "uses_distance_residuals",
        "uses_fit_statistics",
        "physical_validation_claimed",
    ]:
        require(summary[key] == "false", f"summary must keep {key}=false")
    require(len(rows) == int(summary["features_tested"]), "feature count mismatch")
    require(len(rows) >= 5, "expected multiple source-side feature checks")
    passing = 0
    for row in rows:
        for key in [
            "endpoint_replay_allowed",
            "contains_distance_residuals",
            "contains_fit_statistics",
            "physical_validation_claimed",
        ]:
            require(row[key] == "false", f"row must keep {key}=false")
        max_abs = float(row["max_abs_correlation"])
        threshold = float(row["low_correlation_threshold"])
        require(math.isfinite(max_abs), "max_abs_correlation must be finite")
        require(0.0 <= max_abs <= 1.0, "max_abs_correlation out of range")
        require(threshold == float(summary["low_correlation_threshold"]), "threshold mismatch")
        if row["passes_low_correlation_preflight"] == "true":
            passing += 1
            require(max_abs <= threshold + 1e-12, "passing feature exceeds threshold")
        else:
            require(max_abs > threshold - 1e-12, "failing feature below threshold")
    require(passing == int(summary["features_passing_low_correlation"]), "passing feature count mismatch")
    require(summary["best_feature"], "best feature must be populated")
    print(
        "PAPER10_VOID_SOURCE_BASIS_REFINEMENT_R4_INDEPENDENCE_PREFLIGHT_V1_VALIDATED "
        f"passing={passing}/{len(rows)} endpoint_replay_allowed=false"
    )


if __name__ == "__main__":
    main()

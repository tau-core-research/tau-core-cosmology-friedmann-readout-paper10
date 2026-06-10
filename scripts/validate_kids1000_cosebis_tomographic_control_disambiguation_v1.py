#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_tomographic_control_disambiguation_policy_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_control_disambiguation_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_control_disambiguation_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    policy = read_one(POLICY)
    rows = read_rows(OUT)
    summary = read_one(SUMMARY)
    require(policy["endpoint_validation_claimed"] == "false", "policy must not claim validation")
    require(summary["status"] == "TOMOGRAPHIC_CONTROL_DISAMBIGUATION_COMPLETE", "unexpected summary status")
    require(summary["endpoint_validation_claimed"] == "false", "summary must not claim validation")
    require(summary["computes_new_scores"] == "false", "summary must not compute new scores")
    require(summary["uses_kids_data_vector_values_for_source_selection"] == "false", "summary must not leak data into source selection")
    require(summary["better_tomographic_control_count"] == str(len(rows)), "better control count mismatch")
    require(summary["accepted_physical_alternative_count"] == "0", "no tomographic control may be accepted as physical alternative yet")
    require(summary["tomographic_controls_refute_endpoint_signal"] == "false", "controls must not refute endpoint signal")
    require(summary["tomographic_controls_block_validation"] == "true", "controls must continue to block validation")
    for row in rows:
        require(row["beats_candidate_chi2"] == "true", "disambiguation rows must be candidate-beating controls")
        require(row["accepted_as_physical_alternative"] == "false", "candidate-beating controls must not be accepted as physical alternatives")
        require(row["blocks_validation"] == "true", "candidate-beating controls must block validation")
        require(row["refutes_endpoint_signal"] == "false", "candidate-beating controls must not refute signal")
        require(row["computes_new_scores"] == "false", "disambiguation must not compute new scores")
        require(row["uses_kids_data_vector_values_for_source_selection"] == "false", "no source-selection leakage allowed")
        require(row["endpoint_validation_claimed"] == "false", "no row may claim validation")
    print(
        "PAPER10_KIDS1000_COSEBIS_TOMOGRAPHIC_CONTROL_DISAMBIGUATION_V1_VALIDATED "
        f"better_controls={len(rows)} verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()


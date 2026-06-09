#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_log_band_prior_mock_sanity_policy_v1.csv"
GRID = ROOT / "data" / "derived" / "kids1000_cosebis_log_band_prior_mock_sanity_v1_grid.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_log_band_prior_mock_sanity_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    policy = read_one(POLICY)
    grid = read_rows(GRID)
    summary = read_one(SUMMARY)
    if policy["status"] != "LOG_BAND_PRIOR_MOCK_SANITY_POLICY_FROZEN":
        raise SystemExit("unexpected mock sanity policy status")
    if policy["uses_kids_data_vector_values"] != "false" or policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("mock sanity policy must remain non-scoring and data-vector-free")
    if summary["status"] != "LOG_BAND_PRIOR_MOCK_SANITY_COMPLETE":
        raise SystemExit("unexpected mock sanity summary status")
    if summary["mock_sanity_verdict"] != "deterministic_template_recovery_pass_not_physical_mock_validation":
        raise SystemExit("unexpected mock sanity verdict")
    if summary["endpoint_validation_claimed"] != "false":
        raise SystemExit("mock sanity must not claim validation")
    if summary["all_expected_templates_recovered"] != "true":
        raise SystemExit("deterministic mock sanity should recover expected templates")
    if len(grid) != 16 or summary["grid_rows"] != "16":
        raise SystemExit("mock sanity grid row count mismatch")
    if summary["low_truth_best_template"] != "low_log_band_n^-0.5":
        raise SystemExit("low truth should recover low log-band template")
    if summary["flat_truth_best_template"] != "flat_coherent":
        raise SystemExit("flat truth should recover flat template")
    if summary["high_truth_best_template"] != "high_mode_n":
        raise SystemExit("high-mode truth should recover high-mode template")
    if summary["oscillatory_truth_best_template"] != "oscillatory_alternating":
        raise SystemExit("oscillatory truth should recover oscillatory template")
    for row in [summary, *grid]:
        if row["uses_kids_data_vector_values"] != "false":
            raise SystemExit("mock sanity rows must not use KiDS data-vector values")
        if row["uses_fit_statistics"] != "false":
            raise SystemExit("mock sanity rows must not use fit statistics")
        if row["uses_random_noise"] != "false":
            raise SystemExit("mock sanity rows must remain deterministic")
        if row["endpoint_scoring_allowed"] != "false":
            raise SystemExit("mock sanity rows must remain non-scoring")
        if row["endpoint_validation_claimed"] != "false":
            raise SystemExit("mock sanity rows must not claim validation")
        if row["claim_boundary"] != policy["claim_boundary"]:
            raise SystemExit("claim boundary mismatch")
    for row in grid:
        value = float(row["cosine_similarity"])
        if not math.isfinite(value) or not -1.0 <= value <= 1.0:
            raise SystemExit("cosine similarity out of range")
    print(
        "PAPER10_KIDS1000_COSEBIS_LOG_BAND_PRIOR_MOCK_SANITY_V1_VALIDATED "
        f"verdict={summary['mock_sanity_verdict']}"
    )


if __name__ == "__main__":
    main()

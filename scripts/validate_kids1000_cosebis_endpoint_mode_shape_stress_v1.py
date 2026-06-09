#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_endpoint_mode_shape_stress_policy_v1.csv"
GRID = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_mode_shape_stress_v1_grid.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_mode_shape_stress_v1_summary.csv"


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
    if policy["status"] != "ENDPOINT_MODE_SHAPE_STRESS_POLICY_FROZEN":
        raise SystemExit("unexpected mode-shape stress policy status")
    if policy["endpoint_validation_claimed"] != "false":
        raise SystemExit("policy must not claim validation")
    if policy["uses_kids_data_vector_values_for_source_selection"] != "false":
        raise SystemExit("policy must forbid source-selection leakage")
    if policy["retunes_source_frozen_path_mapping"] != "false":
        raise SystemExit("policy must not retune W_path")
    if summary["status"] != "KIDS1000_COSEBIS_ENDPOINT_MODE_SHAPE_STRESS_COMPLETE":
        raise SystemExit("unexpected mode-shape stress summary status")
    if len(grid) != 7:
        raise SystemExit("mode-shape stress grid should contain 7 rows")
    if summary["mode_shape_count"] != "7":
        raise SystemExit("mode shape count mismatch")
    by_shape = {row["mode_shape_id"]: row for row in grid}
    expected = {"flat", "n^-0.25", "n^-0.5_candidate", "n^-0.75", "n^-1.0", "high_sqrt_n", "high_n"}
    if set(by_shape) != expected:
        raise SystemExit("unexpected mode-shape family")
    if summary["best_mode_shape_id"] != "n^-0.5_candidate":
        raise SystemExit("candidate n^-0.5 mode shape should be best in this stress family")
    if summary["candidate_beats_flat_chi2"] != "true":
        raise SystemExit("candidate should beat flat mode shape in chi2")
    if summary["high_mode_weighting_removes_signal"] != "true":
        raise SystemExit("high-n mode shape should remove the signal in this stress test")
    if abs(float(summary["candidate_mode_shape_delta_chi2_vs_baseline"]) + 183.6152665217) > 1e-9:
        raise SystemExit("candidate delta chi2 changed unexpectedly")
    if abs(float(summary["flat_mode_shape_delta_chi2_vs_baseline"]) + 136.5504934506) > 1e-9:
        raise SystemExit("flat delta chi2 changed unexpectedly")
    if float(summary["high_n_mode_shape_delta_chi2_vs_baseline"]) != 0.0:
        raise SystemExit("high_n delta chi2 should be zero")
    for row in [summary, *grid]:
        if row["endpoint_validation_claimed"] != "false":
            raise SystemExit("mode-shape stress rows must not claim validation")
        if row["uses_kids_data_vector_values_for_scoring"] != "true":
            raise SystemExit("mode-shape stress rows should record scoring data use")
        if row["uses_kids_data_vector_values_for_source_selection"] != "false":
            raise SystemExit("mode-shape stress rows must forbid source-selection leakage")
        if row["claim_boundary"] != policy["claim_boundary"]:
            raise SystemExit("claim boundary mismatch")
    for row in grid:
        for field in [
            "mode_shape_weight_min",
            "mode_shape_weight_max",
            "mode_shape_weight_mean",
            "candidate_amplitude",
            "baseline_chi2",
            "candidate_chi2",
            "delta_chi2_vs_baseline",
            "delta_aic_vs_baseline",
        ]:
            value = float(row[field])
            if not math.isfinite(value):
                raise SystemExit(f"{field} must be finite")
    print(
        "PAPER10_KIDS1000_COSEBIS_ENDPOINT_MODE_SHAPE_STRESS_V1_VALIDATED "
        f"best_shape={summary['best_mode_shape_id']} "
        f"candidate_delta={summary['candidate_mode_shape_delta_chi2_vs_baseline']} "
        f"verdict={summary['mode_shape_stress_verdict']}"
    )


if __name__ == "__main__":
    main()

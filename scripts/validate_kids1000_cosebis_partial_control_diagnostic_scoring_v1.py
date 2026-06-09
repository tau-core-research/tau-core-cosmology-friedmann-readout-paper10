#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUN_MANIFEST = ROOT / "data" / "source_manifest" / "kids1000_cosebis_partial_control_diagnostic_scoring_v1.csv"
GRID = ROOT / "data" / "derived" / "kids1000_cosebis_partial_control_diagnostic_scoring_v1_grid.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_partial_control_diagnostic_scoring_v1_summary.csv"

BRANCHES = [
    "baseline_zero",
    "mask_sample_0",
    "mask_sample_98",
    "mask_sample_195",
    "positive_mask_mean",
    "sign_flip_positive_mean",
]


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def main() -> None:
    manifest = read_one(RUN_MANIFEST)
    summary = read_one(SUMMARY)
    with GRID.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if manifest["status"] != "PARTIAL_CONTROL_DIAGNOSTIC_SCORING_NOT_ENDPOINT_VALIDATION":
        raise SystemExit("unexpected diagnostic scoring manifest status")
    if manifest["partial_control_scoring_allowed"] != "true":
        raise SystemExit("partial-control diagnostic scoring must be explicitly allowed")
    if manifest["endpoint_scoring_allowed"] != "false":
        raise SystemExit("endpoint scoring must remain disabled")
    if summary["status"] != manifest["status"]:
        raise SystemExit("summary status mismatch")
    if summary["claim_boundary"] != "partial_control_diagnostic_scoring_not_endpoint_not_validation":
        raise SystemExit("unexpected diagnostic scoring claim boundary")
    if summary["endpoint_scoring_allowed"] != "false":
        raise SystemExit("endpoint scoring must remain disabled in summary")
    if summary["endpoint_validation_claimed"] != "false":
        raise SystemExit("diagnostic scoring must not claim endpoint validation")
    if summary["partial_control_scoring_executed"] != "true":
        raise SystemExit("partial-control diagnostic scoring must be marked executed")
    if summary["uses_kids_data_vector_values_for_scoring"] != "true":
        raise SystemExit("diagnostic scoring must disclose KiDS data-vector use for scoring")
    if summary["uses_kids_data_vector_values_for_source_selection"] != "false":
        raise SystemExit("diagnostic scoring must not use KiDS data vector for source selection")
    if summary["uses_posterior_chains"] != "false" or summary["uses_posthoc_selection"] != "false":
        raise SystemExit("diagnostic scoring must not use posterior chains or posthoc selection")
    if int(summary["n_rows"]) != 300 or int(summary["branch_count"]) != 6:
        raise SystemExit("unexpected diagnostic scoring dimensions")
    if {row["branch"] for row in rows} != set(BRANCHES):
        raise SystemExit("diagnostic scoring grid branch set mismatch")
    if len(rows) != 6:
        raise SystemExit("diagnostic scoring grid must contain one row per branch")
    baseline = next(row for row in rows if row["branch"] == "baseline_zero")
    if float(baseline["best_nonnegative_amplitude"]) != 0:
        raise SystemExit("baseline branch must have zero amplitude")
    baseline_chi2 = float(baseline["chi2"])
    baseline_aic = float(baseline["aic"])
    if abs(float(summary["baseline_chi2"]) - baseline_chi2) > 5e-8:
        raise SystemExit("baseline chi2 mismatch")
    for row in rows:
        if row["claim_boundary"] != summary["claim_boundary"]:
            raise SystemExit("grid claim boundary mismatch")
        if row["endpoint_scoring_allowed"] != "false":
            raise SystemExit("grid must keep endpoint scoring disabled")
        if row["uses_kids_data_vector_values_for_scoring"] != "true":
            raise SystemExit("grid must disclose KiDS data-vector scoring use")
        if row["uses_kids_data_vector_values_for_source_selection"] != "false":
            raise SystemExit("grid must not use KiDS data vector for source selection")
        if row["uses_posterior_chains"] != "false" or row["uses_posthoc_selection"] != "false":
            raise SystemExit("grid must not use posterior chains or posthoc selection")
        if float(row["best_nonnegative_amplitude"]) < 0:
            raise SystemExit("amplitude must be nonnegative")
        if abs(float(row["delta_chi2_vs_baseline"]) - (float(row["chi2"]) - baseline_chi2)) > 5e-8:
            raise SystemExit("delta chi2 mismatch")
        if abs(float(row["delta_aic_vs_baseline"]) - (float(row["aic"]) - baseline_aic)) > 5e-8:
            raise SystemExit("delta AIC mismatch")
    best = min(rows, key=lambda row: float(row["chi2"]))
    if summary["best_branch"] != best["branch"]:
        raise SystemExit("best branch mismatch")
    for marker in [
        "kids_data_vector_values_for_source_selection",
        "posterior_chains",
        "lensing_residuals_for_source_or_branch_selection",
        "posthoc_mask_subset_selection",
        "posthoc_weight_selection",
    ]:
        if marker not in manifest["forbidden_inputs"]:
            raise SystemExit(f"missing forbidden input marker: {marker}")
    print(
        "PAPER10_KIDS1000_COSEBIS_PARTIAL_CONTROL_DIAGNOSTIC_SCORING_V1_VALIDATED "
        f"best_branch={summary['best_branch']} "
        f"delta_chi2={summary['best_delta_chi2_vs_baseline']} "
        "endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()

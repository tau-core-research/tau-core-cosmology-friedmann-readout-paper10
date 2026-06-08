#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "data" / "source_manifest" / "sdss_multitracer_bao_rsd_full_cov_pilot_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "sdss_multitracer_bao_rsd_full_cov_pilot_v1_summary.csv"
GRID = ROOT / "data" / "derived" / "sdss_multitracer_bao_rsd_full_cov_pilot_v1_grid.csv"


def main() -> None:
    with RUN.open(newline="") as f:
        run = list(csv.DictReader(f))[0]
    with SUMMARY.open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with GRID.open(newline="") as f:
        grid_rows = list(csv.DictReader(f))
    if run["status"] != "SDSS_MULTITRACER_BAO_RSD_FULL_COV_PILOT_NOT_VALIDATION":
        raise SystemExit("run status mismatch")
    if summary["status"] != run["status"]:
        raise SystemExit("summary status mismatch")
    if summary["claim_boundary"] != "sdss_multitracer_bao_rsd_full_cov_pilot_not_validation":
        raise SystemExit("claim boundary mismatch")
    if summary["covariance_policy"] != "official_6x6_compressed_parameter_covariance":
        raise SystemExit("SDSS multitracer pilot must use official 6x6 covariance")
    if "W_VOID_MATURITY" not in summary["disabled_channels"]:
        raise SystemExit("W_void must remain disabled in this SDSS multitracer pilot")
    forbidden = run["forbidden_inputs"]
    for marker in ["distance_residuals", "growth_residuals", "posthoc_environment_labels"]:
        if marker not in forbidden:
            raise SystemExit(f"missing forbidden marker: {marker}")
    branches = {row["branch"] for row in grid_rows}
    required = {"baseline_only", "web_growth_shell", "wrong_web_sign", "deterministic_shuffled_web"}
    if not required <= branches:
        raise SystemExit(f"missing branches: {sorted(required - branches)}")
    for key in [
        "baseline_best_chi2",
        "web_best_chi2",
        "wrong_web_sign_best_chi2",
        "shuffled_web_best_chi2",
        "delta_aic_web_minus_baseline",
        "covariance_min_eigenvalue",
    ]:
        float(summary[key])
    print(
        "PAPER10_SDSS_MULTITRACER_BAO_RSD_FULL_COV_PILOT_V1_VALIDATED "
        f"delta_chi2={summary['delta_chi2_web_minus_baseline']} "
        "claim_boundary=sdss_multitracer_bao_rsd_full_cov_pilot_not_validation"
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "data" / "source_manifest" / "sdss_final_bao_rsd_growth_summary_v1.csv"


def main() -> None:
    with SUMMARY.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 6:
        raise SystemExit(f"growth summary must contain 6 rows, found {len(rows)}")
    samples = {row["sample"] for row in rows}
    required = {"MGS", "BOSS_LOWZ", "BOSS_CMASS", "eBOSS_LRG", "eBOSS_ELG", "eBOSS_QSO"}
    if samples != required:
        raise SystemExit(f"unexpected growth samples: {sorted(samples)}")
    for row in rows:
        if row["status"] != "SOURCE_NATIVE_GROWTH_SUMMARY_FROZEN_DIAGONAL_ONLY":
            raise SystemExit(f"{row['growth_product_id']}: invalid status")
        if row["endpoint_allowed"] != "false":
            raise SystemExit(f"{row['growth_product_id']}: endpoint_allowed must be false")
        if row["covariance_status"] != "DIAGONAL_ERROR_ONLY":
            raise SystemExit(f"{row['growth_product_id']}: covariance status must remain diagonal-only")
        z = float(row["z_eff"])
        fs8 = float(row["fsigma8"])
        sigma = float(row["fsigma8_sigma"])
        if not (0.0 < z < 2.0 and 0.0 < fs8 < 1.0 and sigma > 0):
            raise SystemExit(f"{row['growth_product_id']}: invalid numeric range")
        forbidden = row["forbidden_inputs"]
        for marker in ["growth_residuals", "fit_improvement_flags", "posthoc_environment_labels"]:
            if marker not in forbidden:
                raise SystemExit(f"{row['growth_product_id']}: missing forbidden marker {marker}")
    print("PAPER10_SDSS_FINAL_BAO_RSD_GROWTH_SUMMARY_V1_VALIDATED rows=6 endpoint_allowed=false")


if __name__ == "__main__":
    main()

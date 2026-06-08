#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data" / "derived" / "sdss_multitracer_bao_rsd_design_matrix_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "sdss_multitracer_bao_rsd_design_matrix_v1_summary.csv"


def main() -> None:
    with DESIGN.open(newline="") as f:
        rows = list(csv.DictReader(f))
    with SUMMARY.open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    if len(rows) != 6:
        raise SystemExit("SDSS multitracer design matrix must contain six vector entries")
    if summary["endpoint_scoring_allowed"].lower() != "false":
        raise SystemExit("SDSS multitracer design matrix must remain endpoint disabled")
    observables = [row["observable"] for row in rows]
    if observables != ["DM_over_rd", "DH_over_rd", "fsigma8", "DM_over_rd", "DH_over_rd", "fsigma8"]:
        raise SystemExit(f"unexpected observable order: {observables}")
    if any(row["W_web_applies_to_observable"] == "true" for row in rows if row["observable"] != "fsigma8"):
        raise SystemExit("W_web may apply only to fsigma8 entries in this pilot")
    cov = np.loadtxt(ROOT / rows[0]["covariance_path"])
    if cov.shape != (6, 6):
        raise SystemExit("expected 6x6 SDSS multitracer covariance")
    if float(np.linalg.eigvalsh(cov)[0]) <= 0:
        raise SystemExit("covariance is not positive definite")
    print("PAPER10_SDSS_MULTITRACER_BAO_RSD_DESIGN_MATRIX_V1_VALIDATED endpoint_allowed=false")


if __name__ == "__main__":
    main()

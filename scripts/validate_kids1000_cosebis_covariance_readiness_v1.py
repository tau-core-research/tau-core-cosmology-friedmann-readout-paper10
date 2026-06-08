#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_covariance_readiness_policy_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_covariance_readiness_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_covariance_readiness_v1_summary.csv"


def main() -> None:
    with POLICY.open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with OUT.open(newline="") as f:
        rows = list(csv.DictReader(f))
    with SUMMARY.open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    if len(rows) != 1:
        raise SystemExit("covariance readiness inventory must contain one row")
    row = rows[0]
    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("covariance readiness policy must remain endpoint disabled")
    if policy["current_inversion_allowed"] != "false":
        raise SystemExit("covariance inversion must remain disabled")
    if summary["endpoint_scoring_allowed"] != "false" or row["endpoint_scoring_allowed"] != "false":
        raise SystemExit("covariance readiness artifact must remain endpoint disabled")
    if summary["inverse_saved"] != "false" or row["inverse_saved"] != "false":
        raise SystemExit("covariance readiness artifact must not save an inverse covariance")
    for key in ["contains_predictions", "contains_residuals", "contains_fit_statistics"]:
        if summary[key] != "false" or row[key] != "false":
            raise SystemExit(f"covariance readiness artifact must not contain {key}")
    if row["covariance_shape"] != policy["expected_covariance_shape"]:
        raise SystemExit("unexpected COSEBIs covariance shape")
    if row["positive_diagonal"] != "true":
        raise SystemExit("COSEBIs covariance diagonal must be positive")
    if row["positive_definite"] != "true":
        raise SystemExit("COSEBIs covariance must be positive definite")
    if row["cholesky_ready"] != "true":
        raise SystemExit("COSEBIs covariance must be Cholesky-ready")
    if float(row["symmetry_max_abs"]) > 1.0e-10:
        raise SystemExit("COSEBIs covariance symmetry error is unexpectedly large")
    if float(row["condition_number"]) <= 1.0:
        raise SystemExit("COSEBIs covariance condition number is unexpectedly small")
    if summary["status"] != "KIDS1000_COSEBIS_COVARIANCE_READINESS_BUILT_NOT_SCORED":
        raise SystemExit("unexpected covariance readiness status")
    print("PAPER10_KIDS1000_COSEBIS_COVARIANCE_READINESS_V1_VALIDATED endpoint_allowed=false")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_covariance_inversion_policy_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_covariance_inversion_readiness_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_covariance_inversion_readiness_v1_summary.csv"


def main() -> None:
    with POLICY.open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with OUT.open(newline="") as f:
        rows = list(csv.DictReader(f))
    with SUMMARY.open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    if len(rows) != 1:
        raise SystemExit("covariance inversion readiness must contain one row")
    row = rows[0]
    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("covariance-inversion policy must remain endpoint disabled")
    if policy["current_inversion_executed"] != "false":
        raise SystemExit("covariance inversion must not be executed in the policy")
    if summary["endpoint_scoring_allowed"] != "false" or row["endpoint_scoring_allowed"] != "false":
        raise SystemExit("covariance inversion readiness must remain endpoint disabled")
    if summary["current_inversion_executed"] != "false" or row["current_inversion_executed"] != "false":
        raise SystemExit("covariance inversion must not be executed in this gate")
    if summary["inverse_saved"] != "false" or row["inverse_saved"] != "false":
        raise SystemExit("covariance inversion readiness must not save an inverse")
    if summary["contains_theory_vector"] != "false" or row["contains_theory_vector"] != "false":
        raise SystemExit("covariance inversion readiness must not contain a theory vector")
    for key in ["contains_predictions", "contains_residuals", "contains_fit_statistics"]:
        if summary[key] != "false" or row[key] != "false":
            raise SystemExit(f"covariance inversion readiness must not contain {key}")
    if row["covariance_shape"] != policy["expected_covariance_shape"]:
        raise SystemExit("unexpected covariance shape")
    if row["cholesky_ready"] != "true":
        raise SystemExit("covariance must be Cholesky-ready for the frozen future policy")
    if row["requires_frozen_theory_vector"] != "true":
        raise SystemExit("future covariance solve must require a frozen theory vector")
    if "cholesky_solve" not in row["inversion_policy"]:
        raise SystemExit("frozen inversion policy must use Cholesky solve")
    if "do_not_materialize" not in row["inverse_materialization_policy"]:
        raise SystemExit("inverse materialization must remain forbidden")
    if float(row["condition_number"]) <= 1.0:
        raise SystemExit("condition number is unexpectedly small")
    if float(row["min_eigenvalue"]) <= 0.0:
        raise SystemExit("minimum eigenvalue must be positive")
    if summary["status"] != "KIDS1000_COSEBIS_COVARIANCE_INVERSION_READINESS_BUILT_NOT_SCORED":
        raise SystemExit("unexpected covariance inversion readiness status")
    print("PAPER10_KIDS1000_COSEBIS_COVARIANCE_INVERSION_READINESS_V1_VALIDATED endpoint_allowed=false")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_covariance_inversion_policy_v1.csv"
COV_READY = ROOT / "data" / "derived" / "kids1000_cosebis_covariance_readiness_v1_summary.csv"
COV_SUB = ROOT / "data" / "derived" / "kids1000_cosebis_covariance_subselection_inventory_v1_summary.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_covariance_inversion_readiness_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_covariance_inversion_readiness_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def main() -> None:
    policy = read_one(POLICY)
    cov_ready = read_one(COV_READY)
    cov_sub = read_one(COV_SUB)
    if policy["endpoint_scoring_allowed"].lower() != "false":
        raise SystemExit("COSEBIs covariance-inversion policy must remain endpoint disabled")
    if policy["current_inversion_executed"].lower() != "false":
        raise SystemExit("COSEBIs covariance inversion must not be executed in this gate")
    if cov_ready["cholesky_ready"].lower() != "true":
        raise SystemExit("COSEBIs covariance must be Cholesky-ready")
    if cov_ready["inverse_saved"].lower() != "false" or cov_sub["inverse_saved"].lower() != "false":
        raise SystemExit("previous covariance gates must not save an inverse")
    if cov_sub["retained_covariance_shape"] != policy["expected_covariance_shape"]:
        raise SystemExit("retained covariance shape does not match inversion policy")

    row = {
        "policy_id": policy["policy_id"],
        "parent_policy": policy["parent_policy"],
        "covariance_source_policy": policy["covariance_source_policy"],
        "inversion_policy": policy["inversion_policy"],
        "inverse_materialization_policy": policy["inverse_materialization_policy"],
        "covariance_shape": cov_sub["retained_covariance_shape"],
        "condition_number": cov_ready["condition_number"],
        "min_eigenvalue": cov_ready["min_eigenvalue"],
        "max_eigenvalue": cov_ready["max_eigenvalue"],
        "cholesky_ready": cov_ready["cholesky_ready"],
        "requires_frozen_theory_vector": policy["requires_frozen_theory_vector"],
        "current_inversion_executed": "false",
        "inverse_saved": "false",
        "endpoint_scoring_allowed": "false",
        "contains_theory_vector": "false",
        "contains_predictions": "false",
        "contains_residuals": "false",
        "contains_fit_statistics": "false",
        "claim_boundary": "kids1000_cosebis_covariance_inversion_readiness_not_validation",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(row.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(row)
    summary = dict(row)
    summary["status"] = "KIDS1000_COSEBIS_COVARIANCE_INVERSION_READINESS_BUILT_NOT_SCORED"
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_COVARIANCE_INVERSION_READINESS_V1_BUILT "
        f"shape={row['covariance_shape']} method=cholesky_solve inverse_saved=false endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()

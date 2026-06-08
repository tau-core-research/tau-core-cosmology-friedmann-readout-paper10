#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_covariance_subselection_policy_v1.csv"
MASK = ROOT / "data" / "derived" / "kids1000_cosebis_mask_modecut_inventory_v1.csv"
COV_READY = ROOT / "data" / "derived" / "kids1000_cosebis_covariance_readiness_v1_summary.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_covariance_subselection_inventory_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_covariance_subselection_inventory_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def main() -> None:
    policy = read_one(POLICY)
    cov_ready = read_one(COV_READY)
    if policy["endpoint_scoring_allowed"].lower() != "false":
        raise SystemExit("COSEBIs covariance-subselection policy must remain endpoint disabled")
    if policy["current_inversion_allowed"].lower() != "false":
        raise SystemExit("COSEBIs covariance inversion must remain disabled in this gate")
    if cov_ready["inverse_saved"].lower() != "false":
        raise SystemExit("COSEBIs covariance readiness artifact must not save an inverse")
    if cov_ready["covariance_shape"] != policy["expected_full_covariance_shape"]:
        raise SystemExit("COSEBIs covariance readiness shape does not match subselection policy")

    with MASK.open(newline="") as f:
        mask_rows = list(csv.DictReader(f))

    rows: list[dict[str, str]] = []
    start = 0
    for row in mask_rows:
        retained = int(row["retained_rows_for_pair"])
        end = start + retained - 1
        rows.append(
            {
                "policy_id": policy["policy_id"],
                "parent_policy": policy["parent_policy"],
                "pair_id": row["pair_id"],
                "bin1": row["bin1"],
                "bin2": row["bin2"],
                "retained_rows_for_pair": str(retained),
                "covariance_row_start_zero_based": str(start),
                "covariance_row_end_zero_based": str(end),
                "covariance_col_start_zero_based": str(start),
                "covariance_col_end_zero_based": str(end),
                "subselection_action": "retain_pair_block",
                "dropped_covariance_rows": "0",
                "dropped_covariance_cols": "0",
                "uses_residuals": "false",
                "uses_fit_statistics": "false",
                "uses_posterior_chains": "false",
                "inverse_saved": "false",
                "current_inversion_allowed": "false",
                "endpoint_scoring_allowed": "false",
                "contains_predictions": "false",
                "contains_residuals": "false",
                "contains_fit_statistics": "false",
                "claim_boundary": "kids1000_cosebis_covariance_subselection_inventory_not_validation",
            }
        )
        start = end + 1

    retained_rows = sum(int(row["retained_rows_for_pair"]) for row in rows)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "policy_id": policy["policy_id"],
        "status": "KIDS1000_COSEBIS_COVARIANCE_SUBSELECTION_INVENTORY_BUILT_NOT_SCORED",
        "subselection_policy": policy["subselection_policy"],
        "full_covariance_shape": cov_ready["covariance_shape"],
        "retained_covariance_shape": policy["expected_retained_covariance_shape"],
        "retained_rows": str(retained_rows),
        "dropped_covariance_rows": "0",
        "dropped_covariance_cols": "0",
        "n_pair_blocks": str(len(rows)),
        "full_covariance_retained": "true" if retained_rows == int(policy["expected_retained_rows"]) else "false",
        "uses_residuals": "false",
        "uses_fit_statistics": "false",
        "uses_posterior_chains": "false",
        "inverse_saved": "false",
        "current_inversion_allowed": "false",
        "endpoint_scoring_allowed": "false",
        "contains_predictions": "false",
        "contains_residuals": "false",
        "contains_fit_statistics": "false",
        "claim_boundary": "kids1000_cosebis_covariance_subselection_inventory_not_validation",
    }
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_COVARIANCE_SUBSELECTION_INVENTORY_V1_BUILT "
        f"retained_shape={summary['retained_covariance_shape']} dropped=0 endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()

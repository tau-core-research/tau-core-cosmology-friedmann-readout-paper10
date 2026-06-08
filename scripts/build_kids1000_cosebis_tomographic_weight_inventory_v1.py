#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_tomographic_weight_policy_v1.csv"
MASK = ROOT / "data" / "derived" / "kids1000_cosebis_mask_modecut_inventory_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_weight_inventory_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_weight_inventory_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def main() -> None:
    policy = read_one(POLICY)
    if policy["endpoint_scoring_allowed"].lower() != "false":
        raise SystemExit("COSEBIs tomographic-weight policy must remain endpoint disabled")
    if policy["statistical_likelihood_weighting_allowed"].lower() != "false":
        raise SystemExit("COSEBIs tomographic retention weights must not be likelihood weights")
    with MASK.open(newline="") as f:
        mask_rows = list(csv.DictReader(f))
    rows: list[dict[str, str]] = []
    for row in mask_rows:
        rows.append(
            {
                "policy_id": policy["policy_id"],
                "parent_policy": policy["parent_policy"],
                "pair_id": row["pair_id"],
                "bin1": row["bin1"],
                "bin2": row["bin2"],
                "retained_rows_for_pair": row["retained_rows_for_pair"],
                "retained_modes": row["retained_modes"],
                "retention_weight": "1.000000",
                "weight_type": "source_retention_weight_not_likelihood_weight",
                "weight_source": "predeclared_unit_weight_all_pairs",
                "uses_residuals": "false",
                "uses_fit_statistics": "false",
                "uses_posterior_chains": "false",
                "statistical_likelihood_weighting_allowed": "false",
                "endpoint_scoring_allowed": "false",
                "contains_predictions": "false",
                "contains_residuals": "false",
                "contains_fit_statistics": "false",
                "claim_boundary": "kids1000_cosebis_tomographic_weight_inventory_not_validation",
            }
        )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    weights = [float(row["retention_weight"]) for row in rows]
    summary = {
        "policy_id": policy["policy_id"],
        "status": "KIDS1000_COSEBIS_TOMOGRAPHIC_WEIGHT_INVENTORY_BUILT_NOT_SCORED",
        "weight_policy": policy["weight_policy"],
        "n_tomographic_pairs": str(len(rows)),
        "rows_per_pair": policy["expected_rows_per_pair"],
        "min_retention_weight": f"{min(weights):.6f}",
        "max_retention_weight": f"{max(weights):.6f}",
        "sum_retention_weight": f"{sum(weights):.6f}",
        "all_pairs_unit_weight": "true" if set(weights) == {1.0} else "false",
        "uses_residuals": "false",
        "uses_fit_statistics": "false",
        "uses_posterior_chains": "false",
        "statistical_likelihood_weighting_allowed": "false",
        "endpoint_scoring_allowed": "false",
        "contains_predictions": "false",
        "contains_residuals": "false",
        "contains_fit_statistics": "false",
        "claim_boundary": "kids1000_cosebis_tomographic_weight_inventory_not_validation",
    }
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_TOMOGRAPHIC_WEIGHT_INVENTORY_V1_BUILT "
        f"pairs={len(rows)} unit_weight=true endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()

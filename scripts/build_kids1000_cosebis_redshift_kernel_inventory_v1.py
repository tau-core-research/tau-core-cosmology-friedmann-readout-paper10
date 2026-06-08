#!/usr/bin/env python3
from __future__ import annotations

import csv
import tarfile
import tempfile
from pathlib import Path

import numpy as np
from astropy.io import fits


ROOT = Path(__file__).resolve().parents[1]
PRODUCTS = ROOT / "data" / "source_manifest" / "kids1000_lensing_products_v1.csv"
LENSING_INVENTORY = ROOT / "data" / "derived" / "kids1000_lensing_inventory_v1.csv"
HDU_POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_hdu_policy_v1.csv"
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_redshift_kernel_policy_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_redshift_kernel_inventory_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_redshift_kernel_inventory_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def selected_member() -> str:
    with LENSING_INVENTORY.open(newline="") as f:
        rows = list(csv.DictReader(f))
    selected = [row for row in rows if row["selected_for_cosebis_route"] == "true"]
    if len(selected) != 1:
        raise SystemExit("expected exactly one selected COSEBIs member")
    return selected[0]["member_name"]


def sci(value: float) -> str:
    return f"{value:.12e}"


def main() -> None:
    product = read_one(PRODUCTS)
    hdu_policy = read_one(HDU_POLICY)
    policy = read_one(POLICY)
    if product["endpoint_allowed"].lower() != "false":
        raise SystemExit("KiDS product must remain endpoint disabled")
    if policy["endpoint_scoring_allowed"].lower() != "false":
        raise SystemExit("redshift-kernel policy must remain endpoint disabled")

    member = selected_member()
    with tempfile.TemporaryDirectory() as tmp:
        with tarfile.open(ROOT / product["local_path"], "r:gz") as tf:
            tf.extract(member, tmp)
        with fits.open(Path(tmp) / member, memmap=False) as hdul:
            nz = hdul[hdu_policy["selected_hdu_redshift_distribution"]].data

    z_low = np.asarray(nz["Z_LOW"], dtype=float)
    z_mid = np.asarray(nz["Z_MID"], dtype=float)
    z_high = np.asarray(nz["Z_HIGH"], dtype=float)
    dz = z_high - z_low
    rows: list[dict[str, str]] = []
    for idx in range(1, int(policy["expected_source_bins"]) + 1):
        column = f"BIN{idx}"
        values = np.asarray(nz[column], dtype=float)
        area = float(np.sum(values * dz))
        mean_z = float(np.sum(z_mid * values * dz) / area)
        nonzero = values > 0
        support_min = float(np.min(z_low[nonzero]))
        support_max = float(np.max(z_high[nonzero]))
        rows.append(
            {
                "policy_id": policy["policy_id"],
                "parent_policy": policy["parent_policy"],
                "selected_member": member,
                "selected_hdu_redshift_distribution": policy["selected_hdu_redshift_distribution"],
                "source_bin": str(idx),
                "nz_column": column,
                "nz_rows": str(len(values)),
                "z_min": sci(float(np.min(z_low))),
                "z_max": sci(float(np.max(z_high))),
                "support_z_min_nonzero": sci(support_min),
                "support_z_max_nonzero": sci(support_max),
                "area_sum_nz_dz": sci(area),
                "mean_z": sci(mean_z),
                "uses_kids_data_vector_values": "false",
                "uses_residuals": "false",
                "uses_fit_statistics": "false",
                "uses_posterior_chains": "false",
                "endpoint_scoring_allowed": "false",
                "contains_predictions": "false",
                "contains_residuals": "false",
                "contains_fit_statistics": "false",
                "claim_boundary": "kids1000_cosebis_redshift_kernel_inventory_not_validation",
            }
        )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    summary = {
        "policy_id": policy["policy_id"],
        "status": "KIDS1000_COSEBIS_REDSHIFT_KERNEL_INVENTORY_BUILT_NOT_SCORED",
        "selected_hdu_redshift_distribution": policy["selected_hdu_redshift_distribution"],
        "n_source_bins": str(len(rows)),
        "nz_rows": str(len(nz)),
        "min_mean_z": sci(min(float(row["mean_z"]) for row in rows)),
        "max_mean_z": sci(max(float(row["mean_z"]) for row in rows)),
        "kernel_mapping_computed": policy["current_kernel_mapping_computed"],
        "uses_kids_data_vector_values": "false",
        "uses_residuals": "false",
        "uses_fit_statistics": "false",
        "uses_posterior_chains": "false",
        "endpoint_scoring_allowed": "false",
        "contains_predictions": "false",
        "contains_residuals": "false",
        "contains_fit_statistics": "false",
        "claim_boundary": "kids1000_cosebis_redshift_kernel_inventory_not_validation",
    }
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_REDSHIFT_KERNEL_INVENTORY_V1_BUILT "
        f"bins={len(rows)} nz_rows={len(nz)} endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()

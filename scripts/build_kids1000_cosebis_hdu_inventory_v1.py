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
INVENTORY = ROOT / "data" / "derived" / "kids1000_lensing_inventory_v1.csv"
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_hdu_policy_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_hdu_inventory_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_hdu_inventory_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def selected_member() -> str:
    with INVENTORY.open(newline="") as f:
        rows = list(csv.DictReader(f))
    selected = [row for row in rows if row["selected_for_cosebis_route"] == "true"]
    if len(selected) != 1:
        raise SystemExit("expected exactly one selected COSEBIs member")
    return selected[0]["member_name"]


def data_shape_text(data: object) -> str:
    shape = getattr(data, "shape", None)
    if shape is None:
        return ""
    return "x".join(str(item) for item in shape)


def main() -> None:
    product = read_one(PRODUCTS)
    policy = read_one(POLICY)
    if product["endpoint_allowed"].lower() != "false" or policy["endpoint_scoring_allowed"].lower() != "false":
        raise SystemExit("KiDS COSEBIs HDU policy must remain endpoint disabled")
    member = selected_member()
    tar_path = ROOT / product["local_path"]
    rows: list[dict[str, str]] = []
    with tempfile.TemporaryDirectory() as tmp:
        with tarfile.open(tar_path, "r:gz") as tf:
            tf.extract(member, tmp)
        fits_path = Path(tmp) / member
        with fits.open(fits_path, memmap=False) as hdul:
            covariance_positive = "not_checked"
            for idx, hdu in enumerate(hdul):
                hdu_name = hdu.name or "PRIMARY"
                columns = getattr(getattr(hdu, "columns", None), "names", None)
                role = "ignored"
                if hdu_name == policy["selected_hdu_data_vector"]:
                    role = "data_vector"
                elif hdu_name == policy["selected_hdu_covariance"]:
                    role = "covariance"
                    eig = np.linalg.eigvalsh(np.asarray(hdu.data, dtype=float))
                    covariance_positive = "true" if float(eig[0]) > 0 else "false"
                elif hdu_name == policy["selected_hdu_redshift_distribution"]:
                    role = "redshift_distribution"
                rows.append(
                    {
                        "policy_id": policy["policy_id"],
                        "selected_member": member,
                        "hdu_index": str(idx),
                        "hdu_name": hdu_name,
                        "hdu_class": type(hdu).__name__,
                        "role": role,
                        "data_shape": data_shape_text(hdu.data),
                        "n_columns": str(len(columns or [])),
                        "columns": ";".join(columns or []),
                        "endpoint_scoring_allowed": "false",
                        "contains_predictions": "false",
                        "contains_residuals": "false",
                        "contains_fit_statistics": "false",
                        "claim_boundary": "kids1000_cosebis_hdu_inventory_not_validation",
                    }
                )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    role_counts = {role: sum(row["role"] == role for row in rows) for role in ["data_vector", "covariance", "redshift_distribution"]}
    summary = {
        "policy_id": policy["policy_id"],
        "status": "KIDS1000_COSEBIS_HDU_INVENTORY_BUILT_NOT_SCORED",
        "selected_member": member,
        "n_hdus": str(len(rows)),
        "n_data_vector_hdus": str(role_counts["data_vector"]),
        "n_covariance_hdus": str(role_counts["covariance"]),
        "n_redshift_distribution_hdus": str(role_counts["redshift_distribution"]),
        "data_vector_rows": next(row["data_shape"] for row in rows if row["role"] == "data_vector"),
        "covariance_shape": next(row["data_shape"] for row in rows if row["role"] == "covariance"),
        "redshift_distribution_rows": next(row["data_shape"] for row in rows if row["role"] == "redshift_distribution"),
        "covariance_positive_definite": covariance_positive,
        "endpoint_scoring_allowed": "false",
        "contains_predictions": "false",
        "contains_residuals": "false",
        "contains_fit_statistics": "false",
        "claim_boundary": "kids1000_cosebis_hdu_inventory_not_validation",
    }
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_HDU_INVENTORY_V1_BUILT "
        f"hdus={len(rows)} covariance_positive={covariance_positive} endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()

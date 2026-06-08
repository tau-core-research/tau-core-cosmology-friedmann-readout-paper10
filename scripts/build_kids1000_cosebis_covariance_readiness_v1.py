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
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_covariance_readiness_policy_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_covariance_readiness_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_covariance_readiness_v1_summary.csv"


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
    if hdu_policy["endpoint_scoring_allowed"].lower() != "false":
        raise SystemExit("COSEBIs HDU policy must remain endpoint disabled")
    if policy["endpoint_scoring_allowed"].lower() != "false":
        raise SystemExit("COSEBIs covariance readiness policy must remain endpoint disabled")
    if policy["current_inversion_allowed"].lower() != "false":
        raise SystemExit("COSEBIs covariance inversion must remain disabled in this gate")

    member = selected_member()
    tar_path = ROOT / product["local_path"]
    with tempfile.TemporaryDirectory() as tmp:
        with tarfile.open(tar_path, "r:gz") as tf:
            tf.extract(member, tmp)
        fits_path = Path(tmp) / member
        with fits.open(fits_path, memmap=False) as hdul:
            cov = np.asarray(hdul[hdu_policy["selected_hdu_covariance"]].data, dtype=float)

    if cov.ndim != 2 or cov.shape[0] != cov.shape[1]:
        raise SystemExit("COSEBIs covariance must be a square matrix")
    eig = np.linalg.eigvalsh(cov)
    diag = np.diag(cov)
    min_eig = float(eig[0])
    max_eig = float(eig[-1])
    condition_number = max_eig / min_eig if min_eig > 0 else float("inf")
    symmetry_max_abs = float(np.max(np.abs(cov - cov.T)))
    cholesky_ready = "true"
    try:
        np.linalg.cholesky(cov)
    except np.linalg.LinAlgError:
        cholesky_ready = "false"

    row = {
        "policy_id": policy["policy_id"],
        "parent_policy": policy["parent_policy"],
        "selected_member": member,
        "selected_hdu_covariance": policy["selected_hdu_covariance"],
        "covariance_shape": f"{cov.shape[0]}x{cov.shape[1]}",
        "n_rows": str(cov.shape[0]),
        "n_cols": str(cov.shape[1]),
        "symmetry_max_abs": sci(symmetry_max_abs),
        "min_diagonal": sci(float(np.min(diag))),
        "max_diagonal": sci(float(np.max(diag))),
        "min_eigenvalue": sci(min_eig),
        "max_eigenvalue": sci(max_eig),
        "condition_number": sci(condition_number),
        "positive_diagonal": "true" if float(np.min(diag)) > 0 else "false",
        "positive_definite": "true" if min_eig > 0 else "false",
        "cholesky_ready": cholesky_ready,
        "inverse_saved": "false",
        "current_inversion_allowed": "false",
        "endpoint_scoring_allowed": "false",
        "contains_predictions": "false",
        "contains_residuals": "false",
        "contains_fit_statistics": "false",
        "claim_boundary": "kids1000_cosebis_covariance_readiness_not_validation",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(row.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(row)
    with SUMMARY.open("w", newline="") as f:
        summary = dict(row)
        summary["status"] = "KIDS1000_COSEBIS_COVARIANCE_READINESS_BUILT_NOT_SCORED"
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_COVARIANCE_READINESS_V1_BUILT "
        f"shape={row['covariance_shape']} condition={row['condition_number']} endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()

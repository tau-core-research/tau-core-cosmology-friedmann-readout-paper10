#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import requests
from astropy.io import fits


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_dr4_path_mask_subset_policy_v1.csv"
HEAD_SAMPLE = ROOT / "data" / "derived" / "kids1000_dr4_path_mask_head_sample_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_dr4_path_mask_subset_inventory_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_dr4_path_mask_subset_inventory_v1_summary.csv"
RAW_DIR = ROOT / "data" / "raw" / "weak_lensing" / "kids1000_path_masks" / "mask_subset_v1"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def mask_stats(path: Path) -> dict[str, str]:
    with fits.open(path, memmap=False) as hdul:
        image = hdul[0].data
        header = hdul[0].header
        if image is None:
            raise SystemExit(f"missing image data in {path}")
        arr = np.asarray(image)
        finite = np.isfinite(arr)
        finite_values = arr[finite]
        n_pixels = int(arr.size)
        n_finite = int(finite.sum())
        nonzero = int(np.count_nonzero(finite_values))
        return {
            "hdu_count": str(len(hdul)),
            "primary_shape": "x".join(str(value) for value in arr.shape),
            "bitpix": str(header.get("BITPIX", "")),
            "naxis": str(header.get("NAXIS", "")),
            "n_pixels": str(n_pixels),
            "n_finite_pixels": str(n_finite),
            "finite_fraction": f"{(n_finite / n_pixels):.12e}" if n_pixels else "0.000000000000e+00",
            "nonzero_finite_pixels": str(nonzero),
            "nonzero_finite_fraction": f"{(nonzero / n_finite):.12e}" if n_finite else "0.000000000000e+00",
            "min_finite_value": f"{float(np.min(finite_values)):.12e}" if n_finite else "",
            "max_finite_value": f"{float(np.max(finite_values)):.12e}" if n_finite else "",
            "mean_finite_value": f"{float(np.mean(finite_values)):.12e}" if n_finite else "",
        }


def main() -> None:
    policy = read_one(POLICY)
    if policy["endpoint_scoring_allowed"].lower() != "false":
        raise SystemExit("mask subset policy must remain endpoint disabled")
    if policy["current_path_mapping_computed"].lower() != "false":
        raise SystemExit("path mapping must not be computed in this subset inventory")

    with HEAD_SAMPLE.open(newline="") as f:
        head_rows = list(csv.DictReader(f))
    requested_indices = policy["subset_indices_zero_based"].split(";")
    selected = [row for row in head_rows if row["sample_index_zero_based"] in requested_indices]
    if len(selected) != int(policy["expected_subset_count"]):
        raise SystemExit("HEAD sample does not contain the requested subset")

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    fetched_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    rows: list[dict[str, str]] = []
    for head in selected:
        url = head["mask_product_url"]
        filename = url.rsplit("/", 1)[-1]
        local_path = RAW_DIR / filename
        response = requests.get(
            url,
            timeout=60,
            headers={"User-Agent": "tau-core-paper10-kids-mask-subset-freeze/0.1"},
        )
        response.raise_for_status()
        content = response.content
        local_path.write_bytes(content)
        stats = mask_stats(local_path)
        rows.append(
            {
                "policy_id": policy["policy_id"],
                "sample_index_zero_based": head["sample_index_zero_based"],
                "mask_product_url": url,
                "local_path": str(local_path.relative_to(ROOT)),
                "http_status": str(response.status_code),
                "byte_count": str(len(content)),
                "sha256": sha256_bytes(content),
                "fetched_at_utc": fetched_at,
                **stats,
                "mask_product_fetched": "true",
                "mask_pixels_parsed": "true",
                "path_mapping_computed": "false",
                "contains_mapping_vector": "false",
                "contains_theory_vector": "false",
                "contains_predictions": "false",
                "contains_residuals": "false",
                "contains_fit_statistics": "false",
                "uses_kids_data_vector_values": "false",
                "uses_posterior_chains": "false",
                "uses_posthoc_mask_subset_selection": "false",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "kids1000_dr4_path_mask_subset_inventory_not_validation",
            }
        )

    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    summary = {
        "policy_id": policy["policy_id"],
        "status": "KIDS_DR4_PATH_MASK_SUBSET_FETCHED_INVENTORIED_NOT_SCORED",
        "subset_count": str(len(rows)),
        "total_byte_count": str(sum(int(row["byte_count"]) for row in rows)),
        "total_pixels": str(sum(int(row["n_pixels"]) for row in rows)),
        "min_nonzero_finite_fraction": f"{min(float(row['nonzero_finite_fraction']) for row in rows):.12e}",
        "max_nonzero_finite_fraction": f"{max(float(row['nonzero_finite_fraction']) for row in rows):.12e}",
        "mask_products_fetched": "true",
        "mask_pixels_parsed": "true",
        "path_mapping_computed": "false",
        "contains_mapping_vector": "false",
        "contains_theory_vector": "false",
        "contains_predictions": "false",
        "contains_residuals": "false",
        "contains_fit_statistics": "false",
        "uses_kids_data_vector_values": "false",
        "uses_posterior_chains": "false",
        "uses_posthoc_mask_subset_selection": "false",
        "endpoint_scoring_allowed": "false",
        "claim_boundary": "kids1000_dr4_path_mask_subset_inventory_not_validation",
    }
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)
    print(
        "PAPER10_KIDS_DR4_PATH_MASK_SUBSET_V1_FETCHED "
        f"subset={len(rows)} bytes={summary['total_byte_count']} endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()

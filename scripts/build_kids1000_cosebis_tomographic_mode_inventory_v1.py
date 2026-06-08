#!/usr/bin/env python3
from __future__ import annotations

import csv
import tarfile
import tempfile
from pathlib import Path

from astropy.io import fits


ROOT = Path(__file__).resolve().parents[1]
PRODUCTS = ROOT / "data" / "source_manifest" / "kids1000_lensing_products_v1.csv"
LENSING_INVENTORY = ROOT / "data" / "derived" / "kids1000_lensing_inventory_v1.csv"
HDU_POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_hdu_policy_v1.csv"
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_tomographic_mode_policy_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_mode_inventory_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_mode_inventory_v1_summary.csv"


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


def mode_text(values: list[int]) -> str:
    return ";".join(str(value) for value in values)


def main() -> None:
    product = read_one(PRODUCTS)
    hdu_policy = read_one(HDU_POLICY)
    policy = read_one(POLICY)
    if product["endpoint_allowed"].lower() != "false":
        raise SystemExit("KiDS product must remain endpoint disabled")
    if hdu_policy["endpoint_scoring_allowed"].lower() != "false":
        raise SystemExit("COSEBIs HDU policy must remain endpoint disabled")
    if policy["endpoint_scoring_allowed"].lower() != "false":
        raise SystemExit("COSEBIs tomographic/mode policy must remain endpoint disabled")

    member = selected_member()
    tar_path = ROOT / product["local_path"]
    rows: list[dict[str, str]] = []
    with tempfile.TemporaryDirectory() as tmp:
        with tarfile.open(tar_path, "r:gz") as tf:
            tf.extract(member, tmp)
        fits_path = Path(tmp) / member
        with fits.open(fits_path, memmap=False) as hdul:
            data = hdul[hdu_policy["selected_hdu_data_vector"]].data
            pairs = sorted({(int(row["BIN1"]), int(row["BIN2"])) for row in data})
            for bin1, bin2 in pairs:
                pair_rows = [
                    row
                    for row in data
                    if int(row["BIN1"]) == bin1 and int(row["BIN2"]) == bin2
                ]
                modes = sorted(int(row["ANGBIN"]) for row in pair_rows)
                rows.append(
                    {
                        "policy_id": policy["policy_id"],
                        "parent_policy": policy["parent_policy"],
                        "selected_member": member,
                        "selected_hdu_data_vector": policy["selected_hdu_data_vector"],
                        "bin1": str(bin1),
                        "bin2": str(bin2),
                        "pair_id": f"{bin1}-{bin2}",
                        "rows_for_pair": str(len(pair_rows)),
                        "mode_min": str(min(modes)),
                        "mode_max": str(max(modes)),
                        "n_modes": str(len(modes)),
                        "modes": mode_text(modes),
                        "upper_triangular_pair": "true" if bin1 <= bin2 else "false",
                        "endpoint_scoring_allowed": "false",
                        "contains_predictions": "false",
                        "contains_residuals": "false",
                        "contains_fit_statistics": "false",
                        "claim_boundary": "kids1000_cosebis_tomographic_mode_inventory_not_validation",
                    }
                )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    unique_bins = sorted({int(row["bin1"]) for row in rows} | {int(row["bin2"]) for row in rows})
    all_modes = [row["modes"] for row in rows]
    complete_mode_text = mode_text(list(range(1, int(policy["expected_modes_per_pair"]) + 1)))
    all_pairs_complete = all(
        row["rows_for_pair"] == policy["expected_modes_per_pair"]
        and row["n_modes"] == policy["expected_modes_per_pair"]
        and row["modes"] == complete_mode_text
        for row in rows
    )
    summary = {
        "policy_id": policy["policy_id"],
        "status": "KIDS1000_COSEBIS_TOMOGRAPHIC_MODE_INVENTORY_BUILT_NOT_SCORED",
        "selected_member": member,
        "selected_hdu_data_vector": policy["selected_hdu_data_vector"],
        "n_tomographic_bins": str(len(unique_bins)),
        "tomographic_bins": mode_text(unique_bins),
        "n_tomographic_pairs": str(len(rows)),
        "n_modes_per_pair": policy["expected_modes_per_pair"],
        "data_vector_rows": str(sum(int(row["rows_for_pair"]) for row in rows)),
        "mode_min": "1",
        "mode_max": policy["expected_modes_per_pair"],
        "all_pairs_upper_triangular": "true" if all(row["upper_triangular_pair"] == "true" for row in rows) else "false",
        "all_pairs_complete": "true" if all_pairs_complete else "false",
        "unique_mode_blocks": str(len(set(all_modes))),
        "endpoint_scoring_allowed": "false",
        "contains_predictions": "false",
        "contains_residuals": "false",
        "contains_fit_statistics": "false",
        "claim_boundary": "kids1000_cosebis_tomographic_mode_inventory_not_validation",
    }
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_TOMOGRAPHIC_MODE_INVENTORY_V1_BUILT "
        f"pairs={len(rows)} modes_per_pair={policy['expected_modes_per_pair']} endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRODUCTS = ROOT / "data" / "source_manifest" / "kids1000_lensing_products_v1.csv"


def main() -> None:
    with PRODUCTS.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit("KiDS lensing product manifest must contain one row")
    row = rows[0]
    if row["status"] != "SOURCE_NATIVE_PRODUCT_FETCHED_FROZEN":
        raise SystemExit("KiDS lensing tarball must be fetched/frozen")
    if row["endpoint_allowed"].lower() != "false":
        raise SystemExit("KiDS lensing product must remain endpoint disabled")
    path = ROOT / row["local_path"]
    if not path.exists():
        raise SystemExit(f"missing KiDS lensing tarball: {path}")
    if hashlib.sha256(path.read_bytes()).hexdigest() != row["sha256"]:
        raise SystemExit("KiDS lensing tarball sha256 mismatch")
    if int(row["byte_count"]) <= 0:
        raise SystemExit("KiDS lensing tarball byte count is empty")
    for marker in [
        "tomographic_bin_policy",
        "statistic_choice_COSEBIs_or_2PCF_or_bandpowers",
        "covariance_block_policy",
    ]:
        if marker not in row["endpoint_blocker"]:
            raise SystemExit(f"missing endpoint blocker marker: {marker}")
    print("PAPER10_KIDS1000_LENSING_PRODUCTS_VALIDATED endpoint_allowed=false")


if __name__ == "__main__":
    main()

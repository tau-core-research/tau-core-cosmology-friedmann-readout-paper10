#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "data" / "derived" / "void_web_source_native_inventory_v1.csv"


def main() -> None:
    if not INVENTORY.exists():
        raise SystemExit("void/web source-native inventory is missing")
    with INVENTORY.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 4:
        raise SystemExit(f"inventory must contain 4 rows, found {len(rows)}")
    blob = " ".join(row["observable_summary"] for row in rows)
    if "void_rows=" not in blob:
        raise SystemExit("inventory missing void row count")
    if "fits_bintable_rows=" not in blob:
        raise SystemExit("inventory missing FITS table row count")
    for row in rows:
        if row["endpoint_allowed"] != "false":
            raise SystemExit(f"{row['frozen_product_id']}: endpoint_allowed must be false")
        if row["contains_endpoint_scores"] != "false" or row["contains_residuals"] != "false":
            raise SystemExit(f"{row['frozen_product_id']}: inventory cannot contain scores/residuals")
    print(f"PAPER10_VOID_WEB_SOURCE_NATIVE_INVENTORY_V1_VALIDATED rows={len(rows)}")


if __name__ == "__main__":
    main()

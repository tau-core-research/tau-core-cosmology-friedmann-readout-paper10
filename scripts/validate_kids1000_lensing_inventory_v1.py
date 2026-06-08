#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "data" / "derived" / "kids1000_lensing_inventory_v1_summary.csv"
INVENTORY = ROOT / "data" / "derived" / "kids1000_lensing_inventory_v1.csv"


def main() -> None:
    with SUMMARY.open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    with INVENTORY.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if summary["status"] != "KIDS1000_LENSING_INVENTORY_BUILT_NOT_SCORED":
        raise SystemExit("KiDS lensing inventory status mismatch")
    if summary["endpoint_scoring_allowed"] != "false":
        raise SystemExit("KiDS lensing inventory must remain endpoint disabled")
    if summary["contains_residuals"] != "false" or summary["contains_fit_statistics"] != "false":
        raise SystemExit("KiDS lensing inventory must not contain residuals or fit statistics")
    if int(summary["n_members"]) != len(rows):
        raise SystemExit("KiDS lensing inventory member count mismatch")
    if int(summary["n_selected_cosebis_members"]) != 1:
        raise SystemExit("expected exactly one selected COSEBIs FITS member")
    selected = [row for row in rows if row["selected_for_cosebis_route"] == "true"]
    if not selected or selected[0]["member_kind"] != "fits_product":
        raise SystemExit("selected COSEBIs member must be a FITS product")
    if "cosebis_" not in selected[0]["member_name"]:
        raise SystemExit("selected member does not look like a COSEBIs product")
    print("PAPER10_KIDS1000_LENSING_INVENTORY_V1_VALIDATED endpoint_allowed=false")


if __name__ == "__main__":
    main()

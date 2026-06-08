#!/usr/bin/env python3
from __future__ import annotations

import csv
import fnmatch
import tarfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRODUCTS = ROOT / "data" / "source_manifest" / "kids1000_lensing_products_v1.csv"
ROUTE = ROOT / "data" / "source_manifest" / "kids1000_cosebis_lensing_route_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_lensing_inventory_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_lensing_inventory_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def member_kind(name: str) -> str:
    lower = name.lower()
    if lower.endswith(".fits"):
        return "fits_product"
    if "/chain/" in lower:
        return "posterior_chain_or_start"
    if "/config/" in lower:
        return "cosmosis_config"
    if lower.endswith(".py"):
        return "helper_script"
    if lower.endswith("read.me"):
        return "readme"
    if lower.endswith(".ds_store") or "/._" in lower:
        return "metadata_ignored"
    return "other"


def main() -> None:
    product = read_one(PRODUCTS)
    route = read_one(ROUTE)
    if product["endpoint_allowed"].lower() != "false" or route["endpoint_scoring_allowed"].lower() != "false":
        raise SystemExit("KiDS inventory inputs must remain endpoint disabled")
    tar_path = ROOT / product["local_path"]
    selected_glob = route["selected_member_glob"]
    rows: list[dict[str, str]] = []
    with tarfile.open(tar_path, "r:gz") as tf:
        for member in tf.getmembers():
            if member.isdir():
                continue
            kind = member_kind(member.name)
            selected = fnmatch.fnmatch(member.name, selected_glob)
            rows.append(
                {
                    "frozen_product_id": product["frozen_product_id"],
                    "route_id": route["route_id"],
                    "member_name": member.name,
                    "member_size": str(member.size),
                    "member_kind": kind,
                    "selected_for_cosebis_route": "true" if selected else "false",
                    "endpoint_scoring_allowed": "false",
                    "contains_residuals": "false",
                    "contains_fit_statistics": "false",
                    "claim_boundary": "kids1000_lensing_inventory_not_validation",
                }
            )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    selected_rows = [row for row in rows if row["selected_for_cosebis_route"] == "true"]
    summary = {
        "frozen_product_id": product["frozen_product_id"],
        "route_id": route["route_id"],
        "status": "KIDS1000_LENSING_INVENTORY_BUILT_NOT_SCORED",
        "n_members": str(len(rows)),
        "n_fits_products": str(sum(row["member_kind"] == "fits_product" for row in rows)),
        "n_selected_cosebis_members": str(len(selected_rows)),
        "selected_cosebis_total_bytes": str(sum(int(row["member_size"]) for row in selected_rows)),
        "endpoint_scoring_allowed": "false",
        "contains_model_predictions": "false",
        "contains_residuals": "false",
        "contains_fit_statistics": "false",
        "claim_boundary": "kids1000_lensing_inventory_not_validation",
    }
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)
    print(
        "PAPER10_KIDS1000_LENSING_INVENTORY_V1_BUILT "
        f"members={len(rows)} selected_cosebis={len(selected_rows)} endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()

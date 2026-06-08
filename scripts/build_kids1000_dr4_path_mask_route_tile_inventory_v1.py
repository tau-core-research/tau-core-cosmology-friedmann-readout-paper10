#!/usr/bin/env python3
from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_dr4_path_mask_route_tile_inventory_policy_v1.csv"
ROUTE_INVENTORY = ROOT / "data" / "derived" / "kids1000_dr4_path_mask_route_scripts_inventory_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_dr4_path_mask_route_tile_inventory_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_dr4_path_mask_route_tile_inventory_v1_summary.csv"

URL_RE = re.compile(
    r"KiDS_DR4\.1_(?P<ra>[0-9.]+)_(?P<dec>-?[0-9.]+)_ugriZYJHKs_msk\.fits\.gz$"
)


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def parse_route_urls(route_script: Path) -> list[str]:
    urls: list[str] = []
    for line in route_script.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) != 2 or parts[0] != "wget":
            raise SystemExit(f"unexpected route script line: {line}")
        urls.append(parts[1])
    return urls


def parse_url(url: str) -> tuple[str, str]:
    match = URL_RE.search(url)
    if not match:
        raise SystemExit(f"could not parse DR4.1 9-band mask URL: {url}")
    return match.group("ra"), match.group("dec")


def main() -> None:
    policy = read_one(POLICY)
    if policy["endpoint_scoring_allowed"].lower() != "false":
        raise SystemExit("route tile inventory policy must remain endpoint disabled")
    if policy["current_mask_products_fetched"].lower() != "false":
        raise SystemExit("route tile inventory must not fetch mask products")
    if policy["current_path_mapping_computed"].lower() != "false":
        raise SystemExit("route tile inventory must not compute path mapping")

    with ROUTE_INVENTORY.open(newline="") as f:
        route_rows = list(csv.DictReader(f))
    preferred = [row for row in route_rows if row["route_id"] == policy["preferred_route_id"]]
    if len(preferred) != 1:
        raise SystemExit("preferred route inventory row not found")
    preferred_row = preferred[0]
    route_script = ROOT / preferred_row["local_path"]
    urls = parse_route_urls(route_script)
    if len(urls) != int(policy["expected_tile_count"]):
        raise SystemExit("unexpected preferred route tile count")

    rows: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for index, url in enumerate(urls):
        ra, dec = parse_url(url)
        key = (ra, dec)
        rows.append(
            {
                "policy_id": policy["policy_id"],
                "preferred_route_id": policy["preferred_route_id"],
                "tile_index_zero_based": str(index),
                "mask_product_url": url,
                "tile_ra_deg_filename_proxy": ra,
                "tile_dec_deg_filename_proxy": dec,
                "tile_coordinate_source": "KiDS_mask_filename_token",
                "duplicate_tile_coordinate": "true" if key in seen else "false",
                "mask_product_fetched": "false",
                "mask_pixels_parsed": "false",
                "footprint_polygon_computed": "false",
                "path_mapping_computed": "false",
                "contains_mapping_vector": "false",
                "contains_theory_vector": "false",
                "contains_predictions": "false",
                "contains_residuals": "false",
                "contains_fit_statistics": "false",
                "uses_kids_data_vector_values": "false",
                "uses_posterior_chains": "false",
                "uses_posthoc_tile_selection": "false",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "kids1000_dr4_path_mask_route_tile_inventory_not_mapping_not_validation",
            }
        )
        seen.add(key)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    ras = [float(row["tile_ra_deg_filename_proxy"]) for row in rows]
    decs = [float(row["tile_dec_deg_filename_proxy"]) for row in rows]
    summary = {
        "policy_id": policy["policy_id"],
        "status": "KIDS_DR4_PATH_MASK_ROUTE_TILE_INVENTORY_BUILT_NOT_MAPPED",
        "preferred_route_id": policy["preferred_route_id"],
        "tile_count": str(len(rows)),
        "unique_tile_coordinate_count": str(len(seen)),
        "duplicate_tile_coordinate_count": str(sum(row["duplicate_tile_coordinate"] == "true" for row in rows)),
        "min_tile_ra_deg_filename_proxy": f"{min(ras):.6f}",
        "max_tile_ra_deg_filename_proxy": f"{max(ras):.6f}",
        "min_tile_dec_deg_filename_proxy": f"{min(decs):.6f}",
        "max_tile_dec_deg_filename_proxy": f"{max(decs):.6f}",
        "mask_products_fetched": "false",
        "mask_pixels_parsed": "false",
        "footprint_polygon_computed": "false",
        "path_mapping_computed": "false",
        "contains_mapping_vector": "false",
        "contains_theory_vector": "false",
        "contains_predictions": "false",
        "contains_residuals": "false",
        "contains_fit_statistics": "false",
        "uses_kids_data_vector_values": "false",
        "uses_posterior_chains": "false",
        "uses_posthoc_tile_selection": "false",
        "endpoint_scoring_allowed": "false",
        "claim_boundary": "kids1000_dr4_path_mask_route_tile_inventory_not_mapping_not_validation",
    }
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)
    print(
        "PAPER10_KIDS_DR4_PATH_MASK_ROUTE_TILE_INVENTORY_V1_BUILT "
        f"tiles={len(rows)} endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()

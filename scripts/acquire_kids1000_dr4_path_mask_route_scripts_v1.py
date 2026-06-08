#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
from datetime import datetime, timezone
from pathlib import Path

import requests


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "source_manifest" / "kids1000_dr4_path_mask_route_scripts_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_dr4_path_mask_route_scripts_inventory_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_dr4_path_mask_route_scripts_inventory_v1_summary.csv"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_wget_urls(text: str) -> list[str]:
    urls: list[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) == 2 and parts[0] == "wget":
            urls.append(parts[1])
    return urls


def main() -> None:
    with MANIFEST.open(newline="") as f:
        routes = list(csv.DictReader(f))
    rows: list[dict[str, str]] = []
    fetched_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    for route in routes:
        if route["endpoint_allowed"].lower() != "false":
            raise SystemExit("path mask route scripts must remain endpoint disabled")
        response = requests.get(route["route_script_url"], timeout=30)
        response.raise_for_status()
        content = response.content
        local_path = ROOT / route["local_path"]
        local_path.parent.mkdir(parents=True, exist_ok=True)
        local_path.write_bytes(content)
        text = content.decode("utf-8", errors="replace")
        urls = parse_wget_urls(text)
        rows.append(
            {
                "route_id": route["route_id"],
                "status": "KIDS_DR4_PATH_MASK_ROUTE_SCRIPT_FETCHED_FROZEN",
                "provider": route["provider"],
                "route_script_url": route["route_script_url"],
                "local_path": route["local_path"],
                "http_status": str(response.status_code),
                "byte_count": str(len(content)),
                "sha256": sha256_bytes(content),
                "fetched_at_utc": fetched_at,
                "route_script_role": route["route_script_role"],
                "listed_mask_product_count": str(len(urls)),
                "first_listed_mask_product": urls[0] if urls else "",
                "last_listed_mask_product": urls[-1] if urls else "",
                "mask_products_fetched": "false",
                "path_mapping_computed": "false",
                "contains_mapping_vector": "false",
                "contains_theory_vector": "false",
                "contains_predictions": "false",
                "contains_residuals": "false",
                "contains_fit_statistics": "false",
                "uses_kids_data_vector_values": "false",
                "uses_posterior_chains": "false",
                "uses_posthoc_path_selection": "false",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "kids1000_dr4_path_mask_route_scripts_not_validation",
            }
        )

    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    preferred = [row for row in rows if row["route_id"] == "KIDS_DR41_9BAND_MASK_WGET_SCRIPT"][0]
    summary = {
        "status": "KIDS_DR4_PATH_MASK_ROUTE_SCRIPTS_FETCHED_FROZEN_NOT_SCORED",
        "route_script_count": str(len(rows)),
        "preferred_route_id": preferred["route_id"],
        "preferred_listed_mask_product_count": preferred["listed_mask_product_count"],
        "total_listed_mask_product_count": str(sum(int(row["listed_mask_product_count"]) for row in rows)),
        "mask_products_fetched": "false",
        "path_mapping_computed": "false",
        "contains_mapping_vector": "false",
        "contains_theory_vector": "false",
        "contains_predictions": "false",
        "contains_residuals": "false",
        "contains_fit_statistics": "false",
        "uses_kids_data_vector_values": "false",
        "uses_posterior_chains": "false",
        "uses_posthoc_path_selection": "false",
        "endpoint_scoring_allowed": "false",
        "claim_boundary": "kids1000_dr4_path_mask_route_scripts_not_validation",
    }
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)
    print(
        "PAPER10_KIDS_DR4_PATH_MASK_ROUTE_SCRIPTS_V1_FETCHED "
        f"routes={len(rows)} preferred_masks={preferred['listed_mask_product_count']} endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()

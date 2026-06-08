#!/usr/bin/env python3
from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path

import requests


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_dr4_path_mask_head_sample_policy_v1.csv"
ROUTE_INVENTORY = ROOT / "data" / "derived" / "kids1000_dr4_path_mask_route_scripts_inventory_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_dr4_path_mask_head_sample_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_dr4_path_mask_head_sample_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def parse_wget_urls(path: Path) -> list[str]:
    urls: list[str] = []
    for raw in path.read_text().splitlines():
        parts = raw.strip().split()
        if len(parts) == 2 and parts[0] == "wget":
            urls.append(parts[1])
    return urls


def main() -> None:
    policy = read_one(POLICY)
    if policy["endpoint_scoring_allowed"].lower() != "false":
        raise SystemExit("HEAD sample policy must remain endpoint disabled")
    if policy["current_mask_products_fetched"].lower() != "false":
        raise SystemExit("mask products must not be fetched in a HEAD sample")

    with ROUTE_INVENTORY.open(newline="") as f:
        route_rows = list(csv.DictReader(f))
    preferred = [row for row in route_rows if row["route_id"] == policy["preferred_route_id"]]
    if len(preferred) != 1:
        raise SystemExit("expected one preferred route")
    route = preferred[0]
    urls = parse_wget_urls(ROOT / route["local_path"])
    indices = [int(value) for value in policy["sample_indices_zero_based"].split(";")]
    checked_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    rows: list[dict[str, str]] = []
    for index in indices:
        if index < 0 or index >= len(urls):
            raise SystemExit(f"sample index out of range: {index}")
        url = urls[index]
        response = requests.head(
            url,
            allow_redirects=True,
            timeout=30,
            headers={"User-Agent": "tau-core-paper10-kids-mask-head-audit/0.1"},
        )
        rows.append(
            {
                "policy_id": policy["policy_id"],
                "route_id": route["route_id"],
                "sample_index_zero_based": str(index),
                "mask_product_url": url,
                "head_status": "HEAD_CHECKED_MASK_NOT_FETCHED",
                "http_status": str(response.status_code),
                "content_length": response.headers.get("Content-Length", ""),
                "content_type": response.headers.get("Content-Type", ""),
                "etag": response.headers.get("ETag", ""),
                "last_modified": response.headers.get("Last-Modified", ""),
                "checked_at_utc": checked_at,
                "mask_product_fetched": "false",
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
                "claim_boundary": "kids1000_dr4_path_mask_head_sample_not_validation",
            }
        )

    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    ok_count = sum(row["http_status"] == "200" for row in rows)
    content_lengths = [int(row["content_length"]) for row in rows if row["content_length"]]
    summary = {
        "policy_id": policy["policy_id"],
        "status": "KIDS_DR4_PATH_MASK_HEAD_SAMPLE_CHECKED_NOT_FETCHED",
        "preferred_route_id": route["route_id"],
        "sample_rule": policy["sample_rule"],
        "sample_count": str(len(rows)),
        "http_200_count": str(ok_count),
        "min_content_length": str(min(content_lengths) if content_lengths else 0),
        "max_content_length": str(max(content_lengths) if content_lengths else 0),
        "mask_products_fetched": "false",
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
        "claim_boundary": "kids1000_dr4_path_mask_head_sample_not_validation",
    }
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)
    print(
        "PAPER10_KIDS_DR4_PATH_MASK_HEAD_SAMPLE_V1_CHECKED "
        f"sample={len(rows)} http_200={ok_count} endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import csv
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROUTE = ROOT / "data" / "source_manifest" / "kids1000_lensing_route_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_lensing_route_v1_head.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_lensing_route_v1_summary.csv"


def main() -> None:
    with ROUTE.open(newline="") as f:
        route = list(csv.DictReader(f))[0]
    if route["status"] != "KIDS1000_LENSING_ROUTE_DECLARED_NOT_FETCHED":
        raise SystemExit("KiDS route status mismatch")
    if route["endpoint_scoring_allowed"].lower() != "false":
        raise SystemExit("KiDS lensing route must remain endpoint disabled")
    forbidden = route["forbidden_inputs"]
    for marker in ["lensing_residuals", "posthoc_tomographic_selection", "fit_improvement_flags"]:
        if marker not in forbidden:
            raise SystemExit(f"KiDS route missing forbidden marker: {marker}")
    request = urllib.request.Request(
        route["product_url"],
        method="HEAD",
        headers={"User-Agent": "tau-core-paper10-kids-lensing-route-check/0.1"},
    )
    checked_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    with urllib.request.urlopen(request, timeout=30) as response:
        status_code = int(getattr(response, "status", 200))
        headers = response.headers
    row = {
        "route_id": route["route_id"],
        "product_url": route["product_url"],
        "status": "HEAD_ROUTE_CHECKED_ENDPOINT_DISABLED",
        "status_code": str(status_code),
        "content_length": headers.get("Content-Length", ""),
        "content_type": headers.get("Content-Type", ""),
        "etag": headers.get("ETag", ""),
        "last_modified": headers.get("Last-Modified", ""),
        "checked_at_utc": checked_at,
        "endpoint_scoring_allowed": "false",
        "contains_lensing_data_vectors": "false",
        "contains_covariance_matrices": "false",
        "contains_fit_statistics": "false",
        "claim_boundary": "kids1000_lensing_route_not_validation",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(row.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(row)
    summary = {
        "route_id": route["route_id"],
        "status": "KIDS1000_LENSING_ROUTE_HEAD_CHECKED_NOT_FETCHED",
        "status_code": str(status_code),
        "content_length": row["content_length"],
        "content_type": row["content_type"],
        "endpoint_scoring_allowed": "false",
        "future_freeze_items": route["required_future_freeze"],
        "contains_lensing_likelihood": "false",
        "contains_lensing_residuals": "false",
        "claim_boundary": "kids1000_lensing_route_not_validation",
    }
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)
    print(
        "PAPER10_KIDS1000_LENSING_ROUTE_V1_CHECKED "
        f"status_code={status_code} endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()

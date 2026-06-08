#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROUTE = ROOT / "data" / "source_manifest" / "kids1000_lensing_route_v1.csv"
OUT = ROOT / "data" / "source_manifest" / "kids1000_lensing_products_v1.csv"
RAW = ROOT / "data" / "raw" / "weak_lensing" / "kids1000"


def main() -> None:
    with ROUTE.open(newline="") as f:
        route = list(csv.DictReader(f))[0]
    if route["endpoint_scoring_allowed"].lower() != "false":
        raise SystemExit("KiDS route must remain endpoint disabled")
    request = urllib.request.Request(
        route["product_url"],
        headers={"User-Agent": "tau-core-paper10-kids-lensing-product-freeze/0.1"},
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        status_code = int(getattr(response, "status", 200))
        payload = response.read(40_000_000)
    RAW.mkdir(parents=True, exist_ok=True)
    local_path = RAW / "KiDS1000_cosmic_shear_data_release.tgz"
    local_path.write_bytes(payload)
    acquired_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    row = {
        "frozen_product_id": "KIDS1000_COSMIC_SHEAR_TARBALL",
        "route_id": route["route_id"],
        "source_id": route["source_id"],
        "block": route["block"],
        "provider": route["provider"],
        "product_url": route["product_url"],
        "local_path": str(local_path.relative_to(ROOT)),
        "status": "SOURCE_NATIVE_PRODUCT_FETCHED_FROZEN",
        "status_code": str(status_code),
        "byte_count": str(len(payload)),
        "sha256": hashlib.sha256(payload).hexdigest(),
        "acquired_at_utc": acquired_at,
        "transform_rule_id": "TR_KIDS1000_COSEBIS_LENSING_ROUTE_V1",
        "freeze_scope": "source_native_lensing_tarball_inventory_without_endpoint_scoring",
        "endpoint_allowed": "false",
        "endpoint_blocker": route["required_future_freeze"],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(row.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(row)
    print("PAPER10_KIDS1000_LENSING_PRODUCTS_ACQUIRED rows=1 endpoint_allowed=false")


if __name__ == "__main__":
    main()

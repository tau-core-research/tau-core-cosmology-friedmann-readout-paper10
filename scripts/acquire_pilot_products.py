#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "source_manifest" / "pilot_frozen_product_manifest.csv"

PILOT_PRODUCTS = [
    {
        "product_id": "CC_HZ_TABLE",
        "pilot_product_id": "CC_HZ_DATA_CC_DAT",
        "source_id": "HZ_CC_BAO",
        "url": "https://cluster.difa.unibo.it/astro/CC_data/data_CC.dat",
        "local_path": "data/raw/hz_compilation/cosmic_chronometers_hz/data_CC.dat",
        "transform_rule_id": "TR_DISTANCE_HZ_CC_V1",
        "freeze_scope": "pilot_distance_input_without_full_covariance",
        "endpoint_allowed": "false",
        "endpoint_blocker": "covariance_or_systematics_policy_not_frozen",
    },
    {
        "product_id": "PANTHEON_PLUS_LIGHTCURVE_OR_MU",
        "pilot_product_id": "PANTHEON_PLUS_SH0ES_DAT",
        "source_id": "PANTHEON_PLUS_SN",
        "url": "https://raw.githubusercontent.com/PantheonPlusSH0ES/DataRelease/main/Pantheon+_Data/4_DISTANCES_AND_COVAR/Pantheon+SH0ES.dat",
        "local_path": "data/raw/pantheon_plus/pantheon_plus_mu_covariance/Pantheon+SH0ES.dat",
        "transform_rule_id": "TR_DISTANCE_SN_V1",
        "freeze_scope": "pilot_distance_table_without_covariance_matrix",
        "endpoint_allowed": "false",
        "endpoint_blocker": "covariance_matrix_not_frozen",
    },
    {
        "product_id": "PANTHEON_PLUS_LIGHTCURVE_OR_MU",
        "pilot_product_id": "PANTHEON_PLUS_SH0ES_STAT_SYS_COV",
        "source_id": "PANTHEON_PLUS_SN",
        "url": "https://raw.githubusercontent.com/PantheonPlusSH0ES/DataRelease/main/Pantheon+_Data/4_DISTANCES_AND_COVAR/Pantheon+SH0ES_STAT+SYS.cov",
        "local_path": "data/raw/pantheon_plus/pantheon_plus_mu_covariance/Pantheon+SH0ES_STAT+SYS.cov",
        "transform_rule_id": "TR_DISTANCE_SN_COV_V1",
        "freeze_scope": "pilot_distance_covariance_without_mask_policy",
        "endpoint_allowed": "false",
        "endpoint_blocker": "mask_and_calibration_policy_not_frozen",
    },
]


def download(url: str) -> tuple[int, bytes]:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "tau-core-paper10-pilot-product-freeze/0.1"},
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        status = getattr(response, "status", 200)
        payload = response.read(40_000_000)
    return int(status), payload


def main() -> None:
    acquired_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    rows: list[dict[str, str]] = []
    for product in PILOT_PRODUCTS:
        local_path = ROOT / product["local_path"]
        local_path.parent.mkdir(parents=True, exist_ok=True)
        status_code, payload = download(product["url"])
        sha256 = hashlib.sha256(payload).hexdigest()
        local_path.write_bytes(payload)
        rows.append(
            {
                **product,
                "status": "PILOT_PRODUCT_FETCHED_FROZEN",
                "status_code": str(status_code),
                "byte_count": str(len(payload)),
                "sha256": sha256,
                "acquired_at_utc": acquired_at,
            }
        )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "pilot_product_id",
                "product_id",
                "source_id",
                "url",
                "local_path",
                "status",
                "status_code",
                "byte_count",
                "sha256",
                "acquired_at_utc",
                "transform_rule_id",
                "freeze_scope",
                "endpoint_allowed",
                "endpoint_blocker",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"PAPER10_PILOT_PRODUCTS_ACQUIRED rows={len(rows)} endpoint_scoring_allowed=false")


if __name__ == "__main__":
    main()

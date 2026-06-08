#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "source_manifest" / "void_web_source_native_frozen_products_v1.csv"

PRODUCTS = [
    {
        "candidate_id": "VOID_VAST_DR7_PLANCK2018_V1",
        "frozen_product_id": "VOIDFINDER_PLANCK2018_MAXIMAL_VOID_TABLE",
        "channel_id": "W_VOID_MATURITY",
        "source_id": "PUBLIC_VOID_CATALOG",
        "url": (
            "https://zenodo.org/api/records/11043278/files/"
            "VoidFinder-nsa_v1_0_1_Planck2018_comoving_maximal.txt/content"
        ),
        "local_path": (
            "data/raw/public_void_catalog/vast_dr7_planck2018/"
            "VoidFinder-nsa_v1_0_1_Planck2018_comoving_maximal.txt"
        ),
        "transform_rule_id": "TR_VOID_MATURITY_SOURCE_NATIVE_V1",
        "freeze_scope": "source_native_void_maturity_without_endpoint_mapping",
        "endpoint_allowed": "false",
        "endpoint_blocker": "void_redshift_to_pantheon_scope_mapping_not_frozen",
    },
    {
        "candidate_id": "VOID_VAST_DR7_PLANCK2018_V1",
        "frozen_product_id": "VOIDFINDER_PLANCK2018_MASK",
        "channel_id": "W_VOID_MATURITY",
        "source_id": "PUBLIC_VOID_CATALOG",
        "url": "https://zenodo.org/api/records/11043278/files/NSA_main_mask.pickle/content",
        "local_path": "data/raw/public_void_catalog/vast_dr7_planck2018/NSA_main_mask.pickle",
        "transform_rule_id": "TR_VOID_MATURITY_SOURCE_NATIVE_V1",
        "freeze_scope": "source_native_void_mask_without_endpoint_mapping",
        "endpoint_allowed": "false",
        "endpoint_blocker": "void_mask_policy_not_mapped_to_pantheon_scope",
    },
    {
        "candidate_id": "WEB_SDSS_DR17_MCPM_V1",
        "frozen_product_id": "SDSS_DR17_MCPM_SLIMEMOLD_GALAXY_CATALOG",
        "channel_id": "W_WEB_ANISOTROPY",
        "source_id": "COSMIC_WEB_CLASSIFIER",
        "url": (
            "https://data.sdss.org/sas/dr17/env/EBOSS_LSS/mcpm/v1_0_1/"
            "slimeMold_galaxy_catalog_v1_0_1.fits"
        ),
        "local_path": "data/raw/cosmic_web/sdss_dr17_mcpm/slimeMold_galaxy_catalog_v1_0_1.fits",
        "transform_rule_id": "TR_WEB_ANISOTROPY_SOURCE_NATIVE_V1",
        "freeze_scope": "source_native_web_density_catalog_without_endpoint_mapping",
        "endpoint_allowed": "false",
        "endpoint_blocker": "web_density_to_growth_lensing_or_distance_scope_mapping_not_frozen",
    },
    {
        "candidate_id": "WEB_SDSS_DR17_MCPM_V1",
        "frozen_product_id": "SDSS_DR17_MCPM_SHA1SUM",
        "channel_id": "W_WEB_ANISOTROPY",
        "source_id": "COSMIC_WEB_CLASSIFIER",
        "url": (
            "https://data.sdss.org/sas/dr17/env/EBOSS_LSS/mcpm/v1_0_1/"
            "eboss_lss_mcpm_v1_0_1.sha1sum"
        ),
        "local_path": "data/raw/cosmic_web/sdss_dr17_mcpm/eboss_lss_mcpm_v1_0_1.sha1sum",
        "transform_rule_id": "TR_WEB_ANISOTROPY_SOURCE_NATIVE_V1",
        "freeze_scope": "source_native_web_provider_checksum_file",
        "endpoint_allowed": "false",
        "endpoint_blocker": "web_density_to_growth_lensing_or_distance_scope_mapping_not_frozen",
    },
]


def download(url: str) -> tuple[int, bytes]:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "tau-core-paper10-source-native-product-freeze/0.1"},
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        status = getattr(response, "status", 200)
        payload = response.read(80_000_000)
    return int(status), payload


def main() -> None:
    acquired_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    rows: list[dict[str, str]] = []
    for product in PRODUCTS:
        local_path = ROOT / product["local_path"]
        local_path.parent.mkdir(parents=True, exist_ok=True)
        status_code, payload = download(product["url"])
        local_path.write_bytes(payload)
        rows.append(
            {
                **product,
                "status": "SOURCE_NATIVE_PRODUCT_FETCHED_FROZEN",
                "status_code": str(status_code),
                "byte_count": str(len(payload)),
                "sha256": hashlib.sha256(payload).hexdigest(),
                "acquired_at_utc": acquired_at,
            }
        )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "frozen_product_id",
                "candidate_id",
                "channel_id",
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
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)

    print(
        "PAPER10_VOID_WEB_SOURCE_NATIVE_PRODUCTS_ACQUIRED "
        f"rows={len(rows)} endpoint_scoring_allowed=false"
    )


if __name__ == "__main__":
    main()

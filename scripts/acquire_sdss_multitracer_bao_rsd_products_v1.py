#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import zipfile
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "source_manifest" / "sdss_multitracer_bao_rsd_products_v1.csv"
RAW = ROOT / "data" / "raw" / "sdss_multitracer_bao_rsd" / "dr16_lrg_elg"

PRODUCTS = [
    {
        "frozen_product_id": "SDSS_DR16_MULTITRACER_LRG_ELG_CF_BAORSD_ZIP",
        "measurement_space": "configuration_space",
        "url": "https://www.sdss4.org/wp-content/uploads/2020/07/MultiTracer_CF_BAORSD_measurements.zip",
        "zip_path": "data/raw/sdss_multitracer_bao_rsd/dr16_lrg_elg/MultiTracer_CF_BAORSD_measurements.zip",
        "expected_data_file": "MultiTracer_CF_BAORSD_measurements/sdss_DR16_MultiTracerELGLRG_FS_xi.dat",
        "expected_cov_file": "MultiTracer_CF_BAORSD_measurements/sdss_DR16_MultiTracerELGLRG_FS_xi_cov.dat",
    },
    {
        "frozen_product_id": "SDSS_DR16_MULTITRACER_LRG_ELG_PK_BAORSD_ZIP",
        "measurement_space": "fourier_space",
        "url": "https://www.sdss4.org/wp-content/uploads/2020/07/MultiTracer_PK_BAORSD_measurements.zip",
        "zip_path": "data/raw/sdss_multitracer_bao_rsd/dr16_lrg_elg/MultiTracer_PK_BAORSD_measurements.zip",
        "expected_data_file": "MultiTracer_PK_BAORSD_measurements/sdss_DR16_MultiTracerELGLRG_BAORSD_FS_PK.dat",
        "expected_cov_file": "MultiTracer_PK_BAORSD_measurements/sdss_DR16_MultiTracerELGLRG_BAORSD_FS_PK_cov.dat",
    },
]


def download(url: str) -> tuple[int, bytes]:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "tau-core-paper10-sdss-multitracer-product-freeze/0.1"},
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        status = getattr(response, "status", 200)
        payload = response.read(20_000_000)
    return int(status), payload


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    acquired_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    rows: list[dict[str, str]] = []
    for product in PRODUCTS:
        status_code, payload = download(product["url"])
        zip_path = ROOT / product["zip_path"]
        zip_path.parent.mkdir(parents=True, exist_ok=True)
        zip_path.write_bytes(payload)
        with zipfile.ZipFile(zip_path) as zf:
            for member in zf.infolist():
                if member.filename.startswith("__MACOSX/") or "/__MACOSX/" in member.filename:
                    continue
                if Path(member.filename).name.startswith("._"):
                    continue
                zf.extract(member, RAW)
        data_path = RAW / product["expected_data_file"]
        cov_path = RAW / product["expected_cov_file"]
        if not data_path.exists() or not cov_path.exists():
            raise SystemExit(f"missing expected SDSS product after extraction: {product['frozen_product_id']}")
        rows.append(
            {
                "frozen_product_id": product["frozen_product_id"],
                "source_id": "SDSS_FINAL_BAO_RSD_MEASUREMENTS",
                "channel_id": "W_WEB_ANISOTROPY",
                "measurement_space": product["measurement_space"],
                "url": product["url"],
                "zip_path": product["zip_path"],
                "data_path": str(data_path.relative_to(ROOT)),
                "covariance_path": str(cov_path.relative_to(ROOT)),
                "status": "SOURCE_NATIVE_PRODUCT_FETCHED_FROZEN",
                "status_code": str(status_code),
                "byte_count": str(len(payload)),
                "sha256": hashlib.sha256(payload).hexdigest(),
                "acquired_at_utc": acquired_at,
                "transform_rule_id": "TR_SDSS_MULTITRACER_BAO_RSD_WEB_GROWTH_V1",
                "freeze_scope": "source_native_multitracer_bao_rsd_measurement_with_covariance",
                "endpoint_allowed": "false",
                "endpoint_blocker": "joint_multi_probe_likelihood_and_channel_policy_not_endpoint_frozen",
            }
        )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"PAPER10_SDSS_MULTITRACER_BAO_RSD_PRODUCTS_ACQUIRED rows={len(rows)} endpoint_allowed=false")


if __name__ == "__main__":
    main()

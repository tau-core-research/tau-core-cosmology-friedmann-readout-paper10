#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "source_manifest" / "sdss_multitracer_bao_rsd_products_v1.csv"


def main() -> None:
    with MANIFEST.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 2:
        raise SystemExit("SDSS multitracer manifest must contain exactly two product rows")
    spaces = {row["measurement_space"] for row in rows}
    if spaces != {"configuration_space", "fourier_space"}:
        raise SystemExit(f"unexpected measurement spaces: {sorted(spaces)}")
    for row in rows:
        if row["status"] != "SOURCE_NATIVE_PRODUCT_FETCHED_FROZEN":
            raise SystemExit("SDSS multitracer products must be fetched/frozen")
        if row["endpoint_allowed"].lower() != "false":
            raise SystemExit("SDSS multitracer products must remain endpoint disabled")
        zip_path = ROOT / row["zip_path"]
        data_path = ROOT / row["data_path"]
        cov_path = ROOT / row["covariance_path"]
        for path in [zip_path, data_path, cov_path]:
            if not path.exists():
                raise SystemExit(f"missing SDSS product path: {path}")
        if hashlib.sha256(zip_path.read_bytes()).hexdigest() != row["sha256"]:
            raise SystemExit(f"sha256 mismatch for {zip_path}")
        if data_path.stat().st_size <= 0 or cov_path.stat().st_size <= 0:
            raise SystemExit("SDSS data/covariance product is empty")
    print("PAPER10_SDSS_MULTITRACER_BAO_RSD_PRODUCTS_VALIDATED endpoint_allowed=false")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FROZEN = ROOT / "data" / "source_manifest" / "void_web_source_native_frozen_products_v1.csv"
PLAN = ROOT / "data" / "source_manifest" / "void_web_source_native_freeze_plan_v1.csv"

REQUIRED_PRODUCTS = {
    "VOIDFINDER_PLANCK2018_MAXIMAL_VOID_TABLE",
    "VOIDFINDER_PLANCK2018_MASK",
    "SDSS_DR17_MCPM_SLIMEMOLD_GALAXY_CATALOG",
    "SDSS_DR17_MCPM_SHA1SUM",
}


def main() -> None:
    if not FROZEN.exists():
        raise SystemExit("void/web source-native frozen products manifest is missing")

    with PLAN.open(newline="") as f:
        plan_rows = list(csv.DictReader(f))
    with FROZEN.open(newline="") as f:
        rows = list(csv.DictReader(f))

    candidates = {row["candidate_id"] for row in plan_rows}
    product_ids = {row["frozen_product_id"] for row in rows}
    if not REQUIRED_PRODUCTS <= product_ids:
        raise SystemExit(f"missing source-native products: {sorted(REQUIRED_PRODUCTS - product_ids)}")

    failures: list[str] = []
    rows_by_id = {row["frozen_product_id"]: row for row in rows}
    for row in rows:
        product_id = row["frozen_product_id"]
        if row["candidate_id"] not in candidates:
            failures.append(f"{product_id}: unknown candidate_id")
        if row["status"] != "SOURCE_NATIVE_PRODUCT_FETCHED_FROZEN":
            failures.append(f"{product_id}: invalid status")
        if row["endpoint_allowed"].lower() != "false":
            failures.append(f"{product_id}: endpoint_allowed must remain false")
        if not row["endpoint_blocker"]:
            failures.append(f"{product_id}: endpoint_blocker is required")
        if not row["transform_rule_id"].startswith("TR_"):
            failures.append(f"{product_id}: invalid transform_rule_id")
        path = ROOT / row["local_path"]
        if not path.exists():
            failures.append(f"{product_id}: local_path missing")
            continue
        payload = path.read_bytes()
        sha256 = hashlib.sha256(payload).hexdigest()
        if sha256 != row["sha256"]:
            failures.append(f"{product_id}: sha256 mismatch")
        if str(len(payload)) != row["byte_count"]:
            failures.append(f"{product_id}: byte_count mismatch")
        if not (200 <= int(row["status_code"]) < 400):
            failures.append(f"{product_id}: non-success status_code")

    if {
        "SDSS_DR17_MCPM_SLIMEMOLD_GALAXY_CATALOG",
        "SDSS_DR17_MCPM_SHA1SUM",
    } <= rows_by_id.keys():
        fits_row = rows_by_id["SDSS_DR17_MCPM_SLIMEMOLD_GALAXY_CATALOG"]
        sha_row = rows_by_id["SDSS_DR17_MCPM_SHA1SUM"]
        fits_path = ROOT / fits_row["local_path"]
        sha_path = ROOT / sha_row["local_path"]
        provider_sha1 = sha_path.read_text().split()[0]
        local_sha1 = hashlib.sha1(fits_path.read_bytes()).hexdigest()
        if provider_sha1 != local_sha1:
            failures.append("SDSS_DR17_MCPM_SLIMEMOLD_GALAXY_CATALOG: provider sha1 mismatch")

    if failures:
        raise SystemExit("void/web source-native product validation failed: " + "; ".join(failures))

    print(
        "PAPER10_VOID_WEB_SOURCE_NATIVE_PRODUCTS_VALIDATED "
        f"rows={len(rows)} endpoint_scoring_allowed=false"
    )


if __name__ == "__main__":
    main()

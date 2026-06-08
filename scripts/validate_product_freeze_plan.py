#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_MANIFEST = ROOT / "data" / "source_manifest" / "paper10_source_freeze_manifest.csv"
PRODUCT_PLAN = ROOT / "data" / "source_manifest" / "paper10_product_freeze_plan.csv"

ALLOWED_STATUSES = {
    "PRODUCT_SELECTED_NOT_FETCHED",
    "PRODUCT_FETCHED_FROZEN",
    "PRODUCT_BLOCKED",
}

REQUIRED_POLICIES = {
    "covariance_policy",
    "mask_or_selection_policy",
    "transform_rule_id",
    "endpoint_forbidden_inputs",
}


def main() -> None:
    with SOURCE_MANIFEST.open(newline="") as f:
        source_rows = list(csv.DictReader(f))
    with PRODUCT_PLAN.open(newline="") as f:
        product_rows = list(csv.DictReader(f))

    if not product_rows:
        raise SystemExit("product-freeze plan is empty")

    source_ids = {row["source_id"] for row in source_rows}
    product_source_ids = {row["source_id"] for row in product_rows}
    missing = source_ids - product_source_ids
    if missing:
        raise SystemExit(f"product-freeze plan missing source_ids: {sorted(missing)}")

    failures: list[str] = []
    for row in product_rows:
        product_id = row["product_id"]
        if row["freeze_status"] not in ALLOWED_STATUSES:
            failures.append(f"{product_id}: invalid freeze_status")
        if row["source_id"] not in source_ids:
            failures.append(f"{product_id}: unknown source_id")
        for key in REQUIRED_POLICIES:
            if not row[key]:
                failures.append(f"{product_id}: missing {key}")
        if row["endpoint_allowed"].lower() != "false":
            failures.append(f"{product_id}: endpoint_allowed must remain false in scaffold")
        if row["freeze_status"] == "PRODUCT_FETCHED_FROZEN":
            if row["required_hash"].lower() not in {"sha256", "sha512"}:
                failures.append(f"{product_id}: fetched product needs strong hash")
            if row["product_url_status"] == "EXACT_PRODUCT_PENDING":
                failures.append(f"{product_id}: fetched product cannot have pending URL")

    if failures:
        raise SystemExit("product-freeze validation failed: " + "; ".join(failures))

    fetched = [row for row in product_rows if row["freeze_status"] == "PRODUCT_FETCHED_FROZEN"]
    print(
        "PAPER10_PRODUCT_FREEZE_PLAN_VALIDATED "
        f"rows={len(product_rows)} fetched_frozen={len(fetched)} "
        "endpoint_scoring_allowed=false"
    )


if __name__ == "__main__":
    main()

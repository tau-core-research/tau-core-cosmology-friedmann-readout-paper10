#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PILOT_MANIFEST = ROOT / "data" / "source_manifest" / "pilot_frozen_product_manifest.csv"
PRODUCT_PLAN = ROOT / "data" / "source_manifest" / "paper10_product_freeze_plan.csv"


def count_data_rows(path: Path) -> int:
    with path.open() as f:
        lines = [line for line in f if line.strip()]
    if not lines:
        return 0
    return len(lines) - 1


def read_covariance_dimension(path: Path) -> int:
    with path.open() as f:
        first = f.readline().strip()
    try:
        return int(float(first))
    except ValueError as exc:
        raise SystemExit(f"invalid covariance dimension in {path}") from exc


def main() -> None:
    if not PILOT_MANIFEST.exists():
        raise SystemExit("pilot frozen product manifest is missing")

    with PRODUCT_PLAN.open(newline="") as f:
        product_plan = list(csv.DictReader(f))
    with PILOT_MANIFEST.open(newline="") as f:
        rows = list(csv.DictReader(f))

    plan_ids = {row["product_id"] for row in product_plan}
    if not rows:
        raise SystemExit("pilot frozen product manifest is empty")

    failures: list[str] = []
    for row in rows:
        pilot_id = row["pilot_product_id"]
        if row["product_id"] not in plan_ids:
            failures.append(f"{pilot_id}: unknown product_id")
        if row["status"] != "PILOT_PRODUCT_FETCHED_FROZEN":
            failures.append(f"{pilot_id}: invalid status")
        if row["endpoint_allowed"].lower() != "false":
            failures.append(f"{pilot_id}: endpoint_allowed must be false")
        if not row["endpoint_blocker"]:
            failures.append(f"{pilot_id}: endpoint_blocker is required")
        path = ROOT / row["local_path"]
        if not path.exists():
            failures.append(f"{pilot_id}: local_path missing")
            continue
        payload = path.read_bytes()
        sha256 = hashlib.sha256(payload).hexdigest()
        if sha256 != row["sha256"]:
            failures.append(f"{pilot_id}: sha256 mismatch")
        if str(len(payload)) != row["byte_count"]:
            failures.append(f"{pilot_id}: byte_count mismatch")
        if int(row["status_code"]) < 200 or int(row["status_code"]) >= 400:
            failures.append(f"{pilot_id}: non-success status_code")

    if failures:
        raise SystemExit("pilot product validation failed: " + "; ".join(failures))

    rows_by_id = {row["pilot_product_id"]: row for row in rows}
    required_pantheon = {
        "PANTHEON_PLUS_SH0ES_DAT",
        "PANTHEON_PLUS_SH0ES_STAT_SYS_COV",
    }
    if required_pantheon <= rows_by_id.keys():
        data_path = ROOT / rows_by_id["PANTHEON_PLUS_SH0ES_DAT"]["local_path"]
        cov_path = ROOT / rows_by_id["PANTHEON_PLUS_SH0ES_STAT_SYS_COV"]["local_path"]
        data_rows = count_data_rows(data_path)
        cov_dim = read_covariance_dimension(cov_path)
        if data_rows != cov_dim:
            raise SystemExit(
                "Pantheon+ table/covariance mismatch: "
                f"data_rows={data_rows} cov_dim={cov_dim}"
            )

    print(
        "PAPER10_PILOT_PRODUCTS_VALIDATED "
        f"rows={len(rows)} endpoint_scoring_allowed=false"
    )


if __name__ == "__main__":
    main()

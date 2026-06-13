#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/observer_path_metric_product_acquisition_status_v1.csv"
SUMMARY = ROOT / "data/derived/observer_path_metric_product_acquisition_status_v1_summary.csv"
DOC = ROOT / "docs/observer_path_metric_product_acquisition_status_v1.md"
CLAIM_BOUNDARY = "observer_path_metric_product_acquisition_status_not_endpoint_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    rows = read_rows(OUT)
    if len(rows) != 2:
        raise SystemExit("status gate must contain two routes")
    by_id = {row["route_id"]: row for row in rows}
    caveated = by_id["caveated_metric_environment_path_proxy"]
    physical = by_id["physical_kappa_shear_mass_map_product"]
    if caveated["source_aligned_numeric_product_count"] != "12":
        raise SystemExit("caveated product count must be 12")
    if caveated["can_support_physical_lensing_path_claim"] != "false":
        raise SystemExit("caveated product must not support physical lensing claim")
    if physical["route_status"] != "STILL_MISSING":
        raise SystemExit("physical route must remain missing")
    for row in rows:
        for field in [
            "endpoint_replay_allowed",
            "endpoint_validation_claimed",
            "physical_lensing_path_weight_claimed",
        ]:
            if row[field] != "false":
                raise SystemExit(f"{row['route_id']} unsafe field {field}")
        if row["claim_boundary"] != CLAIM_BOUNDARY:
            raise SystemExit(f"{row['route_id']} claim boundary mismatch")
    summary = read_rows(SUMMARY)
    if len(summary) != 1:
        raise SystemExit("summary must contain one row")
    s = summary[0]
    if s["caveated_metric_environment_product_count"] != "12":
        raise SystemExit("summary caveated count mismatch")
    if s["physical_kappa_shear_mass_map_product_count"] != "0":
        raise SystemExit("summary physical count must remain zero")
    if s["endpoint_replay_allowed"] != "false" or s["endpoint_validation_claimed"] != "false":
        raise SystemExit("summary must not authorize endpoint or validation")
    if s["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("summary claim boundary mismatch")
    text = DOC.read_text()
    for marker in ["physical lensing-path route remains blocked", "separate replay-authorization", CLAIM_BOUNDARY]:
        if marker not in text:
            raise SystemExit(f"doc missing marker: {marker}")
    print(
        "OBSERVER_PATH_METRIC_PRODUCT_ACQUISITION_STATUS_V1_VALIDATED "
        f"caveated_count={s['caveated_metric_environment_product_count']} physical_count={s['physical_kappa_shear_mass_map_product_count']}"
    )


if __name__ == "__main__":
    main()

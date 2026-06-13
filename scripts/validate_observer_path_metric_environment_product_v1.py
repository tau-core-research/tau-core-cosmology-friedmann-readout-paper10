#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/observer_path_metric_environment_product_v1.csv"
SUMMARY = ROOT / "data/derived/observer_path_metric_environment_product_v1_summary.csv"
DOC = ROOT / "docs/observer_path_metric_environment_product_v1.md"
CLAIM_BOUNDARY = "observer_path_metric_environment_product_source_side_not_endpoint_not_physical_lensing"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    rows = read_rows(OUT)
    if len(rows) != 12:
        raise SystemExit("metric-environment product must contain the frozen 12-row scope")
    for row in rows:
        if row["metric_environment_product_available_for_source"] != "true":
            raise SystemExit(f"{row['CID']} product unavailable")
        value = float(row["metric_environment_path_weight"])
        if not -1.0 < value < 1.0:
            raise SystemExit(f"{row['CID']} bounded product out of range")
        for field in [
            "endpoint_replay_allowed",
            "endpoint_validation_claimed",
            "contains_endpoint_scores",
            "contains_distance_residuals",
            "contains_lensing_residuals",
            "contains_fit_statistics",
            "physical_lensing_path_weight_claimed",
        ]:
            if row[field] != "false":
                raise SystemExit(f"{row['CID']} unsafe field {field}")
        if row["claim_boundary"] != CLAIM_BOUNDARY:
            raise SystemExit(f"{row['CID']} claim boundary mismatch")
    summary = read_rows(SUMMARY)
    if len(summary) != 1:
        raise SystemExit("summary must contain one row")
    s = summary[0]
    if s["metric_environment_product_available_count"] != "12":
        raise SystemExit("summary product count mismatch")
    if s["physical_lensing_path_weight_claimed"] != "false":
        raise SystemExit("summary must not claim physical lensing")
    if s["endpoint_replay_allowed"] != "false" or s["endpoint_validation_claimed"] != "false":
        raise SystemExit("summary must not authorize endpoint/validation")
    if s["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("summary claim boundary mismatch")
    text = DOC.read_text()
    for marker in ["not physical lensing", "not kappa", CLAIM_BOUNDARY]:
        if marker not in text:
            raise SystemExit(f"doc missing marker: {marker}")
    print(
        "OBSERVER_PATH_METRIC_ENVIRONMENT_PRODUCT_V1_VALIDATED "
        f"rows={len(rows)} available={s['metric_environment_product_available_count']}"
    )


if __name__ == "__main__":
    main()

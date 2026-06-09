#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_web_path_mapping_policy_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_web_path_mapping_readiness_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_web_path_mapping_readiness_v1_summary.csv"


def main() -> None:
    with POLICY.open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with OUT.open(newline="") as f:
        rows = list(csv.DictReader(f))
    with SUMMARY.open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    if len(rows) != 1:
        raise SystemExit("web/path mapping readiness must contain one row")
    row = rows[0]
    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("web/path mapping policy must remain endpoint disabled")
    if policy["current_mapping_computed"] != "true":
        raise SystemExit("web/path mapping policy should record the source-frozen mapping vector")
    if summary["endpoint_scoring_allowed"] != "false" or row["endpoint_scoring_allowed"] != "false":
        raise SystemExit("web/path mapping readiness must remain endpoint disabled")
    if summary["current_mapping_computed"] != "true" or row["current_mapping_computed"] != "true":
        raise SystemExit("web/path mapping should expose the source-frozen mapping vector")
    if summary["contains_mapping_vector"] != "true" or row["contains_mapping_vector"] != "true":
        raise SystemExit("web/path mapping readiness must contain the source-frozen mapping vector")
    for key in [
        "contains_theory_vector",
        "contains_predictions",
        "contains_residuals",
        "contains_fit_statistics",
        "uses_kids_data_vector_values",
        "uses_posterior_chains",
        "uses_posthoc_sky_direction_selection",
    ]:
        if summary[key] != "false" or row[key] != "false":
            raise SystemExit(f"web/path mapping readiness must keep {key}=false")
    if row["target_rows"] != policy["expected_target_rows"]:
        raise SystemExit("unexpected web/path mapping row target")
    if row["target_rows"] != "300":
        raise SystemExit("web/path mapping must target the full 300-row COSEBIs vector")
    if int(row["mapping_unique_value_count"]) <= 1:
        raise SystemExit("mapping vector should not be a single constant value")
    if "W_WEB_ANISOTROPY" not in row["active_channels"] or "W_PATH_PROJECTION" not in row["active_channels"]:
        raise SystemExit("web/path mapping policy must keep web/path channels active")
    for marker in [
        "kids_data_vector_values",
        "posthoc_sky_direction_selection",
        "posthoc_web_environment_labels",
    ]:
        if marker not in policy["forbidden_inputs"]:
            raise SystemExit(f"missing forbidden input: {marker}")
    if summary["status"] != "KIDS1000_COSEBIS_WEB_PATH_MAPPING_READINESS_BUILT_NOT_COMPUTED":
        raise SystemExit("unexpected web/path mapping readiness status")
    print("PAPER10_KIDS1000_COSEBIS_WEB_PATH_MAPPING_READINESS_V1_VALIDATED endpoint_allowed=false")


if __name__ == "__main__":
    main()

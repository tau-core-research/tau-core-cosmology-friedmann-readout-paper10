#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_f_overlap_header_footprint_rule_policy_v1.csv"
TILE_OUT = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_header_footprint_tile_rule_v1.csv"
DOMAIN_OUT = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_header_footprint_rule_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_header_footprint_rule_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def main() -> None:
    policy = read_one(POLICY)
    summary = read_one(SUMMARY)
    with TILE_OUT.open(newline="") as f:
        tile_rows = list(csv.DictReader(f))
    with DOMAIN_OUT.open(newline="") as f:
        domain_rows = list(csv.DictReader(f))
    if policy["status"] != "KIDS1000_COSEBIS_F_OVERLAP_HEADER_FOOTPRINT_RULE_LOCAL_DERIVATION_NOT_SCORED":
        raise SystemExit("unexpected header-footprint policy status")
    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("header-footprint policy must keep endpoint scoring disabled")
    if summary["status"] != "KIDS1000_COSEBIS_F_OVERLAP_HEADER_FOOTPRINT_RULE_BUILT_NOT_MAPPED":
        raise SystemExit("unexpected header-footprint summary status")
    if summary["tile_count"] != "196" or len(tile_rows) != 196:
        raise SystemExit("header-footprint rule must contain 196 tile rows")
    if summary["target_rows"] != "300":
        raise SystemExit("header-footprint rule must target 300 COSEBIs rows")
    if summary["domain_rows"] != "58800" or len(domain_rows) != 58800:
        raise SystemExit("header-footprint rule must contain 58,800 domain rows")
    if summary["header_footprint_rule_available"] != "true":
        raise SystemExit("header-footprint rule should be available")
    if summary["pixel_mask_values_read"] != "false":
        raise SystemExit("header-footprint rule must not read pixel mask values")
    if summary["pixel_mask_overlap_computed"] != "false":
        raise SystemExit("header-footprint rule must not claim pixel-mask overlap")
    if summary["overlap_rule_computed"] != "true":
        raise SystemExit("header-footprint overlap rule should be computed")
    if summary["path_mapping_computed"] != "false":
        raise SystemExit("header-footprint rule must not compute path mapping")
    min_f = float(summary["min_f_overlap_value"])
    max_f = float(summary["max_f_overlap_value"])
    if not (0.0 < min_f <= max_f <= 1.0):
        raise SystemExit("F_overlap values must be in (0,1]")
    if int(summary["unique_f_overlap_value_count_rounded_1e_minus_12"]) < 1:
        raise SystemExit("header-footprint rule must record at least one overlap value")
    if any(row["sha256"] == "" for row in tile_rows):
        raise SystemExit("tile rows must carry source-cache hashes")
    if any(row["header_footprint_support"] != "true" for row in tile_rows):
        raise SystemExit("all tile rows must have header footprint support")
    for key in [
        "path_mapping_computed",
        "contains_mapping_vector",
        "contains_theory_vector",
        "contains_predictions",
        "contains_residuals",
        "contains_fit_statistics",
        "uses_kids_data_vector_values",
        "uses_posterior_chains",
        "uses_posthoc_tile_selection",
        "endpoint_scoring_allowed",
    ]:
        if summary[key] != "false":
            raise SystemExit(f"summary must keep {key}=false")
        if any(row[key] != "false" for row in tile_rows):
            raise SystemExit(f"tile rows must keep {key}=false")
        if any(row[key] != "false" for row in domain_rows):
            raise SystemExit(f"domain rows must keep {key}=false")
    if any(row["pixel_mask_values_read"] != "false" for row in domain_rows):
        raise SystemExit("domain rows must not read pixel mask values")
    if any(row["overlap_rule_computed"] != "true" for row in domain_rows):
        raise SystemExit("domain rows must mark header overlap rule as computed")
    for marker in [
        "kids_data_vector_values",
        "posterior_chains",
        "lensing_residuals",
        "fit_improvement_flags",
        "posthoc_overlap_rule_choice",
        "posthoc_path_projection_labels",
    ]:
        if marker not in policy["forbidden_inputs"]:
            raise SystemExit(f"missing forbidden input marker: {marker}")
    print(
        "PAPER10_KIDS1000_COSEBIS_F_OVERLAP_HEADER_FOOTPRINT_RULE_V1_VALIDATED "
        f"domain_rows={summary['domain_rows']} endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_d_path_full_route_mask_load_rule_policy_v1.csv"
TILE_OUT = ROOT / "data" / "derived" / "kids1000_cosebis_d_path_full_route_mask_load_tile_rule_v1.csv"
DOMAIN_OUT = ROOT / "data" / "derived" / "kids1000_cosebis_d_path_full_route_mask_load_rule_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_d_path_full_route_mask_load_rule_v1_summary.csv"


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
    if policy["status"] != "KIDS1000_COSEBIS_D_PATH_FULL_ROUTE_MASK_LOAD_RULE_SOURCE_ONLY_NOT_SCORED":
        raise SystemExit("unexpected D_path mask-load policy status")
    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("D_path mask-load policy must keep endpoint scoring disabled")
    if summary["status"] != "KIDS1000_COSEBIS_D_PATH_FULL_ROUTE_MASK_LOAD_RULE_BUILT_SOURCE_ONLY_NOT_MAPPED":
        raise SystemExit("unexpected D_path mask-load summary status")
    if summary["tile_count"] != "196" or len(tile_rows) != 196:
        raise SystemExit("D_path mask-load rule must contain 196 tile rows")
    if summary["domain_rows"] != "58800" or len(domain_rows) != 58800:
        raise SystemExit("D_path mask-load rule must contain 58,800 domain rows")
    if summary["d_path_full_route_mask_load_non_degenerate"] != "true":
        raise SystemExit("D_path mask-load rule must be non-degenerate")
    if summary["d_path_source_route_support"] != "true":
        raise SystemExit("D_path mask-load rule should support the D_path route")
    if summary["d_path_not_identical_to_f_overlap"] != "true":
        raise SystemExit("D_path mask-load rule must not be identical to F_overlap")
    if not (0.0 < float(summary["min_d_path_value"]) < float(summary["max_d_path_value"]) <= 1.0):
        raise SystemExit("D_path values must be non-uniform and normalized to (0,1]")
    if int(summary["unique_d_path_value_count_rounded_1e_minus_12"]) <= 1:
        raise SystemExit("D_path values must contain more than one rounded value")
    for row in tile_rows:
        if row["sha256"] == "":
            raise SystemExit("tile rows must carry source-cache hashes")
        if row["d_path_mask_load_computed"] != "true":
            raise SystemExit("tile rows must mark D_path mask load computed")
        if int(row["n_pixels"]) <= 0 or int(row["n_finite_pixels"]) <= 0:
            raise SystemExit("tile rows must carry finite source pixels")
        if float(row["mean_nonzero_mask_value"]) <= 0.0:
            raise SystemExit("tile rows must carry positive nonzero mask-load means")
        if not (0.0 < float(row["d_path_full_route_mask_load_value"]) <= 1.0):
            raise SystemExit("tile rows must carry normalized D_path values")
    if any(row["d_path_mask_load_computed"] != "true" for row in domain_rows):
        raise SystemExit("domain rows must mark D_path mask load computed")
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
        "uses_posthoc_path_projection_labels",
        "endpoint_scoring_allowed",
    ]:
        if summary[key] != "false":
            raise SystemExit(f"summary must keep {key}=false")
        if any(row[key] != "false" for row in tile_rows):
            raise SystemExit(f"tile rows must keep {key}=false")
        if any(row[key] != "false" for row in domain_rows):
            raise SystemExit(f"domain rows must keep {key}=false")
    for marker in [
        "kids_data_vector_values",
        "posterior_chains",
        "lensing_residuals",
        "fit_statistics",
        "posthoc_tile_selection",
        "posthoc_path_projection_labels",
        "posthoc_d_path_rule_choice",
    ]:
        if marker not in policy["forbidden_inputs"]:
            raise SystemExit(f"missing forbidden input marker: {marker}")
    print(
        "PAPER10_KIDS1000_COSEBIS_D_PATH_FULL_ROUTE_MASK_LOAD_RULE_V1_VALIDATED "
        "non_degenerate=true endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()

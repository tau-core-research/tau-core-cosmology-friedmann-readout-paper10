#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_f_overlap_header_footprint_degeneracy_audit_policy_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_header_footprint_degeneracy_audit_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_header_footprint_degeneracy_audit_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def main() -> None:
    policy = read_one(POLICY)
    summary = read_one(SUMMARY)
    with OUT.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if policy["status"] != "KIDS1000_COSEBIS_F_OVERLAP_HEADER_FOOTPRINT_DEGENERACY_AUDIT_DECLARED_NOT_SCORED":
        raise SystemExit("unexpected header-footprint degeneracy policy status")
    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("header-footprint degeneracy policy must keep endpoint scoring disabled")
    if summary["status"] != "KIDS1000_COSEBIS_F_OVERLAP_HEADER_FOOTPRINT_DEGENERACY_AUDIT_BUILT_UNIFORM_NOT_PROMOTABLE":
        raise SystemExit("header-footprint audit should record the current uniform negative result")
    if summary["tile_count"] != "196":
        raise SystemExit("header-footprint audit must cover 196 tiles")
    if summary["audit_item_count"] != "2":
        raise SystemExit("header-footprint audit must contain two audit items")
    if summary["blocking_item_count"] != "2":
        raise SystemExit("both header-footprint degeneracy checks should block promotion")
    if summary["unique_f_overlap_value_count_rounded_1e_minus_12"] != "1":
        raise SystemExit("header-footprint values should currently be uniform")
    if summary["header_rule_uniform"] != "true":
        raise SystemExit("header-footprint audit should mark uniform=true")
    if summary["non_degenerate_mapping_support"] != "false":
        raise SystemExit("uniform header-footprint rule must not support non-degenerate mapping")
    if summary["recommended_next_action"] != "derive_pixel_mask_or_subtile_overlap_rule":
        raise SystemExit("next action should be pixel/subtile overlap derivation")
    if any(row["audit_passed"] != "false" for row in rows):
        raise SystemExit("current header-footprint degeneracy rows should fail")
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
        if any(row[key] != "false" for row in rows):
            raise SystemExit(f"rows must keep {key}=false")
    print(
        "PAPER10_KIDS1000_COSEBIS_F_OVERLAP_HEADER_FOOTPRINT_DEGENERACY_AUDIT_V1_VALIDATED "
        "uniform=true endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_path_weight_construction_rule_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_path_weight_construction_rule_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_path_weight_construction_rule_v1_summary.csv"


def main() -> None:
    with POLICY.open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with OUT.open(newline="") as f:
        rows = list(csv.DictReader(f))
    with SUMMARY.open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    if policy["status"] != "KIDS1000_COSEBIS_PATH_WEIGHT_CONSTRUCTION_RULE_DECLARED_NOT_COMPUTED":
        raise SystemExit("unexpected path-weight policy status")
    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("path-weight policy must remain endpoint disabled")
    if policy["current_weight_rule_declared"] != "true":
        raise SystemExit("policy must declare the symbolic weight rule")
    if policy["current_tile_weights_computed"] != "false":
        raise SystemExit("path-weight policy must not compute tile weights")
    if len(rows) != 7:
        raise SystemExit("path-weight ledger must contain seven factors")
    if summary["status"] != "KIDS1000_COSEBIS_PATH_WEIGHT_CONSTRUCTION_RULE_BUILT_NOT_COMPUTED":
        raise SystemExit("unexpected path-weight summary status")
    if summary["factor_count"] != "7":
        raise SystemExit("unexpected path-weight factor count")
    if summary["available_factor_count"] != "2":
        raise SystemExit("unexpected available factor count")
    if summary["partial_available_factor_count"] != "1":
        raise SystemExit("unexpected partial factor count")
    if summary["missing_factor_count"] != "2":
        raise SystemExit("unexpected missing factor count")
    if summary["declared_not_computed_factor_count"] != "1":
        raise SystemExit("unexpected declared-not-computed factor count")
    if summary["declared_not_executed_factor_count"] != "1":
        raise SystemExit("unexpected declared-not-executed factor count")
    if summary["domain_rows"] != "58800":
        raise SystemExit("path-weight rule must refer to the 58,800-row domain")
    if summary["path_weight_rule_computable"] != "false":
        raise SystemExit("path-weight rule must not be marked computable")
    by_factor = {row["factor_id"]: row for row in rows}
    expected = {
        "N_pair": "available_for_future_rule",
        "T_tile": "available_for_future_rule",
        "F_overlap": "missing",
        "D_path": "partial_available",
        "E_web": "missing",
        "C_norm": "declared_not_computed",
        "null_controls": "declared_not_executed",
    }
    if set(by_factor) != set(expected):
        raise SystemExit("unexpected path-weight factors")
    for factor_id, state in expected.items():
        if by_factor[factor_id]["source_state"] != state:
            raise SystemExit(f"unexpected state for {factor_id}")
    if by_factor["D_path"]["source_count"] != "3":
        raise SystemExit("D_path must remain limited to the three-mask shell")
    if by_factor["T_tile"]["source_count"] != "196":
        raise SystemExit("T_tile must reference all 196 route tiles")
    for key in [
        "tile_weights_computed",
        "path_mapping_computed",
        "contains_mapping_vector",
        "contains_theory_vector",
        "contains_predictions",
        "contains_residuals",
        "contains_fit_statistics",
        "uses_kids_data_vector_values",
        "uses_posterior_chains",
        "uses_posthoc_weight_selection",
        "endpoint_scoring_allowed",
    ]:
        if summary[key] != "false":
            raise SystemExit(f"summary must keep {key}=false")
        if any(row[key] != "false" for row in rows):
            raise SystemExit(f"rows must keep {key}=false")
    for marker in [
        "kids_data_vector_values",
        "posterior_chains",
        "lensing_residuals",
        "fit_improvement_flags",
        "posthoc_path_projection_labels",
        "posthoc_sky_direction_selection",
        "posthoc_tile_selection",
        "posthoc_weight_selection",
    ]:
        if marker not in policy["forbidden_inputs"]:
            raise SystemExit(f"missing forbidden input: {marker}")
    print("PAPER10_KIDS1000_COSEBIS_PATH_WEIGHT_CONSTRUCTION_RULE_V1_VALIDATED endpoint_allowed=false")


if __name__ == "__main__":
    main()

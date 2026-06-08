#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_path_factor_acquisition_plan_v1.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_path_factor_acquisition_plan_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_path_factor_acquisition_plan_v1_summary.csv"


def main() -> None:
    with POLICY.open(newline="") as f:
        policy = list(csv.DictReader(f))[0]
    with OUT.open(newline="") as f:
        rows = list(csv.DictReader(f))
    with SUMMARY.open(newline="") as f:
        summary = list(csv.DictReader(f))[0]
    if policy["status"] != "KIDS1000_COSEBIS_PATH_FACTOR_ACQUISITION_PLAN_DECLARED_NOT_FETCHED":
        raise SystemExit("unexpected acquisition plan policy status")
    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("acquisition plan policy must remain endpoint disabled")
    if policy["current_external_products_fetched"] != "false":
        raise SystemExit("acquisition plan must not fetch products")
    if len(rows) != 7:
        raise SystemExit("acquisition plan must contain seven requirements")
    if summary["status"] != "KIDS1000_COSEBIS_PATH_FACTOR_ACQUISITION_PLAN_BUILT_NOT_FETCHED":
        raise SystemExit("unexpected acquisition plan summary status")
    if summary["requirement_count"] != "7":
        raise SystemExit("unexpected acquisition requirement count")
    if summary["blocking_requirement_count"] != "4":
        raise SystemExit("unexpected blocking requirement count")
    if summary["nonblocking_requirement_count"] != "3":
        raise SystemExit("unexpected nonblocking requirement count")
    by_req = {row["requirement_id"]: row for row in rows}
    expected = {
        "REQ_N_PAIR_LOCK",
        "REQ_T_TILE_LOCK",
        "REQ_F_OVERLAP_SOURCE",
        "REQ_D_PATH_SOURCE",
        "REQ_E_WEB_SOURCE",
        "REQ_C_NORM_RULE",
        "REQ_NULL_CONTROLS_EXECUTION",
    }
    if set(by_req) != expected:
        raise SystemExit("unexpected acquisition requirements")
    for req in ["REQ_F_OVERLAP_SOURCE", "REQ_D_PATH_SOURCE", "REQ_E_WEB_SOURCE", "REQ_C_NORM_RULE"]:
        if by_req[req]["blocks_weight_computation"] != "true":
            raise SystemExit(f"{req} must block weight computation")
    for req in ["REQ_N_PAIR_LOCK", "REQ_T_TILE_LOCK", "REQ_NULL_CONTROLS_EXECUTION"]:
        if by_req[req]["blocks_weight_computation"] != "false":
            raise SystemExit(f"{req} must not directly block weight computation")
    for key in [
        "external_products_fetched",
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
    print("PAPER10_KIDS1000_COSEBIS_PATH_FACTOR_ACQUISITION_PLAN_V1_VALIDATED endpoint_allowed=false")


if __name__ == "__main__":
    main()

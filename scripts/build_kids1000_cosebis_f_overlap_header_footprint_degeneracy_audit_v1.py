#!/usr/bin/env python3
from __future__ import annotations

import csv
import statistics
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_f_overlap_header_footprint_degeneracy_audit_policy_v1.csv"
TILE_RULE = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_header_footprint_tile_rule_v1.csv"
RULE_SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_header_footprint_rule_v1_summary.csv"
OUT = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_header_footprint_degeneracy_audit_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_header_footprint_degeneracy_audit_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain one row")
    return rows[0]


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def float_text(value: float) -> str:
    return f"{value:.12e}"


def main() -> None:
    policy = read_one(POLICY)
    rule_summary = read_one(RULE_SUMMARY)
    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("header-footprint degeneracy audit must keep endpoint scoring disabled")
    if policy["current_path_mapping_computed"] != "false":
        raise SystemExit("header-footprint degeneracy audit must not compute path mapping")
    if rule_summary["overlap_rule_computed"] != "true":
        raise SystemExit("header-footprint degeneracy audit requires a computed header rule")
    with TILE_RULE.open(newline="") as f:
        tile_rows = list(csv.DictReader(f))
    values = [float(row["f_overlap_tile_header_area_norm"]) for row in tile_rows]
    mean_value = statistics.fmean(values)
    max_abs_deviation = max(abs(v - mean_value) for v in values)
    std_value = statistics.pstdev(values)
    unique_rounded = len({round(v, 12) for v in values})
    uniform = unique_rounded == 1 and max_abs_deviation < 1e-12
    rows = [
        {
            "policy_id": policy["policy_id"],
            "audit_item_id": "HEADER_FOOTPRINT_VALUE_UNIFORMITY",
            "current_state": f"unique_rounded_1e_minus_12_{unique_rounded}",
            "required_for_non_degenerate_mapping": "unique_rounded_1e_minus_12_greater_than_1",
            "audit_passed": bool_text(not uniform),
            "blocking_status": "blocking_uniform_header_footprint" if uniform else "not_blocking",
            "diagnostic_value": str(unique_rounded),
            "recommended_next_action": "derive_pixel_mask_or_subtile_overlap_rule" if uniform else "may_enter_mapping_preflight",
        },
        {
            "policy_id": policy["policy_id"],
            "audit_item_id": "HEADER_FOOTPRINT_VARIANCE",
            "current_state": f"std_{float_text(std_value)}_max_abs_deviation_{float_text(max_abs_deviation)}",
            "required_for_non_degenerate_mapping": "positive_variance_above_numerical_tolerance",
            "audit_passed": bool_text(std_value > 1e-12),
            "blocking_status": "blocking_zero_variance" if std_value <= 1e-12 else "not_blocking",
            "diagnostic_value": float_text(std_value),
            "recommended_next_action": "do_not_promote_header_area_rule_as_endpoint_mapping" if std_value <= 1e-12 else "may_enter_mapping_preflight",
        },
    ]
    for row in rows:
        row.update(
            {
                "tile_count": str(len(tile_rows)),
                "mean_f_overlap_value": float_text(mean_value),
                "std_f_overlap_value": float_text(std_value),
                "max_abs_deviation_from_mean": float_text(max_abs_deviation),
                "header_rule_uniform": bool_text(uniform),
                "path_mapping_computed": "false",
                "contains_mapping_vector": "false",
                "contains_theory_vector": "false",
                "contains_predictions": "false",
                "contains_residuals": "false",
                "contains_fit_statistics": "false",
                "uses_kids_data_vector_values": "false",
                "uses_posterior_chains": "false",
                "uses_posthoc_tile_selection": "false",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": policy["claim_boundary"],
            }
        )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    blockers = [row for row in rows if row["blocking_status"] != "not_blocking"]
    summary = {
        "policy_id": policy["policy_id"],
        "status": "KIDS1000_COSEBIS_F_OVERLAP_HEADER_FOOTPRINT_DEGENERACY_AUDIT_BUILT_UNIFORM_NOT_PROMOTABLE"
        if uniform
        else "KIDS1000_COSEBIS_F_OVERLAP_HEADER_FOOTPRINT_DEGENERACY_AUDIT_BUILT_NONUNIFORM",
        "tile_count": str(len(tile_rows)),
        "audit_item_count": str(len(rows)),
        "blocking_item_count": str(len(blockers)),
        "unique_f_overlap_value_count_rounded_1e_minus_12": str(unique_rounded),
        "mean_f_overlap_value": float_text(mean_value),
        "std_f_overlap_value": float_text(std_value),
        "max_abs_deviation_from_mean": float_text(max_abs_deviation),
        "header_rule_uniform": bool_text(uniform),
        "non_degenerate_mapping_support": bool_text(not uniform),
        "recommended_next_action": "derive_pixel_mask_or_subtile_overlap_rule"
        if uniform
        else "enter_mapping_preflight",
        "path_mapping_computed": "false",
        "contains_mapping_vector": "false",
        "contains_theory_vector": "false",
        "contains_predictions": "false",
        "contains_residuals": "false",
        "contains_fit_statistics": "false",
        "uses_kids_data_vector_values": "false",
        "uses_posterior_chains": "false",
        "uses_posthoc_tile_selection": "false",
        "endpoint_scoring_allowed": "false",
        "claim_boundary": policy["claim_boundary"],
    }
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)
    print(
        "PAPER10_KIDS1000_COSEBIS_F_OVERLAP_HEADER_FOOTPRINT_DEGENERACY_AUDIT_V1_BUILT "
        f"uniform={bool_text(uniform)} endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()

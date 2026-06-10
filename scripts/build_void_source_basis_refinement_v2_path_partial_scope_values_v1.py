#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_path_partial_scope_policy.csv"
OUT = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_path_partial_scope_values.csv"
SUMMARY = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_path_partial_scope_values_summary.csv"

ARTIFACT_ID = "VOID_SOURCE_BASIS_REFINEMENT_V2_PATH_PARTIAL_SCOPE_VALUES_V1"
CLAIM_BOUNDARY = "v2_path_partial_scope_values_source_only_not_endpoint"
MAX_CAVEATED_SEP_DEG = 2.0


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def source_path_value(eligibility: str, sep_deg: float) -> tuple[str, str, float]:
    if eligibility == "NOT_PATH_SCOPE_ELIGIBLE":
        return "PATH_OFF_OUTSIDE_PARTIAL_SCOPE", "0.000000000000e+00", 0.0
    raw = max(0.0, (MAX_CAVEATED_SEP_DEG - sep_deg) / MAX_CAVEATED_SEP_DEG)
    # Same bounded activation shell as the declared path rule, with the
    # caveat that P_path is only a tile-proximity proxy here.
    bounded = raw / (1.0 + abs(raw))
    return "SOURCE_ONLY_TILE_PROXIMITY_PARTIAL_SCOPE_VALUE", f"{bounded:.12e}", bounded


def main() -> None:
    policy_rows = read_rows(POLICY)
    if not policy_rows:
        raise SystemExit("partial scope policy is empty")

    rows: list[dict[str, str]] = []
    values: list[float] = []
    candidate_values: list[float] = []
    for row in policy_rows:
        value_status, value_text, value = source_path_value(
            row["path_scope_eligibility"], float(row["nearest_kids_tile_sep_deg"])
        )
        values.append(value)
        if row["path_scope_eligibility"] != "NOT_PATH_SCOPE_ELIGIBLE":
            candidate_values.append(value)
        rows.append(
            {
                "artifact_id": ARTIFACT_ID,
                "CID": row["CID"],
                "source_row_index": row["source_row_index"],
                "zHD": row["zHD"],
                "path_scope_eligibility": row["path_scope_eligibility"],
                "nearest_kids_tile_index_zero_based": row["nearest_kids_tile_index_zero_based"],
                "nearest_kids_tile_sep_deg": row["nearest_kids_tile_sep_deg"],
                "path_weight_rule": "P_tile=max(0,(2deg-sep)/2deg); W_path=P_tile/(1+abs(P_tile))",
                "path_weight_rule_scope": "partial_scope_only_tile_proximity_control",
                "W_path_value_status": value_status,
                "W_path_source_value": value_text,
                "full_lowz_W_path_channel": "false",
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "contains_endpoint_scores": "false",
                "contains_distance_residuals": "false",
                "contains_lensing_residuals": "false",
                "contains_fit_statistics": "false",
                "uses_kids_data_vector_values": "false",
                "uses_posterior_chains": "false",
                "uses_posthoc_sky_direction_selection": "false",
                "uses_posthoc_path_projection_labels": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    strict_count = sum(row["path_scope_eligibility"] == "STRICT_PATH_SCOPE_CANDIDATE" for row in rows)
    caveated_count = sum(row["path_scope_eligibility"] == "CAVEATED_PATH_SCOPE_CANDIDATE" for row in rows)
    candidate_count = strict_count + caveated_count
    summary = [
        {
            "artifact_id": ARTIFACT_ID,
            "status": "V2_PATH_PARTIAL_SCOPE_VALUES_FROZEN_NOT_ENDPOINT_READY",
            "partial_scope_policy_artifact": str(POLICY.relative_to(ROOT)),
            "n_rows": str(len(rows)),
            "strict_path_scope_candidate_count": str(strict_count),
            "caveated_path_scope_candidate_count": str(caveated_count),
            "total_path_scope_candidate_count": str(candidate_count),
            "full_lowz_scope_path_ready": "false",
            "partial_path_values_computed": "true",
            "full_lowz_path_values_computed": "false",
            "nonzero_partial_path_value_count": str(sum(value > 0.0 for value in values)),
            "min_candidate_W_path_source_value": f"{min(candidate_values):.12e}" if candidate_values else "NA",
            "max_candidate_W_path_source_value": f"{max(candidate_values):.12e}" if candidate_values else "NA",
            "mean_candidate_W_path_source_value": f"{sum(candidate_values) / len(candidate_values):.12e}"
            if candidate_values
            else "NA",
            "path_weight_rule": "P_tile=max(0,(2deg-sep)/2deg); W_path=P_tile/(1+abs(P_tile))",
            "rule_status": "SOURCE_ONLY_TILE_PROXIMITY_CONTROL_NOT_PHYSICAL_LENSING_WEIGHT",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "contains_endpoint_scores": "false",
            "contains_distance_residuals": "false",
            "contains_lensing_residuals": "false",
            "contains_fit_statistics": "false",
            "verdict": "partial_scope_W_path_values_available_only_as_source_side_control",
            "recommended_next_action": "external_review_before_any_partial_scope_replay_or_keep_W_path_disabled_for_full_lowz",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(OUT, rows)
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_V2_PATH_PARTIAL_SCOPE_VALUES_BUILT "
        f"candidate_rows={candidate_count} full_lowz=false endpoint=false"
    )


if __name__ == "__main__":
    main()

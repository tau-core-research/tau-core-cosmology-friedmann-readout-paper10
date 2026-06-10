#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CROSSMAP = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_path_projection_crossmap_audit.csv"
OUT = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_path_partial_scope_policy.csv"
SUMMARY = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_path_partial_scope_policy_summary.csv"

ARTIFACT_ID = "VOID_SOURCE_BASIS_REFINEMENT_V2_PATH_PARTIAL_SCOPE_POLICY_V1"
CLAIM_BOUNDARY = "v2_path_partial_scope_policy_not_values_not_scoring"


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


def main() -> None:
    crossmap_rows = read_rows(CROSSMAP)
    if not crossmap_rows:
        raise SystemExit("crossmap audit is empty")

    rows: list[dict[str, str]] = []
    for row in crossmap_rows:
        if row["nearest_tile_within_1_deg"] == "true":
            eligibility = "STRICT_PATH_SCOPE_CANDIDATE"
            recommended_role = "candidate_only_requires_path_weight_rule_freeze"
        elif row["nearest_tile_within_2_deg"] == "true":
            eligibility = "CAVEATED_PATH_SCOPE_CANDIDATE"
            recommended_role = "caveated_control_or_reviewer_gate_before_any_value"
        else:
            eligibility = "NOT_PATH_SCOPE_ELIGIBLE"
            recommended_role = "path_channel_off_for_this_row"
        rows.append(
            {
                "artifact_id": ARTIFACT_ID,
                "CID": row["CID"],
                "source_row_index": row["source_row_index"],
                "zHD": row["zHD"],
                "ra_deg": row["ra_deg"],
                "dec_deg": row["dec_deg"],
                "nearest_kids_tile_index_zero_based": row["nearest_kids_tile_index_zero_based"],
                "nearest_kids_tile_sep_deg": row["nearest_kids_tile_sep_deg"],
                "nearest_tile_within_1_deg": row["nearest_tile_within_1_deg"],
                "nearest_tile_within_2_deg": row["nearest_tile_within_2_deg"],
                "inside_kids_dec_filename_envelope": row["inside_kids_dec_filename_envelope"],
                "path_scope_eligibility": eligibility,
                "recommended_role": recommended_role,
                "W_path_value_status": "NOT_COMPUTED_PARTIAL_SCOPE_POLICY_ONLY",
                "W_path_source_value": "NA",
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
    eligible_count = strict_count + caveated_count
    summary = [
        {
            "artifact_id": ARTIFACT_ID,
            "status": "V2_PATH_PARTIAL_SCOPE_POLICY_FROZEN_VALUES_NOT_COMPUTED",
            "crossmap_audit_artifact": str(CROSSMAP.relative_to(ROOT)),
            "n_rows": str(len(rows)),
            "strict_path_scope_candidate_count": str(strict_count),
            "caveated_path_scope_candidate_count": str(caveated_count),
            "total_path_scope_candidate_count": str(eligible_count),
            "full_lowz_scope_path_ready": str(eligible_count == len(rows)).lower(),
            "path_values_computed": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "contains_endpoint_scores": "false",
            "contains_distance_residuals": "false",
            "contains_lensing_residuals": "false",
            "contains_fit_statistics": "false",
            "verdict": "W_path_is_partial_scope_candidate_only_not_full_lowz_channel",
            "recommended_next_action": "freeze_residual_blind_partial_scope_path_weight_rule_or_keep_W_path_disabled",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(OUT, rows)
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_V2_PATH_PARTIAL_SCOPE_POLICY_BUILT "
        f"strict={strict_count} caveated={caveated_count} path_values_computed=false"
    )


if __name__ == "__main__":
    main()

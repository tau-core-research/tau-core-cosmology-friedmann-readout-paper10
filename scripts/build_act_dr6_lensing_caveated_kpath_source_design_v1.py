#!/usr/bin/env python3
"""Build a caveated ACT DR6 K_path source-side design.

The design is a replay-preparation artifact, not a replay authorization.  It
uses the already frozen ACT baseline/curl/difference source products and
records the narrow conditions under which a future reviewer could allow a
caveated path-proxy replay.
"""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "source_manifest"
DERIVED = ROOT / "data" / "derived"
PRODUCT = SOURCE / "act_dr6_lensing_product_v1.csv"
CANDIDATE = DERIVED / "act_dr6_lensing_path_weight_candidate_v1_summary.csv"
CLOSURE = DERIVED / "act_dr6_lensing_reopen_closure_ledger_v1_summary.csv"
SCAFFOLD = DERIVED / "act_dr6_lensing_next_source_basis_design_scaffold_v1_summary.csv"
OUT = SOURCE / "act_dr6_lensing_caveated_kpath_source_design_v1.csv"
SUMMARY_OUT = DERIVED / "act_dr6_lensing_caveated_kpath_source_design_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise RuntimeError(f"expected one row in {path.relative_to(ROOT)}, found {len(rows)}")
    return rows[0]


def main() -> None:
    product = read_one(PRODUCT)
    candidate = read_one(CANDIDATE)
    closure = read_one(CLOSURE)
    scaffold = read_one(SCAFFOLD)

    rows = [
        {
            "artifact_id": "ACT_DR6_LENSING_CAVEATED_KPATH_SOURCE_DESIGN_V1",
            "design_item_id": "CKPATH_01_SOURCE_PRODUCT",
            "source_side_object": "ACT_DR6_baseline_kappa_alm_with_mask_and_null_variants",
            "source_basis_rule": product["local_path"],
            "allowed_channel_role": "K_path_candidate_caveated_proxy",
            "physical_path_weight_claimed": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "forbidden_inputs": "endpoint_scores;distance_residuals;fit_statistics;posthoc_product_choice",
            "claim_boundary": "source product exists but is not a physical path integral",
        },
        {
            "artifact_id": "ACT_DR6_LENSING_CAVEATED_KPATH_SOURCE_DESIGN_V1",
            "design_item_id": "CKPATH_02_PROXY_MAPPING",
            "source_side_object": "baseline_kappa_mask_positive_median_MAD_shape",
            "source_basis_rule": candidate["normalization_rule"],
            "allowed_channel_role": "dimensionless_K_path_shape_proxy",
            "physical_path_weight_claimed": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "forbidden_inputs": "endpoint_amplitude_tuning;distance_residuals;fit_statistics;best_fit_amplitude",
            "claim_boundary": "proxy mapping freezes shape only and carries no physical response amplitude",
        },
        {
            "artifact_id": "ACT_DR6_LENSING_CAVEATED_KPATH_SOURCE_DESIGN_V1",
            "design_item_id": "CKPATH_03_NULL_QUOTIENT_RULE",
            "source_side_object": "curl_and_frequency_difference_ACT_null_products",
            "source_basis_rule": "curl_null_and_diff_f150_f090_null_remain_K_null_controls",
            "allowed_channel_role": "K_null_control_suite",
            "physical_path_weight_claimed": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "forbidden_inputs": "curl_endpoint_performance_as_positive_signal;dropping_best_control;fit_statistics",
            "claim_boundary": "curl and frequency-difference products cannot be promoted in this design",
        },
        {
            "artifact_id": "ACT_DR6_LENSING_CAVEATED_KPATH_SOURCE_DESIGN_V1",
            "design_item_id": "CKPATH_04_COVERAGE_SCOPE",
            "source_side_object": "low_z_Pantheon_scope_with_ACT_mask_status",
            "source_basis_rule": (
                f"{candidate['source_rows']} source rows; {candidate['mask_positive_rows']} "
                f"mask-positive rows; outside-mask rows assigned zero source weight"
            ),
            "allowed_channel_role": "partial_coverage_source_scope",
            "physical_path_weight_claimed": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "forbidden_inputs": "posthoc_row_dropping;endpoint_score_thresholds;distance_residuals",
            "claim_boundary": "partial ACT coverage must be reported and cannot be converted into population completeness",
        },
        {
            "artifact_id": "ACT_DR6_LENSING_CAVEATED_KPATH_SOURCE_DESIGN_V1",
            "design_item_id": "CKPATH_05_REPLAY_PRECONDITIONS",
            "source_side_object": "external_review_and_control_survival_requirements",
            "source_basis_rule": (
                "external review must accept caveated proxy status; replay must include off, "
                "baseline-only, curl-null, diff-null, wrong-sign, deterministic-shuffle, "
                "rank-reverse, and source-basis-recenter controls"
            ),
            "allowed_channel_role": "review_gated_replay_candidate",
            "physical_path_weight_claimed": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "forbidden_inputs": "endpoint_replay_without_review;posthoc_recenter_rescue;family_verdict",
            "claim_boundary": "this design prepares reviewer authorization but does not authorize replay",
        },
    ]

    SOURCE.mkdir(parents=True, exist_ok=True)
    DERIVED.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "artifact_id": "ACT_DR6_LENSING_CAVEATED_KPATH_SOURCE_DESIGN_V1",
        "status": "CAVEATED_KPATH_SOURCE_DESIGN_READY_FOR_EXTERNAL_REVIEW_NOT_REPLAY",
        "source_product_artifact": product["artifact_id"],
        "candidate_artifact": candidate["artifact_id"],
        "closure_verdict": closure["verdict"],
        "scaffold_verdict": scaffold["verdict"],
        "source_rows": candidate["source_rows"],
        "mask_positive_rows": candidate["mask_positive_rows"],
        "mapping_status": "dimensionless_shape_proxy_only",
        "physical_lensing_path_weight_claimed": "false",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "family_verdict_allowed": "false",
        "dark_sector_inference_allowed": "false",
        "external_review_required_before_replay": "true",
        "control_suite_required": "off;baseline_only;curl_null;diff_f150_f090_null;wrong_sign;deterministic_shuffle;rank_reverse;source_basis_recenter_stress",
        "forbidden_action": "reuse_current_endpoint_scores;posthoc_recenter_rescue;drop_curl_control;claim_physical_K_path",
        "claim_boundary": (
            "this is a caveated source-side K_path proxy design for external review; "
            "it does not reopen endpoint scoring and does not override the current ACT quarantine"
        ),
        "verdict": "ACT_CAVEATED_KPATH_SOURCE_DESIGN_REVIEW_READY_NOT_REPLAY",
    }
    with SUMMARY_OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary))
        writer.writeheader()
        writer.writerow(summary)


if __name__ == "__main__":
    main()

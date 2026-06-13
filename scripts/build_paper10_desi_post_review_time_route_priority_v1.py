#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_post_review_time_route_priority_policy_v1.csv"
NEGATIVE = ROOT / "data/derived/paper10_desi_time_level_negative_control_response_gate_v1_summary.csv"
EXPANSION = ROOT / "data/derived/paper10_desi_time_readout_expansion_manifest_v1_summary.csv"
HOLDOUT = ROOT / "data/derived/paper10_desi_row5_holdout_confirmation_v1_summary.csv"
SYNTHESIS = ROOT / "data/derived/paper10_time_readout_route_synthesis_gate_v1.csv"
OUT = ROOT / "data/derived/paper10_desi_post_review_time_route_priority_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_post_review_time_route_priority_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_post_review_time_route_priority_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required input: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def one_row(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path.relative_to(ROOT)}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def require_false(row: dict[str, str], fields: list[str], label: str) -> None:
    for field in fields:
        if row[field] != "false":
            raise SystemExit(f"{label} {field} must be false")


def main() -> None:
    policy = one_row(POLICY)
    negative = one_row(NEGATIVE)
    expansion = one_row(EXPANSION)
    holdout = one_row(HOLDOUT)
    synthesis = one_row(SYNTHESIS)
    require_false(policy, ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"], "policy")
    require_false(negative, ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"], "negative")
    require_false(expansion, ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"], "expansion")
    require_false(holdout, ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"], "holdout")
    require_false(synthesis, ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"], "synthesis")
    if policy["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("bad priority claim boundary")
    if negative["verdict"] != "desi_time_level_negative_control_response_gate_blocks_replay_until_richer_clock_readout_support":
        raise SystemExit("priority gate expects negative-control route blocker")
    if expansion["verdict"] != "desi_time_readout_expansion_manifest_frozen_but_no_replay_ready_route":
        raise SystemExit("priority gate expects expansion manifest no-ready-route verdict")
    if holdout["verdict"] != "row5_holdout_confirmed_no_gate_closing_source_not_replay":
        raise SystemExit("priority gate expects row5 holdout confirmation")
    if synthesis["synthesis_status"] != "clock_slope_review_candidate_plus_independent_bao_level_route_underresolved_not_endpoint":
        raise SystemExit("priority gate expects level/slope synthesis blocker")

    rows = [
        {
            "priority_id": policy["priority_id"],
            "rank": "1",
            "route": "TIME_READOUT_SHAPE_OBSERVABLE",
            "post_review_role": "primary_next_source_derivation_gate",
            "source_reason": "constant_beta_level_route_is_ordering_fragile_and_level_slope_swap_control_beats_candidate",
            "allowed_work": "derive_source_frozen_slope_curvature_or_phase_observable_without_endpoint_scores",
            "blocked_by": "no_source_native_shape_observable_frozen",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "priority_id": policy["priority_id"],
            "rank": "2",
            "route": "ORDERING_CONTROL_SUITE",
            "post_review_role": "must_preserve_for_any_future_replay",
            "source_reason": "redshift_order_shuffle_is_best_control_in_current_diagnostic",
            "allowed_work": "freeze_leave_row_ordering_and_wrong_basis_controls_before_any_new_replay",
            "blocked_by": "ordering_controls_not_yet_extended_to_new_shape_route",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "priority_id": policy["priority_id"],
            "rank": "3",
            "route": "JOINT_COVARIANCE_AND_NUISANCE_POLICY",
            "post_review_role": "supporting_protocol_gate",
            "source_reason": "beta_rd_nuisance_and_BAO_CC_covariance_must_not_be_retuned_after_scores",
            "allowed_work": "freeze_joint_covariance_rd_marginalization_or_external_prior_policy",
            "blocked_by": "richer_shape_route_covariance_not_final",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "priority_id": policy["priority_id"],
            "rank": "4",
            "route": "MULTI_CLOCK_SUPPORT_PER_BAO_ROW",
            "post_review_role": "source_strengthening_gate",
            "source_reason": "nearest_neighbor_CC_only_scope_is_weak_and_row4_single_family_caveat_remains",
            "allowed_work": "add_independent_clock_redundancy_or_explicit_single_source_caveat_per_row",
            "blocked_by": "incomplete_independent_clock_redundancy",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "priority_id": policy["priority_id"],
            "rank": "5",
            "route": "HIGH_Z_INDEPENDENT_CLOCK_SUPPORT",
            "post_review_role": "future_holdout_reopen_gate_not_current_primary",
            "source_reason": "row5_has_no_gate_closing_high_z_clock_or_source_native_time_readout",
            "allowed_work": "keep_row5_holdout_or_prepare_separate_high_z_handoff_if_new_source_appears",
            "blocked_by": "row5_holdout_confirmed",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(OUT, rows)
    write_csv(
        SUMMARY,
        [
            {
                "priority_id": policy["priority_id"],
                "status": "POST_REVIEW_TIME_ROUTE_PRIORITY_BUILT_NOT_REPLAY_NOT_VALIDATION",
                "primary_next_gate": "TIME_READOUT_SHAPE_OBSERVABLE",
                "secondary_required_gate": "ORDERING_CONTROL_SUITE",
                "row5_role": "HIGH_Z_HOLDOUT_FUTURE_REOPEN_ONLY",
                "route_count": str(len(rows)),
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
                "verdict": "post_review_priority_is_shape_derivation_not_row5_replay",
            }
        ],
    )
    print("PAPER10_DESI_POST_REVIEW_TIME_ROUTE_PRIORITY_BUILT primary=TIME_READOUT_SHAPE_OBSERVABLE")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_ordering_control_suite_policy_v1.csv"
EXPANSION = ROOT / "data/source_manifest/paper10_desi_time_readout_expansion_manifest_v1.csv"
NEGATIVE_DIAG = ROOT / "data/derived/paper10_desi_time_level_negative_control_diagnostic_v1_summary.csv"
PROJECTION_SUMMARY = ROOT / "data/derived/paper10_desi_time_readout_shape_projection_induction_v1_summary.csv"
OUT = ROOT / "data/derived/paper10_desi_ordering_control_suite_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_ordering_control_suite_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_ordering_control_suite_not_validation"


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


def main() -> None:
    policy = one_row(POLICY)
    if policy["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("bad ordering-control policy claim boundary")
    for field in ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"]:
        if policy[field] != "false":
            raise SystemExit(f"policy {field} must remain false")

    expansion_rows = read_rows(EXPANSION)
    ordering_rows = [row for row in expansion_rows if row["route_id"] == "ORDERING_CONTROL_SUITE"]
    if len(ordering_rows) != 1:
        raise SystemExit("expansion manifest must declare exactly one ordering control route")
    ordering = ordering_rows[0]
    negative = one_row(NEGATIVE_DIAG)
    projection = one_row(PROJECTION_SUMMARY)
    if negative["failure_mode"] != "five_row_time_level_constant_beta_endpoint_is_ordering_fragile":
        raise SystemExit("ordering suite expects the constant-beta negative-control failure mode")
    if projection["quotient_survival_gate_status"] != "not_proven_ordering_null_unresolved":
        raise SystemExit("projection-induction ledger must keep ordering-null unresolved")

    controls = [
        {
            "control_family": "redshift_order_shuffle",
            "control_channel": "K_null",
            "source_status": "available_from_negative_control_diagnostic",
            "why_required": "previous_constant_beta_candidate_lost_to_redshift_order_shuffle",
            "minimum_future_rule": "must_be_preserved_for_shape_route",
        },
        {
            "control_family": "leave_row_or_pair",
            "control_channel": "K_null",
            "source_status": "required_not_yet_shape_bound",
            "why_required": "five_row_scope_is_small_and_single_row_leverage_must_be_checked",
            "minimum_future_rule": "must_report_leave_row_or_pair_sensitivity_before_replay",
        },
        {
            "control_family": "cc_window_stress",
            "control_channel": "K_null",
            "source_status": "required_not_yet_shape_bound",
            "why_required": "nearest_neighbor_CC_matching_and_row4_caveated_window_affect_clock_support",
            "minimum_future_rule": "must_preserve_fixed_CC_window_policy_or_caveat",
        },
        {
            "control_family": "wrong_time_basis",
            "control_channel": "K_null",
            "source_status": "required_not_yet_shape_bound",
            "why_required": "clock_level_or_phase_controls_must_not_outperform_the_predeclared_shape",
            "minimum_future_rule": "must_compare_clock_slope_against_wrong_time_basis_controls",
        },
        {
            "control_family": "rd_prior_stress",
            "control_channel": "K_null",
            "source_status": "required_not_yet_shape_bound",
            "why_required": "shape_route_removes_constant_beta_but_future_joint_policy_must_stress_rd_prior_choices",
            "minimum_future_rule": "must_keep_rd_prior_or_marginalization_policy_frozen",
        },
    ]
    rows: list[dict[str, str]] = []
    for control in controls:
        rows.append(
            {
                "gate_id": policy["gate_id"],
                "control_family": control["control_family"],
                "control_channel": control["control_channel"],
                "source_status": control["source_status"],
                "why_required": control["why_required"],
                "minimum_future_rule": control["minimum_future_rule"],
                "derived_from_expansion_manifest": "true",
                "redshift_shuffle_previously_better_than_candidate": "true",
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(OUT, rows)

    available_count = sum(row["source_status"].startswith("available") for row in rows)
    required_count = len(rows)
    summary = [
        {
            "gate_id": policy["gate_id"],
            "status": "DESI_ORDERING_CONTROL_SUITE_DECLARED_NOT_REPLAY_NOT_VALIDATION",
            "required_control_count": str(required_count),
            "available_control_count": str(available_count),
            "shape_bound_control_count": "0",
            "primary_k_null_blocker": "redshift_order_shuffle",
            "negative_control_failure_mode": negative["failure_mode"],
            "expansion_manifest_support_status": ordering["current_support_status"],
            "quotient_survival_gate_status": projection["quotient_survival_gate_status"],
            "ordering_control_suite_ready_for_replay": "false",
            "recommended_next_action": "bind_controls_to_shape_route_before_replay_authorization",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
            "verdict": "k_null_ordering_controls_declared_but_not_shape_bound",
        }
    ]
    write_csv(SUMMARY, summary)
    print(f"wrote {OUT.relative_to(ROOT)}")
    print(f"wrote {SUMMARY.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

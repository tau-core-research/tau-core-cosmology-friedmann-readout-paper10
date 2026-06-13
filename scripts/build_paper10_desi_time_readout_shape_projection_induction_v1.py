#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_time_readout_shape_projection_induction_policy_v1.csv"
SHAPE_SUMMARY = ROOT / "data/derived/paper10_desi_time_readout_shape_observable_gate_v1_summary.csv"
PRIORITY_SUMMARY = ROOT / "data/derived/paper10_desi_post_review_time_route_priority_v1_summary.csv"
ROUTE_SYNTHESIS = ROOT / "data/derived/paper10_time_readout_route_synthesis_gate_v1.csv"
OUT = ROOT / "data/derived/paper10_desi_time_readout_shape_projection_induction_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_time_readout_shape_projection_induction_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_time_readout_shape_projection_induction_not_validation"


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


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def main() -> None:
    policy = one_row(POLICY)
    if policy["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("bad projection-induction policy claim boundary")
    for field in ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"]:
        if policy[field] != "false":
            raise SystemExit(f"policy {field} must remain false")

    shape = one_row(SHAPE_SUMMARY)
    priority = one_row(PRIORITY_SUMMARY)
    route = one_row(ROUTE_SYNTHESIS)

    if shape["verdict"] != "desi_time_readout_shape_candidate_frozen_but_not_endpoint_ready":
        raise SystemExit("shape observable must remain candidate-not-endpoint")
    if priority["primary_next_gate"] != "TIME_READOUT_SHAPE_OBSERVABLE":
        raise SystemExit("post-review priority must select shape observable")
    if route["endpoint_replay_allowed"] != "false":
        raise SystemExit("route synthesis must not authorize endpoint replay")

    rows = [
        {
            "gate_id": policy["gate_id"],
            "candidate_id": "CLOCK_SLOPE_SHAPE",
            "tau_readout_channel": "K_time",
            "operational_source": "adjacent_first_difference_beta_shape",
            "tau_core_basis_mapping": "time_readout_clock_phase_channel",
            "activation_status": "source_candidate_activation_from_frozen_clock_BAO_gradient",
            "quotient_survival_status": "candidate_not_proven_against_ordering_null",
            "closure_stability_status": "constant_beta_removed_but_global_controls_unresolved",
            "readout_survival_status": "source_side_shape_exists_not_endpoint_authorized",
            "projection_induction_complete": "false",
            "allowed_role": "primary_source_side_time_shape_candidate",
            "required_next_gate": "independent_shape_review_or_ordering_control_suite",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": policy["gate_id"],
            "candidate_id": "CLOCK_CURVATURE_SHAPE",
            "tau_readout_channel": "K_time",
            "operational_source": "second_difference_curvature_shape",
            "tau_core_basis_mapping": "time_readout_clock_curvature_channel",
            "activation_status": "source_candidate_activation_from_frozen_clock_BAO_curvature",
            "quotient_survival_status": "candidate_not_proven_against_sparse_row_null",
            "closure_stability_status": "constant_beta_removed_but_five_row_scope_underpowered",
            "readout_survival_status": "source_side_shape_exists_not_endpoint_authorized",
            "projection_induction_complete": "false",
            "allowed_role": "secondary_source_side_time_shape_candidate",
            "required_next_gate": "multi_clock_support_or_independent_shape_review",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": policy["gate_id"],
            "candidate_id": "BAO_LEVEL_CONTEXT",
            "tau_readout_channel": "K_closure",
            "operational_source": "radial_BAO_time_interface_level_context",
            "tau_core_basis_mapping": "closure_test_context_not_clock_source",
            "activation_status": "context_activation_only",
            "quotient_survival_status": "not_a_clock_quotient_support_claim",
            "closure_stability_status": "level_alignment_context_only_slope_alignment_not_supportive",
            "readout_survival_status": "context_only_not_endpoint_authorized",
            "projection_induction_complete": "false",
            "allowed_role": "cross_probe_context",
            "required_next_gate": "do_not_treat_BAO_level_as_clock_support",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": policy["gate_id"],
            "candidate_id": "ORDERING_NULL_CONTROL",
            "tau_readout_channel": "K_null",
            "operational_source": "redshift_order_shuffle_and_leave_row_controls",
            "tau_core_basis_mapping": "null_baseline_absorber_channel",
            "activation_status": "required_control_activation",
            "quotient_survival_status": "must_defeat_ordering_null_before_replay",
            "closure_stability_status": "currently_unresolved_after_constant_beta_negative_control",
            "readout_survival_status": "blocks_endpoint_promotion",
            "projection_induction_complete": "false",
            "allowed_role": "mandatory_null_control",
            "required_next_gate": "ordering_control_suite",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(OUT, rows)

    summary = [
        {
            "gate_id": policy["gate_id"],
            "status": "DESI_TIME_READOUT_SHAPE_PROJECTION_INDUCTION_MAPPED_NOT_REPLAY_NOT_VALIDATION",
            "primary_candidate": "CLOCK_SLOPE_SHAPE",
            "secondary_candidate": "CLOCK_CURVATURE_SHAPE",
            "active_tau_channels": "K_time;K_closure;K_null",
            "shape_candidate_available": shape["shape_observable_candidate_available"],
            "endpoint_ready_shape_observable": shape["endpoint_ready_shape_observable"],
            "projection_induction_complete": "false",
            "activation_gate_status": "source_candidate_only",
            "quotient_survival_gate_status": "not_proven_ordering_null_unresolved",
            "closure_stability_gate_status": "partial_constant_beta_removed_controls_unresolved",
            "readout_survival_gate_status": "not_endpoint_authorized",
            "row5_role": priority["row5_role"],
            "recommended_next_action": "independent_shape_review_plus_ordering_control_suite_before_any_replay",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
            "verdict": "time_shape_maps_to_K_time_candidate_but_projection_induction_incomplete",
        }
    ]
    if summary[0]["shape_candidate_available"] != "true":
        raise SystemExit("shape candidate must be available before theory alignment")
    for row in rows:
        if row["projection_induction_complete"] != "false":
            raise SystemExit("projection induction must remain incomplete")
    write_csv(SUMMARY, summary)
    print(f"wrote {OUT.relative_to(ROOT)}")
    print(f"wrote {SUMMARY.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

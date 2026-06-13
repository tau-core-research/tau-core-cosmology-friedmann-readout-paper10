#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_time_level_route_external_rd_readiness_gate_v1.csv"
RD_POLICY = ROOT / "data/derived/paper10_time_level_rd_policy_selection_gate_v1_summary.csv"
RD_RESPONSE = ROOT / "data/derived/paper10_external_rd_prior_freeze_response_v1_summary.csv"
DIFF_AUDIT = ROOT / "data/derived/paper10_bao_rd_cancelled_time_level_difference_audit_v1_summary.csv"
RD_MARGINALIZATION = ROOT / "data/derived/paper10_bao_rd_marginalization_protocol_v1_summary.csv"
CONTROL_SUITE = ROOT / "data/derived/paper10_time_level_endpoint_control_suite_protocol_v1_summary.csv"
BAO_EXPANSION = ROOT / "data/derived/paper10_time_level_bao_support_expansion_manifest_v1_summary.csv"
DESI_BAO_INVENTORY = ROOT / "data/derived/paper10_desi_dr2_bao_source_inventory_v1_summary.csv"
DESI_BAO_INTERFACE = ROOT / "data/derived/paper10_desi_dr2_radial_bao_time_interface_v1_summary.csv"
DESI_CC_MATCH = ROOT / "data/derived/paper10_desi_dr2_radial_bao_cc_match_v1_summary.csv"
DESI_HIGH_Z_POLICY = ROOT / "data/derived/paper10_desi_dr2_high_z_bao_policy_v1_summary.csv"
DESI_CONTROL_SEEDS = ROOT / "data/derived/paper10_desi_time_level_control_seed_manifest_v1_summary.csv"
OUT = ROOT / "data/derived/paper10_time_level_route_external_rd_readiness_gate_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_time_level_route_external_rd_readiness_gate_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_time_level_route_external_rd_readiness_gate_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def require_false(row: dict[str, str], field: str) -> None:
    if row[field] != "false":
        raise SystemExit(f"{field} must remain false")


def require_no_endpoint_replay(row: dict[str, str]) -> None:
    if "endpoint_replay_allowed" in row:
        require_false(row, "endpoint_replay_allowed")
        return
    if "current_endpoint_replay_allowed" in row:
        if row["current_endpoint_replay_allowed"] != "false":
            raise SystemExit("current_endpoint_replay_allowed must remain false")
        return
    raise SystemExit("missing endpoint replay guard")


def main() -> None:
    policy = read_one(POLICY)
    rd_policy = read_one(RD_POLICY)
    rd_response = read_one(RD_RESPONSE)
    diff = read_one(DIFF_AUDIT)
    rd_marginalization = read_one(RD_MARGINALIZATION)
    control_suite = read_one(CONTROL_SUITE)
    bao_expansion = read_one(BAO_EXPANSION)
    desi_bao = read_one(DESI_BAO_INVENTORY)
    desi_interface = read_one(DESI_BAO_INTERFACE)
    desi_cc_match = read_one(DESI_CC_MATCH)
    desi_high_z = read_one(DESI_HIGH_Z_POLICY)
    desi_control_seeds = read_one(DESI_CONTROL_SEEDS)

    if policy["status"] != "SOURCE_SIDE_EXTERNAL_RD_READINESS_GATE_NOT_REPLAY_NOT_VALIDATION":
        raise SystemExit("bad policy status")
    if policy["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("bad claim boundary")
    for row in [
        policy,
        rd_policy,
        rd_response,
        diff,
        rd_marginalization,
        control_suite,
        bao_expansion,
        desi_bao,
        desi_interface,
        desi_cc_match,
        desi_high_z,
        desi_control_seeds,
    ]:
        require_no_endpoint_replay(row)
        for field in ["endpoint_validation_claimed", "physical_validation_claimed"]:
            require_false(row, field)

    if rd_policy["accepted_current_policy"] != "rd_cancelled_differential_direction":
        raise SystemExit("rd policy gate current policy changed")
    if "external_rd_prior" not in rd_policy["future_pending_policies"]:
        raise SystemExit("external rd prior route missing from policy gate")
    if rd_response["verdict"] != "planck2018_rd_prior_frozen_as_caveated_external_source_not_endpoint":
        raise SystemExit("external rd prior response not frozen")
    if diff["verdict"] != "rd_cancels_direction_agrees_but_bao_delta_low_significance_not_endpoint":
        raise SystemExit("differential BAO audit status changed")
    if rd_marginalization["verdict"] != "rd_marginalization_protocol_frozen_but_endpoint_still_blocked":
        raise SystemExit("rd marginalization protocol not frozen")
    if control_suite["verdict"] != "time_level_endpoint_control_suite_declared_but_not_replayed":
        raise SystemExit("endpoint control suite protocol not declared")
    if bao_expansion["verdict"] != "bao_support_expansion_routes_declared_but_current_endpoint_still_two_point_blocked":
        raise SystemExit("BAO support expansion manifest not declared")
    if desi_bao["verdict"] != "desi_dr2_public_bao_source_frozen_but_time_level_endpoint_not_replayed":
        raise SystemExit("DESI DR2 BAO source inventory not frozen")
    if int(desi_bao["radial_dh_over_rd_rows"]) < int(desi_bao["minimum_radial_rows_for_endpoint_consideration"]):
        raise SystemExit("DESI radial support below declared endpoint-consideration threshold")
    if desi_interface["verdict"] != "desi_radial_bao_time_interface_frozen_but_endpoint_replay_still_blocked":
        raise SystemExit("DESI radial BAO time interface not frozen")
    if desi_interface["radial_row_count"] != desi_bao["radial_dh_over_rd_rows"]:
        raise SystemExit("DESI inventory/interface radial counts disagree")
    if desi_cc_match["verdict"] != "desi_bao_cc_support_partially_matched_high_z_row_blocked_no_replay":
        raise SystemExit("DESI radial BAO CC match ledger not frozen")
    if desi_cc_match["matched_within_cc_range_rows"] != "5":
        raise SystemExit("DESI CC matched row count changed")
    if desi_cc_match["blocked_outside_cc_range_rows"] != "1":
        raise SystemExit("DESI CC blocked row count changed")
    if desi_high_z["verdict"] != "high_z_lya_row_predeclared_excluded_from_first_cc_matched_time_endpoint":
        raise SystemExit("DESI high-z policy not frozen")
    if desi_high_z["matched_rows_allowed_for_first_endpoint"] != desi_cc_match["matched_within_cc_range_rows"]:
        raise SystemExit("DESI high-z policy allowed row count mismatch")
    if desi_control_seeds["verdict"] != "desi_time_level_control_seed_manifest_frozen_not_replayed":
        raise SystemExit("DESI time-level control seed manifest not frozen")
    if desi_control_seeds["parent_high_z_policy"] != "PAPER10_DESI_DR2_HIGH_Z_BAO_POLICY_V1":
        raise SystemExit("DESI control seed manifest parent high-z policy changed")
    if desi_control_seeds["control_family_count"] != "7":
        raise SystemExit("DESI control seed manifest control-family count changed")
    if desi_control_seeds["transform_scope"] != "first_CC_matched_DESI_5row_scope":
        raise SystemExit("DESI control seed manifest scope changed")

    rows = [
        {
            "gate_id": policy["gate_id"],
            "item": "external_rd_prior_source_freeze",
            "status": "CLOSED_SOURCE_SIDE",
            "evidence": rd_response["prior_source_id"],
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": policy["gate_id"],
            "item": "joint_rd_marginalization_protocol_definition",
            "status": "CLOSED_SOURCE_SIDE",
            "evidence": rd_marginalization["protocol_id"],
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": policy["gate_id"],
            "item": "endpoint_control_suite_definition",
            "status": "CLOSED_SOURCE_SIDE",
            "evidence": control_suite["protocol_id"],
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": policy["gate_id"],
            "item": "bao_support_expansion_manifest_declared",
            "status": "CLOSED_SOURCE_SIDE",
            "evidence": bao_expansion["manifest_id"],
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": policy["gate_id"],
            "item": "desi_dr2_public_bao_source_inventory_frozen",
            "status": "CLOSED_SOURCE_SIDE",
            "evidence": f"radial_dh_over_rd_rows={desi_bao['radial_dh_over_rd_rows']};covariance_dimension={desi_bao['covariance_dimension']}",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": policy["gate_id"],
            "item": "desi_dr2_radial_bao_cc_match_ledger_frozen",
            "status": "CLOSED_SOURCE_SIDE",
            "evidence": f"matched_rows={desi_cc_match['matched_within_cc_range_rows']};blocked_rows={desi_cc_match['blocked_outside_cc_range_rows']};cc_extrapolation_used={desi_cc_match['cc_extrapolation_used']}",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": policy["gate_id"],
            "item": "desi_dr2_radial_bao_time_interface_frozen",
            "status": "CLOSED_SOURCE_SIDE",
            "evidence": f"radial_rows={desi_interface['radial_row_count']};z_range={desi_interface['z_min']}-{desi_interface['z_max']};covariance_dimension={desi_interface['covariance_dimension']}",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": policy["gate_id"],
            "item": "desi_dr2_high_z_row_policy_frozen",
            "status": "CLOSED_SOURCE_SIDE",
            "evidence": f"accepted_policy={desi_high_z['accepted_policy']};allowed_rows={desi_high_z['matched_rows_allowed_for_first_endpoint']};blocked_z_eff={desi_high_z['blocked_z_eff']}",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": policy["gate_id"],
            "item": "desi_time_level_control_seed_manifest_frozen",
            "status": "CLOSED_SOURCE_SIDE",
            "evidence": f"control_families={desi_control_seeds['control_family_count']};seed_range={desi_control_seeds['deterministic_seed_min']}-{desi_control_seeds['deterministic_seed_max']};scope={desi_control_seeds['transform_scope']}",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": policy["gate_id"],
            "item": "low_significance_current_sdss_bao_difference",
            "status": "CLOSED_DIAGNOSTIC_NOT_DESI_BLOCKER",
            "evidence": f"delta_bao_snr={diff['delta_bao_snr']}",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": policy["gate_id"],
            "item": "time_level_endpoint_authorization_review_missing",
            "status": "BLOCKER_OPEN",
            "evidence": "source_side_scope_and_control_seeds_frozen_but_no_completed_endpoint_authorization_review",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(OUT, rows)

    summary = {
        "gate_id": policy["gate_id"],
        "status": "SOURCE_SIDE_EXTERNAL_RD_READINESS_GATE_COMPLETE_NOT_REPLAY_NOT_VALIDATION",
        "closed_source_side_blockers": (
            "external_rd_prior_source_freeze;"
            "joint_rd_marginalization_protocol_definition;"
            "endpoint_control_suite_definition;"
            "bao_support_expansion_manifest_declared;"
            "desi_dr2_public_bao_source_inventory_frozen;"
            "desi_dr2_radial_bao_time_interface_frozen;"
            "desi_dr2_radial_bao_cc_match_ledger_frozen;"
            "desi_dr2_high_z_row_policy_frozen;"
            "desi_time_level_control_seed_manifest_frozen"
        ),
        "closed_diagnostics_not_active_endpoint_blockers": "low_significance_current_sdss_bao_difference",
        "open_endpoint_blockers": "time_level_endpoint_authorization_review_missing",
        "rd_prior_source_id": rd_response["prior_source_id"],
        "rd_mpc": rd_response["rd_mpc"],
        "sigma_rd_mpc": rd_response["sigma_rd_mpc"],
        "desi_dr2_radial_dh_over_rd_rows": desi_bao["radial_dh_over_rd_rows"],
        "desi_dr2_covariance_dimension": desi_bao["covariance_dimension"],
        "desi_dr2_time_interface_z_range": f"{desi_interface['z_min']};{desi_interface['z_max']}",
        "desi_dr2_cc_matched_rows": desi_cc_match["matched_within_cc_range_rows"],
        "desi_dr2_cc_blocked_rows": desi_cc_match["blocked_outside_cc_range_rows"],
        "desi_dr2_first_cc_matched_endpoint_rows": desi_high_z["matched_rows_allowed_for_first_endpoint"],
        "desi_time_level_control_family_count": desi_control_seeds["control_family_count"],
        "desi_time_level_control_seed_range": f"{desi_control_seeds['deterministic_seed_min']};{desi_control_seeds['deterministic_seed_max']}",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
        "verdict": "desi_time_cc_matched_scope_and_controls_frozen_but_endpoint_authorization_missing",
    }
    write_csv(SUMMARY, [summary])
    print(
        "PAPER10_TIME_LEVEL_ROUTE_EXTERNAL_RD_READINESS_GATE_BUILT "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()

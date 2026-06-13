#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_time_readout_level_slope_route_split_ledger_policy_v1.csv"
CLOCK_GATE = ROOT / "data/derived/pantheon_clock_slope_route_gate_v1.csv"
BAO_AUDIT = ROOT / "data/derived/sdss_bao_time_readout_observable_route_audit_v1_summary.csv"
JOINT_AUDIT = ROOT / "data/derived/paper10_joint_cc_bao_time_route_consistency_audit_v1_summary.csv"
SYNTHESIS = ROOT / "data/derived/paper10_time_readout_route_synthesis_gate_v1.csv"
OUT = ROOT / "data/derived/paper10_time_readout_level_slope_route_split_ledger_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_time_readout_level_slope_route_split_ledger_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_time_readout_level_slope_route_split_ledger_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def require_false(row: dict[str, str], field: str) -> None:
    if row[field] != "false":
        raise SystemExit(f"{field} must be false in {row}")


def main() -> None:
    policy = read_one(POLICY)
    clock = read_one(CLOCK_GATE)
    bao = read_one(BAO_AUDIT)
    joint = read_one(JOINT_AUDIT)
    synthesis = read_one(SYNTHESIS)

    if policy["status"] != "SOURCE_SIDE_ROUTE_SPLIT_LEDGER_NOT_REPLAY_NOT_VALIDATION":
        raise SystemExit("bad policy status")
    if policy["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("bad claim boundary")
    for row in [policy, clock, bao, joint, synthesis]:
        for field in ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"]:
            require_false(row, field)

    if clock["selected_route_candidate_family"] != "clock_slope":
        raise SystemExit("clock gate must remain clock_slope")
    if clock["local_controls_pass"] != "true" or clock["global_controls_pass"] != "false":
        raise SystemExit("clock_slope gate blocker changed")
    if joint["verdict"] != "radial_bao_aligns_with_cc_level_not_cc_slope_underresolved_not_replay":
        raise SystemExit("joint CC+BAO verdict changed")
    if joint["bao_cc_level_two_point_alignment"] != "1" or joint["bao_cc_slope_two_point_alignment"] != "-1":
        raise SystemExit("joint CC+BAO alignment changed")
    if synthesis["synthesis_status"] != "clock_slope_review_candidate_plus_independent_bao_level_route_underresolved_not_endpoint":
        raise SystemExit("synthesis gate is not the expected split-ready status")

    common = {
        "split_id": policy["gate_id"],
        "status": "SOURCE_SIDE_ROUTE_SPLIT_RECORDED_NOT_REPLAY_NOT_VALIDATION",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    rows = [
        {
            **common,
            "route_id": "time_level_route",
            "route_interpretation": "expansion_level_logH_like_readout",
            "primary_source_evidence": "radial_BAO_DH_over_rd_plus_nearest_CC_logH_level_alignment",
            "source_side_support_status": "independent_bao_level_route_present",
            "cc_support_status": "nearest_CC_level_alignment_two_point",
            "bao_support_status": bao["verdict"],
            "joint_route_alignment": joint["bao_cc_level_two_point_alignment"],
            "main_blockers": "two_point_underresolved;rd_nuisance_unresolved;no_frozen_joint_interface_policy",
            "allowed_next_route": "build_source_side_level_route_with_frozen_rd_or_marginalization_policy_no_endpoint_scores",
            "forbidden_route": "endpoint_replay_or_validation_from_two_BAO_points",
        },
        {
            **common,
            "route_id": "time_slope_route",
            "route_interpretation": "clock_slope_dlogH_dlog1pz_readout",
            "primary_source_evidence": "CC_clock_slope_candidate_local_controls_pass",
            "source_side_support_status": clock["route_status"],
            "cc_support_status": "local_controls_pass_global_controls_blocked",
            "bao_support_status": "radial_BAO_not_slope_support_in_current_joint_audit",
            "joint_route_alignment": joint["bao_cc_slope_two_point_alignment"],
            "main_blockers": "global_rank_control_blocker;external_reviewer_authorization_not_completed;BAO_anti_alignment",
            "allowed_next_route": "complete_clock_slope_reviewer_authorization_or_refine_slope_source_basis_no_endpoint_scores",
            "forbidden_route": "claiming_radial_BAO_as_clock_slope_support",
        },
    ]
    write_csv(OUT, rows)

    summary = {
        "split_id": policy["gate_id"],
        "status": "SOURCE_SIDE_ROUTE_SPLIT_LEDGER_COMPLETE_NOT_REPLAY_NOT_VALIDATION",
        "routes_recorded": str(len(rows)),
        "level_route_status": rows[0]["source_side_support_status"],
        "slope_route_status": rows[1]["source_side_support_status"],
        "level_alignment": joint["bao_cc_level_two_point_alignment"],
        "slope_alignment": joint["bao_cc_slope_two_point_alignment"],
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
        "verdict": "level_and_slope_time_routes_split_source_side_not_endpoint",
    }
    write_csv(SUMMARY, [summary])
    print(
        "PAPER10_TIME_READOUT_LEVEL_SLOPE_ROUTE_SPLIT_LEDGER_BUILT "
        f"routes={summary['routes_recorded']} verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()

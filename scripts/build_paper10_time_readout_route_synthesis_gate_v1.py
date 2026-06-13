#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_time_readout_route_synthesis_gate_v1.csv"
CLOCK_GATE = ROOT / "data/derived/pantheon_clock_slope_route_gate_v1.csv"
BAO_AUDIT = ROOT / "data/derived/sdss_bao_time_readout_observable_route_audit_v1_summary.csv"
JOINT_AUDIT = ROOT / "data/derived/paper10_joint_cc_bao_time_route_consistency_audit_v1_summary.csv"
OUT = ROOT / "data/derived/paper10_time_readout_route_synthesis_gate_v1.csv"
CLAIM_BOUNDARY = "paper10_time_readout_route_synthesis_gate_not_validation"


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
        raise SystemExit(f"{field} must be false")


def main() -> None:
    policy = read_one(POLICY)
    clock = read_one(CLOCK_GATE)
    bao = read_one(BAO_AUDIT)
    joint = read_one(JOINT_AUDIT)
    if policy["status"] != "SOURCE_SIDE_ROUTE_SYNTHESIS_NOT_REPLAY_NOT_VALIDATION":
        raise SystemExit("bad policy status")
    if policy["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("bad claim boundary")
    for field in ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"]:
        require_false(policy, field)
        require_false(clock, field)
        require_false(bao, field)
        require_false(joint, field)

    if clock["selected_route_candidate_family"] != "clock_slope":
        raise SystemExit("clock_slope must remain the selected CC route")
    if clock["local_controls_pass"] != "true" or clock["global_controls_pass"] != "false":
        raise SystemExit("clock_slope route must remain local-pass/global-blocked")
    if bao["verdict"] != "independent_radial_bao_time_observable_present_but_underresolved_not_replay":
        raise SystemExit("unexpected radial BAO audit verdict")
    if joint["verdict"] != "radial_bao_aligns_with_cc_level_not_cc_slope_underresolved_not_replay":
        raise SystemExit("unexpected joint CC+BAO audit verdict")
    if joint["bao_cc_level_two_point_alignment"] != "1" or joint["bao_cc_slope_two_point_alignment"] != "-1":
        raise SystemExit("joint CC+BAO route consistency changed")

    row = {
        "gate_id": policy["gate_id"],
        "status": "SOURCE_SIDE_ROUTE_SYNTHESIS_COMPLETE_NOT_REPLAY_NOT_VALIDATION",
        "cc_selected_route": clock["selected_route_candidate_family"],
        "cc_route_status": clock["route_status"],
        "cc_local_controls_pass": clock["local_controls_pass"],
        "cc_global_controls_pass": clock["global_controls_pass"],
        "cc_delta_chi2_candidate_minus_baseline": clock["candidate_delta_chi2_minus_baseline"],
        "radial_bao_route_status": bao["verdict"],
        "radial_bao_rows": bao["radial_bao_rows"],
        "radial_bao_redshift_range": bao["redshift_range"],
        "radial_bao_independent_from_cc_clock_level_route": bao["independent_from_cc_clock_level_route"],
        "radial_bao_rd_nuisance_unresolved": bao["rd_nuisance_unresolved"],
        "radial_bao_underresolved_for_endpoint_route": bao["underresolved_for_endpoint_route"],
        "joint_cc_bao_time_route_verdict": joint["verdict"],
        "joint_cc_bao_level_alignment": joint["bao_cc_level_two_point_alignment"],
        "joint_cc_bao_slope_alignment": joint["bao_cc_slope_two_point_alignment"],
        "joint_cc_bao_two_point_underresolved": joint["two_point_underresolved"],
        "synthesis_status": (
            "clock_slope_review_candidate_plus_independent_bao_level_route_underresolved_not_endpoint"
        ),
        "allowed_next_route": (
            "complete_clock_slope_reviewer_authorization_or_build_separate_level_and_slope_time_routes_without_endpoint_scores"
        ),
        "forbidden_next_route": (
            "endpoint_replay_validation_or_claiming_radial_bao_supports_clock_slope_before_joint_nuisance_policy"
        ),
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(OUT, [row])
    print(
        "PAPER10_TIME_READOUT_ROUTE_SYNTHESIS_GATE_BUILT "
        f"status={row['synthesis_status']}"
    )


if __name__ == "__main__":
    main()

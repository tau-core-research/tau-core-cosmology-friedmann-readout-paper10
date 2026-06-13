#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/pantheon_clock_slope_route_gate_policy_v1.csv"
CANDIDATE_SUMMARY = ROOT / "data/derived/pantheon_time_readout_clock_rate_phase_cc_support_candidate_v1_summary.csv"
SCREEN_SUMMARY = ROOT / "data/derived/pantheon_clock_rate_phase_cc_support_fast_screen_v1_summary.csv"
FAMILY_SUMMARY = ROOT / "data/derived/pantheon_clock_rate_phase_cc_support_fast_screen_v1_family_summary.csv"
OUT = ROOT / "data/derived/pantheon_clock_slope_route_gate_v1.csv"
CLAIM_BOUNDARY = "clock_slope_route_gate_source_side_not_replay_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain one row")
    return rows[0]


def write_one(path: Path, row: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(row.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(row)


def main() -> None:
    policy = read_one(POLICY)
    candidate = read_one(CANDIDATE_SUMMARY)
    screen = read_one(SCREEN_SUMMARY)
    families = {row["family_id"]: row for row in read_rows(FAMILY_SUMMARY)}
    if policy["status"] != "SOURCE_SIDE_ROUTE_GATE_NOT_REPLAY_NOT_VALIDATION":
        raise SystemExit("bad route policy status")
    for field in ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"]:
        if policy[field] != "false":
            raise SystemExit(f"{field} must be false")
    if policy["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("bad policy claim boundary")
    if candidate["verdict"] != "clock_rate_phase_cc_support_candidate_frozen_source_side_not_endpoint_authorized":
        raise SystemExit("unexpected parent candidate verdict")
    if screen["verdict"] != "clock_rate_phase_cc_support_fast_screen_not_control_resistant":
        raise SystemExit("unexpected parent screen verdict")
    if screen["best_candidate_family"] != "clock_slope":
        raise SystemExit("clock_slope must be the best candidate before route gate")
    slope = families.get("clock_slope")
    if slope is None:
        raise SystemExit("missing clock_slope family row")

    local_controls_pass = slope["family_survives_local_controls"] == "true"
    global_controls_pass = int(screen["controls_better_than_candidate_chi2"]) == 0
    baseline_improves = float(screen["delta_chi2_candidate_minus_baseline"]) < 0
    route_status = (
        "CLOCK_SLOPE_REVIEW_CANDIDATE_ENDPOINT_BLOCKED_BY_GLOBAL_CONTROL"
        if local_controls_pass and baseline_improves and not global_controls_pass
        else "CLOCK_SLOPE_ROUTE_NOT_READY"
    )
    next_action = (
        "build_reviewer_gated_slope_only_route_or_find_independent_time_observable_before_endpoint"
        if route_status == "CLOCK_SLOPE_REVIEW_CANDIDATE_ENDPOINT_BLOCKED_BY_GLOBAL_CONTROL"
        else "do_not_open_clock_slope_route"
    )

    row = {
        "gate_id": policy["gate_id"],
        "status": "SOURCE_SIDE_ROUTE_GATE_COMPLETE_NOT_REPLAY_NOT_VALIDATION",
        "parent_candidate_rows": candidate["included_rows"],
        "parent_used_cc_bin_count": candidate["used_cc_bin_count"],
        "parent_cc_support_edge_counts": candidate["cc_support_edge_counts"],
        "selected_route_candidate_family": "clock_slope",
        "route_source_reason": "clock_slope_is_rate_of_log_expansion_with_respect_to_log_scale_factor_proxy",
        "clock_level_status": "background_level_control_not_selected_as_time_readout_route",
        "clock_phase_status": "mixed_product_control_not_selected_as_primary_time_readout_route",
        "candidate_delta_chi2_minus_baseline": screen["delta_chi2_candidate_minus_baseline"],
        "candidate_delta_chi2_minus_best_global_control": screen["delta_chi2_candidate_minus_best_global_control"],
        "candidate_rank_among_candidate_and_controls": screen["candidate_rank_by_chi2_among_candidate_and_controls"],
        "best_global_control": f"{screen['best_global_control_branch']}/{screen['best_global_control_family']}",
        "local_controls_pass": "true" if local_controls_pass else "false",
        "global_controls_pass": "true" if global_controls_pass else "false",
        "baseline_improves": "true" if baseline_improves else "false",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "route_status": route_status,
        "allowed_next_route": policy["allowed_next_route"],
        "forbidden_next_route": policy["forbidden_next_route"],
        "recommended_next_action": next_action,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_one(OUT, row)
    print(
        "PAPER10_CLOCK_SLOPE_ROUTE_GATE_BUILT "
        f"route_status={route_status} local_controls_pass={row['local_controls_pass']} "
        f"global_controls_pass={row['global_controls_pass']}"
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "data/source_manifest/paper10_time_level_endpoint_control_suite_protocol_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_time_level_endpoint_control_suite_protocol_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_time_level_endpoint_control_suite_protocol_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def write_csv(path: Path, row: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(row.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(row)


def main() -> None:
    row = read_one(PROTOCOL)
    require(row["status"] == "SOURCE_SIDE_ENDPOINT_CONTROL_SUITE_PROTOCOL_NOT_REPLAY_NOT_VALIDATION", "bad status")
    require(row["route_id"] == "time_level_route", "bad route")
    for control in [
        "rd_off_control",
        "external_prior_width_stress",
        "wrong_prior_control",
        "BAO_pair_drop_control",
        "CC_match_window_stress",
        "level_slope_swap_control",
        "redshift_order_shuffle_control",
    ]:
        require(control in row["control_families"], f"missing control: {control}")
    for requirement in [
        "all_control_families_declared_before_endpoint",
        "seeds_frozen_before_replay",
        "control_outputs_reported_before_interpretation",
    ]:
        require(requirement in row["minimum_required_controls"], f"missing requirement: {requirement}")
    require(row["deterministic_seed_policy"] == "future_seed_manifest_required_no_current_scores", "bad seed policy")
    for forbidden in [
        "Pantheon_distance_residuals",
        "fit_statistics",
        "endpoint_scores",
        "late_time_fit_parameters",
        "posthoc_control_selection",
        "posthoc_seed_selection",
        "control_family_dropped_after_score",
    ]:
        require(forbidden in row["forbidden_inputs"], f"missing forbidden input: {forbidden}")
    require(row["endpoint_replay_allowed"] == "false", "endpoint replay must remain false")
    require(row["endpoint_validation_claimed"] == "false", "endpoint validation must remain false")
    require(row["physical_validation_claimed"] == "false", "physical validation must remain false")
    require(row["claim_boundary"] == CLAIM_BOUNDARY, "bad claim boundary")

    summary = {
        "protocol_id": row["protocol_id"],
        "status": "TIME_LEVEL_ENDPOINT_CONTROL_SUITE_PROTOCOL_READY_NOT_REPLAY_NOT_VALIDATION",
        "route_id": row["route_id"],
        "control_family_count": str(len(row["control_families"].split(";"))),
        "protocol_blocker_closed": "endpoint_control_suite_definition",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
        "verdict": "time_level_endpoint_control_suite_declared_but_not_replayed",
    }
    write_csv(SUMMARY, summary)
    print(f"PAPER10_TIME_LEVEL_ENDPOINT_CONTROL_SUITE_PROTOCOL_VALIDATED verdict={summary['verdict']}")


if __name__ == "__main__":
    main()

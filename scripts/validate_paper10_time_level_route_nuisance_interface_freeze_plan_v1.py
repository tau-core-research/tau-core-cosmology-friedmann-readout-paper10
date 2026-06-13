#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "data/source_manifest/paper10_time_level_route_nuisance_interface_freeze_plan_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_time_level_route_nuisance_interface_freeze_plan_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_time_level_route_nuisance_interface_freeze_plan_not_validation"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    row = read_one(PLAN)
    require(row["status"] == "SOURCE_SIDE_NUISANCE_INTERFACE_PLAN_NOT_REPLAY_NOT_VALIDATION", "bad status")
    require(row["route_id"] == "time_level_route", "plan must apply to time_level_route")
    require(row["nuisance_parameter"] == "rd", "rd nuisance must be explicit")
    require("two_point_directional_level_alignment_only" in row["allowed_current_use"], "allowed use too broad")
    require("no_absolute_H_scale_claim" in row["allowed_current_use"], "absolute-scale blocker missing")
    require("fitting_rd_from_Pantheon_residuals" in row["forbidden_use"], "rd leakage forbidden move missing")
    require("using_BAO_as_clock_slope_support" in row["forbidden_use"], "clock-slope leakage forbidden move missing")
    require("freeze_external_rd_prior_or_rd_marginalization_policy" in row["next_required_source_gate"], "next rd gate missing")
    for field in ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"]:
        require(row[field] == "false", f"{field} must remain false")
    require(row["claim_boundary"] == CLAIM_BOUNDARY, "bad claim boundary")

    summary = {
        "plan_id": row["plan_id"],
        "status": "SOURCE_SIDE_NUISANCE_INTERFACE_PLAN_VALIDATED_NOT_REPLAY_NOT_VALIDATION",
        "route_id": row["route_id"],
        "nuisance_parameter": row["nuisance_parameter"],
        "allowed_current_use": row["allowed_current_use"],
        "next_required_source_gate": row["next_required_source_gate"],
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
        "verdict": "time_level_route_rd_policy_required_before_endpoint",
    }
    write_csv(SUMMARY, [summary])
    print(
        "PAPER10_TIME_LEVEL_ROUTE_NUISANCE_INTERFACE_FREEZE_PLAN_VALIDATED "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()

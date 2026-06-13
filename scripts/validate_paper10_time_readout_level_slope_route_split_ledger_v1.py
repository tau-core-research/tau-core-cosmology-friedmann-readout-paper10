#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
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


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    rows = read_rows(OUT)
    summary = read_one(SUMMARY)
    require(len(rows) == 2, "ledger must contain exactly level and slope routes")
    by_route = {row["route_id"]: row for row in rows}
    require(set(by_route) == {"time_level_route", "time_slope_route"}, "bad route ids")
    for row in rows + [summary]:
        require(row["endpoint_replay_allowed"] == "false", "endpoint replay must remain false")
        require(row["endpoint_validation_claimed"] == "false", "endpoint validation must remain false")
        require(row["physical_validation_claimed"] == "false", "physical validation must remain false")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "bad claim boundary")

    level = by_route["time_level_route"]
    slope = by_route["time_slope_route"]
    require(level["joint_route_alignment"] == "1", "level route must carry BAO/CC level alignment")
    require(slope["joint_route_alignment"] == "-1", "slope route must preserve BAO anti-alignment")
    require("rd_nuisance_unresolved" in level["main_blockers"], "level route must preserve rd blocker")
    require("two_point_underresolved" in level["main_blockers"], "level route must preserve underresolved blocker")
    require("global_rank_control_blocker" in slope["main_blockers"], "slope route must preserve global control blocker")
    require("claiming_radial_BAO_as_clock_slope_support" in slope["forbidden_route"], "slope forbidden route missing")
    require(summary["verdict"] == "level_and_slope_time_routes_split_source_side_not_endpoint", "bad verdict")
    print(
        "PAPER10_TIME_READOUT_LEVEL_SLOPE_ROUTE_SPLIT_LEDGER_VALIDATED "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()

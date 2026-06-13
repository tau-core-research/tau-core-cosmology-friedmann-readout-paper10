#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "data/derived/pantheon_clock_slope_route_gate_v1.csv"
CLAIM_BOUNDARY = "clock_slope_route_gate_source_side_not_replay_not_validation"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain one row")
    return rows[0]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    gate = read_one(GATE)
    require(gate["gate_id"] == "PANTHEON_CLOCK_SLOPE_ROUTE_GATE_V1", "bad gate id")
    require(gate["status"] == "SOURCE_SIDE_ROUTE_GATE_COMPLETE_NOT_REPLAY_NOT_VALIDATION", "bad status")
    require(gate["selected_route_candidate_family"] == "clock_slope", "route must select clock_slope")
    require(gate["parent_candidate_rows"] == "1370", "unexpected parent row count")
    require(gate["parent_used_cc_bin_count"] == "31", "unexpected parent CC support count")
    require(gate["baseline_improves"] == "true", "clock_slope should improve over baseline")
    require(gate["local_controls_pass"] == "true", "clock_slope should pass local family controls")
    require(gate["global_controls_pass"] == "false", "global control blocker must remain explicit")
    require(gate["endpoint_replay_allowed"] == "false", "gate must not allow endpoint replay")
    require(gate["endpoint_validation_claimed"] == "false", "gate must not claim endpoint validation")
    require(gate["physical_validation_claimed"] == "false", "gate must not claim physical validation")
    require(
        gate["route_status"] == "CLOCK_SLOPE_REVIEW_CANDIDATE_ENDPOINT_BLOCKED_BY_GLOBAL_CONTROL",
        "unexpected route status",
    )
    require(gate["claim_boundary"] == CLAIM_BOUNDARY, "bad claim boundary")
    print(
        "PAPER10_CLOCK_SLOPE_ROUTE_GATE_VALIDATED "
        f"route_status={gate['route_status']}"
    )


if __name__ == "__main__":
    main()

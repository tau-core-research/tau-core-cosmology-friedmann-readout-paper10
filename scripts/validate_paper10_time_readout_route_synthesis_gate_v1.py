#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/paper10_time_readout_route_synthesis_gate_v1.csv"
CLAIM_BOUNDARY = "paper10_time_readout_route_synthesis_gate_not_validation"


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
    row = read_one(OUT)
    require(row["status"] == "SOURCE_SIDE_ROUTE_SYNTHESIS_COMPLETE_NOT_REPLAY_NOT_VALIDATION", "bad status")
    require(row["cc_selected_route"] == "clock_slope", "bad CC route")
    require(row["cc_local_controls_pass"] == "true", "CC local control pass must be preserved")
    require(row["cc_global_controls_pass"] == "false", "CC global control blocker must be preserved")
    require(
        row["radial_bao_route_status"]
        == "independent_radial_bao_time_observable_present_but_underresolved_not_replay",
        "bad radial BAO status",
    )
    require(row["radial_bao_rows"] == "2", "radial BAO must remain underresolved")
    require(row["radial_bao_independent_from_cc_clock_level_route"] == "true", "BAO route independence lost")
    require(row["radial_bao_rd_nuisance_unresolved"] == "true", "rd blocker must be explicit")
    require(row["radial_bao_underresolved_for_endpoint_route"] == "true", "underresolved blocker must be explicit")
    require(
        row["joint_cc_bao_time_route_verdict"]
        == "radial_bao_aligns_with_cc_level_not_cc_slope_underresolved_not_replay",
        "bad joint CC+BAO route verdict",
    )
    require(row["joint_cc_bao_level_alignment"] == "1", "BAO must align with CC level in the two-point audit")
    require(row["joint_cc_bao_slope_alignment"] == "-1", "BAO must not be claimed as CC slope support")
    require(row["joint_cc_bao_two_point_underresolved"] == "true", "joint audit underresolution blocker missing")
    require(
        row["synthesis_status"]
        == "clock_slope_review_candidate_plus_independent_bao_level_route_underresolved_not_endpoint",
        "bad synthesis status",
    )
    require(row["endpoint_replay_allowed"] == "false", "endpoint replay must not be allowed")
    require(row["endpoint_validation_claimed"] == "false", "endpoint validation must not be claimed")
    require(row["physical_validation_claimed"] == "false", "physical validation must not be claimed")
    require(row["claim_boundary"] == CLAIM_BOUNDARY, "bad claim boundary")
    print(
        "PAPER10_TIME_READOUT_ROUTE_SYNTHESIS_GATE_VALIDATED "
        f"status={row['synthesis_status']}"
    )


if __name__ == "__main__":
    main()

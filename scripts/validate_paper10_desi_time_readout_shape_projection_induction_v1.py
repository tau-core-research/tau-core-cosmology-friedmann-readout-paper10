#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_time_readout_shape_projection_induction_policy_v1.csv"
OUT = ROOT / "data/derived/paper10_desi_time_readout_shape_projection_induction_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_time_readout_shape_projection_induction_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_time_readout_shape_projection_induction_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def one_row(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    policy = one_row(POLICY)
    rows = read_rows(OUT)
    summary = one_row(SUMMARY)
    require(policy["claim_boundary"] == CLAIM_BOUNDARY, "bad policy claim boundary")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "bad summary claim boundary")
    require(len(rows) == 4, "projection-induction ledger must contain four rows")

    for row in rows + [policy, summary]:
        require(row["endpoint_replay_allowed"] == "false", "must not authorize endpoint replay")
        require(row["endpoint_validation_claimed"] == "false", "must not claim endpoint validation")
        require(row["physical_validation_claimed"] == "false", "must not claim physical validation")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "bad row claim boundary")

    by_candidate = {row["candidate_id"]: row for row in rows}
    require(set(by_candidate) == {"CLOCK_SLOPE_SHAPE", "CLOCK_CURVATURE_SHAPE", "BAO_LEVEL_CONTEXT", "ORDERING_NULL_CONTROL"}, "unexpected candidate set")
    require(by_candidate["CLOCK_SLOPE_SHAPE"]["tau_readout_channel"] == "K_time", "clock slope must map to K_time")
    require(by_candidate["CLOCK_CURVATURE_SHAPE"]["tau_readout_channel"] == "K_time", "curvature must map to K_time")
    require(by_candidate["BAO_LEVEL_CONTEXT"]["tau_readout_channel"] == "K_closure", "BAO context must map to K_closure")
    require(by_candidate["ORDERING_NULL_CONTROL"]["tau_readout_channel"] == "K_null", "ordering control must map to K_null")
    require({row["projection_induction_complete"] for row in rows} == {"false"}, "projection induction must remain incomplete")

    require(summary["status"] == "DESI_TIME_READOUT_SHAPE_PROJECTION_INDUCTION_MAPPED_NOT_REPLAY_NOT_VALIDATION", "bad summary status")
    require(summary["primary_candidate"] == "CLOCK_SLOPE_SHAPE", "clock slope must be primary")
    require(summary["projection_induction_complete"] == "false", "summary must not complete projection induction")
    require(summary["quotient_survival_gate_status"] == "not_proven_ordering_null_unresolved", "quotient survival blocker should remain explicit")
    require(summary["verdict"] == "time_shape_maps_to_K_time_candidate_but_projection_induction_incomplete", "bad verdict")
    print("paper10_desi_time_readout_shape_projection_induction_v1: OK")


if __name__ == "__main__":
    main()

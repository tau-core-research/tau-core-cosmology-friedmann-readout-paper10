#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_cc_window_stress_binding_policy_v1.csv"
OUT = ROOT / "data/derived/paper10_desi_cc_window_stress_binding_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_cc_window_stress_binding_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_cc_window_stress_binding_not_validation"


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
    require(len(rows) == 3, "CC-window stress binding must contain three components")
    for row in rows + [policy, summary]:
        require(row["endpoint_replay_allowed"] == "false", "must not authorize replay")
        require(row["endpoint_validation_claimed"] == "false", "must not claim endpoint validation")
        require(row["physical_validation_claimed"] == "false", "must not claim physical validation")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "bad row claim boundary")
    components = {row["stress_component"] for row in rows}
    require(components == {"strict_window_simon_bracket", "non_simon_strict_window_search", "caveated_near_window_context"}, "unexpected stress components")
    require(summary["cc_window_stress_bound_to_shape_route"] == "true", "CC-window stress should be bound")
    require(summary["row_can_enter_replay"] == "false", "row must not enter replay")
    require(summary["shape_route_replay_ready_after_cc_window_stress"] == "false", "shape route must remain non-replay-ready")
    require(summary["cc_window_stress_release_policy"] == "SOURCE_REOPEN_ONLY_NO_REPLAY", "bad release policy")
    require(summary["verdict"] == "cc_window_stress_bound_as_caveated_source_control_not_replay_release", "bad verdict")
    print("paper10_desi_cc_window_stress_binding_v1: OK")


if __name__ == "__main__":
    main()

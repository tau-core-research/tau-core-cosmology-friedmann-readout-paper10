#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_time_level_negative_control_response_gate_v1.csv"
OUTPUT = ROOT / "data/derived/paper10_desi_time_level_negative_control_response_gate_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_time_level_negative_control_response_gate_v1_summary.csv"


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


def main() -> None:
    policy = one_row(POLICY)
    output = one_row(OUTPUT)
    summary = one_row(SUMMARY)
    if policy["endpoint_replay_allowed"] != "false":
        raise SystemExit("policy must keep endpoint replay disabled")
    if output["route_reopened_for_replay"] != "false":
        raise SystemExit("response gate must not reopen replay")
    for row in (output, summary):
        if row["endpoint_replay_allowed"] != "false":
            raise SystemExit("response gate artifacts must keep replay disabled")
        if row["endpoint_validation_claimed"] != "false" or row["physical_validation_claimed"] != "false":
            raise SystemExit("response gate artifacts must not claim validation")
    if output["negative_failure_mode"] != "five_row_time_level_constant_beta_endpoint_is_ordering_fragile":
        raise SystemExit("negative failure mode was not preserved")
    if int(output["controls_better_than_candidate_chi2"]) < 1:
        raise SystemExit("control dominance was not preserved")
    if int(summary["exit_condition_count"]) < 5:
        raise SystemExit("response gate must freeze multiple exit conditions")
    if summary["next_allowed_action"] != "build_source_side_time_readout_expansion_manifest_only":
        raise SystemExit("unexpected next allowed action")
    if summary["verdict"] != "desi_time_level_negative_control_response_gate_blocks_replay_until_richer_clock_readout_support":
        raise SystemExit("bad response gate verdict")
    print("paper10_desi_time_level_negative_control_response_gate_v1: OK")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_time_level_negative_control_response_gate_v1.csv"
NEGATIVE_DIAGNOSTIC = ROOT / "data/derived/paper10_desi_time_level_negative_control_diagnostic_v1_summary.csv"
OUTPUT = ROOT / "data/derived/paper10_desi_time_level_negative_control_response_gate_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_time_level_negative_control_response_gate_v1_summary.csv"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required input: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def one_row(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path.relative_to(ROOT)}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    policy = one_row(POLICY)
    diagnostic = one_row(NEGATIVE_DIAGNOSTIC)
    if diagnostic["verdict"] != "desi_time_level_negative_control_diagnostic_explains_non_control_resistance_not_validation":
        raise SystemExit("negative-control response gate requires the preserved DESI negative diagnostic")
    if diagnostic["failure_mode"] != "five_row_time_level_constant_beta_endpoint_is_ordering_fragile":
        raise SystemExit("unexpected DESI time-level failure mode")
    if int(diagnostic["controls_better_than_candidate_chi2"]) < 1:
        raise SystemExit("response gate requires a control-dominance negative result")
    if policy["endpoint_replay_allowed"] != "false":
        raise SystemExit("response gate must not authorize endpoint replay")

    exit_conditions = [item for item in policy["required_exit_conditions"].split(";") if item]
    forbidden_inputs = [item for item in policy["forbidden_inputs"].split(";") if item]
    ledger = [
        {
            "gate_id": policy["gate_id"],
            "gate_status": policy["status"],
            "negative_diagnostic_status": diagnostic["status"],
            "negative_failure_mode": diagnostic["failure_mode"],
            "controls_better_than_candidate_chi2": diagnostic["controls_better_than_candidate_chi2"],
            "candidate_chi2_per_dof": diagnostic["candidate_chi2_per_dof"],
            "best_control_chi2_per_dof": diagnostic["redshift_shuffle_chi2_per_dof"],
            "exit_condition_count": str(len(exit_conditions)),
            "forbidden_input_count": str(len(forbidden_inputs)),
            "next_allowed_action": policy["next_allowed_action"],
            "route_reopened_for_replay": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": policy["claim_boundary"],
            "verdict": "desi_time_level_route_closed_as_negative_control_pending_source_side_expansion_not_validation",
        }
    ]
    write_csv(OUTPUT, ledger)
    write_csv(
        SUMMARY,
        [
            {
                "gate_id": policy["gate_id"],
                "status": "DESI_TIME_LEVEL_NEGATIVE_CONTROL_RESPONSE_GATE_BUILT_NOT_VALIDATION",
                "route_status": policy["status"],
                "input_negative_failure_mode": diagnostic["failure_mode"],
                "exit_condition_count": str(len(exit_conditions)),
                "forbidden_input_count": str(len(forbidden_inputs)),
                "next_allowed_action": policy["next_allowed_action"],
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "claim_boundary": policy["claim_boundary"],
                "verdict": "desi_time_level_negative_control_response_gate_blocks_replay_until_richer_clock_readout_support",
            }
        ],
    )


if __name__ == "__main__":
    main()

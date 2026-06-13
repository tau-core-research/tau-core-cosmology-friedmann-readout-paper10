#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_row5_high_z_source_route_scout_policy_v1.csv"
OUT = ROOT / "data/derived/paper10_desi_row5_high_z_source_route_scout_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_row5_high_z_source_route_scout_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_row5_high_z_source_route_scout_not_validation"


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
    if policy["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("bad scout claim boundary")
    for field in ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"]:
        if policy[field] != "false":
            raise SystemExit(f"policy {field} must remain false")

    rows = [
        {
            "scout_id": policy["scout_id"],
            "target_id": policy["target_id"],
            "candidate_id": "LOUBSER_2025_DESI_DR1_COSMIC_CHRONOMETERS",
            "candidate_type": "desi_dr1_cosmic_chronometer_Hz_measurements",
            "candidate_z_or_range": "z=0.46;0.67;0.83;sample 0.3<z<1.0",
            "candidate_value_summary": "H(z)=88.48,119.45,108.28 km_s^-1_Mpc^-1 at z=0.46,0.67,0.83 with stat+syst errors",
            "source_reference": "Loubser 2025 MNRAS 544 3064; arXiv:2511.02730",
            "source_url": "https://arxiv.org/abs/2511.02730",
            "route_role": "supports_DESI_CC_source_family_but_not_row5_high_z",
            "gate_result": "RETAIN_AS_LOW_Z_DESI_CC_CONTEXT_ONLY_NOT_ROW5_SUPPORT",
            "gate_reason": "direct independent DESI cosmic-chronometer measurements exist, but they are far below z=2.33 and cannot bracket row5 without extrapolation",
            "accepted_for_row5": "false",
            "control_or_context_only": "true",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "scout_id": policy["scout_id"],
            "target_id": policy["target_id"],
            "candidate_id": "MORESCO_2024_COSMIC_CHRONOMETER_REVIEW",
            "candidate_type": "review_forecast_method_context",
            "candidate_z_or_range": "current constraints discussed to z~2; future surveys may improve",
            "candidate_value_summary": "method review; not a new source-native z=2.33 H(z) value",
            "source_reference": "Moresco 2024 cosmic-chronometer review; arXiv:2412.01994",
            "source_url": "https://arxiv.org/abs/2412.01994",
            "route_role": "method_context_and_future_high_z_forecast",
            "gate_result": "RETAIN_AS_METHOD_CONTEXT_ONLY_NOT_NUMERIC_ROW5_SOURCE",
            "gate_reason": "useful for explaining why high-z chronometers are difficult and future-facing, but does not freeze a z=2.33 clock value",
            "accepted_for_row5": "false",
            "control_or_context_only": "true",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "scout_id": policy["scout_id"],
            "target_id": policy["target_id"],
            "candidate_id": "DESI_DR2_LYA_BAO_Z2P33",
            "candidate_type": "high_z_Ly_alpha_BAO_cross_probe",
            "candidate_z_or_range": "z_eff=2.33",
            "candidate_value_summary": "high-redshift BAO scale above z=2 from Ly-alpha forest; not an independent clock",
            "source_reference": "DESI DR2 Ly-alpha BAO; DESI collaboration",
            "source_url": "https://www.desi.lbl.gov/2025/03/19/desi-dr2-results-march-19-guide/",
            "route_role": "row5_cross_probe_context",
            "gate_result": "RETAIN_AS_CROSS_PROBE_CONTEXT_ONLY_NOT_CLOCK_SUPPORT",
            "gate_reason": "matches the row5 redshift but measures BAO/r_d rather than a clock or source-native time/readout observable",
            "accepted_for_row5": "false",
            "control_or_context_only": "true",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "scout_id": policy["scout_id"],
            "target_id": policy["target_id"],
            "candidate_id": "COSMOLOGICAL_STANDARD_TIMERS_FRAMEWORK",
            "candidate_type": "future_source_native_time_route_framework",
            "candidate_z_or_range": "not row-specific in current artifact",
            "candidate_value_summary": "framework for time-redshift observables; no frozen z=2.33 source-native value",
            "source_reference": "Cosmological Standard Timers framework literature",
            "source_url": "source_route_to_be_reviewed_before_use",
            "route_role": "future_route_prompt_only",
            "gate_result": "RETAIN_AS_FUTURE_ROUTE_PROMPT_ONLY_NOT_SOURCE",
            "gate_reason": "could motivate a non-CC time/readout route, but Paper10 still needs a public source-native observable and a separate reviewer gate before replay",
            "accepted_for_row5": "false",
            "control_or_context_only": "true",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(OUT, rows)
    summary = {
        "scout_id": policy["scout_id"],
        "status": "DESI_ROW5_HIGH_Z_SOURCE_ROUTE_SCOUT_BUILT_NOT_REPLAY_NOT_VALIDATION",
        "candidate_count": str(len(rows)),
        "accepted_for_row5_count": str(sum(row["accepted_for_row5"] == "true" for row in rows)),
        "context_only_count": str(sum(row["control_or_context_only"] == "true" for row in rows)),
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
        "verdict": "row5_high_z_scout_found_context_but_no_gate_closing_source",
        "recommended_next_action": "do_not_replay; either keep_row5_holdout_or_prepare_new_source_native_time_readout_handoff",
    }
    write_csv(SUMMARY, [summary])
    print(
        "PAPER10_DESI_ROW5_HIGH_Z_SOURCE_ROUTE_SCOUT_BUILT "
        f"accepted_for_row5_count={summary['accepted_for_row5_count']}"
    )


if __name__ == "__main__":
    main()

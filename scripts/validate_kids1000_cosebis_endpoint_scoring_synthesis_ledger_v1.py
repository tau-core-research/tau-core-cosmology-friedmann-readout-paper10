#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_endpoint_scoring_synthesis_ledger_policy_v1.csv"
LEDGER = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_scoring_synthesis_ledger_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_endpoint_scoring_synthesis_ledger_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    policy = read_one(POLICY)
    rows = read_rows(LEDGER)
    summary = read_one(SUMMARY)

    if policy["status"] != "ENDPOINT_SCORING_SYNTHESIS_LEDGER_POLICY_FROZEN":
        raise SystemExit("unexpected synthesis policy status")
    if policy["computes_new_scores"] != "false":
        raise SystemExit("synthesis policy must not compute new scores")
    if policy["endpoint_validation_claimed"] != "false":
        raise SystemExit("synthesis policy must not claim endpoint validation")
    if summary["status"] != "ENDPOINT_SCORING_SYNTHESIS_LEDGER_BUILT":
        raise SystemExit("unexpected synthesis summary status")
    if summary["ledger_rows"] != "8" or len(rows) != 8:
        raise SystemExit("synthesis ledger must contain eight rows")
    if summary["diagnostic_endpoint_signal_present"] != "true":
        raise SystemExit("diagnostic endpoint signal should be recorded")
    if summary["candidate_absolute_winner"] != "false":
        raise SystemExit("candidate must not be recorded as absolute winner")
    if summary["tomographic_caveat_active"] != "true":
        raise SystemExit("tomographic caveat must remain active")
    if summary["better_tomographic_controls_accepted_as_physical_alternatives"] != "false":
        raise SystemExit("better tomographic controls must not be accepted as physical alternatives")
    if summary["physical_promotion_ready"] != "false":
        raise SystemExit("physical promotion must remain blocked")
    if summary["computes_new_scores"] != "false":
        raise SystemExit("synthesis summary must not compute new scores")
    if summary["endpoint_validation_claimed"] != "false":
        raise SystemExit("synthesis summary must not claim endpoint validation")
    if summary["physical_validation_claimed"] != "false":
        raise SystemExit("synthesis summary must not claim physical validation")
    if summary["verdict"] != "endpoint_signal_low_tail_caveated_by_tomographic_controls_and_physical_promotion_blockers":
        raise SystemExit("unexpected synthesis verdict")

    by_component = {row["component_id"]: row for row in rows}
    expected = {
        "S0_endpoint_score",
        "S1_null_control_diagnostics",
        "S2_tomographic_structure_robustness",
        "S2b_tomographic_control_plausibility",
        "S3_jackknife_localization",
        "S4_mode_localization",
        "S5_mode_shape_stress",
        "S6_physical_promotion",
    }
    if set(by_component) != expected:
        raise SystemExit("unexpected synthesis component set")
    if by_component["S0_endpoint_score"]["component_status"] != "DIAGNOSTIC_ENDPOINT_SIGNAL_PRESENT":
        raise SystemExit("endpoint score row status mismatch")
    if by_component["S2_tomographic_structure_robustness"]["component_status"] != "TOMOGRAPHIC_CAVEAT_ACTIVE":
        raise SystemExit("tomographic row status mismatch")
    if (
        by_component["S2b_tomographic_control_plausibility"]["component_status"]
        != "BETTER_CONTROLS_NOT_ACCEPTED_AS_PHYSICAL_ALTERNATIVES"
    ):
        raise SystemExit("tomographic plausibility row status mismatch")
    if by_component["S6_physical_promotion"]["component_status"] != "PHYSICAL_PROMOTION_BLOCKED":
        raise SystemExit("physical promotion row status mismatch")
    if by_component["S6_physical_promotion"]["supports_endpoint_signal"] != "false":
        raise SystemExit("physical blocker must not support endpoint signal")

    for row in rows:
        if row["claim_boundary"] != policy["claim_boundary"]:
            raise SystemExit("claim boundary mismatch")
    if summary["claim_boundary"] != policy["claim_boundary"]:
        raise SystemExit("summary claim boundary mismatch")

    print(
        "PAPER10_KIDS1000_COSEBIS_ENDPOINT_SCORING_SYNTHESIS_LEDGER_V1_VALIDATED "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()

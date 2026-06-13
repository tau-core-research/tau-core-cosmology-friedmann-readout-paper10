#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_row4_cc_bracket_source_freeze_policy_v1.csv"
PARENT = ROOT / "data/derived/paper10_desi_row4_clock_reopen_manifest_v1_summary.csv"
OUT = ROOT / "data/derived/paper10_desi_row4_cc_bracket_source_freeze_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_row4_cc_bracket_source_freeze_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_row4_cc_bracket_source_freeze_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required input: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    policy = read_one(POLICY)
    parent = read_one(PARENT)
    if policy["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("policy claim boundary mismatch")
    if parent["status"] != "ROW4_SOURCE_ACQUISITION_REOPENED_NOT_REPLAY_ROW5_BLOCKED":
        raise SystemExit("row4 acquisition must be reopened before freezing bracket source values")
    if parent["row4_can_enter_replay"] != "false":
        raise SystemExit("parent manifest must not authorize replay")
    if parent["row5_remains_blocked"] != "true":
        raise SystemExit("row5 must remain blocked")

    rows = [
        {
            "freeze_id": "PAPER10_DESI_ROW4_CC_BRACKET_SOURCE_FREEZE_V1",
            "entry_id": "SIMON_2005_CC_Z1P43",
            "row_id": "4",
            "target_z_eff": "1.484",
            "z": "1.43",
            "H_z_km_s_Mpc": "177",
            "sigma_H_km_s_Mpc": "18",
            "method": "full_spectrum_fitting",
            "source_reference": "Simon_Verde_Jimenez_2005",
            "source_reference_family": "Simon_2005",
            "compiled_in": "Moresco_2023_cosmic_chronometer_review_table",
            "within_frozen_window_abs_z_minus_target_le_0p10": "true",
            "independent_of_current_blocker_reference_family": "false",
            "source_values_frozen": "true",
            "row_can_enter_replay": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "freeze_id": "PAPER10_DESI_ROW4_CC_BRACKET_SOURCE_FREEZE_V1",
            "entry_id": "SIMON_2005_CC_Z1P53",
            "row_id": "4",
            "target_z_eff": "1.484",
            "z": "1.53",
            "H_z_km_s_Mpc": "140",
            "sigma_H_km_s_Mpc": "14",
            "method": "full_spectrum_fitting",
            "source_reference": "Simon_Verde_Jimenez_2005",
            "source_reference_family": "Simon_2005",
            "compiled_in": "Moresco_2023_cosmic_chronometer_review_table",
            "within_frozen_window_abs_z_minus_target_le_0p10": "true",
            "independent_of_current_blocker_reference_family": "false",
            "source_values_frozen": "true",
            "row_can_enter_replay": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(OUT, rows)
    write_csv(
        SUMMARY,
        [
            {
                "freeze_id": "PAPER10_DESI_ROW4_CC_BRACKET_SOURCE_FREEZE_V1",
                "status": "ROW4_CC_BRACKET_SOURCE_VALUES_FROZEN_REFERENCE_FAMILY_NOT_INDEPENDENT_NOT_REPLAY",
                "row_id": "4",
                "target_z_eff": "1.484",
                "frozen_entry_count": str(len(rows)),
                "source_values_frozen": "true",
                "all_entries_inside_frozen_window": "true",
                "all_entries_same_reference_family": "true",
                "reference_family": "Simon_2005",
                "independent_reference_family_redundancy_satisfied": "false",
                "row4_source_acquisition_improved": "true",
                "row4_can_enter_replay": "false",
                "row5_remains_blocked": "true",
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "verdict": "row4_bracket_values_frozen_but_independence_blocker_remains",
                "recommended_next_action": "find_non_simon_independent_CC_or_time_readout_support_near_z_1p484_or_keep_row4_blocked",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    print("paper10_desi_row4_cc_bracket_source_freeze_v1: built")


if __name__ == "__main__":
    main()

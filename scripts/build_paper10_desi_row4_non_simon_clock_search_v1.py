#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_row4_non_simon_clock_search_policy_v1.csv"
PARENT_FREEZE = ROOT / "data/derived/paper10_desi_row4_cc_bracket_source_freeze_v1_summary.csv"
OUT = ROOT / "data/derived/paper10_desi_row4_non_simon_clock_search_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_row4_non_simon_clock_search_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_row4_non_simon_clock_search_not_validation"


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
        raise SystemExit("bad non-Simon search claim boundary")
    for field in ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"]:
        if policy[field] != "false":
            raise SystemExit(f"policy {field} must remain false")
    parent = one_row(PARENT_FREEZE)
    if parent["status"] != "ROW4_CC_BRACKET_SOURCE_VALUES_FROZEN_REFERENCE_FAMILY_NOT_INDEPENDENT_NOT_REPLAY":
        raise SystemExit("row4 non-Simon search expects the Simon bracket freeze parent")
    if parent["row4_can_enter_replay"] != "false":
        raise SystemExit("row4 must remain outside replay before this search")

    target_z = float(policy["strict_target_z"])
    strict_window = float(policy["strict_window_delta_z"])
    candidates = [
        {
            "candidate_id": "SIMON_2005_CC_Z1P43",
            "candidate_type": "cosmic_chronometer_Hz",
            "candidate_z": "1.43",
            "delta_z_from_row4": f"{abs(1.43 - target_z):.3f}",
            "H_z_km_s_Mpc": "177",
            "sigma_H_km_s_Mpc": "18",
            "source_reference": "Simon, Verde, and Jimenez 2005",
            "source_reference_family": "Simon_2005",
            "source_url": "https://doi.org/10.1103/PhysRevD.71.123001",
            "inside_strict_window": "true",
            "independent_of_current_blocker_reference_family": "false",
            "gate_result": "REJECT_AS_SAME_REFERENCE_FAMILY",
            "gate_reason": "inside row4 window but reuses the Simon_2005 family already responsible for the blocker",
        },
        {
            "candidate_id": "SIMON_2005_CC_Z1P53",
            "candidate_type": "cosmic_chronometer_Hz",
            "candidate_z": "1.53",
            "delta_z_from_row4": f"{abs(1.53 - target_z):.3f}",
            "H_z_km_s_Mpc": "140",
            "sigma_H_km_s_Mpc": "14",
            "source_reference": "Simon, Verde, and Jimenez 2005",
            "source_reference_family": "Simon_2005",
            "source_url": "https://doi.org/10.1103/PhysRevD.71.123001",
            "inside_strict_window": "true",
            "independent_of_current_blocker_reference_family": "false",
            "gate_result": "REJECT_AS_SAME_REFERENCE_FAMILY",
            "gate_reason": "inside row4 window but reuses the Simon_2005 family already responsible for the blocker",
        },
        {
            "candidate_id": "MORESCO_2015_CC_Z1P363",
            "candidate_type": "cosmic_chronometer_Hz",
            "candidate_z": "1.363",
            "delta_z_from_row4": f"{abs(1.363 - target_z):.3f}",
            "H_z_km_s_Mpc": "160",
            "sigma_H_km_s_Mpc": "33.6",
            "source_reference": "Moresco 2015",
            "source_reference_family": "Moresco_2015",
            "source_url": "https://doi.org/10.1093/mnrasl/slv037",
            "inside_strict_window": "false",
            "independent_of_current_blocker_reference_family": "true",
            "gate_result": "REJECT_FOR_ROW4_OUTSIDE_STRICT_WINDOW",
            "gate_reason": "non-Simon independent chronometer source but |1.363-1.484|=0.121 exceeds the frozen 0.10 row4 window",
        },
        {
            "candidate_id": "TOMASETTI_2023_VANDELS_CC_Z1P26",
            "candidate_type": "cosmic_chronometer_Hz",
            "candidate_z": "1.26",
            "delta_z_from_row4": f"{abs(1.26 - target_z):.3f}",
            "H_z_km_s_Mpc": "135",
            "sigma_H_km_s_Mpc": "65",
            "source_reference": "Tomasetti et al. 2023",
            "source_reference_family": "Tomasetti_2023",
            "source_url": "https://doi.org/10.1051/0004-6361/202346992",
            "inside_strict_window": "false",
            "independent_of_current_blocker_reference_family": "true",
            "gate_result": "REJECT_FOR_ROW4_OUTSIDE_STRICT_WINDOW",
            "gate_reason": "non-Simon independent chronometer source but |1.26-1.484|=0.224 exceeds the frozen 0.10 row4 window",
        },
    ]
    rows = []
    for candidate in candidates:
        inside = abs(float(candidate["candidate_z"]) - target_z) <= strict_window
        if candidate["inside_strict_window"] != ("true" if inside else "false"):
            raise SystemExit(f"bad strict-window flag for {candidate['candidate_id']}")
        accepted = inside and candidate["independent_of_current_blocker_reference_family"] == "true"
        rows.append(
            {
                "search_id": policy["search_id"],
                **candidate,
                "accepted_for_row4_release": "true" if accepted else "false",
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(OUT, rows)
    accepted_count = sum(row["accepted_for_row4_release"] == "true" for row in rows)
    non_simon_inside = sum(
        row["inside_strict_window"] == "true"
        and row["independent_of_current_blocker_reference_family"] == "true"
        for row in rows
    )
    summary = [
        {
            "search_id": policy["search_id"],
            "status": "ROW4_NON_SIMON_STRICT_WINDOW_SEARCH_NEGATIVE_NOT_REPLAY",
            "candidate_count": str(len(rows)),
            "strict_target_z": policy["strict_target_z"],
            "strict_window_delta_z": policy["strict_window_delta_z"],
            "non_simon_inside_strict_window_count": str(non_simon_inside),
            "accepted_for_row4_release_count": str(accepted_count),
            "closest_non_simon_candidate": "MORESCO_2015_CC_Z1P363",
            "closest_non_simon_delta_z": "0.121",
            "row4_independent_reference_family_redundancy_satisfied": "false",
            "row4_can_enter_replay": "false",
            "row5_remains_blocked": "true",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
            "verdict": "row4_non_simon_strict_window_search_negative_blocker_remains",
            "recommended_next_action": "find_non_simon_clock_or_source_native_time_readout_inside_row4_window_or_request_external_review_for_window_change",
        }
    ]
    write_csv(SUMMARY, summary)


if __name__ == "__main__":
    main()

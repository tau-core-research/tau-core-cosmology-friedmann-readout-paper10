#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_cc_window_stress_binding_policy_v1.csv"
BRACKET_SUMMARY = ROOT / "data/derived/paper10_desi_row4_cc_bracket_source_freeze_v1_summary.csv"
BRACKET_ROWS = ROOT / "data/derived/paper10_desi_row4_cc_bracket_source_freeze_v1.csv"
NON_SIMON_SUMMARY = ROOT / "data/derived/paper10_desi_row4_non_simon_clock_search_v1_summary.csv"
NON_SIMON_ROWS = ROOT / "data/derived/paper10_desi_row4_non_simon_clock_search_v1.csv"
WINDOW_DECISION = ROOT / "data/derived/paper10_desi_row4_window_decision_gate_v1_summary.csv"
OUT = ROOT / "data/derived/paper10_desi_cc_window_stress_binding_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_cc_window_stress_binding_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_cc_window_stress_binding_not_validation"


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
        raise SystemExit("bad CC-window stress policy claim boundary")
    for field in ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"]:
        if policy[field] != "false":
            raise SystemExit(f"policy {field} must remain false")

    bracket = one_row(BRACKET_SUMMARY)
    non_simon = one_row(NON_SIMON_SUMMARY)
    decision = one_row(WINDOW_DECISION)
    bracket_rows = read_rows(BRACKET_ROWS)
    non_simon_rows = read_rows(NON_SIMON_ROWS)

    if bracket["row4_can_enter_replay"] != "false":
        raise SystemExit("bracket source freeze must not release row4")
    if non_simon["row4_can_enter_replay"] != "false":
        raise SystemExit("non-Simon search must not release row4")
    if decision["row4_can_enter_replay"] != "false":
        raise SystemExit("window decision must not release row4")
    if decision["source_reopen_caveated"] != "true":
        raise SystemExit("CC-window stress binding expects caveated source reopen")

    simon_entries = [row for row in bracket_rows if row["source_reference_family"] == "Simon_2005"]
    moresco_candidates = [row for row in non_simon_rows if row["candidate_id"] == "MORESCO_2015_CC_Z1P363"]
    if len(simon_entries) != 2 or len(moresco_candidates) != 1:
        raise SystemExit("expected two Simon bracket entries and one Moresco caveated candidate")

    moresco = moresco_candidates[0]
    rows = [
        {
            "gate_id": policy["gate_id"],
            "stress_component": "strict_window_simon_bracket",
            "component_status": "bound_source_context_same_reference_family_caveat",
            "row_id": bracket["row_id"],
            "target_z_eff": bracket["target_z_eff"],
            "source_values": ";".join(f"{row['entry_id']}@z={row['z']}:H={row['H_z_km_s_Mpc']}+-{row['sigma_H_km_s_Mpc']}" for row in simon_entries),
            "source_policy": "inside_strict_window_but_same_reference_family_not_independent",
            "row_can_enter_replay": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": policy["gate_id"],
            "stress_component": "non_simon_strict_window_search",
            "component_status": "bound_negative_search",
            "row_id": bracket["row_id"],
            "target_z_eff": bracket["target_z_eff"],
            "source_values": f"non_simon_inside_strict_window_count={non_simon['non_simon_inside_strict_window_count']};closest={non_simon['closest_non_simon_candidate']};delta_z={non_simon['closest_non_simon_delta_z']}",
            "source_policy": "no_independent_non_simon_clock_inside_abs_delta_z_le_0p10",
            "row_can_enter_replay": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": policy["gate_id"],
            "stress_component": "caveated_near_window_context",
            "component_status": "bound_caveated_source_context_no_replay",
            "row_id": bracket["row_id"],
            "target_z_eff": bracket["target_z_eff"],
            "source_values": f"{moresco['candidate_id']}@z={moresco['candidate_z']}:H={moresco['H_z_km_s_Mpc']}+-{moresco['sigma_H_km_s_Mpc']};delta_z={moresco['delta_z_from_row4']}",
            "source_policy": f"{decision['strict_window_decision']};{decision['moresco_2015_eligibility']};{decision['release_policy']}",
            "row_can_enter_replay": "false",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(OUT, rows)

    summary = [
        {
            "gate_id": policy["gate_id"],
            "status": "DESI_CC_WINDOW_STRESS_BOUND_CAVEATED_NOT_REPLAY_NOT_VALIDATION",
            "row_id": bracket["row_id"],
            "target_z_eff": bracket["target_z_eff"],
            "stress_component_count": str(len(rows)),
            "strict_window_simon_bracket_bound": "true",
            "non_simon_strict_window_search_bound": "true",
            "caveated_near_window_context_bound": "true",
            "cc_window_stress_bound_to_shape_route": "true",
            "cc_window_stress_release_policy": "SOURCE_REOPEN_ONLY_NO_REPLAY",
            "row_can_enter_replay": "false",
            "shape_route_replay_ready_after_cc_window_stress": "false",
            "blocks_replay_reason": "cc_window_stress_is_bound_only_as_caveated_source_context_and_separate_replay_authorization_is_missing",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
            "verdict": "cc_window_stress_bound_as_caveated_source_control_not_replay_release",
        }
    ]
    write_csv(SUMMARY, summary)
    print(f"wrote {OUT.relative_to(ROOT)}")
    print(f"wrote {SUMMARY.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

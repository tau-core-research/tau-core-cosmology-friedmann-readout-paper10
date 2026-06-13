#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_row5_holdout_confirmation_policy_v1.csv"
HIGH_Z_POLICY = ROOT / "data/source_manifest/paper10_desi_dr2_high_z_bao_policy_v1.csv"
ROW5_DECISION = ROOT / "data/derived/paper10_desi_row5_high_z_decision_gate_v1_summary.csv"
ROW5_SCOUT = ROOT / "data/derived/paper10_desi_row5_high_z_source_route_scout_v1_summary.csv"
TEMPLATE = ROOT / "data/source_manifest/paper10_desi_time_level_endpoint_replay_run_template_v1.csv"
OUT = ROOT / "data/derived/paper10_desi_row5_holdout_confirmation_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_row5_holdout_confirmation_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_row5_holdout_confirmation_not_validation"


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
    high_z = one_row(HIGH_Z_POLICY)
    row5 = one_row(ROW5_DECISION)
    scout = one_row(ROW5_SCOUT)
    template = one_row(TEMPLATE)
    if policy["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("bad holdout claim boundary")
    for label, row in [
        ("policy", policy),
        ("row5", row5),
        ("scout", scout),
        ("template", template),
    ]:
        for field in ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"]:
            if row[field] != "false":
                raise SystemExit(f"{label} {field} must remain false")
    if high_z["accepted_policy"] != "exclude_from_first_CC_matched_time_endpoint_no_extrapolation":
        raise SystemExit("high-z policy must predeclare exclusion from first CC-matched endpoint")
    if row5["gate_status"] != "ROW5_HIGH_Z_BLOCKER_REMAINS_NOT_REPLAY":
        raise SystemExit("row5 decision must remain blocked before holdout confirmation")
    if scout["accepted_for_row5_count"] != "0":
        raise SystemExit("row5 scout cannot accept a gate-closing source")
    if template["radial_rows_allowed"] != "0;1;2;3;4" or template["radial_rows_excluded"] != "5":
        raise SystemExit("endpoint template must keep row 5 excluded")

    row = {
        "holdout_id": policy["holdout_id"],
        "status": "ROW5_HOLDOUT_CONFIRMED_NOT_REPLAY_NOT_VALIDATION",
        "heldout_radial_row": policy["heldout_radial_row"],
        "heldout_z": policy["heldout_z"],
        "row5_gate_status": row5["gate_status"],
        "row5_scout_verdict": scout["verdict"],
        "accepted_for_row5_count": scout["accepted_for_row5_count"],
        "allowed_radial_rows": template["radial_rows_allowed"],
        "excluded_radial_rows": template["radial_rows_excluded"],
        "holdout_reason": "no_independent_high_z_clock_or_source_native_time_readout_covering_z2p33",
        "post_review_consequence": "keep_row5_holdout_do_not_replay",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
        "verdict": "row5_holdout_confirmed_no_gate_closing_source_not_replay",
    }
    write_csv(OUT, [row])
    write_csv(
        SUMMARY,
        [
            {
                "holdout_id": policy["holdout_id"],
                **row,
                "recommended_next_action": "keep_row5_excluded_or_prepare_new_source_native_time_readout_handoff_before_any_inclusion",
            }
        ],
    )
    print("PAPER10_DESI_ROW5_HOLDOUT_CONFIRMED no_replay")


if __name__ == "__main__":
    main()

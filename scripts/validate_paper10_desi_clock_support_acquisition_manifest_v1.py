#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_clock_support_acquisition_manifest_policy_v1.csv"
ROWS = ROOT / "data/derived/paper10_desi_clock_support_acquisition_manifest_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_clock_support_acquisition_manifest_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_clock_support_acquisition_manifest_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def one_row(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def require_false(row: dict[str, str], fields: list[str], label: str) -> None:
    for field in fields:
        if row.get(field) != "false":
            raise SystemExit(f"{label} {field} must be false")


def main() -> None:
    policy = one_row(POLICY)
    summary = one_row(SUMMARY)
    rows = read_rows(ROWS)
    require_false(policy, ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"], "policy")
    require_false(summary, ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"], "summary")
    if policy["claim_boundary"] != CLAIM_BOUNDARY or summary["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("bad claim boundary")
    if summary["status"] != "DESI_CLOCK_SUPPORT_ACQUISITION_MANIFEST_FROZEN_NOT_FETCHED_NOT_REPLAY_NOT_VALIDATION":
        raise SystemExit("bad summary status")
    if summary["verdict"] != "desi_clock_support_acquisition_targets_frozen_sources_not_attached":
        raise SystemExit("bad summary verdict")
    if summary["source_fetch_completed"] != "false":
        raise SystemExit("source_fetch_completed must remain false")
    if summary["target_count"] != "2" or len(rows) != 2:
        raise SystemExit("acquisition manifest must contain exactly two targets")

    by_target = {row["target_id"]: row for row in rows}
    expected = {
        "DESI_RADIAL_ROW_4_MULTI_CLOCK_REDUNDANCY",
        "DESI_RADIAL_ROW_5_HIGH_Z_CLOCK_SUPPORT",
    }
    if set(by_target) != expected:
        raise SystemExit("unexpected acquisition targets")
    for row in rows:
        require_false(row, ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"], row["target_id"])
        if row["claim_boundary"] != CLAIM_BOUNDARY:
            raise SystemExit(f"{row['target_id']} has bad claim boundary")
        if row["source_fetch_status"] != "not_fetched":
            raise SystemExit(f"{row['target_id']} must remain not_fetched")
        if row["hard_no_extrapolation_rule"] != "true":
            raise SystemExit(f"{row['target_id']} must keep hard_no_extrapolation_rule=true")

    row4 = by_target["DESI_RADIAL_ROW_4_MULTI_CLOCK_REDUNDANCY"]
    if row4["radial_index"] != "4" or row4["target_z_eff"] != "1.484":
        raise SystemExit("row-4 acquisition target changed")
    if row4["preferred_z_window"] != "abs(z-1.484)<=0.10":
        raise SystemExit("row-4 preferred z window changed")
    if "only_one_independent_reference" not in row4["current_blocker"]:
        raise SystemExit("row-4 blocker must record the independent-reference failure")

    row5 = by_target["DESI_RADIAL_ROW_5_HIGH_Z_CLOCK_SUPPORT"]
    if row5["radial_index"] != "5" or row5["target_z_eff"] != "2.33":
        raise SystemExit("row-5 acquisition target changed")
    if row5["preferred_z_window"] != "cover_or_bracket_z_2.33_without_extrapolation":
        raise SystemExit("row-5 preferred support rule changed")
    if "not_bracketed_without_extrapolation" not in row5["current_blocker"]:
        raise SystemExit("row-5 blocker must record no-extrapolation failure")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_row4_non_simon_clock_search_policy_v1.csv"
ROWS = ROOT / "data/derived/paper10_desi_row4_non_simon_clock_search_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_row4_non_simon_clock_search_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_row4_non_simon_clock_search_not_validation"


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
    if summary["status"] != "ROW4_NON_SIMON_STRICT_WINDOW_SEARCH_NEGATIVE_NOT_REPLAY":
        raise SystemExit("bad summary status")
    if summary["candidate_count"] != "4" or len(rows) != 4:
        raise SystemExit("row4 non-Simon search must contain exactly four rows")
    if summary["non_simon_inside_strict_window_count"] != "0":
        raise SystemExit("no non-Simon candidate may be inside the strict row4 window")
    if summary["accepted_for_row4_release_count"] != "0":
        raise SystemExit("row4 release count must remain zero")
    if summary["row4_independent_reference_family_redundancy_satisfied"] != "false":
        raise SystemExit("row4 redundancy must remain unsatisfied")
    if summary["row4_can_enter_replay"] != "false":
        raise SystemExit("row4 must not enter replay")
    if summary["verdict"] != "row4_non_simon_strict_window_search_negative_blocker_remains":
        raise SystemExit("bad summary verdict")
    for row in rows:
        require_false(row, ["accepted_for_row4_release", "endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"], row["candidate_id"])
        if row["claim_boundary"] != CLAIM_BOUNDARY:
            raise SystemExit(f"{row['candidate_id']} has bad claim boundary")
    by_candidate = {row["candidate_id"]: row for row in rows}
    if by_candidate["MORESCO_2015_CC_Z1P363"]["inside_strict_window"] != "false":
        raise SystemExit("Moresco 2015 z=1.363 must remain outside the strict row4 window")
    if by_candidate["MORESCO_2015_CC_Z1P363"]["independent_of_current_blocker_reference_family"] != "true":
        raise SystemExit("Moresco 2015 must remain the nearest non-Simon independent source")
    if by_candidate["SIMON_2005_CC_Z1P43"]["gate_result"] != "REJECT_AS_SAME_REFERENCE_FAMILY":
        raise SystemExit("Simon z=1.43 must remain rejected as same reference family")
    print("PAPER10_DESI_ROW4_NON_SIMON_CLOCK_SEARCH_VALIDATED row4_can_enter_replay=false")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_row4_clock_reopen_manifest_policy_v1.csv"
REVIEW_SUMMARY = ROOT / "data/derived/paper10_desi_clock_support_blocker_external_review_response_v1_summary.csv"
OUT = ROOT / "data/derived/paper10_desi_row4_clock_reopen_manifest_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_row4_clock_reopen_manifest_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_row4_clock_reopen_manifest_not_validation"


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
    review = read_one(REVIEW_SUMMARY)
    if policy["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("policy claim boundary mismatch")
    if review["decision"] != "PARTIAL_SOURCE_ACQUISITION_REOPEN_ROW4_KEEP_ROW5_BLOCKED_NO_REPLAY":
        raise SystemExit("external review must partially reopen row 4 only")
    if review["row4_source_acquisition_gate_can_reopen"] != "true":
        raise SystemExit("row 4 must be reopened by external review")
    if review["row5_remains_blocked"] != "true":
        raise SystemExit("row 5 must remain blocked")
    if review["endpoint_replay_allowed"] != "false":
        raise SystemExit("external review must not authorize replay")

    rows = [
        {
            "manifest_id": "PAPER10_DESI_ROW4_CLOCK_REOPEN_MANIFEST_V1",
            "target_id": "DESI_RADIAL_ROW_4_CLOCK_BRACKET_Z1P484",
            "row_id": "4",
            "target_z_eff": "1.484",
            "source_candidate_id": "MORESCO_CC_REVIEW_BRACKET_Z1P43_Z1P53",
            "required_bracket_z_low": "1.43",
            "required_bracket_z_high": "1.53",
            "source_action_status": "source_acquisition_reopened_not_cached",
            "source_values_frozen": "false",
            "row_can_enter_replay": "false",
            "row5_remains_blocked": "true",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_action": "cache_source_native_CC_values_uncertainties_reference_and_covariance_status_for_z_1p43_and_z_1p53",
        }
    ]
    write_csv(OUT, rows)
    write_csv(
        SUMMARY,
        [
            {
                "manifest_id": "PAPER10_DESI_ROW4_CLOCK_REOPEN_MANIFEST_V1",
                "status": "ROW4_SOURCE_ACQUISITION_REOPENED_NOT_REPLAY_ROW5_BLOCKED",
                "target_count": "1",
                "row4_source_acquisition_gate_can_reopen": "true",
                "row4_source_values_frozen": "false",
                "row4_can_enter_replay": "false",
                "row5_remains_blocked": "true",
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "verdict": "row4_clock_source_acquisition_reopened_but_source_values_not_frozen",
                "recommended_next_action": "cache_source_native_CC_bracket_entries_before_replay_authorization",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    print("paper10_desi_row4_clock_reopen_manifest_v1: built")


if __name__ == "__main__":
    main()

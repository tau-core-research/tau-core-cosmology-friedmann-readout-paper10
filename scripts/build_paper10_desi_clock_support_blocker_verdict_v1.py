#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_clock_support_blocker_verdict_policy_v1.csv"
ACQUISITION = ROOT / "data/derived/paper10_desi_clock_support_acquisition_manifest_v1.csv"
CANDIDATE_SCAN = ROOT / "data/derived/paper10_desi_clock_support_source_candidate_scan_v1_summary.csv"
OUT = ROOT / "data/derived/paper10_desi_clock_support_blocker_verdict_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_clock_support_blocker_verdict_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_clock_support_blocker_verdict_not_validation"


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
    acquisition_rows = read_rows(ACQUISITION)
    scan = one_row(CANDIDATE_SCAN)
    if policy["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("bad blocker verdict claim boundary")
    for field in ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"]:
        if policy[field] != "false":
            raise SystemExit(f"policy {field} must remain false")
    if len(acquisition_rows) != 2:
        raise SystemExit("blocker verdict expects exactly two acquisition targets")
    if scan["accepted_for_acquisition_target_count"] != "0":
        raise SystemExit("blocker verdict expects candidate scan to close zero acquisition targets")
    if scan["endpoint_replay_allowed"] != "false":
        raise SystemExit("candidate scan must not authorize replay")

    rows = [
        {
            "verdict_id": policy["verdict_id"],
            "blocker_id": "ROW4_INDEPENDENT_CLOCK_REDUNDANCY_MISSING",
            "target_id": "DESI_RADIAL_ROW_4_MULTI_CLOCK_REDUNDANCY",
            "blocker_status": "ACTIVE_BLOCKER",
            "blocker_reason": "row4_has_only_simon_2005_clock_support_in_relaxed_window;nearby_qso_bao_rsd_is_cross_probe_not_clock",
            "required_release_condition": "freeze_independent_CC_or_clock_readout_near_z_1p484_not_reusing_current_reference_family",
            "allowed_next_action": "targeted_source_acquisition_or_external_source_review_only",
            "disallowed_next_action": "endpoint_replay;validation_claim;using_BAO_RSD_as_clock_support;posthoc_smoothing",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "verdict_id": policy["verdict_id"],
            "blocker_id": "ROW5_HIGH_Z_CLOCK_SUPPORT_MISSING",
            "target_id": "DESI_RADIAL_ROW_5_HIGH_Z_CLOCK_SUPPORT",
            "blocker_status": "ACTIVE_BLOCKER",
            "blocker_reason": "z_2p33_LyA_BAO_exists_but_is_BAO_rd_cross_probe_not_independent_clock;frozen_CC_table_ends_at_z_1p965",
            "required_release_condition": "freeze_independent_high_z_clock_or_source_native_time_readout_covering_or_bracketing_z_2p33_without_extrapolation",
            "allowed_next_action": "targeted_source_acquisition_or_external_source_review_only",
            "disallowed_next_action": "endpoint_replay;validation_claim;using_LyA_BAO_as_clock_support;CC_extrapolation",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(OUT, rows)
    summary = [
        {
            "verdict_id": policy["verdict_id"],
            "status": "DESI_CLOCK_SUPPORT_ROUTE_BLOCKED_AFTER_SOURCE_SCAN_NOT_REPLAY_NOT_VALIDATION",
            "active_blocker_count": str(len(rows)),
            "candidate_scan_accepted_count": scan["accepted_for_acquisition_target_count"],
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "physical_validation_claimed": "false",
            "claim_boundary": CLAIM_BOUNDARY,
            "verdict": "desi_clock_support_route_remains_blocked_pending_independent_clock_sources",
            "allowed_reopen_conditions": "row4_independent_clock_redundancy_or_row5_high_z_clock_time_readout_source_frozen_before_replay",
            "recommended_next_action": "prepare_external_source_acquisition_review_package_for_the_two_active_blockers",
        }
    ]
    write_csv(SUMMARY, summary)


if __name__ == "__main__":
    main()

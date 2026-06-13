#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_clock_support_source_candidate_scan_policy_v1.csv"
ROWS = ROOT / "data/derived/paper10_desi_clock_support_source_candidate_scan_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_clock_support_source_candidate_scan_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_clock_support_source_candidate_scan_not_validation"


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
    if summary["status"] != "DESI_CLOCK_SUPPORT_SOURCE_CANDIDATE_SCAN_BUILT_NOT_REPLAY_NOT_VALIDATION":
        raise SystemExit("bad summary status")
    if summary["candidate_count"] != "6" or len(rows) != 6:
        raise SystemExit("candidate scan must contain exactly six rows")
    if summary["accepted_for_acquisition_target_count"] != "0":
        raise SystemExit("candidate scan must not accept a gate-closing source")
    if summary["verdict"] != "desi_clock_support_candidate_scan_found_cross_probe_context_but_no_gate_closing_clock_support":
        raise SystemExit("bad summary verdict")
    for row in rows:
        require_false(row, ["accepted_for_acquisition_target", "endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"], row["candidate_id"])
        if row["claim_boundary"] != CLAIM_BOUNDARY:
            raise SystemExit(f"{row['candidate_id']} has bad claim boundary")
        if row["control_or_context_only"] != "true":
            raise SystemExit(f"{row['candidate_id']} must remain control/context only")
    by_candidate = {row["candidate_id"]: row for row in rows}
    if by_candidate["EBOSS_DR16_QSO_BAO_RSD_Z1P48"]["gate_result"] != "RETAIN_AS_ROW4_CROSS_PROBE_CONTROL_ONLY_NOT_CLOCK_SUPPORT":
        raise SystemExit("eBOSS QSO candidate must remain row4 cross-probe control only")
    if by_candidate["TOMASETTI_2023_VANDELS_CC_Z1P26"]["gate_result"] != "REJECT_FOR_ROW4_OUTSIDE_FROZEN_Z_WINDOW":
        raise SystemExit("Tomasetti candidate must remain outside row4 window")
    if by_candidate["EBOSS_DR16_LYA_BAO_Z2P33"]["gate_result"] != "RETAIN_AS_CROSS_PROBE_CONTROL_ONLY_NOT_CLOCK_SUPPORT":
        raise SystemExit("eBOSS Ly-alpha candidate must remain control-only")


if __name__ == "__main__":
    main()

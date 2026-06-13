#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_dr2_radial_bao_cc_match_policy_v1.csv"
OUT = ROOT / "data/derived/paper10_desi_dr2_radial_bao_cc_match_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_dr2_radial_bao_cc_match_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_dr2_radial_bao_cc_match_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    policy_rows = read_rows(POLICY)
    rows = read_rows(OUT)
    summary_rows = read_rows(SUMMARY)
    require(len(policy_rows) == 1, "policy must contain one row")
    require(len(summary_rows) == 1, "summary must contain one row")
    policy = policy_rows[0]
    summary = summary_rows[0]
    require(policy["claim_boundary"] == CLAIM_BOUNDARY, "bad policy claim boundary")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "bad summary claim boundary")
    require(summary["status"] == "DESI_DR2_RADIAL_BAO_CC_MATCH_LEDGER_FROZEN_NOT_REPLAY_NOT_VALIDATION", "bad status")
    require(summary["input_radial_rows"] == "6", "bad input row count")
    require(summary["matched_within_cc_range_rows"] == "5", "bad matched row count")
    require(summary["blocked_outside_cc_range_rows"] == "1", "bad blocked row count")
    require(summary["unique_matched_cc_rows"] == "5", "bad unique CC row count")
    require(summary["blocked_radial_indices"] == "5", "unexpected blocked radial row")
    require(summary["blocked_z_eff"] == "2.33", "unexpected blocked z")
    require(summary["cc_extrapolation_used"] == "false", "CC extrapolation must remain false")
    require(summary["control_seed_manifest_required_before_replay"] == "true", "control seed guard missing")
    require(summary["verdict"] == "desi_bao_cc_support_partially_matched_high_z_row_blocked_no_replay", "bad verdict")
    require(len(rows) == 6, "match ledger must contain six rows")
    require(len([row for row in rows if row["cc_support_status"] == "MATCHED_WITHIN_CC_RANGE"]) == 5, "matched row mismatch")
    require(len([row for row in rows if row["cc_support_status"] == "BLOCKED_OUTSIDE_CC_RANGE_NO_EXTRAPOLATION"]) == 1, "blocked row mismatch")
    for field in ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"]:
        require(policy[field] == "false", f"policy {field} must remain false")
        require(summary[field] == "false", f"summary {field} must remain false")
        require({row[field] for row in rows} == {"false"}, f"rows {field} must remain false")
    require({row["cc_extrapolation_used"] for row in rows} == {"false"}, "CC extrapolation forbidden")
    require({row["claim_boundary"] for row in rows} == {CLAIM_BOUNDARY}, "bad row claim boundary")
    print(f"PAPER10_DESI_DR2_RADIAL_BAO_CC_MATCH_VALIDATED verdict={summary['verdict']}")


if __name__ == "__main__":
    main()

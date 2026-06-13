#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_dr2_high_z_bao_policy_v1.csv"
CC_MATCH = ROOT / "data/derived/paper10_desi_dr2_radial_bao_cc_match_v1_summary.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_dr2_high_z_bao_policy_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_dr2_high_z_bao_policy_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def write_csv(path: Path, row: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(row.keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerow(row)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    policy = read_one(POLICY)
    cc_match = read_one(CC_MATCH)
    require(policy["status"] == "SOURCE_SIDE_HIGH_Z_POLICY_FROZEN_NOT_REPLAY_NOT_VALIDATION", "bad policy status")
    require(policy["claim_boundary"] == CLAIM_BOUNDARY, "bad claim boundary")
    require(cc_match["verdict"] == "desi_bao_cc_support_partially_matched_high_z_row_blocked_no_replay", "CC match ledger not frozen")
    require(policy["blocked_radial_indices"] == cc_match["blocked_radial_indices"], "blocked radial index mismatch")
    require(policy["blocked_z_eff"] == cc_match["blocked_z_eff"], "blocked z mismatch")
    require(policy["accepted_policy"] == "exclude_from_first_CC_matched_time_endpoint_no_extrapolation", "bad accepted policy")
    require(policy["allowed_endpoint_scope"] == "DESI_radial_rows_within_CC_support_only", "bad endpoint scope")
    require("CC_extrapolation" in policy["forbidden_use"], "CC extrapolation must be forbidden")
    for field in ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"]:
        require(policy[field] == "false", f"{field} must remain false")
    summary = {
        "policy_id": policy["policy_id"],
        "status": "DESI_DR2_HIGH_Z_BAO_POLICY_FROZEN_NOT_REPLAY_NOT_VALIDATION",
        "parent_cc_match": policy["parent_cc_match"],
        "accepted_policy": policy["accepted_policy"],
        "allowed_endpoint_scope": policy["allowed_endpoint_scope"],
        "blocked_radial_indices": policy["blocked_radial_indices"],
        "blocked_z_eff": policy["blocked_z_eff"],
        "matched_rows_allowed_for_first_endpoint": cc_match["matched_within_cc_range_rows"],
        "high_z_row_future_role": policy["high_z_row_future_role"],
        "next_required_gate": policy["next_required_gate"],
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_validation_claimed": "false",
        "claim_boundary": CLAIM_BOUNDARY,
        "verdict": "high_z_lya_row_predeclared_excluded_from_first_cc_matched_time_endpoint",
    }
    write_csv(SUMMARY, summary)
    print(f"PAPER10_DESI_DR2_HIGH_Z_BAO_POLICY_VALIDATED verdict={summary['verdict']}")


if __name__ == "__main__":
    main()

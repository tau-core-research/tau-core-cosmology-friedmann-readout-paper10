#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_dr2_bao_source_inventory_policy_v1.csv"
INVENTORY = ROOT / "data/derived/paper10_desi_dr2_bao_source_inventory_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_dr2_bao_source_inventory_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_dr2_bao_source_inventory_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    policy_rows = read_rows(POLICY)
    rows = read_rows(INVENTORY)
    summary_rows = read_rows(SUMMARY)
    require(len(policy_rows) == 1, "policy must contain exactly one row")
    require(len(summary_rows) == 1, "summary must contain exactly one row")
    policy = policy_rows[0]
    summary = summary_rows[0]

    require(policy["claim_boundary"] == CLAIM_BOUNDARY, "bad policy claim boundary")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "bad summary claim boundary")
    require(summary["status"] == "DESI_DR2_BAO_SOURCE_INVENTORY_FROZEN_NOT_REPLAY_NOT_VALIDATION", "bad status")
    require(summary["mean_row_count"] == "13", "unexpected DESI DR2 mean row count")
    require(summary["covariance_dimension"] == "13", "unexpected covariance dimension")
    require(summary["radial_dh_over_rd_rows"] == "6", "unexpected radial row count")
    require(int(summary["radial_dh_over_rd_rows"]) >= int(summary["minimum_radial_rows_for_endpoint_consideration"]), "radial source support below declared threshold")
    require(summary["candidate_bao_support_blocker_status"] == "source_frozen_but_not_integrated_into_endpoint", "bad blocker status")
    require(summary["verdict"] == "desi_dr2_public_bao_source_frozen_but_time_level_endpoint_not_replayed", "bad verdict")
    for field in ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"]:
        require(policy[field] == "false", f"policy {field} must remain false")
        require(summary[field] == "false", f"summary {field} must remain false")
        require({row[field] for row in rows} == {"false"}, f"inventory {field} must remain false")
    require(len(rows) == 13, "inventory must contain all 13 DESI DR2 combined BAO rows")
    radial = [row for row in rows if row["quantity"] == "DH_over_rs"]
    require(len(radial) == 6, "inventory must contain six radial DH rows")
    require({row["claim_boundary"] for row in rows} == {CLAIM_BOUNDARY}, "bad inventory claim boundary")
    require(all(row["mean_file_sha256"] for row in rows), "missing mean hashes")
    require(all(row["cov_file_sha256"] for row in rows), "missing covariance hashes")
    print(f"PAPER10_DESI_DR2_BAO_SOURCE_INVENTORY_VALIDATED verdict={summary['verdict']}")


if __name__ == "__main__":
    main()

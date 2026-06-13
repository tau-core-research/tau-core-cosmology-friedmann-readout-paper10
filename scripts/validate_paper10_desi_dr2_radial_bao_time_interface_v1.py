#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_dr2_radial_bao_time_interface_policy_v1.csv"
OUT = ROOT / "data/derived/paper10_desi_dr2_radial_bao_time_interface_v1.csv"
COV_OUT = ROOT / "data/derived/paper10_desi_dr2_radial_bao_time_interface_covariance_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_dr2_radial_bao_time_interface_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_dr2_radial_bao_time_interface_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    policy_rows = read_rows(POLICY)
    rows = read_rows(OUT)
    cov_rows = read_rows(COV_OUT)
    summary_rows = read_rows(SUMMARY)
    require(len(policy_rows) == 1, "policy must contain one row")
    require(len(summary_rows) == 1, "summary must contain one row")
    policy = policy_rows[0]
    summary = summary_rows[0]
    require(policy["claim_boundary"] == CLAIM_BOUNDARY, "bad policy claim boundary")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "bad summary claim boundary")
    require(summary["status"] == "DESI_DR2_RADIAL_BAO_TIME_INTERFACE_FROZEN_NOT_REPLAY_NOT_VALIDATION", "bad status")
    require(summary["radial_row_count"] == "6", "bad radial row count")
    require(summary["covariance_dimension"] == "6", "bad covariance dimension")
    require(summary["beta_rd_nuisance_required"] == "true", "beta_rd nuisance guard missing")
    require(summary["matched_cc_support_required_before_replay"] == "true", "matched CC replay guard missing")
    require(summary["control_seed_manifest_required_before_replay"] == "true", "control seed replay guard missing")
    require(summary["verdict"] == "desi_radial_bao_time_interface_frozen_but_endpoint_replay_still_blocked", "bad verdict")
    require(len(rows) == 6, "interface must contain six radial rows")
    require(len(cov_rows) == 36, "covariance output must contain 6x6 rows")
    require({row["radial_index"] for row in rows} == {"0", "1", "2", "3", "4", "5"}, "bad radial indices")
    require({row["row_i"] for row in cov_rows} == {"0", "1", "2", "3", "4", "5"}, "bad covariance row indices")
    require({row["row_j"] for row in cov_rows} == {"0", "1", "2", "3", "4", "5"}, "bad covariance column indices")
    for field in ["endpoint_replay_allowed", "endpoint_validation_claimed", "physical_validation_claimed"]:
        require(policy[field] == "false", f"policy {field} must remain false")
        require(summary[field] == "false", f"summary {field} must remain false")
        require({row[field] for row in rows} == {"false"}, f"interface {field} must remain false")
        require({row[field] for row in cov_rows} == {"false"}, f"covariance {field} must remain false")
    require({row["claim_boundary"] for row in rows} == {CLAIM_BOUNDARY}, "bad interface claim boundary")
    require({row["claim_boundary"] for row in cov_rows} == {CLAIM_BOUNDARY}, "bad covariance claim boundary")
    print(f"PAPER10_DESI_DR2_RADIAL_BAO_TIME_INTERFACE_VALIDATED verdict={summary['verdict']}")


if __name__ == "__main__":
    main()

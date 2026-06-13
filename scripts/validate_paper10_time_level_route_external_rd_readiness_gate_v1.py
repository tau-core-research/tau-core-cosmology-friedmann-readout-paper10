#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/paper10_time_level_route_external_rd_readiness_gate_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_time_level_route_external_rd_readiness_gate_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_time_level_route_external_rd_readiness_gate_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    rows = read_rows(OUT)
    summary = read_one(SUMMARY)
    by_item = {row["item"]: row for row in rows}
    require(len(rows) == 11, "readiness gate must record nine closed source blockers, one diagnostic, and one endpoint blocker")
    require(by_item["external_rd_prior_source_freeze"]["status"] == "CLOSED_SOURCE_SIDE", "external prior source freeze not closed")
    require(
        by_item["joint_rd_marginalization_protocol_definition"]["status"] == "CLOSED_SOURCE_SIDE",
        "rd marginalization protocol definition not closed",
    )
    require(
        by_item["endpoint_control_suite_definition"]["status"] == "CLOSED_SOURCE_SIDE",
        "endpoint control suite definition not closed",
    )
    require(
        by_item["bao_support_expansion_manifest_declared"]["status"] == "CLOSED_SOURCE_SIDE",
        "BAO support expansion manifest not declared",
    )
    require(
        by_item["desi_dr2_public_bao_source_inventory_frozen"]["status"] == "CLOSED_SOURCE_SIDE",
        "DESI DR2 source inventory not frozen",
    )
    require(
        by_item["desi_dr2_radial_bao_time_interface_frozen"]["status"] == "CLOSED_SOURCE_SIDE",
        "DESI DR2 radial BAO time interface not frozen",
    )
    require(
        by_item["desi_dr2_radial_bao_cc_match_ledger_frozen"]["status"] == "CLOSED_SOURCE_SIDE",
        "DESI DR2 radial BAO CC match ledger not frozen",
    )
    require(
        by_item["desi_dr2_high_z_row_policy_frozen"]["status"] == "CLOSED_SOURCE_SIDE",
        "DESI DR2 high-z row policy not frozen",
    )
    require(
        by_item["desi_time_level_control_seed_manifest_frozen"]["status"] == "CLOSED_SOURCE_SIDE",
        "DESI time-level control seed manifest not frozen",
    )
    require(
        by_item["low_significance_current_sdss_bao_difference"]["status"]
        == "CLOSED_DIAGNOSTIC_NOT_DESI_BLOCKER",
        "legacy low-significance SDSS diagnostic must be retained but not active as a DESI blocker",
    )
    require(
        by_item["time_level_endpoint_authorization_review_missing"]["status"] == "BLOCKER_OPEN",
        "endpoint authorization review must remain the active open blocker",
    )
    require(summary["rd_prior_source_id"] == "Planck2018_base_LCDM_TTTEEE_lowE_lensing_rdrag", "bad rd source")
    require(
        summary["verdict"]
        == "desi_time_cc_matched_scope_and_controls_frozen_but_endpoint_authorization_missing",
        "bad verdict",
    )
    require(summary["desi_dr2_radial_dh_over_rd_rows"] == "6", "bad DESI radial row count")
    require(summary["desi_dr2_covariance_dimension"] == "13", "bad DESI covariance dimension")
    require(summary["desi_dr2_time_interface_z_range"] == "0.51;2.33", "bad DESI time-interface z range")
    require(summary["desi_dr2_cc_matched_rows"] == "5", "bad DESI CC matched count")
    require(summary["desi_dr2_cc_blocked_rows"] == "1", "bad DESI CC blocked count")
    require(summary["desi_dr2_first_cc_matched_endpoint_rows"] == "5", "bad DESI first endpoint row count")
    require(summary["desi_time_level_control_family_count"] == "7", "bad DESI control-family count")
    require(summary["desi_time_level_control_seed_range"] == "41001;41007", "bad DESI control seed range")
    require("external_rd_prior_source_freeze" in summary["closed_source_side_blockers"], "closed blocker missing")
    require(
        "joint_rd_marginalization_protocol_definition" in summary["closed_source_side_blockers"],
        "rd marginalization protocol blocker missing",
    )
    require(
        "endpoint_control_suite_definition" in summary["closed_source_side_blockers"],
        "endpoint control suite blocker missing",
    )
    require(
        "bao_support_expansion_manifest_declared" in summary["closed_source_side_blockers"],
        "BAO support expansion manifest missing",
    )
    require(
        "desi_dr2_public_bao_source_inventory_frozen" in summary["closed_source_side_blockers"],
        "DESI source inventory blocker missing",
    )
    require(
        "desi_dr2_radial_bao_time_interface_frozen" in summary["closed_source_side_blockers"],
        "DESI time interface blocker missing",
    )
    require(
        "desi_dr2_radial_bao_cc_match_ledger_frozen" in summary["closed_source_side_blockers"],
        "DESI CC match ledger blocker missing",
    )
    require(
        "desi_dr2_high_z_row_policy_frozen" in summary["closed_source_side_blockers"],
        "DESI high-z policy blocker missing",
    )
    require(
        "desi_time_level_control_seed_manifest_frozen" in summary["closed_source_side_blockers"],
        "DESI control seed manifest blocker missing",
    )
    require(
        "low_significance_current_sdss_bao_difference"
        in summary["closed_diagnostics_not_active_endpoint_blockers"],
        "legacy SDSS low-significance diagnostic missing",
    )
    require(
        summary["open_endpoint_blockers"] == "time_level_endpoint_authorization_review_missing",
        "endpoint authorization must be the only active open blocker",
    )
    for row in rows + [summary]:
        require(row["endpoint_replay_allowed"] == "false", "endpoint replay must remain false")
        require(row["endpoint_validation_claimed"] == "false", "endpoint validation must remain false")
        require(row["physical_validation_claimed"] == "false", "physical validation must remain false")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "bad claim boundary")
    print(
        "PAPER10_TIME_LEVEL_ROUTE_EXTERNAL_RD_READINESS_GATE_VALIDATED "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()

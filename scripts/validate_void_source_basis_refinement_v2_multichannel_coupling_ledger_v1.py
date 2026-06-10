#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_multichannel_coupling_ledger.csv"
SUMMARY = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_multichannel_coupling_ledger_summary.csv"

COMPONENT_ID = "V2_MULTI_CHANNEL_COUPLING"
CLAIM_BOUNDARY = "v2_multichannel_coupling_ledger_not_scoring_not_validation"
REQUIRED_RULES = {
    "VOID_WEB_VALUE_PAIR",
    "VOID_WEB_PATH",
    "VOID_WEB_TIME",
    "FULL_V2_PROJECTION_MORPHOLOGY",
}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    rows = read_rows(LEDGER)
    summary = read_one(SUMMARY)
    require(rows, "coupling ledger is empty")
    require({row["coupling_rule_id"] for row in rows} == REQUIRED_RULES, "coupling rule set mismatch")
    require(summary["component_id"] == COMPONENT_ID, "summary component mismatch")
    require(summary["status"] == "V2_MULTI_CHANNEL_COUPLING_LEDGER_FROZEN_ENDPOINT_BLOCKED", "bad summary status")
    require(summary["coupling_rule_count"] == str(len(rows)), "rule count mismatch")
    require(summary["blocked_coupling_rule_count"] == str(len(rows)), "all rules should be blocked")
    require(summary["endpoint_ready_coupling_rule_count"] == "0", "no coupling rule should be endpoint ready")
    require(summary["void_values_available"] == "true", "void values should be available")
    require(summary["web_values_available"] == "true", "web values should be available")
    require(summary["path_values_available"] == "false", "path values should be blocked")
    require(summary["time_values_available"] == "false", "time values should be blocked")
    require(summary["cmb_safety_passed"] == "true", "CMB safety should pass")
    require(summary["void_weak_negative_preserved"] == "true", "void weak negative must be preserved")
    require(summary["endpoint_replay_allowed"] == "false", "summary must not allow endpoint replay")
    require(summary["endpoint_validation_claimed"] == "false", "summary must not claim validation")
    require(summary["contains_endpoint_scores"] == "false", "summary must not contain endpoint scores")
    require(summary["contains_distance_residuals"] == "false", "summary must not contain distance residuals")
    require(summary["contains_fit_statistics"] == "false", "summary must not contain fit statistics")
    require(summary["verdict"] == "multichannel_coupling_accounted_but_endpoint_blocked", "unexpected verdict")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")

    by_rule = {row["coupling_rule_id"]: row for row in rows}
    require(by_rule["VOID_WEB_VALUE_PAIR"]["coupling_values_computable"] == "true", "void+web should be computable")
    require(
        by_rule["VOID_WEB_VALUE_PAIR"]["blocking_reason"] == "void_branch_weak_negative_control_dominance_preserved",
        "void+web blocking reason mismatch",
    )
    require(by_rule["VOID_WEB_PATH"]["source_values_available"] == "false", "path coupling should lack values")
    require(by_rule["VOID_WEB_TIME"]["source_values_available"] == "false", "time coupling should lack values")
    require(by_rule["FULL_V2_PROJECTION_MORPHOLOGY"]["source_values_available"] == "false", "full V2 should lack values")
    for row in rows:
        require(row["component_id"] == COMPONENT_ID, "row component mismatch")
        require(row["endpoint_ready"] == "false", "row must not be endpoint ready")
        require(row["endpoint_replay_allowed"] == "false", "row must not allow endpoint replay")
        require(row["endpoint_validation_claimed"] == "false", "row must not claim validation")
        require(row["contains_endpoint_scores"] == "false", "row must not contain endpoint scores")
        require(row["contains_distance_residuals"] == "false", "row must not contain distance residuals")
        require(row["contains_fit_statistics"] == "false", "row must not contain fit statistics")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
    print(
        "PAPER10_V2_MULTICHANNEL_COUPLING_LEDGER_VALIDATED "
        f"rules={len(rows)} endpoint_ready=0"
    )


if __name__ == "__main__":
    main()

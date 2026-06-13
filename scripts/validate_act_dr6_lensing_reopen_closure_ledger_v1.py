#!/usr/bin/env python3
"""Validate the ACT DR6 path-weight reopen closure ledger."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "data" / "derived" / "act_dr6_lensing_reopen_closure_ledger_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "act_dr6_lensing_reopen_closure_ledger_v1_summary.csv"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    rows = read_rows(LEDGER)
    summary_rows = read_rows(SUMMARY)
    if len(rows) != 7:
        raise SystemExit(f"expected seven ACT reopen rows, found {len(rows)}")
    if len(summary_rows) != 1:
        raise SystemExit(f"expected one summary row, found {len(summary_rows)}")
    summary = summary_rows[0]
    expected_requirements = {
        "ACT_REOPEN_01_SOURCE_OBJECT",
        "ACT_REOPEN_02_E_MODE_ROUTE",
        "ACT_REOPEN_03_CURL_NULL_POLICY",
        "ACT_REOPEN_04_MASK_AND_COVERAGE_POLICY",
        "ACT_REOPEN_05_UNITS_AND_NORMALIZATION",
        "ACT_REOPEN_06_CHANNEL_HANDOFF",
        "ACT_REOPEN_07_CONTROL_SUITE",
    }
    if {row["requirement_id"] for row in rows} != expected_requirements:
        raise SystemExit("unexpected ACT reopen requirement set")
    if any(row["endpoint_replay_allowed"] != "false" for row in rows):
        raise SystemExit("ledger rows must not allow endpoint replay")
    if any(row["physical_lensing_path_weight_claimed"] != "false" for row in rows):
        raise SystemExit("ledger rows must not claim physical path weight")
    expected = {
        "artifact_id": "ACT_DR6_LENSING_REOPEN_CLOSURE_LEDGER_V1",
        "status": "ACT_REOPEN_GATES_CLOSED_FOR_CURRENT_BRANCH_REPLAY_DISABLED",
        "source_basis_verdict": "ACT_SOURCE_BASIS_DEMOTED_REOPEN_ONLY_WITH_NEW_SOURCE_FREEZE",
        "control_diagnostic_verdict": "ACT_PATH_WEIGHT_WEAK_NON_SPECIFIC_SIGNAL_CONTROL_DOMINATED",
        "best_control_branch": "curl_null",
        "controls_better_than_candidate": "4",
        "all_reopen_gates_accounted": "true",
        "all_reopen_gates_closed_or_frozen": "true",
        "current_branch_control_dominated": "true",
        "current_branch_endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "family_verdict_allowed": "false",
        "physical_lensing_path_weight_claimed": "false",
        "dark_sector_inference_allowed": "false",
        "verdict": "ACT_REOPEN_CLOSED_CURRENT_BRANCH_QUARANTINED_NOT_VALIDATION",
    }
    for key, value in expected.items():
        if summary.get(key) != value:
            raise SystemExit(f"{key}: expected {value!r}, got {summary.get(key)!r}")
    if "quarantine rather than replay authorization" not in summary["claim_boundary"]:
        raise SystemExit("claim boundary must state quarantine, not replay authorization")


if __name__ == "__main__":
    main()

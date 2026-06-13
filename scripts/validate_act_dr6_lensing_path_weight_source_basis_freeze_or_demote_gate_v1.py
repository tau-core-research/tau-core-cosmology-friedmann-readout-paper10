#!/usr/bin/env python3
"""Validate the ACT path-weight source-basis freeze-or-demote gate."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "data" / "derived" / "act_dr6_lensing_path_weight_source_basis_freeze_or_demote_gate_v1_summary.csv"
CHECKLIST = ROOT / "data" / "derived" / "act_dr6_lensing_path_weight_source_basis_freeze_or_demote_gate_v1_checklist.csv"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    summary_rows = read_rows(SUMMARY)
    if len(summary_rows) != 1:
        raise SystemExit(f"expected one summary row, found {len(summary_rows)}")
    row = summary_rows[0]
    expected = {
        "artifact_id": "ACT_DR6_LENSING_PATH_WEIGHT_SOURCE_BASIS_FREEZE_OR_DEMOTE_GATE_V1",
        "status": "SOURCE_BASIS_FREEZE_OR_DEMOTE_GATE_BUILT_NOT_VALIDATION",
        "decision": "DEMOTE_CURRENT_UNITLESS_ACT_PATH_WEIGHT_BASIS",
        "current_basis_replay_allowed_now": "false",
        "reopen_allowed_with_new_source_freeze": "true",
        "endpoint_validation_claimed": "false",
        "physical_lensing_path_weight_claimed": "false",
        "dark_sector_inference_allowed": "false",
        "source_object_defined_source_side": "true",
        "e_mode_route_defined_source_side": "true",
        "curl_null_policy_frozen_source_side": "true",
        "curl_current_branch_vetoed": "true",
        "mask_coverage_policy_frozen_source_side": "true",
        "units_normalization_policy_frozen_source_side": "true",
        "physical_normalization_blocker_open": "true",
        "channel_handoff_policy_frozen_source_side": "true",
        "channel_handoff_source_diagnostic_only": "true",
        "control_suite_policy_frozen_source_side": "true",
        "control_suite_replay_disabled": "true",
        "verdict": "ACT_SOURCE_BASIS_DEMOTED_REOPEN_ONLY_WITH_NEW_SOURCE_FREEZE",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise SystemExit(f"{key}: expected {value!r}, got {row.get(key)!r}")

    checklist = read_rows(CHECKLIST)
    if len(checklist) < 7:
        raise SystemExit("expected at least seven reopen checklist rows")
    statuses = {r["current_status"] for r in checklist}
    if (
        "DEFINED_SOURCE_SIDE" not in statuses
        or "FROZEN_SOURCE_SIDE_VETO_ACTIVE" not in statuses
        or "FROZEN_SOURCE_SIDE" not in statuses
        or "PROXY_FROZEN_PHYSICAL_BLOCKER_OPEN" not in statuses
        or "SOURCE_DIAGNOSTIC_ONLY_NOT_PHYSICAL_K_PATH" not in statuses
        or "FROZEN_CURRENT_BRANCH_REPLAY_STILL_DISABLED" not in statuses
    ):
        raise SystemExit(
            "checklist should preserve defined, frozen, proxy-blocked, "
            "diagnostic-only, veto-active, and replay-disabled control blockers"
        )
    if any(r["required_for_reopen"].lower() != "true" for r in checklist):
        raise SystemExit("all checklist rows must be required for reopen")
    if not any(
        r["requirement_id"] == "ACT_REOPEN_01_SOURCE_OBJECT"
        and r["current_status"] == "DEFINED_SOURCE_SIDE"
        for r in checklist
    ):
        raise SystemExit("source object requirement should be defined source-side")
    if not any(
        r["requirement_id"] == "ACT_REOPEN_02_E_MODE_ROUTE"
        and r["current_status"] == "DEFINED_SOURCE_SIDE"
        for r in checklist
    ):
        raise SystemExit("E-mode route requirement should be defined source-side")
    if not any(
        r["requirement_id"] == "ACT_REOPEN_03_CURL_NULL_POLICY"
        and r["current_status"] == "FROZEN_SOURCE_SIDE_VETO_ACTIVE"
        for r in checklist
    ):
        raise SystemExit("curl null policy should be frozen with veto active")
    if not any(
        r["requirement_id"] == "ACT_REOPEN_04_MASK_AND_COVERAGE_POLICY"
        and r["current_status"] == "FROZEN_SOURCE_SIDE"
        for r in checklist
    ):
        raise SystemExit("mask/coverage policy should be frozen source-side")
    if not any(
        r["requirement_id"] == "ACT_REOPEN_05_UNITS_AND_NORMALIZATION"
        and r["current_status"] == "PROXY_FROZEN_PHYSICAL_BLOCKER_OPEN"
        for r in checklist
    ):
        raise SystemExit("units/normalization policy should freeze proxy while keeping physical blocker open")
    if not any(
        r["requirement_id"] == "ACT_REOPEN_06_CHANNEL_HANDOFF"
        and r["current_status"] == "SOURCE_DIAGNOSTIC_ONLY_NOT_PHYSICAL_K_PATH"
        for r in checklist
    ):
        raise SystemExit("channel handoff should be source diagnostic only, not physical K_path")
    if not any(
        r["requirement_id"] == "ACT_REOPEN_07_CONTROL_SUITE"
        and r["current_status"] == "FROZEN_CURRENT_BRANCH_REPLAY_STILL_DISABLED"
        for r in checklist
    ):
        raise SystemExit("control suite should be frozen while replay remains disabled")
    if not any(r["requirement_id"] == "ACT_REOPEN_03_CURL_NULL_POLICY" for r in checklist):
        raise SystemExit("curl null policy blocker missing")
    if "new source-side basis freeze" not in row["claim_boundary"]:
        raise SystemExit("claim boundary must require a new source-side basis freeze")


if __name__ == "__main__":
    main()

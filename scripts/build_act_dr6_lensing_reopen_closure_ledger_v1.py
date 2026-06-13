#!/usr/bin/env python3
"""Build a closure ledger for the ACT DR6 path-weight reopen gates."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data" / "derived"
SOURCE_BASIS = DERIVED / "act_dr6_lensing_path_weight_source_basis_freeze_or_demote_gate_v1_summary.csv"
CHECKLIST = DERIVED / "act_dr6_lensing_path_weight_source_basis_freeze_or_demote_gate_v1_checklist.csv"
CONTROL_DIAGNOSTIC = DERIVED / "act_dr6_lensing_path_weight_control_dominance_diagnostic_v1_summary.csv"
OUT = DERIVED / "act_dr6_lensing_reopen_closure_ledger_v1.csv"
SUMMARY_OUT = DERIVED / "act_dr6_lensing_reopen_closure_ledger_v1_summary.csv"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise RuntimeError(f"expected one row in {path}, found {len(rows)}")
    return rows[0]


def main() -> None:
    source_basis = read_one(SOURCE_BASIS)
    control = read_one(CONTROL_DIAGNOSTIC)
    checklist = read_rows(CHECKLIST)

    status_by_requirement = {row["requirement_id"]: row["current_status"] for row in checklist}
    expected_requirements = {
        "ACT_REOPEN_01_SOURCE_OBJECT",
        "ACT_REOPEN_02_E_MODE_ROUTE",
        "ACT_REOPEN_03_CURL_NULL_POLICY",
        "ACT_REOPEN_04_MASK_AND_COVERAGE_POLICY",
        "ACT_REOPEN_05_UNITS_AND_NORMALIZATION",
        "ACT_REOPEN_06_CHANNEL_HANDOFF",
        "ACT_REOPEN_07_CONTROL_SUITE",
    }
    closed_statuses = {
        "DEFINED_SOURCE_SIDE",
        "FROZEN_SOURCE_SIDE",
        "FROZEN_SOURCE_SIDE_VETO_ACTIVE",
        "PROXY_FROZEN_PHYSICAL_BLOCKER_OPEN",
        "SOURCE_DIAGNOSTIC_ONLY_NOT_PHYSICAL_K_PATH",
        "FROZEN_CURRENT_BRANCH_REPLAY_STILL_DISABLED",
    }
    all_reopen_gates_accounted = set(status_by_requirement) == expected_requirements
    all_reopen_gates_closed_or_frozen = all(
        row["current_status"] in closed_statuses for row in checklist
    )
    control_dominated = (
        control["verdict"] == "ACT_PATH_WEIGHT_WEAK_NON_SPECIFIC_SIGNAL_CONTROL_DOMINATED"
    )

    ledger_rows = []
    for row in checklist:
        ledger_rows.append(
            {
                "artifact_id": "ACT_DR6_LENSING_REOPEN_CLOSURE_LEDGER_V1",
                "requirement_id": row["requirement_id"],
                "current_status": row["current_status"],
                "closure_interpretation": (
                    "closed_or_frozen_for_current_branch"
                    if row["current_status"] in closed_statuses
                    else "open"
                ),
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "physical_lensing_path_weight_claimed": "false",
                "family_verdict_allowed": "false",
                "claim_boundary": "act_reopen_closure_ledger_not_validation",
            }
        )

    summary = {
        "artifact_id": "ACT_DR6_LENSING_REOPEN_CLOSURE_LEDGER_V1",
        "status": "ACT_REOPEN_GATES_CLOSED_FOR_CURRENT_BRANCH_REPLAY_DISABLED",
        "source_basis_gate": source_basis["artifact_id"],
        "source_basis_verdict": source_basis["verdict"],
        "control_diagnostic_verdict": control["verdict"],
        "best_control_branch": control["best_control_branch"],
        "controls_better_than_candidate": control["controls_better_than_candidate"],
        "all_reopen_gates_accounted": str(all_reopen_gates_accounted).lower(),
        "all_reopen_gates_closed_or_frozen": str(all_reopen_gates_closed_or_frozen).lower(),
        "current_branch_control_dominated": str(control_dominated).lower(),
        "current_branch_endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "family_verdict_allowed": "false",
        "physical_lensing_path_weight_claimed": "false",
        "dark_sector_inference_allowed": "false",
        "allowed_next_action": (
            "preserve_current_ACT_branch_as_control_dominated_diagnostic_or_start_new_"
            "source_basis_design_without_reusing_endpoint_scores"
        ),
        "forbidden_next_action": (
            "endpoint_replay_or_family_verdict_from_current_ACT_branch;posthoc_recenter_rescue;"
            "physical_K_path_promotion;dark_sector_inference"
        ),
        "claim_boundary": (
            "all seven ACT reopen gates are now accounted for, but closure means current-branch "
            "quarantine rather than replay authorization"
        ),
        "verdict": "ACT_REOPEN_CLOSED_CURRENT_BRANCH_QUARANTINED_NOT_VALIDATION",
    }

    DERIVED.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(ledger_rows[0]))
        writer.writeheader()
        writer.writerows(ledger_rows)
    with SUMMARY_OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary))
        writer.writeheader()
        writer.writerow(summary)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build the ACT path-weight source-basis freeze-or-demote gate."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data" / "derived"
SOURCE_MANIFEST = ROOT / "data" / "source_manifest"
P11_GATE = DERIVED / "act_dr6_lensing_path_weight_paper11_control_veto_gate_v1_summary.csv"
SOURCE_OBJECT = SOURCE_MANIFEST / "act_dr6_lensing_observer_path_source_object_v1.csv"
E_MODE_ROUTE = SOURCE_MANIFEST / "act_dr6_lensing_e_mode_route_v1.csv"
CURL_NULL_POLICY = SOURCE_MANIFEST / "act_dr6_lensing_curl_null_policy_v1.csv"
MASK_COVERAGE_POLICY = SOURCE_MANIFEST / "act_dr6_lensing_mask_coverage_policy_v1.csv"
UNITS_NORMALIZATION_POLICY = SOURCE_MANIFEST / "act_dr6_lensing_units_normalization_policy_v1.csv"
CHANNEL_HANDOFF_POLICY = SOURCE_MANIFEST / "act_dr6_lensing_channel_handoff_policy_v1.csv"
CONTROL_SUITE_POLICY = DERIVED / "act_dr6_lensing_control_suite_policy_v1_summary.csv"
SUMMARY_OUT = DERIVED / "act_dr6_lensing_path_weight_source_basis_freeze_or_demote_gate_v1_summary.csv"
CHECKLIST_OUT = DERIVED / "act_dr6_lensing_path_weight_source_basis_freeze_or_demote_gate_v1_checklist.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise RuntimeError(f"expected one row in {path}, found {len(rows)}")
    return rows[0]


def main() -> None:
    p11 = read_one(P11_GATE)
    vetoed = p11["verdict"] == "PAPER11_CONTROL_VETO_ACT_PATH_WEIGHT_NOT_FAMILY_VERDICT_ELIGIBLE"
    source_object_defined = False
    if SOURCE_OBJECT.exists():
        source_object = read_one(SOURCE_OBJECT)
        source_object_defined = (
            source_object["verdict"] == "ACT_REOPEN_01_SOURCE_OBJECT_DEFINED_BUT_REPLAY_STILL_DISABLED"
        )
    e_mode_route_defined = False
    if E_MODE_ROUTE.exists():
        e_mode_route = read_one(E_MODE_ROUTE)
        e_mode_route_defined = (
            e_mode_route["verdict"]
            == "ACT_REOPEN_02_E_MODE_ROUTE_DEFINED_SOURCE_SIDE_BUT_NOT_PHYSICAL_KERNEL"
        )
    curl_null_policy_frozen = False
    curl_current_branch_vetoed = False
    if CURL_NULL_POLICY.exists():
        curl_null_policy = read_one(CURL_NULL_POLICY)
        curl_null_policy_frozen = (
            curl_null_policy["status"] == "CURL_NULL_POLICY_FROZEN_SOURCE_SIDE_NOT_THEOREM"
        )
        curl_current_branch_vetoed = (
            curl_null_policy["verdict"] == "ACT_REOPEN_03_CURL_NULL_POLICY_FROZEN_AND_CURRENT_BRANCH_VETOED"
        )
    mask_coverage_policy_frozen = False
    if MASK_COVERAGE_POLICY.exists():
        mask_coverage_policy = read_one(MASK_COVERAGE_POLICY)
        mask_coverage_policy_frozen = (
            mask_coverage_policy["verdict"] == "ACT_REOPEN_04_MASK_AND_COVERAGE_POLICY_FROZEN_SOURCE_SIDE"
        )
    units_normalization_policy_frozen = False
    physical_normalization_blocker_open = False
    if UNITS_NORMALIZATION_POLICY.exists():
        units_normalization_policy = read_one(UNITS_NORMALIZATION_POLICY)
        units_normalization_policy_frozen = (
            units_normalization_policy["verdict"]
            == "ACT_REOPEN_05_UNITS_NORMALIZATION_PROXY_FROZEN_PHYSICAL_BLOCKER_OPEN"
        )
        physical_normalization_blocker_open = (
            units_normalization_policy["physical_normalization_allowed_now"] == "false"
        )
    channel_handoff_policy_frozen = False
    channel_handoff_source_diagnostic_only = False
    if CHANNEL_HANDOFF_POLICY.exists():
        channel_handoff_policy = read_one(CHANNEL_HANDOFF_POLICY)
        channel_handoff_policy_frozen = (
            channel_handoff_policy["verdict"]
            == "ACT_REOPEN_06_CHANNEL_HANDOFF_SOURCE_DIAGNOSTIC_ONLY"
        )
        channel_handoff_source_diagnostic_only = (
            channel_handoff_policy["current_tau_channel_status"]
            == "K_path_candidate_source_diagnostic_only"
        )
    control_suite_policy_frozen = False
    control_suite_replay_disabled = False
    if CONTROL_SUITE_POLICY.exists():
        control_suite_policy = read_one(CONTROL_SUITE_POLICY)
        control_suite_policy_frozen = (
            control_suite_policy["verdict"]
            == "ACT_REOPEN_07_CONTROL_SUITE_FROZEN_CURRENT_BRANCH_REPLAY_STILL_DISABLED"
        )
        control_suite_replay_disabled = (
            control_suite_policy["current_suite_replay_allowed"] == "false"
        )

    checklist = [
        {
            "requirement_id": "ACT_REOPEN_01_SOURCE_OBJECT",
            "required_for_reopen": "true",
            "current_status": "DEFINED_SOURCE_SIDE" if source_object_defined else "MISSING",
            "description": "Define the ACT observer/path source object beyond a unitless sampled vector.",
            "forbidden_inputs": "distance_residuals,fit_statistics,family_winner,endpoint_score",
        },
        {
            "requirement_id": "ACT_REOPEN_02_E_MODE_ROUTE",
            "required_for_reopen": "true",
            "current_status": "DEFINED_SOURCE_SIDE" if e_mode_route_defined else "MISSING",
            "description": "Derive why the baseline kappa/E-mode route is the physical candidate channel.",
            "forbidden_inputs": "distance_residuals,fit_statistics,control_performance",
        },
        {
            "requirement_id": "ACT_REOPEN_03_CURL_NULL_POLICY",
            "required_for_reopen": "true",
            "current_status": "FROZEN_SOURCE_SIDE_VETO_ACTIVE" if curl_null_policy_frozen else "MISSING",
            "description": "Freeze why curl is a null/gauge/control branch and how curl dominance vetoes promotion.",
            "forbidden_inputs": "endpoint_score,residual_shape,family_winner",
        },
        {
            "requirement_id": "ACT_REOPEN_04_MASK_AND_COVERAGE_POLICY",
            "required_for_reopen": "true",
            "current_status": "FROZEN_SOURCE_SIDE" if mask_coverage_policy_frozen else "PARTIAL",
            "description": "Freeze outside-mask, active-row, coverage, and selection policies before replay.",
            "forbidden_inputs": "distance_residuals,fit_statistics",
        },
        {
            "requirement_id": "ACT_REOPEN_05_UNITS_AND_NORMALIZATION",
            "required_for_reopen": "true",
            "current_status": (
                "PROXY_FROZEN_PHYSICAL_BLOCKER_OPEN"
                if units_normalization_policy_frozen
                else "MISSING"
            ),
            "description": (
                "Freeze the unitless median/MAD proxy and keep source-native or theorem-bounded "
                "physical normalization as an open blocker."
            ),
            "forbidden_inputs": "endpoint_score,best_fit_amplitude",
        },
        {
            "requirement_id": "ACT_REOPEN_06_CHANNEL_HANDOFF",
            "required_for_reopen": "true",
            "current_status": (
                "SOURCE_DIAGNOSTIC_ONLY_NOT_PHYSICAL_K_PATH"
                if channel_handoff_policy_frozen
                else "MISSING"
            ),
            "description": (
                "Declare the current baseline route as K_path-candidate source diagnostic only, "
                "with curl retained as K_null control."
            ),
            "forbidden_inputs": "endpoint_score,family_winner",
        },
        {
            "requirement_id": "ACT_REOPEN_07_CONTROL_SUITE",
            "required_for_reopen": "true",
            "current_status": (
                "FROZEN_CURRENT_BRANCH_REPLAY_STILL_DISABLED"
                if control_suite_policy_frozen
                else "PARTIAL"
            ),
            "description": (
                "Freeze current controls including curl, frequency difference, shuffle, sign, rank, "
                "and source-basis recentering as future-only stress."
            ),
            "forbidden_inputs": "posthoc_control_selection",
        },
    ]

    if vetoed:
        decision = "DEMOTE_CURRENT_UNITLESS_ACT_PATH_WEIGHT_BASIS"
        reopen_allowed = "true"
        replay_allowed_now = "false"
        endpoint_validation_claimed = "false"
        verdict = "ACT_SOURCE_BASIS_DEMOTED_REOPEN_ONLY_WITH_NEW_SOURCE_FREEZE"
    else:
        decision = "KEEP_ACT_PATH_WEIGHT_BASIS_UNDER_FAMILY_GATE"
        reopen_allowed = "not_applicable"
        replay_allowed_now = "false"
        endpoint_validation_claimed = "false"
        verdict = "ACT_SOURCE_BASIS_NOT_DEMOTED_BUT_ENDPOINT_STILL_DISABLED"

    row = {
        "artifact_id": "ACT_DR6_LENSING_PATH_WEIGHT_SOURCE_BASIS_FREEZE_OR_DEMOTE_GATE_V1",
        "status": "SOURCE_BASIS_FREEZE_OR_DEMOTE_GATE_BUILT_NOT_VALIDATION",
        "upstream_gate": p11["artifact_id"],
        "upstream_verdict": p11["verdict"],
        "decision": decision,
        "current_basis_replay_allowed_now": replay_allowed_now,
        "reopen_allowed_with_new_source_freeze": reopen_allowed,
        "endpoint_validation_claimed": endpoint_validation_claimed,
        "physical_lensing_path_weight_claimed": "false",
        "dark_sector_inference_allowed": "false",
        "source_object_defined_source_side": str(source_object_defined).lower(),
        "e_mode_route_defined_source_side": str(e_mode_route_defined).lower(),
        "curl_null_policy_frozen_source_side": str(curl_null_policy_frozen).lower(),
        "curl_current_branch_vetoed": str(curl_current_branch_vetoed).lower(),
        "mask_coverage_policy_frozen_source_side": str(mask_coverage_policy_frozen).lower(),
        "units_normalization_policy_frozen_source_side": str(units_normalization_policy_frozen).lower(),
        "physical_normalization_blocker_open": str(physical_normalization_blocker_open).lower(),
        "channel_handoff_policy_frozen_source_side": str(channel_handoff_policy_frozen).lower(),
        "channel_handoff_source_diagnostic_only": str(channel_handoff_source_diagnostic_only).lower(),
        "control_suite_policy_frozen_source_side": str(control_suite_policy_frozen).lower(),
        "control_suite_replay_disabled": str(control_suite_replay_disabled).lower(),
        "required_checklist_artifact": CHECKLIST_OUT.relative_to(ROOT).as_posix(),
        "claim_boundary": (
            "current ACT unitless path-weight basis is preserved as a negative/control-dominated "
            "candidate; any new replay requires a new source-side basis freeze"
        ),
        "verdict": verdict,
    }

    DERIVED.mkdir(parents=True, exist_ok=True)
    with SUMMARY_OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(row))
        writer.writeheader()
        writer.writerow(row)
    with CHECKLIST_OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(checklist[0]))
        writer.writeheader()
        writer.writerows(checklist)


if __name__ == "__main__":
    main()

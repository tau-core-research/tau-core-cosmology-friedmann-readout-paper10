#!/usr/bin/env python3
"""Freeze the ACT DR6 channel-handoff policy for the path-weight branch."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_MANIFEST = ROOT / "data" / "source_manifest"
DERIVED = ROOT / "data" / "derived"
SOURCE_OBJECT = SOURCE_MANIFEST / "act_dr6_lensing_observer_path_source_object_v1.csv"
E_MODE_ROUTE = SOURCE_MANIFEST / "act_dr6_lensing_e_mode_route_v1.csv"
CURL_NULL_POLICY = SOURCE_MANIFEST / "act_dr6_lensing_curl_null_policy_v1.csv"
UNITS_POLICY = SOURCE_MANIFEST / "act_dr6_lensing_units_normalization_policy_v1.csv"
P11_GATE = DERIVED / "act_dr6_lensing_path_weight_paper11_control_veto_gate_v1_summary.csv"
OUT = SOURCE_MANIFEST / "act_dr6_lensing_channel_handoff_policy_v1.csv"
SUMMARY_OUT = DERIVED / "act_dr6_lensing_channel_handoff_policy_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise RuntimeError(f"expected one row in {path}, found {len(rows)}")
    return rows[0]


def main() -> None:
    source_object = read_one(SOURCE_OBJECT)
    e_mode = read_one(E_MODE_ROUTE)
    curl = read_one(CURL_NULL_POLICY)
    units = read_one(UNITS_POLICY)
    p11 = read_one(P11_GATE)

    row = {
        "artifact_id": "ACT_DR6_LENSING_CHANNEL_HANDOFF_POLICY_V1",
        "status": "CHANNEL_HANDOFF_FROZEN_AS_SOURCE_DIAGNOSTIC_NOT_PHYSICAL_K_PATH",
        "source_object_artifact": source_object["artifact_id"],
        "candidate_route_artifact": e_mode["artifact_id"],
        "null_policy_artifact": curl["artifact_id"],
        "units_policy_artifact": units["artifact_id"],
        "upstream_control_veto_artifact": p11["artifact_id"],
        "candidate_input_channel": "ACT_baseline_kappa_convergence_samples",
        "candidate_tau_channel_requested": "K_path_observer_path",
        "current_tau_channel_status": "K_path_candidate_source_diagnostic_only",
        "positive_k_path_promotion_allowed": "false",
        "k_closure_handoff_allowed": "false",
        "k_null_handoff_allowed_for_curl": "true",
        "source_diagnostic_handoff_allowed": "true",
        "why_not_positive_k_path": (
            "the baseline route is source-side only, physical units are missing, and "
            "the Paper11-style control veto found curl_null as the best control"
        ),
        "why_not_k_closure": (
            "no closure equation, closure residual, or theorem-bounded mapping from ACT "
            "kappa samples to a closure term is frozen"
        ),
        "why_curl_is_k_null": (
            "curl is source-native null/control in this paper and curl dominance vetoes "
            "positive-channel promotion"
        ),
        "allowed_use_before_new_reopen": (
            "source-side diagnostic, negative/control-dominated candidate preservation, "
            "and future source-basis design"
        ),
        "disallowed_use_before_new_reopen": (
            "endpoint replay, validation, family verdict, physical K_path claim, K_closure "
            "claim, dark-sector inference, amplitude tuning"
        ),
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "family_verdict_allowed": "false",
        "physical_lensing_path_weight_claimed": "false",
        "dark_sector_inference_allowed": "false",
        "contains_distance_residuals": "false",
        "contains_fit_statistics": "false",
        "forbidden_inputs": "endpoint_score,distance_residuals,fit_statistics,family_winner,best_fit_amplitude",
        "claim_boundary": (
            "freezes ACT_REOPEN_06 by demoting the current baseline route to a "
            "K_path-candidate source diagnostic; curl remains K_null control"
        ),
        "verdict": "ACT_REOPEN_06_CHANNEL_HANDOFF_SOURCE_DIAGNOSTIC_ONLY",
    }

    SOURCE_MANIFEST.mkdir(parents=True, exist_ok=True)
    DERIVED.mkdir(parents=True, exist_ok=True)
    for path in (OUT, SUMMARY_OUT):
        with path.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(row))
            writer.writeheader()
            writer.writerow(row)


if __name__ == "__main__":
    main()

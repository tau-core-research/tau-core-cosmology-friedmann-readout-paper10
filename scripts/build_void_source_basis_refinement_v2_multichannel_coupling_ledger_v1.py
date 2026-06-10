#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VOID = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_void_morphology_values_summary.csv"
WEB = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_web_morphology_values_summary.csv"
PATH = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_path_projection_route_ledger_summary.csv"
TIME = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_time_readout_route_ledger_summary.csv"
CMB = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_cmb_safety_values_summary.csv"
OUT = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_multichannel_coupling_ledger.csv"
SUMMARY = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_multichannel_coupling_ledger_summary.csv"

COMPONENT_ID = "V2_MULTI_CHANNEL_COUPLING"
CLAIM_BOUNDARY = "v2_multichannel_coupling_ledger_not_scoring_not_validation"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    void = read_one(VOID)
    web = read_one(WEB)
    path = read_one(PATH)
    time = read_one(TIME)
    cmb = read_one(CMB)

    void_values_available = void["status"] == "V2_VOID_MORPHOLOGY_VALUES_FROZEN_WEAK_NEGATIVE_NOT_ENDPOINT_READY"
    web_values_available = web["status"] == "V2_WEB_MORPHOLOGY_VALUES_FROZEN_NOT_ENDPOINT_READY"
    path_values_available = path["path_values_computed"] == "true"
    time_values_available = time["time_values_computed"] == "true"
    cmb_safety_passed = cmb["cmb_lowz_support_passed"] == "true"
    void_weak_negative = void["weak_negative_status_inherited"] == "true"

    rows = [
        {
            "component_id": COMPONENT_ID,
            "coupling_rule_id": "VOID_WEB_VALUE_PAIR",
            "active_channels": "W_VOID_MATURITY;W_WEB_ANISOTROPY",
            "required_components": "V2_VOID_MORPHOLOGY;V2_WEB_MORPHOLOGY",
            "source_values_available": str(void_values_available and web_values_available).lower(),
            "coupling_values_computable": "true",
            "endpoint_ready": "false",
            "blocking_reason": "void_branch_weak_negative_control_dominance_preserved",
            "required_next_artifact": "source_side_coupling_controls_before_any_endpoint",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "contains_endpoint_scores": "false",
            "contains_distance_residuals": "false",
            "contains_fit_statistics": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "component_id": COMPONENT_ID,
            "coupling_rule_id": "VOID_WEB_PATH",
            "active_channels": "W_VOID_MATURITY;W_WEB_ANISOTROPY;W_PATH_PROJECTION",
            "required_components": "V2_VOID_MORPHOLOGY;V2_WEB_MORPHOLOGY;V2_OBSERVER_PATH_PROJECTION",
            "source_values_available": str(void_values_available and web_values_available and path_values_available).lower(),
            "coupling_values_computable": "false",
            "endpoint_ready": "false",
            "blocking_reason": "W_path_full_lowz_channel_blocked_partial_values_control_only",
            "required_next_artifact": "data/derived/void_source_basis_refinement_v2_path_projection_values.csv",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "contains_endpoint_scores": "false",
            "contains_distance_residuals": "false",
            "contains_fit_statistics": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "component_id": COMPONENT_ID,
            "coupling_rule_id": "VOID_WEB_TIME",
            "active_channels": "W_VOID_MATURITY;W_WEB_ANISOTROPY;W_TIME_READOUT",
            "required_components": "V2_VOID_MORPHOLOGY;V2_WEB_MORPHOLOGY;V2_TIME_READOUT_PROJECTION",
            "source_values_available": str(void_values_available and web_values_available and time_values_available).lower(),
            "coupling_values_computable": "false",
            "endpoint_ready": "false",
            "blocking_reason": "W_time_values_blocked_products_not_fetched_or_numeric_rule_missing",
            "required_next_artifact": "data/derived/void_source_basis_refinement_v2_time_readout_values.csv",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "contains_endpoint_scores": "false",
            "contains_distance_residuals": "false",
            "contains_fit_statistics": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "component_id": COMPONENT_ID,
            "coupling_rule_id": "FULL_V2_PROJECTION_MORPHOLOGY",
            "active_channels": "W_VOID_MATURITY;W_WEB_ANISOTROPY;W_PATH_PROJECTION;W_TIME_READOUT",
            "required_components": (
                "V2_VOID_MORPHOLOGY;V2_WEB_MORPHOLOGY;V2_OBSERVER_PATH_PROJECTION;"
                "V2_TIME_READOUT_PROJECTION;V2_CMB_SAFETY"
            ),
            "source_values_available": str(
                void_values_available and web_values_available and path_values_available and time_values_available and cmb_safety_passed
            ).lower(),
            "coupling_values_computable": "false",
            "endpoint_ready": "false",
            "blocking_reason": "path_and_time_values_blocked_and_void_branch_weak_negative",
            "required_next_artifact": "path_values;time_values;source_side_family_balanced_coupling_controls",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "contains_endpoint_scores": "false",
            "contains_distance_residuals": "false",
            "contains_fit_statistics": "false",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    blocked_rules = [row for row in rows if row["endpoint_ready"] != "true"]
    summary = [
        {
            "component_id": COMPONENT_ID,
            "status": "V2_MULTI_CHANNEL_COUPLING_LEDGER_FROZEN_ENDPOINT_BLOCKED",
            "void_values_available": str(void_values_available).lower(),
            "web_values_available": str(web_values_available).lower(),
            "path_values_available": str(path_values_available).lower(),
            "time_values_available": str(time_values_available).lower(),
            "cmb_safety_passed": str(cmb_safety_passed).lower(),
            "void_weak_negative_preserved": str(void_weak_negative).lower(),
            "coupling_rule_count": str(len(rows)),
            "blocked_coupling_rule_count": str(len(blocked_rules)),
            "endpoint_ready_coupling_rule_count": "0",
            "endpoint_replay_allowed": "false",
            "endpoint_validation_claimed": "false",
            "contains_endpoint_scores": "false",
            "contains_distance_residuals": "false",
            "contains_fit_statistics": "false",
            "verdict": "multichannel_coupling_accounted_but_endpoint_blocked",
            "recommended_next_action": "freeze_path_and_time_values_then_build_family_balanced_coupling_controls",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(OUT, rows)
    write_csv(SUMMARY, summary)
    print(
        "PAPER10_V2_MULTICHANNEL_COUPLING_LEDGER_BUILT "
        f"rules={len(rows)} endpoint_ready=0 endpoint_replay_allowed=false"
    )


if __name__ == "__main__":
    main()

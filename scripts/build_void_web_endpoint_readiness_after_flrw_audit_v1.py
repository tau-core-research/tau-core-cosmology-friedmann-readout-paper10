#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "void_web_endpoint_readiness_after_flrw_audit_policy_v1.csv"
FLRW = ROOT / "data" / "source_manifest" / "cosmology_flrw_consistency_channel_audit_v1.csv"
PANTHEON = ROOT / "data" / "derived" / "pantheon_void_web_source_native_full_cov_pilot_v1_summary.csv"
GROWTH = ROOT / "data" / "derived" / "growth_web_source_native_pilot_v1_summary.csv"
SDSS = ROOT / "data" / "derived" / "sdss_multitracer_bao_rsd_full_cov_pilot_v1_summary.csv"
CMB = ROOT / "data" / "derived" / "cmb_safety_lowz_support_v1_summary.csv"
OUT = ROOT / "data" / "derived" / "void_web_endpoint_readiness_after_flrw_audit_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "void_web_endpoint_readiness_after_flrw_audit_v1_summary.csv"


def first_row(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def channel_axes(channel_id: str, flrw_rows: list[dict[str, str]]) -> str:
    for row in flrw_rows:
        if row["channel_id"] == channel_id:
            axes = [row["primary_flrw_consistency_axis"]]
            axes.extend(
                axis.strip()
                for axis in row["secondary_flrw_consistency_axes"].split(";")
                if axis.strip()
            )
            return ";".join(dict.fromkeys(axes))
    raise SystemExit(f"missing FLRW audit row for {channel_id}")


def main() -> None:
    policy = first_row(POLICY)
    flrw_rows = rows(FLRW)
    pantheon = first_row(PANTHEON)
    growth = first_row(GROWTH)
    sdss = first_row(SDSS)
    cmb = first_row(CMB)

    if policy["endpoint_scoring_allowed"].lower() != "false":
        raise SystemExit("policy must keep endpoint scoring disabled")
    if policy["physical_validation_claimed"].lower() != "false":
        raise SystemExit("policy must not claim physical validation")

    void_axes = channel_axes("W_VOID_MATURITY", flrw_rows)
    web_axes = channel_axes("W_WEB_ANISOTROPY", flrw_rows)

    ledger = [
        {
            "policy_id": policy["policy_id"],
            "component_id": "pantheon_distance_void_web_full_cov",
            "source_artifact": "pantheon_void_web_source_native_full_cov_pilot_v1_summary.csv",
            "active_channels": pantheon["active_channels"],
            "flrw_consistency_axes": ";".join(dict.fromkeys(void_axes.split(";") + web_axes.split(";"))),
            "pilot_status": pantheon["status"],
            "delta_chi2": pantheon["delta_chi2_source_native_void_web_minus_baseline"],
            "delta_aic": pantheon["delta_aic_source_native_void_web_minus_baseline"],
            "primary_control_result": "deterministic_shuffled_control_can_improve_chi2",
            "readiness_status": "PILOT_SIGNAL_NOT_ENDPOINT_READY",
            "endpoint_blocker": "aic_loss_and_shuffled_control_not_beaten",
            "endpoint_scoring_allowed": "false",
            "physical_validation_claimed": "false",
        },
        {
            "policy_id": policy["policy_id"],
            "component_id": "sdss_growth_web_diagonal_summary",
            "source_artifact": "growth_web_source_native_pilot_v1_summary.csv",
            "active_channels": growth["active_channels"],
            "flrw_consistency_axes": web_axes,
            "pilot_status": growth["status"],
            "delta_chi2": growth["delta_chi2_web_minus_baseline"],
            "delta_aic": growth["delta_aic_web_minus_baseline"],
            "primary_control_result": "wrong_sign_control_equally_good_on_symmetric_grid",
            "readiness_status": "GROWTH_STRESS_TEST_NOT_ENDPOINT_READY",
            "endpoint_blocker": "diagonal_covariance_and_wrong_sign_degeneracy",
            "endpoint_scoring_allowed": "false",
            "physical_validation_claimed": "false",
        },
        {
            "policy_id": policy["policy_id"],
            "component_id": "sdss_multitracer_web_full_cov",
            "source_artifact": "sdss_multitracer_bao_rsd_full_cov_pilot_v1_summary.csv",
            "active_channels": sdss["active_channels"],
            "flrw_consistency_axes": web_axes,
            "pilot_status": sdss["status"],
            "delta_chi2": sdss["delta_chi2_web_minus_baseline"],
            "delta_aic": sdss["delta_aic_web_minus_baseline"],
            "primary_control_result": "wrong_sign_control_equally_good_full_covariance",
            "readiness_status": "SEMI_NEGATIVE_CONTROL_NOT_ENDPOINT_READY",
            "endpoint_blocker": "near_zero_signal_and_wrong_sign_degeneracy",
            "endpoint_scoring_allowed": "false",
            "physical_validation_claimed": "false",
        },
        {
            "policy_id": policy["policy_id"],
            "component_id": "cmb_lowz_safety_support",
            "source_artifact": "cmb_safety_lowz_support_v1_summary.csv",
            "active_channels": "W_VOID_MATURITY;W_WEB_ANISOTROPY",
            "flrw_consistency_axes": "cmb_safety;late_time_support",
            "pilot_status": cmb["status"],
            "delta_chi2": "NA",
            "delta_aic": "NA",
            "primary_control_result": "late_time_support_zero_above_safety_floor",
            "readiness_status": "SAFETY_SUPPORT_PASS_NOT_ENDPOINT_SCORE",
            "endpoint_blocker": "not_a_likelihood_and_contains_no_cmb_map_data",
            "endpoint_scoring_allowed": "false",
            "physical_validation_claimed": "false",
        },
    ]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(ledger[0]))
        writer.writeheader()
        writer.writerows(ledger)

    endpoint_ready = [
        row
        for row in ledger
        if row["readiness_status"] == "ENDPOINT_READY_FOR_COMBINED_SCORING"
    ]
    support_ready = [
        row
        for row in ledger
        if row["readiness_status"] == "SAFETY_SUPPORT_PASS_NOT_ENDPOINT_SCORE"
    ]
    summary = {
        "policy_id": policy["policy_id"],
        "status": "VOID_WEB_ENDPOINT_READINESS_AFTER_FLRW_AUDIT_BUILT_NOT_SCORED",
        "component_count": str(len(ledger)),
        "endpoint_ready_count": str(len(endpoint_ready)),
        "support_ready_count": str(len(support_ready)),
        "blocking_component_count": str(len(ledger) - len(endpoint_ready)),
        "first_blocker": ledger[0]["endpoint_blocker"],
        "endpoint_scoring_allowed": "false",
        "physical_validation_claimed": "false",
        "next_required_gate": "predeclared_combined_multiblock_endpoint_protocol_with_joint_nulls_and_unified_information_criterion",
        "claim_boundary": policy["claim_boundary"],
    }
    with SUMMARY.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary))
        writer.writeheader()
        writer.writerow(summary)
    print(
        "PAPER10_VOID_WEB_ENDPOINT_READINESS_AFTER_FLRW_AUDIT_V1_BUILT "
        f"components={summary['component_count']} endpoint_ready={summary['endpoint_ready_count']}"
    )


if __name__ == "__main__":
    main()

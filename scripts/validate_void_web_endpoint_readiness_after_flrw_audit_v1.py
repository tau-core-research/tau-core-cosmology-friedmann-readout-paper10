#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "void_web_endpoint_readiness_after_flrw_audit_policy_v1.csv"
LEDGER = ROOT / "data" / "derived" / "void_web_endpoint_readiness_after_flrw_audit_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "void_web_endpoint_readiness_after_flrw_audit_v1_summary.csv"

EXPECTED_COMPONENTS = {
    "pantheon_distance_void_web_full_cov",
    "sdss_growth_web_diagonal_summary",
    "sdss_multitracer_web_full_cov",
    "cmb_lowz_safety_support",
}
EXPECTED_STATUSES = {
    "PILOT_SIGNAL_NOT_ENDPOINT_READY",
    "GROWTH_STRESS_TEST_NOT_ENDPOINT_READY",
    "SEMI_NEGATIVE_CONTROL_NOT_ENDPOINT_READY",
    "SAFETY_SUPPORT_PASS_NOT_ENDPOINT_SCORE",
}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    policy_rows = read_rows(POLICY)
    ledger_rows = read_rows(LEDGER)
    summary_rows = read_rows(SUMMARY)
    if len(policy_rows) != 1:
        raise SystemExit("policy must contain exactly one row")
    if len(ledger_rows) != 4:
        raise SystemExit("ledger must contain exactly four components")
    if len(summary_rows) != 1:
        raise SystemExit("summary must contain exactly one row")
    policy = policy_rows[0]
    summary = summary_rows[0]

    if policy["status"] != "VOID_WEB_ENDPOINT_READINESS_AFTER_FLRW_AUDIT_POLICY_FROZEN_NOT_SCORED":
        raise SystemExit("unexpected policy status")
    if policy["endpoint_scoring_allowed"] != "false":
        raise SystemExit("policy must keep endpoint scoring disabled")
    if policy["physical_validation_claimed"] != "false":
        raise SystemExit("policy must not claim physical validation")
    for marker in [
        "posthoc_channel_promotion",
        "distance_residual_driven_activation",
        "growth_residual_driven_activation",
        "fit_improvement_driven_channel_selection",
        "posthoc_void_thresholds",
        "posthoc_environment_labels",
        "endpoint_score_claims",
    ]:
        if marker not in policy["forbidden_inputs"]:
            raise SystemExit(f"missing forbidden input marker: {marker}")

    component_ids = {row["component_id"] for row in ledger_rows}
    if component_ids != EXPECTED_COMPONENTS:
        raise SystemExit(f"unexpected components: {sorted(component_ids)}")
    statuses = {row["readiness_status"] for row in ledger_rows}
    if statuses != EXPECTED_STATUSES:
        raise SystemExit(f"unexpected readiness statuses: {sorted(statuses)}")
    for row in ledger_rows:
        if row["endpoint_scoring_allowed"] != "false":
            raise SystemExit(f"{row['component_id']}: endpoint scoring must be false")
        if row["physical_validation_claimed"] != "false":
            raise SystemExit(f"{row['component_id']}: physical validation must be false")
        if row["component_id"] != "cmb_lowz_safety_support":
            float(row["delta_chi2"])
            float(row["delta_aic"])
        if row["component_id"] == "pantheon_distance_void_web_full_cov":
            for axis in [
                "density_reconstruction",
                "single_flrw_geometry_assumption",
                "distance_optical_readout",
            ]:
                if axis not in row["flrw_consistency_axes"]:
                    raise SystemExit(f"Pantheon readiness missing FLRW axis {axis}")
        if row["component_id"].startswith("sdss"):
            if "growth_readout" not in row["flrw_consistency_axes"]:
                raise SystemExit(f"{row['component_id']}: web growth axis missing")

    if summary["status"] != "VOID_WEB_ENDPOINT_READINESS_AFTER_FLRW_AUDIT_BUILT_NOT_SCORED":
        raise SystemExit("unexpected summary status")
    if summary["component_count"] != "4":
        raise SystemExit("summary component count mismatch")
    if summary["endpoint_ready_count"] != "0":
        raise SystemExit("no endpoint-ready component should be declared")
    if summary["support_ready_count"] != "1":
        raise SystemExit("CMB safety support should be the only support-ready component")
    if summary["endpoint_scoring_allowed"] != "false":
        raise SystemExit("summary must keep endpoint scoring disabled")
    if summary["physical_validation_claimed"] != "false":
        raise SystemExit("summary must not claim physical validation")
    if "combined_multiblock_endpoint_protocol" not in summary["next_required_gate"]:
        raise SystemExit("summary must point to the combined multiblock endpoint gate")

    print(
        "PAPER10_VOID_WEB_ENDPOINT_READINESS_AFTER_FLRW_AUDIT_V1_VALIDATED "
        "endpoint_ready=0 claim_boundary=void_web_endpoint_readiness_after_flrw_audit_not_scoring"
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Validate the ACT DR6 control-suite policy."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "source_manifest" / "act_dr6_lensing_control_suite_policy_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "act_dr6_lensing_control_suite_policy_v1_summary.csv"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    rows = read_rows(MANIFEST)
    summary_rows = read_rows(SUMMARY)
    if len(summary_rows) != 1:
        raise SystemExit(f"expected one summary row, found {len(summary_rows)}")
    summary = summary_rows[0]
    expected_controls = {
        "off",
        "baseline_only",
        "curl_null",
        "diff_f150_f090_null",
        "wrong_sign",
        "deterministic_shuffle",
        "rank_reverse",
        "source_basis_recenter_stress",
    }
    if {row["control_id"] for row in rows} != expected_controls:
        raise SystemExit("unexpected ACT control suite")
    if any(row["control_channel"] != "K_null" for row in rows):
        raise SystemExit("all controls must be K_null controls")
    if not any(
        row["control_id"] == "curl_null"
        and row["current_status"] == "FROZEN_SCORED_CONTROL_VETO_ACTIVE"
        for row in rows
    ):
        raise SystemExit("curl null veto control missing")
    if not any(
        row["control_id"] == "source_basis_recenter_stress"
        and row["scored_in_current_replay"] == "false"
        and row["current_status"] == "FROZEN_REOPEN_STRESS_NOT_SCORED_IN_CURRENT_REPLAY"
        for row in rows
    ):
        raise SystemExit("source-basis recenter stress must be future-only")
    expected_summary = {
        "artifact_id": "ACT_DR6_LENSING_CONTROL_SUITE_POLICY_V1",
        "status": "CURRENT_CONTROL_SUITE_FROZEN_VALIDATION_REOPEN_STRESS_DECLARED",
        "scored_control_count": "7",
        "declared_control_count": "8",
        "missing_scored_controls": "none",
        "curl_veto_active": "true",
        "best_control_branch": "curl_null",
        "current_suite_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "family_verdict_allowed": "false",
        "physical_lensing_path_weight_claimed": "false",
        "dark_sector_inference_allowed": "false",
        "contains_distance_residuals": "false",
        "contains_fit_statistics": "false",
        "verdict": "ACT_REOPEN_07_CONTROL_SUITE_FROZEN_CURRENT_BRANCH_REPLAY_STILL_DISABLED",
    }
    for key, value in expected_summary.items():
        if summary.get(key) != value:
            raise SystemExit(f"{key}: expected {value!r}, got {summary.get(key)!r}")
    if "future reopen stress" not in summary["claim_boundary"]:
        raise SystemExit("claim boundary must keep recentering as future-only")


if __name__ == "__main__":
    main()

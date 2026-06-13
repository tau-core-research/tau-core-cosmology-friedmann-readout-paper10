#!/usr/bin/env python3
"""Validate the ACT DR6 channel-handoff policy."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "source_manifest" / "act_dr6_lensing_channel_handoff_policy_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "act_dr6_lensing_channel_handoff_policy_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"expected one row in {path}, found {len(rows)}")
    return rows[0]


def validate(row: dict[str, str]) -> None:
    expected = {
        "artifact_id": "ACT_DR6_LENSING_CHANNEL_HANDOFF_POLICY_V1",
        "status": "CHANNEL_HANDOFF_FROZEN_AS_SOURCE_DIAGNOSTIC_NOT_PHYSICAL_K_PATH",
        "candidate_tau_channel_requested": "K_path_observer_path",
        "current_tau_channel_status": "K_path_candidate_source_diagnostic_only",
        "positive_k_path_promotion_allowed": "false",
        "k_closure_handoff_allowed": "false",
        "k_null_handoff_allowed_for_curl": "true",
        "source_diagnostic_handoff_allowed": "true",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "family_verdict_allowed": "false",
        "physical_lensing_path_weight_claimed": "false",
        "dark_sector_inference_allowed": "false",
        "contains_distance_residuals": "false",
        "contains_fit_statistics": "false",
        "verdict": "ACT_REOPEN_06_CHANNEL_HANDOFF_SOURCE_DIAGNOSTIC_ONLY",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise SystemExit(f"{key}: expected {value!r}, got {row.get(key)!r}")
    if "physical units are missing" not in row["why_not_positive_k_path"]:
        raise SystemExit("missing physical-units blocker")
    if "curl_null as the best control" not in row["why_not_positive_k_path"]:
        raise SystemExit("missing curl-control veto blocker")
    if "no closure equation" not in row["why_not_k_closure"]:
        raise SystemExit("missing K_closure nonclaim")
    if "curl remains K_null control" not in row["claim_boundary"]:
        raise SystemExit("missing curl/K_null claim boundary")
    for forbidden in ["endpoint_score", "distance_residuals", "fit_statistics", "best_fit_amplitude"]:
        if forbidden not in row["forbidden_inputs"].split(","):
            raise SystemExit(f"missing forbidden input {forbidden!r}")


def main() -> None:
    manifest = read_one(MANIFEST)
    summary = read_one(SUMMARY)
    if manifest != summary:
        raise SystemExit("manifest and summary rows differ")
    validate(manifest)


if __name__ == "__main__":
    main()

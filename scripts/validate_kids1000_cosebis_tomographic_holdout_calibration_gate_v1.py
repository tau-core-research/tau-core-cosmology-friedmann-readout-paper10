#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_tomographic_holdout_calibration_gate_policy_v1.csv"
GATE = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_holdout_calibration_gate_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_tomographic_holdout_calibration_gate_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    policy = read_one(POLICY)
    rows = read_rows(GATE)
    summary = read_one(SUMMARY)

    if policy["status"] != "TOMOGRAPHIC_HOLDOUT_CALIBRATION_GATE_POLICY_FROZEN":
        raise SystemExit("unexpected holdout gate policy status")
    if policy["computes_new_scores"] != "false":
        raise SystemExit("holdout gate policy must not compute scores")
    if policy["endpoint_replay_allowed"] != "false":
        raise SystemExit("holdout gate policy must not authorize replay")
    if policy["endpoint_validation_claimed"] != "false":
        raise SystemExit("holdout gate policy must not claim validation")
    if summary["status"] != "TOMOGRAPHIC_HOLDOUT_CALIBRATION_GATE_BUILT":
        raise SystemExit("unexpected holdout gate summary status")
    if len(rows) != 6 or summary["required_steps"] != "6":
        raise SystemExit("holdout gate should contain six required steps")
    if summary["completed_steps"] != "0":
        raise SystemExit("holdout gate should not mark any required future step complete")
    if summary["requires_independent_photoz_or_tomographic_calibration"] != "true":
        raise SystemExit("independent calibration should be required")
    if summary["requires_holdout_partition_freeze"] != "true":
        raise SystemExit("holdout partition freeze should be required")
    if summary["requires_leakage_validator_before_replay"] != "true":
        raise SystemExit("leakage validator should be required before replay")
    if summary["tomographic_controls_block_validation"] != "true":
        raise SystemExit("tomographic controls should still block validation")
    if summary["endpoint_replay_allowed"] != "false":
        raise SystemExit("endpoint replay should remain blocked")
    if summary["endpoint_validation_claimed"] != "false":
        raise SystemExit("holdout gate must not claim validation")
    if summary["verdict"] != "tomographic_holdout_required_before_endpoint_replay_or_validation":
        raise SystemExit("unexpected holdout gate verdict")

    required = {
        "H0_context",
        "H1_independent_tomographic_evidence",
        "H2_holdout_partition_freeze",
        "H3_tomographic_alternative_promotion_rule",
        "H4_replay_protocol_freeze",
        "H5_authorization_gate",
    }
    if {row["step_id"] for row in rows} != required:
        raise SystemExit("holdout gate rows do not match required steps")
    for row in rows:
        if row["endpoint_replay_allowed_after_step"] != "false":
            raise SystemExit("no individual step should authorize replay in this gate")
        if "endpoint_residuals" not in row["forbidden_inputs"]:
            raise SystemExit("forbidden inputs should include endpoint residuals")
        if row["claim_boundary"] != policy["claim_boundary"]:
            raise SystemExit("claim boundary mismatch")
    if summary["claim_boundary"] != policy["claim_boundary"]:
        raise SystemExit("summary claim boundary mismatch")
    print(
        "PAPER10_KIDS1000_COSEBIS_TOMOGRAPHIC_HOLDOUT_CALIBRATION_GATE_V1_VALIDATED "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()

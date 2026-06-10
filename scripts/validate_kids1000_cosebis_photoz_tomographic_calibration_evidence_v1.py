#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_photoz_tomographic_calibration_evidence_policy_v1.csv"
LEDGER = ROOT / "data" / "derived" / "kids1000_cosebis_photoz_tomographic_calibration_evidence_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_photoz_tomographic_calibration_evidence_v1_summary.csv"


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
    rows = read_rows(LEDGER)
    summary = read_one(SUMMARY)

    if policy["status"] != "PHOTOZ_TOMOGRAPHIC_CALIBRATION_EVIDENCE_POLICY_FROZEN":
        raise SystemExit("unexpected policy status")
    if policy["computes_new_scores"] != "false" or policy["endpoint_replay_allowed"] != "false":
        raise SystemExit("policy must not score or authorize replay")
    if summary["status"] != "PHOTOZ_TOMOGRAPHIC_CALIBRATION_EVIDENCE_LEDGER_BUILT":
        raise SystemExit("unexpected summary status")
    if len(rows) != 4 or summary["evidence_rows"] != "4":
        raise SystemExit("expected four evidence rows")
    if summary["source_native_product_frozen"] != "true":
        raise SystemExit("source-native product should be frozen")
    if summary["cached_public_photoz_markers_present"] != "true":
        raise SystemExit("cached public photo-z markers should be present")
    if summary["source_native_nz_available"] != "true":
        raise SystemExit("source-native NZ should be available")
    if summary["independent_external_photoz_calibration_attached"] != "false":
        raise SystemExit("external calibration should remain unattached")
    if summary["h1_independent_evidence_complete"] != "false":
        raise SystemExit("H1 must remain incomplete")
    if summary["h2_holdout_partition_frozen"] != "true":
        raise SystemExit("H2 should already be frozen")
    if summary["endpoint_replay_allowed"] != "false" or summary["endpoint_validation_claimed"] != "false":
        raise SystemExit("summary must not authorize replay or claim validation")
    if summary["verdict"] != "partial_photoz_tomographic_evidence_available_but_h1_external_calibration_open":
        raise SystemExit("unexpected verdict")
    by_id = {row["evidence_id"]: row for row in rows}
    if by_id["E3_independent_external_calibration"]["evidence_status"] != "OPEN_REQUIRED_BEFORE_REPLAY":
        raise SystemExit("external calibration row must remain open")
    for row in rows:
        if row["endpoint_replay_allowed"] != "false" or row["endpoint_validation_claimed"] != "false":
            raise SystemExit("evidence rows must not authorize replay or validation")
        if row["claim_boundary"] != policy["claim_boundary"]:
            raise SystemExit("claim boundary mismatch")
    if summary["claim_boundary"] != policy["claim_boundary"]:
        raise SystemExit("summary claim boundary mismatch")
    print(
        "PAPER10_KIDS1000_COSEBIS_PHOTOZ_TOMOGRAPHIC_CALIBRATION_EVIDENCE_V1_VALIDATED "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_covariance_model_requirements_gate_v1.csv"
SUMMARY = ROOT / "data/derived/joint_covariance_model_requirements_gate_v1_summary.csv"
DOC = ROOT / "docs/joint_covariance_model_requirements_gate_v1.md"
CLAIM_BOUNDARY = "joint_covariance_model_requirements_gate_not_scoring_not_validation"
EXPECTED = "JOINT_COVARIANCE_MODEL_REQUIREMENTS_PARTIAL_BLOCKS_READY_CROSS_PROBE_BLOCKED"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def main() -> None:
    rows = read_rows(OUT)
    summary = read_one(SUMMARY)
    if len(rows) != 4:
        raise SystemExit("covariance gate must contain three channel rows plus one global row")
    ids = [r["channel_id"] for r in rows]
    expected_ids = [
        "kids_lensing_cosebis_low_mode",
        "observer_path_basis_low_z",
        "desi_shape_time_readout",
        "cross_probe_joint_covariance",
    ]
    if ids != expected_ids:
        raise SystemExit(f"unexpected row order: {ids}")
    for row in rows:
        if row["claim_boundary"] != CLAIM_BOUNDARY:
            raise SystemExit(f"claim boundary mismatch for {row['channel_id']}")
        for flag in ["endpoint_scoring_allowed", "endpoint_validation_claimed", "cosmological_validation_claimed"]:
            if row[flag] != "false":
                raise SystemExit(f"{flag} must remain false for {row['channel_id']}")
    if rows[0]["covariance_status"] != "source_native_full_covariance_ready":
        raise SystemExit("KiDS covariance block should be source-native ready")
    if rows[3]["covariance_status"] != "blocked":
        raise SystemExit("cross-probe covariance must remain blocked")
    if summary["verdict"] != EXPECTED:
        raise SystemExit(f"unexpected verdict: {summary['verdict']}")
    if summary["endpoint_scoring_allowed"] != "false":
        raise SystemExit("scoring must remain blocked")
    if summary["cross_probe_covariance_defined"] != "false":
        raise SystemExit("cross-probe covariance must not be declared defined")
    if int(summary["hard_blockers_open"]) < 1:
        raise SystemExit("expected open covariance blockers")
    text = DOC.read_text()
    for marker in ["not scoring", "block-diagonal", "cross-probe", EXPECTED]:
        if marker not in text:
            raise SystemExit(f"doc missing marker: {marker}")
    print(
        "JOINT_COVARIANCE_MODEL_REQUIREMENTS_GATE_V1_VALIDATED "
        f"verdict={summary['verdict']} blocks={summary['channel_covariance_blocks_available']}/{summary['channel_covariance_blocks_total']}"
    )


if __name__ == "__main__":
    main()

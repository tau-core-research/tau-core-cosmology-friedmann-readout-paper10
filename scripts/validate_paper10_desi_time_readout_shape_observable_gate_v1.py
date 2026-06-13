#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data/source_manifest/paper10_desi_time_readout_shape_observable_gate_policy_v1.csv"
OUT = ROOT / "data/derived/paper10_desi_time_readout_shape_observable_gate_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_time_readout_shape_observable_gate_v1_summary.csv"
CLAIM_BOUNDARY = "paper10_desi_time_readout_shape_observable_gate_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def one_row(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def main() -> None:
    policy = one_row(POLICY)
    rows = read_rows(OUT)
    summary = one_row(SUMMARY)
    if policy["claim_boundary"] != CLAIM_BOUNDARY or summary["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("bad time-readout shape gate claim boundary")
    if len(rows) != 7:
        raise SystemExit("shape gate must contain four first-difference and three curvature rows")
    for row in rows + [policy, summary]:
        if row["endpoint_replay_allowed"] != "false":
            raise SystemExit("shape gate must not authorize replay")
        if row["endpoint_validation_claimed"] != "false" or row["physical_validation_claimed"] != "false":
            raise SystemExit("shape gate must not claim validation")
    if summary["status"] != "DESI_TIME_READOUT_SHAPE_OBSERVABLE_GATE_BUILT_NOT_REPLAY_NOT_VALIDATION":
        raise SystemExit("bad shape gate status")
    if summary["input_cc_matched_rows"] != "5":
        raise SystemExit("shape gate must remain on the five CC-matched rows")
    if summary["high_z_row_included"] != "false":
        raise SystemExit("shape gate must not include the high-z holdout row")
    if summary["constant_beta_nuisance_removed"] != "true":
        raise SystemExit("shape gate must remove constant beta nuisance")
    if summary["first_difference_rows"] != "4" or summary["second_difference_rows"] != "3":
        raise SystemExit("bad shape row counts")
    if summary["shape_observable_candidate_available"] != "true":
        raise SystemExit("shape candidate should be available source-side")
    if summary["endpoint_ready_shape_observable"] != "false":
        raise SystemExit("shape gate must not be endpoint-ready")
    if summary["verdict"] != "desi_time_readout_shape_candidate_frozen_but_not_endpoint_ready":
        raise SystemExit("bad shape gate verdict")
    families = {row["observable_family"] for row in rows}
    if families != {"adjacent_first_difference_beta_shape", "second_difference_curvature_shape"}:
        raise SystemExit("unexpected shape observable families")
    if {row["constant_beta_nuisance_removed"] for row in rows} != {"true"}:
        raise SystemExit("all shape rows must remove constant beta nuisance")
    if {row["high_z_row_included"] for row in rows} != {"false"}:
        raise SystemExit("high-z row must remain excluded in all shape rows")
    print("paper10_desi_time_readout_shape_observable_gate_v1: OK")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_external_photoz_calibration_acquisition_plan_policy_v1.csv"
PLAN = ROOT / "data" / "derived" / "kids1000_cosebis_external_photoz_calibration_acquisition_plan_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_external_photoz_calibration_acquisition_plan_v1_summary.csv"


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
    rows = read_rows(PLAN)
    summary = read_one(SUMMARY)

    if policy["status"] != "EXTERNAL_PHOTOZ_CALIBRATION_ACQUISITION_PLAN_FROZEN_NOT_ATTACHED":
        raise SystemExit("unexpected policy status")
    if summary["status"] != "EXTERNAL_PHOTOZ_CALIBRATION_ACQUISITION_PLAN_BUILT_NOT_ATTACHED":
        raise SystemExit("unexpected summary status")
    if len(rows) != 4 or summary["required_routes"] != "4":
        raise SystemExit("expected four acquisition routes")
    if summary["attached_routes"] != "0":
        raise SystemExit("no external calibration route should be attached yet")
    if summary["leakage_review_complete"] != "false":
        raise SystemExit("leakage review must remain incomplete")
    if summary["h1_independent_evidence_complete"] != "false":
        raise SystemExit("H1 must remain open")
    if summary["h2_holdout_partition_frozen"] != "true":
        raise SystemExit("H2 should remain frozen")
    if summary["endpoint_replay_allowed"] != "false" or summary["endpoint_validation_claimed"] != "false":
        raise SystemExit("summary must not authorize replay or validation")
    if summary["verdict"] != "external_photoz_calibration_acquisition_plan_frozen_h1_still_open":
        raise SystemExit("unexpected verdict")
    route_ids = {row["route_id"] for row in rows}
    if route_ids != {
        "R1_photoz_calibration_reference_manifest",
        "R2_som_gold_or_nz_validation_manifest",
        "R3_tomographic_bin_quality_manifest",
        "R4_leakage_review_for_attached_calibration",
    }:
        raise SystemExit("unexpected acquisition route ids")
    for row in rows:
        if row["forbidden_inputs_used"] != "false":
            raise SystemExit("acquisition routes must not use forbidden inputs")
        if row["endpoint_replay_allowed"] != "false" or row["endpoint_validation_claimed"] != "false":
            raise SystemExit("acquisition routes must not authorize replay or validation")
        if row["claim_boundary"] != policy["claim_boundary"]:
            raise SystemExit("row claim boundary mismatch")
    for key in [
        "computes_new_scores",
        "uses_kids_data_vector_values_for_scoring",
        "uses_kids_data_vector_values_for_source_selection",
        "uses_residuals",
        "uses_fit_statistics",
        "endpoint_replay_allowed",
        "endpoint_validation_claimed",
    ]:
        if summary[key] != "false":
            raise SystemExit(f"summary must keep {key}=false")
    if summary["claim_boundary"] != policy["claim_boundary"]:
        raise SystemExit("summary claim boundary mismatch")
    print(
        "PAPER10_KIDS1000_COSEBIS_EXTERNAL_PHOTOZ_CALIBRATION_ACQUISITION_PLAN_V1_VALIDATED "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()

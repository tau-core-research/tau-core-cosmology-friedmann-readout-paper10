#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "data" / "source_manifest" / "kids1000_cosebis_external_photoz_calibration_source_manifest_policy_v1.csv"
MANIFEST = ROOT / "data" / "derived" / "kids1000_cosebis_external_photoz_calibration_source_manifest_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "kids1000_cosebis_external_photoz_calibration_source_manifest_v1_summary.csv"


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
    rows = read_rows(MANIFEST)
    summary = read_one(SUMMARY)

    if policy["status"] != "EXTERNAL_PHOTOZ_CALIBRATION_SOURCE_MANIFEST_POLICY_FROZEN_PENDING_REVIEW":
        raise SystemExit("unexpected policy status")
    if summary["status"] != "EXTERNAL_PHOTOZ_CALIBRATION_SOURCE_MANIFEST_BUILT_PENDING_REVIEW":
        raise SystemExit("unexpected summary status")
    if len(rows) != 3 or summary["cached_source_count"] != "3":
        raise SystemExit("expected three cached source rows")
    if summary["r1_to_r3_source_artifacts_attached"] != "true":
        raise SystemExit("R1-R3 source artifacts should be attached")
    if summary["r4_leakage_review_complete"] != "false":
        raise SystemExit("R4 leakage review must remain incomplete")
    if summary["h1_independent_evidence_complete"] != "false":
        raise SystemExit("H1 must remain incomplete before leakage review")
    if summary["endpoint_replay_allowed"] != "false" or summary["endpoint_validation_claimed"] != "false":
        raise SystemExit("summary must not authorize replay or validation")
    if summary["verdict"] != "external_photoz_calibration_sources_attached_pending_leakage_review":
        raise SystemExit("unexpected verdict")
    route_cover = {route for row in rows for route in row["route_ids"].split(";")}
    for route in [
        "R1_photoz_calibration_reference_manifest",
        "R2_som_gold_or_nz_validation_manifest",
        "R3_tomographic_bin_quality_manifest",
    ]:
        if route not in route_cover:
            raise SystemExit(f"missing route coverage: {route}")
    source_ids = {row["source_id"] for row in rows}
    if source_ids != {
        "KIDS1000_PHOTOZ_CALIBRATION_AANDA",
        "KIDS1000_PHOTOZ_CALIBRATION_ARXIV",
        "KIDS1000_SOM_GOLD_CATALOGUE",
    }:
        raise SystemExit("unexpected source ids")
    for row in rows:
        cache_path = ROOT / row["cache_path"]
        if not cache_path.exists():
            raise SystemExit(f"missing cache file: {row['cache_path']}")
        if row["all_required_markers_present"] != "true":
            raise SystemExit("all required markers must be present")
        if row["forbidden_inputs_used"] != "false":
            raise SystemExit("source manifest rows must not use forbidden inputs")
        if row["endpoint_replay_allowed"] != "false" or row["endpoint_validation_claimed"] != "false":
            raise SystemExit("source manifest rows must not authorize replay or validation")
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
        "PAPER10_KIDS1000_COSEBIS_EXTERNAL_PHOTOZ_CALIBRATION_SOURCE_MANIFEST_V1_VALIDATED "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()

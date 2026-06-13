#!/usr/bin/env python3
"""Validate the ACT DR6 observer/path source-object definition."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "source_manifest" / "act_dr6_lensing_observer_path_source_object_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "act_dr6_lensing_observer_path_source_object_v1_summary.csv"


def read_one(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"expected one row in {path}, found {len(rows)}")
    return rows[0]


def validate_row(row: dict[str, str]) -> None:
    expected = {
        "artifact_id": "ACT_DR6_LENSING_OBSERVER_PATH_SOURCE_OBJECT_V1",
        "status": "SOURCE_OBJECT_DEFINED_SOURCE_SIDE_NOT_ENDPOINT",
        "endpoint_replay_allowed": "false",
        "endpoint_validation_claimed": "false",
        "physical_lensing_path_weight_claimed": "false",
        "dark_sector_inference_allowed": "false",
        "contains_distance_residuals": "false",
        "contains_fit_statistics": "false",
        "verdict": "ACT_REOPEN_01_SOURCE_OBJECT_DEFINED_BUT_REPLAY_STILL_DISABLED",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise SystemExit(f"{key}: expected {value!r}, got {row.get(key)!r}")
    required_fragments = [
        "convergence reconstruction samples",
        "null-control samples",
        "mask coverage",
    ]
    for fragment in required_fragments:
        if fragment not in row["source_object_definition"]:
            raise SystemExit(f"source object definition missing {fragment!r}")
    forbidden = row["forbidden_inputs"].split(",")
    for field in ["distance_residuals", "fit_statistics", "endpoint_score", "control_performance"]:
        if field not in forbidden:
            raise SystemExit(f"forbidden input missing {field!r}")
    if "not a metric/lensing path integral" not in row["what_it_is_not"]:
        raise SystemExit("missing non-physical-path-integral boundary")
    if "remaining source-basis requirements" not in row["claim_boundary"]:
        raise SystemExit("claim boundary must keep remaining blockers active")


def main() -> None:
    manifest = read_one(MANIFEST)
    summary = read_one(SUMMARY)
    if manifest != summary:
        raise SystemExit("manifest and summary rows differ")
    validate_row(manifest)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_observer_orientation_kernel_v2.csv"
SUMMARY = (
    ROOT
    / "data"
    / "derived"
    / "void_source_basis_refinement_v2_observer_orientation_kernel_v2_summary.csv"
)
CLAIM_BOUNDARY = "v2_observer_orientation_kernel_v2_source_side_not_scoring"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    rows = read_rows(OUT)
    summary = read_one(SUMMARY)
    require(summary["status"] == "OBSERVER_ORIENTATION_KERNEL_V2_BUILT_NOT_SCORING", "bad summary status")
    require(summary["n_rows"] == "12", "summary row count mismatch")
    require(summary["primary_kernel"] == "W_path_times_centered_sky_z", "primary kernel mismatch")
    require(summary["reference_kernel"] == "W_path_times_raw_sky_z", "reference kernel mismatch")
    require(summary["endpoint_replay_allowed"] == "false", "summary must not authorize replay")
    require(summary["endpoint_validation_claimed"] == "false", "summary must not claim validation")
    require(summary["physical_lensing_path_weight_claimed"] == "false", "summary must not claim path physics")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    require(len(rows) == 12, "kernel must contain 12 rows")
    mean_sky_z = float(summary["mean_sky_z_scope"])
    centered_sum = 0.0
    for row in rows:
        sky_z = float(row["sky_z"])
        w_path = float(row["W_path_source_value"])
        centered = float(row["centered_sky_z"])
        centered_sum += centered
        require(abs(centered - (sky_z - mean_sky_z)) < 1e-10, "centered sky_z mismatch")
        require(
            abs(float(row["K_primary_raw_W_path_times_centered_sky_z"]) - w_path * centered) < 1e-10,
            "primary raw mismatch",
        )
        require(
            abs(float(row["K_reference_raw_W_path_times_sky_z"]) - w_path * sky_z) < 1e-10,
            "reference raw mismatch",
        )
        for key in [
            "contains_distance_residuals",
            "contains_fit_statistics",
            "endpoint_replay_allowed",
            "endpoint_validation_claimed",
            "physical_lensing_path_weight_claimed",
        ]:
            require(row[key] == "false", f"row must keep {key}=false")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
    require(abs(centered_sum) < 1e-10, "centered sky_z values must sum to zero")
    for col in ["K_primary_normalized", "K_reference_normalized", "K_axis_x_reference_normalized", "K_axis_y_reference_normalized"]:
        require(abs(max(abs(float(row[col])) for row in rows) - 1.0) < 1e-9, f"{col} not max-abs normalized")
    print(
        "PAPER10_V2_OBSERVER_ORIENTATION_KERNEL_V2_VALIDATED "
        f"n_rows={summary['n_rows']} claim_boundary={CLAIM_BOUNDARY}"
    )


if __name__ == "__main__":
    main()


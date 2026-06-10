#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_sky_z_source_audit_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "void_source_basis_refinement_v2_sky_z_source_audit_v1_summary.csv"
CLAIM_BOUNDARY = "v2_sky_z_source_audit_not_scoring_not_validation"


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
    require(summary["status"] == "V2_SKY_Z_SOURCE_AUDIT_BUILT_NOT_SCORING", "bad summary status")
    require(summary["n_rows"] == "12", "summary row count mismatch")
    require(summary["endpoint_replay_allowed"] == "false", "source audit must not authorize replay")
    require(summary["endpoint_validation_claimed"] == "false", "source audit must not claim validation")
    require(summary["physical_lensing_path_weight_claimed"] == "false", "source audit must not claim path physics")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    require(len(rows) == 12, "sky-z source audit must contain 12 rows")
    max_abs = max(abs(float(row["W_path_x_sky_z_raw"])) for row in rows)
    require(max_abs > 0.0, "raw sky-z product must have nonzero max abs")
    positives = 0
    negatives = 0
    for row in rows:
        ra = math.radians(float(row["ra_deg"]))
        dec = math.radians(float(row["dec_deg"]))
        sky_x = float(row["sky_x"])
        sky_y = float(row["sky_y"])
        sky_z = float(row["sky_z"])
        require(abs(sky_x - math.cos(dec) * math.cos(ra)) < 1e-10, "sky_x mismatch")
        require(abs(sky_y - math.cos(dec) * math.sin(ra)) < 1e-10, "sky_y mismatch")
        require(abs(sky_z - math.sin(dec)) < 1e-10, "sky_z mismatch")
        require(abs(sky_x**2 + sky_y**2 + sky_z**2 - 1.0) < 1e-10, "sky vector not unit norm")
        raw = float(row["W_path_x_sky_z_raw"])
        expected_raw = float(row["W_path_source_value"]) * sky_z
        require(abs(raw - expected_raw) < 1e-10, "raw W_path_x_sky_z mismatch")
        require(abs(float(row["W_path_x_sky_z_normalized"]) - raw / max_abs) < 1e-10, "normalized mismatch")
        require(row["contains_distance_residuals"] == "false", "row must not contain residuals")
        require(row["contains_fit_statistics"] == "false", "row must not contain fit statistics")
        require(row["endpoint_replay_allowed"] == "false", "row must not authorize replay")
        require(row["endpoint_validation_claimed"] == "false", "row must not claim validation")
        require(row["physical_lensing_path_weight_claimed"] == "false", "row must not claim path physics")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
        positives += raw > 0.0
        negatives += raw < 0.0
    require(summary["positive_raw_count"] == str(positives), "positive count mismatch")
    require(summary["negative_raw_count"] == str(negatives), "negative count mismatch")
    print(
        "PAPER10_V2_SKY_Z_SOURCE_AUDIT_V1_VALIDATED "
        f"n_rows={summary['n_rows']} claim_boundary={CLAIM_BOUNDARY}"
    )


if __name__ == "__main__":
    main()


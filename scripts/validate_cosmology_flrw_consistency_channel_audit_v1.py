#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data" / "source_manifest" / "cosmology_flrw_consistency_channel_audit_v1.csv"
CHANNELS = ROOT / "data" / "source_manifest" / "cosmology_channel_manifest_v1.csv"

REQUIRED_CHANNELS = {
    "W_VOID_MATURITY",
    "W_WEB_ANISOTROPY",
    "W_PATH_PROJECTION",
    "W_TIME_READOUT",
}
REQUIRED_AXES = {
    "distance_optical_readout",
    "expansion_time_readout",
    "density_reconstruction",
    "single_flrw_geometry_assumption",
}
REQUIRED_FORBIDDEN = {
    "distance_residuals",
    "growth_residuals",
    "lensing_residuals",
    "fit_improvement_flags",
}
REQUIRED_BASELINE_MARKERS = {
    "flrw_curvature",
    "backreaction",
    "dark_energy",
    "flrw_distance_expansion_consistency",
}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def split_semicolon(value: str) -> set[str]:
    return {part.strip() for part in value.split(";") if part.strip()}


def main() -> None:
    rows = read_rows(AUDIT)
    channel_rows = read_rows(CHANNELS)
    if len(rows) != 4:
        raise SystemExit("FLRW consistency audit must contain exactly four channel rows")

    channels = {row["channel_id"] for row in rows}
    if channels != REQUIRED_CHANNELS:
        raise SystemExit(f"unexpected channels: {sorted(channels)}")

    known_channels = {row["channel_id"] for row in channel_rows}
    unknown = channels - known_channels
    if unknown:
        raise SystemExit(f"unknown channels: {sorted(unknown)}")

    covered_axes: set[str] = set()
    all_baselines: set[str] = set()
    for row in rows:
        channel = row["channel_id"]
        if row["audit_id"] != "FLRW_CONSISTENCY_CHANNEL_AUDIT_V1":
            raise SystemExit(f"{channel}: unexpected audit id")
        if row["current_status"] != "FLRW_AXIS_DECLARED_NOT_SCORED":
            raise SystemExit(f"{channel}: status must remain non-scored")
        if row["endpoint_scoring_allowed"].lower() != "false":
            raise SystemExit(f"{channel}: endpoint scoring must remain false")
        if row["physical_validation_claimed"].lower() != "false":
            raise SystemExit(f"{channel}: physical validation must remain false")

        primary = row["primary_flrw_consistency_axis"]
        secondary = split_semicolon(row["secondary_flrw_consistency_axes"])
        if primary not in REQUIRED_AXES:
            raise SystemExit(f"{channel}: unknown primary axis {primary!r}")
        if not secondary <= REQUIRED_AXES | {"growth_readout", "lensing_readout", "distance_expansion_consistency"}:
            raise SystemExit(f"{channel}: unknown secondary axes {sorted(secondary)}")
        covered_axes.add(primary)
        covered_axes.update(axis for axis in secondary if axis in REQUIRED_AXES)

        forbidden = split_semicolon(row["forbidden_endpoint_fields"])
        missing_forbidden = REQUIRED_FORBIDDEN - forbidden
        if missing_forbidden:
            raise SystemExit(f"{channel}: missing forbidden fields {sorted(missing_forbidden)}")
        baselines = split_semicolon(row["required_baseline_or_null_controls"])
        if len(baselines) < 4:
            raise SystemExit(f"{channel}: too few baseline/null controls")
        all_baselines.update(baselines)
        note = row["notes"].lower()
        if "residual improvement" in note and "cannot be selected" not in note:
            raise SystemExit(f"{channel}: ambiguous residual-improvement wording")

    missing_axes = REQUIRED_AXES - covered_axes
    if missing_axes:
        raise SystemExit(f"missing FLRW consistency axes: {sorted(missing_axes)}")

    missing_baselines = REQUIRED_BASELINE_MARKERS - all_baselines
    if missing_baselines:
        raise SystemExit(f"missing baseline markers: {sorted(missing_baselines)}")

    print(
        "PAPER10_FLRW_CONSISTENCY_CHANNEL_AUDIT_V1_VALIDATED "
        f"rows={len(rows)} axes={len(covered_axes)} endpoint_scoring_allowed=false"
    )


if __name__ == "__main__":
    main()

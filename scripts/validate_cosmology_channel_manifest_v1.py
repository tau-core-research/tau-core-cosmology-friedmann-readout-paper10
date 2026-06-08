#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHANNEL_MANIFEST = ROOT / "data" / "source_manifest" / "cosmology_channel_manifest_v1.csv"
SOURCE_MANIFEST = ROOT / "data" / "source_manifest" / "paper10_source_freeze_manifest.csv"

REQUIRED_CHANNELS = {
    "W_VOID_MATURITY",
    "W_WEB_ANISOTROPY",
    "W_PATH_PROJECTION",
    "W_TIME_READOUT",
}

ALLOWED_FREEZE_STATUSES = {"CHANNEL_DECLARED_NOT_ENDPOINT"}
ALLOWED_RULE_STATUSES = {
    "RULE_DECLARED_NOT_NUMERIC",
    "RULE_FROZEN_NOT_ENDPOINT",
}

REQUIRED_GLOBAL_FORBIDDEN_MARKERS = {
    "distance_residuals",
    "growth_residuals",
    "lensing_residuals",
    "fit_improvement_flags",
}

CHANNEL_REQUIRED_MARKERS = {
    "W_VOID_MATURITY": {"posthoc_void_thresholds", "late_time_fit_parameters"},
    "W_WEB_ANISOTROPY": {"posthoc_environment_labels"},
    "W_PATH_PROJECTION": {"posthoc_sky_direction_selection", "posthoc_cmb_map_selection"},
    "W_TIME_READOUT": {"posthoc_hz_smoothing", "posthoc_clock_anomaly_labels"},
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def split_semicolon(value: str) -> set[str]:
    return {part.strip() for part in value.split(";") if part.strip()}


def main() -> None:
    rows = read_csv(CHANNEL_MANIFEST)
    source_rows = read_csv(SOURCE_MANIFEST)

    if not rows:
        raise SystemExit("cosmology channel manifest is empty")

    channels = {row["channel_id"] for row in rows}
    missing = REQUIRED_CHANNELS - channels
    if missing:
        raise SystemExit(f"cosmology channel manifest missing channels: {sorted(missing)}")

    forbidden_blob = ";".join(row["forbidden_endpoint_fields"] for row in rows)
    global_forbidden = split_semicolon(forbidden_blob)
    missing_global = REQUIRED_GLOBAL_FORBIDDEN_MARKERS - global_forbidden
    if missing_global:
        raise SystemExit(
            "cosmology channel manifest missing global forbidden markers: "
            f"{sorted(missing_global)}"
        )

    source_ids = {row["source_id"] for row in source_rows}

    for row in rows:
        channel = row["channel_id"]
        if row["freeze_status"] not in ALLOWED_FREEZE_STATUSES:
            raise SystemExit(f"{channel}: invalid freeze_status={row['freeze_status']}")
        if row["activation_rule_status"] not in ALLOWED_RULE_STATUSES:
            raise SystemExit(
                f"{channel}: invalid activation_rule_status={row['activation_rule_status']}"
            )
        if row["endpoint_scoring_allowed"].lower() != "false":
            raise SystemExit(f"{channel}: endpoint_scoring_allowed must remain false")
        if not row["activation_rule_id"].startswith("ACT_"):
            raise SystemExit(f"{channel}: activation_rule_id must start with ACT_")
        if not row["null_control"]:
            raise SystemExit(f"{channel}: null_control is blank")
        if not row["projection_induction_role"]:
            raise SystemExit(f"{channel}: projection_induction_role is blank")

        allowed_sources = split_semicolon(row["allowed_source_ids"])
        unknown = allowed_sources - source_ids
        if unknown:
            raise SystemExit(f"{channel}: unknown allowed_source_ids={sorted(unknown)}")

        forbidden = split_semicolon(row["forbidden_endpoint_fields"])
        if "fit_improvement_flags" not in forbidden:
            raise SystemExit(f"{channel}: missing fit_improvement_flags protection")
        missing_specific = CHANNEL_REQUIRED_MARKERS[channel] - forbidden
        if missing_specific:
            raise SystemExit(
                f"{channel}: missing channel-specific forbidden markers={sorted(missing_specific)}"
            )

        observables_blob = row["allowed_source_observables"].lower()
        if "residual" in observables_blob or "fit_improvement" in observables_blob:
            raise SystemExit(f"{channel}: allowed_source_observables contains endpoint language")

    print(
        "PAPER10_COSMOLOGY_CHANNEL_MANIFEST_V1_VALIDATED "
        f"rows={len(rows)} channels={len(channels)} endpoint_scoring_allowed=false"
    )


if __name__ == "__main__":
    main()

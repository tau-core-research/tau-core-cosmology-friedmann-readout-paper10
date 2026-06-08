#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GATE_MANIFEST = ROOT / "data" / "source_manifest" / "cosmology_source_grounding_gate_v1.csv"
CHANNEL_MANIFEST = ROOT / "data" / "source_manifest" / "cosmology_channel_manifest_v1.csv"

REQUIRED_CHANNELS = {
    "W_VOID_MATURITY",
    "W_WEB_ANISOTROPY",
    "W_PATH_PROJECTION",
    "W_TIME_READOUT",
}

REQUIRED_STATUS = "SOURCE_GROUNDING_GATE_DECLARED_NOT_DERIVED"
REQUIRED_FORBIDDEN = {
    "distance_residuals",
    "growth_residuals",
    "lensing_residuals",
    "fit_improvement_flags",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def split_semicolon(value: str) -> set[str]:
    return {part.strip() for part in value.split(";") if part.strip()}


def main() -> None:
    rows = read_csv(GATE_MANIFEST)
    channel_rows = read_csv(CHANNEL_MANIFEST)

    if not rows:
        raise SystemExit("source-grounding gate manifest is empty")

    channels = {row["channel_id"] for row in rows}
    missing = REQUIRED_CHANNELS - channels
    if missing:
        raise SystemExit(f"source-grounding gate missing channels: {sorted(missing)}")

    known_channels = {row["channel_id"] for row in channel_rows}
    unknown = channels - known_channels
    if unknown:
        raise SystemExit(f"source-grounding gate has unknown channels: {sorted(unknown)}")

    for row in rows:
        channel = row["channel_id"]
        if row["current_gate_status"] != REQUIRED_STATUS:
            raise SystemExit(f"{channel}: source-grounding status must remain {REQUIRED_STATUS}")
        if row["endpoint_scoring_allowed"].lower() != "false":
            raise SystemExit(f"{channel}: endpoint_scoring_allowed must remain false")
        if not row["required_future_artifact"].endswith(".csv"):
            raise SystemExit(f"{channel}: required_future_artifact must be a csv path")
        for field in [
            "activation_candidate",
            "quotient_survival_test",
            "closure_stability_test",
            "readout_survival_test",
            "null_control",
        ]:
            if not row[field].strip():
                raise SystemExit(f"{channel}: {field} is blank")
        forbidden = split_semicolon(row["forbidden_inputs"])
        missing_forbidden = REQUIRED_FORBIDDEN - forbidden
        if missing_forbidden:
            raise SystemExit(
                f"{channel}: missing forbidden input markers={sorted(missing_forbidden)}"
            )
        joined_gate_text = " ".join(
            row[field].lower()
            for field in [
                "activation_candidate",
                "quotient_survival_test",
                "closure_stability_test",
                "readout_survival_test",
            ]
        )
        if "residual improvement" in joined_gate_text or "best fit" in joined_gate_text:
            raise SystemExit(f"{channel}: gate text contains endpoint-tuning language")

    print(
        "PAPER10_COSMOLOGY_SOURCE_GROUNDING_GATE_V1_VALIDATED "
        f"rows={len(rows)} endpoint_scoring_allowed=false"
    )


if __name__ == "__main__":
    main()

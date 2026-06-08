#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "data" / "source_manifest" / "void_web_source_native_freeze_plan_v1.csv"
SOURCE_MANIFEST = ROOT / "data" / "source_manifest" / "paper10_source_freeze_manifest.csv"
CHANNEL_MANIFEST = ROOT / "data" / "source_manifest" / "cosmology_channel_manifest_v1.csv"

ALLOWED_STATUS = {
    "SOURCE_NATIVE_CANDIDATE_SELECTED_NOT_FETCHED",
    "SOURCE_NATIVE_PRODUCT_FETCHED_FROZEN",
    "SOURCE_NATIVE_CANDIDATE_BLOCKED",
}

REQUIRED_CHANNELS = {"W_VOID_MATURITY", "W_WEB_ANISOTROPY"}

FORBIDDEN_MARKERS = {
    "distance_residuals",
    "growth_residuals",
    "lensing_residuals",
    "fit_improvement_flags",
}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    rows = read_rows(PLAN)
    source_rows = read_rows(SOURCE_MANIFEST)
    channel_rows = read_rows(CHANNEL_MANIFEST)

    if not rows:
        raise SystemExit("void/web source-native freeze plan is empty")

    source_ids = {row["source_id"] for row in source_rows}
    channel_ids = {row["channel_id"] for row in channel_rows}
    seen_channels = {row["channel_id"] for row in rows}
    if seen_channels != REQUIRED_CHANNELS:
        raise SystemExit(f"plan must contain exactly {sorted(REQUIRED_CHANNELS)}")

    failures: list[str] = []
    for row in rows:
        candidate_id = row["candidate_id"]
        if row["channel_id"] not in channel_ids:
            failures.append(f"{candidate_id}: unknown channel_id")
        if row["source_id"] not in source_ids:
            failures.append(f"{candidate_id}: unknown source_id")
        if row["freeze_status"] not in ALLOWED_STATUS:
            failures.append(f"{candidate_id}: invalid freeze_status")
        if row["endpoint_scoring_allowed"].lower() != "false":
            failures.append(f"{candidate_id}: endpoint_scoring_allowed must remain false")
        if row["required_hash"].lower() != "sha256":
            failures.append(f"{candidate_id}: required_hash must be sha256")
        if not row["planned_local_path"].startswith("data/raw/"):
            failures.append(f"{candidate_id}: planned_local_path must be under data/raw")
        if not row["required_transform_rule"].startswith("TR_"):
            failures.append(f"{candidate_id}: missing transform rule id")
        if not row["null_control"]:
            failures.append(f"{candidate_id}: missing null controls")
        forbidden = row["endpoint_forbidden_inputs"]
        for marker in FORBIDDEN_MARKERS:
            if marker not in forbidden:
                failures.append(f"{candidate_id}: missing forbidden marker {marker}")
        if row["freeze_status"] == "SOURCE_NATIVE_PRODUCT_FETCHED_FROZEN":
            if row["exact_product_path_status"] == "EXACT_FILE_PATH_PENDING":
                failures.append(f"{candidate_id}: fetched product cannot have pending path")
            if "posthoc" in row["mask_or_selection_policy"].lower():
                failures.append(f"{candidate_id}: selection policy cannot be post-hoc")

    if failures:
        raise SystemExit("void/web source-native freeze plan failed: " + "; ".join(failures))

    print(
        "PAPER10_VOID_WEB_SOURCE_NATIVE_FREEZE_PLAN_V1_VALIDATED "
        f"rows={len(rows)} endpoint_scoring_allowed=false"
    )


if __name__ == "__main__":
    main()

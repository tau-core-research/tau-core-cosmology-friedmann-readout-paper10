#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "source_manifest" / "paper10_source_freeze_manifest.csv"

ALLOWED_STATUSES = {
    "SOURCE_SELECTED_NOT_FETCHED",
    "BLOCKED_SOURCE_SELECTION",
    "FETCHED_FROZEN",
}

REQUIRED_BLOCKS = {
    "distance",
    "void_maturity",
    "web_anisotropy",
    "growth",
    "lensing",
    "cmb_safety",
}

FORBIDDEN_MARKERS = {
    "distance_residuals",
    "growth_residuals",
    "lensing_residuals",
    "fit_improvement_flags",
    "posthoc_environment_labels",
}


def main() -> None:
    with MANIFEST.open(newline="") as f:
        rows = list(csv.DictReader(f))

    if not rows:
        raise SystemExit("source manifest is empty")

    blocks = {row["block"] for row in rows}
    missing = REQUIRED_BLOCKS - blocks
    if missing:
        raise SystemExit(f"source manifest missing blocks: {sorted(missing)}")

    for row in rows:
        source_id = row["source_id"]
        status = row["freeze_status"]
        if status not in ALLOWED_STATUSES:
            raise SystemExit(f"{source_id}: invalid freeze_status={status}")
        if not row["official_url"]:
            raise SystemExit(f"{source_id}: official_url is blank; use TBD if not selected")
        if not row["planned_local_artifact"]:
            raise SystemExit(f"{source_id}: planned_local_artifact is blank")
        forbidden = row["forbidden_endpoint_fields"]
        if not forbidden:
            raise SystemExit(f"{source_id}: forbidden_endpoint_fields is blank")
        if status == "FETCHED_FROZEN" and row["hash_status"] == "NOT_FETCHED":
            raise SystemExit(f"{source_id}: fetched source must have a hash status")

    forbidden_blob = ";".join(row["forbidden_endpoint_fields"] for row in rows)
    found_markers = {marker for marker in FORBIDDEN_MARKERS if marker in forbidden_blob}
    if len(found_markers) < 4:
        raise SystemExit(
            "source manifest does not explicitly protect enough endpoint fields"
        )

    blocked = [row["source_id"] for row in rows if row["freeze_status"] == "BLOCKED_SOURCE_SELECTION"]
    print(f"PAPER10_SOURCE_FREEZE_VALIDATED rows={len(rows)} blocked={len(blocked)}")
    if blocked:
        print("blocked_source_selection=" + ",".join(blocked))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/source_manifest/paper10_desi_time_readout_expansion_manifest_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_time_readout_expansion_manifest_v1_summary.csv"
REQUIRED_ROUTES = {
    "HIGH_Z_INDEPENDENT_CLOCK_SUPPORT",
    "MULTI_CLOCK_SUPPORT_PER_BAO_ROW",
    "TIME_READOUT_SHAPE_OBSERVABLE",
    "ORDERING_CONTROL_SUITE",
    "JOINT_COVARIANCE_AND_NUISANCE_POLICY",
}


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required manifest: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path.relative_to(ROOT)}")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    rows = read_rows(MANIFEST)
    route_ids = {row["route_id"] for row in rows}
    missing = REQUIRED_ROUTES - route_ids
    if missing:
        raise SystemExit(f"missing required expansion routes: {sorted(missing)}")
    if len(rows) != len(REQUIRED_ROUTES):
        raise SystemExit("unexpected DESI time-readout expansion row count")
    for row in rows:
        if row["endpoint_replay_allowed"] != "false":
            raise SystemExit(f"{row['route_id']} must not authorize replay")
        if row["endpoint_validation_claimed"] != "false" or row["physical_validation_claimed"] != "false":
            raise SystemExit(f"{row['route_id']} must not claim validation")
        forbidden = row["forbidden_inputs"].split(";")
        for marker in ["endpoint_scores", "validation_language"]:
            if marker not in forbidden:
                raise SystemExit(f"{row['route_id']} is missing forbidden marker {marker}")
    missing_support = sum(1 for row in rows if row["current_support_status"] == "missing")
    partial_support = sum(1 for row in rows if row["current_support_status"] == "partially_available")
    write_csv(
        SUMMARY,
        [
            {
                "manifest_id": "PAPER10_DESI_TIME_READOUT_EXPANSION_MANIFEST_V1",
                "status": "DESI_TIME_READOUT_EXPANSION_MANIFEST_VALIDATED_NOT_REPLAY_NOT_VALIDATION",
                "route_count": str(len(rows)),
                "missing_support_count": str(missing_support),
                "partial_support_count": str(partial_support),
                "endpoint_ready_route_count": "0",
                "next_primary_source_gate": "HIGH_Z_INDEPENDENT_CLOCK_SUPPORT",
                "next_parallel_source_gate": "TIME_READOUT_SHAPE_OBSERVABLE",
                "endpoint_replay_allowed": "false",
                "endpoint_validation_claimed": "false",
                "physical_validation_claimed": "false",
                "claim_boundary": "paper10_desi_time_readout_expansion_manifest_not_validation",
                "verdict": "desi_time_readout_expansion_manifest_frozen_but_no_replay_ready_route",
            }
        ],
    )
    print("paper10_desi_time_readout_expansion_manifest_v1: OK")


if __name__ == "__main__":
    main()

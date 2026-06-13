#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/observer_path_strengthening_gate_v1.csv"
SUMMARY = ROOT / "data/derived/observer_path_strengthening_gate_v1_summary.csv"
DOC = ROOT / "docs/observer_path_strengthening_gate_v1.md"
CLAIM_BOUNDARY = "observer_path_strengthening_gate_source_side_not_endpoint"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def main() -> None:
    rows = read_rows(OUT)
    summary = read_one(SUMMARY)
    if not DOC.exists():
        raise SystemExit("missing observer/path strengthening documentation")
    if len(rows) < 4:
        raise SystemExit("expected at least four gate routes")
    for row in rows:
        if row["claim_boundary"] != CLAIM_BOUNDARY:
            raise SystemExit(f"bad claim boundary for {row['route_id']}")
        if row["endpoint_validation_claimed"] != "false":
            raise SystemExit(f"endpoint validation must remain false for {row['route_id']}")
    for flag in ["endpoint_replay_allowed", "endpoint_validation_claimed", "cosmological_validation_claimed"]:
        if summary[flag] != "false":
            raise SystemExit(f"summary {flag} must remain false")
    if summary["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("summary claim boundary mismatch")
    if summary["current_family_survives_controls"] != "true":
        raise SystemExit("current observer family must survive controls for strengthening gate")
    if int(summary["metric_path_source_aligned_numeric_count"]) != 0:
        raise SystemExit("validator expects full metric path to remain blocked in this gate version")
    if "VALIDATION" in summary["verdict"] and "NOT_VALIDATION" not in summary["verdict"]:
        raise SystemExit("verdict risks validation overclaim")
    print(
        "OBSERVER_PATH_STRENGTHENING_GATE_V1_VALIDATED "
        f"verdict={summary['verdict']}"
    )


if __name__ == "__main__":
    main()

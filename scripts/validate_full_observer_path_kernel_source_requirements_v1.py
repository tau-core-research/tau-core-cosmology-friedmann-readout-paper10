#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQ = ROOT / "data/source_manifest/full_observer_path_kernel_source_requirements_v1.csv"
CLAIM_BOUNDARY = "full_observer_path_kernel_source_requirements_not_scoring_not_validation"
REQUIRED = {"R1", "R2", "R3", "R4", "R5", "R6"}


def main() -> None:
    with REQ.open(newline="") as f:
        rows = list(csv.DictReader(f))
    ids = {row["requirement_id"] for row in rows}
    if ids != REQUIRED:
        raise SystemExit(f"requirement set mismatch: {sorted(ids)}")
    for row in rows:
        if row["endpoint_replay_allowed"] != "false":
            raise SystemExit(f"{row['requirement_id']} must not authorize replay")
        if row["endpoint_validation_claimed"] != "false":
            raise SystemExit(f"{row['requirement_id']} must not claim validation")
        if row["physical_lensing_path_weight_claimed"] != "false":
            raise SystemExit(f"{row['requirement_id']} must not claim physical path weight")
        if row["claim_boundary"] != CLAIM_BOUNDARY:
            raise SystemExit(f"{row['requirement_id']} claim boundary mismatch")
        if not row["required_source_observable"] or not row["source_side_next_step"]:
            raise SystemExit(f"{row['requirement_id']} is incomplete")
    print(
        "PAPER10_FULL_OBSERVER_PATH_KERNEL_SOURCE_REQUIREMENTS_VALIDATED "
        f"requirements={len(rows)}"
    )


if __name__ == "__main__":
    main()

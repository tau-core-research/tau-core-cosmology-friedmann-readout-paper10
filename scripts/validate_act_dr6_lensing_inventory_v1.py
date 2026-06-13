#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "derived" / "act_dr6_lensing_inventory_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "act_dr6_lensing_inventory_v1_summary.csv"
CLAIM_BOUNDARY = "act_dr6_lensing_inventory_source_side_not_endpoint_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    rows = read_rows(OUT)
    summary_rows = read_rows(SUMMARY)
    if len(summary_rows) != 1:
        raise SystemExit("expected one inventory summary row")
    summary = summary_rows[0]
    if not rows:
        raise SystemExit("inventory is empty")
    if summary["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("summary claim boundary mismatch")
    if any(row["claim_boundary"] != CLAIM_BOUNDARY for row in rows):
        raise SystemExit("row claim boundary mismatch")
    for row in rows:
        if row["endpoint_replay_allowed"] != "false":
            raise SystemExit("inventory must not allow endpoint replay")
        if row["endpoint_validation_claimed"] != "false":
            raise SystemExit("inventory must not claim endpoint validation")
        if row["physical_lensing_path_weight_claimed"] != "false":
            raise SystemExit("inventory must not claim physical path weights")
    if summary["recommended_science_variant_available"] != "true":
        raise SystemExit("baseline science variant missing")
    if summary["null_control_variants_available"] != "true":
        raise SystemExit("ACT null-control variants missing")
    if int(summary["kappa_alm_products"]) < 1 or int(summary["mask_products"]) < 1:
        raise SystemExit("inventory must include at least one kappa alm and mask product")
    if summary["endpoint_replay_allowed"] != "false":
        raise SystemExit("summary must not allow endpoint replay")
    print(
        "ACT_DR6_LENSING_INVENTORY_V1_VALIDATED "
        f"rows={summary['rows']} endpoint=false"
    )


if __name__ == "__main__":
    main()

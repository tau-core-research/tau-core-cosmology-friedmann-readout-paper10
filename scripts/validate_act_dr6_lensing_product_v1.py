#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "source_manifest" / "act_dr6_lensing_product_v1.csv"
SUMMARY = ROOT / "data" / "derived" / "act_dr6_lensing_product_v1_summary.csv"
EXPECTED_BYTES = 1371472486
CLAIM_BOUNDARY = "act_dr6_lensing_source_product_acquisition_not_endpoint_not_validation"


def read_one(path: Path) -> dict[str, str]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 1:
        raise SystemExit(f"expected one row in {path.relative_to(ROOT)}")
    return rows[0]


def require_false(row: dict[str, str], key: str) -> None:
    if row.get(key) != "false":
        raise SystemExit(f"{key} must remain false in ACT DR6 acquisition manifest")


def main() -> None:
    row = read_one(MANIFEST)
    summary = read_one(SUMMARY)
    if row["claim_boundary"] != CLAIM_BOUNDARY or summary["claim_boundary"] != CLAIM_BOUNDARY:
        raise SystemExit("claim boundary mismatch")
    if int(row["expected_byte_count"]) != EXPECTED_BYTES:
        raise SystemExit("unexpected ACT expected byte count")
    if row["download_complete"] == "true":
        if int(row["local_byte_count"]) != EXPECTED_BYTES:
            raise SystemExit("download marked complete but byte count mismatch")
        if not row["sha256"]:
            raise SystemExit("complete ACT tarball must have a sha256")
        if summary["status"] != "SOURCE_PRODUCT_COMPLETE":
            raise SystemExit("summary status mismatch for complete ACT product")
    else:
        if row["metric_lensing_numeric_product_available_for_source"] != "false":
            raise SystemExit("incomplete ACT product cannot be marked metric-lensing available")
        if summary["status"] != "SOURCE_PRODUCT_INCOMPLETE_OR_MISSING":
            raise SystemExit("summary status mismatch for incomplete ACT product")
    for item in (row, summary):
        require_false(item, "endpoint_replay_allowed")
        require_false(item, "endpoint_validation_claimed")
        require_false(item, "physical_lensing_path_weight_claimed")
    print(
        "ACT_DR6_LENSING_PRODUCT_V1_VALIDATED "
        f"complete={summary['download_complete']} endpoint=false"
    )


if __name__ == "__main__":
    main()

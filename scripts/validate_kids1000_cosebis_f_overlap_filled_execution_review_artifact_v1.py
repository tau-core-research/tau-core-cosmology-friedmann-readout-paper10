#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_execution_review_schema_v1.csv"
DRY_RUN = ROOT / "data" / "derived" / "kids1000_cosebis_f_overlap_full_mask_batch_dry_run_v1.csv"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


FALSE_ONLY_COLUMNS = [
    "forbidden_inputs_used",
    "uses_kids_data_vector_values",
    "uses_posterior_chains",
    "uses_lensing_residuals",
    "uses_fit_improvement_flags",
    "uses_posthoc_tile_selection",
    "overlap_rule_computed",
    "path_mapping_computed",
    "contains_mapping_vector",
    "contains_theory_vector",
    "contains_predictions",
    "contains_residuals",
    "contains_fit_statistics",
    "endpoint_scoring_allowed",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a KiDS F_overlap filled execution-review artifact against the frozen schema."
    )
    parser.add_argument("--input", required=True, help="CSV artifact to validate.")
    parser.add_argument(
        "--mode",
        choices=["template", "filled"],
        default="filled",
        help="Use template for the committed empty template; filled for a future fetched-batch review artifact.",
    )
    parser.add_argument(
        "--require-accepted",
        action="store_true",
        help="Require every row to have review_artifact_status=accepted_source_freeze_review.",
    )
    return parser.parse_args()


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_columns(path: Path) -> list[str]:
    rows = read_rows(path)
    return [row["column_name"] for row in sorted(rows, key=lambda row: int(row["column_order"]))]


def fail(message: str) -> None:
    raise SystemExit(message)


def main() -> None:
    args = parse_args()
    input_path = Path(args.input)
    if not input_path.is_absolute():
        input_path = ROOT / input_path

    expected_columns = read_columns(SCHEMA)
    with input_path.open(newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        actual_columns = reader.fieldnames or []
    if actual_columns != expected_columns:
        fail("filled execution-review artifact columns do not match frozen schema")
    if len(rows) != 20:
        fail("execution-review artifact must contain the 20 default batch rows")

    dry_rows = read_rows(DRY_RUN)
    expected_by_tile = {row["tile_index_zero_based"]: row for row in dry_rows}
    if set(row["tile_index_zero_based"] for row in rows) != set(expected_by_tile):
        fail("execution-review artifact tile set does not match the dry-run batch")

    for row in rows:
        dry = expected_by_tile[row["tile_index_zero_based"]]
        if row["batch_id"] != dry["batch_id"] or row["batch_index_zero_based"] != dry["batch_index_zero_based"]:
            fail("execution-review artifact batch identity does not match dry-run batch")
        if row["mask_product_url"] != dry["mask_product_url"]:
            fail("execution-review artifact URL does not match dry-run URL")
        if row["expected_cache_path"] != dry["expected_cache_path"]:
            fail("execution-review artifact cache path does not match dry-run cache path")
        for key in FALSE_ONLY_COLUMNS:
            if row[key] != "false":
                fail(f"{key} must remain false")
        if args.mode == "template":
            if row["fetch_mode"] != "template_not_executed":
                fail("template rows must use fetch_mode=template_not_executed")
            if row["fetch_status"] != "template_not_fetched":
                fail("template rows must use fetch_status=template_not_fetched")
            if row["http_status"] or row["byte_count"] or row["sha256"] or row["fetched_at_utc"]:
                fail("template rows must not contain network, checksum, or timestamp outputs")
            if row["review_artifact_status"] != "template_pending_manual_execution_review":
                fail("template rows must keep pending review status")
            if row["reviewer_id_or_role"]:
                fail("template rows must not contain a reviewer role")
        else:
            if row["fetch_mode"] != "execute":
                fail("filled review rows must use fetch_mode=execute")
            if row["fetch_status"] != "fetched":
                fail("filled review rows must use fetch_status=fetched")
            if row["http_status"] != "200":
                fail("filled review rows must have http_status=200")
            try:
                byte_count = int(row["byte_count"])
            except ValueError as exc:
                raise SystemExit("filled review rows must have integer byte_count") from exc
            if byte_count <= 0:
                fail("filled review rows must have positive byte_count")
            if not SHA256_RE.match(row["sha256"]):
                fail("filled review rows must have lowercase 64-character sha256")
            if not row["fetched_at_utc"]:
                fail("filled review rows must include fetched_at_utc")
            if row["review_artifact_status"] not in {
                "accepted_source_freeze_review",
                "rejected_source_freeze_review",
                "caveated_source_freeze_review",
            }:
                fail("filled review rows must have an accepted/rejected/caveated source-freeze review status")
            if args.require_accepted and row["review_artifact_status"] != "accepted_source_freeze_review":
                fail("--require-accepted requires every row to be accepted_source_freeze_review")
            if not row["reviewer_id_or_role"]:
                fail("filled review rows must include reviewer_id_or_role")

    print(
        "PAPER10_KIDS1000_COSEBIS_F_OVERLAP_FILLED_EXECUTION_REVIEW_ARTIFACT_V1_VALIDATED "
        f"mode={args.mode} rows={len(rows)} endpoint_allowed=false"
    )


if __name__ == "__main__":
    main()

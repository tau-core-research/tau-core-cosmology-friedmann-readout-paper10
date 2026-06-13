#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROWS = ROOT / "data/derived/paper10_desi_shape_row1_confirmatory_source_attachment_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_shape_row1_confirmatory_source_attachment_v1_summary.csv"
DOC = ROOT / "docs/paper10_desi_shape_row1_confirmatory_source_attachment_v1.md"
CLAIM_BOUNDARY = "paper10_desi_shape_row1_confirmatory_source_attachment_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path.relative_to(ROOT)} must contain exactly one row")
    return rows[0]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    rows = read_rows(ROWS)
    summary = read_one(SUMMARY)
    require(len(rows) >= 2, "expected at least two Row1 confirmatory support rows")
    refs = {row["attached_source_reference"] for row in rows}
    require("Borghi et al. (2022)" in refs, "missing Borghi 2022 Row1 support")
    require("Stern et al. (2010)" in refs, "missing Stern 2010 Row1 support")
    for row in rows:
        require(row["shape_row"] == "1", "all rows must be Row1")
        require(row["support_role"] == "confirmatory_independent_in_interval_support", "bad support role")
        require(row["endpoint_replay_allowed"] == "false", "attachment rows must not authorize replay")
        require(row["endpoint_validation_claimed"] == "false", "attachment rows must not claim validation")
        require(row["physical_validation_claimed"] == "false", "attachment rows must not claim physical validation")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
    require(summary["status"] == "DESI_SHAPE_ROW1_CONFIRMATORY_SOURCE_ATTACHED_NOT_REPLAY_NOT_VALIDATION", "bad status")
    require(summary["row1_confirmatory_source_count"] == str(len(rows)), "bad support count")
    require(summary["row1_endpoint_ready"] == "false", "Row1 attachment must not create endpoint-ready status")
    require(summary["row1_promotion_ready"] == "false", "Row1 attachment must not promote route")
    require(summary["endpoint_replay_allowed"] == "false", "summary must not authorize replay")
    require(summary["endpoint_validation_claimed"] == "false", "summary must not claim endpoint validation")
    require(summary["physical_validation_claimed"] == "false", "summary must not claim physical validation")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    require(DOC.exists() and DOC.stat().st_size > 0, "missing Row1 attachment doc")
    print("PAPER10_DESI_SHAPE_ROW1_CONFIRMATORY_SOURCE_ATTACHMENT_VALIDATED")


if __name__ == "__main__":
    main()

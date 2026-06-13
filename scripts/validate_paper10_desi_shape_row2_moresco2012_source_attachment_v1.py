#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROWS = ROOT / "data/derived/paper10_desi_shape_row2_moresco2012_source_attachment_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_shape_row2_moresco2012_source_attachment_v1_summary.csv"
DOC = ROOT / "docs/paper10_desi_shape_row2_moresco2012_source_attachment_v1.md"
CLAIM_BOUNDARY = "paper10_desi_shape_row2_moresco2012_source_attachment_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    rows = read_rows(ROWS)
    summary_rows = read_rows(SUMMARY)
    require(len(rows) == 1, "row2 Moresco2012 attachment must contain exactly one row")
    require(len(summary_rows) == 1, "row2 Moresco2012 attachment summary must contain exactly one row")
    row = rows[0]
    require(row["target_id"] == "DESI_SHAPE_ROW_2_CORE_SUPPORT", "attachment must target DESI shape row2")
    require(row["shape_row"] == "2", "attachment must bind shape row 2")
    require(row["source_key"] == "Moresco2012ExpansionRate", "unexpected source key")
    require(row["source_reference"] == "Moresco et al. (2012)", "unexpected source reference")
    require(row["arxiv_id"] == "1201.3609", "unexpected arXiv id")
    require(row["doi"] == "10.1088/1475-7516/2012/08/006", "unexpected DOI")
    require(row["z"] == "1.037", "expected z=1.037 support")
    require(row["H_z_km_s_Mpc"] == "153.7", "expected H(z)=153.7")
    require(row["sigma_H_km_s_Mpc"] == "19.6736", "expected sigma_H=19.6736")
    require(row["support_type"] == "independent_in_interval_clock_support", "bad support type")
    require(row["independent_of_current_endpoint_families"] == "true", "support must be independent")
    require(row["endpoint_pair_replacement"] == "false", "must not be endpoint-pair replacement")
    require(row["row2_source_caveat_reduced"] == "true", "row2 caveat should be reduced")
    require(row["row2_endpoint_ready"] == "false", "row2 must not become endpoint-ready")
    require(row["endpoint_replay_allowed"] == "false", "attachment must not authorize replay")
    require(row["endpoint_validation_claimed"] == "false", "attachment must not claim endpoint validation")
    require(row["physical_validation_claimed"] == "false", "attachment must not claim physical validation")
    require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")

    summary = summary_rows[0]
    require(
        summary["status"] == "DESI_SHAPE_ROW2_MORESCO2012_SOURCE_ATTACHED_PARTIAL_NOT_REPLAY_NOT_VALIDATION",
        "bad summary status",
    )
    require(summary["attached_source_count"] == "1", "summary source count mismatch")
    require(summary["attached_source_key"] == "Moresco2012ExpansionRate", "summary source key mismatch")
    require(summary["row2_source_caveat_reduced"] == "true", "summary caveat flag mismatch")
    require(summary["endpoint_pair_replacement"] == "false", "summary endpoint replacement mismatch")
    require(summary["row2_endpoint_ready"] == "false", "summary endpoint-ready flag mismatch")
    require(summary["endpoint_replay_allowed"] == "false", "summary replay flag mismatch")
    require(summary["endpoint_validation_claimed"] == "false", "summary validation flag mismatch")
    require(summary["physical_validation_claimed"] == "false", "summary physical validation flag mismatch")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    require(
        summary["verdict"] == "row2_moresco2012_in_interval_support_attached_partial_not_endpoint_ready",
        "bad verdict",
    )
    require(DOC.exists() and DOC.stat().st_size > 0, "missing attachment documentation")
    print("paper10_desi_shape_row2_moresco2012_source_attachment_v1: OK")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROWS = ROOT / "data/derived/paper10_desi_shape_core_support_synthesis_gate_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_shape_core_support_synthesis_gate_v1_summary.csv"
DOC = ROOT / "docs/paper10_desi_shape_core_support_synthesis_gate_v1.md"
CLAIM_BOUNDARY = "paper10_desi_shape_core_support_synthesis_gate_not_validation"
EXPECTED_COMPONENTS = {
    "ROUTE_WIDE_REPLAY",
    "ROW_SENSITIVITY",
    "CORE_SOURCE_SUPPORT_SCAN",
    "ROW1_CONFIRMATORY_SOURCE_ATTACHMENT",
    "ROW2_CAVEAT_REDUCTION",
    "ROW2_ONLY_PERMISSION_REPLAY",
}


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
    require(len(rows) == 6, "expected six synthesis components")
    require({row["component_id"] for row in rows} == EXPECTED_COMPONENTS, "component set mismatch")
    for row in rows:
        require(row["endpoint_replay_allowed_by_this_gate"] == "false", "synthesis gate must not authorize replay")
        require(row["endpoint_validation_claimed"] == "false", "synthesis rows must not claim endpoint validation")
        require(row["physical_validation_claimed"] == "false", "synthesis rows must not claim physical validation")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
        artifact = ROOT / row["artifact"]
        require(artifact.exists(), f"component artifact does not exist: {row['artifact']}")
    require(
        summary["status"]
        in {
            "DESI_SHAPE_CORE_SUPPORT_SYNTHESIS_BUILT_SOURCE_STRENGTHENED_NOT_VALIDATION",
            "DESI_SHAPE_CORE_SUPPORT_SYNTHESIS_INCOMPLETE_NOT_VALIDATION",
        },
        "unexpected synthesis status",
    )
    require(summary["core_rows"] == "1;2", "core rows must remain rows 1 and 2")
    require(summary["most_required_row"] == "1", "Row1 should remain the most required row")
    require(summary["row1_status"].startswith("most_required_confirmatory"), "Row1 confirmatory support should be attached")
    require(summary["row2_status"].startswith("caveat_reduced"), "Row2 should be caveat-reduced")
    require(
        summary["route_interpretation"] == "multi_row_narrow_margin_source_sensitive_signal_not_row2_only",
        "route interpretation should be multi-row and not Row2-only",
    )
    require(summary["endpoint_replay_allowed_by_this_gate"] == "false", "summary must not authorize replay")
    require(summary["endpoint_validation_claimed"] == "false", "summary must not claim endpoint validation")
    require(summary["physical_validation_claimed"] == "false", "summary must not claim physical validation")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    require(summary["validation_status"] == "not_endpoint_validation_not_physical_validation_not_falsification", "bad validation status")
    require(DOC.exists() and DOC.stat().st_size > 0, "missing synthesis doc")
    print(f"PAPER10_DESI_SHAPE_CORE_SUPPORT_SYNTHESIS_GATE_VALIDATED status={summary['status']}")


if __name__ == "__main__":
    main()

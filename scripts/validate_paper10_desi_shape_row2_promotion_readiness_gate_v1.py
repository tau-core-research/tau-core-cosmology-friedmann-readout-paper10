#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROWS = ROOT / "data/derived/paper10_desi_shape_row2_promotion_readiness_gate_v1.csv"
SUMMARY = ROOT / "data/derived/paper10_desi_shape_row2_promotion_readiness_gate_v1_summary.csv"
DOC = ROOT / "docs/paper10_desi_shape_row2_promotion_readiness_gate_v1.md"
CLAIM_BOUNDARY = "paper10_desi_shape_row2_promotion_readiness_gate_not_validation"


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
    require(len(rows) == 1, "row2 promotion-readiness gate must contain exactly one row")
    require(len(summary_rows) == 1, "row2 promotion-readiness summary must contain exactly one row")
    row = rows[0]
    summary = summary_rows[0]
    require(row["shape_row"] == "2", "gate must resolve row2")
    require(row["row_sensitivity_class"] == "core_sensitive", "row2 must be core-sensitive")
    require(row["prior_source_caveat"] == "single_reference_family_pair", "prior caveat mismatch")
    require(row["moresco_caveat_reduced"] == "true", "Moresco caveat should be reduced")
    require(row["source_native_shape_caveat_reduced"] == "true", "source-native shape caveat should be reduced")
    require(row["row2_source_caveat_reduced"] == "true", "row2 source caveat should be reduced")
    require(row["endpoint_pair_replacement"] == "false", "attachment must not be endpoint-pair replacement")
    require(row["endpoint_pair_independence_satisfied"] == "false", "endpoint-pair independence must remain blocked")
    require(row["row2_endpoint_ready"] == "false", "row2 must not be endpoint-ready")
    require(row["row2_promotion_ready"] == "false", "row2 must not be promotion-ready")
    require(row["shape_route_promotion_allowed"] == "false", "shape route promotion must remain disabled")
    require(row["endpoint_replay_allowed"] == "false", "gate must not authorize replay")
    require(row["endpoint_validation_claimed"] == "false", "gate must not claim endpoint validation")
    require(row["physical_validation_claimed"] == "false", "gate must not claim physical validation")
    require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
    require(
        summary["status"] == "DESI_SHAPE_ROW2_CAVEAT_REDUCED_BUT_PROMOTION_BLOCKED_NOT_REPLAY_NOT_VALIDATION",
        "bad summary status",
    )
    require(summary["row2_source_caveat_reduced"] == "true", "summary caveat flag mismatch")
    require(summary["moresco_caveat_reduced"] == "true", "summary Moresco caveat mismatch")
    require(summary["source_native_shape_caveat_reduced"] == "true", "summary source-native caveat mismatch")
    require(summary["endpoint_pair_independence_satisfied"] == "false", "summary independence flag mismatch")
    require(summary["row2_promotion_ready"] == "false", "summary promotion-ready flag mismatch")
    require(summary["shape_route_promotion_allowed"] == "false", "summary shape route promotion mismatch")
    require(summary["endpoint_replay_allowed"] == "false", "summary replay flag mismatch")
    require(summary["endpoint_validation_claimed"] == "false", "summary validation flag mismatch")
    require(summary["physical_validation_claimed"] == "false", "summary physical validation flag mismatch")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    require(
        summary["verdict"] == "row2_combined_caveats_reduced_but_promotion_and_endpoint_pair_independence_blockers_remain",
        "bad verdict",
    )
    require(DOC.exists() and DOC.stat().st_size > 0, "missing row2 promotion-readiness documentation")
    print("paper10_desi_shape_row2_promotion_readiness_gate_v1: OK")


if __name__ == "__main__":
    main()

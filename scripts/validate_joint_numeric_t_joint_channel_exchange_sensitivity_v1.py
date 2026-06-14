#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_numeric_t_joint_channel_exchange_sensitivity_v1.csv"
SUMMARY = ROOT / "data/derived/joint_numeric_t_joint_channel_exchange_sensitivity_v1_summary.csv"
DOC = ROOT / "docs/joint_numeric_t_joint_channel_exchange_sensitivity_v1.md"
CLAIM_BOUNDARY = "joint_numeric_t_joint_channel_exchange_sensitivity_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"missing required artifact: {path.relative_to(ROOT)}")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    rows = read_rows(OUT)
    summary_rows = read_rows(SUMMARY)
    require(len(rows) == 2, "expected two channel-exchange rows")
    require(len(summary_rows) == 1, "summary must contain one row")
    summary = summary_rows[0]
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "wrong claim boundary")
    require(summary["source_routes_distinct"] == "true", "source routes must be distinct")
    require(summary["same_score_source_artifact"] == "false", "score source artifacts must differ")
    require(summary["same_control_source_artifact"] == "false", "control source artifacts must differ")
    require(float(summary["q_i_absolute_difference"]) < 0.05, "q_i difference no longer thin")
    require(float(summary["candidate_z_i_absolute_difference"]) < 0.2, "z_i difference no longer thin")
    require(summary["endpoint_validation_claimed"] == "false", "endpoint validation must remain false")
    require(summary["cosmological_validation_claimed"] == "false", "cosmological validation must remain false")
    require(summary["physical_validation_claimed"] == "false", "physical validation must remain false")
    for row in rows:
        require(row["source_distinctness_status"] == "distinct_source_route", "bad source distinctness status")
        require(row["statistic_exchange_sensitivity_status"] == "thin_margin_after_shared_standardization", "bad exchange status")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
    text = DOC.read_text()
    for marker in [CLAIM_BOUNDARY, "source-distinct", "does not strongly penalize"]:
        require(marker in text, f"doc missing marker: {marker}")
    print(
        "JOINT_NUMERIC_T_JOINT_CHANNEL_EXCHANGE_SENSITIVITY_V1_VALIDATED "
        f"zdiff={summary['candidate_z_i_absolute_difference']}"
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_matched_control_distribution_readiness_v1.csv"
SUMMARY = ROOT / "data/derived/joint_matched_control_distribution_readiness_v1_summary.csv"
DOC = ROOT / "docs/joint_matched_control_distribution_readiness_v1.md"
CLAIM_BOUNDARY = "joint_matched_control_distribution_readiness_not_scoring_not_validation"
VERDICT = "MATCHED_CONTROL_DISTRIBUTIONS_AVAILABLE_CAVEATED_NOT_ZI"


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
    rows = read_rows(OUT)
    summary = read_one(SUMMARY)
    require(len(rows) == 3, "expected three channels")
    require(summary["ready_channels"] == "1", "expected one ready channel")
    require(summary["caveated_ready_channels"] == "2", "expected two caveated-ready channels")
    require(summary["blocked_channels"] == "0", "expected no blocked channels")
    require(summary["all_channels_ready_for_numeric_zi"] == "true", "all channels should have distributions available")
    require(summary["center_scale_computable_now"] == "false", "center/scale must not be computable")
    require(summary["numeric_z_i_defined_channels"] == "0", "z_i must not be defined")
    require(summary["verdict"] == VERDICT, "unexpected verdict")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    for field in [
        "computes_numeric_statistic_now",
        "endpoint_scoring_allowed",
        "endpoint_validation_claimed",
        "cosmological_validation_claimed",
        "physical_validation_claimed",
    ]:
        require(summary[field] == "false", f"summary {field} must remain false")
    by_channel = {row["channel_id"]: row for row in rows}
    require(
        by_channel["kids_lensing_cosebis_low_mode"]["readiness_status"]
        == "CAVEATED_READY_ENDPOINT_SCORE_NOT_VALIDATION",
        "KiDS readiness mismatch",
    )
    require(
        by_channel["observer_path_basis_low_z"]["readiness_status"] == "READY_FOR_FUTURE_ZI_DISTRIBUTION_BUILD",
        "observer/path readiness mismatch",
    )
    require(
        by_channel["desi_shape_time_readout"]["readiness_status"] == "CAVEATED_READY_SMALL_N",
        "DESI readiness mismatch",
    )
    for row in rows:
        require(row["center_scale_computable_now"] == "false", "center/scale must not be computed here")
        require(row["numeric_z_i_defined"] == "false", "z_i must not be defined here")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
        for field in [
            "computes_numeric_statistic_now",
            "endpoint_scoring_allowed",
            "endpoint_validation_claimed",
            "cosmological_validation_claimed",
            "physical_validation_claimed",
        ]:
            require(row[field] == "false", f"{row['channel_id']} {field} must remain false")
    text = DOC.read_text()
    for marker in [
        "available but caveated",
        "not scoring",
        "not validation",
        "KiDS and DESI channels remain caveated",
        "does not compute centers",
        VERDICT,
        CLAIM_BOUNDARY,
    ]:
        require(marker in text, f"doc missing marker: {marker}")
    print(f"JOINT_MATCHED_CONTROL_DISTRIBUTION_READINESS_V1_VALIDATED verdict={VERDICT}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_signed_zi_standardization_protocol_v1.csv"
SUMMARY = ROOT / "data/derived/joint_signed_zi_standardization_protocol_v1_summary.csv"
DOC = ROOT / "docs/joint_signed_zi_standardization_protocol_v1.md"
CLAIM_BOUNDARY = "joint_signed_zi_standardization_protocol_not_scoring_not_validation"
VERDICT = "SIGNED_ZI_STANDARDIZATION_PROTOCOL_FROZEN_NUMERIC_ZI_BLOCKED"
EXPECTED_SIGNS = {
    "kids_lensing_cosebis_low_mode": "-1",
    "observer_path_basis_low_z": "-1",
    "desi_shape_time_readout": "+1",
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
    rows = read_rows(OUT)
    summary = read_one(SUMMARY)
    require(len(rows) == 3, "expected three channel rules")
    require(summary["active_channel_count"] == "3", "summary channel count mismatch")
    require(summary["signed_standardization_rule_frozen"] == "true", "sign rule must be frozen")
    require(summary["same_rule_for_candidate_and_controls"] == "true", "same candidate/control rule required")
    require(summary["center_rule"] == "median_of_matched_controls_only", "bad center rule")
    require(summary["scale_rule"] == "MAD1p4826_of_matched_controls_only_else_declared_blocker", "bad scale rule")
    require(summary["candidate_may_define_center_or_scale"] == "false", "candidate must not define center/scale")
    require(summary["numeric_control_distribution_required"] == "true", "control distribution requirement missing")
    require(summary["numeric_z_i_defined_channels"] == "0", "z_i must not be computed")
    require(summary["numeric_t_joint_ready"] == "false", "T_joint must remain blocked")
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
    for row in rows:
        channel = row["channel_id"]
        require(row["support_positive_sign"] == EXPECTED_SIGNS[channel], f"{channel} sign mismatch")
        require(row["same_rule_for_candidate_and_controls"] == "true", f"{channel} same-rule flag missing")
        require(row["requires_numeric_control_distribution"] == "true", f"{channel} control distribution missing")
        require(row["signed_standardization_rule_frozen"] == "true", f"{channel} sign rule not frozen")
        require(row["numeric_z_i_defined"] == "false", f"{channel} z_i must not be defined")
        require(row["numeric_z_i_value"] == "not_computed", f"{channel} z_i value must not be computed")
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "row claim boundary mismatch")
        for field in [
            "computes_numeric_statistic_now",
            "endpoint_scoring_allowed",
            "endpoint_validation_claimed",
            "cosmological_validation_claimed",
            "physical_validation_claimed",
        ]:
            require(row[field] == "false", f"{channel} {field} must remain false")
    text = DOC.read_text()
    for marker in [
        "rule frozen",
        "numeric z_i blocked",
        "matched-control distribution",
        "not scoring",
        VERDICT,
        CLAIM_BOUNDARY,
    ]:
        require(marker in text, f"doc missing marker: {marker}")
    print(f"JOINT_SIGNED_ZI_STANDARDIZATION_PROTOCOL_V1_VALIDATED verdict={VERDICT}")


if __name__ == "__main__":
    main()

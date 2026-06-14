#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/derived/joint_numeric_channel_zi_binding_audit_v1.csv"
SUMMARY = ROOT / "data/derived/joint_numeric_channel_zi_binding_audit_v1_summary.csv"
DOC = ROOT / "docs/joint_numeric_channel_zi_binding_audit_v1.md"
CLAIM_BOUNDARY = "joint_numeric_channel_zi_binding_audit_not_scoring_not_validation"
VERDICT = "NUMERIC_CHANNEL_FIELDS_PRESENT_ZI_STANDARDIZATION_BLOCKED"
EXPECTED_CHANNELS = [
    "kids_lensing_cosebis_low_mode",
    "observer_path_basis_low_z",
    "desi_shape_time_readout",
]


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
    require(len(rows) == 3, "expected three channel rows")
    require([row["channel_id"] for row in rows] == EXPECTED_CHANNELS, "unexpected channel order")
    require(summary["active_channel_count"] == "3", "summary channel count mismatch")
    require(summary["numeric_candidate_fields_present"] == "3", "expected three numeric source fields")
    require(summary["numeric_z_i_defined_channels"] == "0", "z_i must not be defined here")
    require(summary["signed_standardization_rule_frozen"] == "false", "standardization rule must remain unfrozen")
    require(summary["same_rule_for_candidate_and_controls"] == "false", "same candidate/control rule must remain unfrozen")
    require(summary["numeric_channel_binding_ready"] == "false", "channel binding must remain blocked")
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
        require(row["candidate_numeric_source"].startswith("data/derived/"), "bad source path")
        require(row["candidate_numeric_field"], "missing numeric field")
        require(row["candidate_numeric_value"], "missing numeric value")
        require(row["numeric_z_i_defined"] == "false", "row z_i must remain undefined")
        require(row["numeric_z_i_value"] == "not_computed", "row z_i value must not be computed")
        require(row["signed_standardization_rule_frozen"] == "false", "row standardization must remain unfrozen")
        require(row["same_rule_for_candidate_and_controls"] == "false", "row same-rule flag must remain false")
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
        "numeric source fields present",
        "z_i standardization blocked",
        "does not compute `z_i`",
        VERDICT,
        CLAIM_BOUNDARY,
    ]:
        require(marker in text, f"doc missing marker: {marker}")
    print(f"JOINT_NUMERIC_CHANNEL_ZI_BINDING_AUDIT_V1_VALIDATED verdict={VERDICT}")


if __name__ == "__main__":
    main()

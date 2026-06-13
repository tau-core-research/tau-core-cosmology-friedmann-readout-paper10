#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/derived/void_source_basis_refinement_v2_full_kernel_proxy_component_audit_v1.csv"
CLASS_SUMMARY = ROOT / "data/derived/void_source_basis_refinement_v2_full_kernel_proxy_component_audit_v1_class_summary.csv"
SUMMARY = ROOT / "data/derived/void_source_basis_refinement_v2_full_kernel_proxy_component_audit_v1_summary.csv"
CLAIM_BOUNDARY = "v2_full_kernel_proxy_component_audit_not_endpoint_not_validation"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    if len(rows) != 1:
        raise SystemExit(f"{path} must contain exactly one row")
    return rows[0]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    audit = read_rows(AUDIT)
    classes = read_rows(CLASS_SUMMARY)
    summary = read_one(SUMMARY)
    require(len(audit) == 17, "expected 17 full-kernel proxy families")
    require(summary["n_families"] == str(len(audit)), "summary family count mismatch")
    require(summary["base_family"] == "W_path_x_sky_x_x_zcenter", "wrong base family")
    require(summary["families_stronger_than_base"] == "0", "extra proxy should not beat base in this audit")
    require(
        summary["verdict"] == "extra_proxy_factors_do_not_outperform_base_observer_basis",
        "unexpected summary verdict",
    )
    require(summary["endpoint_replay_allowed"] == "false", "summary must not authorize replay")
    require(summary["endpoint_validation_claimed"] == "false", "summary must not claim validation")
    require(summary["physical_lensing_path_weight_claimed"] == "false", "summary must not claim path physics")
    require(summary["claim_boundary"] == CLAIM_BOUNDARY, "summary claim boundary mismatch")
    for row in audit:
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "audit claim boundary mismatch")
        require(row["endpoint_replay_allowed"] == "false", "audit must not authorize replay")
        require(row["endpoint_validation_claimed"] == "false", "audit must not claim validation")
        require(row["physical_lensing_path_weight_claimed"] == "false", "audit must not claim path physics")
        float(row["candidate_best_chi2_screen"])
        float(row["delta_chi2_candidate_minus_baseline"])
        float(row["delta_chi2_candidate_minus_base_observer_basis"])
        float(row["delta_chi2_candidate_minus_best_control"])
        float(row["vector_std"])
        int(row["unique_value_count"])
    for row in classes:
        require(row["claim_boundary"] == CLAIM_BOUNDARY, "class claim boundary mismatch")
        require(row["endpoint_replay_allowed"] == "false", "class must not authorize replay")
        require(row["endpoint_validation_claimed"] == "false", "class must not claim validation")
        require(row["physical_lensing_path_weight_claimed"] == "false", "class must not claim path physics")
        int(row["n_families"])
        int(row["surviving_family_count"])
    print(
        "PAPER10_FULL_KERNEL_PROXY_COMPONENT_AUDIT_VALIDATED "
        f"verdict={summary['verdict']} "
        f"stronger_than_base={summary['families_stronger_than_base']}"
    )


if __name__ == "__main__":
    main()
